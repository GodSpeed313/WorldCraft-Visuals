# =============================================================
#  MYTHOS-SYNC FRAMEWORK — TEST SUITE
#  Standard library only (unittest). No install step required.
#      python -m unittest -v
# =============================================================

import contextlib
import io
import itertools
import os
import random
import tempfile
import unittest

import mythos_sync
from logic_auditor import (
    MODALITY_RANK,
    POWER_FAMILIES,
    POWER_REGISTRY,
    TRANSPOSITION_MAP,
    audit_power,
    family_members,
    family_of,
)
from modality_classifier import CHARACTER_REGISTRY, classify, classify_fusion
from mythos_sync import POWER_POOL, TAG_POWER_MAP, build_legacy_profile

ALL_MODALITIES = ("LEGACY", "GROUNDED", "HIGH_CONCEPT")


def quiet(fn, *args, **kwargs):
    """Run fn with stdout swallowed — the engine narrates heavily."""
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def is_legal(power: str, modality: str) -> bool:
    """True if `power` is permitted for a fusion of `modality`."""
    return MODALITY_RANK[POWER_REGISTRY[power]["min_modality"]] <= MODALITY_RANK[modality]


# ------------------------------------------------------------------
class TestModalityClassifier(unittest.TestCase):

    def test_known_character_keeps_its_registry_modality(self):
        self.assertEqual(classify("Bruce Lee")["modality"], "LEGACY")
        self.assertEqual(classify("James Bond")["modality"], "GROUNDED")
        self.assertEqual(classify("Vash")["modality"], "HIGH_CONCEPT")

    def test_unknown_character_defaults_to_grounded(self):
        unknown = quiet(classify, "Some Nobody")
        self.assertEqual(unknown["modality"], "GROUNDED")
        self.assertEqual(unknown["tags"], ["unknown"])

    def test_high_dominance_takes_alpha_modality(self):
        # Malcolm X (LEGACY) dominating Vash (HIGH_CONCEPT) stays LEGACY.
        fusion = quiet(classify_fusion, "Malcolm X", "Vash", 80)
        self.assertEqual(fusion["modality"], "LEGACY")
        self.assertIn("Malcolm X", fusion["dominant"])

    def test_low_dominance_takes_beta_modality(self):
        fusion = quiet(classify_fusion, "Malcolm X", "Vash", 20)
        self.assertEqual(fusion["modality"], "HIGH_CONCEPT")
        self.assertIn("Vash", fusion["dominant"])

    def test_balanced_dominance_takes_the_higher_modality(self):
        fusion = quiet(classify_fusion, "Bruce Lee", "Maka", 50)
        self.assertEqual(fusion["modality"], "HIGH_CONCEPT")
        self.assertEqual(fusion["dominant"], "balanced blend")

    def test_fusion_inherits_tags_from_both_characters(self):
        fusion = quiet(classify_fusion, "Bruce Lee", "Maka", 50)
        self.assertIn("martial_arts", fusion["tags"])   # Bruce Lee
        self.assertIn("soul_resonance", fusion["tags"])  # Maka


