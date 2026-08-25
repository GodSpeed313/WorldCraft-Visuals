# Authorizations

This file records operator authorizations to edit corpus text. It exists because an authorization
that lives only in a chat turn, a commit message, or a signature row is not discoverable later by
anyone reading the corpus.

**What this file is not.** It is not a section or appendix of any contract or ruling. It is not the
gap register (`open_contract_gaps.md`), which tracks what a contract fails to enforce, and it is not
the corrections register (`corrections.md`), which records defects in text and — by its own standing
rule at `corrections.md:12-13` — **cannot** authorize an edit. An authorization is a third act: it
grants permission to change text, names exactly what may change, and closes when the authorized
commit lands.

**Standing rule.** An entry here authorizes only what it names. Nothing in this file is a signature,
and no entry ticks a sign-off box. An authorization that has been exercised remains on the record;
it is not deleted once used.

**Why this file was created on 2026-08-23.** The two prior pre-signature amendments to Contract 001
were authorized nowhere in the corpus. `425aa09` (`:114`, `:153`) carries its authority only in its
commit message — *"Operator ruling: match :114 to :128's count basis rather than tie it to a support
threshold."* `0c83577` (`:57`) carries no authorization line at all, and is known to have been
authorized only because §6's signature (`contract_001_domain_resolution.md:271`) later cites it as
*"the standing precedent that the route is available in this corpus."* Grepping `docs/` for either
hash returns two signature rows and nothing else. Those two amendments are not reopened by this
file; the gap in the record is noted, not retroactively filled.

---

## AUTH-001

```
Authorizes:        editing Contract 001 §7, and only §7
Target lines:      :245, :246, :248 — three edits, enumerated below
Route:             amend-then-sign (route A), per the precedent at 0c83577
Granted by:        Kevin Brown, operator
Granted at:        2026-08-23, in session
Basis:             CR-002 findings 1, 2, 3 and CR-003, all recorded in
                   corrections.md; §7 is UNSIGNED, so no attestation is
                   disturbed by an edit made before signature
Status:            granted; NOT YET EXERCISED — no edit has been made to
                   contract_001_domain_resolution.md as of this recording
```

**Why route A and not route C.** Route C — relocating §7 out of the contract entirely, so that
§1's self-test (`contract_001_domain_resolution.md:41-42`) no longer reaches it — was presented and
not taken. Route A keeps `:239`'s pattern where a reader of the contract meets it, and §6's own
stated test for when amendment is available is met: these are local text repairs, not the
*"substantive invariant design with implementation consequences"* that §6's signature
(`contract_001_domain_resolution.md:271`) gives as its reason for declining the route for GAP-4 and
GAP-5. No invariant is touched by any edit below.

### The three authorized edits

**Edit 1 — `:245`, row 2's "what is preserved" cell.** Discharges CR-002 finding 1.

- From: `the meaning of a category`
- To: `the integrity of what members inherit from a family`

Grounded in `ruling_002_family_taxonomy_integrity.md:96` and the mechanism amendment at
`ruling_002_family_taxonomy_integrity.md:101-108`. Deliberately neutral between the two inheritance
channels: the amendment warns at `ruling_002_family_taxonomy_integrity.md:107-108` that a future
reader must not read the grounding sentence as current behavior, so the cell may not say
"grounding"; "classification" alone would drop the prospective half the amendment states is a
reason for the same rule.

**Edit 2 — `:246`, row 3's rule cell.** Discharges CR-002 finding 2.

- From: `ambiguity is preserved, never collapsed`
- To: `ambiguity is preserved, never collapsed; selecting arbitrarily is prohibited`

I3 (`contract_001_domain_resolution.md:221-222`) closes *"Selecting arbitrarily is prohibited"* —
the clause §6's signature (`:271`) identifies as operative and without which it holds I3 is not
adequately represented. Row 3's "what is preserved" cell was not flagged by Beat 1 and is **not**
authorized for change.

**Edit 3 — `:248`, the synthesis sentence.** Discharges CR-002 finding 3 **and** CR-003 in a single
amendment.

- From: `In each case the system is permitted to be *incomplete* but never permitted to be *falsely certain*.`
- To: `Each of the three rules accepts a less resolved result rather than a wrongly resolved one: a duplicate left unmerged, a family left unadmitted, a domain left unselected.`

