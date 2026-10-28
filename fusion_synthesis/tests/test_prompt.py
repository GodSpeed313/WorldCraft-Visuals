"""The descriptor-only image prompt and its length ceiling (AUTH-011 §6 test 4)."""

import io
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis import demo
from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.render import (
    DEFAULT_PROMPT_MAX_CHARS,
    PromptTooLongError,
    build_prompt,
    finalize,
)
from fusion_synthesis.schema import SCENE_FIELDS, SLOTS, SchemaError

from . import A_NAME, B_NAME, default_cards, deep, synthetic_pair, write_library


def synthetic_library(mutate_pair=None):
    card_a, card_b = default_cards()
    pair = synthetic_pair(A_NAME, B_NAME)
    if mutate_pair:
        mutate_pair(pair)
    tmp = tempfile.TemporaryDirectory()
    try:
        root = write_library(Path(tmp.name), [card_a, card_b], [pair])
        return tmp, load_library(root)
    except Exception:
        tmp.cleanup()
        raise


def expected_prompt(pair):
    parts = [pair.visual.subject.descriptor]
    parts += [dict(pair.visual.slots)[s].descriptor for s in SLOTS]
    parts += [dict(pair.visual.scene)[f].descriptor for f in SCENE_FIELDS]
    return ", ".join(parts) + " " + pair.visual.parameters


class PromptShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()

    def test_order_is_subject_slots_scene_then_parameters(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                self.assertEqual(build_prompt(pair).text, expected_prompt(pair))
                self.assertEqual(
                    [label for label, _ in build_prompt(pair).components],
                    ["subject", *SLOTS, *SCENE_FIELDS],
                )

    def test_every_descriptor_survives_verbatim_and_nothing_is_truncated(self):
        for pair in self.library.pairs:
            built = build_prompt(pair)
            for label, descriptor in built.components:
                with self.subTest(pair=pair.slug, component=label):
                    self.assertIn(descriptor, built.text)
            self.assertTrue(built.text.endswith(pair.visual.parameters))

    def test_card_reports_length_ceiling_and_the_component_order(self):
        for pair in self.library.pairs:
            card = finalize(
                assemble_card(self.library, pair), pair,
                self.library.characters[pair.a], self.library.characters[pair.b], self.library.allowlist,
            )
            ip = card["image_prompt"]
            self.assertEqual(ip["length"], len(ip["text"]))
            self.assertLessEqual(ip["length"], ip["ceiling"])
            self.assertEqual(ip["order"], ["subject", *SLOTS, *SCENE_FIELDS, "parameters"])

    def test_there_is_exactly_one_prompt_format(self):
        pair = self.library.pairs[0]
        card = finalize(
            assemble_card(self.library, pair), pair,
            self.library.characters[pair.a], self.library.characters[pair.b], self.library.allowlist,
        )
        self.assertEqual([k for k in card if "prompt" in k.lower()], ["image_prompt"])
        self.assertEqual([k for k in card["image_prompt"] if k not in ("text", "suppressed", "order", "length", "ceiling")], [])
        out = io.StringIO()
        demo.main([pair.a, pair.b], stdout=out)
        self.assertEqual(out.getvalue().count("IMAGE PROMPT"), 1)


class DescriptorOnlyTests(unittest.TestCase):
    def test_prompt_depends_only_on_descriptors_and_parameters(self):
        """Changing every non-descriptor authored field must not change the prompt."""
        def scramble(p):
            p["concept"] = "A different concept sentence entirely."
            p["interaction"]["description"] = "A different rule description."
            p["emergent_ability"]["description"] = "A different ability description."
            p["emergent_ability"]["limitations"] = ["A different limitation."]
            p["trait_outcomes"][0]["result_text"] = "Different text."
            p["exclusions"] = []
            for slot in ("hair", "clothing"):
                p["visual"]["slots"][slot]["design_delta"]["from"] = "a different starting point"

        tmp1, lib1 = synthetic_library()
        tmp2, lib2 = synthetic_library(scramble)
        try:
            self.assertEqual(build_prompt(lib1.pairs[0]).text, build_prompt(lib2.pairs[0]).text)
        finally:
            tmp1.cleanup(), tmp2.cleanup()

    def test_parent_names_are_in_provenance_but_not_in_the_prompt(self):
        tmp, lib = synthetic_library()
        try:
            pair = lib.pairs[0]
            card = finalize(assemble_card(lib, pair), pair, lib.characters[pair.a], lib.characters[pair.b], lib.allowlist)
            prompt = card["image_prompt"]["text"].lower()
            self.assertNotIn(A_NAME.lower(), prompt)
            self.assertNotIn(B_NAME.lower(), prompt)
            self.assertTrue(any(A_NAME in p["character"] for r in card["visual_provenance"] for p in r["parents"]))
        finally:
            tmp.cleanup()


class CeilingTests(unittest.TestCase):
    def test_default_ceiling_is_900_and_documented_as_a_convention(self):
        self.assertEqual(DEFAULT_PROMPT_MAX_CHARS, 900)
        source = (Path(__file__).parents[1] / "render.py").read_text(encoding="utf-8")
        self.assertIn("project convention", source)

    def test_exactly_at_the_ceiling_passes_and_one_over_fails_clearly(self):
        tmp, lib = synthetic_library()
        length = len(build_prompt(lib.pairs[0]).text)
        tmp.cleanup()
        self.assertGreaterEqual(length - 1, 200, "synthetic prompt must be long enough to test the boundary")

        tmp, lib = synthetic_library(lambda p: p.update(prompt_max_chars=length))
        try:
            self.assertEqual(build_prompt(lib.pairs[0]).length, length)
        finally:
            tmp.cleanup()

        tmp, lib = synthetic_library(lambda p: p.update(prompt_max_chars=length - 1))
        try:
            with self.assertRaises(PromptTooLongError) as ctx:
                build_prompt(lib.pairs[0])
            message = str(ctx.exception)
            self.assertIn(str(length), message)
            self.assertIn(str(length - 1), message)
            self.assertIn("component lengths", message)
            self.assertIn("nothing is truncated", message)
        finally:
            tmp.cleanup()

    def test_override_within_range_is_honoured(self):
        tmp, lib = synthetic_library(lambda p: p.update(prompt_max_chars=2000))
        try:
            self.assertEqual(build_prompt(lib.pairs[0]).ceiling, 2000)
        finally:
            tmp.cleanup()

    def test_out_of_range_overrides_are_rejected(self):
        for bad in (0, 199, 2001, "900", 900.5, True):
            with self.subTest(value=bad):
                with self.assertRaises(SchemaError):
                    synthetic_library(lambda p: p.update(prompt_max_chars=bad))

    def test_demo_reports_an_over_ceiling_prompt_as_exit_2_with_no_prompt(self):
        tmp, lib = synthetic_library()
        length = len(build_prompt(lib.pairs[0]).text)
        tmp.cleanup()
        card_a, card_b = default_cards()
        pair = synthetic_pair(A_NAME, B_NAME)
        pair["prompt_max_chars"] = length - 1
        with tempfile.TemporaryDirectory() as t:
            root = write_library(Path(t), [card_a, card_b], [pair])
            out, err = io.StringIO(), io.StringIO()
            code = demo.main([], stdout=out, stderr=err, data_dir=root)
            self.assertEqual(code, 2)
            self.assertEqual(out.getvalue(), "")
            self.assertIn("over its ceiling", err.getvalue())


if __name__ == "__main__":
    unittest.main()
