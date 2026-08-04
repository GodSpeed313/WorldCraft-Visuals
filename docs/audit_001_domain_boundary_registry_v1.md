# WorldCraft Domain Boundary Audit — Registry v1

**Type:** Evidence document. **Not a ruling.** It records what the registry currently is; it decides
nothing and names nothing.

**Purpose (as commissioned):** *Determine whether current family assignments preserve semantic
locality or rely on accidental compatibility.*

**Scope:** all 30 `POWER_REGISTRY` entries, with the eight HIGH_CONCEPT entries flagged as priority
cases. Audited against `logic_auditor.py` at commit `fd72897`.

**Method note — measured vs. judged.** Part 1 is computed from the engine and is reproducible. Part 2
contains semantic judgments, which are lore and therefore proposals for the operator to accept,
revise, or reject. The two are kept separate on purpose; a judgment presented as a measurement is the
same class of error this audit exists to find.

---

## Part 1 — Measured findings

### M1. The family-fallback path is currently dead code

`_grounding_candidates` uses a curated `TRANSPOSITION_MAP` entry when one exists and falls back to
the power's family only when none does.

```
powers that can ever require grounding : 12
of those, WITHOUT a curated entry      : 0
=> the family-fallback branch fires for 0 of 12
```

All 12 non-LEGACY powers have hand-written transposition entries. The 18 LEGACY powers are legal at
every modality and never ground. **The family-fallback branch therefore never executes against the
authored registry.**

### M2. Every grounding edge is intra-family, and every one is curated

The reverse index — for each landing target, which powers can ground onto it — returns exactly one
source family for every target. There are **zero cross-family grounding edges** in the current
registry.

This is not an accident of the algorithm. It is authorship: the `TRANSPOSITION_MAP` comment records
the rule being applied by hand —

> *"Every entry now stays inside the source power's family: a perception-driven person grounds into a
> different EXPRESSION of perception, not into somebody else's essence."*

**The locality property Ruling 002 §5.1 proposes as a domain invariant is already being enforced
manually, one family down.** The domain layer is not a new principle. It is the existing principle
extended to a taxonomy that can hold non-human concepts.

### M3. The safety is a property of authorship, not of the system — and learning is what breaks it

Simulating the arrival of a learned power with no curated entry (`Wood Release`, HIGH_CONCEPT,
cost 8), grounded into a LEGACY fusion, under each possible family assignment:

| assigned family | fallback pool | grounds to |
|---|---|---|
| DISCIPLINE | Adaptive Combat, Indomitable Will, Iron Discipline, Martial Perfection | **Adaptive Combat** |
| COGNITION | Art of War, Mastermind Architecture, Pattern Recognition, Strategic Genius, Tactical Brilliance, The Scientific Method | **The Scientific Method** |
| INFLUENCE | Cultural Resonance, Diplomatic Mastery, Rhetoric & Legacy, Symbolic Authority | **Symbolic Authority** |
| PERCEPTION | Intuitive Insight, Memory Palace, Psychological Mastery, Situational Awareness | **Intuitive Insight** |

**There is no correct answer available.** Every landing is a human-excellence power, under every
family assignment, because the entire LEGACY destination space is human excellence. The defect is not
that the family is wrong — it is that **no legal landing exists for a non-human concept**.

This is the precise mechanism by which the redirection to learned vocabulary breaks the engine:
curation currently supplies the safety, curation cannot scale to an unbounded input space, and the
first uncurated power activates a branch that has never run.

### M4. Domain is not derivable from modality

Two GROUNDED entries settle this. `Espionage` is GROUNDED and unambiguously human-excellence;
`Electromagnetic Pulse` is GROUNDED and unambiguously not. Meanwhile `Equivalent Exchange` is
HIGH_CONCEPT and is a world-law rather than a capability at all.

**Domain and modality are orthogonal axes.** Adding a domain layer does not duplicate modality, and
domain cannot be inferred from the modality already stored. This is a load-bearing input to Ruling
002 §5.

---

## Part 2 — Per-entry audit

**Failure types.** 1 = honest fit · 2 = wrong family, same domain · 3 = wrong domain · 4 = ambiguous
boundary case.

**Cluster labels are descriptive placeholders, not proposed names.** Naming domains is lore and is
deliberately left open.

### Priority cases — the eight HIGH_CONCEPT entries

| Power | Current family | Domain assumption | Fit | Type | Proposed cluster | Confidence |
|---|---|---|---|---|---|---|
| Cursed Energy | INFLUENCE | human excellence | **fail** | **3** | energy system | high |
| Angelic Override | INFLUENCE | human excellence | **fail** | **3** | supernatural manifestation | high |
| Reality Glitch | COGNITION | human excellence | **fail** | **3** | reality alteration | high |
| Domain Expansion | COGNITION | human excellence | **fail** | **3** | supernatural manifestation | high |
| Titan-Shifting | DISCIPLINE | human excellence | **fail** | **3** | biological transformation | high |
| Soul Resonance | DISCIPLINE | human excellence | **fail** | **3** | supernatural manifestation | medium |
| Spiral Power | DISCIPLINE | human excellence | partial | **4** | energy system | medium |
| Equivalent Exchange | COGNITION | human excellence | **fail** | **4** | world-law / systemic principle | medium |

