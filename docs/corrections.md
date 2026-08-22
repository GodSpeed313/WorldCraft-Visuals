# Corrections

This file records defects discovered in already-signed corpus text. It does not amend, reopen, or
retroactively alter any signature. A signed row remains exactly what was attested on its signing
date; this file records what was later found wrong about it.

**What this file is not.** It is not a section or appendix of Contract 001, and it is not part of
the gap register (`open_contract_gaps.md`). A gap entry closes when a contract carries a new
invariant; a correction entry records a defect in text that is already signed, and closes nothing.
The two instruments answer different questions and neither substitutes for the other.

**Standing rule.** No entry in this file authorizes editing the text it describes. The corrected
reference lives here, beside the defect, and the signed text stays as attested.

---

## CR-001

```
Target:            Contract 001 §1, :273
Signed:            2026-08-16 (545d846)
Defect:            citation cites the wrong line for its stated source
Correct reference: ruling_001_canonicalization_policy.md:243
Classification:    factual/referential defect — the underlying proposition
                   ("Ruling 001 §5 owns provider choice") is unchanged;
                   only the line number is wrong.
Basis:             The corrected reference does not alter what §1 asserts —
                   only which line supports it.
Evidence:          ruling_001 locked at aa50070, 2026-08-06; unchanged since.
                   At 545d846 (§1's signing commit), ruling_001:243 already
                   read "Scope of this section — operator ruling, 2026-08-06.
                   §5 owns the provider authority boundary"; ruling_001:273
                   read "The core engine must know nothing about Anthropic" —
                   unrelated. Both lines confirmed unchanged in ruling_001
                   today. contract_001 was 263 lines at signing, so :273
                   could never have been a same-document reference either.
                   As of this recording contract_001 is 275 lines, so :273
                   now resolves within contract_001 to the §8 sign-off row —
                   a false same-document hit that did not exist at signing.
Effect:            None on §1's substantive proposition. §1's signed text
                   (:265) is untouched and remains exactly as attested.
Recorded:          2026-08-21
Historical status: §1 remains signed as of 2026-08-16, defect and all.
                   This record does not retroactively alter that signature.
```

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-21 17:41 EDT
```

Statement: *"I confirm CR-001 correctly identifies a referential defect, not a substantive one —
it changes no proposition §1 asserts, only which line supports it. §1's signature is unaffected."*

---

## CR-002

```
Target:            Contract 001 §7 "The conservative principle at three
                   levels", :237-248 — UNSIGNED at time of recording
Recorded:          2026-08-22
Defect class:      batch — citation fidelity across three cited rows and
                   one synthesis sentence
