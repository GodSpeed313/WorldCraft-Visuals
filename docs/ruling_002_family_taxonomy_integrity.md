# WorldCraft Ruling 002 — Family Taxonomy Integrity

**Status:** **LOCKED** — all sections signed off by the operator, 2026-08-15. Binding.

**Relationship to Ruling 001.** 001 governs how concepts enter the system and when two concepts may
be treated as one. 002 governs the *categories* concepts are admitted into. It supersedes 001 §7.1,
which flagged this as blocking and deferred it here.

**Why it is separate.** 001's failure mode is *"we do not know this thing yet."* 002's is *"our
categories are not large enough for this thing."* Solving either one does not solve the other, and
conflating them would hide the second behind the first.

**Evidence base.** §§4, 5.1, 5.2 and 6 are grounded in
`docs/audit_001_domain_boundary_registry_v1.md`, a measured audit of all 30 registry entries at
commit `fd72897`. Where this ruling makes an empirical claim, the audit is the source; claims that
could not be measured are marked as such.

---

## 1. The reframing — what `family` actually is

**`family` is not an ontology of powers. It is a grounding behavior class inherited from the legacy
system.**

Verified against the engine — `family` is consumed in exactly two places:

| Site | Use | Kind |
|---|---|---|
| `logic_auditor.py:150` (`_grounding_candidates`) | supplies substitution candidates when a power exceeds the fusion's modality ceiling and has no explicit transposition entry | **behavior** |
| `mythos_sync.py:238` (`dominant_family`) | characterizes the fusion's disposition | **description** |

The second use is an accident of history, and the code says so: *"family is the closest thing the
engine currently has to a disposition."* Family was pressed into service as a disposition proxy
because nothing better existed. See §7.

**Scope amendment — operator ruling, 2026-08-06.** Additional non-engine uses may exist outside this
scope. Audit 002 (C3) records one such unresolved use: family represented as an accumulating
resource quantity in card output. Such representations are not governed by this section.

### 1.1 The transition this ruling actually governs

**The original LEGACY design was not wrong. It was a closed-world model.** Every concept was
authored, every concept was human, and every grounding destination was known in advance. Within that
world the four families are complete and correct — the audit confirms all 18 LEGACY entries are
honest fits.

**WorldCraft is becoming an open-world model.** Concepts arrive unauthored, from any source, at any
modality. **The domain layer is the boundary between those two realities**, and every invariant below
exists to make that transition safe rather than to repair a defect.

## 2. Ruling — family is not a catch-all category

**A concept must not be assigned an existing family merely because a slot exists.**

If no existing family semantically contains the concept, the correct outcome is:

```
UNRESOLVED_FAMILY
```

**not**

```
BEST_GUESS_EXISTING_FAMILY
```

**The precedent this prevents.** Forcing Wood Release into DISCIPLINE or COGNITION would establish
exactly the rule the normalization layer exists to eliminate:

> *"When reality does not fit the taxonomy, bend reality to the taxonomy."*

That is the same defect as Ruling 001 §6's silent GROUNDED default, relocated one layer up. A coerced
family is not a small inaccuracy — it is a false statement about what kind of thing the concept is,
inherited by everything that grounds through it.

**Scope — operator ruling, 2026-08-06. This section governs family assignment only.** It rules what
may be written into a concept's `family` field and nothing else. It does **not** govern what the
grounding layer does with a concept whose family could not be resolved: under Addendum A's fixed
`domain → family → grounding` sequencing, that is a separate layer, and expanding this ruling to
reach it would put taxonomy authority over a stage it does not own.

The implementation's grounding-target fallback — `DEFAULT_TRANSPOSITIONS` — is therefore **not
ruled on here**, and no reader may take §2 as having authorized, forbidden, or bounded it. It is
carried as **GAP-4** in `docs/open_contract_gaps.md`, which records the verification finding that
the halt preventing an unplaceable concept from reaching grounding is stated in §8 and §8.1 but is
enforced by no invariant and no code. **Signing §2 does not close that gap and must not be read as
having closed it.**

## 3. Expansion rates — why families need a higher threshold than powers

| | expands | a change is |
|---|---|---|
| **Power vocabulary** | frequently — Wood Release, Mokuton, Gravity Manipulation, Ki Projection | **local** |
| **Family vocabulary** | rarely | an **ecosystem change** |

A family changes grounding behavior for everything beneath it. **New power = local change. New
family = ecosystem change.** The admission threshold for a family is therefore *higher* than for a
power — the opposite of the usual instinct, which treats broader categories as safer because they are
vaguer.

**Mechanism — operator ruling, 2026-08-06.** Inheritance currently flows through **profile
classification**, not grounding. `family_of` feeds `power_families` and `dominant_family` into every
emitted profile (`mythos_sync.py:238–252`), and a single family reassignment changes the emitted
`dominant_family` in a mean of 7.2% of sampled fusions. **The grounding channel this section names
is not yet live**: the family fallback is Audit 001 (M1)'s dead branch, firing 0 of 12. The higher
threshold is therefore justified today by classification inheritance and prospectively by grounding
inheritance, and both are reasons for the same rule. A future reader must not take the grounding
sentence as a description of current behavior.

This inverts the Ruling 001 §1 economics one level up and for a different reason: there, minting is
cheap because a redundant power is recoverable. Here, minting is expensive because a family is
inherited.

## 4. Finding — the four families are complete for one observed capability cluster only

`COGNITION` / `INFLUENCE` / `DISCIPLINE` / `PERCEPTION` were authored for the LEGACY tier rebalance.
They are **human capability families**: thinking, affecting, training/mastery, sensing.

