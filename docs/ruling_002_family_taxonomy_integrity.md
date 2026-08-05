# WorldCraft Ruling 002 — Family Taxonomy Integrity

**Status:** DRAFT — pending operator review and sign-off.

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

## 3. Expansion rates — why families need a higher threshold than powers

| | expands | a change is |
|---|---|---|
| **Power vocabulary** | frequently — Wood Release, Mokuton, Gravity Manipulation, Ki Projection | **local** |
| **Family vocabulary** | rarely | an **ecosystem change** |

A family changes grounding behavior for everything beneath it. **New power = local change. New
family = ecosystem change.** The admission threshold for a family is therefore *higher* than for a
power — the opposite of the usual instinct, which treats broader categories as safer because they are
vaguer.

This inverts the Ruling 001 §1 economics one level up and for a different reason: there, minting is
cheap because a redundant power is recoverable. Here, minting is expensive because a family is
inherited.

## 4. Finding — the four families are complete for the LEGACY domain only

`COGNITION` / `INFLUENCE` / `DISCIPLINE` / `PERCEPTION` were authored for the LEGACY tier rebalance.
They are **human capability families**: thinking, affecting, training/mastery, sensing.

They do not describe elemental transformation, reality alteration, supernatural manifestation, energy
systems, or biological mutation.

**Measured (audit Part 2, Q5):** all 18 LEGACY entries are honest fits, partitioning 6/4/4/4 with no
coercions and no boundary cases. **10 of 30 entries do not sit honestly in their assigned family** —
seven wrong-domain, three boundary cases. The original taxonomy is not defective; it is correct and
complete for its domain, and the failures are concentrated entirely outside it.

## 5. The domain layer

**Not adopted by this ruling. Recorded as the agreed direction, to be decided deliberately.**

The four families are **not** to be replaced. The safer evolution nests them:

```
domain
├── human excellence
│   ├── COGNITION
│   ├── INFLUENCE
│   ├── DISCIPLINE
│   └── PERCEPTION
├── (further domains — see audit Q4)
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
- **There are zero cross-family grounding edges in the registry** (audit M2). The system is not
  currently contaminated.
- **That locality is authorship, not architecture.** The `TRANSPOSITION_MAP` comment records the rule
  being applied by hand: *"Every entry now stays inside the source power's family."* **The invariant
  this ruling proposes is already being enforced manually, one layer down.** The domain layer
  generalizes an existing rule rather than imposing a new one.
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
fusion, simulated under every possible family assignment:

| assigned family | grounds to |
|---|---|
| DISCIPLINE | Adaptive Combat |
| COGNITION | The Scientific Method |
| INFLUENCE | Symbolic Authority |
| PERCEPTION | Intuitive Insight |

**The failure is not classification. The failure is that every available destination belongs to the
wrong ontology.** The entire LEGACY destination space is human excellence, so no family assignment
can produce a correct landing.

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
fusion continues                       ├── cautionary unresolved
                                       └── GROUNDING_UNAVAILABLE
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

**The evidence (audit Part 2, GROUNDED tier).** `Electromagnetic Pulse` is classified `COGNITION`.
An EMP is an energy effect, not an act of thinking. The assignment is almost certainly inherited from
Tesla, whose *character* is cognitive:

```
Tesla → COGNITION
   ↓
