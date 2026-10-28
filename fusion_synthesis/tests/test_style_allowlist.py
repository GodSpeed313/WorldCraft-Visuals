"""Style allowlist behaviour and denylist precedence (AUTH-011 §6 test 6).

The allowlist may skip the capitalized-word heuristic for approved generic
style terms and for nothing else. Denylist precedence is mandatory: an
allowlisted term that matches ANY denylist entry is a validation failure, and
adding a term to the allowlist can never bypass a denylist check.
"""

import json
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.render import check_text, find_capitalized, find_denylist_leaks, finalize
from fusion_synthesis.schema import (
    StyleAllowlist,
    StyleAllowlistError,
    SchemaError,
    parse_style_allowlist,
    pair_denylist,
)

from . import A_NAME, B_NAME, default_cards, synthetic_pair, write_library


def load_with_terms(terms, mutate_pair=None):
    card_a, card_b = default_cards()
    pair = synthetic_pair(A_NAME, B_NAME)
    if mutate_pair:
        mutate_pair(pair)
    with tempfile.TemporaryDirectory() as tmp:
        root = write_library(Path(tmp), [card_a, card_b], [pair], terms=terms)
        return load_library(root)


class AllowedTermsTests(unittest.TestCase):
    def test_1_an_approved_generic_style_term_can_pass_the_capitalization_heuristic(self):
        self.assertEqual(find_capitalized("a Baroque portrait", ("Baroque",), "prompt"), [])
        lib = load_with_terms(["Baroque"], lambda p: p["visual"]["style"].update(descriptor="detailed Baroque study"))
        pair = lib.pairs[0]
        card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], lib.allowlist)
        self.assertEqual(card["leak_check"]["status"], "PASS")
        self.assertIn("Baroque", card["image_prompt"]["text"])

    def test_2_a_non_allowlisted_capitalized_term_remains_subject_to_detection(self):
        self.assertEqual([l.token for l in find_capitalized("a Rococo portrait", ("Baroque",), "prompt")], ["Rococo"])
        lib = load_with_terms(["Baroque"], lambda p: p["visual"]["style"].update(descriptor="detailed Rococo study"))
        pair = lib.pairs[0]
        card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], lib.allowlist)
        self.assertEqual(card["leak_check"]["status"], "FAIL")
        self.assertIsNone(card["image_prompt"]["text"])


class DenylistPrecedenceTests(unittest.TestCase):
    def test_3_an_allowlisted_term_matching_any_denylist_entry_fails_validation(self):
        cases = {
            "parent name": "Zorblax",
            "parent name, other parent": "Quillon",
            "property-name phrase": "Zorblax Core",
            "property-name token": "Core",
            "emergent ability name": "Hollow Chorus",
            "emergent ability token": "Chorus",
            "fusion name token": "Marrowind",
            "proper noun": "Zorblax",
            "term containing a denylist token": "Gothic Zorblax",
            "case-insensitive": "zORBLAX",
        }
        for label, term in cases.items():
            with self.subTest(case=label):
                with self.assertRaises(StyleAllowlistError) as ctx:
                    load_with_terms(["Baroque", term])
                self.assertIn("cannot override the denylist", str(ctx.exception))
                self.assertIn(term, str(ctx.exception))

    def test_4_adding_a_term_cannot_bypass_the_denylist_checks(self):
        # (a) The loader refuses it (test 3). (b) Even forced past the loader, the detector still flags it.
        lib = load_with_terms(["Baroque"], lambda p: p["visual"]["setting"].update(
            descriptor=f"a quiet salt flat where {A_NAME.lower()} once stood"))
        pair = lib.pairs[0]
        forced = StyleAllowlist(terms=("Baroque", A_NAME, "Hollow Chorus", "Pell Marrowind"))
        card = finalize(assemble_card(lib, pair), pair, lib.characters[A_NAME], lib.characters[B_NAME], forced)
        self.assertEqual(card["leak_check"]["status"], "FAIL")
        self.assertIsNone(card["image_prompt"]["text"])
        self.assertTrue(any(f["kind"] in ("phrase", "token") for f in card["leak_check"]["findings"]))

        entries = pair_denylist(pair, lib.characters[A_NAME], lib.characters[B_NAME])
        for term in (A_NAME, "Hollow Chorus", "Pell Marrowind", "Core"):
            with self.subTest(term=term):
                text = f"a portrait of {term}"
                self.assertTrue(find_denylist_leaks(text, entries, "prompt"))
                self.assertTrue(check_text(text, entries, (term,), "prompt"), "allowlisting the term must not hide it")

    def test_a_capitalized_denylisted_name_is_reported_by_the_denylist_even_if_allowlisted(self):
        entries = [("Zorblax", "x: name")]
        leaks = check_text("Zorblax stands here", entries, ("Zorblax",), "prompt")
        self.assertEqual([l.kind for l in leaks], ["phrase"])


