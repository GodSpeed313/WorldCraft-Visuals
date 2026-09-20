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

---

## CR-004

```
Target:            Contract 001 §8, :258-259 — the Ruling 002 §1.1 citation.
                   UNSIGNED at time of recording.
Recorded:          2026-08-23
Defect class:      citation fidelity — the citing text carries a valence the
                   cited source expressly declines
Basis commit:      11efeab (origin/main; audited against origin/main blobs)
Authorizes:        no edit to contract_001_domain_resolution.md
Status:            recorded; §8 remains unsigned
```

**Scope note.** This entry records **one** finding, from a four-check audit of §8. The audit's other
finding — that §8's normative requirement at `:252-254` is unclassified, unscoped and untestable — is
**not recorded here.** It is filed as **GAP-8** in `open_contract_gaps.md`, because it closes when
Contract 001 gains text, and this file's own definition (`corrections.md:9`) is that a correction
entry *"closes nothing."* The two findings are different species and are deliberately not merged.

**Text stability.** §8 (`:250-259`) is byte-identical to its state at `545d846` and has never been
amended. Line references resolve identically at `545d846`, `bc1b8d3`, `55b55d0` and `11efeab`.

### Citation existence — clean

§8 makes exactly one citation. Ruling 002 §1.1 exists at
`ruling_002_family_taxonomy_integrity.md:40`, titled *"The transition this ruling actually governs"*;
LOCKED 2026-08-15, §1 signed at `ruling_002_family_taxonomy_integrity.md:622`. **No CR-001-class
referential defect.** The line numbers are right and the section says something on the subject.

### Three fidelity items, one of which is the finding

| Item | Verdict | Basis |
|---|---|---|
| *"assumption"* vs *"model"* | recorded, not a finding | `ruling_002_family_taxonomy_integrity.md:42` says *"It was a closed-world **model**."* The word *assumption* appears nowhere in §1.1; ruling_002's only use is at `ruling_002_family_taxonomy_integrity.md:278`, on an unrelated subject. §8's word choice, carrying no change in substance. |
| *"the thing WorldCraft is leaving behind"* | recorded, not a finding | *leaving behind* appears nowhere in ruling_002. §1.1's own framing is *"WorldCraft is becoming an open-world model"* (`:47`) and *"the domain layer is the boundary between those two realities"* (`:48-49`). Becoming open-world from a closed-world starting point entails leaving it behind. Faithful paraphrase. |
| **The valence** | **PARTIALLY SUPPORTED** | See below. |

**The finding.** §1.1 opens: *"The original LEGACY design was **not wrong.** It was a closed-world
model"* (`ruling_002_family_taxonomy_integrity.md:42`). It closes: every invariant *"exists to make
that transition safe **rather than to repair a defect**"* (`:48-49`). §1.1 twice, deliberately,
refuses to treat the closed-world model as an error.

§8 deploys it as one. At `:257-259` a contract that could not be extended without a rewrite *"would
reproduce, at the level of the state machine, exactly the closed-world assumption Ruling 002 §1.1
identifies as the thing WorldCraft is leaving behind"* — the closed-world assumption appearing purely
as the bad outcome to be avoided, with §1.1 named as the source of that characterization.

**§8's proposition is defensible on the merits.** Reproducing a closed-world assumption *in an
open-world context* is a real error even where the closed-world model was correct for its own world.
But §8 does not say that. It attributes the negative valence to §1.1, and §1.1 declines to supply it.

**Class.** The same shape as CR-002 finding 1 — the citing text's gloss differs from the cited
source's own ground — and milder in degree. Finding 1 substituted a **different ground**
(*"the meaning of a category"* for inheritance). This **adds a valence the source disclaims** while
leaving the underlying proposition intact.

**Not a defect: the level shift.** §1.1's subject is the LEGACY family taxonomy; §8's is the state
machine. §8 flags the analogy itself — *"at the level of the state machine"* — so the shift is
disclosed, not smuggled.

### Not decided by this entry

- What `:258-259` should say. No repair is authorized, proposed, or implied.
- Whether §8 is signable, and on what terms. §8 remains unsigned.
- GAP-8's classification question, which is filed separately and is not a defect in what §8 says.
- Whether the two prior items in the table above should be corrected. They are recorded as accurate
  or immaterial, not as pending.

### Recording note

