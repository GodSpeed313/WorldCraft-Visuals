"""
IMP-001 M2 request construction and spending guard. Standard library only.

The model input is the M1 packet plus ONE fixed instruction with no pair-specific text
(Protocol Revision 2.1, section 1). Temperature is omitted, not defaulted (AUTH, A4);
Claude Opus 5.5 rejects sampling parameters. Thinking is adaptive.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal

from proposer.m2_config import M2Config, Rates
from proposer.m2_evidence import sha256_hex

# Fixed, pair-neutral instruction. It names no character, hints at no mechanism, and
# does not rank anything. Its SHA-256 is recorded with every request.
SYSTEM_PROMPT = (
    "You will receive one JSON packet as the user message. It contains two character "
    "profiles, a requirements document, and a pair-file schema reference. Follow the "
    "requirements document exactly, using only the material in the packet. Return "
    "exactly one output in the format that document defines, with no text before or "
    "after it."
)


class SpendGuardError(RuntimeError):
    """Generation is refused: the spending upper bound is unavailable, unverified or above the cap."""


@dataclass(frozen=True)
class RequestBundle:
    generation_body: dict
    generation_bytes: bytes
    generation_sha256: str
    count_body: dict
    count_bytes: bytes
    system_prompt_sha256: str
    packet_sha256_recomputed: str
    parameters: dict


def _dump(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_request(packet, cfg: M2Config) -> RequestBundle:
    """Build the exact generation request and the matching token-count request.

    The packet text sent is the packet's canonical bytes decoded as UTF-8, so its hash is
    recomputed here from what is actually put in the request, not copied from the packet.
    """
    packet_text = packet.canonical_bytes.decode("utf-8")
    recomputed = sha256_hex(packet_text.encode("utf-8"))
    if recomputed != packet.packet_sha256:
        raise ValueError("the packet text placed in the request does not hash to the packet's own packet_sha256")

    thinking = {"type": cfg.thinking_type}
    messages = [{"role": "user", "content": packet_text}]
    generation = {
        "model": cfg.model,
        "max_tokens": cfg.max_tokens,
        "stream": True,
        "thinking": thinking,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }
    # The token-count endpoint takes the same model, system, messages and thinking
    # configuration; max_tokens and stream are generation-only fields.
    count = {"model": cfg.model, "thinking": thinking, "system": SYSTEM_PROMPT, "messages": messages}
    gen_bytes = _dump(generation)
    return RequestBundle(
        generation_body=generation,
        generation_bytes=gen_bytes,
        generation_sha256=sha256_hex(gen_bytes),
        count_body=count,
        count_bytes=_dump(count),
        system_prompt_sha256=sha256_hex(SYSTEM_PROMPT.encode("utf-8")),
        packet_sha256_recomputed=recomputed,
        parameters={
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "stream": True,
            "thinking": thinking,
            "temperature": "OMITTED (not sent)",
            "system_prompt": SYSTEM_PROMPT,
        },
    )


def _as_tokens(value, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise SpendGuardError(f"{label} is not a non-negative integer: {value!r}")
    return value


def cost_report(input_tokens, max_tokens: int, rates: Rates, cap: Decimal) -> dict:
    """Conservative upper bound: counted input tokens x input rate + max_tokens x output rate."""
    report = {
        "formula": "counted_input_tokens * input_rate + max_tokens * output_rate",
        "counted_input_tokens": input_tokens,
        "max_tokens": max_tokens,
        "input_rate_usd_per_mtok": None if rates.input_per_mtok is None else str(rates.input_per_mtok),
        "output_rate_usd_per_mtok": None if rates.output_per_mtok is None else str(rates.output_per_mtok),
        "rates_source": rates.source,
        "rates_verified": rates.verified,
        "rates_verified_on": rates.verified_on,
        "cap_usd": str(cap),
        "upper_bound_usd": None,
        "within_cap": False,
        "generation_permitted": False,
        "refusal_reason": None,
    }
    try:
        tokens = _as_tokens(input_tokens, "counted input tokens")
        if rates.input_per_mtok is None or rates.output_per_mtok is None:
            raise SpendGuardError("pricing is unavailable")
        bound = (Decimal(tokens) * rates.input_per_mtok + Decimal(max_tokens) * rates.output_per_mtok) / Decimal(1_000_000)
    except SpendGuardError as exc:
        report["refusal_reason"] = str(exc)
        return report
    report["upper_bound_usd"] = str(bound)
    report["within_cap"] = bound <= cap
    if not rates.verified:
        report["refusal_reason"] = "pricing rates are not verified against the provider; generation is refused until they are"
    elif not report["within_cap"]:
        report["refusal_reason"] = f"upper bound {bound} USD exceeds the {cap} USD cap"
    else:
        report["generation_permitted"] = True
    return report


def enforce_spend_guard(report: dict) -> None:
    """Fail closed: anything other than an explicit, verified, within-cap bound refuses generation."""
    if report.get("generation_permitted") is not True or report.get("refusal_reason") is not None:
        raise SpendGuardError(report.get("refusal_reason") or "the spending upper bound could not be established")


__all__ = [
    "RequestBundle",
    "SYSTEM_PROMPT",
    "SpendGuardError",
    "build_request",
    "cost_report",
    "enforce_spend_guard",
]
