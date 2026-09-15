"""
Fusion Engine — C2: Provenance Ledger.

Spec: docs/fusion_engine_requirements_v0.1.md §9-§11, INV-01 through INV-08.

The structural home of every mechanic-derivation provenance state: the
single place every other component reads a provenance value from (INV-01,
INV-02). No component other than this ledger may compute or assert a
competing provenance value for an id it already tracks.

Boundary (AUTH-004, ADR-001 AD-1): this module must never import the legacy
governance modules or reference their registries or resolution functions.
"""

from __future__ import annotations

from .types import EmergentProperty, InteractionRule, Provenance, SourceProperty


class ProvenanceLedgerError(ValueError):
    """A programming-contract violation against the ledger's own invariants."""


class ProvenanceLedger:
    """The single authoritative provenance store (INV-01, INV-02).

    Every id registered here has exactly one provenance value, readable only
    through `get()`. Registration is one-shot: an id cannot be re-registered
    with a different value, which makes INV-01's "one authoritative state"
    a property the ledger enforces mechanically rather than by convention.
    """

    def __init__(self) -> None:
        self._provenance: dict[str, Provenance] = {}
        self._dependencies: dict[str, tuple[str, ...]] = {}

    def register_source_property(self, prop: SourceProperty) -> None:
        """Register a Source-Derived leaf (spec §9.1)."""
        self._register(prop.id, prop.provenance, dependency_ids=())

    def register_interaction_rule(self, rule: InteractionRule) -> None:
        """Register an interaction/transformation rule's own, independently
        supplied provenance (INV-04) — recorded as given, never computed
        from its dependencies. Dependency ids are recorded for ancestry
        queries only; they do not affect the rule's own registered value.
        """
        for dep_id in rule.dependency_ids:
            if dep_id not in self._provenance:
                raise ProvenanceLedgerError(
                    f"Interaction {rule.id!r} depends on unregistered id {dep_id!r}. "
                    "Every dependency must be registered before the rule that uses it."
                )
        self._register(rule.id, rule.provenance, dependency_ids=rule.dependency_ids)

    def register_emergent_property(
        self, emergent: EmergentProperty, governing_rule: InteractionRule
    ) -> Provenance:
        """Compute and register an emergent property's provenance as the
        weakest link across its direct ancestors' provenance and its
        governing rule's own provenance (INV-04, INV-05). Because each
        ancestor's provenance was itself computed the same way, this
        computation is correct through multi-hop chains without walking the
        full graph each time (INV-06) — no downstream hop resets provenance.
        """
        required_ids = (*emergent.direct_ancestor_ids, governing_rule.id)
        for dep_id in required_ids:
            if dep_id not in self._provenance:
                raise ProvenanceLedgerError(
                    f"Emergent property {emergent.id!r} depends on unregistered id {dep_id!r}."
                )
        if emergent.governing_rule_id != governing_rule.id:
            raise ProvenanceLedgerError(
                f"Emergent property {emergent.id!r}.governing_rule_id "
                f"({emergent.governing_rule_id!r}) does not match the rule passed in "
                f"({governing_rule.id!r})."
            )

        dependency_provenances = [self._provenance[d] for d in emergent.direct_ancestor_ids]
        rule_provenance = self._provenance[governing_rule.id]
        computed = min([rule_provenance, *dependency_provenances])  # weakest link, INV-05
        self._register(emergent.id, computed, dependency_ids=required_ids)
        return computed

    def get(self, item_id: str) -> Provenance:
        """The only sanctioned read path (INV-02)."""
        if item_id not in self._provenance:
            raise ProvenanceLedgerError(f"{item_id!r} is not registered in this ledger.")
        return self._provenance[item_id]

    def get_ancestry(self, item_id: str) -> tuple[str, ...]:
        """Every id in item_id's full dependency chain (multi-hop, INV-06).

        Deterministic for a fixed graph: a depth-first walk that visits each
        ancestor once, in a stable order derived from each node's own
        declared dependency order.
        """
        if item_id not in self._dependencies:
            raise ProvenanceLedgerError(f"{item_id!r} is not registered in this ledger.")
        seen: set[str] = set()
        ordered: list[str] = []

        def _walk(node_id: str) -> None:
            for dep_id in self._dependencies.get(node_id, ()):
                if dep_id not in seen:
                    seen.add(dep_id)
                    ordered.append(dep_id)
                    _walk(dep_id)

        _walk(item_id)
        return tuple(ordered)

    def invented_ancestors(self, item_id: str) -> tuple[str, ...]:
        """INV-08 — every ancestor of item_id whose own registered
        provenance is Invented Bridge or weaker.

        Invented ancestry may become indirect; it must not disappear
        (INV-08). Because this reads the same ledger every provenance value
        comes from, an invented ancestor cannot silently drop out of this
        list without also dropping out of the provenance it feeds.
        """
        return tuple(
            anc for anc in self.get_ancestry(item_id) if self._provenance[anc] <= Provenance.INVENTED_BRIDGE
        )

    def _register(self, item_id: str, provenance: Provenance, dependency_ids: tuple[str, ...]) -> None:
        if item_id in self._provenance:
            raise ProvenanceLedgerError(f"{item_id!r} is already registered; provenance is not reassignable.")
        self._provenance[item_id] = provenance
        self._dependencies[item_id] = dependency_ids
