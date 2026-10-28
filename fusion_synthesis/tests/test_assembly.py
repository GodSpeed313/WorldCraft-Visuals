"""C1 -> C2 -> C3 assembly over every authored pair, plus the engine's edge outcomes (AUTH-011 §6 test 2)."""

import tempfile
import unittest
from pathlib import Path

from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.schema import slugify

from . import A_NAME, B_NAME, default_cards, deep, synthetic_pair, write_library


def synthetic_card(mutate_a=None, mutate_b=None, mutate_pair=None):
    card_a, card_b = default_cards()
    pair = synthetic_pair(A_NAME, B_NAME)
    for fn, target in ((mutate_a, card_a), (mutate_b, card_b), (mutate_pair, pair)):
        if fn:
            fn(target)
    tmp = tempfile.TemporaryDirectory()
    root = write_library(Path(tmp.name), [card_a, card_b], [pair])
    library = load_library(root)
    try:
        return assemble_card(library, library.pairs[0])
    finally:
        tmp.cleanup()


class AuthoredPairTests(unittest.TestCase):
    """Data-driven: every pair found in the real data directory, with no pair named here."""

    @classmethod
    def setUpClass(cls):
        cls.library = load_library()

    def test_every_pair_assembles_and_carries_every_property_once(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                expected = {p.id for n in (pair.a, pair.b) for p in self.library.characters[n].properties}
                listed = [t["property_id"] for t in card["traits"]]
                self.assertEqual(sorted(listed), sorted(expected))
                self.assertEqual(len(listed), len(set(listed)))

    def test_emergent_provenance_is_read_from_the_ledger(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                # Weakest link over SOURCE_DERIVED ancestors and the authored rule = the rule's provenance.
                self.assertEqual(card["emergent_ability"]["provenance"], pair.interaction.provenance)
                self.assertNotEqual(card["emergent_ability"]["provenance"], "SOURCE_DERIVED")
                self.assertEqual(card["emergent_ability"]["governing_rule"]["provenance"], pair.interaction.provenance)

    def test_ancestry_includes_the_rule_and_every_direct_ancestor(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                ids = {a["id"] for a in card["ancestry"]}
                self.assertIn(pair.interaction.id, ids)
                self.assertTrue(set(pair.emergent.direct_ancestor_ids) <= ids)

    def test_authored_limitations_and_inherited_limitations_propagate(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                em = card["emergent_ability"]
                self.assertEqual(em["limitations"], list(pair.emergent.limitations))
                flagged = {
                    p.id
                    for n in (pair.a, pair.b)
                    for p in self.library.characters[n].properties
                    if (p.is_hard_limitation or p.is_prohibition) and p.id in pair.emergent.direct_ancestor_ids
                }
                self.assertEqual({x["property_id"] for x in em["inherited_limitations"]}, flagged)

    def test_compatibility_reports_what_was_evaluated(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                props = {p.id: p for n in (pair.a, pair.b) for p in self.library.characters[n].properties}
                conditioned = sum(1 for d in pair.interaction.dependency_ids if props[d].activation_condition)
                self.assertEqual(card["compatibility"]["evaluated_conditions"], conditioned)
                self.assertIn(card["compatibility"]["status"], ("COMPATIBLE", "CONDITIONALLY_COMPATIBLE", "INCOMPATIBLE", "UNRESOLVED"))

    def test_partial_success_preservation_when_compatible(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                all_ids = {p.id for n in (pair.a, pair.b) for p in self.library.characters[n].properties}
                if card["compatibility"]["status"] == "COMPATIBLE":
                    self.assertEqual(set(card["recorded_contribution_ids"]), all_ids)

    def test_recorded_ids_account_for_not_carried_traits_under_the_renamed_key(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                card = assemble_card(self.library, pair)
                self.assertNotIn("preserved_contribution_ids", card)
                not_carried = {t["property_id"] for t in card["traits"] if t["outcome"] == "not_carried"}
                if card["compatibility"]["status"] == "COMPATIBLE":
                    self.assertTrue(not_carried <= set(card["recorded_contribution_ids"]))

    def test_dominance_is_fixed_and_not_applied(self):
        for pair in self.library.pairs:
            card = assemble_card(self.library, pair)
            self.assertEqual(card["dominance"], {"value": 50, "applied": False, "note": "fixed in Phase 1; not applied as a weighting"})


class EngineOutcomeTests(unittest.TestCase):
    """C3's explicit-predicate outcomes still surface honestly on a card (synthetic data)."""

    def condition(self, comparator, value):
        return {"variable": "E", "comparator": comparator, "value": value}

    def with_conditions(self, disclosed=False):
        sa, sb = slugify(A_NAME), slugify(B_NAME)
        return synthetic_card(
            mutate_a=lambda c: c["properties"][0].update(activation_condition=self.condition("==", 0)),
            mutate_b=lambda c: c["properties"][0].update(activation_condition=self.condition(">", 0)),
            mutate_pair=lambda p: p["interaction"].update(is_disclosed_modification=disclosed),
        )

    def test_no_conditions_means_compatible_with_zero_evaluated(self):
        card = synthetic_card()
        self.assertEqual(card["compatibility"]["status"], "COMPATIBLE")
        self.assertEqual(card["compatibility"]["evaluated_conditions"], 0)

    def test_contradictory_conditions_are_refused_not_hidden(self):
        card = self.with_conditions()
        self.assertEqual(card["compatibility"]["status"], "INCOMPATIBLE")
        self.assertEqual(card["compatibility"]["evaluated_conditions"], 2)
        self.assertIn("simultaneous", card["compatibility"]["contradiction"])

    def test_disclosed_modification_is_conditionally_compatible(self):
        card = self.with_conditions(disclosed=True)
        self.assertEqual(card["compatibility"]["status"], "CONDITIONALLY_COMPATIBLE")
        self.assertTrue(card["compatibility"]["required_bridge"])

    def test_inv19_preserves_independent_contributions_when_not_compatible(self):
        card = self.with_conditions()
        sa, sb = slugify(A_NAME), slugify(B_NAME)
        preserved = set(card["recorded_contribution_ids"])
        self.assertIn(f"{sa}.bound", preserved)
        self.assertNotIn(f"{sa}.core", preserved)
        self.assertNotIn(f"{sb}.core", preserved)


if __name__ == "__main__":
    unittest.main()
