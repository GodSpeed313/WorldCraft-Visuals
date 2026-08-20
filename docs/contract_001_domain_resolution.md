# WorldCraft Contract 001 — Domain Resolution

**Type:** Resolution contract. Defines states, transitions, terminal outcomes, and invariants.
**It is not an ontology document and not an implementation plan.**

**Status:** DRAFT — pending operator review and sign-off.

**Why it exists.** Rulings 001 and 002 introduced four separate state vocabularies across two
documents written in response to different questions — proposal outcomes, family outcomes, grounding
outcomes, and fusion result states. Ruling 002 §8.1 already needed a three-column table to reconcile
them. This contract consolidates what has been decided into one coherent state model, **before**
implementation, so that code does not become the place the remaining ontology decisions get made by
accident.

**Sequencing intent.** The contract is deliberately written while the taxonomy is unfinished. If it
can only be completed after the domains are named, it has failed its own purpose.

---

## 1. Scope boundary

**This contract defines only:**

- resolution states
- allowed transitions
- terminal outcomes
- invariants

**It does not define:**

| Excluded | Belongs to |
|---|---|
| domain names | lore — operator |
| domain count | lore — operator, informed by `audit_001` |
| provider choice | Ruling 001 §5 |
| prompts | unassigned — see GAP-7 |
| model usage | coupled to GAP-6 — no independent owner; resolves only if the document that claims caching/storage ownership also addresses model usage, not on GAP-6's closure alone |
| caching, storage strategy | unassigned — tracked as GAP-6 |
| registry expansion rules | Ruling 002 §3, §8 |

Anything from the left-hand column — a topic this contract has excluded — appearing as a normative
condition anywhere in this contract is a defect in this contract.

## 2. Contract validity constraints

**These are not features of the contract. They are conditions the contract must satisfy to be
valid.** The distinction matters: treated as features they become negotiable, and this document
becomes the place hidden assumptions creep back in.

**Scope.** V1 and V2 are conditions on the whole of this contract, §1 through §8. A signature on
either constraint attests that the document satisfies that condition as of that signature.

**Scoped term.** In this contract, *domain candidate* means a domain that is a defensible placement
for the concept currently being resolved. It is distinct from *candidate domain* as used in
`audit_001` Part 3 Q4 and Ruling 002 §10.1 — a cluster proposed for adoption into the taxonomy — and
from *grounding candidate* (§5, I4), a substitution target for a power. This contract uses the term
in the first sense only. Defensibility is evidence-relative: a placement stops qualifying as a domain candidate once current evidence justifies selecting a competing placement over it. A domain candidate need not be a registered domain.

### V1 — Cardinality independence

> **A valid domain resolution contract must produce identical state semantics regardless of the
> number of registered domains.**

The contract must behave identically at:

```
domain count: 1        domain count: 5        domain count: 20
```

At every count it must still distinguish:

- a domain candidate exists
- multiple domain candidates exist
- no domain candidate exists

**Invalid, and the canonical example of the failure:**

```
if supernatural domain exists:
    ...
else:
    ...
```

That is no longer resolution logic. **That is taxonomy.**

**Conformance check.** Substitute the domain set with any other domain set, of any size, including a
set of one. If any state definition, transition, or terminal condition changes, V1 is violated. No
state, transition, or terminal condition in this contract may contain a predicate that names a
specific domain.

**The contract must be able to run before the ontology is finalized.**

### V2 — Epistemic distinction preservation

The contract must at all times distinguish three knowledge conditions, and must never allow one to
be reported as another:

| The system must be able to say | State |
|---|---|
| *"I don't know what this is."* | `UNRESOLVED_DOMAIN` |
| *"I know what this could be, but not which interpretation wins."* | `AMBIGUOUS_DOMAIN` |
| *"I have enough evidence to continue."* | `RESOLVED_DOMAIN` |

**Those are three different realities.** Collapsing any pair destroys the operator's ability to know
what action is required. No case may be reported as one of these three unless it satisfies that
condition's stated definition. Where no condition's definition is satisfied, the case may not be
assigned to any of the three.

## 3. Domain resolution states

### 3.1 `UNRESOLVED_DOMAIN`

**Meaning:** the system cannot currently establish a domain candidate.

```
Unknown ability
      ↓
No matching domain evidence
      ↓
UNRESOLVED_DOMAIN
```

**Operator implication:** gather more evidence · enrich vocabulary · **do not ground**.

### 3.2 `AMBIGUOUS_DOMAIN`

**Meaning:** multiple domain candidates are defensible, and current evidence does not justify
selecting one.

```
Cursed Energy
      ↓
Domain candidate A
Domain candidate B
      ↓
AMBIGUOUS_DOMAIN
```

**Operator implication:** preserve alternatives · **do not collapse identity** · await additional
criteria.

**Ambiguity is not failure. It is a valid epistemic state.** A concept in this state is fully
understood; what is undetermined is which of several legitimate placements is correct. Forcing the
choice would be an unsupported assertion, not a resolution.

