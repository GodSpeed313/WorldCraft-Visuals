"""Shared fixtures for the IMP-001 M2 harness tests. No real network access is ever possible here."""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

from fusion_synthesis.loader import read_json
from fusion_synthesis.schema import SLOTS, SCENE_FIELDS, parse_character
from proposer.m2_config import COMMITTED_CONFIG, Rates
from proposer.packet import CHARACTER_DIR, REPO_ROOT

# Built at run time so no key-shaped literal sits in the source. It is a placeholder, not a credential.
FAKE_KEY = "sk-" + "ant-api03-TESTONLY-" + "x" * 24
VERIFIED_RATES = Rates(Decimal("4.00"), Decimal("20.00"), "test fixture rates", "2026-01-01", True)
FAKE_GIT = {"commit": "a" * 40, "tracked_tree_dirty": False}
COUNT_PATH = COMMITTED_CONFIG.count_tokens_path
GEN_PATH = COMMITTED_CONFIG.messages_path


def fake_git(_repo_root):
    return dict(FAKE_GIT)


def load_cards(a="ilse_marrow", b="sable_quillon"):
    return tuple(parse_character(read_json(REPO_ROOT / CHARACTER_DIR / f"{s}.json"), s) for s in (a, b))


# --- scripted fake http.client connections ------------------------------------

class FakeResponse:
    def __init__(self, status, body, headers, read_error_after=None):
        self.status, self._body, self._headers = status, body, headers
        self._pos, self._err = 0, read_error_after

    def getheader(self, name, default=None):
        return self._headers.get(name.lower(), default)

    def read(self, n=-1):
        limit = len(self._body) if self._err is None else len(self._body) // 2
        if self._pos >= limit:
            if self._err is not None:
                raise self._err           # the connection drops half way through the body
            return b""
        chunk = self._body[self._pos:min(limit, self._pos + (n if n > 0 else limit))]
        self._pos += len(chunk)
        return chunk


class FakeConnection:
    def __init__(self, factory, plan):
        self.factory, self.plan, self.auto_open, self.sock, self.closed = factory, plan, 1, None, False

    def connect(self):
        self.factory.connect_attempts += 1
        if self.plan.get("connect_error"):
            raise self.plan["connect_error"]

    def request(self, method, path, body=None, headers=None):
        self.factory.requests.append({"path": path, "body": body, "headers": dict(headers or {})})
        if self.plan.get("send_error"):
            raise self.plan["send_error"]

    def getresponse(self):
        if self.plan.get("getresponse_error"):
            raise self.plan["getresponse_error"]
        return FakeResponse(self.plan.get("status", 200), self.plan.get("body", b""),
                            {k.lower(): v for k, v in self.plan.get("headers", {"request-id": "req_fake"}).items()},
                            self.plan.get("read_error_after"))

    def close(self):
        self.closed = True


class FakeFactory:
    """One scripted plan per connection, in order. Asking for more connections than planned fails the test."""

    def __init__(self, *plans):
        self.plans, self.requests, self.connect_attempts, self.created, self.conns = list(plans), [], 0, 0, []

    def __call__(self, host, timeout):
        if self.created >= len(self.plans):
            raise AssertionError(f"unplanned extra connection #{self.created + 1}: a send happened that the test did not script")
        plan = self.plans[self.created]
        self.created += 1
        conn = FakeConnection(self, plan)
        self.conns.append(conn)
        return conn

    def paths(self):
        return [r["path"] for r in self.requests]

    def generation_requests(self):
        return [r for r in self.requests if r["path"] == GEN_PATH]


def count_ok(tokens=15000):
    return {"status": 200, "body": json.dumps({"input_tokens": tokens}).encode()}


