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
import io
import unittest

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

import mythos_sync
from logic_auditor import (
    CAUSE_NO_LEGAL_CANDIDATE_FOR_FUSION,
    CAUSE_NO_LEGITIMATE_CANDIDATE,
    DEFAULT_TRANSPOSITIONS,
    GROUNDING_UNAVAILABLE,
    MODALITY_RANK,
    POWER_FAMILIES,
    POWER_REGISTRY,
    TRANSPOSITION_MAP,
    _GroundingHalt,
    _grounding_candidates,
    audit_power,
    family_of,
    ground_power,
)
from mythos_sync import build_legacy_profile

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


@contextlib.contextmanager
def injected_transposition(name: str, targets: list):
    """Temporarily add a synthetic TRANSPOSITION_MAP entry.

    Same rationale as `injected_power`: TRANSPOSITION_MAP is module-level
    mutable state shared by every consumer, so the entry is always removed,
    including on failure.
    """
    TRANSPOSITION_MAP[name] = targets
    try:
        yield name
    finally:
        TRANSPOSITION_MAP.pop(name, None)


def quiet(fn, *args, **kwargs):
    """Run fn with stdout swallowed — mythos_sync narrates heavily.

    Deliberately not imported from test_engine.py: this file stays
    independent of it by design (see the module docstring above).
    """
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


# Family values that are NOT part of the sanctioned taxonomy. Text is drawn
# from a broad alphabet rather than a fixed list so shrinking reports the
# smallest offending value rather than whichever literal was hand-picked.
unsanctioned_family = st.text(min_size=1, max_size=24).filter(
    lambda s: s not in POWER_FAMILIES
)


class Gap4UnresolvedFamilyTests(unittest.TestCase):
    """GAP-4 — CLOSED (Contract 002 I8), implemented under AUTH-005.

    The first three tests below previously pinned FACT-FINDING assertions
    describing an unenforced gap; GAP-4's closure and AUTH-005's
    implementation are exactly the event their own docstrings said should
    make them fail, so they are revised here to assert the now-governing
    I8(b) behavior directly, rather than left green by accident.

    The remaining two tests are unaffected by AUTH-005 — they characterise
    a different, adjacent boundary (a missing `family` key; an unregistered
    power) that I8 does not touch — and remain FACT-FINDING as before.

    The condition I8 governs is still unreachable in production with real
    data only because all 30/30 POWER_REGISTRY entries carry a sanctioned
    family with a legal LEGACY-rank kin — a property of the data, not of
    the code, exactly as before AUTH-005.
    """

    @settings(max_examples=200, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(family=unsanctioned_family, min_modality=st.sampled_from(ALL_MODALITIES))
    def test_unsanctioned_family_falls_through_to_the_blanket_default(
        self, family, min_modality
    ):
        """GOVERNED (Contract 002 I8(b), AUTH-005).

        `_grounding_candidates` still returns the DEFAULT_TRANSPOSITIONS
        values for an unsanctioned family — that low-level lookup was
        never the defect — now wrapped in a `_GroundingCandidates` marking
        it explicitly `legitimate=False`, which is what `ground_power`
        reads rather than inferring legitimacy from object identity. What
        changed is that `audit_power` no longer treats reaching this
        fallback as a legitimate candidate: it now halts to
        GROUNDING_UNAVAILABLE with cause NO_LEGITIMATE_CANDIDATE instead
        of transposing to a DEFAULT_TRANSPOSITIONS member.
        """
        assume(min_modality != "LEGACY")  # a LEGACY power is never illegal to ground
        entry = {"min_modality": min_modality, "cost_factor": 5, "family": family}
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        with injected_power(entry) as name:
            assume(name not in TRANSPOSITION_MAP)
            candidates = _grounding_candidates(name)
            self.assertEqual(
                candidates,
                DEFAULT_TRANSPOSITIONS,
                "the low-level lookup's values are unchanged by AUTH-005",
            )
            self.assertFalse(
                candidates.legitimate,
                "the DEFAULT_TRANSPOSITIONS menu must be marked illegitimate",
            )
            result = audit_power(name, fusion)
            self.assertEqual(result["state"], GROUNDING_UNAVAILABLE)
            self.assertEqual(result["unavailable_cause"], CAUSE_NO_LEGITIMATE_CANDIDATE)
            self.assertIsNone(result["transposed_to"])

    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(family=unsanctioned_family)
    def test_unsanctioned_family_is_reported_as_an_ordinary_transposition(self, family):
        """GOVERNED (Contract 002 I8(b)/(d)/(f), AUTH-005).

        The audit result is now distinct from an ordinary transposition,
        not indistinguishable from one: `state` is GROUNDING_UNAVAILABLE,
        never TRANSPOSED; `transposed_to` is None; and `unavailable_cause`
        names I8(b) specifically. This is the CAUTIONARY-shaped signal
        GAP-4 found missing, now present.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": family}
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        with injected_power(entry) as name:
            assume(name not in TRANSPOSITION_MAP)
            result = audit_power(name, fusion)
            self.assertEqual(result["state"], GROUNDING_UNAVAILABLE)
            self.assertNotEqual(result["state"], "TRANSPOSED")
            self.assertIsNone(result["transposed_to"])
            self.assertEqual(result["unavailable_cause"], CAUSE_NO_LEGITIMATE_CANDIDATE)

    def test_family_set_to_none_also_falls_through(self):
        """GOVERNED (Contract 002 I8(b), AUTH-005).

        `family: None` takes the same halt path as an unsanctioned value.
        `_grounding_candidates`'s values are unchanged (still
        DEFAULT_TRANSPOSITIONS — `family_of` returns None without raising,
        so the falsy branch at :151 is what skips the family lookup rather
        than an exception), now wrapped `legitimate=False`; `audit_power`
        halts on top of that explicit signal.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": None}
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        with injected_power(entry) as name:
            candidates = _grounding_candidates(name)
            self.assertEqual(candidates, DEFAULT_TRANSPOSITIONS)
            self.assertFalse(candidates.legitimate)
            result = audit_power(name, fusion)
            self.assertEqual(result["state"], GROUNDING_UNAVAILABLE)
            self.assertEqual(result["unavailable_cause"], CAUSE_NO_LEGITIMATE_CANDIDATE)

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


