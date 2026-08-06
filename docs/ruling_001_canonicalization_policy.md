# WorldCraft Ruling 001 — Concept Canonicalization Policy

**Status:** **LOCKED** — all sections signed off by the operator, 2026-08-06. Binding.

Amendments recorded inline are part of what was signed and carry the same authority as the original
text. Changing a signed section requires a new operator ruling, recorded in that section the way the
2026-08-06 amendments are.

**Authority:** This is the first WorldCraft ruling. It governs how unknown concepts enter the
system, when two concepts may be treated as one, and what the resolver is permitted to decide.
It is spec-first: no implementation precedes sign-off.

**Why it exists.** WorldCraft is being redirected from a finite hand-authored registry to a
*governed reality synthesis engine* over an unbounded input space. Once concepts can be learned,
the knowledge graph's trustworthiness becomes the load-bearing property of the whole system — and
canonicalization is the one operation that can corrupt it permanently. This ruling is therefore
foundational to, and precedes, the resolver's engineering design.

---

## 1. Core principle

> **Minting is cheap. Merging is expensive.**

A new concept may be redundant. A destructive merge is permanent contamination.

- Low confidence → **preserve the distinction**
- High confidence → **canonicalize**
- **Never merge on name similarity alone**

**The system prefers a slightly noisy ontology over a falsely unified one.** A duplicate is
recoverable by a later merge. A false identity is inherited by every fusion built on top of it and
is hidden behind the cache, which makes it invisible precisely where it does the most damage.

## 2. The three invariants

These are binding on every component and may not be traded away for convenience.

**Invariant 1 — No silent grounding.**
Unknown concepts never inherit a reality classification. Defaulting an unrecognized input to
GROUNDED is not a harmless fallback; it manufactures false certainty.

**Invariant 2 — Merge conservatively.**
A duplicate is recoverable. A false identity is structural corruption.

**Invariant 3 — Learned vocabulary is constrained vocabulary.**
The model may propose `name`, `family`, `modality`, `cost_factor`. **It may not invent mechanics.**

**Amendment — operator ruling, 2026-08-06.** "Mechanics," for the purposes of this invariant, means
any behavior, rule, or effect that is not derivable from the four permitted fields (name, family,
modality, cost_factor) by lookup against the existing engine logic. A proposal violates this
invariant if content within an allowed field requires interpretation by the validator rather than
resolution by lookup — e.g. a name that encodes a mechanical effect, or a family value that
functions as an ad hoc rule rather than a reference to an existing or properly-proposed taxonomic
category.

## 3. Canonicalization policy

### 3.1 Default posture: conservative

Worked example, as ruled:

```
Mokuton                          <- canonical identity
├── aliases:
│   ├── Wood Release
│   ├── Wood Style
│   └── Wood Element
└── grounding candidate:
    └── requires taxonomy validation
```

The example demonstrates canonical identity and alias handling only. **The family assignment is
intentionally omitted**, because family membership is governed by Ruling 002 and must not be
inferred from descriptive similarity.

**`Divine Tree Manipulation` does NOT automatically merge into Mokuton.** It may be a technique
derived from Mokuton, a related but separate ability, a higher-order transformation, or an ability
specific to an artifact or system. Absent evidence distinguishing these, the graph **preserves
lineage before identity**.

### 3.2 Merge requirements — all three are required

A merge requires agreement across multiple dimensions. Any one of these failing means the concepts
stay separate.

**(a) Semantic identity.** The question is *"are these actually the same phenomenon?"* — **not**
*"do they produce similar effects?"* Similarity of effect is insufficient and is never grounds for
a merge on its own.

**(b) Source consensus.** Multiple independent sources treat the terms as interchangeable.

- Qualifying: *"Mokuton, also called Wood Release…"* — the sources equate the terms.
- Not qualifying: *"This character has plant powers similar to Wood Release."* — the source draws
  a comparison, not an identity.

**(c) Mechanical equivalence.** The registry classification must match on `min_modality`, `family`,
and `cost_factor`. **If the classification differs, the concepts stay separate until the
discrepancy is itself resolved.** A classification disagreement is evidence that the two concepts
are not the same phenomenon, and it is treated as such rather than averaged away.

