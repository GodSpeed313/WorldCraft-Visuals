"""
Fusion Synthesis — C5-min: assemble one card record (AUTH-011 §1, §3).

Runs the existing, unmodified Fusion Engine C1 -> C2 -> C3 slice for a pair and
collects its structured output, plus the authored fields, into one ordered
record. It generates nothing: every trait outcome, rule and descriptor is authored.
The prompt, the composed paragraph and the leak check are added by render.py.
"""

from __future__ import annotations

from fusion_engine.pipeline import run_slice
from fusion_engine.types import EmergentProperty, InteractionRule, Provenance

from .loader import Library, build_source
from .schema import FIXED_DOMINANCE, PairCard, visual_traits_of

CARD_SCHEMA = "fusion-synthesis-card/1"


def assemble_card(library: Library, pair: PairCard) -> dict:
    card_a, card_b = library.characters[pair.a], library.characters[pair.b]
    props = {}
    for owner, side in ((card_a, "A"), (card_b, "B")):
        for p in owner.properties:
            props[p.id] = (p, owner.name, side)
    vis_owner = {}
    for owner in (card_a, card_b):
        for t in owner.visual_traits:
            vis_owner[t.id] = owner.name

    interaction = InteractionRule(
        id=pair.interaction.id,
        description=pair.interaction.description,
        dependency_ids=pair.interaction.dependency_ids,
        provenance=Provenance[pair.interaction.provenance],
        is_disclosed_modification=pair.interaction.is_disclosed_modification,
    )
    emergent = EmergentProperty(
        id=pair.emergent.id,
        description=pair.emergent.description,
        direct_ancestor_ids=pair.emergent.direct_ancestor_ids,
        governing_rule_id=interaction.id,
        contribution_type=pair.emergent.contribution_type,
        architectural_placement=pair.emergent.architectural_placement,
    )
    result = run_slice(build_source(card_a), build_source(card_b), interaction, emergent)

    evaluated = sum(1 for pid in interaction.dependency_ids if props[pid][0].activation_condition is not None)

    rows = []
    for label, trait in visual_traits_of(pair):
        parents = []
        for pid in trait.parent_ids:
            parents.append(
                {"id": pid, "character": vis_owner[pid] if pid in vis_owner else "emergent ability"}
            )
        row = {
            "slot": label,
            "descriptor": trait.descriptor,
            "origin": trait.origin,
            "parent_ids": list(trait.parent_ids),
            "parents": parents,
        }
        if trait.design_delta is not None:
            row["design_delta"] = {
                "changed": trait.design_delta.changed,
                "from": trait.design_delta.from_text,
                "to": trait.design_delta.to_text,
            }
        rows.append(row)

    traits = []
    for o in pair.trait_outcomes:
        p, owner_name, side = props[o.property_id]
        entry = {
            "property_id": p.id,
            "name": p.name,
            "source": side,
            "character": owner_name,
            "outcome": o.outcome,
            "result_text": o.result_text,
            "contribution_type": p.contribution_type.name,
            "epistemic_status": "FICTIONAL",
            "provenance": Provenance.SOURCE_DERIVED.name,
        }
        if o.reason is not None:
            entry["reason"] = o.reason
        traits.append(entry)

    inherited_limits = []
    for pid in pair.emergent.direct_ancestor_ids:
        p, owner_name, side = props[pid]
        if p.is_hard_limitation or p.is_prohibition:
            inherited_limits.append(
                {
                    "property_id": p.id,
                    "name": p.name,
                    "character": owner_name,
                    "kind": "prohibition" if p.is_prohibition else "hard limitation",
                    "description": p.description,
                }
            )

    ancestry = []
    for aid in result.emergent_property_ancestry:
        if aid == interaction.id:
            ancestry.append({"id": aid, "kind": "interaction rule", "provenance": interaction.provenance.name})
        else:
            _, owner_name, _side = props[aid]
            ancestry.append(
                {"id": aid, "kind": "source property", "character": owner_name,
                 "provenance": Provenance.SOURCE_DERIVED.name}
            )

    compat = result.compatibility
    return {
        "schema": CARD_SCHEMA,
        "fusion_name": pair.fusion_name,
        "sources": {"A": pair.a, "B": pair.b},
        "concept": pair.concept,
        "dominance": {
            "value": FIXED_DOMINANCE,
            "applied": False,
            "note": "fixed in Phase 1; not applied as a weighting",
        },
        "appearance": {
            "subject": pair.visual.subject.descriptor,
            "slots": {slot: trait.descriptor for slot, trait in pair.visual.slots},
            "scene": {field: trait.descriptor for field, trait in pair.visual.scene},
        },
        "visual_provenance": rows,
        "traits": traits,
        "emergent_ability": {
            "id": pair.emergent.id,
            "name": pair.emergent.name,
            "description": pair.emergent.description,
            "governing_rule": {
                "id": interaction.id,
                "description": interaction.description,
                "provenance": interaction.provenance.name,
            },
            "provenance": result.emergent_property_provenance.name,
            "direct_ancestor_ids": list(pair.emergent.direct_ancestor_ids),
            "activation": pair.emergent.activation,
            "limitations": list(pair.emergent.limitations),
            "inherited_limitations": inherited_limits,
        },
        "exclusions": [
            {
                "item": x.item,
                "source": x.source,
                "character": pair.a if x.source == "A" else pair.b,
                "reason": x.reason,
            }
            for x in pair.exclusions
        ],
        "compatibility": {
            "status": compat.status.name,
            "evaluated_conditions": evaluated,
            "contradiction": compat.contradiction,
            "required_bridge": compat.required_bridge,
            "unresolved_reason": compat.unresolved_reason,
        },
        "ancestry": ancestry,
        # The engine's INV-19 value, unchanged. "Recorded" = accounted for in the structured result,
        # including contributions marked not_carried; it does not mean they were inherited.
        "recorded_contribution_ids": list(result.preserved_contribution_ids),
    }
