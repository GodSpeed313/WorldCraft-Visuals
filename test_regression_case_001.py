"""
Regression Case 001 protection — Hashirama Senju x William Vangeance.

Standard library only (unittest). No install step required.

Authorized by AUTH-006 (docs/authorizations.md). Regression Case 001 is the
preserved exhibit docs/evidence/regression_case_001.json (MSF-001): two
unrecognized inputs were silently defaulted to GROUNDED with the "unknown" tag
and a full profile was generated anyway, its own lore_summary naming
"Unknown Entity" twice.

This file holds two kinds of test, kept in separate classes on purpose:

  PERMANENT INVARIANTS (RegressionCase001DetectorTests,
  RegressionCase001EngineInvariantTests)
      Reject the original failure signatures. They never assert on the result's
      `state`, never require either character to stay unregistered, and never
      forbid an extra result key, so a future authorized resolver that returns
      a legitimately resolved result (or a CAUTIONARY result that carries a
      `reason`) still passes them.

  BASELINE (RegressionCase001BaselineAt4cedae0)
      Records what the engine does today. It is expected to change only under a
      future authorization.

The exhibit is only read, never regenerated. Nothing here calls save_to_matrix
or export_for_web, so containment_matrix.json is never touched.
"""

import contextlib
import io
import json
import random
import unittest
from pathlib import Path

from modality_classifier import CHARACTER_REGISTRY, classify_fusion
from mythos_sync import build_legacy_profile


EXHIBIT_PATH = (
    Path(__file__).resolve().parent / "docs" / "evidence" / "regression_case_001.json"
)

# The exact set the original default path produced. Supplementary only: the
# original power draw was random (docs/evidence/README.md), so this rejects that
# one draw, not the failure mode. The grounded/"unknown" signature and the lore
# check below are what protect against the failure mode.
FORBIDDEN_POWER_SET = frozenset(
    {"Espionage", "One-Inch Punch", "Psychological Mastery"}
)

# Fields only a generated profile carries. A CAUTIONARY result must hold none of
# them. This is a denylist, not an allowlist of permitted keys, so a future
# CAUTIONARY result that adds a `reason` key is not rejected.
GENERATED_PROFILE_FIELDS = (
    "approved_powers",
    "power_families",
    "dominant_family",
    "signature_ability",
    "influence_pattern",
    "rhetorical_style",
    "lore_summary",
    "audit_log",
    "biome",
)

SIG_GROUNDED_UNKNOWN = "grounded-with-unknown-tag"
SIG_LORE = "lore-names-unknown-entity"
SIG_POWER_SET = "exact-forbidden-power-set"
SIG_CAUTIONARY_FIELD = "cautionary-with-generated-field"


def forbidden_signatures(result: dict) -> list:
    """Return the Regression Case 001 failure signatures present in `result`.

    An empty list means none were found. The function reads the result only; it
    makes no assumption about which `state` a legitimate result carries.
    """
    found = []

    tags = result.get("tags")
    if not isinstance(tags, (list, tuple)):
        tags = []
    if result.get("modality") == "GROUNDED" and "unknown" in tags:
        found.append(SIG_GROUNDED_UNKNOWN)

    lore = result.get("lore_summary")
    if isinstance(lore, str) and "Unknown Entity" in lore:
        found.append(SIG_LORE)

    powers = result.get("approved_powers")
    if isinstance(powers, (list, tuple, set, frozenset)):
        if frozenset(powers) == FORBIDDEN_POWER_SET:
            found.append(SIG_POWER_SET)

    if result.get("state") == "CAUTIONARY":
        for field in GENERATED_PROFILE_FIELDS:
            if field in result:
                found.append(f"{SIG_CAUTIONARY_FIELD}:{field}")

    return found


def run_quietly(fn, *args):
    """Call `fn` with console output suppressed and random state controlled.

    The global random state is saved, seeded deterministically, and restored
    afterwards. The current CAUTIONARY path consumes no randomness; seeding is
    here so a future resolved path that does is still exercised once, from a
    fixed state, rather than by repeated trials.
    """
    saved_state = random.getstate()
    random.seed(0)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return fn(*args)
    finally:
        random.setstate(saved_state)