**One edit, not two, and the reason is not merely that both defects share a sentence.** A bare
strike of *"in each case"* would repair jurisdiction — the distribution onto row 2 disappears and
the subject reverts to I6's shape — but would leave *"the system is permitted to be incomplete"*
asserted without restriction and without any cited support, which is a worse sourcing posture than
CR-002 finding 3 describes rather than a repair of it. Each defect's fix redefines the other's
target, so the two cannot be sequenced in either order and must be one amendment justified by both
findings.

The replacement was checked against four things:

1. **Jurisdiction (CR-003).** The subject is *the three rules*, not *the system*, and no deontic
   verb remains. The sentence reports rather than conditions, placing it in the same observational
   register as `:245`, which already survives `:41-42`.
2. **`:239`'s stated purpose.** The section's value is the pattern. The replacement names all three
   rows in table order, so the sentence stays tied to the table it summarizes.
3. **CR-002 finding 3.** The original's error was choosing *incomplete* as the unifying term, which
   fits rows 2-3 but not row 1, where Ruling 001 §1 licenses noise — over-completeness
   (`ruling_001_canonicalization_policy.md:31`). *Less resolved* covers all three: an unmerged
   duplicate is an identity question the system declined to decide. Row 1 is no longer an exception.
4. **What Beat 1 found sound is preserved.** *"Never falsely certain"* held across all three rows;
   *"rather than a wrongly resolved one"* carries it forward.

### This authorization does NOT authorize

- Any edit to `contract_001_domain_resolution.md` outside `:245`, `:246`, and `:248`.
- Any wording at those three lines other than the wording set out above. A different repair requires
  a different authorization.
- Ticking §7's sign-off box (`:272`), or any other box. Amendment and signature are separate acts,
  and §7 remains unsigned when the authorized edits land.
- Any edit to `:272`'s existing text, whose rejection as clearance is recorded in CR-003.
- Reopening, amending, or correcting CR-002 or CR-003, or any signed row.
- Any edit to Ruling 001 or Ruling 002, both LOCKED.
- Route C. Relocating §7 out of the contract is not authorized by this entry.

### Verification required before the authorized commit lands

- Every line of `contract_001_domain_resolution.md` other than `:245`, `:246`, and `:248` byte-identical
  to the pre-edit file, so no signature's anchors shift — the check `0c83577`'s commit message
  records ("zero anchor shift").
- File length unchanged at 275 lines.
- Every `:NNN` reference in the amended §7 re-resolved by extraction against the post-edit file.

### Known consequence, recorded not addressed

CR-002 and CR-003 quote `:245`, `:246`, and `:248` as they read **before** these edits. Those
quotations become historical on the authorized commit. Both entries are true as of their recording
dates and are left as recorded, per the standing disposition this corpus applies to signatures.
Correcting them would be a separate act, and this authorization does not permit it.

**Acknowledgment** — an acknowledgment, not a section signature.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-23 19:20 EDT
```

Statement: *"AUTH-001 is acknowledged. Creating a third instrument rather than forcing the
authorization into `corrections.md` is correct, and it was checked into existence rather than
argued into it: grepping for the two prior amendment hashes and finding nothing outside a commit
message and two signature rows demonstrates that authorization living only in ephemeral text is
not a hypothetical risk — it has already happened twice. Recording that `425aa09` and `0c83577`
lack discoverable authorization, without retroactively supplying one, is right; the record should
show the gap existed rather than paper over it now that the fix is available. The authorization is
bounded to wording and not only to line numbers, and the does-not-authorize list is part of what is
granted, not commentary on it. **AUTH-001 pre-clears the permission question only. It does not
pre-clear the wording.** The §7 amendment commit remains subject to diff review of its proposed
replacement text before it lands; permission and wording-is-good are separate reviews, even though
this entry lists specimens."*

---

## AUTH-002

```
Authorizes:        adding authored new text to Contract 001 §8, and only §8
Target lines:      insertion after :259 and before :261 — :250 through :259
                   byte-identical, the normative clause at :252-254 not altered
Route:             extend-then-close-then-sign — three acts, not two, per
                   open_contract_gaps.md:397-403
Granted by:        Kevin Brown, operator
Granted at:        2026-08-25, in session
Basis:             GAP-8 (open_contract_gaps.md:313-405), whose closure
                   condition at open_contract_gaps.md:380-388 requires
                   authored new text; §8 is UNSIGNED at :273, so no
                   attestation is disturbed by an edit made before signature
