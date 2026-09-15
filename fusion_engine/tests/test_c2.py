"""C2 (Provenance Ledger) tests: INV-01 through INV-08."""

import itertools
import unittest

from fusion_engine.c2_ledger import ProvenanceLedger, ProvenanceLedgerError
from fusion_engine.types import (
    ArchitecturalPlacement,
    ContributionType,
    EmergentProperty,
    EpistemicStatus,
    InteractionRule,
    Provenance,
    SourceProperty,
)


def _leaf(prop_id):
    return SourceProperty(
        id=prop_id,
        description=f"Leaf property {prop_id}.",
        contribution_type=ContributionType.MECHANISM,
        architectural_placement=ArchitecturalPlacement.CORE_MECHANISM,
        epistemic_status=EpistemicStatus.FICTIONAL,
    )


def _emergent(prop_id, ancestor_ids, rule_id):
    return EmergentProperty(
        id=prop_id,
        description=f"Emergent property {prop_id}.",
        direct_ancestor_ids=tuple(ancestor_ids),
        governing_rule_id=rule_id,
        contribution_type=ContributionType.MECHANISM,
        architectural_placement=ArchitecturalPlacement.EMERGENT_PROPERTY,
    )


class TestAuthoritativeProvenanceConsistency(unittest.TestCase):
    def test_get_matches_what_was_registered_regardless_of_call_site(self):
        # INV-01/INV-02: every read of the same id, from anywhere, must
        # return the identical authoritative value.
        ledger = ProvenanceLedger()
        leaf = _leaf("x")
        ledger.register_source_property(leaf)

        first_read = ledger.get("x")
        second_read = ledger.get("x")
        self.assertEqual(first_read, second_read)
        self.assertEqual(first_read, Provenance.SOURCE_DERIVED)

    def test_cannot_reregister_an_id(self):
        ledger = ProvenanceLedger()
        ledger.register_source_property(_leaf("x"))
        with self.assertRaises(ProvenanceLedgerError):
            ledger.register_source_property(_leaf("x"))

    def test_get_unregistered_id_rejected(self):
        ledger = ProvenanceLedger()
        with self.assertRaises(ProvenanceLedgerError):
            ledger.get("never-registered")


class TestWeakestLinkComputation(unittest.TestCase):
    def test_all_rank_combinations(self):
        # INV-05: descendant provenance is the weakest link across every
        # required dependency plus the governing rule's own provenance.
        ranks = list(Provenance)
        for rule_rank, dep_rank in itertools.product(ranks, repeat=2):
            with self.subTest(rule_rank=rule_rank, dep_rank=dep_rank):
                ledger = ProvenanceLedger()
                leaf = _leaf("leaf")
                ledger._register(leaf.id, dep_rank, dependency_ids=())  # exact dependency rank under test
                rule = InteractionRule(
                    id="rule", description="rule", dependency_ids=(leaf.id,), provenance=rule_rank
                )
                ledger.register_interaction_rule(rule)
                emergent = _emergent("emergent", [leaf.id], rule.id)
                computed = ledger.register_emergent_property(emergent, rule)
                self.assertEqual(computed, min(rule_rank, dep_rank))


class TestMultiHopPropagation(unittest.TestCase):
    def test_spec_worked_example_A_plus_B_plus_interaction1_to_C_then_C_plus_D_to_E(self):
        # INV-06's own worked example, literally: C depends on A and B; E
        # later depends on C and D. C's inherited provenance must
        # participate in E's computation without being re-derived.
        ledger = ProvenanceLedger()
        a = _leaf("A")
        b = _leaf("B")  # both SOURCE_DERIVED leaves
        ledger.register_source_property(a)
        ledger.register_source_property(b)

        interaction1 = InteractionRule(
            id="interaction1",
            description="A + B interact",
            dependency_ids=(a.id, b.id),
            provenance=Provenance.INVENTED_BRIDGE,  # weaker than either leaf
        )
        ledger.register_interaction_rule(interaction1)
        c = _emergent("C", [a.id, b.id], interaction1.id)
        c_provenance = ledger.register_emergent_property(c, interaction1)
        self.assertEqual(c_provenance, Provenance.INVENTED_BRIDGE)

        d = _leaf("D")
        ledger.register_source_property(d)

        interaction2 = InteractionRule(
            id="interaction2",
            description="C + D interact",
            dependency_ids=(c.id, d.id),
            provenance=Provenance.SOURCE_DERIVED,  # strong rule, weak ancestor
        )
        ledger.register_interaction_rule(interaction2)
        e = _emergent("E", [c.id, d.id], interaction2.id)
        e_provenance = ledger.register_emergent_property(e, interaction2)

        # E's weakest link must reflect C's already-weaker inherited
        # provenance, not just interaction2's own strong rating.
        self.assertEqual(e_provenance, Provenance.INVENTED_BRIDGE)