They do not describe elemental transformation, reality alteration, supernatural manifestation, energy
systems, or biological mutation.

**Measured (audit Part 2, per-entry audit; restated at Part 3 Q5):** all 18 `LEGACY` entries are
honest fits, partitioning **6/4/4/4** — COGNITION 6, INFLUENCE 4, DISCIPLINE 4, PERCEPTION 4 — with
no coercions and no boundary cases.

**The set these families serve is wider than the `LEGACY` modality tier.** Audit Part 3 Q4 records a
confirmed cluster of **20 entries**: the 18 `LEGACY` entries plus `One-Inch Punch` and `Espionage`,
both `GROUNDED`. Both resolve cleanly to an existing family — `One-Inch Punch` → `DISCIPLINE`,
`Espionage` → `PERCEPTION` — so neither is a family failure. (`Espionage` is flagged at Part 3 Q1 on
**modality** grounds only; that is a question for its modality, not for its family.) Across all 20 the
partition is **6/4/5/5**. The 6/4/4/4 figure above is scoped to the 18-entry `LEGACY` subset.

**This section records an observed capability cluster, not a domain.** A cluster records an
observation; a domain asserts architecture. No domain is named or established here — the audit's
"human excellence" label is a descriptive placeholder (audit Part 2 preamble), and domain naming
remains open under §10.

**10 of 30 entries do not sit honestly in their assigned family** — seven of audit failure-type 3
(wrong domain), three of type 4 (ambiguous boundary). **All ten fall outside the 20-entry cluster**:
the split is 20/10 with no overlap. The original taxonomy is not defective. It is correct and complete
*for the cluster it was authored against*, and the failures are concentrated entirely outside it.

## 5. The domain layer

**The domain taxonomy is not adopted by this ruling** — no domain is named, no membership is
assigned, and the domain set is not fixed. Those decisions are recorded here as the agreed
direction, to be made deliberately.

**The domain concept is not deferred, and this ruling does not pretend otherwise.** It is already
load-bearing in signed material: Ruling 001 §4 — locked — defines `SURFACED` as the state reached
when *"no in-domain grounding candidate exists"*, citing §5.3 as its source, and maps
`GROUNDING_UNAVAILABLE` → `SURFACED` for a fusion resolved *"against a domain where grounding would
require a bridge that does not exist"*. That state is unstatable without the concept. What remains
open is the taxonomy, not the idea.

Adoption of the machine-enforceable form is Contract 001's to make — it defines the three domain
resolution states and invariant I7, and this ruling does not adopt them on its behalf.

The four families are **not** to be replaced. The safer evolution nests them:

```
domain
├── ‹"human excellence"› — descriptive placeholder, not an adopted domain name
│   ├── COGNITION
│   ├── INFLUENCE
│   ├── DISCIPLINE
│   └── PERCEPTION
├── (further domains — see audit Part 3, Q4)
```

**This is a taxonomy decision, not a patch.** Domain names are lore and belong to the operator.

### 5.1 Domain isolation is a precondition for learned grounding

**Stated as measured, not as alarm.** The audit establishes:

> **The current architecture relies on authored transpositions to preserve locality. Learned
> vocabulary removes that guarantee unless domain isolation exists.**

The supporting measurements:

- **The family-fallback branch is currently dead code.** All 12 powers that can ever require
  grounding carry hand-written `TRANSPOSITION_MAP` entries; the 18 LEGACY powers never ground. The
  fallback fires for 0 of 12 (audit M1).
- **There are zero cross-family grounding edges in the registry** (audit M2). Measured across all
  12 entries — every destination in every source's candidate list shares that source's family, in
  the 8 `HIGH_CONCEPT` entries as well as the 4 `GROUNDED` ones. The system is not currently
  contaminated.
- **That locality is authorship, not architecture.** The 12/12 measurement above is the evidence;
  the `TRANSPOSITION_MAP` comment at `logic_auditor.py:126-128` records the intent, for the
  `GROUNDED` block it sits under: *"Every entry now stays inside the source power's family."* That
  comment does not speak for the 8 `HIGH_CONCEPT` entries above it, which carry no such note — their
  locality is equally real and equally hand-made, just undocumented. **The invariant this ruling
  proposes is already being enforced manually, one layer down.** The domain layer generalizes an
  existing rule rather than imposing a new one.
- **The locality check is evaluated against the family assignments themselves, and 10 of 30 of those
  are wrong** (audit Part 3, Q1). A passing locality check is therefore not evidence of a correct
  grounding. Live example: `Reality Glitch` → `Electromagnetic Pulse` passes, both being `COGNITION`
  — and **both are type-3 wrong-domain failures**, `Electromagnetic Pulse` sitting in `COGNITION`
  only because it inherited the family of Tesla, its originating character. Two entries in the same
  wrong family satisfy an invariant that only compares them to each other. This does not weaken the
  finding; it sharpens it — hand-enforcement preserved family-adjacency but could not preserve
  domain-adjacency, because no domain exists yet to preserve.
- **Learning removes the guarantee.** The first uncurated power activates a branch that has never
  run.

### 5.2 — No Cross-Domain Terminal Substitution

**A concept may not resolve into a grounding candidate outside its domain.**

If a domain has no valid grounding member, the terminal state is:

```
GROUNDING_UNAVAILABLE
```

**The engine must not manufacture a bridge between incompatible realities.**

**The decisive evidence (audit M3).** A learned `Wood Release` (HIGH_CONCEPT) entering a LEGACY
fusion, simulated under every possible family assignment. The grounding target is **not** a single
value: `ground_power` ends in `random.choice`, so each assignment yields a *set* of legal candidates
and one is drawn per run.

