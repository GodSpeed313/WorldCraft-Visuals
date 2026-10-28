"""Schema validation and glob discovery (AUTH-011 §6 test 1)."""

import json
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis.loader import load_library
from fusion_synthesis.schema import SchemaError, slugify

from . import A_NAME, B_NAME, C_NAME, deep, default_cards, synthetic_character, synthetic_pair, write_library


def load_with(mutate_a=None, mutate_pair=None):
    """Build a synthetic library, apply mutations, load it. Returns the error text or None."""
    card_a, card_b = default_cards()
    pair = synthetic_pair(A_NAME, B_NAME)
    if mutate_a:
        mutate_a(card_a)
    if mutate_pair:
        mutate_pair(pair)
    with tempfile.TemporaryDirectory() as tmp:
        write_library(Path(tmp), [card_a, card_b], [pair])
        try:
            load_library(Path(tmp))
        except SchemaError as exc:
            return str(exc)
    return None


class ValidLibraryTests(unittest.TestCase):
    def test_valid_synthetic_library_loads(self):
        self.assertIsNone(load_with())

    def test_loader_discovers_cards_by_glob_only(self):
        card_a, card_b = default_cards()
        card_c = synthetic_character(C_NAME)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_library(root, [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            self.assertEqual(len(load_library(root).pairs), 1)
            # Add a character and a pair by writing files only; no code is touched.
            write_library(root, [card_a, card_b, card_c], [synthetic_pair(A_NAME, B_NAME), synthetic_pair(C_NAME, B_NAME)])
            library = load_library(root)
            self.assertEqual({f"{p.a}|{p.b}" for p in library.pairs}, {f"{A_NAME}|{B_NAME}", f"{C_NAME}|{B_NAME}"})
            self.assertEqual(sorted(library.characters), sorted([A_NAME, B_NAME, C_NAME]))

    def test_real_data_directory_loads(self):
        library = load_library()
        self.assertGreaterEqual(len(library.pairs), 1)


class RejectionTests(unittest.TestCase):
    """Every malformed shape is rejected with a clear message naming the problem."""

    def expect(self, label, message_part, mutate_a=None, mutate_pair=None):
        with self.subTest(case=label):
            error = load_with(mutate_a, mutate_pair)
            self.assertIsNotNone(error, f"{label}: expected a SchemaError")
            self.assertIn(message_part, error)

    def test_character_rejections(self):
        s = slugify(A_NAME)
        self.expect("wrong schema", "schema", lambda c: c.update(schema="nope/1"))
        self.expect("unknown key", "unknown key", lambda c: c.update(extra=1))
        self.expect("LEGACY epistemic status", "FICTIONAL", lambda c: c.update(epistemic_status="LEGACY"))
        self.expect("bad contribution type", "contribution_type",
                    lambda c: c["properties"][0].update(contribution_type="MAGIC"))
        self.expect("bad placement", "architectural_placement",
                    lambda c: c["properties"][0].update(architectural_placement="NOWHERE"))
        self.expect("unprefixed property id", "must start with", lambda c: c["properties"][0].update(id="core"))
        self.expect("duplicate property id", "duplicate property id",
                    lambda c: c["properties"][1].update(id=c["properties"][0]["id"]))
        self.expect("missing slot trait", "exactly one trait per slot", lambda c: c["visual_traits"].pop())
        self.expect("bad slot name", "slot", lambda c: c["visual_traits"][0].update(slot="shoes"))
        self.expect("derives_from unknown", "derives_from",
                    lambda c: c["visual_traits"][0].update(derives_from=[f"{s}.ghost"]))
        self.expect("non-string proper noun", "expected a non-empty string", lambda c: c.update(proper_nouns=[3]))
        self.expect("bad condition comparator", "comparator",
                    lambda c: c["properties"][0].update(
                        activation_condition={"variable": "E", "comparator": "!=", "value": 1}))
        self.expect("whitespace padding", "whitespace", lambda c: c["properties"][0].update(description=" padded"))

    def test_pair_rejections(self):
        sa, sb = slugify(A_NAME), slugify(B_NAME)
        scope = f"{sa}__{sb}"
        self.expect("dominance not 50", "dominance", mutate_pair=lambda p: p.update(dominance=60))
        self.expect("ceiling too low", "prompt_max_chars", mutate_pair=lambda p: p.update(prompt_max_chars=199))
        self.expect("ceiling too high", "prompt_max_chars", mutate_pair=lambda p: p.update(prompt_max_chars=2001))
        self.expect("bad origin label", "origin",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"].update(origin="C"))
        self.expect("unknown parent id", "parent id",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"].update(parent_ids=["ghost.v_hair"]))
        self.expect("origin A with a different descriptor", "verbatim",
                    mutate_pair=lambda p: p["visual"]["slots"]["build"].update(descriptor="something else entirely"))
        self.expect("origin A with the other character's parent", "exactly one parent",
                    mutate_pair=lambda p: p["visual"]["slots"]["build"].update(parent_ids=[f"{sb}.v_build"]))
        self.expect("transformed without a design_delta", "design_delta",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"].pop("design_delta"))
        self.expect("delta on a non-transformed trait", "only allowed when origin",
                    mutate_pair=lambda p: p["visual"]["slots"]["build"].update(
                        design_delta={"changed": "form", "from": "x", "to": "y"}))
        self.expect("delta from equals to", "must differ",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"]["design_delta"].update(
                        to=p["visual"]["slots"]["hair"]["design_delta"]["from"]))
        self.expect("delta 'to' not in descriptor", "appear in the transformed descriptor",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"]["design_delta"].update(to="not in there"))
        self.expect("bad delta kind", "changed",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"]["design_delta"].update(changed="vibe"))
        self.expect("transformed identical to parent", "must differ from its parent",
                    mutate_pair=lambda p: p["visual"]["slots"]["hair"].update(
                        descriptor="braided copper hair",
                        design_delta={"changed": "color", "from": "silver", "to": "braided copper hair"}))
        self.expect("new with the wrong parent", "emergent ability id",
                    mutate_pair=lambda p: p["visual"]["mood"].update(parent_ids=[f"{sa}.v_build"]))
        self.expect("interaction id outside the pair scope", "must start with",
                    mutate_pair=lambda p: p["interaction"].update(id="elsewhere.rule"))
        self.expect("interaction and emergent share an id", "different ids",
                    mutate_pair=lambda p: p["emergent_ability"].update(id=p["interaction"]["id"]))
        self.expect("missing trait outcome", "cover every property",
                    mutate_pair=lambda p: p["trait_outcomes"].pop())
        self.expect("not_carried without a reason", "reason",
                    mutate_pair=lambda p: p["trait_outcomes"][3].pop("reason"))
        self.expect("bad outcome label", "outcome",
                    mutate_pair=lambda p: p["trait_outcomes"][0].update(outcome="stolen"))
        self.expect("bad parameters", "parameter syntax",
                    mutate_pair=lambda p: p["visual"].update(parameters="ar 3:4"))
        self.expect("missing slot", "slots",
                    mutate_pair=lambda p: p["visual"]["slots"].pop("palette"))
        self.expect("unknown interaction dependency", "dependency",
                    mutate_pair=lambda p: p["interaction"].update(dependency_ids=["ghost.core"]))
        self.expect("unknown emergent ancestor", "ancestor",
                    mutate_pair=lambda p: p["emergent_ability"].update(direct_ancestor_ids=["ghost.core"]))
        self.expect("SOURCE_DERIVED interaction", "provenance",
                    mutate_pair=lambda p: p["interaction"].update(provenance="SOURCE_DERIVED"))
        self.expect("no limitations", "limitations",
                    mutate_pair=lambda p: p["emergent_ability"].update(limitations=[]))
        self.expect("pair names the same character twice", "different characters",
                    mutate_pair=lambda p: p.update(b=A_NAME))

    def test_file_name_must_match_content(self):
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            (root / "characters" / f"{slugify(A_NAME)}.json").rename(root / "characters" / "wrong_name.json")
            with self.assertRaises(SchemaError) as ctx:
                load_library(root)
            self.assertIn("file name must be", str(ctx.exception))

    def test_pair_needs_both_character_cards(self):
        card_a, _ = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a], [synthetic_pair(A_NAME, B_NAME)])
            with self.assertRaises(SchemaError) as ctx:
                load_library(root)
            self.assertIn("no character card named", str(ctx.exception))

    def test_duplicate_json_keys_are_rejected(self):
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            path = root / "characters" / f"{slugify(A_NAME)}.json"
            path.write_text(path.read_text(encoding="utf-8").replace('"name": "Zorblax",', '"name": "Zorblax", "name": "x",', 1),
                            encoding="utf-8")
            with self.assertRaises(SchemaError) as ctx:
                load_library(root)
            self.assertIn("duplicate key", str(ctx.exception))

    def test_unparseable_json_is_a_clear_error(self):
        card_a, card_b = default_cards()
        with tempfile.TemporaryDirectory() as tmp:
            root = write_library(Path(tmp), [card_a, card_b], [synthetic_pair(A_NAME, B_NAME)])
            (root / "pairs" / f"{slugify(A_NAME)}__{slugify(B_NAME)}.json").write_text("{not json", encoding="utf-8")
            with self.assertRaises(SchemaError) as ctx:
                load_library(root)
            self.assertIn("not valid JSON", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