def load_exhibit() -> dict:
    with open(EXHIBIT_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    return records[0]


class _ExhibitCase(unittest.TestCase):
    """Loads the preserved exhibit and derives the exact regression inputs."""

    @classmethod
    def setUpClass(cls):
        cls.exhibit = load_exhibit()
        names = cls.exhibit["fusion_name"].split(" x ")
        if len(names) != 2:
            raise AssertionError(
                f"exhibit fusion_name does not split into two inputs: "
                f"{cls.exhibit['fusion_name']!r}"
            )
        cls.alpha, cls.beta = names
        cls.dominance = cls.exhibit["dominance"]


# ------------------------------------------------------------------
class RegressionCase001DetectorTests(_ExhibitCase):
    """Permanent: the detector recognizes the original failure and nothing else."""

    def test_inputs_are_derived_from_the_preserved_exhibit(self):
        self.assertEqual(self.alpha, "Hashirama Senju")
        self.assertEqual(self.beta, "William Vangeance")
        self.assertEqual(self.dominance, 50)

    def test_detector_identifies_every_exhibit_failure_signature(self):
        # The detector must not pass vacuously: run against the original record.
        self.assertEqual(
            set(forbidden_signatures(self.exhibit)),
            {SIG_GROUNDED_UNKNOWN, SIG_LORE, SIG_POWER_SET},
        )

    def test_grounded_alone_is_not_the_prohibited_combination(self):
        result = {"modality": "GROUNDED", "tags": ["shinobi"]}
        self.assertEqual(forbidden_signatures(result), [])

    def test_unknown_tag_alone_is_not_the_prohibited_combination(self):
        for modality in (None, "LEGACY", "HIGH_CONCEPT"):
            with self.subTest(modality=modality):
                result = {"modality": modality, "tags": ["unknown"]}
                self.assertEqual(forbidden_signatures(result), [])

    def test_lore_without_the_unknown_entity_phrase_is_not_flagged(self):
        result = {"lore_summary": "Born from the tension between two named lineages."}
        self.assertEqual(forbidden_signatures(result), [])

    def test_a_single_forbidden_power_is_not_flagged(self):
        for power in sorted(FORBIDDEN_POWER_SET):
            with self.subTest(power=power):
                self.assertEqual(forbidden_signatures({"approved_powers": [power]}), [])

    def test_a_larger_set_containing_the_forbidden_set_is_not_flagged(self):
        powers = sorted(FORBIDDEN_POWER_SET) + ["Fire"]
        self.assertEqual(forbidden_signatures({"approved_powers": powers}), [])

    def test_power_set_match_ignores_order_and_duplicates(self):
        powers = ["Psychological Mastery", "Espionage", "One-Inch Punch", "Espionage"]
        self.assertEqual(
            forbidden_signatures({"approved_powers": powers}), [SIG_POWER_SET]
        )

    def test_every_denylisted_field_is_flagged_on_a_cautionary_result(self):
        for field in GENERATED_PROFILE_FIELDS:
            with self.subTest(field=field):
                result = {"state": "CAUTIONARY", "modality": None, field: "x"}
                self.assertEqual(
                    forbidden_signatures(result),
                    [f"{SIG_CAUTIONARY_FIELD}:{field}"],
                )

    def test_denylisted_fields_are_not_flagged_on_a_non_cautionary_result(self):
        # Permanent protection does not depend on the current CAUTIONARY baseline.
        result = {
            "state": "RESOLVED",
            "modality": "GROUNDED",
            "tags": ["shinobi"],
            "approved_powers": ["Fire", "Wood Release"],
            "biome": "Hidden Village",
        }
        self.assertEqual(forbidden_signatures(result), [])

    def test_a_reason_field_on_a_cautionary_result_is_not_flagged(self):
        result = {
            "fusion_name": "A x B",
            "state": "CAUTIONARY",
            "modality": None,
            "reason": "unresolved input",
        }
        self.assertEqual(forbidden_signatures(result), [])


# ------------------------------------------------------------------
class RegressionCase001EngineInvariantTests(_ExhibitCase):
    """Permanent: the engine never reproduces the original failure.

    These assert only that no failure signature is present. They do not assert
    on `state`, and do not require either character to remain unregistered, so
    they stay valid after a future authorized resolver changes the path.
    """

    def test_build_legacy_profile_carries_no_failure_signature(self):
        result = run_quietly(build_legacy_profile, self.alpha, self.beta, self.dominance)
        self.assertEqual(forbidden_signatures(result), [])

    def test_classify_fusion_carries_no_failure_signature(self):
        result = run_quietly(classify_fusion, self.alpha, self.beta, self.dominance)
        self.assertEqual(forbidden_signatures(result), [])


# ------------------------------------------------------------------
class RegressionCase001BaselineAt4cedae0(_ExhibitCase):
    """Baseline: records the engine's behavior at commit 4cedae0.

    At 4cedae0 neither exhibit input is in CHARACTER_REGISTRY, so the fusion is
    CAUTIONARY, carries no modality, and generates no profile (Ruling 001 §4,
    implemented under AUTH-003 at c7f0ab7).

    These tests describe the CURRENT implementation, not a permanent rule. A
    future authorized resolver change may legitimately change this behavior, and
    would then require a separately authorized modification of this existing
    baseline test. The permanent invariants above are what must keep holding.
    """

    def _assert_baseline_premise(self):
        for name in (self.alpha, self.beta):
            self.assertNotIn(
                name,
                CHARACTER_REGISTRY,
                f"baseline premise changed: {name!r} is now registered, so the "
                f"4cedae0 CAUTIONARY baseline no longer describes this input",
            )

    def test_build_legacy_profile_is_cautionary_with_no_generated_profile(self):
        """Baseline at 4cedae0: CAUTIONARY, no modality, no generated profile."""
        self._assert_baseline_premise()
        result = run_quietly(build_legacy_profile, self.alpha, self.beta, self.dominance)
        self.assertEqual(result["state"], "CAUTIONARY")
        self.assertIsNone(result["modality"])
        for field in GENERATED_PROFILE_FIELDS:
            with self.subTest(field=field):
                self.assertNotIn(field, result)

    def test_classify_fusion_is_cautionary_with_no_modality(self):
        """Baseline at 4cedae0: the fusion classification halts as CAUTIONARY."""
        self._assert_baseline_premise()
        result = run_quietly(classify_fusion, self.alpha, self.beta, self.dominance)
        self.assertEqual(result["state"], "CAUTIONARY")
        self.assertIsNone(result["modality"])


if __name__ == "__main__":
    unittest.main()