| assigned family | grounds to — full candidate set | n |
|---|---|---|
| DISCIPLINE | Adaptive Combat · Iron Discipline · Martial Perfection · Indomitable Will | 4 |
| COGNITION | The Scientific Method · Pattern Recognition · Strategic Genius · Mastermind Architecture · Art of War · Tactical Brilliance | 6 |
| INFLUENCE | Symbolic Authority · Cultural Resonance · Rhetoric & Legacy · Diplomatic Mastery | 4 |
| PERCEPTION | Intuitive Insight · Memory Palace · Situational Awareness · Psychological Mastery | 4 |

Measured at `7c423a9`. The four sets total **18** — the entire LEGACY tier — and partition
**6/4/4/4**, the same partition recorded in §4.

**The failure is not classification. The failure is that every available destination belongs to the
wrong ontology.** The entire LEGACY destination space is human excellence, so no family assignment
can produce a correct landing.

**The wrong landing is not even stable.** Because selection is random within the set, the same
learned `Wood Release` grounds to a different human capability on each run. The concept does not
merely land wrongly — it has no fixed meaning in the output at all.

**Relation to Regression Case 001 — a shared defect class, not a shared code path.** That
instability is the same *class* of failure as the artifact recorded in §9: a random selection over a
candidate set the taxonomy cannot narrow. It is **not** the same mechanism, and the two must not be
merged in the record. Regression Case 001's variance enters at character resolution — unknown inputs
tagged `unknown`, powers drawn at random during fusion assembly, measured at **90 distinct
approved-power sets over 200 runs** (seeds 0–199, at `7c423a9`) — and its grounding path never
fires, because the powers drawn are already legal for that fusion. The instability described here
enters one layer later, at grounding-target selection. Two entry points, one shape: **where the
taxonomy cannot decide, the engine picks.** This is the runtime form of §9's failure 2, not a third
defect.

The required result:

```
Wood Release
    modality : HIGH_CONCEPT
    domain   : unresolved supernatural / natural phenomenon
    grounding: unavailable
```

**not**

```
Wood Release → closest human achievement
```

**Why this is an invariant and not a preference.** A fallback *implies comparability*. If two
concepts cannot exist in the same grounding space, substitution is not a lossy operation — it is a
**false** one. This also resolves the `Indomitable Will` question: the defect was never that it was a
poor fallback, but that offering any fallback across a domain boundary asserts a relationship that
does not exist.

### 5.3 — Unresolvable Grounding Must Surface

**A failed grounding resolution must never be silently substituted or discarded.**

Ruling 002 invalidated an assumption the Grounding Filter was built on: that substitution is always
possible. The filter's output space has therefore expanded.

```
Before:                          After:
requested power                  requested power
      ↓                                ↓
grounding candidate              grounding resolution
      ↓                                ├── grounded candidate
fusion continues                       └── GROUNDING_UNAVAILABLE
```

**Ruling: a fusion surfaces the incompatibility.** Not a hard failure, and not a silent partial
result. Fusion output must preserve:

- accepted powers
- unresolved powers
- **the reason for exclusion**

```
Fusion generated:
    accepted components : X
    rejected components : Y — no valid grounding domain
```

**Enforcement is currently partial.** Contract 001 **I5** requires the reason to travel to the output
and **I7** fixes `SURFACED` as terminal; **no invariant requires a `SURFACED` result to report the
accepted components alongside the rejected ones.** Without one, an implementation may discard what
resolved and still conform — the hard-failure alternative this section rejects. Tracked as **GAP-5**.

**`GROUNDING_UNAVAILABLE` is not an error condition. It is a valid ontology state.**

The rejected alternatives, and why: a *hard fusion failure* discards the work that did resolve, and a
*silent partial result* lets the system report "the fusion succeeded" when the truth is "the fusion
partially resolved and one component had no legal reality anchor." Surfacing is chosen because it
**preserves information** — not because it is more forgiving. It keeps the worldbuilding experience
intact without permitting false mechanics.

### 5.4 — Terminal Resolution Policy, not terminal fallback

**"Every domain needs a terminal fallback" was too broad. The correct statement is: every domain
needs a terminal resolution *policy*.** These are not the same thing.

A *fallback* implies a member of the same reality class is available to absorb the concept. That
holds for human excellence and may be impossible elsewhere: a supernatural concept cannot resolve
into a human-limit concept without violating §5.2, and LEGACY *means* human limits.

| Domain | Terminal policy |
|---|---|
| human excellence | fallback → `Indomitable Will` — coherent, because the domain is itself grounded in human capability |
| supernatural phenomenon | fallback → **none**; resolution → `GROUNDING_UNAVAILABLE` |

**Ruling: Option B — some domains terminate with refusal.** The rejected alternative (Option A, every
domain gets a terminal member) would force the invention of *artificial bridge concepts whose only
purpose is being a fallback* — lore authored to satisfy a mechanism rather than to mean anything.

**The underlying model shift this reflects:**

> **domain = compatibility boundary, not bucket of things.**
> **Some boundaries have neighbours. Some boundaries are walls.**

A domain is not a folder. Refusal is a legitimate terminal state for a wall.

## 6. — Provenance Does Not Determine Classification

**A power's originator does not define the power's family. Classification belongs to the capability
itself.**

**Who this rule addresses.** This is a rule about **classification authority**: it binds whoever
assigns a family to an entry. It is not a runtime invariant. No code path carries a family from a
character to a power — characters hold no `family` field at all (`modality_classifier.py`), and the
character→power link that does exist is tag-based (`TAG_POWER_MAP`, `mythos_sync.py:50`), which
carries no family information. No code path in the character-to-power pipeline could therefore violate
this rule. How it should be enforced once family assignment is no longer hand-authored is not ruled
here.

