"""C1 (Contribution/Placement Classifier) tests: admission and validation."""

import unittest

from fusion_engine.c1_classifier import SourceAdmissionError, admit_source
from fusion_engine.types import (
    ArchitecturalPlacement,
    ContributionType,
    EpistemicStatus,
    Provenance,
    Source,
    SourceProperty,
)


def _valid_property(prop_id="p1"):
    return SourceProperty(
        id=prop_id,
        description="A test property.",
        contribution_type=ContributionType.MECHANISM,
        architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
        epistemic_status=EpistemicStatus.FICTIONAL,
    )


class TestAdmitSourceHappyPath(unittest.TestCase):
    def test_admits_well_formed_source(self):
        source = Source(name="[TEST] Source", properties=(_valid_property(),))
        admitted = admit_source(source)
        self.assertEqual(len(admitted), 1)
        self.assertEqual(admitted[0].id, "p1")

    def test_admitted_properties_are_source_derived(self):
        # Spec §9.1: a raw, unfused property is Source-Derived by construction.
        source = Source(name="[TEST] Source", properties=(_valid_property(),))
        (prop,) = admit_source(source)
        self.assertEqual(prop.provenance, Provenance.SOURCE_DERIVED)


class TestAdmitSourceRejectsMalformedInput(unittest.TestCase):
    def test_rejects_empty_name(self):
        source = Source(name="", properties=(_valid_property(),))
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)

    def test_rejects_no_properties(self):
        source = Source(name="[TEST] Empty", properties=())
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)

    def test_rejects_duplicate_property_ids(self):
        source = Source(name="[TEST] Dup", properties=(_valid_property("dup"), _valid_property("dup")))
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)

    def test_rejects_empty_property_description(self):
        malformed = SourceProperty(
            id="p1",
            description="",
            contribution_type=ContributionType.MECHANISM,
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
        )
        source = Source(name="[TEST] Bad description", properties=(malformed,))
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)

    def test_rejects_malformed_activation_condition(self):
        # activation_condition must be a Condition or None — a bare string or
        # other value would otherwise pass admission silently and only fail
        # later, confusingly, inside C3.
        malformed = SourceProperty(
            id="p1",
            description="A test property.",
            contribution_type=ContributionType.MECHANISM,
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
            activation_condition="E == 0",  # type: ignore[arg-type]
        )
        source = Source(name="[TEST] Malformed condition", properties=(malformed,))
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)

    def test_rejects_invalid_contribution_type(self):
        # Malformed data does not go through the type system in Python; C1
        # must catch this at admission rather than let it silently pass.
        malformed = SourceProperty(
            id="p1",
            description="A test property.",
            contribution_type="NOT_A_REAL_CONTRIBUTION_TYPE",  # type: ignore[arg-type]
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
        )
        source = Source(name="[TEST] Malformed", properties=(malformed,))
        with self.assertRaises(SourceAdmissionError):
            admit_source(source)


if __name__ == "__main__":
    unittest.main()