Status:            granted; NOT YET EXERCISED — no edit has been made to
                   contract_001_domain_resolution.md as of this recording
```

**Why this authorization is bounded differently from AUTH-001.** Two differences, both forced by what
GAP-8 asks for rather than chosen.

1. **No From/To specimens.** AUTH-001 bounded wording by specimen because each of its three edits
   replaced text that already existed. GAP-8 requires *"authored new text, not a wording
   substitution"* (`open_contract_gaps.md:394`); there is no From to quote. This entry therefore
   bounds by location and by required and forbidden content. That is a **weaker bound than
   AUTH-001's**, and it is stated as weaker rather than dressed up as equivalent; the
   does-not-authorize list below and the mandatory wording review are what compensate. The principle
   relied on is already on the record — AUTH-001's acknowledgment holds that *"permission and
   wording-is-good are separate reviews, even though this entry lists specimens"*
   (`authorizations.md:146-149`), and GAP-8 states the same requirement for this gap specifically
   (`open_contract_gaps.md:401-402`).
2. **Anchor shift is unavoidable.** AUTH-001 required every unedited line byte-identical *"so no
   signature's anchors shift"* and the file unchanged at 275 lines (`authorizations.md:118-121`). New
   text can satisfy neither. This is not a relaxation of AUTH-001's standard for convenience; it is a
   property of adding lines. It is governed by rule under **Known consequence** below.

### What the authorized text must do

Restated from GAP-8's closure condition (`open_contract_gaps.md:380-388`), because an authorization
that does not state what it is buying cannot be checked against what lands:

1. **Classify the requirement at `:252-254`** — mirroring what `:46-48` does for §2, or naming it a
   fourth kind of thing.
2. **Carry a scope statement** — stating what the requirement binds and what a signature on it
   attests.
3. **Be testable, or say why not** — an operational check in V1's form (`:87-90`), including what
   violating it looks like; or an explicit statement that no such test exists and why, in the manner
   of Ruling 001 §7.4's recorded deferral.

**Partial satisfaction does not close GAP-8** (`open_contract_gaps.md:390`). This authorization does
not permit a partial landing to be treated as closure, and landing text under it is not itself
closure.

### Why the own-scope-clause branch, and not an amended `:50`

GAP-8 offers both routes (`open_contract_gaps.md:384-385`). This entry authorizes only the second.

AUTH-001's basis line states the ground: an edit made before signature disturbs no attestation
(`authorizations.md:38-39`). `:50` has no such standing. It sits in §2, and §2's two rows are
**signed** at `:266` and `:267`; both signatures attest that the document satisfies conditions `:50`
scopes. This corpus has no precedent for amending text a signature attests, and establishing one is
not a side effect this authorization should carry while its actual subject is elsewhere.

**Consequence for the classification, stated because it is not obvious.** Because `:50` may not be
amended, the authorized text **may not classify `:252-254` as a third validity constraint.** `:50`
names V1 and V2 only. A V3 that `:50` does not reach would reproduce GAP-8's own finding — a
normative requirement no scope clause governs — in a new place and under a more official-looking
name. GAP-8 already says the clause *"is not a third validity constraint"* and that no V3 exists
anywhere in `docs/` (`open_contract_gaps.md:334-336`). The classification must therefore mirror
`:46-48`'s form for §8 alone, or name a fourth kind of thing per `open_contract_gaps.md:383`, and
carry its own scope statement either way.

### The `knowledge conditions` question — one branch only

GAP-8 records that §8's proviso restates V2's substance in V2's own coined term without citing V2,
the term occurring exactly twice in the contract, at `:96` and `:253`, and that closure must decide
whether this is *"duplication to remove, a cross-reference to add, or correct as written"*
(`open_contract_gaps.md:346-348`).

**This authorization permits the cross-reference branch only, and only inside the new text.** A
citation of V2 placed in the authorized text decides the question without touching `:252-254`.
Removing the duplication would mean rewriting the normative clause itself, which is not authorized
here; if that is the decision, it requires a different authorization. Concluding *correct as written*
requires no edit and is not restricted by this entry.

### This authorization does NOT authorize

- Any edit to `contract_001_domain_resolution.md` outside the insertion region after `:259` and
  before `:261`.
- Any alteration to `:250` through `:259`, including the normative clause at `:252-254` and the
  rationale at `:256-259`.
- Amending `:50`, any other text in §2, or any text attested by a signature at `:265` through `:272`.
- Classifying `:252-254` as V3, or as any member of the V-set, for the reason stated above.
- Adding an invariant, or creating I8. GAP-8 holds that an invariant is *"probably the wrong
  instrument"* (`open_contract_gaps.md:317-318`) and that I8 *"would create an eighth member of a set
  §8's clause does not belong to, without saying what the clause itself is"*
  (`open_contract_gaps.md:375-377`).
- Ticking §8's sign-off box at `:273`, or any other box. Extension and signature are separate acts,
  and §8 remains unsigned when the authorized text lands.
- Closing GAP-8 in the register. The register is a working ledger that rules nothing
  (`open_contract_gaps.md:3`) and closes this entry on the commit (`open_contract_gaps.md:403`);
  recording that closure is a separate act under the register's own rules, and it would be the
  register's **first** — its Closed section reads *"(none yet)"*
  (`open_contract_gaps.md:409-411`).
- Correcting any anchor that shifts as a result of the authorized commit. See **Known consequence**.
- Amending AUTH-001 to name CR-004, or repairing CR-004. CR-005 leaves both undecided
  (`corrections.md:559-560`); this entry decides neither and inherits neither.
- Reopening, amending, or correcting CR-002, CR-003, CR-004, CR-005, or any signed row.
- Any edit to Ruling 001 or Ruling 002, both LOCKED.

### Verification required before the authorized commit lands

- Lines `:1` through `:259` byte-identical to the pre-edit file.
- Every line from old `:260` to old `:275` byte-identical in **content**, its number larger by
  exactly N, where N is the count of lines added and is stated in the commit message.
- File length exactly 275 + N. The pre-edit file is 275 lines and contains zero CR bytes; both
  verified at granting, the latter by byte count rather than by line-oriented search.
- §8's box still reads `- [ ]`, at old `:273` / new `:273 + N`.
- Every `:NNN` in the new text extracted programmatically and re-resolved against the **post-edit**
  file, printing the line **content**, not merely checking the range (`audit_method.md:26-34`,
  `audit_method.md:55-61`, `audit_method.md:70-77`).
- Every cross-document anchor in the new text qualified with its filename, and **every item** in any
  list of anchors qualified, not only the first (`audit_method.md:46-53`, `audit_method.md:88-95`).
- Operator wording review of the drafted text, by diff, before it lands
  (`open_contract_gaps.md:401-402`).
- After push, the **remote** ref queried rather than the local branch (`audit_method.md:63-68`).

### Known consequence, stated as a rule

CR-005 found AUTH-001's known-consequence clause named two entries where three qualified, and left to
AUTH-002 onward *"whether future authorizations should state their known-consequence scope by rule
rather than by enumeration"* (`corrections.md:561-562`). This clause states a rule.

**Rule.** Every reference anywhere in this corpus to a line of `contract_001_domain_resolution.md` at
or after old `:260` — written qualified or bare, listed below or not, existing at this granting or
added before the commit — points after the authorized commit at a line number larger by exactly N.
Every such reference is true as of its recording date and is left as recorded. **This authorization
permits the correction of none of them.**

The disposition is the corpus's established one and the precedent is already on the record: `:269`
records that a Ruling 002 pointer had gone stale, *"now landing at"* a different line, and leaves it
*"recorded, not corrected, per the standing disposition that a signature is true as of its date."*
`:268` declines on the same ground to update `:266` and `:267` after the questions they routed had
been answered.

**Orientation only, and expressly not the operative enumeration.** At granting, extraction finds 29
such references across four files — `authorizations.md`, `contract_001_domain_resolution.md`,
`corrections.md` and `open_contract_gaps.md` — concentrated in the sign-off rows at `:265` through
`:273`. The rule above governs whether that count is complete and whether it goes stale. That is the
point of stating it as a rule: CR-005's defect was an enumeration accurate when written and
incomplete when exercised, and a count cannot fail that way if nothing depends on it.

**Acknowledgment** — an acknowledgment, not a section signature.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-25 15:32 EDT
```

Statement: *"I acknowledge AUTH-002 as drafted — all four decisions as you made them
(own-scope-clause not amended `:50`, no V3, insertion after `:259`, cross-reference-only for
"knowledge conditions")."*