**The evidence (audit Part 2, GROUNDED tier).** `Electromagnetic Pulse` is classified `COGNITION`
(`logic_auditor.py:50`). An EMP is an energy effect, not an act of thinking. The misclassification is
the finding, and it stands on the entry alone.

**On origin — an inference, not a finding.** Tesla's *character* is cognitive, and the assignment may
have been reasoned from him. This is not established: no mechanism exists that could have propagated a
family from character to power, so the resemblance is the only evidence for it and it is not
sufficient. The failure mode named here — *a technology inheriting its inventor's family* — is what
this section forbids going forward; it is not a diagnosis of how this entry came to be wrong.

**Why this finding is disproportionately important:** it proves the domain problem is **not** confined
to HIGH_CONCEPT. The boundary was already crossed in the GROUNDED tier, in an entry nobody had flagged
as suspicious. Auditing all 30 entries rather than the eight obvious ones is what surfaced it.

## 7. Consequence — `dominant_family` breaks under a domain layer

`dominant_family` is computed as `max(set(families), key=families.count)` over the approved powers
(`mythos_sync.py:238-239`). Once powers span domains, that expression takes a plurality vote across
**incommensurable categories** — a set like `[COGNITION, NATURE_TRANSFORMATION, PERCEPTION]` yields an
arbitrary winner that characterizes nothing. `NATURE_TRANSFORMATION` is a **descriptive placeholder**
used to illustrate a cross-domain set; it is not a registry family, and this section mints no family
name.

**The expression is already failing, before any domain layer exists.** The domain consequence above is
this section's subject and is unchanged. What follows is a present-tense finding: the current registry
alone is sufficient to produce the failure.

- **Ties are structurally possible under the current registry.** A profile carries three approved
  powers drawn over four families, so no plurality is guaranteed and a tie requires no cross-domain
  vocabulary to arise.
- **Ties occur in actual emitted profiles.** This is observed behavior, not a hypothetical property of
  the expression.
- **The tie winner is process-dependent.** `set()` over family strings iterates in string-hash order,
  and string hashing is randomized per process. Demonstrated on fixed input, with no engine and no
  seeded randomness involved: `["COGNITION", "PERCEPTION", "INFLUENCE"]` resolves to `PERCEPTION`
  under `PYTHONHASHSEED=0`, to `COGNITION` under `PYTHONHASHSEED=1`, and varies between runs when the
  seed is unset.
- **That value reaches persisted output.** `dominant_family` is written into every emitted profile
  (`mythos_sync.py:252`) and exported to `containment_matrix.json` (`export_for_web`), which the
  dashboard reads. The nondeterminism is consequential, not internal.
- **The existing tests do not detect this axis.** They assert that `dominant_family` is a member of
  `POWER_FAMILIES` and appears among the profile's own families (`test_engine.py:383-385`). Both hold
  whichever tied family wins, so the suite is satisfied under every permutation.

The section's mechanism is therefore right and its timing is not: the break does not wait for domains.
A domain layer widens an expression that is already returning an unreproducible answer. This section
records the defect; it does not rule a remedy.

The disposition question is real and worth keeping; `family` was only ever a stand-in for it. Whether
disposition becomes its own field, is computed per-domain, or is derived from the philosophy axes
already on the roadmap is an open design question and is **not** resolved here.

## 8. The normalization contract

**A learned concept may not enter the registry unless all of the following are valid:**

- `modality`
- `family`
- `cost_factor`

**If family validation fails, the proposal is rejected:**

```
proposal rejected: concept requires taxonomy extension
```

**not**

```
concept coerced into nearest family
```

Rejection is not failure — it is the system correctly reporting that its categories are too small. A
rejected proposal is a signal to the operator that the taxonomy needs extending, which is a lore
decision, not an engineering one.

### 8.1 Mapping to Ruling 001 §4 result states

Three vocabularies now exist and must not be confused. `UNRESOLVED_FAMILY` is a **proposal** outcome;
`GROUNDING_UNAVAILABLE` is a **grounding** outcome; `ADMITTED` / `SURFACED` / `CAUTIONARY` /
`BLOCKED` are **fusion result** states.

**Scope of "proposal" in this section.** Throughout §8, *proposal* means a family-classification
proposal — the three-field submission this section governs. The term is this section's own and
carries no authority outside it. The fusion-result vocabulary belongs to Ruling 001 §4; §8 maps onto
it and does not characterize the scope of any of its states.

| Situation | Proposal | Grounding | Fusion result |
|---|---|---|---|
| Recognized or resolved, all three fields valid, grounding legal or unnecessary | accepted | n/a or resolved | **ADMITTED** |
| Resolved, but no existing family contains it | `UNRESOLVED_FAMILY` | — | **CAUTIONARY** |
| Resolved and classified, but no in-domain grounding candidate exists | accepted | `GROUNDING_UNAVAILABLE` | **`SURFACED`** — accepted and rejected components both reported, with reason (§5.3); terminal, not a degraded `ADMITTED` |
| Could not be resolved at all | unresolved | — | **BLOCKED** |

The second row is the one that matters most: the concept is *understood* but *uncategorizable*. That
must never present as the same condition as "unknown," because the operator action it calls for is
completely different — extend the taxonomy, not resolve the name.

## 9. Regression Case 001 — receipt of failure 2

The two independent failures exposed by Hashirama Senju × William Vangeance are recorded in
**Ruling 001 §6**, which is locked, together with the artifact itself and the requirement that they
stay separate. That table is the record. This section does not restate it, and no restatement of it
belongs here.