A methodology finding arose during this audit and is **not** recorded here, because this file records
defects in corpus text and that finding is about how sweeps are run: a phrase split by a blockquote
line-wrap is invisible to line-based `grep`, which nearly caused a term collision at
`contract_001_domain_resolution.md:253` to be missed. It is filed as **M2** in `docs/audit_method.md`.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-23 19:41 EDT
```

Statement: *"CR-004 is acknowledged. §8's citation of Ruling 002 §1.1 carries a valence the source
expressly declines: §1.1 states that the original LEGACY design was not wrong, and that the
invariants exist to make the transition safe rather than to repair a defect. The finding is a
fidelity defect of the same class as CR-002 finding 1 and milder in degree — it adds a valence
rather than substituting a ground — and §8's underlying proposition is left intact. Recording the
other two fidelity items as not findings is correct. The §8 audit's classification finding is
deliberately not recorded here; it is GAP-8, because it closes and a correction entry closes
nothing. This acknowledgment authorizes no edit to §8's text and does not affect §8's unsigned
status."*

---

## CR-005

```
Target:            AUTH-001's "Known consequence, recorded not addressed"
                   clause, authorizations.md:126-129 — ACKNOWLEDGED, not
                   signed, at time of recording
Recorded:          2026-08-23
Defect class:      incomplete enumeration — the clause names two entries
                   whose quotations its own disposition governs, and there
                   are three
Basis commit:      c0f7ec7 (origin/main), the commit that exercised AUTH-001
                   and made the quotations historical
Authorizes:        no edit to authorizations.md, and no edit to CR-004
Status:            recorded; AUTH-001 remains exercised and unamended
```

**Scope note.** This entry records a defect in AUTH-001's text. It does **not** correct CR-004, whose
status changed without CR-004 becoming wrong, and it does **not** extend AUTH-001's authorization by
so much as one line. AUTH-001 was bounded to `:245`, `:246` and `:248` of
`contract_001_domain_resolution.md` and to specific wording at each; nothing here alters that, and
AUTH-001 is now exercised and spent.

**Why this targets AUTH-001 and not CR-004.** CR-004 is not defective. Its quotation of the
pre-amendment wording was accurate when recorded and is now historical, which is the ordinary fate of
a quotation in this corpus and requires no correction. AUTH-001's clause, by contrast, states
something that was already incomplete when written. The defective text is the one that gets the
entry.

### The defect

AUTH-001's known-consequence clause (`authorizations.md:126-129`) reads, in relevant part:

> *"CR-002 and CR-003 quote `:245`, `:246`, and `:248` as they read **before** these edits. Those
> quotations become historical on the authorized commit. Both entries are true as of their recording
> dates and are left as recorded…"*

**Three entries quote the pre-amendment wording, not two.** CR-004 does so at `corrections.md:445`,
quoting *"the meaning of a category"* while comparing its own finding to CR-002 finding 1. The clause
names CR-002 and CR-003 only, and its phrase *"Both entries"* forecloses a third by its own wording.

**Timing.** AUTH-001 was granted and acknowledged on 2026-08-23 (`11efeab`). CR-004 was filed later
the same day (`06e707b`). The enumeration was therefore complete when written and became incomplete
before AUTH-001 was exercised, with nothing in the corpus recording the change.

### Effect — none on the disposition, only on the enumeration

The clause's **substance** reaches CR-004 unchanged: a quotation is true as of its recording date and
is left as recorded, per the standing disposition this corpus applies to signatures. CR-004's
quotation is historical on `c0f7ec7` for exactly the reason CR-002's and CR-003's are, and is left as
recorded for exactly the same reason.

Only the count and the list are wrong. No proposition AUTH-001 asserts about what it authorizes,
bounds, or forbids is affected, and the three authorized edits landed exactly as specified.

### Verified at recording

By extraction against `c0f7ec7`, the corpus references quoting the pre-amendment wording of `:245`,
`:246` or `:248` are:

| Location | Entry | Status |
|---|---|---|
| `corrections.md:100`, `corrections.md:112`, `corrections.md:172` | CR-002 | historical, left as recorded |
| `corrections.md:236`, `corrections.md:241` | CR-003 | historical, left as recorded |
| `corrections.md:445` | CR-004 | historical, left as recorded — **not named by AUTH-001** |
| `authorizations.md:56`, `authorizations.md:79`, `authorizations.md:84` | AUTH-001's own From specimens | not historical; recording the replaced text is their purpose |

`open_contract_gaps.md:398` cites all three line numbers but quotes none of the wording, and is
unaffected. In total 42 corpus references point at the edited lines; none resolves to a different row
after the amendment.

### Not decided by this entry

- Whether AUTH-001's clause should be amended to name CR-004. No repair is authorized or proposed,
  and amending an exercised authorization would itself require a separate act.
- Whether future authorizations should state their known-consequence scope by rule rather than by
  enumeration. That is a drafting question for AUTH-002 onward, not a finding about AUTH-001.
- Anything about §7's signature, which remains unsigned at `:272`.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-23 21:35 EDT
```

