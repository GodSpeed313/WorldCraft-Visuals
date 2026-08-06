# WorldCraft Audit 002 — Character Corpus, Output Structure

**Status:** OPEN — evidence collection in progress. This document records measurements only.
It contains no rulings and asserts no lore. Findings marked `(C#)` are observations about
existing artifacts, not decisions about them.

**Why it exists.** Ruling 001 and Ruling 002 govern how concepts *enter* the system. Nothing
governs the *shape of what comes out*. A fusion output has no defined structure anywhere in the
governing documents — not the field set, not the ability count, not whether a resource mechanic is
required. Deriving that structure from an operator-authored corpus follows the sequencing rule
established during Audit 001: **inspect, identify clusters, measure contradictions, derive
candidates, then name.** The alternative is inventing a schema and forcing existing work into it.

## Sample boundary — read before using any finding here

This audit is **incomplete by construction**. Audit 001 examined all 30 registry entries and could
therefore make exhaustive claims. This one cannot yet.

| | Count | Source |
|---|---|---|
| Finished character cards examined | 3 | Cenotaph Veyl, Gunslinger, Astra Mashenclad |
| Named locations observed | 3 | Aeralith Ascend…, Auralith Expanse, Pneumachora |
| Orphan abilities observed | 1 | Writstorm Mantle |
| Corpus files inspected | 90 filenames, ~12 WorldCraft-relevant | local download slice |
| Full corpus size | **unknown — not inspected** | operator's Midjourney library |

**No finding below may be stated as exhaustive.** Counts are floors, not totals. The full library
has not been enumerated, and the three cards were the three that happened to be downloaded locally.

---

## (C1) A stable output schema exists across all three cards

Nine elements are present on every card examined:

1. Name
2. Epithet
3. Creator mark (`NU ERA SENJU` — the operator's Midjourney handle, **not** a universe identifier)
4. Portrait with an art-direction caption
5. A first-person governing quote
6. Exactly five abilities
7. One emphasized terminal ability
8. A three-segment resource bar with a one-line governing law
9. `WORLDCRAFT · DNA-SPLICED` footer

The terminal ability is emphasized *visually* on two cards and *labeled* `FINISHER` on the third.
**The concept is stable where the encoding is not.**

### Divergences across the same three cards

| Element | Veyl | Gunslinger | Astra |
|---|---|---|---|
| Ability ordering | `01`–`05` | `01`–`05` | glyphs, unordered |
| Passive count | 1 | 1 | 2 |
| `ROLE` field | absent | absent | present (`Petitioner`) |
| Combat-style block | absent | absent | present |
| Personality prose | absent | absent | present |
| `POWER` / `DEFENSE` stats | present, **blank** | present, **blank** | absent |
| Relationship field | absent | absent | present (`YOUNGER BROTHER`) |

**A field that is present and never populated is an undecided field, not an empty one.**
`POWER` / `DEFENSE` appear on two of three cards and carry no value on either.

## (C2) Three structurally different resource mechanics are rendered identically

All three cards display a three-segment bar. The bars do not represent the same kind of thing.

| Character | Bar | Structure |
|---|---|---|
| Cenotaph Veyl | `VAPOR → ASH → MOLTEN` | **progression ladder** — one axis, rising intensity |
| Astra Mashenclad | `OBSERVED → WRITTEN → CLOSED` | **state sequence** — phases of a commit, not intensities |
| Gunslinger | `DISCIPLINE ←→ SHOWMANSHIP` | **bipolar tradeoff** — two poles, spending one gains the other |

This is the same failure shape as Audit 001's Cursed Energy observation: a shared visual
presentation concealing distinct underlying kinds. An engine generating these must know which of
the three it is producing, because their rules differ. **Not a defect in the cards** — each reads
correctly on its own. It is a modelling requirement.

## (C3) `DISCIPLINE` is used simultaneously as a power family and as a resource pool

`POWER_FAMILIES` is exactly `COGNITION`, `INFLUENCE`, `DISCIPLINE`, `PERCEPTION`. Ruling 002
establishes that `family` is a **grounding behavior class**, not a quantity.

The Gunslinger card uses `DISCIPLINE` as an accumulating meter: *"Creed Unbroken — every called
shot that lands builds Discipline."*

One token, two incompatible meanings across the ontology layer and the output layer. This is the
mechanism Ruling 002 §6 names, observed in finished operator-authored work rather than in
hypothetical input. **Recorded as a collision requiring resolution; this audit does not propose
which meaning yields.**

**Cross-reference, 2026-08-06.** Ruling 002 §1 has been scope-amended to state that non-engine uses
of `family` exist outside its scope and names this finding explicitly. The collision is therefore
*acknowledged and excluded from §1's governance*, not resolved. It remains open.

## (C4) At least one ability is defined relative to another entity

*"Little Brother's Gravity — Certainty degrades around him. Anyone reading outcomes — his brother
included — gets a blurred page where he's standing."*

The Gunslinger's kit is built on reading outcomes in advance (`Deadline`, and the governing quote
*"Every fight has already been decided. I'm just the first one to see how."*). Astra's passive
degrades precisely that capability and names him as an affected party.

**Consequences measured:**

- The ability **cannot be validated standalone.** Every governing document to date models a fusion
  result as a self-contained profile. This one is not.
- **The relationship cannot be derived.** The brothers share no surname; nothing in either
  identifier indicates a sibling edge. It exists only as an explicit operator-authored fact. This
  parallels Audit 001 (M4): as with domain, the relationship **must be stored, not inferred**.
- Ruling 001 §3.3 defines a relationship graph for **concepts** (canonical / aliases / derivatives
  / related). No equivalent structure exists for **entities**.

## (C5) First observed homonym case — a proper name colliding with a generic term

`Gunslinger` is the older brother's name, not an archetype label (operator statement, 2026-08-06).
The same token is a generic descriptor in general usage.

Under Ruling 001 §3.2(a) the two readings fail semantic identity and must not be merged. The case
is notable because it is **not** a vocabulary gap: a system holding both meanings knows each of
them, and the open question is which one an input intends. That is the epistemic shape Contract 001
names `AMBIGUOUS` — *know what it could be, not which wins* — rather than `UNRESOLVED`.

Recorded as the first observed instance of this class. Expected to generalize once vocabulary is
learned rather than authored.

## (C6) Abilities exist outside the characters that carry them

`Writstorm Mantle` appears in the corpus as a Cenotaph Veyl ability with generated art. It is on no
card. The ability set visible on a card is therefore **a selection, not an inventory.**

---

## Worked application — not a finding

`Aeralith Ascend…` (a vast vertical city-world) and `Auralith Expanse` (a desert plain of obelisks)
differ by one vowel. Name similarity alone tempts a merge; Ruling 001 §3.2(a) asks whether they are
the same *phenomenon*, and a vertical city and a desert expanse are not. **The policy resolves the
case against the merge in a single step, without recourse to the operator.**

Recorded here as evidence that Ruling 001 §3 is operative on real data, not as a decision about
either location. Whether they are related places, a rename, or unrelated remains lore and is the
operator's to state.

---

## Open — required before this audit can close

1. Enumerate the full corpus. Current sample is a local download slice of unknown proportion.
2. Determine whether the five-ability count is a rule or an artifact of three examples.
3. Determine which fields are required, optional, or undecided (`POWER` / `DEFENSE`).
4. Establish whether every character carries a resource mechanic, and which of the three kinds.
5. Measure how much corpus vocabulary falls outside the 30-entry `POWER_REGISTRY`.
6. Identify further cross-entity abilities beyond (C4).

Opened 2026-08-06.