class InvalidAllowlistTests(unittest.TestCase):
    def bad(self, raw, part):
        with self.subTest(raw=raw):
            with self.assertRaises(StyleAllowlistError) as ctx:
                parse_style_allowlist(raw)
            self.assertIn(part, str(ctx.exception))

    def test_5_invalid_allowlist_data_is_rejected_with_a_clear_error(self):
        ok = {"schema": "fusion-synthesis-style-allowlist/1", "terms": ["Baroque"]}
        self.assertEqual(parse_style_allowlist(ok).terms, ("Baroque",))
        self.bad([], "expected an object")
        self.bad({"schema": "wrong/1", "terms": []}, "schema")
        self.bad({"schema": ok["schema"]}, "missing key")
        self.bad(dict(ok, extra=1), "unknown key")
        self.bad(dict(ok, terms="Baroque"), "expected a list")
        self.bad(dict(ok, terms=[3]), "terms[0]")
        self.bad(dict(ok, terms=[""]), "terms[0]")
        self.bad(dict(ok, terms=[" Baroque"]), "leading or trailing space")
        self.bad(dict(ok, terms=["Baroque "]), "leading or trailing space")
        self.bad(dict(ok, terms=["Art_Deco"]), "letters, digits, spaces and hyphens")
        self.bad(dict(ok, terms=["Baroque!"]), "letters, digits, spaces and hyphens")
        self.bad(dict(ok, terms=["x" * 41]), "1-40 characters")
        self.bad(dict(ok, terms=["Baroque", "baroque"]), "duplicate")
        self.bad(dict(ok, terms=["Art Nouveau", "art  nouveau"]), "duplicate")

    def test_an_empty_term_list_is_valid_but_a_missing_file_is_an_error(self):
        self.assertEqual(parse_style_allowlist({"schema": "fusion-synthesis-style-allowlist/1", "terms": []}).terms, ())
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            (root / "style_allowlist.json").unlink()
            with self.assertRaises(StyleAllowlistError) as ctx:
                load_library(root)
            self.assertIn("style_allowlist.json", str(ctx.exception))

    def test_invalid_allowlist_file_content_is_a_style_allowlist_error_via_the_loader(self):
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            (root / "style_allowlist.json").write_text(json.dumps({"schema": "x", "terms": []}), encoding="utf-8")
            with self.assertRaises(StyleAllowlistError):
                load_library(root)
            (root / "style_allowlist.json").write_text("{broken", encoding="utf-8")
            with self.assertRaises(StyleAllowlistError):
                load_library(root)

    def test_a_style_allowlist_error_is_a_schema_error_so_the_demo_exits_2(self):
        self.assertTrue(issubclass(StyleAllowlistError, SchemaError))

    def test_the_real_allowlist_has_no_character_specific_terms(self):
        library = load_library()
        entries = []
        for card in library.characters.values():
            entries += [(card.name, "name")] + [(p, "proper noun") for p in card.proper_nouns]
        for term in library.allowlist.terms:
            self.assertEqual(find_denylist_leaks(term, entries, "allowlist"), [], term)


if __name__ == "__main__":
    unittest.main()