Statement: *"CR-005 is acknowledged. AUTH-001's known-consequence clause names two entries where
three quote the pre-amendment wording; CR-004's quotation at `corrections.md:445` is governed by the
clause's substance but excluded by its enumeration. Targeting AUTH-001 rather than CR-004 is
correct — CR-004 is not being fixed, its status is being recorded as changed, which is what keeps
this consistent with the standing rule that records are never retroactively rewritten and a
correction is always a separate act. This acknowledgment authorizes no edit to `authorizations.md`
and no edit to CR-004, and does not extend AUTH-001, which is exercised and spent."*

---

## CR-006

```
Target:            commit 2009c1d's message, VERIFICATION paragraph — the
                   line-endings sentence, and the "normalized to LF"
                   qualifier in the sentence that follows it
Recorded:          2026-08-28
Defect class:      false verification claim — a check reported as performed
                   at blob level was not performed there, and the
                   proposition it reported is false
Basis commit:      2009c1d (origin/main), the commit whose message carries
                   the claim
Authorizes:        no edit to docs/amendment_policy.md, no edit to any
                   document in this corpus, and no rewrite of git history
Status:            recorded; 2009c1d stands as committed
```

**Scope note.** This entry records a defect in a commit message. It does **not** touch, re-verify, or
reopen `docs/amendment_policy.md`, whose content is unaffected and independently confirmed below. It
does **not** reopen GAP-9, which remains open on its own three-part closure condition, and it closes
nothing — per this register's standing rule (`corrections.md:9`), a correction entry "records a
defect in text that is already signed, and closes nothing."

**Why this targets the commit message and not the file.** The file is not defective. It landed with
LF line endings, which is what every other document in this corpus uses, so the outcome was correct;
only the message describing how that outcome was verified is wrong. The defective text is the one
that gets the entry, which is CR-005's holding on the same point.

**Why this register, for a target of a new kind.** Every prior entry targets document text — CR-001
through CR-004 target Contract 001 sections, and CR-005 targets AUTH-001, which is acknowledged
rather than signed. A commit message is neither signed nor a document in `docs/`. It is admitted here
on the register's **behaviour** rather than its subject matter: the text cannot be edited, because
correcting it in place would require rewriting published history, and this register exists precisely
for text that must stand as recorded while the corrected fact lives beside it (`corrections.md:13`,
"the signed text stays as attested"). Whether commit messages are generally within this register's
reach is **not** decided here; see below.

### The defect

The VERIFICATION paragraph of `2009c1d` reads, in relevant part:

> *"164 lines, CRLF, matching the corpus convention in the blob rather than only in the worktree."*

**Three propositions, all false.**

1. **The landed blob is not CRLF.** `HEAD:docs/amendment_policy.md` is blob `9e6119f8`, 10491 bytes,
   containing **zero** CR bytes. 10491 is exactly the byte count of the reviewed LF draft; a CRLF
   encoding of the same 164 lines would be 10655.
2. **There is no CRLF convention in this corpus's blobs.** Every document blob checked contains zero
   CR bytes (table below). No `.gitattributes` exists, so nothing is forcing normalization in either
   direction. The convention the sentence claims to match does not exist and never did.
3. **The stated distinction was not drawn.** The phrase "in the blob rather than only in the
   worktree" asserts that the check discriminated between the git object and the checked-out file.
   It did not, and could not have — see the root cause.

The sentence that follows carries the same defect in its qualifier: *"The staged blob, **normalized
to LF**, is byte-identical to the reviewed draft."* No normalization was required, because the blob
was already LF. The **conclusion** of that sentence is true and is re-verified below; only its stated
method is wrong.

### Root cause — the check reported line counts, not CR counts

The check was run as `git show <ref>:<path>` piped into `grep -c` with an ANSI-C carriage-return
pattern. In the shell used, inside command substitution, that pattern reached `grep` as an **empty
pattern**, which matches every line. The command therefore returned each file's line count under a CR
label. Demonstrated against `authorizations.md`, whose blob contains zero CR bytes:

| Measurement of `HEAD:docs/authorizations.md` | Result |
|---|---|
| piped `grep -c` with the carriage-return pattern | 314 |
| piped `grep -c` with an explicitly empty pattern (control) | 314 |
| `wc -l` (line count) | 314 |

