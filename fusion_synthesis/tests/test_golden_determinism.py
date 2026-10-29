"""Byte-identical determinism and operator-approved golden snapshots (AUTH-011 §6 test 7/8).

Data-driven: every pair found by glob must have a golden text and JSON
snapshot, and the demo's output must equal both exactly. A golden file is the
operator-approved rendering of its pair; changing approved content requires
re-approval, so a mismatch here is a finding, never something to silently
regenerate.
"""

import io
import json
import unittest

from fusion_synthesis import demo
from fusion_synthesis.loader import golden_paths, load_library


def run(argv):
    out = io.StringIO()
    code = demo.main(argv, stdout=out)
    return code, out.getvalue()


class GoldenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()

    def test_every_pair_has_both_golden_snapshots(self):
        for pair in self.library.pairs:
            for path in golden_paths(self.library.data_dir, pair):
                with self.subTest(pair=pair.slug, file=path.name):
                    self.assertTrue(path.is_file(), f"missing operator-approved golden snapshot {path.name}")

    def test_demo_output_equals_the_golden_text_and_json(self):
        for pair in self.library.pairs:
            txt_path, json_path = golden_paths(self.library.data_dir, pair)
            with self.subTest(pair=pair.slug):
                code, text = run([pair.a, pair.b])
                self.assertEqual(code, 0)
                self.assertEqual(text, txt_path.read_bytes().decode("utf-8"))
                code, js = run([pair.a, pair.b, "--json"])
                self.assertEqual(code, 0)
                self.assertEqual(js, json_path.read_bytes().decode("utf-8"))

    def test_golden_files_use_lf_line_endings_only(self):
        for pair in self.library.pairs:
            for path in golden_paths(self.library.data_dir, pair):
                with self.subTest(file=path.name):
                    self.assertNotIn(b"\r", path.read_bytes())

    def test_two_runs_are_byte_identical(self):
        for argv in ([], ["--json"], ["--prompt"]):
            with self.subTest(argv=argv):
                self.assertEqual(run(argv), run(argv))

    def test_the_json_golden_is_valid_and_matches_the_card_schema(self):
        for pair in self.library.pairs:
            _txt, json_path = golden_paths(self.library.data_dir, pair)
            card = json.loads(json_path.read_bytes().decode("utf-8"))
            with self.subTest(pair=pair.slug):
                self.assertEqual(card["schema"], "fusion-synthesis-card/1")
                self.assertEqual(card["leak_check"]["status"], "PASS")
                self.assertEqual(card["sources"], {"A": pair.a, "B": pair.b})


if __name__ == "__main__":
    unittest.main()