Ruling 001 §6 assigns the second failure — *"the registry has no honest place for
non-human-excellence abilities"* — to Ruling 002, under the column heading **Governed by**. **This
section is the acknowledgement of that assignment.** The failure is Ruling 002's to govern, and it is
**not resolved by this ruling**; the taxonomy extension it calls for is carried as §10.1, which is
open. Acknowledging an assignment records ownership, not closure.

Its relationship to the grounding instability measured in this document is already stated at **§5.2**
— ***a shared defect class, not a shared code path*** — including the measurement that Regression
Case 001's own grounding path never fires. That statement is §5.2's; this section adds nothing to it
and does not re-derive it.

---

## Addendum A — Domain Before Family

**The operative resolution order.** Consolidates §§2, 5.1, 5.2 and 6 into the sequence the engine
must follow.

1. **Family is only meaningful inside a domain.**
2. **Domain cannot be inferred from family** — nor from modality (audit M4; the two axes are
   orthogonal, proven by `Espionage` and `Electromagnetic Pulse` sharing a modality and not a domain).
3. **Learned concepts require domain resolution before family grounding.**
4. **Cross-domain fallback is prohibited.**
5. **A domain without a valid grounding candidate returns no substitution.**

```
concept
   ↓
domain resolution
   ↓
family resolution
   ↓
grounding candidates
   ↓
fusion compatibility
```

**not**

```
concept
   ↓
family
   ↓
hope the neighbours are similar
```

---

## 10. Open questions

**10.1 — Which candidate domains become domains, and what are they called?** The audit identifies
*"one confirmed domain and several candidate domains requiring additional evidence"* (audit Part 3,
Q4). Names are lore.

Signed §9 (`:462`) routes locked Ruling 001 §6's failure-2 "taxonomy extension" here, and this item
is worded as a domain question. Whether it splits — domain adoption on one side, taxonomy extension
on the other — or whether domain promotion **is** the taxonomy extension under Addendum A Point 3
(*"Learned concepts require domain resolution before family grounding"*) is part of this question.

**10.2 — DISCHARGED → §5.4.** Ruled: terminal resolution *policy*, not terminal fallback. Some
domains terminate with refusal (Option B); artificial bridge concepts are rejected.

**10.3 — What replaces `dominant_family` as disposition?** §7 diagnoses the defect in full —
ties are structural, the tie winner is process-dependent, and the expression already fails
pre-domain — and rules no remedy. What replaces it remains undecided.

**10.4 — Who may propose a family or domain?** Operator-authored only, or model-proposed under a
stricter audit than powers receive. §3 argues the family threshold must be higher than for powers;
no equivalent threshold argument exists for domains. Domain naming is already settled as
operator-only (§5, 10.1); domain admission — whether a new domain may ever be proposed at all — is
not.

`contract_001:31-38` routes domain names and domain count to "lore — operator" (`:33-34`). That is a
routing assignment in a draft document, not a threshold argument, so it neither supplies the missing
argument nor contradicts the negative above. Recorded as an observation; Contract 001 is unsigned
and nothing here rests on it.

**10.5 — How, and in what order, are the ten mis-fitted entries reclassified?** The audit identifies
them; it does not reclassify them. Order and method are open, and `Electromagnetic Pulse` (§6) is
the priority case because it sits in the tier nobody was watching.

This item and 10.7 divide by **axis, not by entry**. 10.5 concerns family placement; 10.7 concerns
modality placement. `Kinetic Mastery` appears in both — it is one of the ten (audit Part 3 Q1, a
type-4 boundary case) and is also 10.7's subject. `Espionage` is expressly outside the count of ten,
flagged there "on modality grounds," so it belongs to 10.7 alone.

**10.6 — DISCHARGED → §5.3.** Ruled: unresolvable grounding must surface. Fusion output preserves
accepted powers, unresolved powers, and the reason for exclusion; `GROUNDING_UNAVAILABLE` is a valid
ontology state rather than an error. Enforcement is currently partial — Contract 001 I5 carries the
reason, I7 fixes terminality, and no invariant requires a `SURFACED` result to report the accepted
set alongside the rejected — tracked as GAP-5.

**10.7 — Are `Kinetic Mastery` and `Espionage` correctly placed on the modality axis?** Both are
marked `GROUNDED` under "the body exceeds ordinary human limits" (`logic_auditor.py:47`), yet real
spies exist and the one-inch punch is documented. A modality question, not a family one; see 10.5
for the axis split.

The evidence just given is uneven, and that is recorded rather than repaired. "Real spies exist"
supports `Espionage`; "the one-inch punch is documented" supports `One-Inch Punch`
(`logic_auditor.py:51`) — same block, inside the confirmed 20-entry cluster, and not a subject of
this question. Nothing above supports `Kinetic Mastery`.

`Kinetic Mastery` carries a prior authorial ruling this question must account for. `bca630b`
(2026-08-03) recorded: *"Kinetic Mastery stays GROUNDED. Promoting it would collapse the rung
between 'the mind commands the body' and 'the body exceeds normal limits'. LEGACY-tier DISCIPLINE
powers were added alongside it instead."* A reason, a classification, and a consequential action —
one day before both Audit 001 and this section. It does **not** discharge this question: a commit
message is not a governing document.

**10.8 — May Ruling 002 characterize the scope of Ruling 001's locked `BLOCKED` row?** Three scoped
uses of *proposal* bear on this question, and this section establishes co-reference between none of
them.

Locked Ruling 001 uses the word twice, in different places and for different work. Invariant 3
(`ruling_001:47`) constrains learned vocabulary: *"The model may propose `name`, `family`,
`modality`, `cost_factor`."* §4's `BLOCKED` row (`ruling_001:182`) states a resolution-state
trigger: *"Resolution failed or validation rejected the proposal. No output."* The row does not cite
Invariant 3, and Ruling 001 nowhere states that §4's *the proposal* is Invariant 3's submission.