class TestUnresolvedDependencyPropagation(unittest.TestCase):
    def test_unresolved_dependency_forces_descendant_unresolved(self):
        # INV-07: an Unresolved required dependency forces the descendant
        # Unresolved, even if the governing rule itself is strong.
        ledger = ProvenanceLedger()
        leaf = _leaf("leaf")
        ledger._register(leaf.id, Provenance.UNRESOLVED, dependency_ids=())
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(leaf.id,), provenance=Provenance.SOURCE_DERIVED
        )
        ledger.register_interaction_rule(rule)
        emergent = _emergent("emergent", [leaf.id], rule.id)
        computed = ledger.register_emergent_property(emergent, rule)
        self.assertEqual(computed, Provenance.UNRESOLVED)


class TestInventedAncestryVisibility(unittest.TestCase):
    def test_invented_ancestor_remains_visible_through_a_later_hop(self):
        # INV-08: invented ancestry may become indirect; it may not disappear.
        ledger = ProvenanceLedger()
        a = _leaf("A")
        ledger.register_source_property(a)

        invented_rule = InteractionRule(
            id="invented_rule",
            description="an invented bridge",
            dependency_ids=(a.id,),
            provenance=Provenance.INVENTED_BRIDGE,
        )
        ledger.register_interaction_rule(invented_rule)
        c = _emergent("C", [a.id], invented_rule.id)
        ledger.register_emergent_property(c, invented_rule)

        d = _leaf("D")
        ledger.register_source_property(d)
        later_rule = InteractionRule(
            id="later_rule",
            description="a later, source-derived rule",
            dependency_ids=(c.id, d.id),
            provenance=Provenance.SOURCE_DERIVED,
        )
        ledger.register_interaction_rule(later_rule)
        e = _emergent("E", [c.id, d.id], later_rule.id)
        ledger.register_emergent_property(e, later_rule)

        # invented_rule is two hops back from E, but must still be visible.
        self.assertIn(invented_rule.id, ledger.invented_ancestors(e.id))
        self.assertIn(invented_rule.id, ledger.get_ancestry(e.id))


class TestCyclesAreStructurallyImpossible(unittest.TestCase):
    """Every registration method requires all referenced ids to already be
    registered before the new id is accepted, and no id may be registered
    twice. Together these two facts mean a genuine cycle can never be
    constructed: whichever node of a would-be cycle is registered second
    fails its own dependency check, because the first node's edge back to it
    cannot yet exist. These tests verify that explicitly rather than leaving
    it as an inference from reading the code.
    """

    def test_interaction_rule_cannot_depend_on_its_own_id(self):
        ledger = ProvenanceLedger()
        rule = InteractionRule(
            id="self_loop", description="depends on itself", dependency_ids=("self_loop",),
            provenance=Provenance.DEFENSIBLY_DERIVED,
        )
        with self.assertRaises(ProvenanceLedgerError):
            ledger.register_interaction_rule(rule)
        # And the failed attempt must not have partially registered anything.
        with self.assertRaises(ProvenanceLedgerError):
            ledger.get("self_loop")

    def test_emergent_property_cannot_depend_on_its_own_id(self):
        ledger = ProvenanceLedger()
        a = _leaf("A")
        ledger.register_source_property(a)
        rule = InteractionRule(
            id="rule", description="rule", dependency_ids=(a.id,), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        ledger.register_interaction_rule(rule)
        # emergent.id appears among its own direct_ancestor_ids.
        emergent = _emergent("emergent", [a.id, "emergent"], rule.id)
        with self.assertRaises(ProvenanceLedgerError):
            ledger.register_emergent_property(emergent, rule)

    def test_a_two_node_cycle_cannot_be_constructed(self):
        # To register A->B and B->A, one of the two edges must be registered
        # first. Whichever is first names a target that cannot yet exist, so
        # the attempt fails before the second edge could ever be added —
        # there is no ordering that lets both registrations succeed.
        ledger = ProvenanceLedger()
        rule_a_depends_on_b = InteractionRule(
            id="A", description="A depends on B", dependency_ids=("B",), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        with self.assertRaises(ProvenanceLedgerError):
            ledger.register_interaction_rule(rule_a_depends_on_b)

        # Symmetric check, fresh ledger: B depends on A first instead.
        ledger2 = ProvenanceLedger()
        rule_b_depends_on_a = InteractionRule(
            id="B", description="B depends on A", dependency_ids=("A",), provenance=Provenance.DEFENSIBLY_DERIVED
        )
        with self.assertRaises(ProvenanceLedgerError):
            ledger2.register_interaction_rule(rule_b_depends_on_a)


if __name__ == "__main__":
    unittest.main()
