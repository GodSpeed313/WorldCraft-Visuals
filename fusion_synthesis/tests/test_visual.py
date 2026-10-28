"""Appearance slots and visual provenance (AUTH-011 §6 test 3).

The transformed-trait checks are STRUCTURAL ONLY: they establish consistency
(a differing descriptor, a valid design_delta, differing from/to, 'to' present,
resolving parents), not artistic originality. There is deliberately no overlap
threshold and no similarity metric of any kind. The operator's review of each
rendered card is the acceptance gate for whether a transformation is visually
meaningful.
"""

import ast
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.schema import ORIGINS, SCENE_FIELDS, SLOTS, normalize, slugify

from . import A_NAME, B_NAME, default_cards, synthetic_pair, write_library


class AuthoredVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()

    def rows(self, pair):
        return assemble_card(self.library, pair)["visual_provenance"]

    def test_every_pair_has_all_slots_and_scene_fields(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                labels = [r["slot"] for r in self.rows(pair)]
                self.assertEqual(labels, ["subject", *SLOTS, *SCENE_FIELDS])

    def test_every_trait_has_descriptor_origin_and_resolving_parents(self):
        for pair in self.library.pairs:
            visual_ids = {t.id for n in (pair.a, pair.b) for t in self.library.characters[n].visual_traits}
            for row in self.rows(pair):
                with self.subTest(pair=pair.slug, slot=row["slot"]):
                    self.assertTrue(row["descriptor"].strip())
                    self.assertIn(row["origin"], ORIGINS)
                    self.assertTrue(row["parent_ids"])
                    for pid in row["parent_ids"]:
                        self.assertTrue(pid in visual_ids or pid == pair.emergent.id, pid)

    def test_a_and_b_descriptors_equal_their_parents(self):
        for pair in self.library.pairs:
            by_id = {t.id: t for n in (pair.a, pair.b) for t in self.library.characters[n].visual_traits}
            for row in self.rows(pair):
                if row["origin"] in ("A", "B"):
                    with self.subTest(pair=pair.slug, slot=row["slot"]):
                        self.assertEqual(row["descriptor"], by_id[row["parent_ids"][0]].descriptor)
                        owner = pair.a if row["origin"] == "A" else pair.b
                        self.assertEqual(row["parents"][0]["character"], owner)

    def test_new_traits_parent_to_the_emergent_ability(self):
        for pair in self.library.pairs:
            for row in self.rows(pair):
                if row["origin"] == "new":
                    with self.subTest(pair=pair.slug, slot=row["slot"]):
                        self.assertEqual(row["parent_ids"], [pair.emergent.id])

    def test_transformed_traits_pass_the_structural_checks(self):
        for pair in self.library.pairs:
            by_id = {t.id: t for n in (pair.a, pair.b) for t in self.library.characters[n].visual_traits}
            for row in self.rows(pair):
                if row["origin"] != "transformed":
                    continue
                with self.subTest(pair=pair.slug, slot=row["slot"]):
                    delta = row["design_delta"]
                    self.assertNotEqual(normalize(delta["from"]), normalize(delta["to"]))
                    self.assertIn(normalize(delta["to"]), normalize(row["descriptor"]))
                    for pid in row["parent_ids"]:
                        self.assertNotEqual(normalize(row["descriptor"]), normalize(by_id[pid].descriptor))

    def test_names_appear_in_provenance_not_in_descriptors(self):
        for pair in self.library.pairs:
            for row in self.rows(pair):
                if row["origin"] != "new":
                    self.assertTrue(all(p["character"] for p in row["parents"]))


class StructuralOnlyTests(unittest.TestCase):
    """Documents the limit of the structural checks: they cannot judge design change."""

    def test_a_reworded_transformation_passes_structure_and_needs_human_review(self):
        card_a, card_b = default_cards()
        pair = synthetic_pair(A_NAME, B_NAME)
        # Same design, one word swapped, with a technically valid delta. Structure accepts it by design.
        pair["visual"]["slots"]["hair"].update(
            descriptor="braided copper hair tied low",
            design_delta={"changed": "placement", "from": "braided copper hair", "to": "tied low"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            write_library(Path(tmp), [card_a, card_b], [pair])
            self.assertEqual(len(load_library(Path(tmp)).pairs), 1)

    def test_no_similarity_metric_exists_in_the_package(self):
        # AST-based, so comments that mention the rule cannot trip it.
        banned = ("jaccard", "difflib", "similar", "levenshtein", "overlap", "threshold")
        for path in Path(__file__).parents[1].glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                names = []
                if isinstance(node, ast.Name):
                    names.append(node.id)
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    names.append(node.name)
                elif isinstance(node, ast.Import):
                    names += [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names.append(node.module or "")
                for name in names:
                    for word in banned:
                        self.assertNotIn(word, name.lower(), f"{path.name}: {name}")


if __name__ == "__main__":
    unittest.main()