class Auth005GroundingUnavailableCoverageTests(unittest.TestCase):
    """New coverage required by AUTH-005 for Contract 002 I8, beyond what
    the revised Gap4UnresolvedFamilyTests assertions cover. Before AUTH-005,
    every GAP-4 test targeted I8(b) only — I8(c) had zero coverage
    (open_contract_gaps.md:680-683 names both fallback sites; only one had
    a test).
    """

    FUSION = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}

    def _i8b_case(self):
        """A power with an unsanctioned family — I8(b): no legitimate
        candidate ever existed for the resolved family."""
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": "NOT_A_REAL_FAMILY"}
        with injected_power(entry, name="AUTH-005 Probe B") as name:
            return audit_power(name, self.FUSION)

    def _i8c_case(self):
        """A power with a real, curated TRANSPOSITION_MAP entry whose every
        target requires HIGH_CONCEPT — I8(c): legitimate candidates existed
        but none was legal for this (LEGACY) fusion."""
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": None}
        targets = ["Domain Expansion", "Reality Glitch"]  # both HIGH_CONCEPT-only
        with injected_power(entry, name="AUTH-005 Probe C") as name, \
             injected_transposition(name, targets):
            return audit_power(name, self.FUSION)

    def test_legal_candidates_all_illegal_for_fusion_halts_as_grounding_unavailable(self):
        """Contract 002 I8(c) — legitimate candidates existed, none legal
        for this fusion. Confirmed via a real, temporary TRANSPOSITION_MAP
        entry (a genuinely legitimate grounding path, not the
        DEFAULT_TRANSPOSITIONS fallback): `ground_power`'s own
        empty-after-filter branch fires because every candidate requires
        HIGH_CONCEPT and the fusion is LEGACY.
        """
        entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": None}
        targets = ["Domain Expansion", "Reality Glitch"]
        with injected_power(entry, name="AUTH-005 Probe C") as name, \
             injected_transposition(name, targets):
            candidates = _grounding_candidates(name)
            self.assertEqual(candidates, targets)
            self.assertTrue(
                candidates.legitimate,
                "this must be the curated route, not the I8(b) fallback",
            )
            result = audit_power(name, self.FUSION)
            self.assertEqual(result["state"], GROUNDING_UNAVAILABLE)
            self.assertEqual(result["unavailable_cause"], CAUSE_NO_LEGAL_CANDIDATE_FOR_FUSION)
            self.assertIsNone(result["transposed_to"])

    def test_ground_power_determines_the_cause_once_and_audit_power_reads_it(self):
        """The cause must be determined once, at ground_power's own point
        of decision, and consumed by audit_power rather than re-derived.

        Checked directly against ground_power()'s own return value (a
        `_GroundingHalt`), not inferred from audit_power()'s dict alone —
        this is what would fail if a future edit reintroduced a second,
        independent computation of the cause inside audit_power.
        """
        b_entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": "NOT_A_REAL_FAMILY"}
        with injected_power(b_entry, name="AUTH-005 Probe B3") as name:
            halt = ground_power(name, MODALITY_RANK["LEGACY"])
            self.assertIsInstance(halt, _GroundingHalt)
            self.assertEqual(halt.cause, CAUSE_NO_LEGITIMATE_CANDIDATE)
            result = audit_power(name, self.FUSION)
            self.assertEqual(result["unavailable_cause"], halt.cause)

        c_entry = {"min_modality": "HIGH_CONCEPT", "cost_factor": 5, "family": None}
        targets = ["Domain Expansion", "Reality Glitch"]
        with injected_power(c_entry, name="AUTH-005 Probe C3") as name, \
             injected_transposition(name, targets):
            halt = ground_power(name, MODALITY_RANK["LEGACY"])
            self.assertIsInstance(halt, _GroundingHalt)
            self.assertEqual(halt.cause, CAUSE_NO_LEGAL_CANDIDATE_FOR_FUSION)
            result = audit_power(name, self.FUSION)
            self.assertEqual(result["unavailable_cause"], halt.cause)

    def test_i8b_and_i8c_causes_are_distinguishable_from_each_other(self):
        """Contract 002 I8(f) — the two causes must be distinguishable from
        EACH OTHER, not merely from APPROVED/TRANSPOSED.
        """
        b_result = self._i8b_case()
        c_result = self._i8c_case()
        self.assertEqual(b_result["state"], GROUNDING_UNAVAILABLE)
        self.assertEqual(c_result["state"], GROUNDING_UNAVAILABLE)
        self.assertEqual(b_result["unavailable_cause"], CAUSE_NO_LEGITIMATE_CANDIDATE)
        self.assertEqual(c_result["unavailable_cause"], CAUSE_NO_LEGAL_CANDIDATE_FOR_FUSION)
        self.assertNotEqual(b_result["unavailable_cause"], c_result["unavailable_cause"])

    def test_audit_power_never_reports_terminal_as_transposed_or_unverified(self):
        """AUTH-005's explicit prohibition, checked directly against both
        governed causes: a GROUNDING_UNAVAILABLE result's `state`/`status`
        must never be TRANSPOSED or UNVERIFIED.
        """
        for result in (self._i8b_case(), self._i8c_case()):
            self.assertEqual(result["state"], GROUNDING_UNAVAILABLE)
            self.assertNotEqual(result["state"], "TRANSPOSED")
            self.assertNotEqual(result["state"], "UNVERIFIED")
            self.assertNotIn("TRANSPOSED", result["status"])
            self.assertNotIn("UNVERIFIED", result["status"])


