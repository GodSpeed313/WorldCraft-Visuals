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
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-22 15:04 EDT
```

Statement: *"I confirm CR-002 correctly identifies four findings arising from Beat 1's citation
audit of Contract 001 §7: (1) Row 2's 'meaning of a category' gloss is a fidelity defect against
Ruling 002 §3's actual inheritance-based grounding; (2) Row 3's reduction of I3 to its title
sentence is not a complete representation of the invariant, given §6's own signed record that I3 is
not reducible to that sentence; (3) the synthesis sentence at :248 is asymmetrically supported — the
false-certainty half is sound, the incompleteness half is not uniformly sourced across all three
rows; and (4) the :245/:248 boundary is confirmed, and reserved, as Beat 2's jurisdiction question,
stated as: can a normative synthesis over an observational proposition create a new normative
condition about an excluded subject? This acknowledgment does not resolve that question, does not
authorize any edit to §7's text, and does not affect §7's unsigned status."*

---

## CR-003

```
Target:            Contract 001 §7, :248 — the synthesis sentence.
                   UNSIGNED at time of recording.
Recorded:          2026-08-23
Defect class:      jurisdictional — an excluded topic appearing as a
                   normative condition, contrary to §1's self-test (:41-42)
Basis commit:      55b55d0 (origin/main; audited against origin/main blobs)
Prior record:      CR-002 (2026-08-22) reserved this question as "Beat 2"
                   and gave no answer. This entry answers it.