The contract does not decide *how* ambiguity is later discharged. A future ruling may introduce a
second criterion beyond thematic similarity — fusion locality, i.e. *which placement minimizes
cross-domain leakage* — but that requires more registry evidence and is out of scope here.

### 3.3 `RESOLVED_DOMAIN`

**Meaning:** exactly one domain candidate is defensible.

**This is the only state that proceeds into family resolution.**

## 4. Transition graph

```
                 ┌─────────────────┐
                 │  Input Concept  │
                 └────────┬────────┘
                          │
                          v
                 ┌─────────────────┐
                 │  Domain Resolve │
                 └────────┬────────┘
                          │
          ┌───────────────┼────────────────┐
          v               v                v
 UNRESOLVED_DOMAIN  AMBIGUOUS_DOMAIN  RESOLVED_DOMAIN
          │               │                │
          │               │                v
          │               │       Family Resolution
          │               │                │
          │               │                v
          │               │      Grounding Resolution
          │               │
          └───────────────┴──────────────>
             terminal / evidence required
```

**Two branches terminate without proceeding.** Neither is an error path; both are states that
require evidence the system does not have. Only `RESOLVED_DOMAIN` continues, per Ruling 002
Addendum A: *family is only meaningful inside a domain.*

## 5. Downstream states — consolidated

The stages below are already ruled; they are collected here so the full pipeline exists in one place.

| Stage | States | Source |
|---|---|---|
| Domain resolution | `UNRESOLVED_DOMAIN` · `AMBIGUOUS_DOMAIN` · `RESOLVED_DOMAIN` | this contract §3 |
| Family resolution | `UNRESOLVED_FAMILY` · resolved | Ruling 002 §2, §8 |
| Grounding resolution | grounded candidate · `GROUNDING_UNAVAILABLE` · grounding not required | Ruling 002 §5.2, §5.3 |
| Fusion result | `ADMITTED` · `SURFACED` · `CAUTIONARY` · `BLOCKED` | Ruling 001 §4 |

### 5.1 Terminal mapping

| Terminal condition | Fusion result | Operator action |
|---|---|---|
| Concept could not be identified at all | `BLOCKED` | resolve the name |
| `UNRESOLVED_DOMAIN` | `CAUTIONARY` | gather evidence / enrich vocabulary |
| `AMBIGUOUS_DOMAIN` | `CAUTIONARY` | preserve alternatives, await criteria |
| `UNRESOLVED_FAMILY` | `CAUTIONARY` | extend the taxonomy |
| `GROUNDING_UNAVAILABLE` | `SURFACED` — accepted and rejected components both reported, with reason | none required; a valid ontology state, terminal |
| All stages resolved | `ADMITTED` | none |

**Critical property: the fusion result states are lossy.** Three distinct terminal conditions map onto
`CAUTIONARY`, and each calls for a *different* operator action. **The reason must therefore travel
with the result and may never be discarded on the way out** — this is Ruling 002 §5.3 applied to the
whole pipeline rather than to grounding alone. A `CAUTIONARY` without its reason is indistinguishable
from the silent-default failure both rulings exist to eliminate.

## 6. Invariants

**I1 — Cardinality independence.** §V1. No predicate may name a specific domain.

**I2 — Resolution order is fixed.** Domain → family → grounding. Ruling 002 Addendum A.

**I3 — Ambiguity is preserved, never collapsed.** A concept with multiple domain candidates stays
in `AMBIGUOUS_DOMAIN` until evidence discharges it. Selecting arbitrarily is prohibited.

**I4 — No cross-domain substitution.** No transition may produce a grounding candidate outside the
concept's domain. Ruling 002 §5.2.

**I5 — No silent terminal.** Every terminal state carries its reason to the output. Ruling 001
Invariant 1, Ruling 002 §5.3.

**I6 — Unknown is not false. Uncertain is not resolved.** The two principles that have emerged across
001, 002 and this contract, stated as one invariant because they fail together: both are violated by
the same move — treating an absence of evidence as a determination.

**I7 — `SURFACED` is terminal.** A `SURFACED` result is not a degraded `ADMITTED` result and may not
be auto-resolved through taxonomy expansion. Ruling 001 §4, Ruling 002 §5.2, §5.4.

## 7. The conservative principle at three levels

This contract is the third application of one idea, and recording the pattern is worth more than any
single rule:

| Level | Ruling | The rule | What is preserved |
|---|---|---|---|
| Concept identity | 001 §1 | minting is cheap, merging is expensive | distinctions between concepts |
| Category integrity | 002 §3 | family threshold higher than power threshold | the meaning of a category |
| Epistemic state | this contract, I3 | ambiguity is preserved, never collapsed | the honest description of what is known |

In each case the system is permitted to be *incomplete* but never permitted to be *falsely certain*.

## 8. Future extensibility

> **This contract must permit additional resolution states without invalidating existing states,
> provided new states preserve the distinction between unknown, ambiguous, and resolved knowledge
> conditions.**

