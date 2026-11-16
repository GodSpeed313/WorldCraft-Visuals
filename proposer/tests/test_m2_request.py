"""IMP-001 M2 request shape (A4) and the fail-closed spending guard (A5, negative test 1)."""

from __future__ import annotations

import ast
import dataclasses
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from proposer.m2_config import COMMITTED_CONFIG, EXPECTED_PACKET_SHA256, Rates
from proposer.m2_request import SYSTEM_PROMPT, SpendGuardError, build_request, cost_report, enforce_spend_guard
from proposer.packet import AUTHORIZED_CHARACTERS, CHARACTER_DIR, REPO_ROOT, REQUIREMENTS_PATH, SCHEMA_PATH, build_packet
from proposer.tests.m2_support import VERIFIED_RATES

CAP = Decimal("2.00")


def real_packet():
    c = REPO_ROOT / CHARACTER_DIR
    return build_packet(c / "ilse_marrow.json", c / "sable_quillon.json", REPO_ROOT / REQUIREMENTS_PATH, REPO_ROOT / SCHEMA_PATH)


class RequestShapeTests(unittest.TestCase):
    def setUp(self):
        self.packet = real_packet()
        self.bundle = build_request(self.packet, COMMITTED_CONFIG)

    def test_approved_configuration_is_what_is_sent(self):
        body = self.bundle.generation_body
        self.assertEqual(body["model"], "claude-opus-5-5")
        self.assertEqual(body["max_tokens"], 32000)
        self.assertEqual(body["thinking"], {"type": "adaptive"})
        self.assertEqual(COMMITTED_CONFIG.spend_cap_usd, CAP)
        self.assertEqual(COMMITTED_CONFIG.prepaid_backstop_usd, Decimal("5"))
        self.assertEqual(COMMITTED_CONFIG.pair, ("ilse_marrow", "sable_quillon"))

    def test_temperature_and_every_other_sampling_parameter_is_omitted_and_that_is_recorded(self):
        body = self.bundle.generation_body
        for key in ("temperature", "top_p", "top_k"):
            self.assertNotIn(key, body)
        self.assertEqual(self.bundle.parameters["temperature"], "OMITTED (not sent)")

    def test_the_packet_keeps_its_exact_bytes_and_hash(self):
        self.assertEqual(self.packet.packet_sha256, EXPECTED_PACKET_SHA256)
        self.assertEqual(self.bundle.packet_sha256_recomputed, EXPECTED_PACKET_SHA256)
        self.assertEqual(self.bundle.generation_body["messages"][0]["content"].encode("utf-8"), self.packet.canonical_bytes)

    def test_the_bytes_sent_hash_to_the_recorded_request_hash(self):
        import hashlib
        self.assertEqual(hashlib.sha256(self.bundle.generation_bytes).hexdigest(), self.bundle.generation_sha256)
        self.assertEqual(json.loads(self.bundle.generation_bytes), self.bundle.generation_body)

    def test_the_system_prompt_is_fixed_and_pair_neutral(self):
        for banned in ("ilse", "sable", "marrow", "quillon", "tamsin", "pell", "dunmore", "tone", "cartograph", "fusion"):
            self.assertNotIn(banned, SYSTEM_PROMPT.lower())
        self.assertEqual(self.bundle.generation_body["system"], SYSTEM_PROMPT)

    def test_the_token_count_request_carries_the_thinking_configuration_and_the_same_content(self):
        count = json.loads(self.bundle.count_bytes)
        gen = self.bundle.generation_body
        self.assertEqual(count["thinking"], {"type": "adaptive"})
        for key in ("model", "system", "messages", "thinking"):
            self.assertEqual(count[key], gen[key])
        self.assertEqual(set(gen) - set(count), {"max_tokens", "stream"})

    def test_the_four_development_characters_are_the_only_authorized_ones(self):
        self.assertEqual(set(AUTHORIZED_CHARACTERS), {"ilse_marrow", "sable_quillon", "tamsin_vey", "pell_dunmore"})

    def test_a_different_pair_changes_the_packet_hash(self):
        c = REPO_ROOT / CHARACTER_DIR
        other = build_packet(c / "tamsin_vey.json", c / "pell_dunmore.json", REPO_ROOT / REQUIREMENTS_PATH, REPO_ROOT / SCHEMA_PATH)
        self.assertNotEqual(other.packet_sha256, EXPECTED_PACKET_SHA256)