**Amendment — operator ruling, 2026-08-06.** For **operator-authored concepts**, operator
declaration satisfies (b). A concept is operator-authored when its canonical identity, and the lore
establishing it, originate with the operator rather than with a model proposal or an external
source. Requirements **(a) semantic identity and (c) mechanical equivalence are unchanged** and
remain binding on operator-authored and learned concepts alike. Source consensus continues to apply
in full to learned concepts, for which the operator is not a source.

**The operator is providing authoritative source consensus, not a merge override.** The exemption
supplies what (b) asks for; it does not excuse a merge from (a) or (c). A merge that fails semantic
identity or mechanical equivalence remains rejected regardless of who declares it.

**Why the amendment exists.** As originally drafted, (b) was unsatisfiable for anything the operator
authors: original lore has exactly one source. Because all three requirements are required, the
merge path was structurally unreachable for the operator's own corpus — a branch that could never
fire, the same finding shape as Audit 001 (M1). The amendment opens that path without weakening the
test for learned vocabulary, where the risk (b) guards against actually lives.

### 3.3 Alias is not merge — the load-bearing architectural separation

The graph distinguishes four relationship kinds. Collapsing them into "everything similar is the
same thing" is the failure this ruling exists to prevent.

```
Concept
├── canonical identity
├── aliases            — different names, same phenomenon
├── derivatives        — descended from it, not identical to it
└── related concepts   — adjacent, distinct
```

Worked example:

```
Mokuton
├── Divine Tree Manipulation   (derived)
├── Plant Control              (related)
└── Wood Clone Technique       (application)
```

**Fusion depends on these relationships.** An engine that knows Wood Clone Technique is an
*application* of Mokuton can reason about it; an engine that has flattened them into one entry has
destroyed the information the fusion needed. Preserving the graph is not bookkeeping — it is
capability.

### 3.4 Reversibility

Because canonicalization is permanent in a way individual profiles are not, merges are recorded as
**reversible, reviewable operations tracked separately from per-profile provenance.** A bad profile
is re-resolved on its own; a bad merge must be undoable without re-resolving everything downstream
of it.

## 4. Resolution states — unknown inputs

**Ruling: resolve-then-proceed, never silently default.**

The current behavior — `unknown → GROUNDED → continue` — is the exact defect that produced the
Hashirama × William artifact (§6). It is not a fallback; it is false certainty.

```
Input
  │
  ▼
Recognized?
  ├── yes ──────────────► validate ──► continue
  └── no
        │
        ▼
   normalization request
        ├── resolved ────► validate ──► continue
        └── unresolved ──► blocked
```

**The application does not hard-fail.** WorldCraft is a creative engine and exploration matters.
Results therefore carry one of four states:

| State | Output | Meaning |
|---|---|---|
| **ADMITTED** | emitted — complete | Concept recognized or resolved and validated, and every component grounded. Fusion proceeds normally. |
| **SURFACED** | emitted — deliberately incomplete | Some components are grounded; others are rejected because no in-domain grounding candidate exists. Accepted and rejected components are both reported, each rejection carrying its reason. Terminal. Ruling 002 §5.3. |
| **CAUTIONARY** | none — pending | Concept requires normalization. The idea may be inspected, but **no fusion output is generated until validation.** The engine never pretends the concept is grounded. |
| **BLOCKED** | none — refused | Resolution failed or validation rejected the proposal. No output. |

**`SURFACED` is not a degraded `ADMITTED` state.** It does not describe a fusion that almost
succeeded, and it is not awaiting anything. It represents a **compatibility boundary, not incomplete
validation**, and it cannot be resolved by expanding the taxonomy — doing so would require inventing
precisely the *artificial bridge concepts whose only purpose is being a fallback* that Ruling 002
§5.4 rejects.

The contrast with `UNRESOLVED_FAMILY` — a vocabulary gap, where extending the taxonomy *is* the
correct operator action — is governed by Ruling 002 §2 and §8.

Worked examples:

