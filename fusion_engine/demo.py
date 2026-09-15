"""
Fusion Engine — minimal structured demonstration of the C1 -> C2 -> C3 slice.

Prints the pipeline's structured, non-prose output for two scenarios: a
compatible pairing and a contradictory one. This proves the engine path
exists; it does not generate creative prose (that is C6's future role, not
authorized here).

Run: python -m fusion_engine.demo
"""

from __future__ import annotations

import sys

from .fixtures import dev_fixture_001 as fx
from .pipeline import run_slice
from .types import IntermediateFusionResult


def _use_utf8_output() -> None:
    """Force UTF-8 on stdout/stderr, stdlib-only, local to this package.

    Windows consoles default to a codepage that cannot encode this output's
    non-ASCII characters (e.g. section signs). `reconfigure` is Python 3.7+
    stdlib; guarded because a stream without it (or one that refuses
    reconfiguration) should fall back to the platform default rather than
    raise.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _print_result(label: str, result: IntermediateFusionResult) -> None:
    print(f"--- {label} " + "-" * max(1, 50 - len(label)))
    print(f"source_a: {result.source_a.name}")
    for p in result.source_a.properties:
        print(f"  - {p.id}: {p.description}")
        print(
            f"    contribution_type={p.contribution_type.name} "
            f"architectural_placement={p.architectural_placement.name} "
            f"provenance={p.provenance.name}"
        )
    print(f"source_b: {result.source_b.name}")
    for p in result.source_b.properties:
        print(f"  - {p.id}: {p.description}")
        print(
            f"    contribution_type={p.contribution_type.name} "
            f"architectural_placement={p.architectural_placement.name} "
            f"provenance={p.provenance.name}"
        )
    print(f"interaction: {result.interaction.id}")
    print(f"  provenance={result.interaction.provenance.name}")
    print(f"  disclosed_modification={result.interaction.is_disclosed_modification}")
    print(f"emergent_property: {result.emergent_property.id}")
    print(f"  provenance={result.emergent_property_provenance.name}")
    print(f"  ancestry={list(result.emergent_property_ancestry)}")
    print(f"compatibility: {result.compatibility.status.name}")
    if result.compatibility.contradiction:
        print(f"  contradiction={result.compatibility.contradiction}")
    if result.compatibility.required_bridge:
        print(f"  required_bridge={result.compatibility.required_bridge}")
    if result.compatibility.unresolved_reason:
        print(f"  unresolved_reason={result.compatibility.unresolved_reason}")
    print(f"preserved_contribution_ids: {list(result.preserved_contribution_ids)}")
    print()


def main() -> None:
    _use_utf8_output()
    compatible = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.HARMLESS_PAIRING, fx.HARMLESS_PAIRING_RESULT)
    _print_result("COMPATIBLE CASE", compatible)

    incompatible = run_slice(
        fx.SOURCE_A, fx.SOURCE_B, fx.CONFLICTING_FIELD_REQUIREMENT, fx.CONFLICTING_RESULT
    )
    _print_result("INCOMPATIBLE CASE (E=0 vs E>0)", incompatible)

    conditionally_compatible = run_slice(
        fx.SOURCE_A, fx.SOURCE_B, fx.DISCLOSED_FIELD_BRIDGE, fx.DISCLOSED_BRIDGE_RESULT
    )
    _print_result("CONDITIONALLY COMPATIBLE CASE (disclosed bridge)", conditionally_compatible)

    unresolved = run_slice(fx.SOURCE_A, fx.SOURCE_B, fx.UNRESOLVED_COUPLING, fx.UNRESOLVED_RESULT)
    _print_result("UNRESOLVED CASE", unresolved)


if __name__ == "__main__":
    main()