class SpendGuardTests(unittest.TestCase):
    def report(self, tokens, rates=VERIFIED_RATES, max_tokens=32000, cap=CAP):
        return cost_report(tokens, max_tokens, rates, cap)

    def test_upper_bound_formula_is_exact(self):
        r = self.report(15000)
        self.assertEqual(Decimal(r["upper_bound_usd"]), Decimal("0.70"))        # 15000*4/1e6 + 32000*20/1e6
        self.assertTrue(r["generation_permitted"])
        enforce_spend_guard(r)

    # --- negative test 1: a bound above $2.00 prevents generation ---

    def test_the_cap_is_inclusive_and_one_token_over_is_refused(self):
        at_cap = self.report(340_000)                                           # exactly 1.36 + 0.64 = 2.00
        self.assertEqual(Decimal(at_cap["upper_bound_usd"]), CAP)
        enforce_spend_guard(at_cap)
        over = self.report(340_001)
        self.assertFalse(over["generation_permitted"])
        with self.assertRaisesRegex(SpendGuardError, "exceeds"):
            enforce_spend_guard(over)

    def test_the_bound_covers_the_full_output_allowance_not_just_the_input(self):
        r = self.report(0)
        self.assertEqual(Decimal(r["upper_bound_usd"]), Decimal("0.64"))
        big_output = self.report(0, max_tokens=128_000)
        self.assertFalse(big_output["generation_permitted"])

    def test_unverified_rates_fail_closed_even_when_the_bound_is_small(self):
        # explicit unverified fixtures; the committed rates are now verified, so they are not relied on here
        unverified_committed = dataclasses.replace(COMMITTED_CONFIG.rates, verified=False, verified_on=None)
        for rates in (dataclasses.replace(VERIFIED_RATES, verified=False), unverified_committed):
            r = self.report(1000, rates=rates)
            self.assertTrue(r["within_cap"])
            self.assertFalse(r["generation_permitted"])
            with self.assertRaisesRegex(SpendGuardError, "not verified"):
                enforce_spend_guard(r)

    def test_missing_pricing_fails_closed(self):
        for rates in (Rates(None, Decimal("20"), "x", None, True), Rates(Decimal("4"), None, "x", None, True), Rates(None, None, "x", None, False)):
            r = self.report(1000, rates=rates)
            self.assertIsNone(r["upper_bound_usd"])
            with self.assertRaisesRegex(SpendGuardError, "pricing is unavailable"):
                enforce_spend_guard(r)

    def test_an_unusable_token_count_fails_closed(self):
        for bad in (None, True, -1, "5", 1.5):
            r = self.report(bad)
            self.assertFalse(r["generation_permitted"], bad)
            with self.assertRaises(SpendGuardError):
                enforce_spend_guard(r)

    def test_the_guard_trusts_only_an_explicit_permission_flag(self):
        for forged in ({}, {"within_cap": True}, {"generation_permitted": "yes"}, {"generation_permitted": True, "refusal_reason": "x"}):
            with self.assertRaises(SpendGuardError):
                enforce_spend_guard(forged)

    def test_rates_record_their_source_and_verification_state(self):
        url = "https://platform.claude.com/docs/en/about-claude/pricing"
        r = self.report(1000, rates=COMMITTED_CONFIG.rates)          # the committed, verified rates
        self.assertEqual(r["rates_source"], url)
        self.assertIs(r["rates_verified"], True)
        self.assertEqual(r["rates_verified_on"], "2026-11-15")
        # and an unverified state is recorded as unverified, never as verified
        unverified = dataclasses.replace(COMMITTED_CONFIG.rates, verified=False, verified_on=None)
        r = self.report(1000, rates=unverified)
        self.assertEqual(r["rates_source"], url)
        self.assertIs(r["rates_verified"], False)
        self.assertIsNone(r["rates_verified_on"])


class StandardLibraryOnlyTests(unittest.TestCase):
    """A1: no SDK and no third-party dependency in the harness."""

    ALLOWED_LOCAL = {"proposer", "fusion_synthesis", "fusion_engine"}

    def test_harness_modules_import_only_the_standard_library_and_this_repository(self):
        for path in sorted(Path(REPO_ROOT, "proposer").glob("m2_*.py")) + sorted(Path(REPO_ROOT, "proposer", "tests").glob("*m2_*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                        [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else []
                for name in names:
                    top = name.split(".")[0]
                    self.assertTrue(top in sys.stdlib_module_names or top in self.ALLOWED_LOCAL, f"{path.name} imports {name}")

    def test_no_sdk_is_loaded_by_importing_the_harness(self):
        import proposer.m2_harness  # noqa: F401
        for banned in ("anthropic", "requests", "httpx", "httpx2", "urllib3", "aiohttp"):
            self.assertNotIn(banned, sys.modules)


if __name__ == "__main__":
    unittest.main()