§8 uses the word a third way, and signed §8.1 bounds it: *"Throughout §8, proposal means a
family-classification proposal — the three-field submission this section governs. The term is this
section's own and carries no authority outside it"* (`:436-439`; the three fields are `modality`,
`family`, `cost_factor`, at `:410-412`). §8's sign-off (`:633`) records the collision between that
term and Ruling 001 §4's row as observed and not resolved.

The comparison this section must not make follows from that boundary. §8.1 row 2 routes
`UNRESOLVED_FAMILY` to `CAUTIONARY`. Whether that conflicts with the locked `BLOCKED` row can only
be asked after deciding whether the case §8.1 row 2 describes is one `ruling_001:182` would refuse —
and that cannot be decided without reading §8's term past the boundary §8.1 sets for it. Comparing
the two outcomes presupposes the co-reference at issue.

Field lists that overlap do not establish co-reference; neither does shared terminology, nor an
apparently shared case whose identification requires that same import. What is established is a
collision between independently scoped usages. Whether they co-refer to one submission or one case
is unresolved, and whether Ruling 002 may characterize the scope of a locked Ruling 001 row in order
to settle it is the jurisdiction question this section does not decide.

**10.9 — Are the thin single-member clusters real?** Audit Part 3 Q4 marks three clusters
"Candidate — insufficient" at n = 1: biological transformation (`Titan-Shifting`), world laws /
systems (`Equivalent Exchange`), and enhanced physical (`Kinetic Mastery`, "may be a sub-cluster of
human excellence"). Distinct from 10.1: that item asks which candidates are **adopted** as domains;
this asks whether the thin ones exist as clusters at all. The audit states them as separate
sentences (Part 5).

**10.10 — Which meaning of `DISCIPLINE` yields?** Audit 002 (C3, `audit_002:79-94`) records
`DISCIPLINE` used simultaneously as a power family and as an accumulating resource pool in card
output. §1's 2026-08-06 scope amendment named this finding and placed non-engine uses of `family`
outside that section's governance, so the collision is *"acknowledged and excluded from §1's
governance, not resolved"*, closing *"It remains open"* (`audit_002:92-94`). This is the only item
here deferred **by** Ruling 002 rather than to it.

**10.11 — Which document governs the per-power audit-state field?** The audit log's per-power state
field is written by `mythos_sync.py`, and no document claims it. §7's sign-off parked the question
explicitly — *"no gap opened, no Contract 001 jurisdiction decision, nothing decided about
`mythos_sync.py:185`"* — and it has not been taken up since. Scoped to jurisdiction over the field
alone: whether an unverified power is preserved or refused sits with Ruling 001 under locked §6
row 1, and `dominant_family`'s disposition is 10.3's.

---

## Sign-off checklist

- [x] §1 Family is a grounding behavior class, not an ontology; closed-world → open-world transition — signed with the 2026-08-06 scope amendment (non-engine uses outside scope; Audit 002 C3 named and excluded from this section's governance)
- [x] §2 No catch-all assignment — `UNRESOLVED_FAMILY`, never best-guess — signed 2026-08-06 **narrow**: governs family assignment only; grounding-target fallback (`DEFAULT_TRANSPOSITIONS`) is a separate layer under Addendum A sequencing and is carried as GAP-4, not ruled here
- [x] §3 Family threshold is higher than power threshold — ecosystem vs local — signed 2026-08-06 with the mechanism amendment: inheritance flows today through profile classification (`dominant_family`, measured 7.2% mean blast radius), not through grounding, whose family fallback is Audit 001 (M1)'s dead branch; the grounding sentence is prospective, not a description of current behavior
- [x] §4 The four families are complete for one observed capability cluster only (measured) — signed 2026-08-08 with the wording correction: "LEGACY domain" replaced with "observed capability cluster" (cluster records observation, domain asserts architecture); no domain named, naming stays with §10; `One-Inch Punch` → `DISCIPLINE` and `Espionage` → `PERCEPTION` accounted for explicitly; 6/4/4/4 scoped to the 18-entry `LEGACY` subset, cluster-wide partition stated as 6/4/5/5
- [x] §5 Domain taxonomy recorded as direction, not adopted — signed 2026-08-08 with the scope amendment: "not adopted" scoped to taxonomy/naming/membership only; the domain *concept* recorded as already load-bearing in locked Ruling 001 §4 (`SURFACED`); diagram nesting retained with the "human excellence" node marked a descriptive placeholder, not an adopted domain name; audit cross-ref corrected to Part 3, Q4
- [x] §5.1 Domain isolation is a precondition for learned grounding (measured, not alarm) — signed 2026-08-08 with the caveat accepted: M2 re-cited to the 12/12 measurement across all entries rather than to the `TRANSPOSITION_MAP` comment, which is demoted to authorial-intent evidence for the `GROUNDED` block only (`logic_auditor.py:126-128`); added the finding that the locality check is evaluated against family assignments 10/30 of which are wrong, with `Reality Glitch` → `Electromagnetic Pulse` as the live example; thesis unchanged
- [x] §5.2 **No Cross-Domain Terminal Substitution** — `GROUNDING_UNAVAILABLE` is a valid terminal state — signed 2026-08-08, substance unchanged, with the M3 evidence amended: full candidate sets shown per family (18 total, 6/4/4/4) instead of one sample each; grounding-target selection stated as non-deterministic (`random.choice`); related to Regression Case 001 as a shared defect *class* only, with its 90-sets-over-200-runs variance measured and its distinct mechanism preserved. `GROUNDING_UNAVAILABLE` cross-refs verified consistent across Ruling 001 §4, §8.1 and Contract 001; GAP-4 widened to both fallback sites
- [x] §5.3 **Unresolvable Grounding Must Surface** — accepted + unresolved + reason, never silent — signed 2026-08-08, substance unchanged, with two corrections: the output-space diagram loses its `cautionary unresolved` branch (it named no state anywhere in the corpus and disagreed with Contract 001 §5's enumeration of the same stage), and enforcement is recorded as partial — I5 carries the reason, I7 carries terminality, no invariant requires the accepted set to be reported alongside the rejected set, opened as GAP-5
- [x] §5.4 **Terminal Resolution Policy, not fallback** — Option B; domain = compatibility boundary — signed 2026-08-08 as written. Consequence recorded in GAP-4 rather than here: §5.4 is the first ruling to name `Indomitable Will`, its authorization is domain-scoped, and neither fallback implementation site is domain-scoped — so neither is authorized by §5.4 and both remain debt-bearing, latent rather than active (both unreachable by any existing call path with existing data)
- [x] §6 **Provenance Does Not Determine Classification** — signed 2026-08-09, ruling unchanged, with two amendments that fix evidentiary status and scope of authority: the `Tesla → COGNITION / EMP → COGNITION` diagram is deleted with no prose substitute (it rendered an inference in the same notation as a registry value — characters carry no `family` field at all, so the top edge asserted data that does not exist), and the "semantic leakage of exactly the kind the registry exists to prevent" sentence is replaced, because it dropped the preceding sentence's hedge and restated the same unsupported inheritance claim as fact. Origin is now labelled an inference with its verified negative attached: no mechanism could have propagated a family from character to power. Added an explicit addressee — §6 is a **classification-authority** rule binding whoever assigns a family, not a runtime invariant; no code path in the character-to-power pipeline could violate it (`modality_classifier.py` holds no `family`; `TAG_POWER_MAP`, `mythos_sync.py:50`, carries none). Enforcement under non-hand-authored assignment is explicitly not ruled. No gap opened and Contract 001 not amended, per operator ruling. The section's argument is untouched and fully verified: `Electromagnetic Pulse` → `COGNITION` (`logic_auditor.py:50`) in the *non-priority* GROUNDED tier (audit 001 Part 2, `:122`, finding at `:135`), surfaced only by auditing all 30 entries rather than the eight HIGH_CONCEPT priority cases (`:92`)
- [x] §7 `dominant_family` breaks under domains — signed 2026-08-09, domain consequence unchanged, with a present-tense finding added: the expression is **already** failing pre-domains, so §7's mechanism is right and its timing understated. Recorded as a hierarchy, deliberately without any percentage — ties are structurally possible under the current registry (3 approved powers over 4 families), they occur in actual emitted profiles, the tie winner is **process-dependent** (`set()` iterates in string-hash order, randomized per process; demonstrated on fixed input with no engine and no seeded randomness — `PYTHONHASHSEED=0` → `PERCEPTION`, `PYTHONHASHSEED=1` → `COGNITION`), that value reaches persisted output (`mythos_sync.py:252` → `containment_matrix.json` → dashboard), and the suite cannot detect this axis because its assertions (`test_engine.py:383-385`) hold whichever tied family wins. Operator ruling: **no sampling methodology enters the locked text**, so no tie-rate figure is recorded here. `NATURE_TRANSFORMATION` marked a descriptive placeholder with an explicit statement that §7 mints no family name. Boundary held per operator instruction — §7 amendment only: the section records the defect and does **not** rule a remedy; no gap opened, no Contract 001 jurisdiction decision, nothing decided about `mythos_sync.py:185`
- [x] §8 Normalization contract + three-vocabulary state mapping — signed 2026-08-11; §8's substance unamended, with one scope addition to §8.1: "proposal" is declared this section's own term (a family-classification submission) carrying no authority outside it, and §8 is stated to map onto Ruling 001 §4's fusion-result vocabulary without characterizing the scope of any of its states. The collision between §8's "proposal" and locked Ruling 001 §4's `BLOCKED` row ("validation rejected the proposal") is recorded as **§10.8** — observed, not resolved — rather than folded into §8's prose as a settled reading; jurisdiction over characterizing a locked Ruling 001 row is expressly left undecided. Not filed against the gap register, whose entries close on a Contract 001 invariant — a shape this collision does not have — so no gap number is opened.
- [x] §9 Regression Case 001 — receipt of failure 2 — signed 2026-08-11, rewritten as a receipt: the section's duplicate of locked Ruling 001 §6's two-failure table is **removed rather than corrected**, because the duplicate had already drifted — its column header read *Fixed by* where the locked table reads *Governed by*, asserting a remedy where the locked text assigns jurisdiction, and claiming failure 1 fixed when no resolver exists (locked Ruling 001 §4: the tradeoff stands *"until the resolver exists"*). Also removed: the unconditional claim that normalization alone yields `GROUNDING_UNAVAILABLE`, which locked Ruling 001 §4 denies (*"Resolution alone does not determine the state"*) and which restated §5.2's relationship as mechanism after §5.2 settled it as class-only. §9 now cites Ruling 001 §6 as the record and §5.2 as the relationship, and states that Ruling 002 owns failure 2 without closing it. Section retitled to match. `docs/evidence/README.md` repointed in the same commit; `ruling_002:243`'s *"recorded in §9"* left standing in signed §5.2 and parked.
- [x] Addendum A — Domain Before Family — signed 2026-08-12 as written. Point 1 verified consistent with §5 and §5.4. Point 2 verified via §4, §6, and its own M4 citation — not via §2, §5.1, or §5.2. Point 3 verified consistent with §5.1; Points 4 and 5 verified consistent with §5.2. Diagram nodes 2–4 verified consistent with §5.1 and §5.2 jointly. Diagram node 5 (fusion compatibility) has no independent source anywhere in the corpus outside Addendum A itself; this attestation does not claim one. §2 was checked and found circular — its own domain reference at :78 cites this addendum — so it cannot corroborate the addendum it defers to. Corpus-wide sweep found no independent restatement anywhere. Whether downstream citations — Contract 001 §4 (:171), Contract 001 I2 (:205), open_contract_gaps.md:111, and locked Ruling 001 §4 (:206) — accurately paraphrase this addendum's ordering is expressly not decided here. Each cites a three-node "domain → family → grounding" compression not stated in that form in this addendum's five-node diagram or in Point 3's learned-concept-scoped wording. Characterizing another document's citation of this one, including a locked row, is outside this addendum's jurisdiction.
- [x] §10 Open questions — signed 2026-08-15, as a scoping record: §10 holds eleven items, nine of them open, with 10.2 and 10.6 standing as DISCHARGED pointers to §5.4 and §5.3, and this signature resolves none of the nine. **Scope.** §10's completeness is scoped to questions not otherwise carried; matters already carried by a signed sign-off line were considered and carried elsewhere, and this attestation does not claim §10 adjudicated them. Audit 002 was swept and five of its six findings — C1, C2, C4, C5, C6 — were not received by Ruling 002, recorded as provenance rather than adoption; Audit 002's own closure conditions are out of scope, and naming C4 does not transfer ownership of that mechanism. Drafting and process rules were ruled not to belong in Ruling 002; which instrument owns them is a separate, later decision, and this signature creates and amends no such instrument. Ruling 001 §7 items 7.1–7.7 were read, by operator ruling, as validation rather than as a gap search: a closed negative cannot generate a missing item. **Recorded as fact, not as ruling.** `ruling_002:243`'s "recorded in §9" is left standing in signed §5.2, preserved without reopening §5.2, with the park recorded at §9's sign-off (`:634`); the phrase "the registry exists to prevent" was dropped from §6 as asserting a purpose unevidenced anywhere in the corpus; §10 is this document's home for its own open questions during its own review, which `6fdc13c` recorded as outside `ruling_001:352-356`'s prohibition on deciding a document's contents from outside it, explanatory and minting no jurisdiction rule; and `3b18b90` recorded that §7's finding leaves Ruling 001 §6 untouched — a scope claim bounding that finding's reach into locked text, restated here without extending it. **Routed, not adjudicated.** Three propositions go to the gap register and none is decided by this signature: enforcement of §6's provenance rule under non-hand-authored assignment, "explicitly not ruled" (`:631`); the ecosystem-vs-local ordering's non-demonstrability in the current engine, with the two measured quantities recorded as not evidence against the ordering (`8477573`); and governed vocabulary that exists in specification without implementation. Five further propositions are recorded as outside Ruling 002, on four different bases, none of which this signature adjudicates: R15 (a document should not record another document's governed current state) and R23 (precedent applies by shared reason, not by analogical extension) are outside under M4 step 1, which settles only that they do not belong in Ruling 002, the two kept distinct as different mechanisms; R17 (gap numbering is sequential, and reserving a number for an unopened gap would itself decide to open an unruled gap) is recorded as elevated rather than flattened under M4, because it governs the gap register itself; R27 (preserve-or-refuse for an unverified power) is Ruling 001's by the locked assignment at `ruling_001:319-320` row 1 — jurisdiction settled, answer not — and reading that locked row as reaching the `UNVERIFIED` case is itself a reading of locked text, recorded as a routing basis and not as a finding §10 asserts; and R28 (whether locked Ruling 001 §5's external-dependency clause at `:254-256` reaches a test-only dependency) is a reading question about signed text that does not enter §10 merely because it is unresolved. No destination is decided for any of the five; where the worksheet names one it does so as "likely" or "natural home," which this signature does not convert into a decision. **Discharged.** `bfc8ecc` discharged the claim that `ruling_001:190-191` can authorize characterizing `BLOCKED`, and its verification condition was checked by two repository-wide sweeps, excluding `.git` and the untracked routing worksheet — the citation itself in any file type, and the phrasings in which the discharged reading was expressed ("expressly defers", "own deferral", "no dispute exists") — both returning nothing, with the only remaining line pairing `UNRESOLVED_FAMILY` with governance being §2's sign-off (`:623`), which claims nothing about Ruling 001's `BLOCKED` row; no dependence was found by those searches. §9's dropped operator-action test was fixed by the same commit that recorded it, and §9 now cites locked §6 as the record. **Not decided by this signature:** which candidate domains are adopted or what they are called (10.1); what replaces `dominant_family` (10.3); whether a new domain may ever be proposed (10.4); the order and method of reclassifying the ten mis-fitted entries (10.5); the modality placement of `Kinetic Mastery` and `Espionage` (10.7); whether the three scoped uses of "proposal" co-refer and whether Ruling 002 may characterize the scope of Ruling 001's locked `BLOCKED` row (10.8); whether the thin single-member clusters are real (10.9); which meaning of `DISCIPLINE` yields (10.10); and which document governs the per-power audit-state field (10.11). Ruling 001 is not amended, no gap number is opened, and GAP-6 remains free.

Drafted 2026-08-04. All fifteen sections signed off by the operator; marked LOCKED 2026-08-15.
Binding. A locked ruling states what is true; it does not assert that implementations already obey
it, and §10's nine open questions remain open and owned by this ruling.