Authorizes:        no edit to contract_001_domain_resolution.md
Status:            recorded; §7 remains unsigned
```

**Scope note.** This entry records a defect and the reasoning establishing it. It authorizes no
edit to §7, closes no gap, and does **not** decide what §7's text should say instead. Like CR-002
it records a finding in *unsigned* text, so it corrects no attestation.

**Text stability.** §7 (`:237-248`) is byte-identical to its state at `545d846`, §1's signing
commit, and has never been amended. Every `:NNN` reference below resolves identically at
`545d846`, `bc1b8d3`, and `55b55d0`.

### The question, as reserved

CR-002 ruling 4 stated it: *Can a normative synthesis over an observational proposition create a
new normative condition about an excluded subject?*

**Answer: yes, and at `:248` it does.**

### The test, element by element

§1's self-test (`:41-42`): *"Anything from the left-hand column — a topic this contract has
excluded — appearing as a **normative condition** anywhere in this contract is a defect in this
contract."*

**(a) A topic from the left-hand column.** `:39` excludes *registry expansion rules → Ruling 002
§3, §8*. §1's own signature (`:265`) fixes §3's share of that exclusion: *"§3 the family admission
threshold."* §7's row 2 (`:245`) names exactly that — *"family threshold higher than power
threshold."* Element satisfied.

**(b) Appearing as a normative condition.** The contested element. Addressed below.

**(c) Anywhere in this contract.** `:41-42` says *anywhere*; `:50` binds V1 and V2 across §1
through §8. No provision anywhere in the contract exempts narrative, summary, or pattern-recording
sections from either. §7 is in scope without qualification.

### Why `:245` passes and `:248` fails — the quantifier

Beat 1 established that `:245` is observational and survives the test. That holds: a table cell
reporting what another document's rule *is* states no condition of this contract.

`:248` — *"In each case the system is permitted to be incomplete but never permitted to be falsely
certain"* — is deontic in form, and its grammatical subject is **the system**, not the three cited
rules. It does not report that each rule has a shared shape; it states what the system may and may
not do. *"In each case"* is not naming sources. It distributes the predicate onto each of the three
rows individually, and one of those rows is the family admission threshold. Unpacked at row 2, the
sentence reads: *with respect to family admission, the system is permitted to be incomplete but
never permitted to be falsely certain.* That is a first-order normative claim about how family
admission must behave, stated by a document that excludes family admission at `:39`.

**The defect localizes in the quantifier**, not in the deontic vocabulary and not in the table.

### The control case — I6

I6 (`:230-232`) is deontic, names the same three documents (*"across 001, 002 and this contract"*),
and is **signed** via §6 on 2026-08-21 (`:271`). It does not trip `:41-42`, and the difference is
precisely the one identified above: I6's normative subject is the epistemic distinction itself — a
topic inside this contract's remit per `:22-27`. 001 and 002 appear in I6 as *where the pattern was
observed*, not as subjects the sentence binds.

I6 therefore establishes that cross-document pattern language is not itself the defect. What
distinguishes `:248` is that its quantifier binds the norm to an enumerated excluded case.

### The evidentiary limb — Beat 1 finding 1

Finding 1 (`corrections.md:100`) is the only one of Beat 1's four findings that can support this
ruling, because it is the only one showing **divergence on the excluded row specifically**, rather
than absence of support on a non-excluded row.

Its verbatim terms: *"Rule cell faithful; the 'what is preserved' cell ('the meaning of a
category') is §7's own gloss — the source grounds the threshold in **inheritance** (classification
today, grounding prospectively, per the 2026-08-06 amendment), not in 'meaning.'"* Verified against
the source at `ruling_002_family_taxonomy_integrity.md:103-108`. Ruled a fidelity defect by the
operator on 2026-08-22 (CR-002 ruling 1).

The consequence for jurisdiction: when `:248` distributes its norm over row 2, it distributes over
**§7's own divergent characterization of the excluded topic**, not over what Ruling 002 §3 states.
The contract is therefore not reporting the owner's norm. It is norming its own gloss of a subject
it excluded — origination, not restatement.

**On finding 1's PARTIALLY SUPPORTED classification.** Recorded explicitly so a later reader need
not re-derive that the divergence claim survives the qualifier. PARTIALLY SUPPORTED is the more
precise fact pattern for this ruling than NOT SUPPORTED would have been, not a weaker one. It
records that §7's row 2 *did* connect to Ruling 002 §3 — its rule cell is faithful — but connected
its "what is preserved" cell through a paraphrase rather than the source's own terms. Mere absence
of support would leave a use/mention defense open: an unrepeated but accurate mention. Divergence
forecloses it. A source's proposition cannot be inaccurately mentioned and still be mention; the
inaccuracy is the document's own contribution, which makes it assertion by construction.

### The counter-reading, and why it does not hold

The available defense is that §7 is second-order reporting — `:239` frames the section as
*"recording the pattern"* — supported by the V1 precedent at `:79`, where a domain name appears
inside the fence opened at `:76` and §2's signature (`:266`) records it as *"a counter-example, not
a live predicate."*

The precedent does not reach `:248`. At `:79` the fence is labeled *"Invalid, and the canonical
example of the failure"* (`:76`), and that frame is what converts mention into non-assertion.
`:248` carries no such frame: it is the contract's summary prose, stated flatly in its own voice,
in a document whose self-test reaches *anywhere* (`:41-42`) and whose validity constraints reach
§1 through §8 (`:50`). The mechanism that rescues `:79` is absent here.

### Beat 1 finding 3 — recorded as row-1-scoped and NOT load-bearing

Finding 3 (`corrections.md:102`) does **not** support this ruling, and is recorded here to prevent
a later reader from enlisting it.

Its verbatim terms: *"'Permitted to be incomplete' holds for rows 2-3 but not row 1, which licenses
redundancy/noise (over-completeness), not incompleteness."* The unsourced half therefore attaches
to **row 1 — Ruling 001 §1, concept identity** — verified independently at
`ruling_001_canonicalization_policy.md:31`, *"The system prefers a slightly noisy ontology over a
falsely unified one"*: noise is over-completeness. For **row 2** the incompleteness half **is**
sourced — a higher admission bar leaves the taxonomy incomplete rather than admitting a family on
weak evidence.

Row 1's subject is not excluded. §1's exclusion table (`:33-39`) names Ruling 001 **§5** at `:35`
(provider choice) and nowhere names Ruling 001 §1. An unsourced normative claim on row 1 is
therefore a citation-fidelity defect with no jurisdictional dimension.

**Direction of dependence between sourcing and jurisdiction.** Curing a sourcing defect does not
cure a jurisdiction defect: a perfectly-sourced normative condition about an excluded topic still
trips `:41-42`. The converse — that a sourcing failure can be *evidence* of a jurisdiction
violation — is valid, and is the reasoning this entry uses, but it runs through finding 1's
divergence, not finding 3's absence.

**Consequence for CR-002 ruling 3.** That ruling preserved the possibility of a *surgical*
correction addressing only the unsupported half of `:248`. Such a repair would not reach this
defect. Both halves are deontic and both are distributed by the same quantifier over row 2.

### `:272` is not clearance

§7's checklist row (`:272`) asserts that §7 *"cites Ruling 002 §3's threshold observationally to
build the cross-ruling pattern; does not assert ownership or restate it as a binding condition of
this contract."* That qualifier was added by `2dac6ff` — the same commit that corrected §1's
self-test — and §1's signature then expressly declined to adjudicate it: *"§7's observational
citation of Ruling 002 §3 is recorded on §7's own line and not adjudicated here"* (`:265`).

It is a proposition placed on the record by §1's work and attested by no signature. It is also the
proposition this entry tests. §7's eventual signature may not cite `:272` as support; doing so
would be the row clearing itself.

Also recorded: §1's signature states the corrected self-test *"was then run against this document
and returns nothing."* That run is not evidence against this finding. It is expressly qualified by
the carve-out above, and the record shows it considered §7's *citation* — table-cell-shaped,
singular — with no indication `:248` was examined separately.

### Not decided by this entry

- What `:248` should say. No repair is authorized, proposed, or implied.
- Whether the same analysis reaches `:246` (row 3, this contract's own I3) or any other row. Only
  row 2's subject is on `:39`; other rows were not tested for jurisdiction.
- The "one idea" / "two principles" / "inversion" reconciliation, parked by CR-002 and still
  parked. This entry's use of I6 concerns the *scope of I6's normative subject* only, and takes no
  position on whether I6's "two principles" and §7's "one idea" describe the same recurrence.
- §7's signability. §7 remains unsigned; this entry records what a signature would have to
  confront.

### Recording note

Four anchor errors were caught during drafting and verification and are recorded rather than silently dropped,
this file existing to record exactly this defect class.

1. The session analysis cited provider choice at `:36`. It is `:35`; `:36` is *prompts*. Analyst
   error, corrected before drafting.
2. A review remark characterized the exclusion table as naming Ruling 001 §5 for "provider choice,
   caching." The table does not bundle these: provider choice is `:35` → Ruling 001 §5; caching,
   storage strategy is `:38` → *unassigned — tracked as GAP-6*. The conclusion drawn from the
   remark — that Ruling 001 §1 is nowhere excluded — is unaffected and independently verified
   against `:33-39`.
3. The phrase *"partially supported, interpretive gloss replacing the source's mechanism claim"*
   was attributed in review to Beat 1. It appears nowhere in this corpus. Finding 1's actual text
   is quoted verbatim above from `corrections.md:100`.

4. The draft of this entry cited `ruling_001_canonicalization_policy.md:29` for *"The system
   prefers a slightly noisy ontology over a falsely unified one."* That line is `:31`; `:29` is
   *"Never merge on name similarity alone."* Analyst error, caught by the post-drafting anchor
   sweep of this entry's own citations, before commit. The proposition it supports — that Ruling
   001 §1 licenses over-completeness, not incompleteness — is unchanged and verified at `:31`.

None of the four alters the ruling.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-23 19:06 EDT
```

Statement: *"CR-003 stands as filed. The jurisdiction violation at `:248` is confirmed; finding 1
is the evidentiary limb, with the PARTIALLY SUPPORTED qualifier addressed on the record; finding 3
is correctly scoped to row 1 and is non-load-bearing for jurisdiction; `:272` is rejected as
clearance. `:246`/row 3 is explicitly left untested and unbounded by this ruling. This
acknowledgment authorizes no edit to §7's text and does not affect §7's unsigned status."*
