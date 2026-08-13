# =============================================================
#  MYTHOS-SYNC FRAMEWORK — PROPERTY TESTS (Hypothesis)
#
#  Requires a dev install:  pip install -r requirements-dev.txt
#
#  Deliberately SEPARATE from test_engine.py, which documents itself as
#  "Standard library only (unittest). No install step required." That
#  property is worth keeping: `python -m unittest test_engine` must stay
#  runnable with zero installs. Hypothesis-dependent tests live here so
#  that header stays true.
#
#  These are a strict upgrade of the seeded-random sweeps already in
#  test_engine.py (test_transposition_never_yields_an_illegal_power,
#  test_grounding_prefers_a_relative_when_one_is_legal), not a new
#  testing philosophy: same invariants, generated space instead of a
#  fixed seed, with shrinking to a minimal counterexample on failure.
#  The originals are NOT replaced — they remain the install-free guard.
# =============================================================

import contextlib
import unittest

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from logic_auditor import (
    DEFAULT_TRANSPOSITIONS,
    MODALITY_RANK,
    POWER_FAMILIES,
    POWER_REGISTRY,
    TRANSPOSITION_MAP,
    _grounding_candidates,
    audit_power,
    family_of,
    ground_power,
)

ALL_MODALITIES = ("LEGACY", "GROUNDED", "HIGH_CONCEPT")

# Registry keys are sampled from a sorted snapshot so the generated space is
# deterministic across runs and independent of dict insertion order.
REGISTERED_POWERS = tuple(sorted(POWER_REGISTRY))

SYNTHETIC = "Synthetic Probe Power"


def is_legal(power_name: str, modality: str) -> bool:
    """A power is legal when the fusion's rank meets its minimum."""
    entry = POWER_REGISTRY[power_name]
    return MODALITY_RANK[entry["min_modality"]] <= MODALITY_RANK[modality]


@contextlib.contextmanager
def injected_power(entry: dict, name: str = SYNTHETIC):
    """Temporarily place a synthetic entry in the global POWER_REGISTRY.

    POWER_REGISTRY is module-level mutable state shared by every consumer,
    so the entry is always removed, including on failure. Restoring rather
    than rebuilding keeps the rest of the registry byte-identical.
    """
    POWER_REGISTRY[name] = entry
    try:
        yield name
    finally:
        POWER_REGISTRY.pop(name, None)


# Family values that are NOT part of the sanctioned taxonomy. Text is drawn
# from a broad alphabet rather than a fixed list so shrinking reports the
# smallest offending value rather than whichever literal was hand-picked.
unsanctioned_family = st.text(min_size=1, max_size=24).filter(
    lambda s: s not in POWER_FAMILIES
)