Not because further states are expected immediately, but because **the entire purpose of this layer
is preventing forced classification.** A contract that could not itself be extended without a
rewrite would reproduce, at the level of the state machine, exactly the closed-world assumption
Ruling 002 §1.1 identifies as the thing WorldCraft is leaving behind.

---

## Sign-off checklist

- [x] §1 Scope boundary — states/transitions/terminals/invariants only — signed 2026-08-16, after the bundled provider row was split three ways (`2dac6ff`). Every destination in the exclusion table was verified to own what it is sent, or to name a register entry recording that no document does: `audit_001` Part 3 Q4 (`:181`) informs domain count and deliberately refuses a number; Ruling 001 §5 owns *provider choice* under its 2026-08-06 scope amendment (`:273`); Ruling 002 §3 and §8 own *registry expansion rules* substantively — §3 the family admission threshold, §8 the registry entry condition. *prompts* routes to GAP-7 and *caching, storage strategy* to GAP-6, each recording that no document claims the topic; *model usage* is coupled to GAP-6 without merging into it, carrying the register's stricter semantics — closure on caching/storage alone does not resolve it. The self-test sentence was corrected to name the **left-hand** column, an excluded topic appearing as a **normative** condition, so that observational citation is not caught; the corrected test was then run against this document and returns nothing. **Not attested by this signature:** whether §1's "defines only" list reaches §8, which states a normative requirement on the contract without the reconciling clause §2 carries for itself — that belongs to §8's signature; §7's observational citation of Ruling 002 §3 is recorded on §7's own line and not adjudicated here. Correcting §1's self-test removed the stated authority GAP-6's derivation rested on; that derivation is preserved and marked historical in the register rather than restated as current. No gap is closed and no invariant is added.
- [x] §2 V1 cardinality independence, with conformance check — signed 2026-08-19. The conformance check at `:87-90` was run against the whole document by extraction rather than spot-check: every domain name appearing in the registry (`audit_001`) was searched against this file, and the only occurrence in any position is `:79`, inside the fence opened at `:76` as the labeled *"Invalid, and the canonical example of the failure"* — a counter-example, not a live predicate. No state definition, transition, or terminal condition contains a predicate naming a specific domain. The substitution test holds at any domain count, including a set of one, because §3's state definitions reference *domain candidate* in `:57`'s scoped sense, whose closing clause decouples candidacy from registration; `474f16e` normalized `:114`, `:128`, `:153` and I3 `:221` onto that one term, so the test now runs against a single term rather than four. Recorded as passing rather than omitted: `:132`'s *Cursed Energy* is a concept name inside §3.2's illustrative diagram, not a domain name, and V1's rule reaches predicates that name a specific **domain**; that diagram's outputs are lettered `Domain candidate A`/`B` precisely so no domain is named. **Not attested by this signature:** `:114`'s undefined *valid*, placed on the record by `474f16e` and routed to §3's signature; and the I1/`:217` attestation-boundary question, which is outside the corpus by its own terms. No gap is closed and no invariant is added.
- [x] §2 V2 epistemic distinction preservation — signed 2026-08-19, as to mutual exclusivity and non-misreporting only. §3.1-3.3's three states are mutually exclusive on their stated definitions: `:114` is the zero case, its diagram at `:118` reading *No matching domain evidence*; `:128` requires *multiple*; `:153` requires *one* with *sufficient support*. `:106-108` forbids reporting a case as one of the three unless it satisfies that condition's stated definition, which is what V2's *never allow one to be reported as another* requires. §5.1's mapping of both `UNRESOLVED_DOMAIN` and `AMBIGUOUS_DOMAIN` onto a single `CAUTIONARY` does not violate V2: that collapse is at the fusion-result layer, not the knowledge-condition layer, and `:210-211` together with I5 (`:227`) hold the originating reason to the output, so no condition is reported as another. **Not attested by this signature — exhaustiveness.** A single domain candidate with insufficient support satisfies none of the three definitions: not zero, not multiple, not sufficient. `:106-108` leaves such a case unassigned and names no fourth state; it forbids papering the case over without giving it a destination. Whether that is a live gap or no gap at all depends on the reading of `:114`'s *valid* — if *valid* means *has sufficient support*, §3.1 absorbs the case and the set is exhaustive; if it means *well-formed*, the case has no home. That word is excluded from this signature and routed to §3's, and the exhaustiveness question is routed with it. *sufficient support* occurs once in this document (`:153`) and is not defined. **Also not attested:** the I1/`:217` attestation-boundary question, outside the corpus by its own terms. No gap is closed and no invariant is added.
- [ ] §3 Three domain states, with operator implications
- [ ] §4 Transition graph — two terminal branches, one continuing
- [ ] §5 Consolidated pipeline + four-state fusion result + terminal mapping; reasons are lossless
- [ ] §6 Invariants I1–I7
- [ ] §7 The conservative principle at three levels — cites Ruling 002 §3's threshold observationally to build the cross-ruling pattern; does not assert ownership or restate it as a binding condition of this contract.
- [ ] §8 Future extensibility clause

Drafted 2026-08-04. Not binding until signed off and marked LOCKED.
