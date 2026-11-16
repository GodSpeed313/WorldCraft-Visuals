"""
IMP-001 M2 harness: dry-run and the single guarded attempt. Standard library only.

    python -m proposer.m2_harness dry-run
    python -m proposer.m2_harness run --authorization-ref "<operator act reference>"

Constructing this file authorizes NEITHER command. `dry-run` makes one live token-count
request and `run` makes a paid generation request; each needs its own operator authorization.
There is no flag for the evidence root, no way to release or reset a reservation, and no
resume or retry of an existing reservation.

Order of a `run` (everything before step 7 can fail without consuming the milestone):
  1 verify evidence root  2 milestone still open  3 pair + authorization reference
  4 build packet + request, check pre-declared packet hash  5 count tokens
  6 spending guard (fails closed)  7 CREATE THE RESERVATION  8 write packet/request evidence
  9 send (A2 retry policy)  10 raw response  11 run record  12 PENDING billing addendum
  13 validate, verdicts, review files.
The run record is written before the proposer's OUTPUT is parsed. Transport-level stream
assembly (needed to know whether the response is complete) precedes it; checking the
output text against REQ-001 follows it.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from decimal import Decimal
from pathlib import Path
from typing import Callable, Optional

from fusion_synthesis.loader import read_json
from fusion_synthesis.schema import parse_character
from proposer.m2_config import (API_KEY_ENV_VAR, COMMITTED_CONFIG, HARNESS_VERSION, M2Config,
                                RETRY_POLICY_DECLARATION)
from proposer.m2_evidence import EvidenceError, EvidenceStore, RESERVATION_NAME, sha256_hex, verify_root
from proposer.m2_provider import (COMPLETE, CountTokensStop, count_input_tokens, default_connection_factory,
                                  message_text, send_generation, utc_now)
from proposer.m2_request import SpendGuardError, build_request, cost_report, enforce_spend_guard
from proposer.m2_validate import VALID, assess_reproducibility, validate_output
from proposer.packet import CHARACTER_DIR, REPO_ROOT, REQUIREMENTS_PATH, SCHEMA_PATH, build_packet

RUN_RECORD = "M2_RUN_RECORD.json"
BILLING_ADDENDUM = "M2_BILLING_ADDENDUM.json"


class HarnessStop(RuntimeError):
    """A pre-reservation guard stopped the run. The milestone is still open."""


# --- helpers ------------------------------------------------------------------

def _stamp(now: Callable) -> str:
    return now().replace(":", "").replace(".", "")


def git_info(repo_root) -> dict:
    def git(*args):
        return subprocess.run(["git", *args], cwd=str(repo_root), capture_output=True, text=True, timeout=30)
    try:
        head = git("rev-parse", "HEAD")
        dirty = git("status", "--porcelain", "--untracked-files=no")
        if head.returncode != 0 or dirty.returncode != 0:
            return {"commit": None, "tracked_tree_dirty": None}
        return {"commit": head.stdout.strip() or None, "tracked_tree_dirty": bool(dirty.stdout.strip())}
    except (OSError, subprocess.SubprocessError):
        return {"commit": None, "tracked_tree_dirty": None}


def _character_path(repo_root: Path, slug: str) -> Path:
    return Path(repo_root) / CHARACTER_DIR / f"{slug}.json"


def _packet(pair: tuple, repo_root: Path):
    return build_packet(_character_path(repo_root, pair[0]), _character_path(repo_root, pair[1]),
                        Path(repo_root) / REQUIREMENTS_PATH, Path(repo_root) / SCHEMA_PATH, repo_root=repo_root)


def _cards(pair: tuple, repo_root: Path):
    out = []
    for slug in pair:
        path = _character_path(repo_root, slug)
        out.append(parse_character(read_json(path), path.name))
    return out[0], out[1]


def _prepare(cfg: M2Config, pair: tuple, repo_root: Path):
    packet = _packet(pair, repo_root)
    bundle = build_request(packet, cfg)
    matches = None if cfg.expected_packet_sha256 is None else (bundle.packet_sha256_recomputed == cfg.expected_packet_sha256)
    return packet, bundle, matches


def _file_ref(name: str, sha: str, size: int) -> dict:
    return {"name": name, "sha256": sha, "size": size}


# --- dry run (A5) -------------------------------------------------------------

def dry_run(cfg: M2Config = COMMITTED_CONFIG, *, api_key: str, connection_factory: Callable = default_connection_factory,
            repo_root=REPO_ROOT, pair: Optional[tuple] = None, git_info_fn: Callable = git_info, now: Callable = utc_now) -> dict:
    """Build the exact request, count its input tokens, report the cost bound. NEVER sends a generation request."""
    if not api_key:
        raise HarnessStop("no API key available in the environment")
    pair = tuple(pair or cfg.pair)
    root = verify_root(cfg.evidence_root, repo_root)
    store = EvidenceStore(root, api_key)
    packet, bundle, matches = _prepare(cfg, pair, Path(repo_root))
    report = {
        "record_type": "imp-001-m2-dry-run/1", "status": "STOPPED", "generation_request_sent": False,
        "harness_version": HARNESS_VERSION, "git": git_info_fn(repo_root), "created_utc": now(),
        "pair": list(pair), "packet_sha256": bundle.packet_sha256_recomputed, "packet_sha256_matches_expected": matches,
        "request_body_sha256": bundle.generation_sha256, "system_prompt_sha256": bundle.system_prompt_sha256,
        "request_parameters": bundle.parameters, "milestone_blocked_by_existing_artifacts": store.attempt_artifacts(),
    }
    name = f"M2_DRYRUN_{_stamp(now)}.json"
    try:
        count = count_input_tokens(cfg, bundle.count_bytes, api_key, connection_factory=connection_factory, now=now)
    except CountTokensStop as exc:
        report["stop_reason"] = str(exc)
        store.write_json_once(name, report)
        raise
    cost = cost_report(count["input_tokens"], cfg.max_tokens, cfg.rates, cfg.spend_cap_usd)
    report.update(status="COMPLETE", token_count={"input_tokens": count["input_tokens"], "provider_request_id": count["provider_request_id"],
                                                    "response_sha256": sha256_hex(count["raw_response"])},
                  cost_report=cost, prepaid_backstop_usd=str(cfg.prepaid_backstop_usd),
                  note="The $5 prepaid balance is an independent backstop, not a substitute for this pre-send guard.")
    digest, _ = store.write_json_once(name, report)
    return dict(report, report_file=name, report_sha256=digest)


# --- the single guarded attempt (A2, A3, A6) ----------------------------------

def run(cfg: M2Config = COMMITTED_CONFIG, *, api_key: str, authorization_ref: str,
        connection_factory: Callable = default_connection_factory, repo_root=REPO_ROOT, pair: Optional[tuple] = None,
        git_info_fn: Callable = git_info, now: Callable = utc_now, sleep: Callable = time.sleep) -> dict:
    if not api_key:
        raise HarnessStop("no API key available in the environment")
    root = verify_root(cfg.evidence_root, repo_root)
    store = EvidenceStore(root, api_key)
    store.assert_milestone_open()                                   # any existing attempt artifact blocks every pair
    pair = tuple(pair or cfg.pair)
    if pair != tuple(cfg.pair):
        raise HarnessStop(f"pair {pair} is not the pair this configuration approves {tuple(cfg.pair)}")
    if not (authorization_ref or "").strip():
        raise HarnessStop("an operator authorization reference is required to run")

    packet, bundle, matches = _prepare(cfg, pair, Path(repo_root))
    if matches is False:
        raise HarnessStop("the packet does not hash to the pre-declared packet_sha256; refusing to run")
    git = git_info_fn(repo_root)

    count = count_input_tokens(cfg, bundle.count_bytes, api_key, connection_factory=connection_factory, now=now)
    report = cost_report(count["input_tokens"], cfg.max_tokens, cfg.rates, cfg.spend_cap_usd)
    enforce_spend_guard(report)                                      # raises SpendGuardError; nothing reserved yet

    # ---- point of no return: from here the milestone stays blocked whatever happens ----
    reserved_utc = now()
    reservation_id, reservation_sha = store.reserve({
        "record_type": "imp-001-m2-reservation/1", "milestone": "IMP-001 M2", "state": "RESERVED",
        "pair": list(pair), "reserved_utc": reserved_utc, "authorization_ref": authorization_ref.strip(),
        "harness_version": HARNESS_VERSION, "repo_commit_sha": git["commit"], "model_id": cfg.model, "max_tokens": cfg.max_tokens,
        "packet_sha256": bundle.packet_sha256_recomputed, "request_body_sha256": bundle.generation_sha256,
        "spend_guard": report, "retry_policy": RETRY_POLICY_DECLARATION, "max_retries": cfg.max_retries,
    })
    hashes = {RESERVATION_NAME: reservation_sha}
    hashes["M2_PACKET.json"] = store.write_once("M2_PACKET.json", packet.canonical_bytes)
    hashes["M2_REQUEST_BODY.json"] = store.write_once("M2_REQUEST_BODY.json", bundle.generation_bytes)
    hashes["M2_TOKEN_COUNT_RESPONSE.json"] = store.write_once("M2_TOKEN_COUNT_RESPONSE.json", count["raw_response"])

    def log_start(n: int) -> None:
        name = f"M2_ATTEMPT_{n}_START.json"
        hashes[name], _ = store.write_json_once(name, {"attempt": n, "reservation_id": reservation_id, "logged_utc": now(),
                                                      "step": "about to open the connection; no request byte sent"})

    def log_intent(n: int, info: dict) -> None:
        name = f"M2_ATTEMPT_{n}_SEND_INTENT.json"
        hashes[name], _ = store.write_json_once(name, {"attempt": n, "reservation_id": reservation_id, "logged_utc": now(),
                                                      "step": "connected; the request is about to be transmitted",
                                                      "path": info["path"], "recorded_request_headers": info["recorded_request_headers"]})

    def log_outcome(n: int, result) -> None:
        name = f"M2_ATTEMPT_{n}_OUTCOME.json"
        hashes[name], _ = store.write_json_once(name, {
            "attempt": n, "reservation_id": reservation_id, "logged_utc": now(), "outcome": result.outcome,
            "transmission_started": result.transmission_started, "http_status": result.http_status,
            "error_class": result.error_class, "error_detail": result.error_detail,
            "response_bytes": len(result.raw_bytes), "response_sha256": sha256_hex(result.raw_bytes)})

    outcome = send_generation(cfg, bundle.generation_bytes, api_key, connection_factory=connection_factory,
                              log_attempt_start=log_start, log_send_intent=log_intent, log_attempt_outcome=log_outcome,
                              sleep=sleep, now=now)
    final = outcome.final
    raw_sha = None
    if final.transmission_started:
        raw_sha = hashes["M2_RESPONSE.raw"] = store.write_once("M2_RESPONSE.raw", final.raw_bytes)

    message = final.message or {}
    usage = message.get("usage") or {}
    estimate = None
    if isinstance(usage.get("input_tokens"), int) and isinstance(usage.get("output_tokens"), int) \
            and cfg.rates.input_per_mtok is not None and cfg.rates.output_per_mtok is not None:
        estimate = str((Decimal(usage["input_tokens"]) * cfg.rates.input_per_mtok
                        + Decimal(usage["output_tokens"]) * cfg.rates.output_per_mtok) / Decimal(1_000_000))
    record = {
        "record_type": "imp-001-m2-run-record/1", "status": outcome.status,
        "repo_commit_sha": git["commit"], "tracked_tree_dirty": git["tracked_tree_dirty"], "harness_version": HARNESS_VERSION,
        "request_sent_utc": final.request_sent_utc, "response_complete_utc": final.response_complete_utc,
        "pair": list(pair), "packet_sha256": bundle.packet_sha256_recomputed,
        "packet_sha256_matches_expected": matches, "packet_bytes_file": _file_ref("M2_PACKET.json", hashes["M2_PACKET.json"], len(packet.canonical_bytes)),
        "model_id": cfg.model,
        "request_parameters": dict(bundle.parameters, system_prompt_sha256=bundle.system_prompt_sha256),
        "request_headers_recorded": final.recorded_request_headers,
        "request_body_sha256": bundle.generation_sha256,
        "request_body_file": _file_ref("M2_REQUEST_BODY.json", hashes["M2_REQUEST_BODY.json"], len(bundle.generation_bytes)),
        "raw_response_sha256": raw_sha, "raw_response_size": len(final.raw_bytes) if raw_sha else None,
        "http_status": final.http_status, "provider_request_id": final.provider_request_id,
        "stop_reason": message.get("stop_reason"), "usage_input_tokens": usage.get("input_tokens"),
        "usage_output_tokens": usage.get("output_tokens"), "usage": usage or None,
        "error": {"class": final.error_class, "detail": final.error_detail} if final.error_class else None,
        "token_count": {"input_tokens": count["input_tokens"], "provider_request_id": count["provider_request_id"],
                        "response_sha256": hashes["M2_TOKEN_COUNT_RESPONSE.json"]},
        "estimated_cost": {"label": "ESTIMATE from reported usage x recorded rates; never merged with billed cost",
                           "post_response_estimate_usd": estimate, "pre_send_upper_bound": report},
        "billed_cost_addendum": {"status": "PENDING", "file": BILLING_ADDENDUM},
        "attempt_history": outcome.attempts, "retry_policy": RETRY_POLICY_DECLARATION,
        "reservation": {"id": reservation_id, "sha256": reservation_sha, "file": RESERVATION_NAME},
        "evidence_file_hashes": dict(hashes),
    }
    record_sha, _ = store.write_json_once(RUN_RECORD, record)       # BEFORE the output text is parsed
    store.write_json_once(BILLING_ADDENDUM, {
        "record_type": "imp-001-m2-billing-addendum/1", "status": "PENDING", "billed_cost_usd": None,
        "references": {"file": RUN_RECORD, "sha256": record_sha},
        "note": "Fill from the provider's billing record in a separate, later addendum; never merge with the estimate."})

    repro = assess_reproducibility(record, outcome.status)
    verdict = {
        "record_type": "imp-001-m2-verdict/1", "run_record": {"file": RUN_RECORD, "sha256": record_sha},
        "note": "Three verdicts are recorded separately and are never combined into one score.",
        "valid": {"verdict": "NOT_EVALUATED", "reason": f"no complete output (status {outcome.status})"},
        "defensible": {"status": "PENDING_OPERATOR_REVIEW"}, "creative": {"status": "PENDING_OPERATOR_REVIEW"},
        "reproducibility": repro,
    }
    if outcome.status == COMPLETE:
        card_a, card_b = _cards(pair, Path(repo_root))
        text = message_text(final.message)
        hashes["M2_OUTPUT_TEXT.txt"] = store.write_once("M2_OUTPUT_TEXT.txt", text.encode("utf-8"))
        result = validate_output(text, card_a, card_b, message.get("stop_reason"))
        verdict["valid"] = {"verdict": result["verdict"], "outcome_type": result["outcome_type"],
                            "failed_checks": result["failed_checks"], "checks": result["checks"]}
        if result["verdict"] == VALID:
            parsed = result["parsed"]
            if result["outcome_type"] == "proposal":
                # card first: the pair file alone, with the causal explanation and declarations kept apart
                store.write_json_once("M2_REVIEW_CARD.json", parsed["pair_file"])
                store.write_json_once("M2_REVIEW_DECLARATIONS.json", {k: v for k, v in parsed.items() if k != "pair_file"})
            else:
                store.write_json_once("M2_REVIEW_NO_FUSION_REPORT.json", parsed)
    verdict_sha, _ = store.write_json_once("M2_VERDICT.json", verdict)
    return {"status": outcome.status, "valid": verdict["valid"]["verdict"], "reproducibility": repro["verdict"],
            "reservation_id": reservation_id, "run_record_sha256": record_sha, "verdict_sha256": verdict_sha,
            "evidence_root": str(root)}


# --- CLI ----------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m proposer.m2_harness",
                                     description="IMP-001 M2 harness. Each command needs its own separate operator authorization.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("dry-run", help="count input tokens and report the cost bound; sends no generation request")
    runner = sub.add_parser("run", help="the single paid attempt")
    runner.add_argument("--authorization-ref", required=True, help="reference to the operator act authorizing this run")
    args = parser.parse_args(argv)

    api_key = os.environ.get(API_KEY_ENV_VAR, "")
    try:
        if args.command == "dry-run":
            out = dry_run(api_key=api_key)
        else:
            out = run(api_key=api_key, authorization_ref=args.authorization_ref)
    except (HarnessStop, SpendGuardError, CountTokensStop, EvidenceError) as exc:
        print(f"STOPPED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