Every figure reported as a CR count in that session — 314, 101, 579, 539, and 164 — is the
corresponding line count. The premise that this corpus stores CRLF blobs originated in the first such
reading and was never independently tested before the commit message asserted it.

The failure is not that the check read the worktree instead of the blob. It read the blob and
measured the wrong property, which is why its result did not disagree with the worktree and so raised
no suspicion. A blob-level claim must be confirmed by a method that cannot silently degrade to a
trivially-true one — raw object size via `git cat-file -s`, or byte counting over `git cat-file blob`
output.

### Effect — none on the landed text

`docs/amendment_policy.md` is unaffected in content, and its integrity claim holds once the defective
qualifier is removed. Blob `9e6119f8` hashes to
`8f6cd0bf3ab8f6df7f96463477712258900002bde1161a63028c407064372bbd`, byte-identical to the reviewed
draft with **no normalization applied**. The sha256 stated in the commit message is correct as
stated.

The remaining verification claims in that paragraph are unaffected, having been performed by an
independent method: the five-anchor sweep was resolved in Python against the remote blobs by content,
and the test result (53 passed, 1156 subtests passed) was read from the runner's own output.

### Verified at recording

Measured with `git cat-file`, which returns the raw object and applies no working-tree conversion:

| Blob (`HEAD:docs/`) | Object | Bytes | CR bytes |
|---|---|---|---|
| `amendment_policy.md` | `9e6119f8` | 10491 | 0 |
| `authorizations.md` | `69da5612` | 19616 | 0 |
| `corrections.md` | `2c6d45bb` | 34335 | 0 |
| `contract_001_domain_resolution.md` | `9f445e04` | 38206 | 0 |
| `open_contract_gaps.md` | `3624d0d0` | 34368 | 0 |
| `audit_method.md` | `365cc674` | 5206 | 0 |

**Recorded as fact, not as defect:** the working copy of `docs/amendment_policy.md` on the machine
that made the commit is CRLF — 10655 bytes, 164 CR bytes — because it was written that way before
staging, and `core.autocrlf=true` normalized it on add. Every other document's working copy is LF and
byte-identical to its blob. This is a local artifact outside the repository, produces no diff, and
changes nothing about what landed. It is recorded because a correct worktree-level check on this one
file would still have reported CRLF while the blob is LF, so the worktree could not have served as a
fallback confirmation.

### Not decided by this entry

- Whether commit messages are generally within this register's reach. This entry is admitted on the
  narrow ground that its target is unamendable and its claim is verifiable; no rule of general
  application is stated, and no instrument is amended to accommodate it.
- Whether a line-ending convention should be established for this corpus, or recorded anywhere. The
  corpus is uniformly LF as a matter of fact; nothing here converts that fact into a rule.
- Anything about GAP-9, which remains open, and anything about the content of
  `docs/amendment_policy.md`, which is not in question.
- Whether the verification technique should be recorded in `audit_method.md` as a further M-item.
  That is a separate act under that instrument's own rules.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than what
a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-28 19:16 EDT
```

---

## CR-007

```
Target:            ADR-001 §5 (`docs/adr_001_fusion_engine_architecture_reconciliation.md:103`)
                   and §6 (`:109`) — internal inconsistency in scope of §0
                   item 3 (Ruling 002 §10.3 / Seam 3) for §38-gating purposes
Recorded:          2026-09-13
Defect class:      internal inconsistency — two sections of the same
                   ACCEPTED document state conflicting scope for the same
                   named item