**`Hashirama Senju` → `Wood Release`.** The state depends on the fusion context, and this example is
written to expose that variable rather than hide it.

| Stage | Result |
|---|---|
| Standalone resolution | Known power → `Wood Release`. No unsupported substitution occurs. |
| Fusion A — against a compatible HIGH_CONCEPT domain | grounding legal or unnecessary → **ADMITTED** |
| Fusion B — against a domain where grounding would require a bridge that does not exist | `GROUNDING_UNAVAILABLE` → **SURFACED** |

**Resolution alone does not determine the state.** Under the pre-domain model this example read
*known power → family assignment → fusion accepted*, treating the family label as sufficient. It is
not. Per Ruling 002 Addendum A the order is domain → family → grounding, and the fusion's own
compatibility decides the terminal state. Fusion B is Regression Case 001's corrected path (§6).

- `Shadow Dragon Reality Collapse` (original character) → unknown → **CAUTIONARY**: *"Power concept
  requires normalization."* Inspectable; no fusion output.

**Operator acceptance recorded 2026-08-06 — a record of what was accepted, not an amendment to this
section.** Signing §4 accepts a known cost explicitly. `CAUTIONARY` and `BLOCKED` both emit nothing,
and combined with Invariant 1's prohibition on silent grounding, the engine will frequently return a
reason where it previously returned a guess. **That tradeoff is intentional and is preferred over
false certainty**, and it is expected to read as a regression in the dashboard until the resolver
exists. A future reader encountering empty results should treat them as the ruling working, not
failing.

## 5. The provider boundary

**Model calls are acceptable. The model is not the authority.**

```
LLM ──► Proposal ──► WorldCraft validator ──► Registry
```

The model proposes a classification:

```
name:      Wood Release
family:    <proposed — validated against Ruling 002 §8>
modality:     HIGH_CONCEPT
cost_factor:  8
```

**The engine decides whether that enters reality.** The validator determines whether the proposed
family exists and whether the classification is admissible under the current taxonomy; a family that
does not exist is rejected as `UNRESOLVED_FAMILY`, never coerced. This is the Continuum separation
restated: what generates is never what validates. The LLM is the historian; WorldCraft is the
scientist.

**Scope of this section — operator ruling, 2026-08-06.** §5 owns the **provider authority boundary**
and **taxonomy existence validation** only. The content-interpretation validation required by
Invariant 3 as amended — determining whether content within an allowed field requires interpretation
rather than resolution by lookup — is **not** governed here. It is owned by Contract 001 as a
separate invariant alongside I7, and is tracked as GAP-1 in `docs/open_contract_gaps.md` until that
invariant exists. The validator described in this section is therefore **not the whole validator**,
and no reader may treat §5 as an exhaustive account of what validation performs.

**Cost.** Acceptable. The model is classifying unknown concepts, not generating worlds — a narrow
enough task that 2–3 calls per novel concept is reasonable, and the result is cached permanently.

**Dependencies.** Initial implementation remains stdlib-only. Future external dependencies require
documented justification, explicit scope, and review before adoption — triggered when a resolver
capability cannot be implemented without one.

The moment WorldCraft acquires a dependency stack it loses one of its strongest properties — *anyone
can run the engine anywhere*. A thin transport layer is sufficient:

```
worldcraft/
└── resolver/
    ├── provider.py     — interface
    ├── anthropic.py    — one implementation
    └── cache.py        — resolved-concept memory
```

The repository is currently flat. Adopting this layout is an **implementation follow-up, not a
ruling blocker** (operator ruling, 2026-08-06): it requires becoming a package and touches imports,
CI, and the test module, none of which affects whether this section is true.

**The core engine must know nothing about Anthropic.** The provider is swappable and the engine's
correctness must not depend on which one is installed, or on one being installed at all.

## 6. Normalization Regression Case 001 — preserved permanently

`containment_matrix.json` currently holds exactly one fusion: **Hashirama Senju × William
Vangeance**, both silently defaulted to GROUNDED with `tags: ["unknown"]`, producing
`Espionage / One-Inch Punch / Psychological Mastery` — two nature-magic leaders rendered as spies.

