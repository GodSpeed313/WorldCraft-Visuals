# WorldCraft Ruling 001 — Concept Canonicalization Policy

**Status:** DRAFT — pending operator review and sign-off.

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
The model may propose `name`, `family`, `modality`, `cost`. **It may not invent mechanics.**

## 3. Canonicalization policy

### 3.1 Default posture: conservative

Worked example, as ruled:

```
Mokuton                          <- canonical identity
├── aliases:
│   ├── Wood Release
│   ├── Wood Style
│   └── Wood Element
└── family: Nature Transformation
```

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
Results therefore carry one of three states:

| State | Meaning |
|---|---|
| **ADMITTED** | Concept recognized or resolved and validated. Fusion proceeds normally. |
| **CAUTIONARY** | Concept requires normalization. The idea may be inspected, but **no fusion output is generated until validation.** The engine never pretends the concept is grounded. |
| **BLOCKED** | Resolution failed or validation rejected the proposal. No output. |

Worked examples:

- `Hashirama Senju` → known: Wood Release, HIGH_CONCEPT, Nature family → **ADMITTED**.
- `Shadow Dragon Reality Collapse` (original character) → unknown → **CAUTIONARY**: *"Power concept
  requires normalization."* Inspectable; no fusion output.

## 5. The provider boundary

**Model calls are acceptable. The model is not the authority.**

```
LLM ──► Proposal ──► WorldCraft validator ──► Registry
```

The model proposes a classification — `name: Wood Release`, `family: Nature`,
`modality: HIGH_CONCEPT`, `cost: 8`. **The engine decides whether that enters reality.** This is the
Continuum separation restated: what generates is never what validates. The LLM is the historian;
WorldCraft is the scientist.

**Cost.** Acceptable. The model is classifying unknown concepts, not generating worlds — a narrow
enough task that 2–3 calls per novel concept is reasonable, and the result is cached permanently.

**Dependencies: stdlib only, initially.** The moment WorldCraft acquires a dependency stack it loses
one of its strongest properties — *anyone can run the engine anywhere*. A thin transport layer is
sufficient:

```
worldcraft/
└── resolver/
    ├── provider.py     — interface
    ├── anthropic.py    — one implementation
    └── cache.py        — resolved-concept memory
```

**The core engine must know nothing about Anthropic.** The provider is swappable and the engine's
correctness must not depend on which one is installed, or on one being installed at all.

## 6. Normalization Regression Case 001 — preserved permanently

`containment_matrix.json` currently holds exactly one fusion: **Hashirama Senju × William
Vangeance**, both silently defaulted to GROUNDED with `tags: ["unknown"]`, producing
`Espionage / One-Inch Punch / Psychological Mastery` — two nature-magic leaders rendered as spies.

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

**7.1 — SUPERSEDED BY RULING 002.** This ruling's own example refers to a `Nature` /
`Nature Transformation` family that does not exist; `POWER_FAMILIES` is exactly `COGNITION`,
`INFLUENCE`, `DISCIPLINE`, `PERCEPTION`. That gap turned out to be an ontology boundary rather than
a missing label, and is governed by `docs/ruling_002_family_taxonomy_integrity.md`. The operative
consequence for *this* ruling: **§5's example proposal (`family: Nature`) is illustrative of the
proposal shape only — it is not a valid classification under the current taxonomy**, and would be
rejected as `UNRESOLVED_FAMILY` per Ruling 002 §8.

**7.2 — `cost_factor` exact-match as a merge criterion.** §3.2(c) requires `cost_factor` to match
for a merge. As an integer, this makes an otherwise-identical pair with costs 8 and 9 permanently
unmergeable. This is arguably correct under Invariant 2 (conservative is the point), but it should be
a deliberate choice rather than an artifact of the field's type.

**7.3 — Modality's role polymorphism.** Modality generalizes across input types as *how far
consensus reality must bend*, but plays three different logical roles: **ceiling** for a character
(what it may hold), **ambient law** for a place (what may happen there), **requirement** for an
ability (what world it needs). The existing grounding filter already implements the ability-inside-a
-place case. Formalizing this belongs in Ruling 002.

---

## Sign-off checklist

- [ ] §1 Core principle — minting cheap, merging expensive
- [ ] §2 The three invariants
- [ ] §3 Canonicalization policy — conservative default, three merge requirements, alias≠merge, reversibility
- [ ] §4 Resolution states — ADMITTED / CAUTIONARY / BLOCKED, no hard-fail
- [ ] §5 Provider boundary — model proposes, engine decides; stdlib; core knows nothing about Anthropic
- [ ] §6 Regression Case 001 preserved permanently
- [ ] §7 Open questions carried, 7.1 flagged blocking

Drafted 2026-08-04. Not binding until signed off and marked LOCKED.