# ------------------------------------------------------------------
class TestLogicAuditor(unittest.TestCase):

    LEGACY_FUSION = {
        "fusion_name": "Test Fusion",
        "modality": "LEGACY",
        "dominant": "test",
        "tags": [],
    }

    def test_legal_power_is_approved_untouched(self):
        result = audit_power("Strategic Genius", self.LEGACY_FUSION)
        self.assertIsNone(result["transposed_to"])
        self.assertIn("APPROVED", result["status"])

    def test_illegal_power_is_transposed(self):
        result = audit_power("Domain Expansion", self.LEGACY_FUSION)
        self.assertIn("TRANSPOSED", result["status"])
        self.assertIn(result["transposed_to"], TRANSPOSITION_MAP["Domain Expansion"])
        self.assertTrue(is_legal(result["transposed_to"], "LEGACY"))

    def test_unregistered_power_is_flagged_unverified(self):
        result = audit_power("Hypernova Fist", self.LEGACY_FUSION)
        self.assertIn("UNVERIFIED", result["status"])
        self.assertIsNone(result["transposed_to"])

    def test_every_transposition_target_is_a_registered_power(self):
        for source, targets in TRANSPOSITION_MAP.items():
            for target in targets:
                with self.subTest(source=source, target=target):
                    self.assertIn(target, POWER_REGISTRY)

    def test_every_power_has_at_least_one_universal_fallback(self):
        """Every entry must contain a LEGACY-tier power, otherwise a LEGACY
        fusion has nothing legal to ground to and hits the blanket default."""
        for source, targets in TRANSPOSITION_MAP.items():
            with self.subTest(source=source):
                self.assertTrue(
                    any(is_legal(t, "LEGACY") for t in targets),
                    f"{source} cannot be grounded for a LEGACY fusion",
                )

    def test_transposition_never_yields_an_illegal_power(self):
        """Regression guard: Soul Resonance -> Kinetic Mastery grounded a
        HIGH_CONCEPT power only as far as GROUNDED, which still leaked an
        illegal power into LEGACY profiles. Repeated because grounding now
        picks at random among equally-ranked candidates."""
        random.seed(21)
        for modality in ALL_MODALITIES:
            fusion = dict(self.LEGACY_FUSION, modality=modality)
            for power in POWER_REGISTRY:
                with self.subTest(modality=modality, power=power):
                    for _ in range(20):
                        result = audit_power(power, fusion)
                        final = result["transposed_to"] or result["power"]
                        self.assertTrue(
                            is_legal(final, modality),
                            f"{power} -> {final} is illegal for {modality}",
                        )

    def test_grounding_keeps_the_richest_legal_tier(self):
        """A power should fall only as far as it must: Soul Resonance stays
        GROUNDED for a GROUNDED fusion, but drops to LEGACY for a LEGACY one."""
        grounded = dict(self.LEGACY_FUSION, modality="GROUNDED")
        self.assertEqual(
            audit_power("Soul Resonance", grounded)["transposed_to"],
            "Kinetic Mastery",
        )
        # At LEGACY it has to fall further, but stays in DISCIPLINE — before
        # the rebalance it landed on Art of War, i.e. became a strategist.
        legacy_target = audit_power("Soul Resonance", self.LEGACY_FUSION)["transposed_to"]
        self.assertIn(legacy_target, ("Adaptive Combat", "Martial Perfection"))
        self.assertEqual(family_of(legacy_target), family_of("Soul Resonance"))

    def test_grounding_is_not_always_the_same_power(self):
        """The whole point of the widened map: a LEGACY fusion should not
        funnel every illegal power into one stand-in."""
        random.seed(22)
        targets = set()
        for power in POWER_REGISTRY:
            for _ in range(30):
                result = audit_power(power, self.LEGACY_FUSION)
                if result["transposed_to"]:
                    targets.add(result["transposed_to"])
        self.assertGreaterEqual(
            len(targets), 4,
            f"grounding collapsed onto too few powers: {sorted(targets)}",
        )

    def test_legacy_powers_are_legal_at_every_modality(self):
        for power in POWER_POOL["LEGACY"]:
            for modality in ALL_MODALITIES:
                with self.subTest(power=power, modality=modality):
                    self.assertTrue(is_legal(power, modality))


# ------------------------------------------------------------------
class TestPowerFamilies(unittest.TestCase):
    """Families are the semantic layer that tension and philosophy will read."""

    def test_every_power_declares_a_known_family(self):
        for power, entry in POWER_REGISTRY.items():
            with self.subTest(power=power):
                self.assertIn("family", entry)
                self.assertIn(entry["family"], POWER_FAMILIES)

    def test_family_of_returns_none_for_unregistered_power(self):
        self.assertIsNone(family_of("Hypernova Fist"))

    def test_family_members_respects_the_modality_ceiling(self):
        for family in POWER_FAMILIES:
            legacy_only = family_members(family, "LEGACY")
            everything = family_members(family)
            with self.subTest(family=family):
                self.assertTrue(set(legacy_only).issubset(everything))
                for power in legacy_only:
                    self.assertTrue(is_legal(power, "LEGACY"))

    def test_families_partition_the_registry(self):
        counted = sum(len(family_members(f)) for f in POWER_FAMILIES)
        self.assertEqual(counted, len(POWER_REGISTRY))

    def test_every_family_can_ground_to_itself_at_legacy(self):
        """Was an expectedFailure: PERCEPTION had no LEGACY-tier power, so
        Espionage had to leave its family entirely when grounded. Closed by
        the registry rebalance."""
        for family in POWER_FAMILIES:
            with self.subTest(family=family):
                self.assertTrue(
                    family_members(family, "LEGACY"),
                    f"{family} has no LEGACY-tier power to ground into",
                )

    def test_grounding_prefers_a_relative_when_one_is_legal(self):
        """Titan-Shifting is DISCIPLINE; grounded at LEGACY it should land on
        a DISCIPLINE power rather than drifting to another family."""
        random.seed(31)
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        for _ in range(20):
            target = audit_power("Titan-Shifting", fusion)["transposed_to"]
            self.assertEqual(family_of(target), family_of("Titan-Shifting"))

    def test_unmapped_power_grounds_through_its_family(self):
        """Powers with no TRANSPOSITION_MAP entry fall back to family rather
        than the blanket default list."""
        random.seed(32)
        fusion = {"fusion_name": "t", "modality": "LEGACY", "dominant": "", "tags": []}
        # Angelic Override is INFLUENCE and mapped; strip the entry to prove
        # the family path alone produces a same-family, legal result.
        original = TRANSPOSITION_MAP.pop("Angelic Override")
        try:
            for _ in range(10):
                target = audit_power("Angelic Override", fusion)["transposed_to"]
                self.assertTrue(is_legal(target, "LEGACY"))
                self.assertEqual(family_of(target), "INFLUENCE")
        finally:
            TRANSPOSITION_MAP["Angelic Override"] = original


