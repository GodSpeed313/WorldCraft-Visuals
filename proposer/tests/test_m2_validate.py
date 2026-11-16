"""IMP-001 M2 mechanical validity: negative tests 11 and 12, plus positive controls."""

from __future__ import annotations

import json
import unittest

from proposer.m2_validate import INVALID, VALID, assess_reproducibility, validate_output
from proposer.tests.m2_support import load_cards, no_fusion_text, pair_file, proposal_text


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.a, self.b = load_cards()

    def check(self, text, stop="end_turn"):
        return validate_output(text, self.a, self.b, stop)

    # --- positive controls: a valid output must pass, or the INVALID tests prove nothing ---

    def test_valid_proposal_passes_every_check(self):
        r = self.check(proposal_text(self.a, self.b))
        self.assertEqual(r["verdict"], VALID, r["failed_checks"])
        self.assertEqual(r["outcome_type"], "proposal")
        self.assertGreaterEqual(len(r["checks"]), 10)
        self.assertEqual(r["parsed"]["declared_levels"], {"shared_structure": 3, "emergence": 2})

    def test_valid_no_fusion_report_with_three_and_with_one_candidate(self):
        self.assertEqual(self.check(no_fusion_text(self.a, self.b, 3))["verdict"], VALID)
        r = self.check(no_fusion_text(self.a, self.b, 1))
        self.assertEqual(r["verdict"], VALID, r["failed_checks"])

    def test_reversed_pair_order_in_the_pair_file_is_still_valid(self):
        pair = pair_file(self.b, self.a)          # same two characters, named in the other order
        pair["a"], pair["b"] = self.b.name, self.a.name
        r = self.check(proposal_text(self.a, self.b, pair=pair))
        self.assertEqual(r["verdict"], VALID, r["failed_checks"])

    # --- negative test 11: invalid proposer output is marked INVALID, with failed checks recorded ---

    def assertInvalid(self, text, check_name, stop="end_turn"):
        r = self.check(text, stop)
        self.assertEqual(r["verdict"], INVALID)
        self.assertIn(check_name, r["failed_checks"], r["failed_checks"])
        self.assertIsNone(r["parsed"])
        return r

    def test_truncated_output_is_invalid(self):
        self.assertInvalid(proposal_text(self.a, self.b), "complete_output", stop="max_tokens")

    def test_refusal_or_prose_is_invalid(self):
        self.assertInvalid("I can't help with that.", "template_structure", stop="refusal")
        self.assertInvalid("Sure! Here is a fusion.\nOUTCOME: proposal", "template_structure")

    def test_both_output_types_in_one_text_is_invalid(self):
        self.assertInvalid(proposal_text(self.a, self.b) + "\nSTATEMENT: no defensible fusion found", "single_output_type")

    def test_missing_or_misordered_heading_is_invalid(self):
        self.assertInvalid(proposal_text(self.a, self.b, unc=None), "template_structure")
        self.assertInvalid(proposal_text(self.a, self.b, levels="DECLARED PROVENANCE: Invented Bridge\nDECLARED LEVELS: shared structure 3; emergence 2",
                                         prov=None), "template_structure")

    def test_pair_file_that_is_not_json_or_fails_schema(self):
        self.assertInvalid(proposal_text(self.a, self.b, pair={}) .replace("{}", "{not json"), "pair_file_parses")
        bad = pair_file(self.a, self.b)
        del bad["fusion_name"]
        self.assertInvalid(proposal_text(self.a, self.b, pair=bad), "pair_file_schema")

    def test_unknown_property_id_cited_by_the_pair_file_fails_cross_validation(self):
        bad = pair_file(self.a, self.b)
        bad["interaction"]["dependency_ids"] = [self.a.properties[0].id, "sable_quillon.invented_property"]
        self.assertInvalid(proposal_text(self.a, self.b, pair=bad), "pair_file_cross_validation")

    def test_interaction_must_depend_on_both_parents(self):
        bad = pair_file(self.a, self.b)
        bad["interaction"]["dependency_ids"] = [self.a.properties[0].id, self.a.properties[1].id]
        self.assertInvalid(proposal_text(self.a, self.b, pair=bad), "interaction_depends_on_both_parents")

    def test_trait_outcomes_must_cover_every_property(self):
        bad = pair_file(self.a, self.b)
        bad["trait_outcomes"] = bad["trait_outcomes"][:-1]
        r = self.assertInvalid(proposal_text(self.a, self.b, pair=bad), "trait_outcomes_cover_all_properties")
        self.assertIn("missing", next(c["detail"] for c in r["checks"] if c["name"] == "trait_outcomes_cover_all_properties"))

    def test_explanation_must_cite_real_ids_from_both_parents(self):
        a0, b0 = self.a.properties[0].id, self.b.properties[0].id
        causal = lambda p1, p2: (f"CAUSAL EXPLANATION:\n  Parent 1 contribution (property ids): {p1}\n"
                                 f"  Parent 2 contribution (property ids): {p2}\n  Interaction: x\n  Beyond either parent? No.")
        self.assertInvalid(proposal_text(self.a, self.b, causal=causal(a0, "sable_quillon.no_such_thing")), "parent_contributions_cite_valid_ids")
        self.assertInvalid(proposal_text(self.a, self.b, causal=causal(a0, self.a.properties[1].id)), "citations_from_both_parents")
        self.assertInvalid(proposal_text(self.a, self.b, causal=causal("", b0)), "parent_contributions_cite_valid_ids")

    def test_every_limitation_must_name_a_source(self):
        self.assertInvalid(proposal_text(self.a, self.b, lims="LIMITATION SOURCES:\n  (none given)"), "limitations_sourced")
        self.assertInvalid(proposal_text(self.a, self.b, lims="LIMITATION SOURCES:\n  Works only where both conditions hold at once. -> ilse_marrow.nope"),
                           "limitations_sourced")

    def test_levels_and_provenance_must_be_declared_in_range(self):
        self.assertInvalid(proposal_text(self.a, self.b, levels="DECLARED LEVELS: shared structure 3; emergence 1"), "declared_levels_present")
        self.assertInvalid(proposal_text(self.a, self.b, levels="DECLARED LEVELS: unknown"), "declared_levels_present")
        for bad in ("Source-Derived", "Unresolved", ""):
            self.assertInvalid(proposal_text(self.a, self.b, prov=f"DECLARED PROVENANCE: {bad}"), "provenance_declared")

    def test_no_fusion_rejection_evidence_is_required(self):
        self.assertInvalid(no_fusion_text(self.a, self.b, stmt="STATEMENT: a fusion exists"), "template_structure")
        self.assertInvalid(no_fusion_text(self.a, self.b, 2, fewer=None), "fewer_than_three_explained")
        self.assertInvalid(no_fusion_text(self.a, self.b, cands="CANDIDATE 1: just a mechanism"), "candidates_each_rejected")
        self.assertInvalid(no_fusion_text(self.a, self.b, cands=f"CANDIDATE 1: m; failed test(s): 2; property ids: sable_quillon.nope"),
                           "candidate_property_ids_valid")
        same = "\n".join(f"CANDIDATE {i}: identical mechanism; failed test(s): 2; property ids: {self.a.properties[0].id}" for i in (1, 2, 3))
        self.assertInvalid(no_fusion_text(self.a, self.b, cands=same), "candidates_distinct")
        skipped = f"CANDIDATE 1: m1; failed test(s): 2; property ids: {self.a.properties[0].id}\nCANDIDATE 3: m3; failed test(s): 2; property ids: {self.a.properties[0].id}"
        self.assertInvalid(no_fusion_text(self.a, self.b, 2, cands=skipped), "candidate_count_and_numbering")

    def test_a_failed_output_is_never_repaired(self):
        text = proposal_text(self.a, self.b, unc=None)
        r = self.check(text)
        self.assertEqual(r["verdict"], INVALID)
        self.assertEqual(text, proposal_text(self.a, self.b, unc=None))   # input untouched; result carries no corrected text
        self.assertNotIn("repaired", json.dumps(r).lower())


