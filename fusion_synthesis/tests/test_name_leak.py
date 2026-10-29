"""Name-leak detector, its negative controls, and fail-closed suppression (AUTH-011 §6 test 5).

CLAIM UNDER TEST. A passing leak check establishes compliance with the
IMPLEMENTED DETECTOR only. It is not a guarantee that every recognizable proper
noun, character reference or franchise reference has been excluded.

These tests must be able to fail: each leak class and each fail-closed
behaviour has a negative control that injects the defect and requires detection.
"""

import inspect
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fusion_synthesis import demo, render
from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.render import (
    LEAK_CLAIM,
    PromptBuild,
    build_prompt,
    check_text,
    find_capitalized,
    find_denylist_leaks,
    finalize,
)
from fusion_synthesis.schema import character_denylist, pair_denylist

from . import A_NAME, B_NAME, C_NAME, default_cards, synthetic_character, synthetic_pair, write_library


class DetectorTests(unittest.TestCase):
    def test_full_phrase_is_always_detected_case_insensitively(self):
        entries = [("The Marsh Cartographer", "x: name")]
        for text in ("a portrait of the marsh cartographer at dusk", "THE MARSH CARTOGRAPHER", "the, marsh-cartographer."):
            with self.subTest(text=text):
                leaks = find_denylist_leaks(text, entries, "prompt")
                self.assertEqual([l.kind for l in leaks], ["phrase"])

    def test_full_phrase_matching_is_not_weakened_by_stop_words_or_short_tokens(self):
        # An entry made only of stop words has no token-level matches, yet its phrase is still caught.
        self.assertEqual([l.kind for l in find_denylist_leaks("the of", [("The Of", "x")], "p")], ["phrase"])
        self.assertEqual(find_denylist_leaks("the sun of dawn", [("The Of", "x")], "p"), [])
        # A one-letter token is ignored individually, but the whole phrase is caught.
        self.assertEqual([l.kind for l in find_denylist_leaks("ke x brandt", [("Ke-x Brandt", "x")], "p")], ["phrase"])
        self.assertEqual(find_denylist_leaks("the x shape", [("Ke-x Brandt", "x")], "p"), [])
        self.assertEqual([l.token for l in find_denylist_leaks("brandt", [("Ke-x Brandt", "x")], "p")], ["brandt"])

    def test_stop_words_apply_to_token_matching_only(self):
        entries = [("The Marsh Cartographer", "x")]
        self.assertEqual(find_denylist_leaks("the sunset", entries, "p"), [])
        self.assertEqual([l.token for l in find_denylist_leaks("marsh lantern", entries, "p")], ["marsh"])
        self.assertEqual([l.token for l in find_denylist_leaks("a travelling cartographer", entries, "p")], ["cartographer"])

    def test_negative_controls_for_every_denylist_class(self):
        card_a, card_b = default_cards()
        tmp = tempfile.TemporaryDirectory()
        try:
            root = write_library(Path(tmp.name), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            lib = load_library(root)
            pair = lib.pairs[0]
            entries = pair_denylist(pair, lib.characters[A_NAME], lib.characters[B_NAME])
            entries.append(("Dread Citadel", "proper noun"))
            probes = {
                "parent name": f"a portrait of {A_NAME.lower()}",
                "other parent name": f"{B_NAME} in the rain",
                "property/ability name token": "a figure with a core of light",
                "property name phrase": "the quillon bound",
                "emergent ability name": "a hollow chorus rising",
                "fusion name": "marrowind weather",
                "proper noun": "standing before the dread citadel",
            }
            for label, text in probes.items():
                with self.subTest(leak_class=label):
                    self.assertTrue(find_denylist_leaks(text, entries, "prompt"), f"{label} was not detected")
            self.assertEqual(find_denylist_leaks("a quiet salt flat under a wide sky", entries, "prompt"), [])
        finally:
            tmp.cleanup()

    def test_capitalized_words_are_suspected_proper_nouns(self):
        leaks = find_capitalized("a lantern near Dunmere Hold", (), "prompt")
        self.assertEqual([l.token for l in leaks], ["Dunmere", "Hold"])
        self.assertEqual(find_capitalized("a lantern near the hold", (), "prompt"), [])

    def test_the_allowlist_can_only_skip_the_capitalization_heuristic(self):
        self.assertEqual(find_capitalized("a Baroque portrait", ("Baroque",), "prompt"), [])
        self.assertEqual(len(find_capitalized("a Baroque portrait", (), "prompt")), 1)
        # Multi-word terms cover the whole phrase, not isolated words.
        self.assertEqual(find_capitalized("an Art Nouveau poster", ("Art Nouveau",), "prompt"), [])
        self.assertEqual([l.token for l in find_capitalized("an Art Deco poster", ("Art Nouveau",), "prompt")], ["Art", "Deco"])
        # find_denylist_leaks has no allowlist parameter at all: it cannot be loosened.
        self.assertNotIn("allow", " ".join(inspect.signature(find_denylist_leaks).parameters))

    def test_allowlisted_term_does_not_hide_a_denylist_hit(self):
        entries = [("Zorblax", "x: name")]
        leaks = check_text("a Zorblax portrait", entries, ("Zorblax",), "prompt")
        self.assertEqual([l.kind for l in leaks], ["phrase"])


class AuthoredCardLeakTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()

    def final(self, pair):
        lib = self.library
        return finalize(assemble_card(lib, pair), pair, lib.characters[pair.a], lib.characters[pair.b], lib.allowlist)

    def test_every_authored_card_passes_the_implemented_detector(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = self.final(pair)
                self.assertEqual(card["leak_check"]["findings"], [])
                self.assertEqual(card["leak_check"]["status"], "PASS")
                self.assertFalse(card["image_prompt"]["suppressed"])

    def test_every_source_descriptor_is_name_free(self):
        for card in self.library.characters.values():
            entries = character_denylist(card)
            for trait in card.visual_traits:
                with self.subTest(character=card.name, slot=trait.slot):
                    self.assertEqual(check_text(trait.descriptor, entries, self.library.allowlist.terms, "source"), [])

    def test_prompt_descriptors_and_paragraph_are_each_clean(self):
        for pair in self.library.pairs:
            entries = pair_denylist(pair, self.library.characters[pair.a], self.library.characters[pair.b])
            card = self.final(pair)
            with self.subTest(pair=pair.slug):
                self.assertEqual(find_denylist_leaks(card["image_prompt"]["text"], entries, "prompt"), [])
                self.assertEqual(find_denylist_leaks(card["appearance"]["composed_paragraph"], entries, "paragraph"), [])
                for row in card["visual_provenance"]:
                    self.assertEqual(find_denylist_leaks(row["descriptor"], entries, row["slot"]), [])

    def test_pass_wording_states_the_detector_scope_not_a_guarantee(self):
        pair = self.library.pairs[0]
        out = io.StringIO()
        demo.main([pair.a, pair.b], stdout=out)
        self.assertIn("LEAK CHECK (implemented detector): PASS", out.getvalue())
        card = self.final(pair)
        self.assertEqual(card["leak_check"]["claim"], LEAK_CLAIM)
        self.assertIn("not a guarantee", LEAK_CLAIM)
        self.assertNotIn("guaranteed", out.getvalue().lower())


def leaking_library(tmp, mutate_pair=None, with_clean_second_pair=False):
    card_a, card_b = default_cards()
    pair = synthetic_pair(A_NAME, B_NAME)
    if mutate_pair:
        mutate_pair(pair)
    cards, pairs = [card_a, card_b], [pair]
    if with_clean_second_pair:
        cards.append(synthetic_character(C_NAME))
        pairs.append(synthetic_pair(C_NAME, B_NAME))
    return write_library(Path(tmp), cards, pairs)


def leak_in_setting(pair):
    pair["visual"]["setting"]["descriptor"] = f"a quiet salt flat where {A_NAME.lower()} once stood"


class FailClosedTests(unittest.TestCase):
    """A leak in the prompt, any descriptor or the paragraph suppresses the prompt in EVERY output mode."""

    def run_demo(self, root, argv):
        out, err = io.StringIO(), io.StringIO()
        code = demo.main(argv, stdout=out, stderr=err, data_dir=root)
        return code, out.getvalue(), err.getvalue()

    def test_text_mode_suppresses_the_prompt_reports_tokens_and_exits_3(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp, leak_in_setting)
            lib = load_library(root)
            full_prompt = build_prompt(lib.pairs[0]).text
            code, out, _err = self.run_demo(root, [A_NAME, B_NAME])
            self.assertEqual(code, 3)
            self.assertNotIn(full_prompt, out)
            self.assertIn("[suppressed: the leak check failed]", out)
            self.assertIn("LEAK CHECK (implemented detector): FAIL", out)
            self.assertIn("zorblax", out.lower())

    def test_json_mode_nulls_the_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp, leak_in_setting)
            code, out, _err = self.run_demo(root, [A_NAME, B_NAME, "--json"])
            self.assertEqual(code, 3)
            card = json.loads(out)
            self.assertIsNone(card["image_prompt"]["text"])
            self.assertTrue(card["image_prompt"]["suppressed"])
            self.assertEqual(card["leak_check"]["status"], "FAIL")
            self.assertTrue(any(f["token"] == "zorblax" for f in card["leak_check"]["findings"]))

    def test_prompt_mode_prints_nothing_on_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp, leak_in_setting)
            code, out, err = self.run_demo(root, [A_NAME, B_NAME, "--prompt"])
            self.assertEqual(code, 3)
            self.assertEqual(out, "")
            self.assertIn("zorblax", err)
            self.assertIn("no prompt printed", err)

    def test_all_cards_run_prints_clean_cards_but_never_the_leaking_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp, leak_in_setting, with_clean_second_pair=True)
            lib = load_library(root)
            leaking = next(p for p in lib.pairs if p.a == A_NAME)
            clean = next(p for p in lib.pairs if p.a == C_NAME)
            code, out, _err = self.run_demo(root, [])
            self.assertEqual(code, 3)
            self.assertIn(build_prompt(clean).text, out)
            self.assertNotIn(build_prompt(leaking).text, out)
            self.assertIn("2 cards, 1 leaks", out)
            code, out, _err = self.run_demo(root, ["--prompt"])
            self.assertEqual(code, 3)
            self.assertEqual(out.strip().splitlines(), [build_prompt(clean).text])

    def test_a_leak_only_in_the_paragraph_suppresses_the_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp)
            lib = load_library(root)
            pair = lib.pairs[0]
            with mock.patch.object(render, "compose_paragraph", return_value=f"A portrait of {A_NAME}."):
                card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], lib.allowlist)
            self.assertEqual(card["leak_check"]["status"], "FAIL")
            self.assertEqual({f["where"] for f in card["leak_check"]["findings"]}, {"paragraph"})
            self.assertIsNone(card["image_prompt"]["text"])

    def test_a_leak_only_in_a_descriptor_suppresses_the_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp, leak_in_setting)
            lib = load_library(root)
            pair = lib.pairs[0]
            benign = PromptBuild("benign text --ar 3:4", "benign text", "--ar 3:4", 20, 900, ())
            with mock.patch.object(render, "build_prompt", return_value=benign):
                card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], lib.allowlist)
            wheres = {f["where"] for f in card["leak_check"]["findings"]}
            self.assertIn("descriptor:setting", wheres)
            self.assertNotIn("prompt", wheres)
            self.assertIsNone(card["image_prompt"]["text"])

    def test_a_leak_only_in_the_prompt_suppresses_the_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(tmp)
            lib = load_library(root)
            pair = lib.pairs[0]
            tainted = PromptBuild(f"{A_NAME} portrait --ar 3:4", f"{A_NAME} portrait", "--ar 3:4", 25, 900, ())
            with mock.patch.object(render, "build_prompt", return_value=tainted):
                card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], lib.allowlist)
            self.assertEqual({f["where"] for f in card["leak_check"]["findings"]}, {"prompt"})
            self.assertIsNone(card["image_prompt"]["text"])

    def test_an_unallowlisted_capitalized_term_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(
                tmp, lambda p: p["visual"]["setting"].update(descriptor="a quiet salt flat near Dunmere Hold")
            )
            code, out, _err = self.run_demo(root, [A_NAME, B_NAME, "--json"])
            self.assertEqual(code, 3)
            card = json.loads(out)
            self.assertEqual({f["kind"] for f in card["leak_check"]["findings"]}, {"capitalized"})
            self.assertIsNone(card["image_prompt"]["text"])

    def test_an_allowlisted_capitalized_term_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = leaking_library(
                tmp, lambda p: p["visual"]["style"].update(descriptor="detailed Baroque character study")
            )
            code, out, _err = self.run_demo(root, [A_NAME, B_NAME, "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["leak_check"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
