"""Foundational-type tests: provenance ordering and type separation."""

import unittest

from fusion_engine.types import CompatibilityStatus, Provenance


class TestProvenanceOrdering(unittest.TestCase):
    def test_canonical_rank_ordering(self):
        # CHECK-05: Source-Derived > Defensibly Derived > Invented Bridge > Unresolved.
        self.assertGreater(Provenance.SOURCE_DERIVED, Provenance.DEFENSIBLY_DERIVED)
        self.assertGreater(Provenance.DEFENSIBLY_DERIVED, Provenance.INVENTED_BRIDGE)
        self.assertGreater(Provenance.INVENTED_BRIDGE, Provenance.UNRESOLVED)

    def test_weakest_link_is_min(self):
        # INV-05's weakest-link function is exactly min() over this ordering.
        values = [Provenance.SOURCE_DERIVED, Provenance.UNRESOLVED, Provenance.DEFENSIBLY_DERIVED]
        self.assertEqual(min(values), Provenance.UNRESOLVED)


class TestStateIdentitySeparation(unittest.TestCase):
    def test_provenance_and_compatibility_status_are_different_enum_classes(self):
        self.assertIsNot(Provenance, CompatibilityStatus)
        self.assertFalse(issubclass(CompatibilityStatus, Provenance))
        self.assertFalse(issubclass(Provenance, CompatibilityStatus))

    def test_shared_unresolved_label_does_not_imply_equivalence(self):
        # Spec §4.4 State-Identity Principle / CHECK-04: shared natural-language
        # labels never establish shared semantics. Two members named UNRESOLVED
        # from unrelated Enum classes must not compare equal.
        self.assertNotEqual(Provenance.UNRESOLVED, CompatibilityStatus.UNRESOLVED)


if __name__ == "__main__":
    unittest.main()
