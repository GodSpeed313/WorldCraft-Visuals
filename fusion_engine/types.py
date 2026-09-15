"""
Fusion Engine — foundational types.

Names the vocabulary C1, C2, and C3 operate on. Defines no behavior.

Spec: docs/fusion_engine_requirements_v0.1.md
  - Contribution Type: §7
  - Architectural Placement: §8
  - Epistemic Status: §18
  - Provenance ordering: §9, CHECK-05
  - Compatibility outcomes: §14
  - State-Identity Principle (natural-language labels are not globally
    unique; authoritative state identities are): §4.4, CHECK-04, CHECK-08
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional


class ContributionType(Enum):
    """Spec §7 — what kind of thing a source contributes."""

    MECHANISM = "MECHANISM"
    ABILITY = "ABILITY"
    KNOWLEDGE = "KNOWLEDGE"
    RESOURCE = "RESOURCE"
    BEHAVIOR = "BEHAVIOR"
    CONCEPTUAL_ROLE = "CONCEPTUAL_ROLE"
    OBJECT_RELATIONSHIP = "OBJECT_RELATIONSHIP"
    GOVERNING_RULE = "GOVERNING_RULE"


class ArchitecturalPlacement(Enum):
    """Spec §8 — where a contribution functions within the fused system."""

    DOMAIN = "DOMAIN"
    AUTHORITY = "AUTHORITY"
    CORE_MECHANISM = "CORE_MECHANISM"
    ACTIVATION = "ACTIVATION"
    SCOPE = "SCOPE"
    MANIFESTATION = "MANIFESTATION"
    SECONDARY_EFFECTS = "SECONDARY_EFFECTS"
    INTERACTIONS = "INTERACTIONS"
    LIMITATIONS = "LIMITATIONS"
    EMERGENT_PROPERTY = "EMERGENT_PROPERTY"


class EpistemicStatus(Enum):
    """Spec §18 — evidentiary/ontological standing a SOURCE claims.

    Orthogonal to Provenance (spec §18.1, INV-14): this axis never answers
    how a fused mechanic was derived, only what standing its source claims.
    """

    ESTABLISHED = "ESTABLISHED"
    REPORTED = "REPORTED"
    CLAIMED = "CLAIMED"
    FICTIONAL = "FICTIONAL"
    MYTHOLOGICAL = "MYTHOLOGICAL"
    SPECULATIVE = "SPECULATIVE"
    UNRESOLVED = "UNRESOLVED"


class Provenance(IntEnum):
    """Spec §9 / CHECK-05 — mechanic-derivation provenance, ranked strongest
    to weakest so the weakest-link function (INV-05) is `min()` over these
    values rather than a hand-written comparison the ordering could drift
    from.

    Do not compare against CompatibilityStatus. They are unrelated types
    (spec §4.4 State-Identity Principle; CHECK-04) even though both happen to
    define an UNRESOLVED member.
    """

    UNRESOLVED = 0
    INVENTED_BRIDGE = 1
    DEFENSIBLY_DERIVED = 2
    SOURCE_DERIVED = 3


class CompatibilityStatus(Enum):
    """Spec §14 — fusion-compatibility outcome.

    A plain Enum, not an IntEnum: compatibility carries no strength ordering
    the way provenance does. Using a structurally different Enum base than
    Provenance means `CompatibilityStatus.UNRESOLVED == Provenance.UNRESOLVED`
    is False by construction, not merely by convention.
    """

    COMPATIBLE = "COMPATIBLE"
    CONDITIONALLY_COMPATIBLE = "CONDITIONALLY_COMPATIBLE"
    INCOMPATIBLE = "INCOMPATIBLE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class Condition:
    """A literal, explicit operating-condition predicate — e.g. E = 0.

    Deliberately not a free-text string. This slice's contradiction check
    (spec §4.2's worked E=0 / E>0 example) needs only numeric-comparator
    reasoning; representing conditions this way keeps that check a small,
    auditable function rather than a parser.
    """

    variable: str
    comparator: str  # one of "==", ">", "<", ">=", "<="
    value: float


@dataclass(frozen=True)
class SourceProperty:
    """Spec §5/§6/§7/§8 — one substantive property of a Source.

    `provenance` is fixed at SOURCE_DERIVED for every SourceProperty and is
    not a constructor argument: a raw, unfused property is by definition
    established directly by its source (spec §9.1). Only a computed
    interaction or emergent property (see the Provenance Ledger) can carry a
    weaker classification.
    """

    id: str
    description: str
    contribution_type: ContributionType
    architectural_placement: ArchitecturalPlacement
    epistemic_status: EpistemicStatus
    is_hard_limitation: bool = False
    is_prohibition: bool = False
    activation_condition: Optional[Condition] = None
    provenance: Provenance = field(default=Provenance.SOURCE_DERIVED, init=False)


@dataclass(frozen=True)
class Source:
    """Spec §5 — a fusion source: a defined entity supplied as input."""

    name: str
    properties: tuple[SourceProperty, ...]


@dataclass(frozen=True)
class InteractionRule:
    """Spec §9/§12, INV-04 — a rule that combines, modifies, transforms,
    amplifies, converts, constrains, or otherwise changes one or more
    ancestor properties.

    `provenance` is supplied directly by whoever authors the rule,
    independently of its dependencies' provenance (INV-04) — it is never
    inferred from them.
    """

    id: str
    description: str
    dependency_ids: tuple[str, ...]
    provenance: Provenance
    is_disclosed_modification: bool = False  # spec §14 Conditionally Compatible


@dataclass(frozen=True)
class EmergentProperty:
    """Spec §12 — a property that exists only because ancestors interacted
    or were transformed under a named governing rule.

    Provenance is deliberately NOT a field here: it is always read from the
    Provenance Ledger (C2), never asserted independently on this object
    (INV-01, INV-02).
    """

    id: str
    description: str
    direct_ancestor_ids: tuple[str, ...]
    governing_rule_id: str
    contribution_type: ContributionType
    architectural_placement: ArchitecturalPlacement


@dataclass(frozen=True)
class CompatibilityResult:
    """Spec §14/§24 — C3's output shape."""

    status: CompatibilityStatus
    contradiction: Optional[str] = None
    required_bridge: Optional[str] = None
    unresolved_reason: Optional[str] = None


@dataclass(frozen=True)
class IntermediateFusionResult:
    """The slice's structured, non-prose output.

    Deliberately a proper subset of the eventual spec §24 Structured
    Reasoning Record: Source Contributions, Interaction, one Emergent
    Property, and Compatibility are present. Dominance and full Audit
    Findings are absent — not stubbed with placeholder values — because C4
    and C5 own them and have not been built.
    """

    source_a: Source
    source_b: Source
    interaction: InteractionRule
    emergent_property: EmergentProperty
    emergent_property_provenance: Provenance
    emergent_property_ancestry: tuple[str, ...]
    compatibility: CompatibilityResult
    preserved_contribution_ids: tuple[str, ...]
