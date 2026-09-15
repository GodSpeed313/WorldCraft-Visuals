"""
Fusion Engine — C1: Contribution/Placement Classifier.

Spec: docs/fusion_engine_requirements_v0.1.md
  §5  Source Model
  §6  Source Preservation
  §7  Contribution Types
  §8  Architectural Placement

AUTH-004 scope: admission/validation of already-classified, hand-authored
Source data. Automated semantic classification is neither implemented nor
required for this slice.

Boundary (AUTH-004, ADR-001 AD-1): this module must never import the legacy
governance modules or reference their registries or resolution functions.
"""

from __future__ import annotations

from .types import ArchitecturalPlacement, Condition, ContributionType, EpistemicStatus, Source, SourceProperty


class SourceAdmissionError(ValueError):
    """A Source or SourceProperty is malformed.

    A programming-contract violation, not a legitimate spec outcome — unlike
    Provenance.UNRESOLVED or CompatibilityStatus.UNRESOLVED, which are
    ordinary successful results (spec §9.4, §28).
    """


def admit_source(source: Source) -> tuple[SourceProperty, ...]:
    """Validate and admit a hand-authored Source's properties.

    Confirms every property carries a well-formed Contribution Type,
    Architectural Placement, and Epistemic Status (spec §7/§8/§18), and a
    non-empty id and description. Source-Derived baseline provenance (spec
    §9.1) is enforced by SourceProperty's own definition and cannot be
    overridden here or anywhere else.

    Raises SourceAdmissionError on any malformed property rather than
    silently coercing or dropping it — dropping an unrecognized property
    would be exactly the reinterpretation spec §6 forbids.
    """
    if not source.name or not source.name.strip():
        raise SourceAdmissionError("Source must have a non-empty name.")
    if not source.properties:
        raise SourceAdmissionError(f"Source {source.name!r} has no properties to admit.")

    seen_ids: set[str] = set()
    for prop in source.properties:
        if not prop.id or not prop.id.strip():
            raise SourceAdmissionError(f"Source {source.name!r} has a property with no id.")
        if prop.id in seen_ids:
            raise SourceAdmissionError(f"Duplicate property id {prop.id!r} in source {source.name!r}.")
        seen_ids.add(prop.id)

        if not isinstance(prop.contribution_type, ContributionType):
            raise SourceAdmissionError(f"{prop.id}: contribution_type must be a ContributionType.")
        if not isinstance(prop.architectural_placement, ArchitecturalPlacement):
            raise SourceAdmissionError(
                f"{prop.id}: architectural_placement must be an ArchitecturalPlacement."
            )
        if not isinstance(prop.epistemic_status, EpistemicStatus):
            raise SourceAdmissionError(f"{prop.id}: epistemic_status must be an EpistemicStatus.")
        if not prop.description or not prop.description.strip():
            raise SourceAdmissionError(f"{prop.id}: description must not be empty.")
        if prop.activation_condition is not None and not isinstance(prop.activation_condition, Condition):
            raise SourceAdmissionError(f"{prop.id}: activation_condition must be a Condition or None.")

    return source.properties
