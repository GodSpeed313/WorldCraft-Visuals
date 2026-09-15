"""
Fusion Engine — C3: Contradiction/Compatibility Evaluator.

Spec: docs/fusion_engine_requirements_v0.1.md §14, INV-09, INV-10, INV-11.

Structurally distinct from the legacy auditor's grounding function: refusal
and Unresolved are first-class successful outcomes here (spec §28), never
exceptions, and nothing in this module guarantees a substitute or a rescue
always exists.

Boundary (AUTH-004, ADR-001 AD-1): this module must never import the legacy
governance modules or reference their registries or resolution functions.
"""

from __future__ import annotations

from .types import CompatibilityResult, CompatibilityStatus, Condition, InteractionRule, Provenance, SourceProperty

_INF = float("inf")


def _bounds(condition: Condition) -> tuple[float, bool, float, bool]:
    """(lo, lo_inclusive, hi, hi_inclusive) for one comparator/value pair.

    Scoped deliberately to what this slice needs: "==", ">", "<", ">=", "<=".
    "!=" is not supported — representing it exactly requires an
    excluded-point interval, which no fixture in this slice needs, and this
    slice is explicit-predicate, not a general constraint solver.
    """
    comparator, value = condition.comparator, condition.value
    if comparator == "==":
        return (value, True, value, True)
    if comparator == ">":
        return (value, False, _INF, True)
    if comparator == ">=":
        return (value, True, _INF, True)
    if comparator == "<":
        return (-_INF, True, value, False)
    if comparator == "<=":
        return (-_INF, True, value, True)
    raise ValueError(
        f"Comparator {comparator!r} is not supported by this slice's explicit "
        "predicate model (supported: ==, >, <, >=, <=)."
    )


def _bound_includes(point: float, lo: float, lo_inc: bool, hi: float, hi_inc: bool) -> bool:
    if point < lo or point > hi:
        return False
    if point == lo and not lo_inc:
        return False
    if point == hi and not hi_inc:
        return False
    return True


def _conditions_contradict(a: Condition, b: Condition) -> bool:
    """True iff no value of the shared variable can satisfy both conditions
    simultaneously — spec §4.2's worked example (E=0 vs E>0), generalized to
    the small comparator set this slice supports.
    """
    if a.variable != b.variable:
        return False

    a_lo, a_lo_inc, a_hi, a_hi_inc = _bounds(a)
    b_lo, b_lo_inc, b_hi, b_hi_inc = _bounds(b)
    lo = max(a_lo, b_lo)
    hi = min(a_hi, b_hi)

    if lo > hi:
        return True
    if lo < hi:
        return False

    point = lo
    overlaps = _bound_includes(point, a_lo, a_lo_inc, a_hi, a_hi_inc) and _bound_includes(
        point, b_lo, b_lo_inc, b_hi, b_hi_inc
    )
    return not overlaps


def evaluate_compatibility(
    relevant_properties: tuple[SourceProperty, ...],
    interaction: InteractionRule,
) -> CompatibilityResult:
    """Evaluate compatibility of the properties a candidate interaction
    requires (spec §14).

    `relevant_properties` should be exactly the properties the interaction
    depends on — compatibility is evaluated for what this fusion actually
    requires operating together, not a blanket scan of every property either
    source happens to carry.

    Returns one of Compatible / Conditionally Compatible / Incompatible /
    Unresolved as an ordinary result. Never raises for a legitimate
    spec-defined outcome (spec §28).
    """
    if interaction.provenance == Provenance.UNRESOLVED:
        return CompatibilityResult(
            status=CompatibilityStatus.UNRESOLVED,
            unresolved_reason=(
                f"Interaction {interaction.id!r} is itself Unresolved (spec §9.4) — "
                "available source rules are insufficient to determine whether it "
                "validly governs these properties."
            ),
        )

    conditioned = [p for p in relevant_properties if p.activation_condition is not None]

    contradiction = None
    for i, p1 in enumerate(conditioned):
        for p2 in conditioned[i + 1 :]:
            if _conditions_contradict(p1.activation_condition, p2.activation_condition):
                contradiction = (
                    f"{p1.id} requires {p1.activation_condition.variable} "
                    f"{p1.activation_condition.comparator} {p1.activation_condition.value}, "
                    f"but {p2.id} requires {p2.activation_condition.variable} "
                    f"{p2.activation_condition.comparator} {p2.activation_condition.value}, "
                    "during the same simultaneous operating condition (spec §4.2)."
                )
                break
        if contradiction:
            break

    if contradiction is None:
        return CompatibilityResult(status=CompatibilityStatus.COMPATIBLE)

    # A contradiction exists. It may be rescued only by an interaction whose
    # author has explicitly disclosed it as a modification (spec §14:
    # "The required modification must be named.") — never silently (INV-11:
    # no relabeling, suppression, or hidden exception).
    if interaction.is_disclosed_modification:
        return CompatibilityResult(
            status=CompatibilityStatus.CONDITIONALLY_COMPATIBLE,
            required_bridge=interaction.description,
        )

    return CompatibilityResult(status=CompatibilityStatus.INCOMPATIBLE, contradiction=contradiction)