**The primary exhibit is the artifact's own lore text.** The engine recorded that it did not know
what either input was, and generated a complete profile anyway:

```
"lore_summary": "Born from the tension between the Unknown Entity (Neutral)
                 and the Unknown Entity (Neutral), this fusion haunts
                 Cold War Safehouse with singular intent"
```

Both inputs are named `Unknown Entity (Neutral)` — the same placeholder, twice. **This is not a
system that failed to notice its own ignorance. It wrote the ignorance down and proceeded**, emitting
a signature ability, a dominant family, and a biome on that basis. That is Invariant 1's violation
stated in the engine's own words, and it forecloses any reading in which the engine merely guessed
badly.

**The false certainty propagated into downstream fields.** `biome: "Cold War Safehouse"` is where the
espionage framing entered: the spy reading is not a consequence of power selection alone but of a
setting derived from inputs the engine had already recorded as unknown. **A defaulted classification
does not stay where it was defaulted.**

Secondary observation, recorded as fact and not analysed here: the artifact also carries
`dominant_family: "PERCEPTION"`, the field governed by Ruling 002 §7.

**This artifact is retained permanently as the first Normalization Regression Case**, not as a bug
record but as the demonstration of why the layer exists:

```
Before:  Unknown → GROUNDED → espionage punch
After:   Unknown → resolve → Wood Release detected → false classification rejected
```

It is the birth certificate of the normalization layer, and any future change that would let the
"before" path run again must fail against it.

**The artifact exposes two independent failures, and they must stay separate in the record:**

| # | Failure | Class | Governed by |
|---|---|---|---|
| 1 | Unknown character/power silently became GROUNDED | **normalization bug** | this ruling — Invariant 1 |
| 2 | The registry has no honest place for non-human-excellence abilities | **ontology boundary** | Ruling 002 |

Fixing the first does not fix the second. With normalization alone, Hashirama resolves correctly to
Wood Release and then has nowhere legal to land. The system must be able to distinguish *"we do not
know this thing yet"* from *"our categories are not large enough for this thing"* — the operator
action each calls for is completely different.

## 7. Open questions carried forward — NOT resolved by this ruling

**7.1 — FAMILY CLASSIFICATION EXAMPLES. SUPERSEDED BY RULING 002.**

This ruling originally used descriptive families as examples — a `Nature` / `Nature Transformation`
family that does not exist, where `POWER_FAMILIES` is exactly `COGNITION`, `INFLUENCE`, `DISCIPLINE`,
`PERCEPTION`. Those examples were not taxonomy assignments and have been removed from §3.1 and §5.

**Family membership, grounding behavior, and unresolved-family handling are governed exclusively by
`docs/ruling_002_family_taxonomy_integrity.md`.** This ruling owns concept identity, aliasing and
merges, the provider boundary, normalization, and the resolution states. It does not own family
decisions, and nothing in it may be read as making one.

**7.2 — `cost_factor` exact-match as a merge criterion.** §3.2(c) requires `cost_factor` to match
for a merge. As an integer, this makes an otherwise-identical pair with costs 8 and 9 permanently
unmergeable. This is arguably correct under Invariant 2 (conservative is the point), but it should be
a deliberate choice rather than an artifact of the field's type.

**7.3 — Modality's role polymorphism.** Modality generalizes across input types as *how far
consensus reality must bend*, but plays three different logical roles: **ceiling** for a character
(what it may hold), **ambient law** for a place (what may happen there), **requirement** for an
ability (what world it needs). The existing grounding filter already implements the ability-inside-a
-place case.

**Ownership — operator ruling, 2026-08-06: this question is owned by Ruling 001.** An earlier draft
of this entry assigned formalization to Ruling 002. Ruling 002 neither formalizes modality's role
polymorphism nor carries it as an open question, so the handoff was never received. Assigning
content to that document while its own review is incomplete would mean deciding its contents from
outside it. The question remains open and stays here.

