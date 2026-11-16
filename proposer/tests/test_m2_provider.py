"""IMP-001 M2 provider: retry/transmission safety (negative tests 3, 4, 5) and token-count stops (test 13)."""

from __future__ import annotations

import dataclasses
import json
import unittest

from proposer.m2_provider import (AMBIGUOUS, COMPLETE, HTTP_ERROR, NO_OUTPUT_EXHAUSTED, PRE_TRANSMISSION_FAILURE, CountTokensStop,
                                  StreamIncomplete, count_input_tokens, message_text, parse_event_stream, send_generation, transmit)
from proposer.tests.m2_support import COUNT_PATH, FAKE_KEY, FakeFactory, M2TestCase, count_ok, gen_ok, sse


class Recorder:
    """Stands in for the durable evidence callbacks and records the order they were called in."""

    def __init__(self, fail_on=None):
        self.events, self.fail_on = [], fail_on

    def _hit(self, name, *a):
        self.events.append((name, *a))
        if self.fail_on == name:
            raise RuntimeError(f"{name} could not be written")

    def start(self, n): self._hit("start", n)
    def intent(self, n, info): self._hit("intent", n)
    def outcome(self, n, result): self._hit("outcome", n, result.outcome)


class RetryPolicyTests(M2TestCase):
    def send(self, factory, rec=None, cfg=None):
        rec = rec or Recorder()
        out = send_generation(cfg or self.cfg, b'{"x":1}', self.key, connection_factory=factory, log_attempt_start=rec.start,
                              log_send_intent=rec.intent, log_attempt_outcome=rec.outcome, sleep=lambda s: None)
        return out, rec

    # --- negative test 4: a proven pre-transmission failure permits at most two retries ---

    def test_connect_failures_are_retried_at_most_twice_then_stop(self):
        factory = FakeFactory({"connect_error": OSError("dns")}, {"connect_error": OSError("refused")}, {"connect_error": OSError("tls")})
        out, rec = self.send(factory)                 # a fourth connection would raise AssertionError
        self.assertEqual(out.status, NO_OUTPUT_EXHAUSTED)
        self.assertEqual((factory.connect_attempts, len(factory.requests)), (3, 0), "1 attempt + 2 retries, and no request byte")
        self.assertEqual([a["outcome"] for a in out.attempts], [PRE_TRANSMISSION_FAILURE] * 3)

    def test_a_connect_failure_then_success_sends_exactly_one_generation_request(self):
        factory = FakeFactory({"connect_error": ConnectionResetError("reset while connecting")}, gen_ok())
        out, _ = self.send(factory)
        self.assertEqual(out.status, COMPLETE)
        self.assertEqual(len(factory.generation_requests()), 1)
        self.assertEqual([a["outcome"] for a in out.attempts], [PRE_TRANSMISSION_FAILURE, COMPLETE])

    def test_retries_come_from_the_config_not_a_hidden_default(self):
        cfg = dataclasses.replace(self.cfg, max_retries=0)
        factory = FakeFactory({"connect_error": OSError("dns")})
        out, _ = self.send(factory, cfg=cfg)
        self.assertEqual((out.status, factory.connect_attempts), (NO_OUTPUT_EXHAUSTED, 1))

    # --- negative test 5: ambiguous or post-transmission failure stops with no retry ---

    def test_every_post_transmission_failure_stops_after_exactly_one_send(self):
        spare = gen_ok()    # a retry would consume this; the assertions prove it never is
        cases = {
            "send raised": {"send_error": ConnectionResetError("reset during send")},
            "no status line": {"getresponse_error": TimeoutError("timed out waiting for response")},
            "body dropped half way": {"status": 200, "body": sse("OUTCOME: no-fusion"), "read_error_after": ConnectionResetError("dropped")},
            "stream truncated": {"status": 200, "body": sse(truncate=True)},
            "stream error event": {"status": 200, "body": sse(with_error=True)},
            "not an event stream": {"status": 200, "body": b"<html>gateway</html>"},
        }
        for label, plan in cases.items():
            with self.subTest(label):
                factory = FakeFactory(plan, spare, spare)
                out, _ = self.send(factory)
                self.assertEqual(out.status, AMBIGUOUS)
                self.assertEqual(len(factory.generation_requests()), 1, "a post-transmission failure must never cause another send")
                self.assertEqual(factory.created, 1)
                self.assertTrue(out.final.transmission_started)

    def test_an_explicit_http_error_is_not_retried(self):
        for status in (400, 401, 429, 500, 529):
            with self.subTest(status):
                factory = FakeFactory({"status": status, "body": b'{"type":"error"}'}, gen_ok())
                out, _ = self.send(factory)
                self.assertEqual(out.status, HTTP_ERROR)
                self.assertEqual((len(factory.requests), factory.created), (1, 1))

    def test_a_connection_exception_alone_is_not_proof_of_non_transmission(self):
        """The same exception class is retryable inside connect() and ambiguous once the request has started."""
        before = FakeFactory({"connect_error": ConnectionResetError("x")}, gen_ok())
        self.assertEqual(self.send(before)[0].status, COMPLETE)
        after = FakeFactory({"send_error": ConnectionResetError("x")}, gen_ok())
        out, _ = self.send(after)
        self.assertEqual((out.status, after.created), (AMBIGUOUS, 1))

    # --- negative test 3: no automatic or hidden retry / resend path ---

    def test_http_client_cannot_reconnect_and_resend_on_its_own(self):
        factory = FakeFactory(gen_ok())
        self.send(factory)
        self.assertTrue(all(c.auto_open == 0 for c in factory.conns), "auto_open must be off so http.client cannot reopen the socket")
        self.assertTrue(all(c.closed for c in factory.conns))

    def test_retry_follows_the_durable_log_and_never_precedes_it(self):
        factory = FakeFactory({"connect_error": OSError("dns")}, gen_ok())
        _, rec = self.send(factory)
        self.assertEqual(rec.events, [("start", 1), ("outcome", 1, PRE_TRANSMISSION_FAILURE),
                                      ("start", 2), ("intent", 2), ("outcome", 2, COMPLETE)])

    def test_if_the_attempt_log_cannot_be_written_nothing_is_sent(self):
        for fail_on, connections in (("start", 0), ("intent", 1)):
            with self.subTest(fail_on):
                factory = FakeFactory(gen_ok())
                with self.assertRaises(RuntimeError):
                    self.send(factory, Recorder(fail_on=fail_on))
                self.assertEqual(len(factory.requests), 0)
                self.assertEqual(factory.created, connections)

    def test_if_the_outcome_log_fails_there_is_no_retry(self):
        factory = FakeFactory({"connect_error": OSError("dns")}, gen_ok())
        with self.assertRaises(RuntimeError):
            self.send(factory, Recorder(fail_on="outcome"))
        self.assertEqual((factory.connect_attempts, len(factory.requests)), (1, 0))

    def test_the_request_is_sent_once_per_connection_with_the_key_but_it_is_not_recorded(self):
        factory = FakeFactory(gen_ok())
        out, _ = self.send(factory)
        sent = factory.requests[0]["headers"]
        self.assertEqual(sent["x-api-key"], FAKE_KEY)
        recorded = out.final.recorded_request_headers
        self.assertEqual(sorted(recorded), ["accept", "anthropic-version", "content-type"])
        self.assertNotIn(FAKE_KEY, json.dumps(recorded))
        self.assertNotIn("x-api-key", {k.lower() for k in recorded})

    def test_dry_run_style_transmit_reports_state_without_any_retry(self):
        r = transmit(self.cfg, COUNT_PATH, b"{}", self.key, stream=False, connection_factory=FakeFactory(count_ok()))
        self.assertEqual((r.outcome, r.transmission_started), (COMPLETE, True))


