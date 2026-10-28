"""The demo command: variants, output sections and exit codes (AUTH-011 §4, §6 test 9)."""

import io
import json
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis import demo
from fusion_synthesis.loader import load_library

from . import A_NAME, B_NAME, default_cards, synthetic_pair, write_library

SECTION_ORDER = [
    "CONCEPT", "APPEARANCE", "VISUAL PROVENANCE", "TRAITS", "EMERGENT ABILITY",
    "EXCLUSIONS", "COMPATIBILITY", "ANCESTRY", "IMAGE PROMPT", "LEAK CHECK (implemented detector):",
]


def run(argv, data_dir=None):
    out, err = io.StringIO(), io.StringIO()
    code = demo.main(argv, stdout=out, stderr=err, data_dir=data_dir)
    return code, out.getvalue(), err.getvalue()


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.pair = cls.library.pairs[0]

    def test_all_pairs_run_lists_every_card_and_a_summary(self):
        code, out, err = run([])
        self.assertEqual((code, err), (0, ""))
        for pair in self.library.pairs:
            self.assertIn(f"({pair.a} x {pair.b})", out)
        n = len(self.library.pairs)
        self.assertTrue(out.rstrip().endswith(f"{n} cards, 0 leaks"))

    def test_one_card_has_every_section_in_order_and_no_summary(self):
        code, out, _ = run([self.pair.a, self.pair.b])
        self.assertEqual(code, 0)
        positions = [out.index(section) for section in SECTION_ORDER]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("cards,", out)
        self.assertIn("dominance: 50/50 (fixed in Phase 1; not applied as a weighting)", out)

    def test_json_variants(self):
        code, out, _ = run([self.pair.a, self.pair.b, "--json"])
        self.assertEqual(code, 0)
        card = json.loads(out)
        self.assertEqual(card["fusion_name"], self.pair.fusion_name)
        code, out, _ = run(["--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), len(self.library.pairs))

    def test_prompt_variant_prints_only_the_prompt_line(self):
        code, out, _ = run([self.pair.a, self.pair.b, "--prompt"])
        card = json.loads(run([self.pair.a, self.pair.b, "--json"])[1])
        self.assertEqual(code, 0)
        self.assertEqual(out, card["image_prompt"]["text"] + "\n")
        self.assertEqual(out.count("\n"), 1)

    def test_unknown_pair_is_exit_2_and_lists_the_authored_pairs(self):
        code, out, err = run(["Nobody", "Nowhere"])
        self.assertEqual((code, out), (2, ""))
        self.assertIn("no authored pair", err)
        self.assertIn(f"{self.pair.a} x {self.pair.b}", err)

    def test_pair_order_is_exact(self):
        code, out, err = run([self.pair.b, self.pair.a])
        self.assertEqual((code, out), (2, ""))

    def test_usage_errors_are_exit_2(self):
        for argv in (["--bogus"], ["OnlyOne"], ["a", "b", "c"], ["--json", "--prompt"], [self.pair.a, self.pair.b, "--xml"]):
            with self.subTest(argv=argv):
                code, out, err = run(argv)
                self.assertEqual((code, out), (2, ""))
                self.assertIn("usage", err)

    def test_invalid_data_is_exit_2_with_a_clear_message_and_no_output(self):
        card_a, card_b = default_cards()
        pair = synthetic_pair(A_NAME, B_NAME)
        pair["dominance"] = 60
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [pair])
            code, out, err = run([], root)
            self.assertEqual((code, out), (2, ""))
            self.assertIn("dominance", err)

    def test_an_empty_data_directory_with_an_allowlist_runs_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [], [])
            code, out, err = run([], root)
            self.assertEqual((code, err), (0, ""))
            self.assertIn("0 cards, 0 leaks", out)

    def test_a_missing_allowlist_is_exit_2(self):
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            (root / "style_allowlist.json").unlink()
            code, out, err = run([], root)
            self.assertEqual((code, out), (2, ""))
            self.assertIn("style_allowlist.json", err)

    def test_output_is_utf8_with_lf_endings_when_written_to_a_binary_stream(self):
        class Wrapper:
            def __init__(self):
                self.buffer = io.BytesIO()
            def flush(self):
                pass
        w = Wrapper()
        demo.main([self.pair.a, self.pair.b], stdout=w)
        data = w.buffer.getvalue()
        self.assertNotIn(b"\r", data)
        data.decode("utf-8")


if __name__ == "__main__":
    unittest.main()
