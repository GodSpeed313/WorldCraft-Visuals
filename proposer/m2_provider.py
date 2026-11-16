"""
IMP-001 M2 Anthropic provider on the standard library (`http.client`). No SDK, no third-party code.

Transmission-state discipline (AUTH IMP-001 M2 Harness Construction, A1 and A2):

  1. The connection is opened by an explicit `connect()` call, with `auto_open` off so
     http.client can never reconnect and resend behind our back.
  2. Only a failure INSIDE that `connect()` call is proof that no request byte was sent
     (outcome PRE_TRANSMISSION_FAILURE). It is the only outcome that may be retried.
  3. The instant before `request()` is called, the state becomes TRANSMISSION_STARTED.
     Every later failure (send, status line, body read, truncated or errored stream) is
     AMBIGUOUS and stops. A connection exception alone never proves non-transmission.
  4. An explicit HTTP error response (non-200) proves nothing about generation and is
     recorded as HTTP_ERROR. It is never retried.

There is no retry loop outside `send_generation`, and it only loops on outcome 2.
"""

from __future__ import annotations

import http.client
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

from proposer.m2_config import M2Config

COMPLETE = "COMPLETE"
PRE_TRANSMISSION_FAILURE = "PRE_TRANSMISSION_FAILURE"
HTTP_ERROR = "HTTP_ERROR"
AMBIGUOUS = "AMBIGUOUS"
NO_OUTPUT_EXHAUSTED = "NO_OUTPUT_PRE_TRANSMISSION_EXHAUSTED"

_CHUNK = 65536


class StreamIncomplete(ValueError):
    """The event stream is truncated, unparseable, or carried a provider error event."""


class CountTokensStop(RuntimeError):
    """The token-count request failed or was rejected. The dry run stops for operator review."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def default_connection_factory(host: str, timeout: float):
    return http.client.HTTPSConnection(host, timeout=timeout)


@dataclass
class AttemptResult:
    outcome: str
    transmission_started: bool
    http_status: Optional[int] = None
    raw_bytes: bytes = b""
    provider_request_id: Optional[str] = None
    request_sent_utc: Optional[str] = None
    response_complete_utc: Optional[str] = None
    error_class: Optional[str] = None
    error_detail: Optional[str] = None
    recorded_request_headers: dict = field(default_factory=dict)
    message: Optional[dict] = None


@dataclass
class GenerationOutcome:
    status: str
    final: AttemptResult
    attempts: list


# --- event stream -------------------------------------------------------------

def parse_event_stream(raw: bytes) -> dict:
    """Assemble the streamed message. Raises StreamIncomplete unless message_start .. message_stop is intact."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise StreamIncomplete("stream is not valid UTF-8") from None
    message = None
    blocks: dict = {}
    stopped = False
    for chunk in re.split(r"\r?\n\r?\n", text):
        data_lines = []
        for line in chunk.splitlines():
            if line.startswith("data:"):
                data_lines.append(line[5:][1:] if line[5:6] == " " else line[5:])
        if not data_lines:
            continue
        try:
            payload = json.loads("\n".join(data_lines))
        except json.JSONDecodeError:
            raise StreamIncomplete("an event carried unparseable JSON") from None
        kind = payload.get("type") if isinstance(payload, dict) else None
        if kind == "error":
            err = payload.get("error") if isinstance(payload.get("error"), dict) else {}
            raise StreamIncomplete(f"provider error event: {err.get('type', 'unknown')}")
        if kind == "message_start":
            m = payload.get("message") or {}
            message = {"id": m.get("id"), "model": m.get("model"), "role": m.get("role"),
                       "usage": dict(m.get("usage") or {}), "stop_reason": None}
        elif message is None:
            continue
        elif kind == "content_block_start":
            blocks[payload["index"]] = dict(payload.get("content_block") or {})
        elif kind == "content_block_delta":
            block, delta = blocks.get(payload.get("index")), payload.get("delta") or {}
            if block is None:
                raise StreamIncomplete("a delta arrived for a block that never started")
            if delta.get("type") == "text_delta":
                block["text"] = block.get("text", "") + delta.get("text", "")
            elif delta.get("type") == "thinking_delta":
                block["thinking"] = block.get("thinking", "") + delta.get("thinking", "")
            elif delta.get("type") == "signature_delta":
                block["signature"] = delta.get("signature")
        elif kind == "message_delta":
            delta = payload.get("delta") or {}
            if "stop_reason" in delta:
                message["stop_reason"] = delta["stop_reason"]
            if "stop_details" in delta:
                message["stop_details"] = delta["stop_details"]
            message["usage"].update(payload.get("usage") or {})
        elif kind == "message_stop":
            stopped = True
    if message is None or not stopped or message.get("stop_reason") is None:
        raise StreamIncomplete("stream ended before message_stop with a stop_reason")
    message["content"] = [blocks[i] for i in sorted(blocks)]
    return message


def message_text(message: dict) -> str:
    """Concatenated text blocks only (thinking blocks are not part of the proposer's output)."""
    return "".join(b.get("text", "") for b in message.get("content", []) if b.get("type") == "text")


# --- one attempt --------------------------------------------------------------

