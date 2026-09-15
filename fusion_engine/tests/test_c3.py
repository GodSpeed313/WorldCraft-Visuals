"""C3 (Contradiction/Compatibility Evaluator) tests: spec §14, INV-09-11."""

import unittest

from fusion_engine.c3_compatibility import evaluate_compatibility
from fusion_engine.types import (
    ArchitecturalPlacement,
    CompatibilityStatus,
    Condition,
    ContributionType,
    EpistemicStatus,
    InteractionRule,
    Provenance,
    SourceProperty,
)


def _prop(prop_id, condition=None):
    return SourceProperty(
        id=prop_id,
        description=f"Property {prop_id}.",
        contribution_type=ContributionType.MECHANISM,
        architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
        epistemic_status=EpistemicStatus.FICTIONAL,
        activation_condition=condition,
    )


class TestCompatibleOutcome(unittest.TestCase):
    def test_no_conditions_is_compatible(self):
        p1, p2 = _prop("p1"), _prop("p2")
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.COMPATIBLE)
        self.assertIsNone(result.contradiction)

    def test_non_overlapping_variables_are_compatible(self):
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("F", ">", 0.0))  # different variable
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.COMPATIBLE)

    def test_compatible_ranges_on_same_variable(self):
        p1 = _prop("p1", Condition("E", ">=", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))  # overlaps for any E > 0
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.COMPATIBLE)


class TestIncompatibleOutcome(unittest.TestCase):
    def test_explicit_E_eq_0_vs_E_gt_0_contradiction(self):
        # Spec §4.2's worked example, literally.
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        rule = InteractionRule(
            id="rule",
            description="requires both simultaneously",
            dependency_ids=(p1.id, p2.id),
            provenance=Provenance.DEFENSIBLY_DERIVED,
            is_disclosed_modification=False,
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.INCOMPATIBLE)
        self.assertIsNotNone(result.contradiction)

    def test_contradiction_names_both_properties(self):
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertIn("p1", result.contradiction)
        self.assertIn("p2", result.contradiction)


class TestConditionallyCompatibleOutcome(unittest.TestCase):
    def test_disclosed_modification_rescues_a_contradiction(self):
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        bridge = InteractionRule(
            id="bridge",
            description="an explicitly disclosed buffer rule",
            dependency_ids=(p1.id, p2.id),
            provenance=Provenance.INVENTED_BRIDGE,
            is_disclosed_modification=True,
        )
        result = evaluate_compatibility((p1, p2), bridge)
        self.assertEqual(result.status, CompatibilityStatus.CONDITIONALLY_COMPATIBLE)
        self.assertEqual(result.required_bridge, bridge.description)

    def test_undisclosed_interaction_does_not_silently_rescue_a_contradiction(self):
        # INV-11: a contradiction must not be laundered away by an
        # interaction that never named itself as a rescue.
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        rule = InteractionRule(
            id="rule",
            description="not disclosed as a modification",
            dependency_ids=(p1.id, p2.id),
            provenance=Provenance.INVENTED_BRIDGE,
            is_disclosed_modification=False,
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.INCOMPATIBLE)


class TestUnresolvedOutcome(unittest.TestCase):
    def test_unresolved_interaction_yields_unresolved_compatibility(self):
        p1, p2 = _prop("p1"), _prop("p2")
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.UNRESOLVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.UNRESOLVED)
        self.assertIsNotNone(result.unresolved_reason)

    def test_unresolved_interaction_overrides_an_apparent_contradiction(self):
        # If the governing rule itself is Unresolved, no defensible
        # determination can be made at all — not even "Incompatible".
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.UNRESOLVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.UNRESOLVED)


class TestComparatorBoundaries(unittest.TestCase):
    """Explicit interval-boundary cases for the five supported comparators.

    These are the cases most likely to be off by one inclusivity flag, so
    each is checked directly rather than trusted from the general-case tests
    above.
    """

    def _check(self, comparator_a, comparator_b, expect_status):
        p1 = _prop("p1", Condition("E", comparator_a, 0.0))
        p2 = _prop("p2", Condition("E", comparator_b, 0.0))
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, expect_status, f"{comparator_a} 0 vs {comparator_b} 0")

    def test_ge_zero_vs_le_zero_is_compatible_at_the_shared_boundary_point(self):
        self._check(">=", "<=", CompatibilityStatus.COMPATIBLE)

    def test_gt_zero_vs_le_zero_is_incompatible(self):
        # E > 0 excludes 0; E <= 0 requires <= 0. No value satisfies both.
        self._check(">", "<=", CompatibilityStatus.INCOMPATIBLE)

    def test_ge_zero_vs_lt_zero_is_incompatible(self):
        # Symmetric to the above: E >= 0 excludes nothing below 0; E < 0
        # excludes 0 itself. No shared value.
        self._check(">=", "<", CompatibilityStatus.INCOMPATIBLE)

    def test_gt_zero_vs_lt_zero_is_incompatible(self):
        self._check(">", "<", CompatibilityStatus.INCOMPATIBLE)

    def test_ge_zero_vs_ge_zero_is_compatible(self):
        self._check(">=", ">=", CompatibilityStatus.COMPATIBLE)

    def test_eq_zero_vs_eq_zero_is_compatible(self):
        self._check("==", "==", CompatibilityStatus.COMPATIBLE)

    def test_eq_zero_vs_eq_one_is_incompatible(self):
        p1 = _prop("p1", Condition("E", "==", 0.0))
        p2 = _prop("p2", Condition("E", "==", 1.0))
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        result = evaluate_compatibility((p1, p2), rule)
        self.assertEqual(result.status, CompatibilityStatus.INCOMPATIBLE)

    def test_eq_zero_vs_ge_zero_is_compatible(self):
        self._check("==", ">=", CompatibilityStatus.COMPATIBLE)

    def test_eq_zero_vs_gt_zero_is_incompatible(self):
        # The boundary case this slice was built to get right: E == 0 vs
        # E > 0, spec §4.2's own worked example.
        self._check("==", ">", CompatibilityStatus.INCOMPATIBLE)

    def test_unsupported_comparator_raises_rather_than_silently_passing(self):
        p1 = _prop("p1", Condition("E", "!=", 0.0))
        p2 = _prop("p2", Condition("E", ">", 0.0))
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(p1.id, p2.id), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        with self.assertRaises(ValueError):
            evaluate_compatibility((p1, p2), rule)


if __name__ == "__main__":
    unittest.main()