class Auth005AuditAndTakePromotionTests(unittest.TestCase):
    """AUTH-005 — `audit_and_take` (inside `build_legacy_profile`) must not
    promote a GROUNDING_UNAVAILABLE result into `approved_powers`.

    `audit_and_take` is a nested function with no standalone import path, so
    this exercises it through the real, unmodified `build_legacy_profile`
    pipeline. The real GAP-4 condition is unreachable with current registry
    data, so `mythos_sync.audit_power` is temporarily wrapped to force
    exactly the FIRST power the pipeline happens to audit to report
    GROUNDING_UNAVAILABLE; every subsequent audit in the same run goes
    through the real, unmodified `audit_power` exactly as production would.
    """

    def test_grounding_unavailable_is_not_promoted_into_approved_powers(self):
        """AUTH-005 / Contract 002 I8(d) — a GROUNDING_UNAVAILABLE result
        must not itself promote the rejected original power or a
        substitute into `approved_powers`.

        `build_legacy_profile` selects powers via an unseeded
        `random.shuffle`/`random.choice` pipeline (`mythos_sync.py:176-238`)
        over a set-derived pool, so which power is audited first, and
        whether that SAME power name is drawn again later from a
        different pool, is not deterministic run to run.

        Two distinct sources of non-determinism were found, empirically,
        not assumed, via a 500-iteration stochastic stress run of an
        earlier version of this test:

        1. The forced power can be drawn a SECOND time from a different
           pool later in the same run (`generic_pool`/`universal_candidates`
           only filter `p not in approved_powers`, `mythos_sync.py:228`,
           `:236` — not "already audited this run"). Fixed by forcing
           EVERY encounter of the drawn power, not just the first, so
           there is no unforced legitimate encounter of that name to
           confuse a per-entry check with.
        2. Even with every encounter of the forced power's own SUBJECT
           audit forced, the SAME name can still legitimately enter
           `approved_powers` as the `transposed_to` TARGET of some
           unrelated OTHER power's legitimate grounding — 8 of 500
           stress-run iterations failed exactly this way (e.g. a
           different illegal power legitimately transposing to "The
           Scientific Method" while "The Scientific Method" was itself
           the forced power). This is correct production behavior, not a
           bug, and a blanket `assertNotIn(name, approved_powers)` cannot
           tell it apart from an actual promotion of the terminal itself.

        Fixed by reconstructing the governed rule directly from
        `audit_log` — never let a `grounding_unavailable` entry
        contribute to `approved_powers` — in the same order
        `audit_and_take` applies it, and requiring the actual, real
        `approved_powers` to match that reconstruction exactly. This
        tests the invariant itself, entry by entry, rather than a
        specific power's final membership, so it is correct regardless
        of which power gets drawn, how many times, or what any other
        power's legitimate grounding target happens to be — no
        production randomness is touched to achieve this.
        """
        forced_name = {}
        real_audit_power = mythos_sync.audit_power

        def fake_audit_power(power_name, fusion_profile):
            if not forced_name:
                forced_name["name"] = power_name
            if power_name == forced_name.get("name"):
                return {
                    "fusion": fusion_profile.get("fusion_name", "t"),
                    "power": power_name,
                    "status": "🛑 GROUNDING UNAVAILABLE",
                    "state": GROUNDING_UNAVAILABLE,
                    "message": "forced for test",
                    "cost_factor": None,
                    "transposed_to": None,
                    "unavailable_cause": CAUSE_NO_LEGITIMATE_CANDIDATE,
                }
            return real_audit_power(power_name, fusion_profile)

        mythos_sync.audit_power = fake_audit_power
        try:
            profile = quiet(build_legacy_profile, "Malcolm X", "Bruce Lee", 50)
        finally:
            mythos_sync.audit_power = real_audit_power

        self.assertIn("name", forced_name, "the fake was never invoked — nothing was audited")
        name = forced_name["name"]
        audit_log = profile["audit_log"]

        matching_log_entries = [l for l in audit_log if l["power"] == name]
        self.assertTrue(matching_log_entries, "the forced terminal never reached audit_log")
        # Every encounter of this power was forced to the terminal, so
        # every one of its audit_log entries must show it — not merely
        # the first — confirming there is no unforced, legitimate
        # encounter of the same power hiding among them.
        for entry in matching_log_entries:
            self.assertEqual(entry["status"], "grounding_unavailable")
            self.assertEqual(entry["unavailable_cause"], CAUSE_NO_LEGITIMATE_CANDIDATE)

        # The governed rule, reconstructed directly from audit_log in the
        # same order audit_and_take applies it: a grounding_unavailable
        # entry contributes nothing; anything else contributes its
        # transposed_to (or itself), deduplicated. This is what the fix
        # in mythos_sync.py::audit_and_take is required to produce, and it
        # is checked here regardless of which power was forced or how
        # many times, and regardless of what any other power's legitimate
        # grounding target happens to be.
        expected_approved = []
        for entry in audit_log:
            if entry["status"] == "grounding_unavailable":
                continue
            final = entry["transposed_to"] or entry["power"]
            if final not in expected_approved:
                expected_approved.append(final)

        self.assertEqual(
            expected_approved,
            profile["approved_powers"],
            "approved_powers does not match the governed reconstruction from audit_log "
            "(a grounding_unavailable entry must never contribute) — a terminal result "
            "may have been promoted",
        )


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
