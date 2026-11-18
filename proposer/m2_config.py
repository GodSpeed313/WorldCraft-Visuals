"""
IMP-001 Milestone 2 harness configuration. Standard library only.

This file is the ONLY place the experimental configuration and the evidence/
reservation root are defined. The root is never taken from a command-line flag,
an environment variable, or any per-invocation argument; changing it needs a
reviewed code change and PR (AUTH IMP-001 M2 Harness Construction, A3).

Nothing here authorizes a live call. The harness refuses to transmit a
generation request unless a separate operator authorization is supplied at run
time and every guard in m2_harness passes.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

HARNESS_VERSION = "imp-001-m2-harness/1.0.0"

# Pre-declared M1 packet hash for Ilse Marrow x Sable Quillon (AUTH, section 2).
EXPECTED_PACKET_SHA256 = "de29933eff89bf0803473c305cca9d549e11728f96e4209fb6a72e3a4822b060"

PROVIDER_KEY_PREFIX = "sk-ant-"
API_KEY_ENV_VAR = "ANTHROPIC_API_KEY"

# Declared stricter narrowing of Protocol Revision 2.1 section 6 (AUTH, A2).
RETRY_POLICY_DECLARATION = (
    "A retry is permitted ONLY when the harness established, from its own controlled "
    "connect step, that no byte of the generation request was transmitted. At most two "
    "retries after the initial attempt, inside one uninterrupted invocation. Any failure "
    "once transmission began, any uncertain transmission state, and any explicit HTTP "
    "error response is classified AMBIGUOUS or stopped and is never retried. A new "
    "invocation never resumes or retries an existing reservation. This is stricter than "
    "Protocol Revision 2.1 section 6, which allowed a retry after an HTTP error response."
)


@dataclass(frozen=True)
class Rates:
    """Per-million-token rates. `verified` gates generation; unverified rates fail closed."""

    input_per_mtok: Optional[Decimal]
    output_per_mtok: Optional[Decimal]
    source: str
    verified_on: Optional[str]
    verified: bool


@dataclass(frozen=True)
class M2Config:
    evidence_root: str
    model: str
    max_tokens: int
    pair: tuple
    spend_cap_usd: Decimal
    prepaid_backstop_usd: Decimal
    rates: Rates
    # Pre-declared packet hash for the approved pair; a mismatch stops the run. None skips the check.
    expected_packet_sha256: Optional[str] = None
    thinking_type: str = "adaptive"
    api_host: str = "api.anthropic.com"
    api_version: str = "2023-06-01"
    messages_path: str = "/v1/messages"
    count_tokens_path: str = "/v1/messages/count_tokens"
    max_retries: int = 2
    retry_delay_seconds: float = 5.0
    # http.client timeouts are per socket operation, not whole-request. Streaming keeps
    # the read side alive with pings, so a read timeout means the provider went silent.
    connect_timeout_seconds: float = 30.0
    read_timeout_seconds: float = 300.0
    # Header names recorded in evidence. Everything else (notably x-api-key) is never persisted.
    recorded_request_headers: tuple = ("anthropic-version", "content-type", "accept")


# Standard Claude Opus 5.5 rates, verified on 2026-11-15 against the provider's pricing
# page (https://platform.claude.com/docs/en/about-claude/pricing): $4 / MTok base input,
# $20 / MTok output. They apply to this request, which uses no Batch API, fast mode,
# prompt caching or non-default data residency. Verified pricing only lets the spending
# guard compute its bound; it does not by itself permit generation. The reservation,
# authorization reference, evidence-root and every other guard still apply. Changing a
# rate or the verified flag needs a reviewed code change and PR.
COMMITTED_RATES = Rates(
    input_per_mtok=Decimal("4.00"),
    output_per_mtok=Decimal("20.00"),
    source="https://platform.claude.com/docs/en/about-claude/pricing",
    verified_on="2026-11-15",
    verified=True,
)

COMMITTED_CONFIG = M2Config(
    evidence_root=r"C:\Users\User\WorldCraft-Evidence\imp-001-m2",
    model="claude-opus-5-5",
    max_tokens=64000,
    pair=("ilse_marrow", "sable_quillon"),
    spend_cap_usd=Decimal("2.00"),
    prepaid_backstop_usd=Decimal("5"),
    rates=COMMITTED_RATES,
    expected_packet_sha256=EXPECTED_PACKET_SHA256,
)

__all__ = [
    "API_KEY_ENV_VAR",
    "COMMITTED_CONFIG",
    "COMMITTED_RATES",
    "EXPECTED_PACKET_SHA256",
    "HARNESS_VERSION",
    "M2Config",
    "PROVIDER_KEY_PREFIX",
    "RETRY_POLICY_DECLARATION",
    "Rates",
]
