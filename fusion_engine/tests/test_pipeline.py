"""Integration-path tests: Source A + Source B -> C1 -> C2 -> C3 -> result."""

import unittest

from fusion_engine.c1_classifier import SourceAdmissionError
from fusion_engine.fixtures import dev_fixture_001 as fx
from fusion_engine.pipeline import run_slice
from fusion_engine.types import (
    ArchitecturalPlacement,
    CompatibilityStatus,
    ContributionType,
    EpistemicStatus,
    Provenance,
    Source,
    SourceProperty,
)


class TestHappyPath(unittest.TestCase):
    def test_compatible_case_end_to_end(self):
        result = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)
        self.assertEqual(result.compatibility.status, CompatibilityStatus.COMPATIBLE)
        self.assertEqual(result.emergent_property_provenance, Provenance.DEFENSIBLY_DERIVED)
        self.assertIn("a.layered_plating", result.emergent_property_ancestry)
        self.assertIn("b.signal_dampening", result.emergent_property_ancestry)

    def test_incompatible_case_end_to_end(self):
        result = run_slice(
            fx.SOURCE_A, fx.SOURCE_B, fx.CONFLICTING_FIELD_REQUIREMENT, fx.CONFLICTING_RESULT
        )
        self.assertEqual(result.compatibility.status, CompatibilityStatus.INCOMPATIBLE)
        self.assertIsNotNone(result.compatibility.contradiction)


class TestDeterminism(unittest.TestCase):
    def test_repeated_execution_is_byte_identical(self):
        first = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)
        second = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)
        self.assertEqual(first, second)

    def test_repeated_execution_is_deterministic_for_the_contradiction_case(self):
        first = run_slice(
            fx.SOURCE_A, fx.SOURCE_B, fx.CONFLICTING_FIELD_REQUIREMENT, fx.CONFLICTING_RESULT
        )
        second = run_slice(
            fx.SOURCE_A, fx.SOURCE_B, fx.CONFLICTING_FIELD_REQUIREMENT, fx.CONFLICTING_RESULT
        )
        self.assertEqual(first, second)


class TestMalformedInputRejection(unittest.TestCase):
    def test_run_slice_rejects_a_source_with_no_properties(self):
        empty_source = Source(name="[TEST] Empty", properties=())
        with self.assertRaises(SourceAdmissionError):
            run_slice(empty_source, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)

    def test_colliding_property_ids_across_source_a_and_source_b_fail_loudly(self):
        shared_id_prop = SourceProperty(
            id="a.kinetic_discharge",  # collides with fx.SOURCE_A's own id
            description="A second, unrelated property that happens to reuse an id.",
            contribution_type=ContributionType.ABILITY,
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
        )
        colliding_source_b = Source(name="[TEST] Colliding Source", properties=(shared_id_prop,))
        with self.assertRaises(SourceAdmissionError):
            run_slice(fx.SOURCE_A, colliding_source_b, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)


class TestINV19PartialSuccessPreservation(unittest.TestCase):
    def test_independent_contribution_survives_an_incompatible_interaction(self):
        # a.layered_plating and b.signal_dampening are not among
        # CONFLICTING_FIELD_REQUIREMENT's dependencies, so they must still
        # appear as preserved even though the interaction under test is
        # Incompatible (INV-19), while the two disqualified properties do not
        # (INV-07's own exclusion is not reintroduced here).
        result = run_slice(
            fx.SOURCE_A, fx.SOURCE_B, fx.CONFLICTING_FIELD_REQUIREMENT, fx.CONFLICTING_RESULT
        )
        self.assertEqual(result.compatibility.status, CompatibilityStatus.INCOMPATIBLE)
        self.assertIn("a.layered_plating", result.preserved_contribution_ids)
        self.assertIn("b.signal_dampening", result.preserved_contribution_ids)
        self.assertNotIn("a.kinetic_discharge", result.preserved_contribution_ids)
        self.assertNotIn("b.ambient_field_draw", result.preserved_contribution_ids)

    def test_everything_is_preserved_when_compatible(self):
        result = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)
        self.assertEqual(result.compatibility.status, CompatibilityStatus.COMPATIBLE)
        all_ids = {p.id for p in fx.SOURCE_A.properties} | {p.id for p in fx.SOURCE_B.properties}
        self.assertEqual(set(result.preserved_contribution_ids), all_ids)


class TestFixturesAreClearlyLabeledSynthetic(unittest.TestCase):
    def test_fixture_source_names_are_tagged_as_dev_fixtures(self):
        self.assertTrue(fx.SOURCE_A.name.startswith("[DEV FIXTURE]"))
        self.assertTrue(fx.SOURCE_B.name.startswith("[DEV FIXTURE]"))


if __name__ == "__main__":
    unittest.main()