# ------------------------------------------------------------------
class TestRegistryIntegrity(unittest.TestCase):

    def test_transposition_preserves_family(self):
        """Grounding changes a power's EXPRESSION, not its essence. Espionage
        becoming Strategic Genius turned a perceptive person into a strategist;
        it should become Situational Awareness instead."""
        for source, targets in TRANSPOSITION_MAP.items():
            for target in targets:
                with self.subTest(source=source, target=target):
                    self.assertEqual(
                        family_of(target), family_of(source),
                        f"{source} ({family_of(source)}) grounds to "
                        f"{target} ({family_of(target)})",
                    )

    def test_every_power_is_reachable_from_some_tag(self):
        """A power no tag routes to can only arrive via the single random
        universal slot — more combinations carrying less meaning."""
        routed = {p for powers in TAG_POWER_MAP.values() for p in powers}
        for power in POWER_REGISTRY:
            with self.subTest(power=power):
                self.assertIn(power, routed)

    def test_no_family_dominates_the_legacy_tier(self):
        """The skew that made 91% of LEGACY fusions read as strategists."""
        legacy = [p for p in POWER_REGISTRY if is_legal(p, "LEGACY")]
        for family in POWER_FAMILIES:
            share = len([p for p in legacy if family_of(p) == family]) / len(legacy)
            with self.subTest(family=family):
                self.assertLessEqual(share, 0.40, f"{family} is {share:.0%} of LEGACY")

    def test_tag_power_map_only_references_registered_powers(self):
        """Unregistered powers are silently dropped during selection, so a
        typo here would quietly shrink a tag's thematic pool."""
        for tag, powers in TAG_POWER_MAP.items():
            for power in powers:
                with self.subTest(tag=tag, power=power):
                    self.assertIn(power, POWER_REGISTRY)

    def test_power_pools_only_reference_registered_powers(self):
        for modality, powers in POWER_POOL.items():
            for power in powers:
                with self.subTest(modality=modality, power=power):
                    self.assertIn(power, POWER_REGISTRY)

    def test_power_pool_entries_are_legal_for_their_own_modality(self):
        for modality, powers in POWER_POOL.items():
            for power in powers:
                with self.subTest(modality=modality, power=power):
                    self.assertTrue(is_legal(power, modality))