Basis commit:      b2e1124 (origin/main), the commit that accepted ADR-001
Authorizes:        no edit to docs/adr_001_fusion_engine_architecture_reconciliation.md
Status:            recorded; ADR-001 stands as accepted, defect and all
```

**Scope note.** This entry records a defect in ADR-001's own text. It does not amend, reopen, or
supersede ADR-001, does not adjudicate Ruling 002 §10.3, GAP-4, or GAP-5, and does not touch the
successor-contract hold or the existing-code UNMODIFIED hold. Per this register's standing rule
(`corrections.md:9`), it closes nothing.

### The defect

ADR-001 §5 (`:103`) states: *"FE §38's Pre-Implementation Gate items ... are not satisfied by this
ADR — items 1–3 above are exactly the unruled conflicts §38 has in mind."* Item 3 of §0 is Ruling
002 §10.3 (Seam 3). Read plainly, §5 places Seam 3 among the unruled conflicts §38 gates on.

ADR-001 §6 (`:109`) states the opposite of Seam 3 specifically: *"Seam 3 does not block Fusion
Engine implementation unless a future §10.3 decision chooses to connect disposition synthesis to
C4."* §6 is ADR-001's own "Status and next steps" section — its final, most specific word on what
each seam actually requires.

Both sentences are part of the same ACCEPTED document. They cannot both be read as unqualified with
respect to Seam 3.

### Operator determination

Recorded here as the operator's determination regarding the intended meaning of accepted ADR-001,
not as a new substantive ruling:

- §10.3 / Seam 3 does not block satisfaction of the Fusion Engine §38 Pre-Implementation Gate.
- §10.3 / Seam 3 does not block Fusion Engine implementation.
- ADR-001 §6 reflects the operator's intended determination.
- ADR-001 §5's "items 1–3" reference is overinclusive for §38-gating purposes.

### Not decided by this entry

- §10.3 itself, which remains unresolved.
- Whether disposition synthesis is ever connected to C4 — no connection is created here.
- GAP-4, which remains unresolved.
- GAP-5, which remains unresolved and non-blocking.
- The successor-contract hold, which remains intact.
- The existing-code UNMODIFIED hold, which remains intact.
- Whether §38 is satisfied — it is not declared satisfied by this entry; Seams 1 and 2 remain
  open per ADR-001 §6 itself.
- Any implementation or code change, none of which is authorized here.
- Whether an ACCEPTED ADR may later be directly amended, which remains unresolved.

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-09-13 23:26 EDT
```

Statement: *"I confirm that CR-007 accurately records my determination regarding the inconsistency
between ADR-001 §5 and §6. My intent in accepting ADR-001 was that Ruling 002 §10.3 / Seam 3 does
not block satisfaction of the Fusion Engine §38 Pre-Implementation Gate and does not block Fusion
Engine implementation. ADR-001 §6 reflects that intent, and the §5 reference to 'items 1–3' is
overinclusive for §38-gating purposes.

I am not resolving §10.3 itself or deciding what replaces `dominant_family`, and I am not creating a
connection between disposition synthesis and C4. GAP-4 remains unresolved. GAP-5 remains unresolved
and non-blocking. The successor-contract hold and existing-code UNMODIFIED hold remain in place.

This acknowledgment does not declare §38 satisfied, authorize implementation or any code change,
amend ADR-001, or decide whether an ACCEPTED ADR may later be directly amended. I am acknowledging
CR-007 only as the accurate record of my intended meaning of ADR-001 on the Seam 3 / §10.3 gating
question."*

---

## CR-008