def sse(text="OUTCOME: no-fusion", stop_reason="end_turn", input_tokens=15000, output_tokens=900, with_error=False, truncate=False):
    def ev(name, data):
        return f"event: {name}\ndata: {json.dumps(data)}\n\n"
    out = [ev("message_start", {"type": "message_start", "message": {"id": "msg_1", "model": "claude-opus-5-5", "role": "assistant",
                                                                   "usage": {"input_tokens": input_tokens, "output_tokens": 1}}}),
           ev("ping", {"type": "ping"}),
           ev("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}}),
           ev("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "sig"}}),
           ev("content_block_stop", {"type": "content_block_stop", "index": 0}),
           ev("content_block_start", {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}),
           ev("content_block_delta", {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": text}}),
           ev("content_block_stop", {"type": "content_block_stop", "index": 1})]
    if with_error:
        out.append(ev("error", {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}))
    if not truncate and not with_error:
        out.append(ev("message_delta", {"type": "message_delta", "delta": {"stop_reason": stop_reason}, "usage": {"output_tokens": output_tokens}}))
        out.append(ev("message_stop", {"type": "message_stop"}))
    return "".join(out).encode("utf-8")


def gen_ok(text="OUTCOME: no-fusion", **kw):
    return {"status": 200, "body": sse(text, **kw)}


# --- output fixtures ----------------------------------------------------------

def pair_file(card_a, card_b):
    slug = f"{card_a.slug}__{card_b.slug}"
    pa, pb = card_a.properties[0].id, card_b.properties[0].id
    emergent_id = f"{slug}.emergent"

    def trait(text):
        return {"descriptor": text, "origin": "new", "parent_ids": [emergent_id]}

    return {
        "schema": "fusion-synthesis-pair/1", "a": card_a.name, "b": card_b.name, "dominance": 50,
        "fusion_name": "Test Fusion", "concept": "A fixture concept.",
        "interaction": {"id": f"{slug}.interaction", "description": "A fixture interaction.", "dependency_ids": [pa, pb],
                        "provenance": "INVENTED_BRIDGE", "is_disclosed_modification": False},
        "emergent_ability": {"id": emergent_id, "name": "Fixture ability", "description": "A fixture ability.",
                             "direct_ancestor_ids": [pa, pb], "contribution_type": "ABILITY",
                             "architectural_placement": "CORE_MECHANISM",
                             "limitations": ["Works only where both conditions hold at once."], "activation": "When both hold."},
        "trait_outcomes": [{"property_id": p.id, "outcome": "inherited", "result_text": "kept"}
                           for p in (*card_a.properties, *card_b.properties)],
        "exclusions": [],
        "visual": {"subject": trait("a fixture subject"), "slots": {s: trait(f"fixture {s}") for s in SLOTS},
                   **{f: trait(f"fixture {f}") for f in SCENE_FIELDS}, "parameters": "--ar 3:4"},
    }


def proposal_text(card_a, card_b, pair=None, **over):
    pair = pair if pair is not None else pair_file(card_a, card_b)
    parts = {
        "head": "OUTCOME: proposal", "pair": "PAIR FILE:\n" + json.dumps(pair, indent=1),
        "causal": (f"CAUSAL EXPLANATION:\n  Parent 1 contribution (property ids): {card_a.properties[0].id}\n"
                   f"  Parent 2 contribution (property ids): {card_b.properties[0].id}\n"
                   "  Interaction: they act on each other.\n  Beyond either parent? No."),
        "levels": "DECLARED LEVELS: shared structure 3; emergence 2",
        "prov": "DECLARED PROVENANCE: Invented Bridge",
        "lims": "LIMITATION SOURCES:\n  Works only where both conditions hold at once. -> " + card_a.properties[0].id,
        "unc": "DISCLOSED UNCERTAINTIES: none",
    }
    parts.update(over)
    return "\n".join(v for v in parts.values() if v is not None)


def no_fusion_text(card_a, card_b, n=3, **over):
    ids = [card_a.properties[0].id, card_b.properties[0].id]
    cands = [f"CANDIDATE {i}: mechanism number {i} is different; failed test(s): 2, 3; property ids: {ids[0]}, {ids[1]}" for i in range(1, n + 1)]
    parts = {"head": "OUTCOME: no-fusion", "stmt": "STATEMENT: no defensible fusion found", "cands": "\n".join(cands),
             "fewer": "FEWER THAN THREE BECAUSE: only these were reasonable." if n < 3 else None}
    parts.update(over)
    return "\n".join(v for v in parts.values() if v is not None)


# --- base case ----------------------------------------------------------------

class M2TestCase(unittest.TestCase):
    """Temp evidence root, test config, fake key, and a hard block on real network access."""

    def setUp(self):
        for target in ("socket.socket.connect", "socket.create_connection", "socket.getaddrinfo"):
            patcher = mock.patch(target, side_effect=AssertionError("real network access attempted in a test"))
            patcher.start()
            self.addCleanup(patcher.stop)
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="m2test_"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = os.path.join(self.tmp, "evidence")
        os.mkdir(self.root)
        self.cfg = dataclasses.replace(COMMITTED_CONFIG, evidence_root=self.root, rates=VERIFIED_RATES, retry_delay_seconds=0.0)
        self.key = FAKE_KEY

    def files(self):
        return sorted(os.listdir(self.root))

    def read_json(self, name):
        return json.loads(Path(self.root, name).read_text(encoding="utf-8"))

    def run_kwargs(self, factory, **extra):
        return dict(api_key=self.key, authorization_ref="TEST-AUTH", connection_factory=factory, git_info_fn=fake_git,
                    sleep=lambda s: None, **extra)
