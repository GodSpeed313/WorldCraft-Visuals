"""
IMP-001 M2 harness end to end, against a scripted fake connection and a temp evidence root.
Negative tests 1, 2, 6, 7, 8, 9, 12, 14 and 15. No real network is reachable (see m2_support).
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import inspect
import io
import json
import os
import unittest
from pathlib import Path
from unittest import mock

from proposer import m2_harness
from proposer.m2_config import COMMITTED_CONFIG, EXPECTED_PACKET_SHA256
from proposer.m2_evidence import EvidenceError, EvidenceStore, RESERVATION_NAME, ReservationExists, RootRejected, SecretDetected
from proposer.m2_harness import BILLING_ADDENDUM, HarnessStop, RUN_RECORD, dry_run, run
from proposer.m2_provider import CountTokensStop
from proposer.m2_request import SpendGuardError
from proposer.packet import REPO_ROOT
from proposer.tests.m2_support import (COUNT_PATH, GEN_PATH, FakeFactory, M2TestCase, count_ok, fake_git, gen_ok, load_cards,
                                       proposal_text, no_fusion_text)

A, B = load_cards()
GOOD = proposal_text(A, B)
CONNECT_FAIL = {"connect_error": OSError("name resolution failed")}


class HarnessCase(M2TestCase):
    def do_run(self, *plans, cfg=None, **extra):
        factory = FakeFactory(*plans)
        out = run(cfg or self.cfg, **self.run_kwargs(factory, **extra))
        return out, factory

    def sha_of(self, name):
        return hashlib.sha256(Path(self.root, name).read_bytes()).hexdigest()


class HappyPathTests(HarnessCase):
    def test_a_valid_proposal_is_recorded_completely_and_the_three_verdicts_stay_separate(self):
        out, factory = self.do_run(count_ok(15000), gen_ok(GOOD, input_tokens=15000, output_tokens=1200))
        self.assertEqual((out["status"], out["valid"], out["reproducibility"]), ("COMPLETE", "VALID", "REPRODUCIBLE"))
        self.assertEqual(factory.paths(), [COUNT_PATH, GEN_PATH])

        rec = self.read_json(RUN_RECORD)
        self.assertEqual(rec["repo_commit_sha"], "a" * 40)
        self.assertEqual(rec["model_id"], "claude-opus-5-5")
        self.assertEqual(rec["packet_sha256"], EXPECTED_PACKET_SHA256)
        self.assertIs(rec["packet_sha256_matches_expected"], True)
        self.assertEqual(rec["request_parameters"]["thinking"], {"type": "adaptive"})
        self.assertEqual(rec["request_parameters"]["temperature"], "OMITTED (not sent)")
        self.assertEqual((rec["stop_reason"], rec["usage_input_tokens"], rec["usage_output_tokens"], rec["provider_request_id"]),
                         ("end_turn", 15000, 1200, "req_fake"))
        self.assertEqual(rec["estimated_cost"]["pre_send_upper_bound"]["upper_bound_usd"], "1.34")
        self.assertEqual(rec["estimated_cost"]["post_response_estimate_usd"], "0.084")       # 15000*4 + 1200*20, per 1e6
        self.assertEqual(rec["billed_cost_addendum"]["status"], "PENDING")
        self.assertIn("stricter than", rec["retry_policy"])
        self.assertEqual([a["outcome"] for a in rec["attempt_history"]], ["COMPLETE"])
        self.assertEqual(rec["reservation"]["sha256"], self.sha_of(RESERVATION_NAME))

        # every hash in the record is the hash of the file on disk
        for name, sha in rec["evidence_file_hashes"].items():
            self.assertEqual(sha, self.sha_of(name), name)
        # the request body recorded is byte-for-byte the body that was transmitted
        self.assertEqual(Path(self.root, "M2_REQUEST_BODY.json").read_bytes(), factory.generation_requests()[0]["body"])
        self.assertEqual(rec["request_body_sha256"], hashlib.sha256(factory.generation_requests()[0]["body"]).hexdigest())
        # raw response bytes preserved exactly
        self.assertEqual(rec["raw_response_sha256"], self.sha_of("M2_RESPONSE.raw"))

        addendum = self.read_json(BILLING_ADDENDUM)
        self.assertEqual((addendum["status"], addendum["billed_cost_usd"], addendum["references"]["sha256"]), ("PENDING", None, out["run_record_sha256"]))
        self.assertEqual(self.sha_of(RUN_RECORD), out["run_record_sha256"])

        verdict = self.read_json("M2_VERDICT.json")
        self.assertEqual(verdict["valid"]["verdict"], "VALID")
        self.assertEqual((verdict["defensible"]["status"], verdict["creative"]["status"]), ("PENDING_OPERATOR_REVIEW",) * 2)
        self.assertFalse({"score", "overall", "total", "combined"} & set(verdict), "verdicts must never be merged into one score")

    def test_card_first_review_files_keep_the_declarations_apart_from_the_card(self):
        self.do_run(count_ok(), gen_ok(GOOD))
        card = self.read_json("M2_REVIEW_CARD.json")
        decl = self.read_json("M2_REVIEW_DECLARATIONS.json")
        self.assertEqual(card["schema"], "fusion-synthesis-pair/1")
        self.assertNotIn("causal_explanation", card)
        self.assertEqual(decl["declared_levels"], {"shared_structure": 3, "emergence": 2})
        self.assertIn("causal_explanation", decl)
        self.assertNotIn("pair_file", decl)

    def test_a_valid_no_fusion_report_is_recorded_without_calling_it_evidence_that_none_exists(self):
        out, _ = self.do_run(count_ok(), gen_ok(no_fusion_text(A, B)))
        self.assertEqual(out["valid"], "VALID")
        self.assertIn("M2_REVIEW_NO_FUSION_REPORT.json", self.files())
        self.assertNotIn("M2_REVIEW_CARD.json", self.files())

    def test_the_api_key_is_used_but_never_persisted_anywhere(self):
        out, factory = self.do_run(count_ok(), gen_ok(GOOD))
        self.assertTrue(all(r["headers"]["x-api-key"] == self.key for r in factory.requests))
        for name in self.files():
            data = Path(self.root, name).read_bytes()
            self.assertNotIn(self.key.encode(), data, name)
            self.assertNotIn(b"sk-ant-", data, name)
        self.assertNotIn(self.key, json.dumps(out))

    def test_a_retry_after_a_proven_non_transmission_is_logged_in_the_durable_reservation_trail(self):
        out, factory = self.do_run(count_ok(), CONNECT_FAIL, gen_ok(GOOD))
        self.assertEqual(out["status"], "COMPLETE")
        self.assertEqual(len(factory.generation_requests()), 1)
        for name in ("M2_ATTEMPT_1_START.json", "M2_ATTEMPT_1_OUTCOME.json", "M2_ATTEMPT_2_START.json",
                     "M2_ATTEMPT_2_SEND_INTENT.json", "M2_ATTEMPT_2_OUTCOME.json"):
            self.assertIn(name, self.files())
        self.assertNotIn("M2_ATTEMPT_1_SEND_INTENT.json", self.files(), "attempt 1 never got as far as sending")
        self.assertEqual(self.read_json("M2_ATTEMPT_1_OUTCOME.json")["outcome"], "PRE_TRANSMISSION_FAILURE")
        self.assertEqual([a["outcome"] for a in self.read_json(RUN_RECORD)["attempt_history"]], ["PRE_TRANSMISSION_FAILURE", "COMPLETE"])


class OutputAndRecordTests(HarnessCase):
    # --- negative test 11 end to end: invalid output is INVALID and nothing is repaired or retried ---

    def test_invalid_output_is_marked_invalid_with_failed_checks_and_not_retried(self):
        out, factory = self.do_run(count_ok(), gen_ok("OUTCOME: proposal\nthis is not a pair file"), gen_ok(GOOD))
        self.assertEqual((out["status"], out["valid"]), ("COMPLETE", "INVALID"))
        self.assertEqual(len(factory.generation_requests()), 1)
        v = self.read_json("M2_VERDICT.json")["valid"]
        self.assertIn("template_structure", v["failed_checks"])
        self.assertNotIn("M2_REVIEW_CARD.json", self.files())

    def test_truncated_output_is_invalid(self):
        out, _ = self.do_run(count_ok(), gen_ok(GOOD, stop_reason="max_tokens"))
        self.assertEqual(out["valid"], "INVALID")
        self.assertIn("complete_output", self.read_json("M2_VERDICT.json")["valid"]["failed_checks"])

    # --- negative test 12 end to end ---

    def test_a_missing_audit_field_marks_the_attempt_not_reproducible(self):
        out, _ = self.do_run(count_ok(), {"status": 200, "body": gen_ok(GOOD)["body"], "headers": {}})   # no request-id header
        self.assertEqual(out["valid"], "VALID")
        self.assertEqual(out["reproducibility"], "NOT REPRODUCIBLE")
        self.assertEqual(self.read_json("M2_VERDICT.json")["reproducibility"]["missing_fields"], ["provider_request_id"])

    def test_an_unknown_commit_sha_also_marks_it_not_reproducible(self):
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        out = run(self.cfg, api_key=self.key, authorization_ref="T", connection_factory=factory,
                  git_info_fn=lambda r: {"commit": None, "tracked_tree_dirty": None}, sleep=lambda s: None)
        self.assertEqual(out["reproducibility"], "NOT REPRODUCIBLE")
        self.assertEqual(self.read_json("M2_VERDICT.json")["reproducibility"]["missing_fields"], ["repo_commit_sha"])

    def test_the_run_record_is_written_before_the_output_is_checked(self):
        order = []
        real_validate = m2_harness.validate_output
        real_write = EvidenceStore.write_json_once

        def spy_write(store, name, obj):
            order.append(name)
            return real_write(store, name, obj)

        def spy_validate(*a, **k):
            order.append("VALIDATE")
            return real_validate(*a, **k)

        with mock.patch.object(EvidenceStore, "write_json_once", spy_write), mock.patch.object(m2_harness, "validate_output", spy_validate):
            self.do_run(count_ok(), gen_ok(GOOD))
        self.assertLess(order.index(RUN_RECORD), order.index("VALIDATE"))

    # --- negative test 2 end to end: a secret stops the write ---

    def test_a_credential_in_the_response_prevents_the_record_and_leaves_the_milestone_blocked(self):
        leaky = gen_ok("OUTCOME: no-fusion\n" + self.key)
        with self.assertRaises(SecretDetected):
            self.do_run(count_ok(), leaky)
        self.assertNotIn("M2_RESPONSE.raw", self.files())
        self.assertNotIn(RUN_RECORD, self.files())
        self.assertIn(RESERVATION_NAME, self.files())
        with self.assertRaises(ReservationExists):
            self.do_run()

    def test_a_credential_in_the_authorization_reference_stops_before_anything_is_sent(self):
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaises(SecretDetected):
            run(self.cfg, **dict(self.run_kwargs(factory), authorization_ref=f"approved with {self.key}"))
        self.assertEqual(factory.paths(), [COUNT_PATH], "no generation request")
        self.assertEqual(self.files(), [], "no file, redacted or otherwise")


class SpendGuardEndToEndTests(HarnessCase):
    # --- negative test 1 ---

    def test_a_bound_above_the_cap_prevents_transmission_and_consumes_nothing(self):
        factory = FakeFactory(count_ok(400_000), gen_ok(GOOD))
        with self.assertRaisesRegex(SpendGuardError, "exceeds"):
            run(self.cfg, **self.run_kwargs(factory))
        self.assertEqual(factory.paths(), [COUNT_PATH])
        self.assertEqual(self.files(), [], "a refused run writes no reservation: the milestone stays open")
        out, _ = self.do_run(count_ok(15000), gen_ok(GOOD))                  # and a later, within-cap run is still possible
        self.assertEqual(out["status"], "COMPLETE")

    def test_the_committed_unverified_rates_refuse_generation(self):
        # explicit unverified fixture: the committed rates with verified=False and verified_on=None
        unverified = dataclasses.replace(COMMITTED_CONFIG.rates, verified=False, verified_on=None)
        cfg = dataclasses.replace(self.cfg, rates=unverified)
        factory = FakeFactory(count_ok(15000), gen_ok(GOOD))
        with self.assertRaisesRegex(SpendGuardError, "not verified"):
            run(cfg, **self.run_kwargs(factory))
        self.assertEqual((factory.paths(), self.files()), ([COUNT_PATH], []))

    def test_a_failed_token_count_stops_before_any_generation(self):
        factory = FakeFactory({"status": 400, "body": b'{"error":{"message":"bad thinking"}}'}, gen_ok(GOOD))
        with self.assertRaises(CountTokensStop):
            run(self.cfg, **self.run_kwargs(factory))
        self.assertEqual((factory.paths(), self.files()), ([COUNT_PATH], []))

    def test_a_packet_that_no_longer_matches_the_predeclared_hash_is_refused(self):
        cfg = dataclasses.replace(self.cfg, expected_packet_sha256="0" * 64)
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaisesRegex(HarnessStop, "pre-declared"):
            run(cfg, **self.run_kwargs(factory))
        self.assertEqual((factory.requests, self.files()), ([], []))


class MilestoneLockTests(HarnessCase):
    def blocked_after(self, label, *plans):
        """Run once with `plans`, then prove nothing at all can be sent by a second invocation."""
        self.do_run(*plans)
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaises(ReservationExists, msg=label):
            run(self.cfg, **self.run_kwargs(factory))
        self.assertEqual(factory.requests, [], f"{label}: not even a token count may be made")

    # --- negative tests 6 and 15: no second attempt in any terminal state ---

    def test_a_second_invocation_cannot_reuse_the_reservation_after_any_outcome(self):
        scenarios = {
            "valid proposal": (count_ok(), gen_ok(GOOD)),
            "invalid output": (count_ok(), gen_ok("garbage")),
            "truncated output": (count_ok(), gen_ok(GOOD, stop_reason="max_tokens")),
            "ambiguous (stream cut)": (count_ok(), {"status": 200, "body": gen_ok(GOOD, truncate=True)["body"]}),
            "http error": (count_ok(), {"status": 529, "body": b'{"type":"error"}'}),
            "no output, retries exhausted": (count_ok(), CONNECT_FAIL, CONNECT_FAIL, CONNECT_FAIL),
        }
        for label, plans in scenarios.items():
            with self.subTest(label):
                for entry in os.listdir(self.root):
                    os.unlink(os.path.join(self.root, entry))            # fresh evidence root per scenario (test cleanup only)
                self.blocked_after(label, *plans)

    # --- negative test 7 ---

    def test_a_reservation_for_ilse_and_sable_also_blocks_a_different_pair(self):
        self.do_run(count_ok(), gen_ok(GOOD))
        other = dataclasses.replace(self.cfg, pair=("tamsin_vey", "pell_dunmore"), expected_packet_sha256=None)
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaises(ReservationExists):
            run(other, **self.run_kwargs(factory))
        self.assertEqual(factory.requests, [])
        self.assertEqual(self.read_json(RESERVATION_NAME)["pair"], ["ilse_marrow", "sable_quillon"])

    def test_the_reservation_records_the_pair_and_is_created_before_the_generation_request(self):
        seen = {}

        class Spy(FakeFactory):
            def __call__(spy, host, timeout):
                seen.setdefault("reservation_existed_at_connection_%d" % (spy.created + 1), os.path.exists(os.path.join(self.root, RESERVATION_NAME)))
                return super().__call__(host, timeout)

        factory = Spy(count_ok(), gen_ok(GOOD))
        run(self.cfg, **self.run_kwargs(factory))
        self.assertFalse(seen["reservation_existed_at_connection_1"], "token counting happens before the reservation")
        self.assertTrue(seen["reservation_existed_at_connection_2"], "the reservation must exist before generation is transmitted")

    def test_a_pair_the_configuration_does_not_approve_is_refused(self):
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaisesRegex(HarnessStop, "not the pair"):
            run(self.cfg, **self.run_kwargs(factory, pair=("tamsin_vey", "pell_dunmore")))
        self.assertEqual((factory.requests, self.files()), ([], []))

    # --- negative test 8: a crash or failed record write does not release the reservation ---

    def test_a_failed_run_record_write_leaves_the_milestone_blocked(self):
        real = EvidenceStore.write_json_once

        def failing(store, name, obj):
            if name == RUN_RECORD:
                raise EvidenceError("disk full")
            return real(store, name, obj)

        with mock.patch.object(EvidenceStore, "write_json_once", failing):
            with self.assertRaises(EvidenceError):
                self.do_run(count_ok(), gen_ok(GOOD))
        self.assertIn(RESERVATION_NAME, self.files())
        self.assertNotIn(RUN_RECORD, self.files())
        self.assertIn("M2_RESPONSE.raw", self.files(), "the raw response was already preserved")
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaises(ReservationExists):
            run(self.cfg, **self.run_kwargs(factory))
        self.assertEqual(factory.requests, [], "a missing run record is not proof that no attempt occurred")

    def test_a_crash_during_the_send_leaves_the_milestone_blocked(self):
        for crash in (RuntimeError("process died"), KeyboardInterrupt(), SystemExit(1)):
            with self.subTest(type(crash).__name__):
                for entry in os.listdir(self.root):
                    os.unlink(os.path.join(self.root, entry))
                with mock.patch.object(m2_harness, "send_generation", side_effect=crash):
                    with self.assertRaises(type(crash)):
                        self.do_run(count_ok())
                self.assertIn(RESERVATION_NAME, self.files())
                factory = FakeFactory(count_ok(), gen_ok(GOOD))
                with self.assertRaises(ReservationExists):
                    run(self.cfg, **self.run_kwargs(factory))
                self.assertEqual(factory.requests, [])

    def test_a_crash_after_the_request_was_sent_is_visible_in_the_attempt_trail(self):
        # simulate dying between SEND_INTENT and the outcome log: the START and SEND_INTENT files exist, OUTCOME does not
        real = EvidenceStore.write_json_once

        def die_on_outcome(store, name, obj):
            if name.endswith("_OUTCOME.json"):
                raise KeyboardInterrupt()
            return real(store, name, obj)

        with mock.patch.object(EvidenceStore, "write_json_once", die_on_outcome):
            with self.assertRaises(KeyboardInterrupt):
                self.do_run(count_ok(), gen_ok(GOOD))
        self.assertTrue({"M2_ATTEMPT_1_START.json", "M2_ATTEMPT_1_SEND_INTENT.json"} <= set(self.files()))
        self.assertNotIn("M2_ATTEMPT_1_OUTCOME.json", self.files())
        with self.assertRaises(ReservationExists):
            self.do_run()

    def test_there_is_no_parameter_that_could_release_resume_or_force(self):
        names = set(inspect.signature(run).parameters) | set(inspect.signature(dry_run).parameters)
        for word in ("force", "override", "resume", "release", "reset", "retry", "evidence"):
            self.assertFalse([n for n in names if word in n.lower()], word)
        # the only root-like parameter locates the repository (for packet paths); the evidence root has no parameter at all
        self.assertEqual([n for n in names if "root" in n.lower()], ["repo_root"])

    # --- A6: authorization reference, evidence root (negative test 9 end to end) ---

    def test_a_run_needs_an_operator_authorization_reference(self):
        for ref in ("", "   ", None):
            factory = FakeFactory(count_ok(), gen_ok(GOOD))
            with self.assertRaisesRegex(HarnessStop, "authorization reference"):
                run(self.cfg, **dict(self.run_kwargs(factory), authorization_ref=ref))
            self.assertEqual((factory.requests, self.files()), ([], []))

    def test_a_missing_or_unsafe_evidence_root_stops_before_any_request_and_is_never_created(self):
        missing = os.path.join(self.tmp, "nope", "imp-001-m2")
        factory = FakeFactory(count_ok(), gen_ok(GOOD))
        with self.assertRaises(RootRejected):
            run(dataclasses.replace(self.cfg, evidence_root=missing), **self.run_kwargs(factory))
        self.assertEqual(factory.requests, [])
        self.assertFalse(os.path.exists(os.path.dirname(missing)), "no replacement root is created and there is no fallback")
        inside = os.path.join(str(REPO_ROOT), "proposer", "tests", "_would_be_repo_internal")
        with self.assertRaises(RootRejected):
            run(dataclasses.replace(self.cfg, evidence_root=inside), **self.run_kwargs(FakeFactory(count_ok())))
        self.assertFalse(os.path.exists(inside))

    def test_no_api_key_stops_immediately(self):
        factory = FakeFactory(count_ok())
        with self.assertRaisesRegex(HarnessStop, "no API key"):
            run(self.cfg, **dict(self.run_kwargs(factory), api_key=""))
        self.assertEqual(factory.requests, [])


class FailureStatusTests(HarnessCase):
    def test_an_ambiguous_stream_is_recorded_as_ambiguous_with_the_partial_bytes_and_stops(self):
        cut = gen_ok(GOOD, truncate=True)["body"]
        out, factory = self.do_run(count_ok(), {"status": 200, "body": cut}, gen_ok(GOOD))
        self.assertEqual((out["status"], out["valid"]), ("AMBIGUOUS", "NOT_EVALUATED"))
        self.assertEqual(len(factory.generation_requests()), 1)
        self.assertEqual(Path(self.root, "M2_RESPONSE.raw").read_bytes(), cut)
        self.assertEqual(self.read_json(RUN_RECORD)["error"]["class"], "StreamIncomplete")
        self.assertNotIn("M2_OUTPUT_TEXT.txt", self.files())

    def test_an_http_error_is_recorded_and_not_retried(self):
        out, factory = self.do_run(count_ok(), {"status": 529, "body": b'{"type":"error","error":{"type":"overloaded_error"}}'}, gen_ok(GOOD))
        self.assertEqual(out["status"], "HTTP_ERROR")
        self.assertEqual(len(factory.generation_requests()), 1)
        self.assertEqual(self.read_json(RUN_RECORD)["http_status"], 529)

    def test_exhausted_pre_transmission_retries_are_recorded_with_no_response_and_still_block(self):
        out, factory = self.do_run(count_ok(), CONNECT_FAIL, CONNECT_FAIL, CONNECT_FAIL)
        self.assertEqual(out["status"], "NO_OUTPUT_PRE_TRANSMISSION_EXHAUSTED")
        self.assertEqual(len(factory.generation_requests()), 0)
        self.assertNotIn("M2_RESPONSE.raw", self.files())
        self.assertEqual(len(self.read_json(RUN_RECORD)["attempt_history"]), 3)
        self.assertEqual(out["reproducibility"], "REPRODUCIBLE")
        self.assertIn(RESERVATION_NAME, self.files())


class DryRunTests(HarnessCase):
    def dry(self, *plans, cfg=None):
        factory = FakeFactory(*plans)
        return dry_run(cfg or self.cfg, api_key=self.key, connection_factory=factory, git_info_fn=fake_git), factory

    # --- negative test 14 ---

    def test_a_dry_run_cannot_send_a_generation_request(self):
        report, factory = self.dry(count_ok(15000), gen_ok(GOOD), gen_ok(GOOD))
        self.assertEqual(factory.paths(), [COUNT_PATH])
        self.assertEqual(factory.created, 1)
        self.assertIs(report["generation_request_sent"], False)
        self.assertEqual(report["status"], "COMPLETE")

    def test_the_dry_run_reports_the_exact_request_the_run_would_send_and_the_cost_bound(self):
        report, factory = self.dry(count_ok(15000))
        sent = json.loads(factory.requests[0]["body"])
        self.assertEqual(sent["thinking"], {"type": "adaptive"})
        self.assertNotIn("max_tokens", sent)
        self.assertEqual(report["packet_sha256"], EXPECTED_PACKET_SHA256)
        self.assertEqual(report["cost_report"]["upper_bound_usd"], "1.34")
        self.assertIs(report["cost_report"]["generation_permitted"], True)
        self.assertEqual(report["prepaid_backstop_usd"], "5")

    def test_with_the_committed_unverified_rates_the_dry_run_reports_but_does_not_permit(self):
        # explicit unverified fixture: the committed rates with verified=False and verified_on=None
        unverified = dataclasses.replace(COMMITTED_CONFIG.rates, verified=False, verified_on=None)
        report, _ = self.dry(count_ok(15000), cfg=dataclasses.replace(self.cfg, rates=unverified))
        self.assertEqual(report["cost_report"]["upper_bound_usd"], "1.34")
        self.assertIs(report["cost_report"]["generation_permitted"], False)
        self.assertIn("not verified", report["cost_report"]["refusal_reason"])

    def test_a_dry_run_report_is_not_an_attempt_and_does_not_block_the_milestone(self):
        report, _ = self.dry(count_ok())
        self.assertTrue(report["report_file"].startswith("M2_DRYRUN_"))
        out, _ = self.do_run(count_ok(), gen_ok(GOOD))
        self.assertEqual(out["status"], "COMPLETE")

    # --- negative test 13 end to end ---

    def test_a_rejected_thinking_configuration_stops_the_dry_run_and_records_why(self):
        rejected = {"status": 400, "body": b'{"type":"error","error":{"type":"invalid_request_error","message":"thinking: unsupported"}}'}
        factory = FakeFactory(rejected, count_ok())
        with self.assertRaisesRegex(CountTokensStop, "thinking: unsupported"):
            dry_run(self.cfg, api_key=self.key, connection_factory=factory, git_info_fn=fake_git)
        self.assertEqual(len(factory.requests), 1, "no fallback to a different configuration")
        stopped = [n for n in self.files() if n.startswith("M2_DRYRUN_")]
        self.assertEqual(len(stopped), 1)
        self.assertEqual(self.read_json(stopped[0])["status"], "STOPPED")

    def test_a_dry_run_with_an_existing_reservation_reports_the_block_and_still_sends_nothing_else(self):
        self.do_run(count_ok(), gen_ok(GOOD))
        report, factory = self.dry(count_ok())
        self.assertIn(RESERVATION_NAME, report["milestone_blocked_by_existing_artifacts"])
        self.assertEqual(factory.paths(), [COUNT_PATH])


class CliTests(unittest.TestCase):
    def test_the_cli_stops_cleanly_without_a_key_and_touches_nothing(self):
        for argv in (["dry-run"], ["run", "--authorization-ref", "T"]):
            with mock.patch.dict(os.environ, {}, clear=False) as env:
                env.pop("ANTHROPIC_API_KEY", None)
                err = io.StringIO()
                with contextlib.redirect_stderr(err), mock.patch("socket.create_connection", side_effect=AssertionError("network")):
                    self.assertEqual(m2_harness.main(argv), 2)
            self.assertIn("no API key", err.getvalue())

    def test_the_run_command_cannot_be_invoked_without_an_authorization_reference(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            m2_harness.main(["run"])


if __name__ == "__main__":
    unittest.main()