Basis commit:      bc1b8d3 (origin/main; audited against origin/main blobs)
Authorizes:        no edit to contract_001_domain_resolution.md
Status:            recorded; §7 remains unsigned
```

**Scope note.** This entry records findings and rulings on those findings. It does not resolve §7's
jurisdiction question (see *Beat 2 reserved*), and it authorizes no edit to §7's text. Findings are
separated by which pass produced them, so the record does not attribute later adjudication to
Beat 1 itself.

**Why this entry differs from CR-001.** CR-001 records a defect in *signed* text. §7 is unsigned, so
nothing here corrects an attestation; this entry records what a sign-off audit found *before*
signature, and preserves the separation between the audit's findings and the operator's rulings on
them.

### Beat 1 established — citation existence and fidelity

All three of §7's cited sources exist, sit where §7 says, and are signed/binding:

| Cited row | Source | Status |
|---|---|---|
| Row 1 | `ruling_001_canonicalization_policy.md:21-33` (§1) | LOCKED 2026-08-06 (`ruling_001_canonicalization_policy.md:3`) |
| Row 2 | `ruling_002_family_taxonomy_integrity.md:89-112` (§3) | LOCKED 2026-08-15 (`ruling_002_family_taxonomy_integrity.md:3`); §3 signed 2026-08-06 with the mechanism amendment (`ruling_002_family_taxonomy_integrity.md:624`) |
| Row 3 | `contract_001_domain_resolution.md:221-222` (I3) | line numbers verified exact; signed via §6, 2026-08-21 (`:271`) |

**No citation is fabricated or misattributed.** No CR-001-class referential defect was found in §7.

### Per-row / per-sentence findings, as originally rendered

| Item | Beat 1 verdict | Basis |
|---|---|---|
| Row 1 (001 §1, `:244`) | SUPPORTED | Verbatim rule; "what is preserved" corroborated by source text directly. |
| Row 2 (002 §3, `:245`) | PARTIALLY SUPPORTED | Rule cell faithful; the "what is preserved" cell ("the meaning of a category") is §7's own gloss — the source grounds the threshold in **inheritance** (classification today, grounding prospectively, per the 2026-08-06 amendment), not in "meaning." |
| Row 3 (I3, `:246`) | PARTIALLY SUPPORTED | Rule cell reproduces only I3's title sentence; §6's own signature (`:271`) states I3 "is not reducible to its first sentence" and identifies the prohibition clause as operative. |
| Synthesis (`:248`) | PARTIALLY SUPPORTED | "Never permitted to be falsely certain" holds for all three rows. "Permitted to be incomplete" holds for rows 2-3 but not row 1, which licenses redundancy/noise (over-completeness), not incompleteness. |

Beat 1 also located, **without resolving**, a structural boundary: the table cell at `:245` is
observational and survives §1's self-test (`:41-42`) against the registry-expansion-rules exclusion
(`:39`); the synthesis sentence at `:248` is normative in form and quantifies over that same row.

### Kevin review adjudicates — 2026-08-22, conversational ruling

Four questions were put to review as a batch, following Beat 1. Rulings:

1. **Row 2 gloss — ACCEPTED as a fidelity defect.** "The meaning of a category" is not what the cited
   source establishes; the source's own ground is inheritance/classification. This ruling does not
   extend the finding beyond what Beat 1 already supports.

2. **Row 3 — SEVERITY UPGRADED**, from Beat 1's PARTIALLY SUPPORTED to **NOT SUPPORTED AS A COMPLETE
   REPRESENTATION OF I3**. This upgrade is a post-Beat-1 adjudication, not a Beat 1 conclusion, and is
   recorded as such: Beat 1 found the row incomplete; this ruling additionally finds the
   incompleteness **disqualifying**, because §6's own signed record (`:271`) has already rejected
   reduction to I3's title sentence as a legitimate representation of the invariant. The ruling does
   not yet decide what §7's row should say — only that it does not currently say enough. **No repair
   is authorized by this ruling.**

3. **Synthesis sentence — ACCEPTED as asymmetrically supported.** The sentence is not globally false;
   its two propositions (false-certainty prohibited / incompleteness permitted) carry unequal
   evidentiary weight across the three rows. This distinction is preserved because any eventual
   correction may be **surgical** — addressing only the unsupported half — rather than requiring
   wholesale rewrite.

4. **`:245`/`:248` boundary — CONFIRMED as Beat 2's jurisdiction question, unresolved.** Stated form:
   *Can a normative synthesis over an observational proposition create a new normative condition about
   an excluded subject?* `:245` passing §1's self-test does not settle `:248`. Beat 2 will address
   this directly; **no answer is given here.**

### Beat 2 reserved — not yet undertaken

The jurisdiction question at ruling 4 above. To be taken up only after this record is committed, and
separately from the "one idea" reconciliation issue below.

### Parked — not counted among the four findings; not a citation defect

**"One idea" / "two principles" / "inversion, for a different reason."** Three descriptions of the
same cross-document recurrence, at possibly different levels of abstraction:

- `ruling_002_family_taxonomy_integrity.md:110-112` frames the 001-§1 / 002-§3 relationship as an
  **inversion**, *"and for a different reason."*
- `contract_001_domain_resolution.md:239` (§7) frames the same span as **"one idea."**
- `contract_001_domain_resolution.md:230-232` (I6) frames the recurrence across 001, 002 and this
  contract as **"two principles."**

Not treated as contradictory on its face — they could be compatible descriptions at different
abstraction levels — but §7 has not established that they are, and has no standing license to
collapse them into "one idea" absent that showing. Labeled **unresolved conceptual reconciliation**,
preserved for possible future relevance, **not adjudicated here.**

### Recording note

Two anchors in the entry as first drafted cited `:270` for §6's signature. §6's signature is at
`:271`; `:270` is §5's row and does not contain the quoted text. Corrected at filing, before this
entry was committed. Recorded here rather than silently amended, because this file exists to record
exactly this defect class.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than what
a Contract 001 row receives.

```
Acknowledged (operator):
Acknowledged at:
```

Statement: *pending operator acknowledgment.*