class ReproducibilityTests(unittest.TestCase):
    def complete_record(self):
        return {"repo_commit_sha": "a" * 40, "harness_version": "h", "request_sent_utc": "t1", "response_complete_utc": "t2",
                "pair": ["x", "y"], "packet_sha256": "p", "packet_bytes_file": {"name": "n"}, "model_id": "m",
                "request_parameters": {"k": 1}, "request_body_sha256": "r", "raw_response_sha256": "s",
                "provider_request_id": "req", "stop_reason": "end_turn", "usage_input_tokens": 1, "usage_output_tokens": 2,
                "estimated_cost": {"x": 1}, "billed_cost_addendum": {"status": "PENDING"}, "attempt_history": [{"attempt": 1}],
                "retry_policy": "declared", "reservation": {"id": "r"}}

    # --- negative test 12 ---

    def test_complete_record_is_reproducible_and_pending_billing_is_not_missing(self):
        r = assess_reproducibility(self.complete_record(), "COMPLETE")
        self.assertEqual(r, {"verdict": "REPRODUCIBLE", "missing_fields": []})

    def test_each_missing_audit_field_makes_it_not_reproducible(self):
        for field in list(self.complete_record()):
            rec = self.complete_record()
            rec.pop(field)
            r = assess_reproducibility(rec, "COMPLETE")
            self.assertEqual(r["verdict"], "NOT REPRODUCIBLE", field)
            self.assertEqual(r["missing_fields"], [field])

    def test_empty_values_count_as_missing(self):
        rec = self.complete_record()
        rec["provider_request_id"] = None
        self.assertEqual(assess_reproducibility(rec, "COMPLETE")["missing_fields"], ["provider_request_id"])

    def test_response_fields_are_only_required_for_a_complete_response(self):
        rec = self.complete_record()
        for f in ("response_complete_utc", "raw_response_sha256", "provider_request_id", "stop_reason", "usage_input_tokens", "usage_output_tokens"):
            rec.pop(f)
        self.assertEqual(assess_reproducibility(rec, "AMBIGUOUS")["verdict"], "REPRODUCIBLE")
        self.assertEqual(assess_reproducibility(rec, "COMPLETE")["verdict"], "NOT REPRODUCIBLE")


if __name__ == "__main__":
    unittest.main()
