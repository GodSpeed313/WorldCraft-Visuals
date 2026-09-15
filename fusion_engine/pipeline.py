"""
Fusion Engine — integration path (C1 -> C2 -> C3).

Wires the three authorized components into one deterministic, inspectable
slice: Source A + Source B -> C1 -> C2 -> C3 -> IntermediateFusionResult.

No C4 (Dominance), C5 (Structured Reasoning Record), or C6 (Presentation) is
implemented or invoked here — AUTH-004 does not authorize them.

Boundary (AUTH-004, ADR-001 AD-1): this module must never import the legacy
governance modules or reference their registries or resolution functions.
"""

from __future__ import annotations

from .c1_classifier import SourceAdmissionError, admit_source
from .c2_ledger import ProvenanceLedger
from .c3_compatibility import evaluate_compatibility
from .types import (
    CompatibilityStatus,
    EmergentProperty,
    IntermediateFusionResult,
    InteractionRule,
    Source,
)


def run_slice(
    source_a: Source,
    source_b: Source,
    interaction: InteractionRule,
    emergent_property: EmergentProperty,
) -> IntermediateFusionResult:
    """Run the full C1 -> C2 -> C3 slice for one fixture pair.

    `interaction.dependency_ids` must be ids already present among
    source_a's and source_b's admitted properties.
    `emergent_property.governing_rule_id` must equal `interaction.id`, and
    `emergent_property.direct_ancestor_ids` must be a subset of the same
    admitted property ids.
    """
    properties_a = admit_source(source_a)
    properties_b = admit_source(source_b)

    # admit_source only guards against a duplicate id WITHIN one source; a
    # collision ACROSS the two sources would otherwise surface only as an
    # opaque re-registration failure deep in the ledger. Catching it here,
    # explicitly, keeps identity preservation (spec §6) a C1-shaped concern
    # with a diagnosable message naming both sources.
    ids_a = {p.id for p in properties_a}
    ids_b = {p.id for p in properties_b}
    colliding_ids = ids_a & ids_b
    if colliding_ids:
        raise SourceAdmissionError(
            f"Property id(s) {sorted(colliding_ids)!r} appear in both {source_a.name!r} and "
            f"{source_b.name!r}. Source property ids must be unique across the whole fusion."
        )

    all_properties = properties_a + properties_b

    ledger = ProvenanceLedger()
    for prop in all_properties:
        ledger.register_source_property(prop)

    ledger.register_interaction_rule(interaction)
    emergent_provenance = ledger.register_emergent_property(emergent_property, interaction)

    relevant_properties = tuple(p for p in all_properties if p.id in interaction.dependency_ids)
    compatibility = evaluate_compatibility(relevant_properties, interaction)

    # INV-19 — preserve every independently-classified contribution that does
    # not depend on the interaction responsible for a non-Compatible
    # classification. This slice evaluates exactly one interaction, so "does
    # not depend on it" reduces to "not among its dependency ids"; a future
    # multi-interaction slice would need to walk the ledger's ancestry graph
    # instead, which register_emergent_property's dependency tracking already
    # supports. INV-07's own exclusions are not reintroduced here — nothing
    # excluded from preservation by an Unresolved dependency is reclassified.
    if compatibility.status == CompatibilityStatus.COMPATIBLE:
        preserved_ids = tuple(p.id for p in all_properties)
    else:
        preserved_ids = tuple(p.id for p in all_properties if p.id not in interaction.dependency_ids)

    ancestry = ledger.get_ancestry(emergent_property.id)

    return IntermediateFusionResult(
        source_a=source_a,
        source_b=source_b,
        interaction=interaction,
        emergent_property=emergent_property,
        emergent_property_provenance=emergent_provenance,
        emergent_property_ancestry=ancestry,
        compatibility=compatibility,
        preserved_contribution_ids=preserved_ids,
    )