```
Target:            20 distinct exact-line citations into open_contract_gaps.md
                   (23 citation instances across 19 source lines), from:
                     contract_001_domain_resolution.md :320 (5 instances), :322 (1)
                     contract_002_domain_resolution_invariants.md :328 (1)
                     corrections.md :553 (1)
                     authorizations.md :160,163,164,176,183,191,202,208,
                       221,222,230,247,249,253,277 (15)

Signed:            contract_001 §5 (cbf14c45, 2026-08-20), §6 (bc1b8d36,
                   2026-08-21), §8 (7ee64605, 2026-08-25); contract_002 §4
                   (42427a6, 2026-09-15, LOCKED); corrections.md entry
                   (92481f36, 2026-08-23); authorizations.md AUTH-002
                   (cf4b79f5, 2026-08-25, acknowledged)

Defect:            each citation below resolved correctly in
                   docs/open_contract_gaps.md as it stood at commit dddaa09
                   (5a3ba9f's immediate predecessor for this file — no
                   intervening commit touches it) and resolves to different,
                   wrong content at HEAD. Commit 5a3ba9f ("docs: record
                   GAP-4 closure in the gap register", 2026-09-15) inserted
                   text at four points in open_contract_gaps.md — 2 lines
                   after old :186, 54 lines after old :658, and 1+1+2 lines
                   at three points inside the GAP-4 successor-restatement
                   section — without updating any citation from outside the
                   file. Verified via `git show 5a3ba9f -- docs/open_contract_gaps.md`
                   (5 hunks) and by diffing each target below between
                   dddaa09 and HEAD directly, not by arithmetic. Re-verified
                   against the repository baseline current at filing
                   (8de5b5f, which post-dates 5a3ba9f but touches only
                   open_contract_gaps.md lines 844 onward — none of the
                   ranges below).

Corrected references (old target → corrected target, dddaa09 → HEAD):

  | # | Citing document                                | Source line(s) | Old target | Corrected target |
  |---|-------------------------------------------------|-----------------|------------|-------------------|
  | 1 | contract_001_domain_resolution.md               | :320            | :197       | :199              |
  | 2 | contract_001_domain_resolution.md               | :320            | :201       | :203              |
  | 3 | contract_001_domain_resolution.md               | :320            | :203       | :205              |
  | 4 | contract_001_domain_resolution.md               | :320            | :205-206   | :207-208          |
  | 5 | contract_001_domain_resolution.md               | :320            | :222-223   | :224-225          |
  | 6 | contract_001_domain_resolution.md               | :322            | :390       | :392              |
  | 7 | contract_002_domain_resolution_invariants.md    | :328            | :717-719   | :775-777          |
  | 8 | corrections.md                                  | :553            | :398       | :400              |
  | 9 | authorizations.md                               | :160            | :397-403   | :399-405          |
  | 10| authorizations.md                               | :163            | :313-405   | :315-407          |
  | 11| authorizations.md                               | :164, :191      | :380-388   | :382-390          |
  | 12| authorizations.md                               | :176            | :394       | :396              |
  | 13| authorizations.md                               | :183, :277      | :401-402   | :403-404          |
  | 14| authorizations.md                               | :202            | :390       | :392              |
  | 15| authorizations.md                               | :208            | :384-385   | :386-387          |
  | 16| authorizations.md                               | :221            | :334-336   | :336-338          |
  | 17| authorizations.md                               | :222            | :383       | :385              |
  | 18| authorizations.md                               | :230            | :346-348   | :348-350          |
  | 19| authorizations.md                               | :247            | :317-318   | :319-320          |
  | 20| authorizations.md                               | :249            | :375-377   | :377-379          |
  | 21| authorizations.md                               | :253            | :403       | :405              |

  (Rows 11, 13 each cover 2 of the 23 citation instances, sharing one
  target pair; all other rows cover 1 instance each — 21 rows, 23
  instances.)

Classification:    factual/referential defect — same shape as CR-001. For
                   every row, the underlying proposition the citing
                   document draws from that line is unchanged; only the
                   line number is wrong.

Basis:             Immediate predecessor for docs/open_contract_gaps.md is
                   dddaa09 (confirmed via `git log --oneline -- docs/open_contract_gaps.md`
                   — no other commit touches this file between dddaa09 and
                   5a3ba9f). For each row above: `git show dddaa09:docs/open_contract_gaps.md`
                   at the "Old target" line contains the proposition the
                   citing source line states; the same line at HEAD
                   (`docs/open_contract_gaps.md`) does not; the "Corrected
                   target" line at HEAD does. Every row independently
                   verified this way, not inferred from a shared offset,
                   and re-verified against HEAD at commit 8de5b5f.

Effect:            None on any signed proposition's substance. For all 21
                   rows, the content each citation was written to support
                   still exists in open_contract_gaps.md, at the corrected
                   line shown above. This entry:
                     - does not amend contract_001_domain_resolution.md,
                       contract_002_domain_resolution_invariants.md,
                       corrections.md, or authorizations.md — all cited
                       text stays exactly as attested;
                     - does not reopen any signature, acknowledgment, or
                       grant;
                     - does not change Contract 001 or Contract 002;
                     - does not change or reopen GAP-4 or GAP-5;
                     - closes no open_contract_gaps.md register entry;
                     - authorizes no implementation of any kind;
                     - edits open_contract_gaps.md nowhere — this entry
                       records corrected references only, in
                       corrections.md, exactly as CR-001 through CR-007
                       already do for other locked-text citations.

Scope note — why these 21 rows are one batch:
                   All share (a) the same causal commit, 5a3ba9f; (b) the
                   same affected target file, open_contract_gaps.md; (c)
                   the same mechanism, insertion-driven exact-line drift
                   with no corresponding update to external citations; (d)
                   the same remediation constraint — every citing document
                   is locked, LOCKED, or an acknowledged/granted record,
                   none of which this corpus's amendment_policy.md permits
                   editing in place; (e) the same substantive effect —
                   every underlying proposition remains true and findable,
                   only its address moved. No other stranded citation
                   found in this audit shares all five properties, and
                   none of the following is included on that basis:
                     - ruling_002_family_taxonomy_integrity.md:635 →
                       open_contract_gaps.md:111 — different cause
                       (109fafe7 and 5229f9f1, 2026-08-15/16, a month
                       before 5a3ba9f); tracked as a separate candidate,
                       not filed here.
                     - authorizations.md:256 → open_contract_gaps.md:409-411
                       — different cause (20f2a43, 2026-08-25) and a
                       different defect shape: no corrected target exists
                       because the cited fact itself later became untrue,
                       not merely relocated; held separately, not filed
                       here.
                     - open_contract_gaps.md's own self-citations at
                       :604, :626, :722, :727, :728 (x3), :729, :730, :809,
                       :834 — displaced by the same commit, but the citing
                       document (the register itself) is editable, so the
                       remediation is a direct in-register fix, not a
                       corrections.md entry; excluded per (d), not repaired
                       here.

Recorded:          2026-09-17
```

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-09-17 21:07 EDT
```

Statement: *"I acknowledge CR-008 as filed. The exact-line citation drift caused by commit 5a3ba9f
is confirmed for the 23 citation instances recorded here. CR-008 corrects those references only; it
does not amend the underlying signed or acknowledged text, change any substantive proposition, or
authorize any implementation."*

---

## CR-009

```
Target:            3 passages in Contract 002, all bearing on GAP-5's
                   successor-contract routing status:

                     1. Preamble, "What this document does not do"
                        (docs/contract_002_domain_resolution_invariants.md:67-68):
                        "It does not touch, bundle, or reserve a place for
                        GAP-5. GAP-5's own successor-contract restatement
                        remains 'proposed / not operative'; nothing here
                        changes that, and no invariant number is reserved
                        for it." — the defect is not the quoted historical
                        fact (see Defect, Target 1 below) but the
                        present-state implication carried by "nothing here
                        changes that": that GAP-5 had no operative routing
                        as of this reading.
                     2. §5 Exclusions, table row (:243):
                        "GAP-5 (`SURFACED` payload completeness) | tracked
                        separately; its successor-contract routing is not
                        operative and is not addressed here" — direct state
                        assertion.
                     3. §7 Sign-off checklist, §5-row attestation clause
                        (:334-338, clause at :338): "...GAP-5 to its own,
                        not-yet-operative routing;..." — direct state
                        assertion.