**Notes.**

- `Cursed Energy → INFLUENCE` is the clearest single failure in the registry. INFLUENCE means moving
  people; cursed energy is a fuel source. It grounds today onto `Rhetoric & Legacy`, `Symbolic
  Authority`, `Cultural Resonance` — a supernatural resource becoming political persuasion.
- **`Spiral Power` — type 4 confirmed by operator ruling, superseding the type-2 commissioning
  example.** The earlier example assumed the domain was right and only the family wrong; the audit
  showed the domain itself is the questionable part. Two competing interpretations are live and
  **the ambiguity is to be preserved, not resolved**:
  - *human potential* — willpower, determination, growth (overlaps DISCIPLINE genuinely)
  - *energy system* — a supernatural force, a measurable fictional energy, reality-affecting

  Choosing prematurely because of the thematic overlap with DISCIPLINE would be the mistake. It is
  recorded as **domain unresolved**.
- `Equivalent Exchange` is marked 4 as commissioned: it may be a world-law, a conceptual ability, or a
  supernatural technique, and forcing the choice now creates exactly the future debt described.

### Non-priority findings — the GROUNDED tier

The eight above were already suspicious. These were not, and are the reason the audit covered all 30.

| Power | Current family | Domain assumption | Fit | Type | Proposed cluster | Confidence |
|---|---|---|---|---|---|---|
| **Electromagnetic Pulse** | COGNITION | human excellence | **fail** | **3** | energy system / technology | high |
| Kinetic Mastery | DISCIPLINE | human excellence | partial | **4** | enhanced physical | medium |
| One-Inch Punch | DISCIPLINE | human excellence | pass | 1 | human excellence | high |
| Espionage | PERCEPTION | human excellence | partial | **4** | human excellence | medium |

**Notes.**

- **`Electromagnetic Pulse → COGNITION` is a cross-domain failure hiding in the GROUNDED tier.** An
  EMP is an energy effect, not an act of thinking. It was almost certainly assigned COGNITION because
  it entered via Tesla, whose *character* is cognitive — the power inherited its owner's family. This
  is the audit's most useful non-obvious result: **the taxonomy boundary was already crossed outside
  the eight priority cases.**
- `Kinetic Mastery` and `Espionage` raise a *modality* question rather than a family one, and are
  logged here rather than resolved: both are marked GROUNDED under the comment "the body exceeds
  ordinary human limits," yet real spies exist and Bruce Lee's one-inch punch is documented. Whether
  the LEGACY/GROUNDED line is drawn correctly for these is out of scope for a family audit but should
  not be lost.

### The LEGACY tier — 18 entries, all type 1

| Family | Entries | Fit | Type | Confidence |
|---|---|---|---|---|
| COGNITION | Strategic Genius · The Scientific Method · Art of War · Pattern Recognition · Mastermind Architecture · Tactical Brilliance | pass | 1 | high |
| DISCIPLINE | Indomitable Will · Martial Perfection · Adaptive Combat · Iron Discipline | pass | 1 | high |
| INFLUENCE | Rhetoric & Legacy · Cultural Resonance · Diplomatic Mastery · Symbolic Authority | pass | 1 | high |
| PERCEPTION | Intuitive Insight · Situational Awareness · Psychological Mastery · Memory Palace | pass | 1 | high |

**All 18 are honest fits.** The four families partition human capability cleanly — thinking,
affecting, mastery, sensing — with no coercions and no boundary cases. The original taxonomy is not
defective. It is correct and complete *for its domain*, which is exactly the finding Ruling 002 §4
asserts, now measured rather than assumed.

---

## Part 3 — Answers to the commissioned questions

**Q1 — Which entries violate their assigned family?**
Seven type-3 failures: `Cursed Energy`, `Angelic Override`, `Reality Glitch`, `Domain Expansion`,
`Titan-Shifting`, `Soul Resonance`, `Electromagnetic Pulse`. Three type-4 boundary cases:
`Equivalent Exchange`, `Spiral Power`, `Kinetic Mastery` (plus `Espionage` on modality grounds).
**10 of 30 entries — a third of the registry — do not sit honestly in their assigned family.**