def transmit(cfg: M2Config, path: str, body: bytes, api_key: str, *, stream: bool,
             connection_factory: Callable = default_connection_factory,
             before_send: Optional[Callable] = None, now: Callable = utc_now) -> AttemptResult:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": cfg.api_version,
        "content-type": "application/json",
        "accept": "text/event-stream" if stream else "application/json",
    }
    recorded = {k: v for k, v in headers.items() if k in cfg.recorded_request_headers}
    result = AttemptResult(outcome=AMBIGUOUS, transmission_started=False, recorded_request_headers=recorded)

    conn = connection_factory(cfg.api_host, cfg.connect_timeout_seconds)
    try:
        if hasattr(conn, "auto_open"):
            conn.auto_open = 0
        try:
            conn.connect()
        except Exception as exc:  # noqa: BLE001 - any failure here happened before any request byte
            result.outcome = PRE_TRANSMISSION_FAILURE
            result.error_class = type(exc).__name__
            result.error_detail = str(exc)
            return result

        sock = getattr(conn, "sock", None)
        if sock is not None:
            sock.settimeout(cfg.read_timeout_seconds)
        if before_send is not None:
            before_send({"path": path, "recorded_request_headers": recorded})  # may raise: nothing sent yet

        result.transmission_started = True          # from here on, nothing proves non-transmission
        result.request_sent_utc = now()
        try:
            conn.request("POST", path, body=body, headers=headers)
            resp = conn.getresponse()
            result.http_status = resp.status
            result.provider_request_id = resp.getheader("request-id") or resp.getheader("x-request-id")
            parts = []
            try:
                while True:
                    chunk = resp.read(_CHUNK)
                    if not chunk:
                        break
                    parts.append(chunk)
            finally:
                result.raw_bytes = b"".join(parts)
        except Exception as exc:  # noqa: BLE001 - post-transmission: ambiguous, never retried
            result.outcome = AMBIGUOUS
            result.error_class = type(exc).__name__
            result.error_detail = str(exc)
            return result

        result.response_complete_utc = now()
        if result.http_status != 200:
            result.outcome = HTTP_ERROR
            return result
        if stream:
            try:
                result.message = parse_event_stream(result.raw_bytes)
            except StreamIncomplete as exc:
                result.outcome = AMBIGUOUS
                result.error_class = "StreamIncomplete"
                result.error_detail = str(exc)
                return result
        result.outcome = COMPLETE
        return result
    finally:
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass


# --- generation with the A2 retry policy --------------------------------------

def send_generation(cfg: M2Config, body: bytes, api_key: str, *, connection_factory: Callable,
                    log_attempt_start: Callable, log_send_intent: Callable, log_attempt_outcome: Callable,
                    sleep: Callable = time.sleep, now: Callable = utc_now) -> GenerationOutcome:
    """Send ONE generation request. Loops only after a proven pre-transmission failure, at most max_retries times.

    The three log_* callbacks write durable evidence; if any raises, the exception propagates
    and nothing further is sent. Retry happens only after the failed attempt's outcome was logged.
    """
    attempts: list = []
    for number in range(1, cfg.max_retries + 2):
        log_attempt_start(number)
        result = transmit(cfg, cfg.messages_path, body, api_key, stream=True,
                          connection_factory=connection_factory,
                          before_send=lambda info, n=number: log_send_intent(n, info), now=now)
        attempts.append({
            "attempt": number, "outcome": result.outcome, "transmission_started": result.transmission_started,
            "http_status": result.http_status, "error_class": result.error_class,
            "request_sent_utc": result.request_sent_utc, "response_complete_utc": result.response_complete_utc,
        })
        log_attempt_outcome(number, result)
        if result.outcome == PRE_TRANSMISSION_FAILURE and number <= cfg.max_retries:
            sleep(cfg.retry_delay_seconds)
            continue
        status = {COMPLETE: COMPLETE, HTTP_ERROR: HTTP_ERROR, AMBIGUOUS: AMBIGUOUS,
                  PRE_TRANSMISSION_FAILURE: NO_OUTPUT_EXHAUSTED}[result.outcome]
        return GenerationOutcome(status=status, final=result, attempts=attempts)
    raise AssertionError("unreachable: the loop always returns")  # pragma: no cover


# --- token count (non-generation) ---------------------------------------------

def count_input_tokens(cfg: M2Config, body: bytes, api_key: str, *, connection_factory: Callable = default_connection_factory,
                       now: Callable = utc_now) -> dict:
    """One token-count request, no retries. Raises CountTokensStop on any rejection or odd response."""
    result = transmit(cfg, cfg.count_tokens_path, body, api_key, stream=False, connection_factory=connection_factory, now=now)
    if result.outcome != COMPLETE:
        detail = result.error_class or f"HTTP {result.http_status}"
        raise CountTokensStop(f"token count did not complete ({result.outcome}: {detail}); provider said: "
                              f"{result.raw_bytes[:500].decode('utf-8', 'replace')!r}")
    try:
        payload = json.loads(result.raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise CountTokensStop("token-count response was not JSON") from None
    if not isinstance(payload, dict):
        raise CountTokensStop("token-count response was not a JSON object")
    tokens = payload.get("input_tokens")
    if "error" in payload or isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0:
        raise CountTokensStop("token-count response had no valid integer input_tokens")
    return {"input_tokens": tokens, "provider_request_id": result.provider_request_id,
            "raw_response": result.raw_bytes, "request_sent_utc": result.request_sent_utc,
            "response_complete_utc": result.response_complete_utc}


__all__ = [
    "AMBIGUOUS", "AttemptResult", "COMPLETE", "CountTokensStop", "GenerationOutcome", "HTTP_ERROR",
    "NO_OUTPUT_EXHAUSTED", "PRE_TRANSMISSION_FAILURE", "StreamIncomplete", "count_input_tokens",
    "default_connection_factory", "message_text", "parse_event_stream", "send_generation", "transmit", "utc_now",
]