**7.4 — Component eligibility semantics.** §4's `SURFACED` definition is deliberately
component-neutral: *some components are grounded; others are rejected.* It does not distinguish
components that participate in grounding eligibility from those that do not, because no such
component ontology exists yet. Once it does, it must define whether a rejected non-participating
component (metadata, flavor, a non-essential modifier) can move a fusion out of `ADMITTED` — it
should not. Deferred deliberately: gating a state on a `required` predicate today would make the
state machine depend on an undefined component model.

**7.5 — Merge-review counterweight.** §1's conservatism has no alarm attached to it. A merge that
should have happened and did not produces no event, no warning, and no artifact; the symptom is
absence, and a graph can fragment slowly without anything marking the moment it began. §3.4's
reversibility makes a periodic review pass over near-miss merge candidates safe to run, but nothing
in this ruling requires one and no criteria exist for what qualifies as a near-miss. Scoped as open
by operator ruling on 2026-08-06, taken at the same time §1 was signed off: the counterweight is a
separate future decision and **does not gate §1**.

**7.6 — Mechanic authorship.** Open question regarding whether mechanics are operator-authored
canon, generated proposals requiring validation, or another category. Invariant 3 as amended
establishes that the model may not author them; it does not establish who may. Evidence: the
operator-authored character corpus contains mechanics with no equivalent anywhere in the engine —
`Audit 002 (C2)` records three structurally distinct resource mechanics across three cards.

**7.7 — Entity relationships.** Open question regarding representation of relationships between
entities (for example, sibling relationships) distinct from concept identity relationships. §3.3
defines a relationship graph for **concepts** — canonical, aliases, derivatives, related. No
equivalent exists for **entities**. Evidence: `Audit 002 (C4)` records an ability whose effect is
defined relative to another named entity, where the relationship is derivable from neither
identifier and exists only as an explicit fact.

---

## Sign-off checklist

- [x] §1 Core principle — minting cheap, merging expensive
- [x] §2 The three invariants — 1 and 2 as written; 3 signed with the 2026-08-06 amendment defining "mechanics" as lookup-derivable, not validator-interpreted
- [x] §3 Canonicalization policy — 3.1 and 3.3 as written; 3.2 signed with the 2026-08-06 amendment (operator declaration satisfies (b) for operator-authored concepts only; (a) and (c) unchanged); 3.4 accepted as written with enforcement deferred to Contract 001
- [x] §4 Resolution states — ADMITTED / SURFACED / CAUTIONARY / BLOCKED, no hard-fail; SURFACED is terminal and is not a degraded ADMITTED — signed as written; no-output tradeoff accepted explicitly; §7.4 component neutrality affirmed as a deferred gap, not to be resolved by inventing a component model
- [x] §5 Provider boundary — model proposes, engine decides; core knows nothing about Anthropic — signed 2026-08-06 with: scope limited to provider authority + taxonomy existence validation (content-interpretation owned by Contract 001, GAP-1 Option 2); dependency-governance condition replacing "stdlib only, initially"; `cost` → `cost_factor`; package layout recorded as implementation follow-up
- [x] §6 Regression Case 001 preserved permanently — signed 2026-08-06 with the amendment promoting the artifact's own `lore_summary` to primary exhibit, recording `biome` as propagation evidence, and noting `dominant_family` as a one-sentence pointer to Ruling 002 §7
- [x] §7 Open questions carried — signed 2026-08-06 as a complete inventory of known unresolved areas: 7.1 discharged to Ruling 002 with jurisdiction stated; **7.2 through 7.7 open and owned by Ruling 001**, including 7.3 retained here rather than handed onward, and 7.6 / 7.7 added from the 2026-08-06 corpus audit

Drafted 2026-08-04. **All seven sections signed off by the operator 2026-08-06; marked LOCKED and
binding as of that date.**

**Open questions carried under §7 are not closed by this lock.** §7 was signed as a complete
inventory of what remains unresolved, not as a resolution of it — 7.2 through 7.7 stay open and
owned by this ruling. Requirements ruled here but not yet enforceable are tracked in
`docs/open_contract_gaps.md` (GAP-1 from §2 Invariant 3, GAP-2 and GAP-3 from §3.4). A locked ruling
states what is true; it does not assert that implementations already obey it.