**Q2 — Which entries are only "working" because their current family is broad?**
All eight HIGH_CONCEPT entries, and `Electromagnetic Pulse`. They work because COGNITION, DISCIPLINE
and INFLUENCE are broad enough to absorb anything if read loosely — COGNITION as "mental," DISCIPLINE
as "physical," INFLUENCE as "affects others." Read strictly, as the LEGACY tier uses them, none of the
nine fits. **The breadth doing the absorbing is the accidental compatibility the audit was
commissioned to look for.**

**Q3 — Which entries share a grounding neighborhood despite different families?**
**None.** Measured, not estimated — see M2. Zero cross-family grounding edges exist. This is the
audit's most surprising result and it is *good* news: the current registry has no active contamination.

**Q4 — How many natural domains exist?**

**Operator ruling on how to state this:** the audit has identified **one confirmed domain and several
candidate domains requiring additional evidence.** Not "two or three domains" — that phrasing would
pre-commit to a count the evidence does not support, and would abandon the same conservative
philosophy Ruling 001 applies to canonicalization.

| Status | Cluster | Members | Evidence |
|---|---|---|---|
| **Confirmed** | human excellence | 18 LEGACY + One-Inch Punch + Espionage = 20 | all LEGACY entries honest fits; four existing families; stable, measured grounding behavior |
| **Likely** | supernatural / phenomenon | Cursed Energy, Domain Expansion, Angelic Override, Soul Resonance, Reality Glitch | five members, consistent character |
| Candidate — insufficient | energy systems | Spiral Power, Cursed Energy, Electromagnetic Pulse | needs more entries before it can be separated from *supernatural / phenomenon* |
| Candidate — insufficient | biological transformation | Titan-Shifting | **n = 1** — needs a second member |
| Candidate — insufficient | world laws / systems | Equivalent Exchange | **n = 1** — needs a second member |
| Candidate — insufficient | enhanced physical | Kinetic Mastery | **n = 1** — may be a sub-cluster of human excellence |

**`Cursed Energy` appears in two clusters, and that is a finding rather than a bookkeeping error.**
It is the clearest evidence that *energy systems* may not separate from *supernatural / phenomenon*
at all — the same member reads naturally in both. Until a member exists that belongs to one and not
the other, the separation is unsupported.

**Caution: three clusters have exactly one member.** A domain minted for a single entry cannot be
distinguished from a mis-assignment, and under Ruling 002 §3 a domain is an ecosystem change. Thin
clusters are recorded as candidates awaiting a second member, not created now.

**Q5 — Are some current families actually subfamilies inside a larger domain?**
**Yes, and the evidence is unambiguous.** All four families are subfamilies of human excellence:
18 of 18 LEGACY entries are honest fits, partitioning 6/4/4/4 with no coercions. The nesting sketched
in Ruling 002 §5 is confirmed by the data rather than merely plausible.

---

## Part 4 — What this changes about Ruling 002

1. **§5.1 is confirmed as a safety invariant, and its urgency is now measurable.** The cross-domain
   contamination path is real, currently dormant, and activated by the *first* uncurated power (M1,
   M3). It is not a latent risk to monitor; it is a guaranteed failure on the first learned concept.

2. **§5.1 is also less novel than it read, in a way that strengthens it.** Intra-family locality is
   already enforced by hand across all 12 curated entries (M2). The domain rule generalizes a rule the
   operator already applied, rather than imposing a new one.

3. **The terminal-fallback problem is worse than "each domain needs one."** M3 shows the entire LEGACY
   destination space is human excellence, so a non-human power grounding into a LEGACY fusion has
   nowhere legal to land *at all*. Per-domain fallbacks require per-domain LEGACY-legal members to
   exist first — which for supernatural or energy domains may be a contradiction in terms, since
   LEGACY means human limits. **This may mean cross-domain grounding must be refused rather than
   redirected** — i.e. the correct outcome is a CAUTIONARY result, not a substitution. That is a
   ruling decision, not an audit finding.

4. **Domain must be stored, not derived (M4).** It is orthogonal to modality and cannot be inferred
   from it.

5. **The commissioning premise was too narrow** (open question §9.5 in the pre-audit draft of Ruling
   002, since discharged and removed by this audit). It scoped the audit to the eight HIGH_CONCEPT entries;
   `Electromagnetic Pulse` shows the boundary was already crossed in the GROUNDED tier. The
   instruction to audit all 30 was correct and produced the finding.

---

## Part 5 — What this audit does not decide

Domain names. Which clusters become domains. Whether the thin single-member clusters are real. Per-
domain terminal fallbacks, or whether cross-domain grounding is refused instead. Whether the ten
mis-fitted entries are reclassified, and in what order. Whether `Kinetic Mastery` and `Espionage`
are correctly placed on the modality axis.

All lore, all operator decisions. The audit's contribution is that these are now decisions about a
measured shape rather than an imagined one.

---

**Audit performed 2026-08-04 against `fd72897`. Part 1 is reproducible; Part 2 is proposal.**
