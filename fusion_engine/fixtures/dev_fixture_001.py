"""
Fusion Engine — development fixture 001.

SYNTHETIC DEVELOPMENT DATA. These two sources are not drawn from, and are
not a substitute for, any entry in the legacy character or power registries.
They carry no WorldCraft lore standing of any kind and exist solely to
exercise the C1 -> C2 -> C3 slice's structural requirements: limitations,
activation conditions, provenance, interaction rules, compatibility, and
contradiction.

Names are bracket-tagged "[DEV FIXTURE]" so nothing downstream can mistake
them for canonical WorldCraft content.
"""

from __future__ import annotations

from ..types import (
    ArchitecturalPlacement,
    Condition,
    ContributionType,
    EmergentProperty,
    EpistemicStatus,
    InteractionRule,
    Provenance,
    Source,
    SourceProperty,
)

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

SOURCE_A = Source(
    name="[DEV FIXTURE] Prototype Kinetic Relay",
    properties=(
        SourceProperty(
            id="a.kinetic_discharge",
            description="Releases stored kinetic charge in a single directed pulse.",
            contribution_type=ContributionType.MECHANISM,
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
            activation_condition=Condition(variable="E", comparator="==", value=0.0),
        ),
        SourceProperty(
            id="a.layered_plating",
            description="Passive plating that absorbs a bounded amount of incoming force.",
            contribution_type=ContributionType.MECHANISM,
            architectural_placement=ArchitecturalPlacement.LIMITATIONS,
            epistemic_status=EpistemicStatus.FICTIONAL,
            is_hard_limitation=True,
        ),
    ),
)

SOURCE_B = Source(
    name="[DEV FIXTURE] Prototype Field Conduit",
    properties=(
        SourceProperty(
            id="b.ambient_field_draw",
            description="Draws continuously from an ambient energy field to stay active.",
            contribution_type=ContributionType.ABILITY,
            architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
            epistemic_status=EpistemicStatus.FICTIONAL,
            activation_condition=Condition(variable="E", comparator=">", value=0.0),
        ),
        SourceProperty(
            id="b.signal_dampening",
            description="Suppresses stray signal frequencies outside its own operating band.",
            contribution_type=ContributionType.BEHAVIOR,
            architectural_placement=ArchitecturalPlacement.SECONDARY_EFFECTS,
            epistemic_status=EpistemicStatus.FICTIONAL,
            is_prohibition=True,
        ),
    ),
)

# ---------------------------------------------------------------------------
# Interaction rules — one per exercised C3 outcome
# ---------------------------------------------------------------------------

HARMLESS_PAIRING = InteractionRule(
    id="interaction.harmless_pairing",
    description="Layered Plating and Signal Dampening operate independently with no shared "
    "operating condition.",
    dependency_ids=("a.layered_plating", "b.signal_dampening"),
    provenance=Provenance.DEFENSIBLY_DERIVED,
)

CONFLICTING_FIELD_REQUIREMENT = InteractionRule(
    id="interaction.conflicting_field_requirement",
    description="Kinetic Discharge and Ambient Field Draw are proposed to operate together.",
    dependency_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    provenance=Provenance.DEFENSIBLY_DERIVED,
)

DISCLOSED_FIELD_BRIDGE = InteractionRule(
    id="interaction.disclosed_field_bridge",
    description="An explicitly disclosed buffer rule letting Kinetic Discharge fire during a "
    "brief zero-crossing window of Ambient Field Draw's cycle, instead of requiring E=0 for the "
    "full operating period.",
    dependency_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    provenance=Provenance.INVENTED_BRIDGE,
    is_disclosed_modification=True,
)

UNRESOLVED_COUPLING = InteractionRule(
    id="interaction.unresolved_coupling",
    description="Whether these two mechanics can be coupled at all is not established by either "
    "source.",
    dependency_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    provenance=Provenance.UNRESOLVED,
)

# ---------------------------------------------------------------------------
# Emergent properties — one per interaction rule above
# ---------------------------------------------------------------------------

HARMLESS_PAIRING_RESULT = EmergentProperty(
    id="emergent.combined_passive_defense",
    description="Combined passive resilience from plating and dampening operating together.",
    direct_ancestor_ids=("a.layered_plating", "b.signal_dampening"),
    governing_rule_id=HARMLESS_PAIRING.id,
    contribution_type=ContributionType.MECHANISM,
    architectural_placement=ArchitecturalPlacement.EMERGENT_PROPERTY,
)

CONFLICTING_RESULT = EmergentProperty(
    id="emergent.field_discharge_coupling",
    description="Proposed coupling between Kinetic Discharge and Ambient Field Draw.",
    direct_ancestor_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    governing_rule_id=CONFLICTING_FIELD_REQUIREMENT.id,
    contribution_type=ContributionType.MECHANISM,
    architectural_placement=ArchitecturalPlacement.EMERGENT_PROPERTY,
)

DISCLOSED_BRIDGE_RESULT = EmergentProperty(
    id="emergent.buffered_field_discharge_coupling",
    description="Buffered coupling between Kinetic Discharge and Ambient Field Draw via the "
    "disclosed zero-crossing bridge.",
    direct_ancestor_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    governing_rule_id=DISCLOSED_FIELD_BRIDGE.id,
    contribution_type=ContributionType.MECHANISM,
    architectural_placement=ArchitecturalPlacement.EMERGENT_PROPERTY,
)

UNRESOLVED_RESULT = EmergentProperty(
    id="emergent.unresolved_field_discharge_coupling",
    description="Unresolved proposed coupling between Kinetic Discharge and Ambient Field Draw.",
    direct_ancestor_ids=("a.kinetic_discharge", "b.ambient_field_draw"),
    governing_rule_id=UNRESOLVED_COUPLING.id,
    contribution_type=ContributionType.MECHANISM,
    architectural_placement=ArchitecturalPlacement.EMERGENT_PROPERTY,
)