Signed:            contract_002, attested in full (`:362`) — every row of §7
                   signed 2026-09-15, LOCKED 2026-09-15, single commit
                   (42427a6). Target 2 is itself the §5 body; Target 3 is
                   §7's own verification of §5; Target 1 is preamble text
                   the LOCKED status line (`:362`, "attested in full")
                   covers along with the rest of the document, not only the
                   seven numbered §7 rows.

Defect:            Common chronology. GAP-5's closure condition has carried
                   exactly one successor-contract restatement since
                   2026-08-28 (`open_contract_gaps.md:805-843`), Status
                   "proposed / not operative," until 2026-09-17, when the
                   operator approved a second, later restatement as GAP-5's
                   operative routing target (`docs/open_contract_gaps.md:846-916`,
                   "Proposed successor-contract restatement — 2026-09-17,"
                   Status: "operative / not closed"; closing paragraph
                   `:914-916` — "now GAP-5's operative closure-condition
                   routing"). That determination is substantively recorded
                   in open_contract_gaps.md; commit 8de5b5f ("docs: approve
                   GAP-5 successor routing restatement") is the
                   repository-history record of when it was committed, not
                   the substantive authority for the determination itself.
                   Contract 002 was LOCKED 2026-09-15, two days before that
                   determination. None of the three passages is mislocated
                   or misquoted; the defect is in the governance-state
                   proposition or implication each carries, not in where the
                   passage resides.

                   Target 2 (`:243`). Direct state assertion. "Its
                   successor-contract routing is not operative" was true at
                   LOCK (2026-09-15) and is false as of 2026-09-17.

                   Target 3 (`:338`). Direct state assertion, same shape as
                   Target 2. "GAP-5 to its own, not-yet-operative routing"
                   was true at LOCK and is false as of 2026-09-17.

                   Target 1 (`:67-68`). Different shape from Targets 2/3 —
                   preserved as such, not flattened into the same wording.
                   The quoted historical sub-clause — "GAP-5's own
                   successor-contract restatement remains 'proposed / not
                   operative'" — is NOT the defect and did NOT become
                   false: it names the 2026-08-28 restatement specifically,
                   which was never edited or retracted and still carries
                   that literal Status label today. The defect is the
                   present-state implication the sentence carries via
                   "nothing here changes that" — read at the time Contract
                   002 was LOCKED, this told a reader that GAP-5 currently
                   had no operative routing at all. That implication became
                   stale on 2026-09-17: GAP-5 does now have an operative
                   routing target, created by a separate, later restatement
                   the 2026-08-28 text and this preamble sentence could not
                   have anticipated. The historical fact quoted remains
                   true; the present-state reading it invites is what is
                   now misleading.

                   Contract 002 is LOCKED and, per its own §6 text
                   (`:260-262`) and `amendment_policy.md`, no part of a
                   LOCKED document's text is amended for any reason,
                   including a defect this or a later act discovers; none
                   of the three passages can be corrected in place.

Classification:    historical-state defect batch. Targets 2 and 3 are
                   direct state assertions made false by subsequent
                   governance; Target 1 is a present-state implication made
                   stale by the same governance act while its literal
                   quoted historical clause remains true. Distinct in kind
                   from CR-008 (referential/pointer drift). See scope note
                   below.

Basis:             Substantive authority for all three: `docs/open_contract_gaps.md:846-916`,
                   the 2026-09-17 operator determination. Provenance only:
                   commit 8de5b5f, confirmed via `git show 8de5b5f --
                   docs/open_contract_gaps.md`. Contract 002's LOCKED status
                   and 2026-09-15 date confirmed at
                   `docs/contract_002_domain_resolution_invariants.md:7`.

                   Sweep scope note. All three targets were located by a
                   full-document sweep of contract_002 for "GAP-5" (4
                   instances total) and "operative" (8 instances total,
                   case-insensitive). The sweep found one further GAP-5
                   instance (`:344`, "no GAP-5 content") and five further
                   "operative" instances (`:7`, `:8`, `:17`, `:36` — Contract
                   002's own supersession status; `:48-49` — GAP-4's,
                   not GAP-5's, routing) and excluded all of them: none
                   depends on GAP-5's routing status, so none is made false
                   or stale by the 2026-09-17 determination. They are not
                   correction targets and are noted here only to record why
                   the sweep stopped at three. Re-verified against the
                   repository baseline current at drafting (`main` at
                   2371880).

Effect:            None on Contract 002's substance and none on GAP-5's
                   status. This entry:
                     - does not amend contract_002_domain_resolution_invariants.md
                       at any of the three locations — the LOCKED text stays
                       exactly as attested;
                     - does not reopen Contract 002's LOCK or any signature,
                       including any individual §7 row;
                     - does not close GAP-5, which remains open;
                     - does not itself create the operative routing — that
                       was already done by the 2026-09-17 operator
                       determination; this entry only records that three
                       passages of Contract 002's text are now stale with
                       respect to it;
                     - does not draft or authorize the GAP-5 successor
                       contract, and does not authorize any implementation;
                     - does not extend beyond these three proven
                       historical-state defects — the excluded items noted
                       under Basis are not corrected here and require their
                       own separate treatment, if any, to be added.

                   Unaffected propositions, stated narrowly per target:
                     - Target 1: "It does not touch, bundle, or reserve a
                       place for GAP-5" and "no invariant number is reserved
                       for it" remain true; the literal quoted historical
                       clause about the 2026-08-28 restatement's own Status
                       label remains true.
                     - Target 2: "tracked separately" and "is not addressed
                       here" remain true.
                     - Target 3: the other eight exclusion-routing clauses
                       in the same §7 sentence (domain names, provider
                       choice, registry expansion, implementation mechanism,
                       Seam 3, Ruling 002 §10.5/§10.7, Fusion Engine, other
                       governance-document edits) remain true and are
                       unaffected.

Scope note — CR-009 is state drift, not pointer drift like CR-008:
                   CR-008 corrects citations whose exact-line target moved
                   because an editable file had text inserted above the
                   cited line — the underlying proposition stayed true
                   throughout; only its address changed, and each of its 21
                   rows corrects a distinct citation to a distinct
                   proposition. CR-009 is the opposite shape: no address
                   ever moved or was wrong, but a factual proposition (or,
                   for Target 1, a present-state implication) written into
                   LOCKED text — true, or not yet stale, when LOCKED — was
                   made false or stale by a later, independent governance
                   act that the LOCKED text has no mechanism to reflect.
                   CR-009's three targets are batched together, not as
                   distinct claims sharing only a cause (CR-008's shape),
                   but as one recurring claim about GAP-5's routing status,
                   asserted twice directly and implied once, all three
                   overtaken by the same 2026-09-17 act. Both entries are
                   recorded here only because the affected text cannot be
                   edited in place; the distinction between them is kept as
                   register precedent for classifying future candidates of
                   either shape.

Recorded:          2026-09-20
```

**Acknowledgment** — pending. No operator acknowledgment has been given for CR-009.