class StreamTests(unittest.TestCase):
    def test_a_complete_stream_assembles_text_usage_and_stop_reason(self):
        m = parse_event_stream(sse("hello world", input_tokens=123, output_tokens=45))
        self.assertEqual(message_text(m), "hello world")
        self.assertEqual((m["stop_reason"], m["usage"]["input_tokens"], m["usage"]["output_tokens"]), ("end_turn", 123, 45))
        self.assertEqual([b["type"] for b in m["content"]], ["thinking", "text"])
        self.assertEqual(m["id"], "msg_1")

    def test_truncated_errored_and_garbled_streams_are_incomplete(self):
        for raw in (sse(truncate=True), sse(with_error=True), b"data: {not json}\n\n", b"", b"\xff\xfe"):
            with self.assertRaises(StreamIncomplete):
                parse_event_stream(raw)

    def test_max_tokens_stop_reason_is_preserved_for_the_validator(self):
        self.assertEqual(parse_event_stream(sse("cut off", stop_reason="max_tokens"))["stop_reason"], "max_tokens")


class CountTokensTests(M2TestCase):
    body = b'{"model":"m"}'

    def count(self, plan):
        return count_input_tokens(self.cfg, self.body, self.key, connection_factory=FakeFactory(plan))

    def test_a_good_response_returns_the_count(self):
        self.assertEqual(self.count(count_ok(777))["input_tokens"], 777)

    # --- negative test 13: an unsupported or rejected thinking configuration stops the dry run ---

    def test_a_rejected_thinking_configuration_stops_with_the_providers_words(self):
        rejected = {"status": 400, "body": b'{"type":"error","error":{"type":"invalid_request_error","message":"thinking.type: adaptive is not supported"}}'}
        with self.assertRaisesRegex(CountTokensStop, "thinking.type: adaptive is not supported"):
            self.count(rejected)

    def test_no_silent_fallback_the_endpoint_is_asked_exactly_once(self):
        factory = FakeFactory({"status": 400, "body": b"{}"}, count_ok(), count_ok())
        with self.assertRaises(CountTokensStop):
            count_input_tokens(self.cfg, self.body, self.key, connection_factory=factory)
        self.assertEqual(len(factory.requests), 1)

    def test_odd_responses_stop_rather_than_guess(self):
        for plan in ({"status": 200, "body": b"not json"}, {"status": 200, "body": b"[]"},
                     {"status": 200, "body": b'{"input_tokens": "5"}'}, {"status": 200, "body": b'{"input_tokens": true}'},
                     {"status": 200, "body": b'{"input_tokens": -1}'}, {"status": 200, "body": b'{"error": {}, "input_tokens": 5}'},
                     {"status": 200, "body": b"{}"}, {"connect_error": OSError("dns")}, {"send_error": OSError("x")}):
            with self.subTest(plan), self.assertRaises(CountTokensStop):
                self.count(plan)


if __name__ == "__main__":
    unittest.main()