class Gap4UnresolvedFamilyTests(unittest.TestCase):
    """GAP-4 — does an unresolved family actually halt, or ground anyway?

    The rulings assume UNRESOLVED_FAMILY resolves to CAUTIONARY. Nothing in
    logic_auditor.py enforces that. The condition is currently unreachable
    in production only because all 30/30 POWER_REGISTRY entries carry a
    family drawn from POWER_FAMILIES — a property of the data, not a
    property of the code.

    These tests are FACT-FINDING. They characterise what the code does
    today; they do not assert that it is correct. If GAP-4 is later ruled
    and fixed, these tests SHOULD fail — that failure is the signal to
    update them deliberately, which is the point of pinning the behaviour
    rather than leaving it undescribed.
    """

    @settings(max_examples=200, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(family=unsanctioned_family, min_modality=st.sampled_from(ALL_MODALITIES))
    def test_unsanctioned_family_falls_through_to_the_blanket_default(
        self, family, min_modality
    ):
        """FINDING: it does NOT halt. A power carrying a family outside
        POWER_FAMILIES silently receives DEFAULT_TRANSPOSITIONS.

        The fall-through is structural, at logic_auditor.py:151-156: an
        unsanctioned family yields no `family_members`, so `kin` is empty
        and the blanket default is returned. No signal distinguishes this
        from a power that legitimately has no curated mapping.
        """
        entry = {"min_modality": min_modality, "cost_factor": 5, "family": family}
        with injected_power(entry) as name:
            assume(name not in TRANSPOSITION_MAP)
            self.assertEqual(
                _grounding_candidates(name),
                DEFAULT_TRANSPOSITIONS,
                "expected the blanket default; a halt would not return candidates",
            )

    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(family=unsanctioned_family)
    def test_unsanctioned_family_is_reported_as_an_ordinary_transposition(self, family):
        """FINDING: the audit result is indistinguishable from a legitimate one.

        `state` is TRANSPOSED and `transposed_to` names a real power. A
        consumer reading the contract cannot tell this apart from a normal
        grounding — which is precisely the CAUTIONARY signal GAP-4 says
        should exist and does not.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": family}
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        with injected_power(entry) as name:
            assume(name not in TRANSPOSITION_MAP)
            result = audit_power(name, fusion)
            self.assertEqual(result["state"], "TRANSPOSED")
            self.assertIn(result["transposed_to"], DEFAULT_TRANSPOSITIONS)
            self.assertIsNone(
                result.get("cautionary"),
                "no CAUTIONARY channel exists on the audit result (GAP-4)",
            )

    def test_family_set_to_none_also_falls_through(self):
        """`family: None` takes the same silent path as an unsanctioned value.

        Distinct from a missing key (below) because `family_of` returns None
        without raising, so the falsy branch at :151 is what skips the family
        lookup rather than an exception.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": None}
        with injected_power(entry) as name:
            self.assertEqual(_grounding_candidates(name), DEFAULT_TRANSPOSITIONS)

    def test_missing_family_key_raises_rather_than_falling_through(self):
        """FINDING (asymmetry): a MISSING `family` key fails loudly instead.

        `family_of` indexes `entry["family"]` directly (logic_auditor.py:91),
        so an entry with no family key raises KeyError rather than grounding
        silently. Recorded because it means GAP-4's exposure is narrower than
        "any malformed entry": the silent path requires a family that is
        PRESENT but unsanctioned. A schema that omits the key is already loud.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5}
        with injected_power(entry) as name:
            with self.assertRaises(KeyError):
                _grounding_candidates(name)

    def test_unregistered_power_never_reaches_grounding(self):
        """Boundary: a power absent from the registry short-circuits earlier.

        `audit_power` returns UNVERIFIED at :209-218 before any grounding is
        attempted, so the GAP-4 path is reachable only for powers that ARE
        registered but carry an unsanctioned family. This is what keeps the
        gap dormant in production rather than merely unobserved.
        """
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        result = audit_power("Not A Registered Power", fusion)
        self.assertEqual(result["state"], "UNVERIFIED")
        self.assertIsNone(result["transposed_to"])


class GeneratedInvariantTests(unittest.TestCase):
    """Hypothesis versions of the two seeded sweeps in test_engine.py.

    The originals stay where they are. These run the same invariants over a
    generated space so a future break yields a shrunk minimal counterexample
    instead of whichever case `random.seed(21)` happened to reach.
    """

    @settings(max_examples=400, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(
        power=st.sampled_from(REGISTERED_POWERS),
        modality=st.sampled_from(ALL_MODALITIES),
    )
    def test_transposition_never_yields_an_illegal_power(self, power, modality):
        """Whatever a fusion ends up with must be legal at its own modality.

        Grounding picks at random among equally-ranked candidates, so each
        example is exercised repeatedly — a single call can pass by luck.
        """
        fusion = {"fusion_name": "t", "modality": modality, "dominant": "", "tags": []}
        for _ in range(20):
            result = audit_power(power, fusion)
            final = result["transposed_to"] or result["power"]
            self.assertTrue(
                is_legal(final, modality),
                f"{power} -> {final} is illegal for {modality}",
            )

    @settings(max_examples=300, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(
        power=st.sampled_from(REGISTERED_POWERS),
        modality=st.sampled_from(ALL_MODALITIES),
    )
    def test_grounding_prefers_a_relative_when_one_is_legal(self, power, modality):
        """Generalised from the Titan-Shifting case: whenever a same-family
        stand-in is legal at the target modality, grounding must choose one.

        Guarded by `assume` rather than asserted unconditionally, because the
        invariant is conditional by construction — a power whose family offers
        no legal relative is entitled to leave the family, and asserting
        otherwise would be a stronger claim than the engine makes.
        """
        assume(not is_legal(power, modality))

        rank = MODALITY_RANK[modality]
        legal_kin = [
            p
            for p in _grounding_candidates(power)
            if p in POWER_REGISTRY
            and MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] <= rank
            and family_of(p) == family_of(power)
        ]
        assume(bool(legal_kin))

        for _ in range(20):
            target = ground_power(power, rank)
            self.assertEqual(
                family_of(target),
                family_of(power),
                f"{power} grounded out of its family to {target} at {modality}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