# ------------------------------------------------------------------
class TestPowerSelection(unittest.TestCase):
    """The pipeline-level invariants — where the pre-filter bug lived."""

    def test_no_profile_ever_holds_an_illegal_power(self):
        """Sweeps every ordered character pair at three dominance levels."""
        random.seed(1)
        checked = 0
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            for dominance in (10, 50, 80):
                profile = quiet(build_legacy_profile, alpha, beta, dominance)
                checked += 1
                for power in profile["approved_powers"]:
                    self.assertTrue(
                        is_legal(power, profile["modality"]),
                        f"{profile['fusion_name']} [{profile['modality']}] "
                        f"illegally holds {power}",
                    )
        self.assertGreater(checked, 300)

    def test_illegal_powers_still_reach_the_auditor(self):
        """Regression guard: build_legacy_profile() once filtered illegal
        powers out of the thematic pool before audit_power() saw them, which
        made the whole transposition system unreachable dead code."""
        random.seed(0)
        considered = set()
        for _ in range(50):
            profile = quiet(build_legacy_profile, "Malcolm X", "Vash", 80)
            self.assertEqual(profile["modality"], "LEGACY")
            considered.update(entry["power"] for entry in profile["audit_log"])

        illegal = {p for p in considered if not is_legal(p, "LEGACY")}
        self.assertTrue(
            illegal,
            "no power above the LEGACY ceiling ever reached the auditor — "
            "the thematic pool is being pre-filtered again",
        )

    def test_transposition_actually_fires_in_the_pipeline(self):
        random.seed(0)
        fired = 0
        for _ in range(50):
            profile = quiet(build_legacy_profile, "Malcolm X", "Vash", 80)
            if any(e["transposed_to"] for e in profile["audit_log"]):
                fired += 1
        self.assertGreater(fired, 0, "Grounding Filter never fired")

    def test_every_profile_holds_at_least_two_powers(self):
        """Transposition can collapse several powers onto one target, so
        selection has to keep drawing until it holds two distinct ones."""
        random.seed(2)
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            profile = quiet(build_legacy_profile, alpha, beta, 50)
            with self.subTest(fusion=profile["fusion_name"]):
                self.assertGreaterEqual(len(profile["approved_powers"]), 2)

    def test_powers_are_deduplicated(self):
        random.seed(3)
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            profile = quiet(build_legacy_profile, alpha, beta, 80)
            powers = profile["approved_powers"]
            with self.subTest(fusion=profile["fusion_name"]):
                self.assertEqual(len(powers), len(set(powers)))

    def test_signature_ability_is_one_of_the_held_powers(self):
        random.seed(4)
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            profile = quiet(build_legacy_profile, alpha, beta, 50)
            with self.subTest(fusion=profile["fusion_name"]):
                self.assertIn(profile["signature_ability"], profile["approved_powers"])

    def test_profile_exposes_the_keys_the_dashboard_reads(self):
        random.seed(5)
        profile = quiet(build_legacy_profile, "Bruce Lee", "Maka", 50)
        for key in (
            "fusion_name", "modality", "dominant", "alpha", "beta", "dominance",
            "tags", "biome", "approved_powers", "power_families",
            "dominant_family", "signature_ability",
            "influence_pattern", "rhetorical_style", "lore_summary",
            "audit_log", "created_at",
        ):
            with self.subTest(key=key):
                self.assertIn(key, profile)

    def test_power_families_field_matches_the_held_powers(self):
        random.seed(8)
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            profile = quiet(build_legacy_profile, alpha, beta, 50)
            with self.subTest(fusion=profile["fusion_name"]):
                self.assertEqual(
                    set(profile["power_families"]), set(profile["approved_powers"])
                )
                self.assertIn(profile["dominant_family"], POWER_FAMILIES)
                self.assertIn(
                    profile["dominant_family"], profile["power_families"].values()
                )

    def test_biome_matches_the_fusion_modality(self):
        random.seed(6)
        for alpha, beta in itertools.permutations(CHARACTER_REGISTRY, 2):
            profile = quiet(build_legacy_profile, alpha, beta, 50)
            with self.subTest(fusion=profile["fusion_name"]):
                self.assertIn(profile["biome"], mythos_sync.BIOMES[profile["modality"]])

    def test_unknown_characters_still_produce_a_valid_profile(self):
        random.seed(7)
        profile = quiet(build_legacy_profile, "Nobody Special", "Vash", 50)
        self.assertGreaterEqual(len(profile["approved_powers"]), 2)
        for power in profile["approved_powers"]:
            self.assertTrue(is_legal(power, profile["modality"]))


# ------------------------------------------------------------------
class TestPersistence(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._original = mythos_sync.MATRIX_FILE
        mythos_sync.MATRIX_FILE = os.path.join(self._tmpdir.name, "matrix.json")

    def tearDown(self):
        mythos_sync.MATRIX_FILE = self._original
        self._tmpdir.cleanup()

    def test_missing_matrix_loads_as_empty(self):
        self.assertEqual(mythos_sync.load_matrix(), [])

    def test_saved_profile_round_trips(self):
        profile = {"fusion_name": "A x B", "signature_ability": "Strategic Genius"}
        quiet(mythos_sync.save_to_matrix, profile)
        self.assertEqual(mythos_sync.load_matrix(), [profile])

    def test_duplicate_profile_is_not_saved_twice(self):
        profile = {"fusion_name": "A x B", "signature_ability": "Strategic Genius"}
        quiet(mythos_sync.save_to_matrix, profile)
        quiet(mythos_sync.save_to_matrix, profile)
        self.assertEqual(len(mythos_sync.load_matrix()), 1)

    def test_same_fusion_with_a_different_signature_is_kept(self):
        quiet(mythos_sync.save_to_matrix,
              {"fusion_name": "A x B", "signature_ability": "Strategic Genius"})
        quiet(mythos_sync.save_to_matrix,
              {"fusion_name": "A x B", "signature_ability": "Art of War"})
        self.assertEqual(len(mythos_sync.load_matrix()), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