EMP → COGNITION
```

This is semantic leakage of exactly the kind the registry exists to prevent — *scientist creates
technology, technology inherits the scientist's cognitive family.*

**Why this finding is disproportionately important:** it proves the domain problem is **not** confined
to HIGH_CONCEPT. The boundary was already crossed in the GROUNDED tier, in an entry nobody had flagged
as suspicious. Auditing all 30 entries rather than the eight obvious ones is what surfaced it.

## 7. Consequence — `dominant_family` breaks under a domain layer

`dominant_family` is computed as `max(set(families), key=families.count)` over the approved powers.
Once powers span domains, that expression takes a plurality vote across **incommensurable
categories** — a set like `[COGNITION, NATURE_TRANSFORMATION, PERCEPTION]` yields an arbitrary winner
that characterizes nothing.

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

| Situation | Proposal | Grounding | Fusion result |
|---|---|---|---|
| Recognized or resolved, all three fields valid, grounding legal or unnecessary | accepted | n/a or resolved | **ADMITTED** |
| Resolved, but no existing family contains it | `UNRESOLVED_FAMILY` | — | **CAUTIONARY** |
| Resolved and classified, but no in-domain grounding candidate exists | accepted | `GROUNDING_UNAVAILABLE` | **`SURFACED`** — accepted and rejected components both reported, with reason (§5.3); terminal, not a degraded `ADMITTED` |
| Could not be resolved at all | unresolved | — | **BLOCKED** |

The second row is the one that matters most: the concept is *understood* but *uncategorizable*. That
must never present as the same condition as "unknown," because the operator action it calls for is
completely different — extend the taxonomy, not resolve the name.

## 9. Regression Case 001 exposes two independent failures

Hashirama Senju × William Vangeance (Ruling 001 §6) is retained permanently, and demonstrates **two
distinct defects that must stay separate in the record**:

| # | Failure | Class | Fixed by |
|---|---|---|---|
| 1 | Unknown character/power silently became GROUNDED | **normalization bug** | Ruling 001 — Invariant 1, resolve-then-proceed |
| 2 | The registry has no honest place for non-human-excellence abilities | **ontology boundary** | Ruling 002 — taxonomy extension, unresolved |

**Fixing the first does not fix the second.** With normalization alone, Hashirama resolves correctly
to Wood Release — and then, per §5.2, correctly returns `GROUNDING_UNAVAILABLE` rather than becoming
a spy. The artifact proves both layers are necessary.

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
**one confirmed domain and several candidates requiring further evidence** (audit Q4). Names are lore.

**10.2 — DISCHARGED → §5.4.** Ruled: terminal resolution *policy*, not terminal fallback. Some
domains terminate with refusal (Option B); artificial bridge concepts are rejected.

**10.3 — What replaces `dominant_family` as disposition.** §7.

**10.4 — Who may propose a family or domain.** Operator-authored only, or model-proposed under a
stricter audit than powers receive. §3 argues the threshold must be higher than for powers either way.

**10.5 — Reclassification of the ten mis-fitted entries.** The audit identifies them; it does not
reclassify them. Order and method are open, and `Electromagnetic Pulse` (§6) is the priority case
because it sits in the tier nobody was watching.

**10.6 — DISCHARGED → §5.3.** Ruled: unresolvable grounding must surface. Fusion output preserves
accepted powers, unresolved powers, and the reason for exclusion; `GROUNDING_UNAVAILABLE` is a valid
ontology state rather than an error.

**10.7 — Modality placement of `Kinetic Mastery` and `Espionage`.** Both are marked GROUNDED under
"the body exceeds ordinary human limits," yet real spies exist and the one-inch punch is documented.
A modality question, not a family one; logged so it is not lost.

---

## Sign-off checklist

- [ ] §1 Family is a grounding behavior class, not an ontology; closed-world → open-world transition
- [ ] §2 No catch-all assignment — `UNRESOLVED_FAMILY`, never best-guess
- [ ] §3 Family threshold is higher than power threshold — ecosystem vs local
- [ ] §4 The four families are complete for the LEGACY domain only (measured)
- [ ] §5 Domain layer recorded as direction, not adopted
- [ ] §5.1 Domain isolation is a precondition for learned grounding (measured, not alarm)
- [ ] §5.2 **No Cross-Domain Terminal Substitution** — `GROUNDING_UNAVAILABLE` is a valid terminal state
- [ ] §5.3 **Unresolvable Grounding Must Surface** — accepted + unresolved + reason, never silent
- [ ] §5.4 **Terminal Resolution Policy, not fallback** — Option B; domain = compatibility boundary
- [ ] §6 **Provenance Does Not Determine Classification**
- [ ] §7 `dominant_family` breaks under domains
- [ ] §8 Normalization contract + three-vocabulary state mapping
- [ ] §9 Regression Case 001 demonstrates two independent failures
- [ ] Addendum A — Domain Before Family
- [ ] §10 Open questions

Drafted 2026-08-04. Not binding until signed off and marked LOCKED.
