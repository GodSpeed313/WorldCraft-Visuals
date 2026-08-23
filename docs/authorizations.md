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
