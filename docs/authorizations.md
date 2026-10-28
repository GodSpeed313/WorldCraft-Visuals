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

---

## AUTH-003

```
Authorizes:        an independent operator determination narrowly releasing
                   FE Requirements §39's "Existing WorldCraft-Visuals code —
                   UNMODIFIED" hold, for Seam 1 conformance work only
Target functions:  modality_classifier.py::classify()
                   modality_classifier.py::classify_fusion()
                   mythos_sync.py::build_legacy_profile()
Target tests:      test_engine.py::test_unknown_character_defaults_to_grounded
                   test_engine.py::test_unknown_characters_still_produce_a_valid_profile
Route:             operator determination (independent act, releasing the
                   hold) → recorded here for durability/discoverability →
                   implement → verify against the checklist below → commit
Granted by:        Kevin Brown, operator
Granted at:        2026-09-14, in session
Basis:             Ruling 001 §4 (`ruling_001_canonicalization_policy.md:153-218`),
                   LOCKED, ruling "resolve-then-proceed, never silently
                   default"; Ruling 001 §6 (`:276-322`), Normalization
                   Regression Case 001, naming "Unknown character/power
                   silently became GROUNDED" as failure #1 under Invariant 1;
                   ADR-001 Seam 1 (`adr_001_....md:70-76`), finding "no new
                   semantic ruling is required to prohibit unknown→GROUNDED;
                   only the concrete implementation path and scoped
                   authorization remain open"; FE Requirements §39, whose
                   hold is released ONLY for the scope named above
Status:            granted; NOT YET EXERCISED — no edit has been made to
                   any file as of this recording
```

**What actually releases the hold, and what this entry is.** These are two different things and this
entry keeps them separate on purpose:

- **The operator determination** is Kevin Brown's own act, made independently of this file, narrowing
  the FE §39 hold to permit exactly the work named above. That determination is what has legal force.
  It does not derive its authority from `authorizations.md`.
- **This AUTH-003 record** is the archive of that determination — the durable, discoverable place
  where the corpus states that the determination was made, what it covers, and what it does not. It
  performs the same function this register already performs for prior operator acts. It does not
  create the authority; it preserves it.

**On `authorizations.md`'s own stated scope — recorded explicitly, not glossed over:**

1. `authorizations.md`'s introductory text presently describes itself as recording authorizations "to
   edit corpus text." Read strictly, that sentence does not mention source code.
2. This entry does **not** determine that the register's stated subject matter generally encompasses
   source code. No such general finding is made here.
3. This entry does **not** expand or amend the register's introductory definition. That sentence is
   untouched by this entry, and this entry does not depend on it being read broadly.
4. The FE §39 hold release, for the narrow scope named above, is an **independent operator act** —
   its authority comes from Kevin Brown's own determination, not from this register's jurisdiction.
5. AUTH-003 exists to **record** that act, in the same durable/discoverable form every prior
   authorization uses, so it is not lost to a chat turn or an unlabeled commit message
   (`authorizations.md:3-5`, restating why this file exists at all).
6. Whether future code authorizations generally belong in this register, and under what definitional
   revision, is **not decided here** and remains open.
7. **AUTH-003's validity does not depend on resolving that broader question.** If the register's
   scope is later formally extended to code, or if code authorizations are later routed to some other
   instrument instead, this entry's validity is unaffected either way — it stands on the operator
   determination it records, not on a jurisdictional reading of this file's own definition.

### What "resolve-then-proceed" must do here, stated behaviorally

Restated so the authorized work has something to be checked against, not invented at implementation
time. Corrected against Ruling 001 §4's actual text rather than a shorthand attribution:

1. Unknown/unregistered character input passed to `classify()` must no longer silently become
   `GROUNDED`. Per §4's own diagram (`:160-172`), unrecognized input must instead follow the
   `normalization request` branch to either a resolved-and-validated result or an `unresolved →
   blocked` outcome — not default straight to a fabricated profile.
2. `classify_fusion()` must safely propagate or handle that outcome rather than failing through, or
   silently succeeding past, its modality-rank lookup (`MODALITY_RANK[...]` keyed off a fabricated
   modality would either `KeyError` or silently succeed today; neither is acceptable).
3. `build_legacy_profile()` must stop, or propagate, that outcome before it reaches downstream
   grounding/audit logic (`audit_power`/`ground_power`, untouched by this authorization, must not be
   reached with fabricated input as a result of this change).
4. The two named tests must be changed to assert the corrected Ruling-001 behavior for unrecognized
   input, rather than the superseded assertion that it yields `GROUNDED`.
5. No new unresolved-state semantics may be invented under this authorization. Ruling 001 §4 presents
   the four-state output framework (ADMITTED/SURFACED/CAUTIONARY/BLOCKED) at `:175-182`, but the table
   itself attributes SURFACED's governance to Ruling 002 §5.3, not to Ruling 001 alone. For
   unrecognized-character input specifically, §4's own diagram routes only to `CAUTIONARY` (pending,
   normalization requested) or `BLOCKED` (resolution/validation failed) — `ADMITTED` and `SURFACED`
   describe post-recognition or post-grounding outcomes and are not what `classify()` is expected to
   produce here. Implementation must map onto `CAUTIONARY`/`BLOCKED` as already defined; it must not
   invent a new state, and must not silently reach for `SURFACED`, which is Ruling 002's terminal
   grounding-layer concept, not a character-recognition outcome.

### This authorization does NOT authorize

- Any edit to `logic_auditor.py`. It must remain byte-identical.
- Either GAP-4 fallback site (`logic_auditor.py:136`, `:173-174`) or any GAP-4 resolution.
- Any Fusion Engine C1–C6 implementation.
- Anything concerning §10.3 / Seam 3, resolved as non-blocking by CR-007 but not otherwise touched.
- Anything concerning GAP-5.
- Any edit to `server.py`.
- Any dashboard/UI work, including `export_for_web` or `dashboard.html`.
- Any unrelated cleanup or refactoring in any file this authorization touches or elsewhere.
- Any change outside the three named production functions and two named tests.
- General release of the §39 existing-code UNMODIFIED hold. The hold remains in force for every file
  and function not named above, including the rest of `modality_classifier.py` and `mythos_sync.py`.
- Release of the successor-contract hold.
- Any amendment to `authorizations.md`'s introductory definition of what this register covers.

### Known residual limitation — recorded, not corrected, not legitimized

`server.py` calls `build_legacy_profile()` directly (`server.py:48`) and has no handling today for an
unresolved outcome distinct from a completed profile. Its current generic-error / non-render behavior
when something goes wrong upstream is **outside this authorization**. This authorization does not
correct that behavior and does not legitimize it as the intended handling of Ruling 001's
`CAUTIONARY`/`BLOCKED` states reaching an HTTP boundary. Encountering this limitation during
implementation is not grounds to expand this authorization's scope to `server.py`; that would require
a separate authorization.

### Verification required before any commit under this authorization lands

- Diff touches only: `modality_classifier.py::classify()`, `modality_classifier.py::classify_fusion()`,
  `mythos_sync.py::build_legacy_profile()`, `test_engine.py::test_unknown_character_defaults_to_grounded`,
  `test_engine.py::test_unknown_characters_still_produce_a_valid_profile`.
- `logic_auditor.py` byte-identical to its pre-commit state (`git diff --stat` empty for that path).
- No Fusion Engine C1–C6 component is introduced anywhere in the diff.
- Full existing test suite (`test_engine.py`, `test_hypothesis_properties.py`) is run, not only the
  two named tests.
- Every test failure, if any, beyond the two intentionally-changed tests is accounted for by name.
- No unrelated refactor or cleanup accompanies the change, in the touched files or elsewhere.

**Acknowledgment** — records Kevin Brown's own determination, in his own words.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-09-14 00:11 EDT
```

Statement: *"I independently authorize the narrow release of the Fusion Engine Requirements §39
'Existing WorldCraft-Visuals code — UNMODIFIED' hold for Seam 1 conformance work only.

This release permits changes only to `modality_classifier.py::classify()`,
`modality_classifier.py::classify_fusion()`, and `mythos_sync.py::build_legacy_profile()`, together
with the corresponding updates to `test_engine.py::test_unknown_character_defaults_to_grounded` and
`test_engine.py::test_unknown_characters_still_produce_a_valid_profile`, for the purpose of
implementing Ruling 001 §4's already-established resolve-then-proceed model and eliminating the
silent unknown/unregistered-character → GROUNDED behavior.

I am exercising this authority independently of `authorizations.md`'s stated scope. I am not
determining that its definition generally encompasses source code, and I am not amending that
definition. AUTH-003 records this operator determination for durability and discoverability; it does
not supply the authority for it.

This authorization does not extend to `logic_auditor.py`, either GAP-4 fallback site, GAP-4
resolution, Fusion Engine C1–C6 implementation, §10.3 / Seam 3, GAP-5, `server.py`, dashboard/UI
work, unrelated cleanup or refactoring, or any other code or test outside the specifically named
scope. The remainder of the §39 existing-code UNMODIFIED hold remains in force, and the
successor-contract hold remains intact.

This authorization does not itself declare Seam 1 implemented or verified. The authorized
implementation must still satisfy AUTH-003's verification requirements before its implementation
commit lands."*

---

## AUTH-004

```
Authorizes:        creation of new, additive Fusion Engine implementation files for the
                   minimum C1 -> C2 -> C3 vertical slice: foundational types, C1
                   (Contribution/Placement Classifier — admission/validation only, no
                   automated semantic classification required), C2 (Provenance Ledger),
                   C3 (Contradiction/Compatibility Evaluator), one integration/pipeline
                   entrypoint, one hand-authored development fixture module, new
                   automated tests for the above, and optionally one minimal demo/
                   __main__ entrypoint
Target scope:      new files only, under a new top-level package (illustratively
                   `fusion_engine/`); minor filename/module-boundary adjustments within
                   this functional scope are permitted, expansion of responsibility
                   beyond it is not
Route:             operator authorization (direct act, permitting new-file
                   implementation of already-locked FE v0.1 requirements; no locked
                   text is amended and no existing-code hold requires release) →
                   recorded here for durability/discoverability → implement → verify
                   against the checklist below → commit
Granted by:        Kevin Brown, operator
Granted at:        2026-09-15 01:39 EDT, in session
Basis:             WorldCraft Fusion Engine Requirements & Architecture Specification
                   v0.1, LOCKED 2026-09-12 (`fusion_engine_requirements_v0.1.md`) —
                   §5 Source Model, §6 Source Preservation, §7 Contribution Types,
                   §8 Architectural Placement, §9/INV-01-08 (Interaction Provenance,
                   Authoritative Provenance, Recursive Provenance), §14/INV-09-11
                   (Contradiction Handling), INV-19 (Partial-Success Preservation);
                   ADR-001, ACCEPTED 2026-09-13
                   (`adr_001_fusion_engine_architecture_reconciliation.md`) — §2's
                   naming and responsibilities for C1/C2/C3, and AD-1's boundary that
                   the Fusion Engine does not read `POWER_REGISTRY`/`CHARACTER_REGISTRY`
                   or call `classify()`/`classify_fusion()`/`audit_power()`/
                   `ground_power()` as part of its own reasoning
Status:            granted; NOT YET EXERCISED — no edit has been made to any file as
                   of this recording
```

**What actually authorizes implementation, and what this entry is.** As with AUTH-003, these are
two different things:

- **The operator authorization** is Kevin Brown's own act, made by acknowledging the statement
  below. That act is what has legal force. It does not derive its authority from this file's own
  stated scope.
- **This AUTH-004 record** is the archive of that act — the durable, discoverable place recording
  that it was made, what it covers, and what it does not.

**On `authorizations.md`'s own stated scope.** As AUTH-003 already recorded (`:359-377`), this
file's introductory text describes itself as recording authorizations "to edit corpus text," and
whether that sentence's stated subject matter generally encompasses source code remains open. This
entry does not resolve that question either, and does not need to: like AUTH-003, its validity
rests on the operator act it records, not on a jurisdictional reading of this file's own
definition.

**Unlike AUTH-003, this entry does not release the FE Requirements §39 "Existing
WorldCraft-Visuals code — UNMODIFIED" hold.** New, additive files are not "existing"
WorldCraft-Visuals code within that hold's plain terms, so no release is required for them. What
this entry supplies instead is the operator authorization act that FE Requirements §41 and
ADR-001 §6 both state is still required before any Fusion Engine implementation — new files
included — may begin: *"implementation remains unauthorized"* until such an act occurs. The §39
hold itself remains fully in force for every existing file, exactly as before.

**This entry decides no new substantive question.** C1, C2, and C3's responsibilities are already
fixed by the locked FE v0.1 specification and ADR-001's accepted architecture, cited above. This
authorization grants permission to build already-governed behavior; it does not further specify
what that behavior must be beyond what those two documents already state.

### What the authorized work must do, stated behaviorally

1. New Fusion Engine code must not read `CHARACTER_REGISTRY` or `POWER_REGISTRY`, and must not
   call `classify()`, `classify_fusion()`, `audit_power()`, or `ground_power()` — per ADR-001 AD-1
   (`adr_001_....md:33-35`).
2. C1 must classify hand-authored Source properties by Contribution Type (§7) and Architectural
   Placement (§8), preserve the preservation-relevant constraints named in §6, and confirm each
   unfused property as Source-Derived (§9.1). Validation/admission of already-classified fixture
   data satisfies this; automated semantic classification is not required.
3. C2 must maintain one authoritative provenance state per tracked item (INV-01) as the sole
   source every other component reads from (INV-02), compute descendant provenance as the
   weakest link across required dependencies and each interaction/rule's own independently
   classified provenance (INV-04, INV-05), propagate that recursively through multi-hop chains
   without any hop resetting it (INV-06), propagate Unresolved dependencies (INV-07), and preserve
   Invented Bridge ancestry visibility throughout the dependency chain (INV-08).
4. C3 must be capable of returning each of Compatible, Conditionally Compatible, Incompatible, and
   Unresolved (§14), with refusal and Unresolved as legitimate successful results rather than
   exceptions, and must not launder a formal contradiction into a false compatible result through
   relabeling, suppression, or hidden exception (INV-11). Explicit deterministic predicates are
   sufficient; general semantic reasoning is not required.
5. The integration path must preserve an independently-classified contribution in the structured
   result even when another interaction's classification is Conditionally Compatible,
   Incompatible, or Unresolved — except where INV-07's own unresolved-dependency propagation
   already excludes that contribution (INV-19).
6. Development fixtures must be clearly labeled as synthetic/development data, must not be named
   or presented as canonical registry entries, and must not require any edit to
   `CHARACTER_REGISTRY` or `POWER_REGISTRY`.

### Relationship to Disposition 002 and GAP-4 — recorded explicitly, not left to be inferred

Disposition 002 (`docs/disposition_002_gap4_grounding_terminal_policy.md`) records Kevin's
substantive determination for GAP-4's eventual invariant. It is authoritative operator input for
future governing text, not an implementation authorization, and authorizes nothing here. This
entry is independent of it: the slice it authorizes does not implement, depend on, or presuppose
GAP-4's eventual resolution, because the authorized code never reaches `logic_auditor.py`'s
grounding layer at all (per AD-1, restated at item 1 above). **GAP-4 remains OPEN**, exactly as
before this entry.

### This authorization does NOT authorize

- Any edit to `logic_auditor.py`, `modality_classifier.py`, `mythos_sync.py`, `server.py`,
  `console.py`, `fantasy_kingdom_generator.py`, or `dashboard.html`. All must remain
  byte-identical.
- Any edit to `CHARACTER_REGISTRY` or `POWER_REGISTRY`.
- C4 (Dominance/Substantive-Participation Evaluator), C5 (Structured Reasoning Record), or C6
  (Presentation Renderer) implementation, in whole or in part.
- Resource-accounting implementation (FE §16/INV-13).
- Real WorldCraft-registry character ingestion into the Fusion Engine Source model.
- Any legacy-engine integration, server/API integration, or dashboard/UI work.
- Any edit to any existing test file (`test_engine.py`, `test_hypothesis_properties.py`), including
  a test-discovery configuration change. If one appears genuinely necessary during implementation,
  that necessity must be stopped on and reported rather than assumed to already be covered here.
- GAP-4 implementation, GAP-4 resolution, or any edit to `open_contract_gaps.md`.
- Any successor-contract work.
- Any unrelated cleanup or refactoring in any file this authorization touches or elsewhere.
- General release of the FE §39 existing-code UNMODIFIED hold. It remains in force for every
  existing file.
- Release of the successor-contract hold.
- Any amendment to `authorizations.md`'s introductory definition of what this register covers.

### Verification required before any commit under this authorization lands

- Diff touches only new files within the authorized implementation scope: the new Fusion Engine
  package (foundational types, C1, C2, C3, pipeline, fixtures), new Fusion Engine test files, and
  optional minimal demo/`__main__` entrypoint — every file named in the exclusion list above is
  absent from the diff.
- No import anywhere in the new code of `logic_auditor`, `modality_classifier`, or `mythos_sync`;
  no reference anywhere to `CHARACTER_REGISTRY` or `POWER_REGISTRY`.
- No C4-, C5-, or C6-shaped component is introduced anywhere in the diff.
- The full existing test suite (`test_engine.py`, `test_hypothesis_properties.py`) still passes,
  unmodified, confirming no accidental coupling was introduced.
- New tests cover at minimum: happy-path C1->C2->C3 execution; authoritative-provenance
  consistency; deterministic repeated execution; malformed/missing-input rejection; unresolved
  provenance propagation; an explicit contradiction/refusal case; and INV-19 partial-success
  preservation — plus foundational tests for provenance rank ordering, provenance-vs-compatibility
  type separation, weakest-link computation, multi-hop ancestry, and all four compatibility
  outcomes.
- Development fixtures are clearly labeled as synthetic/development data in their own text or
  docstrings.
- No unrelated refactor or cleanup accompanies the change.

**Acknowledgment** — records Kevin Brown's own determination, in his own words.

```
Acknowledged (operator): Kevin Brown
Acknowledged at:          2026-09-15 01:39 EDT
```

Statement:

*"I authorize creation of new, additive files implementing the minimum C1 -> C2 -> C3 Fusion
Engine vertical slice — foundational types, C1's admission/validation, C2's provenance ledger, C3's
compatibility evaluator, one integration entrypoint, one hand-authored development fixture, and new
automated tests — under a new top-level package, per the scope and behavioral requirements recorded
in this entry.

This authorization does not extend to `logic_auditor.py`, `modality_classifier.py`,
`mythos_sync.py`, `server.py`, `console.py`, `fantasy_kingdom_generator.py`, `dashboard.html`,
either registry, C4/C5/C6 implementation, resource accounting, real registry ingestion, legacy-
engine or server/dashboard integration, any existing test file, GAP-4 implementation or
`open_contract_gaps.md`, or any successor-contract work. The FE §39 existing-code UNMODIFIED hold
remains in force for every existing file, and the successor-contract hold remains intact.

I acknowledge that Disposition 002 is authoritative operator input for GAP-4's eventual governing
text and is not, and does not function as, an authorization of any kind — it authorizes nothing
here, and this entry authorizes nothing for GAP-4. GAP-4 remains OPEN.

This authorization does not itself declare the C1-C3 slice implemented or verified. The authorized
implementation must still satisfy this entry's verification requirements before its implementation
commit lands."*

---

## AUTH-005

```
Authorizes:        an independent operator determination narrowly releasing
                   FE Requirements §39's "Existing WorldCraft-Visuals code —
                   UNMODIFIED" hold, plus the implementation authority to
                   discharge Contract 002 I8 within that released surface only
Target functions:  logic_auditor.py::_grounding_candidates()
                   logic_auditor.py::ground_power()
                   logic_auditor.py::audit_power()
                   mythos_sync.py::build_legacy_profile() (audit_and_take
                   nested logic only)
                   dashboard.html::openCase() (audit-log/status rendering
                   and all-clear determination only)
                   dashboard.html::renderGrid() (aggregate audit-status
                   reporting only)
Target tests:      test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::
                     test_unsanctioned_family_falls_through_to_the_blanket_default
                   test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::
                     test_unsanctioned_family_is_reported_as_an_ordinary_transposition
                   test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::
                     test_family_set_to_none_also_falls_through
                   plus new regression coverage per the Required Tests
                   section below
Route:             operator determination (independent act, releasing the
                   §39 hold for the named surface) → recorded here for
                   durability/discoverability → implement → verify against
                   the checklist below → commit
Granted by:        Kevin Brown, operator
Granted at:        2026-09-16, in session
Basis:             Contract 002 I8 ("Grounding-Terminal Halting and Causal
                   Preservation"), `contract_002_domain_resolution_invariants.md:190-230`,
                   LOCKED, governing invariant; GAP-4 CLOSED 2026-09-15
                   by `42427a6`, `open_contract_gaps.md:664-712`, naming both
                   fallback sites explicitly — Site 1 `logic_auditor.py:136`
                   (I8(b)) and Site 2 `logic_auditor.py:173-174` (I8(c))
                   (`open_contract_gaps.md:680-683`); the same closure record
                   stating in terms that "it does not authorize any
                   implementation of I8, Seam 2, or any Fusion Engine
                   component" (`open_contract_gaps.md:698-700`) — this entry
                   is what that closure withheld, and closure alone supplies
                   no implementation authority; Disposition 002
                   (`disposition_002_gap4_grounding_terminal_policy.md`),
                   acknowledged 2026-09-15, substantive determination that
                   both conditions halt to `GROUNDING_UNAVAILABLE` with no
                   new generic fallback — Disposition 002 itself likewise
                   authorizes nothing and supplies no implementation
                   authority on its own; ADR-001 Seam 2
                   (`adr_001_fusion_engine_architecture_reconciliation.md:78-84`),
                   confirming the fallback "always terminate[s] in a
                   concrete, legal power with no distinguishable 'unresolved'
                   signal"; Ruling 002 §5.3 (`ruling_002_family_taxonomy_integrity.md:445`),
                   requiring accepted and rejected components both reported,
                   with reason; Ruling 002 §5.4
                   (`ruling_002_family_taxonomy_integrity.md:316-339`), the
                   `Indomitable Will` exception this entry does not disturb;
                   FE Requirements §39, whose hold is released ONLY for the
                   scope named above, and which itself grants no
                   implementation authority — the separate implementation
                   determination below is what supplies that
Status:            granted; NOT YET EXERCISED — no edit has been made to
                   any file as of this recording
```

**What actually releases the hold, what actually authorizes implementation, and what this entry is.** Three separate things, kept separate on purpose, extending AUTH-003's two-act structure to three:

- **The §39 release** is Kevin Brown's own act, stated in his own words below. It releases the hold for the named surface only. It does not, by itself, authorize any implementation — releasing a hold removes a prohibition; it does not supply an affirmative grant.
- **The GAP-4 closure** (`42427a6`, `open_contract_gaps.md:664`) is a separate, prior act. Its own record states plainly that it "does not authorize any implementation of I8, Seam 2, or any Fusion Engine component" (`open_contract_gaps.md:698-700`). Nothing in this entry treats that closure as if it had.
- **The implementation authorization**, below, is a third, independent operator act. It is what actually permits code to be written. It presupposes the §39 release (without it, the named files remain held) but is not identical to it.
- **This AUTH-005 record** is the archive of all three, in the same durable/discoverable form every prior authorization uses. It creates none of the authority it records.

**Relationship to GAP-4's closure — stated because AUTH-004 could say the opposite and this entry cannot.** AUTH-004 authorized work that did not implement, depend on, or presuppose GAP-4's resolution, and recorded "GAP-4 remains OPEN" (`authorizations.md:580-581`, `:650`). That is no longer true of anything this entry touches: **GAP-4 is CLOSED**. This entry exists specifically to implement the invariant whose closure the register already recorded, and which the closure record itself named as unauthorized by the closure act alone. This entry supplies exactly that missing authorization, for the narrow surface named, and for no other purpose. This entry does not reopen, amend, or re-record GAP-4's closure.

### What the authorized work must do, stated behaviorally

Restated from Contract 002 I8(a)-(g), because an authorization that does not state what it is buying cannot be checked against what lands:

1. Where family resolution succeeds but no legitimate grounding candidate exists for the resolved family (`_grounding_candidates()`'s fallback at `:150-156`, reached via the `DEFAULT_TRANSPOSITIONS` constant at `:136`), grounding must halt — I8(b).
2. Where legitimate grounding candidates exist but none is legal under the fusion's modality constraints (`ground_power()`'s `if not candidates:` branch at `:173-174`), grounding must halt on the same basis — I8(c).
3. The terminal outcome for both (1) and (2) is `GROUNDING_UNAVAILABLE` — I8(d). Neither condition may search further, substitute a candidate, or manufacture one merely to return something concrete — I8(d).
4. No new generic or universal grounding fallback is authorized for either condition — I8(e).
5. The distinction between (1) and (2) — whether no legitimate candidate ever existed, or legitimate candidates existed but were all illegal — must remain available in authoritative, machine-readable state, recoverable by any downstream consumer — I8(f). No particular representation, schema, or field is prescribed.
6. **`GROUNDING_UNAVAILABLE` must not be classified, represented, routed, counted, or surfaced as either `TRANSPOSED` or `UNVERIFIED`, anywhere in the diff.** It is the distinct governed terminal outcome required by Contract 002 I8(d), with the I8(b)/I8(c) originating cause remaining machine-recoverable as required by I8(f). This is the governing constraint for items 7, 8, 10, and 11 below, stated once here so it is not read as weaker in any of them.
7. `audit_power()` must be changed so that it does not wrap either terminal outcome into its existing `state: "TRANSPOSED"` branch, and does not represent it via the existing `state: "UNVERIFIED"` branch either — per item 6. Its own docstring names `state` "the authority for downstream consumers"; an unmodified `audit_power()` would itself manufacture the exact misrepresentation item 6 forbids, because it currently wraps whatever `ground_power()` returns as a successful transposition unconditionally.
8. `audit_and_take()` (inside `build_legacy_profile()`, `mythos_sync.py:188-208`) must be changed so that `final = result["transposed_to"] or result["power"]` (`:206`) does not promote the original, declared-illegal power into `approved_powers` when the result is terminal. This is a demonstrated defect in existing code, not new design: as written today, that line would silently re-admit the excluded power the moment `ground_power()` starts returning `None`/a sentinel for a terminal case — exactly I8(d)'s forbidden "fall through to a concrete grounding," reproduced one call frame up.
9. The existing `audit_log` append in `audit_and_take()` (`:199-205`) is already generic over `result["state"]`/`result["message"]` and needs no change to carry a fourth state — the terminal result and its reason propagate through this path automatically once (7) and (8) land.
10. `dashboard.html::openCase()` must represent a `GROUNDING_UNAVAILABLE` audit-log entry distinctly, not through its current unconditional else-branch (`:538-546`, `class="audit-dot ok"`, no reason shown) — verified as an active misrepresentation, not an absence of presentation, because that branch is the literal fall-through for anything not `'transposed'`/`'unverified'`. Per item 6, the distinct representation must not itself be built by reusing the `'transposed'` or `'unverified'` branches. The all-clear determination (`:548`, gated on `transposed.length === 0 && unverified.length === 0`) must also stop asserting "All powers cleared — no transpositions needed" when a grounding-terminal entry is present.
11. **`renderGrid()`'s aggregate reporting must not make a fusion containing one or more `GROUNDING_UNAVAILABLE` audit entries indistinguishable, with respect to aggregate grounding/audit status, from a fusion containing none. `GROUNDING_UNAVAILABLE` must not be counted, classified, represented, or surfaced as either `TRANSPOSED` or `UNVERIFIED` merely to reuse an existing bucket. This requirement does not prescribe or independently authorize any particular new counter, badge, stat tile, or broader dashboard redesign. The implementation must use the minimum change necessary to preserve the distinct terminal outcome accurately in the aggregate view.**
12. Ruling 002 §5.4's `Indomitable Will` exception (`ruling_002_family_taxonomy_integrity.md:325-328`) is not deleted, generalized, or assumed available — I8(g). Its governing predicate (resolution within the human-excellence domain) has no implemented prover today (Disposition 002 §2); until one exists, every case reaching (1) or (2) above resolves to `GROUNDING_UNAVAILABLE`, never to `Indomitable Will`, regardless of which power is involved.
13. All existing, non-GAP-4 grounding behavior is unchanged. This is verifiable directly: every real `POWER_REGISTRY` entry (30/30) carries a sanctioned family with a legal LEGACY-rank kin, so no code path reachable with current registry data is altered by this authorization — confirmed, not assumed, by the read-only propagation analysis this entry is drafted from.

### This authorization does NOT authorize

- Any edit to `logic_auditor.py`, `mythos_sync.py`, or `dashboard.html` outside the six named functions/surfaces above.
- Any edit to `POWER_REGISTRY`, `TRANSPOSITION_MAP`, `CHARACTER_REGISTRY`, or any registry/taxonomy content.
- Any edit to `modality_classifier.py`, or any Seam 1 work. AUTH-003's scope and exclusions stand untouched.
- Any edit to `fusion_engine/`, any C1-C6 component, or `fusion_engine/tests/`. AUTH-004's scope and exclusions stand untouched; this entry does not extend it.
- Any edit to `open_contract_gaps.md`. GAP-4 is already CLOSED and this entry does not reopen, amend, or re-record that closure.
- GAP-5 — untouched, "proposed / not operative" exactly as the closure record left it (`open_contract_gaps.md:696-697`).
- Any edit to Contract 002, Ruling 002, Ruling 001, Contract 001, Disposition 002, or ADR-001 — all LOCKED or otherwise not amendable by this entry.
- Any new generic or universal grounding fallback, for either I8(b) or I8(c) — I8(e) is exclusionary, not merely silent.
- **Classifying, representing, routing, counting, or surfacing `GROUNDING_UNAVAILABLE` as either `TRANSPOSED` or `UNVERIFIED`, anywhere in the diff, including inside `dashboard.html`'s counters and all-clear text.** This does not authorize redesigning unrelated state machinery, or changing the existing meaning of `TRANSPOSED` or `UNVERIFIED` for any other case.
- Broadening Ruling 002 §5.4 by analogy, extension, or by treating its predicate as satisfied without an actual domain-resolution capability.
- Any dashboard redesign, new UI infrastructure, or new test framework introduced merely because `dashboard.html`/`server.py` currently have zero automated test coverage. The absence of existing coverage is not license to build coverage infrastructure beyond the narrowest mechanism that regression-guards the two authorized dashboard changes.
- Any edit to `server.py` or `console.py`. Both confirmed, by direct reading, to contain no status-dependent logic this entry's changes could affect.
- Any edit to `test_engine.py`. Confirmed by direct reading that every relevant assertion there draws from real, sanctioned-family registry data and is unaffected by this entry's changes; if implementation evidence shows otherwise, that is grounds to stop and report, not to proceed.
- Any edit to any test in `test_hypothesis_properties.py` other than the three named above, and the new coverage named below.
- Solving the `signature_ability = approved_powers[0]` all-terminal edge case (`mythos_sync.py:232`). Recorded as a known, currently-dormant limitation — the same structural dormancy property that keeps GAP-4 itself unreachable with current registry data keeps this edge case unreachable too. If implementation evidence shows the authorized changes make it reachable with current real data, that is grounds to stop and report, not to expand this authorization's scope to cover it.
- Any unrelated cleanup or refactoring in any file this authorization touches or elsewhere.

### Required tests

**Deliberate revision required** (fact-finding assertions pinning pre-fix behavior, explicitly not regressions to preserve):
- `test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::test_unsanctioned_family_falls_through_to_the_blanket_default` — currently asserts `_grounding_candidates(name) == DEFAULT_TRANSPOSITIONS`; must assert the I8(b) terminal instead.
- `test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::test_unsanctioned_family_is_reported_as_an_ordinary_transposition` — currently asserts `state == "TRANSPOSED"` and no `cautionary` field; must assert the new terminal state and that the two causes are distinguishable.
- `test_hypothesis_properties.py::Gap4UnresolvedFamilyTests::test_family_set_to_none_also_falls_through` — same fallback site as the first, `family: None` variant; same revision.

**Unchanged, confirmed by direct code reading, not assumed:**
- `test_missing_family_key_raises_rather_than_falling_through` — different code path (`family_of` raises `KeyError` before any fallback logic runs).
- `test_unregistered_power_never_reaches_grounding` — different code path (`audit_power`'s `UNVERIFIED` short-circuit, before grounding is attempted).
- `GeneratedInvariantTests` in the same file, and all of `test_engine.py` — both draw exclusively from `REGISTERED_POWERS = tuple(sorted(POWER_REGISTRY))`, real data only, which never reaches either dormant site.

**New regression coverage required** (none of this exists today — confirmed by full-file reads, not inferred):
- I8(c): a case where legitimate grounding candidates exist but all are illegal for the fusion. No existing test constructs this; every current GAP-4 test targets I8(b) only.
- I8(f): a case proving the I8(b) and I8(c) causes remain distinguishable from each other in the returned state, not just distinguishable from `APPROVED`/`TRANSPOSED`.
- `audit_power()` returns the terminal state, and not `TRANSPOSED` or `UNVERIFIED`, for both (b) and (c).
- `audit_and_take()`/`build_legacy_profile()` does not promote a terminal/rejected power into `approved_powers`.
- Existing valid (non-GAP-4) grounding behavior is unchanged — a regression check over real registry data, not merely inferred from the analysis above.
- The narrowest reasonable regression mechanism for the two authorized `dashboard.html` changes, covering both the `openCase()` distinct-representation requirement and the `renderGrid()` aggregate-accuracy requirement. No dashboard test framework exists today; this authorization does not license building one. Implementation must find or state the minimum mechanism (e.g., a pure-function extraction of the affected rendering logic, or a documented manual verification step) rather than treating the absence of a framework as permission to add one.

### Known residual limitation — recorded, not corrected, not legitimized

`mythos_sync.py:232`'s `signature_ability = approved_powers[0]` would raise `IndexError` if every candidate in every pool terminated `GROUNDING_UNAVAILABLE`. This is unreachable with current real registry data (same dormancy property as GAP-4 itself) and has no sanctioned fix under I8(e)'s prohibition on new universal fallbacks. This authorization does not correct it and does not legitimize the current absence of a fix. Encountering it during implementation is not grounds to expand this authorization's scope; that would require a separate authorization.

### Verification required before any commit under this authorization lands

- Diff touches only: the six named functions/surfaces, the three named test revisions, and the new tests required above.
- `modality_classifier.py`, `server.py`, `console.py`, `fantasy_kingdom_generator.py`, every file under `fusion_engine/`, and `open_contract_gaps.md` byte-identical to their pre-commit state.
- No edit to `POWER_REGISTRY`, `TRANSPOSITION_MAP`, or `CHARACTER_REGISTRY` content.
- The full existing test suite (`test_engine.py`, `test_hypothesis_properties.py`, `fusion_engine/tests`) run, not only the touched tests; every failure beyond the three intentionally-revised tests accounted for by name.
- No occurrence anywhere in the diff of `GROUNDING_UNAVAILABLE` being assigned `state`/`status` value `"TRANSPOSED"` or `"UNVERIFIED"`, and no occurrence of it being counted by any `'transposed'`-keyed or `'unverified'`-keyed filter.
- `renderGrid()`'s aggregate reporting, post-change, does not make a fusion containing one or more `GROUNDING_UNAVAILABLE` entries indistinguishable from a fusion containing none, and does not achieve this by counting or classifying `GROUNDING_UNAVAILABLE` as `TRANSPOSED` or `UNVERIFIED`. No new counter/badge/stat tile exists in the diff unless it is the minimum change necessary to satisfy this requirement.
- `Indomitable Will` does not appear as a returned grounding target from either I8(b) or I8(c)'s branch anywhere in the diff, absent an implemented, provable §5.4 domain predicate (none is authorized or expected to exist after this commit).
- The I8(b)/I8(c) distinction is present in the returned state in a form a new test can assert against — not merely asserted in a docstring or comment.
- No unrelated refactor or cleanup accompanies the change, in the touched files or elsewhere.

**Acknowledgment** — records Kevin Brown's own determinations and authorization, in his own words, given across two statements in this session.

```
Acknowledged (operator): Kevin Brown
Acknowledged at:          2026-09-16 14:50 EDT
```

Statement 1 — §39 release (as given, with the `renderGrid()` paragraph carried forward in its final, synchronized form per this entry's own correction):

*"I release the §39 UNMODIFIED hold, narrowly, for `logic_auditor.py::_grounding_candidates`, `logic_auditor.py::ground_power`, `logic_auditor.py::audit_power`, `mythos_sync.py::build_legacy_profile` (`audit_and_take` logic only), and the two demonstrated `dashboard.html` consumer surfaces: `openCase()`'s audit-log/status rendering and all-clear determination, and `renderGrid()`'s aggregate audit-status reporting — solely to implement and accurately surface Contract 002 I8(a)–(g), preserving I8(f)'s distinction between the two `GROUNDING_UNAVAILABLE` causes and I8(g)'s Ruling 002 §5.4 restriction exactly as written, and for no other purpose.

`renderGrid()`'s aggregate reporting must not make a fusion containing one or more `GROUNDING_UNAVAILABLE` audit entries indistinguishable, with respect to aggregate grounding/audit status, from a fusion containing none. `GROUNDING_UNAVAILABLE` must not be counted, classified, represented, or surfaced as either `TRANSPOSED` or `UNVERIFIED` merely to reuse an existing bucket. This requirement does not prescribe or independently authorize any particular new counter, badge, stat tile, or broader dashboard redesign. The implementation must use the minimum change necessary to preserve the distinct terminal outcome accurately in the aggregate view.

All other §39-held code, every other function or section of those files, and every other existing WorldCraft-Visuals file remain under the §39 UNMODIFIED hold exactly as recorded."*

Statement 2 — implementation authorization (as given):

*"I authorize the narrowly scoped implementation described by AUTH-005, and no broader work. The implementation may modify only the released functions and dashboard surfaces named in AUTH-005, together with the specifically authorized test revisions and new regression coverage, solely to enforce and accurately propagate Contract 002 I8(a)–(g).

The implementation must make both governed grounding-failure conditions halt as `GROUNDING_UNAVAILABLE`, preserve which condition occurred in machine-recoverable authoritative state, prevent either terminal from being converted back into a successful transposition or approved power downstream, and prevent the authorized dashboard surfaces from presenting the terminal as cleared, approved, `TRANSPOSED`, `UNVERIFIED`, or otherwise invisible in aggregate grounding/audit status.

Ruling 002 §5.4 remains exactly as governed. This authorization does not broaden or presume the `Indomitable Will` exception, authorize a domain resolver, create a generic fallback, modify registry or taxonomy content, touch GAP-5, modify the Fusion Engine/C2, reopen GAP-4, or authorize unrelated cleanup or refactoring.

The known all-terminal `signature_ability = approved_powers[0]` edge case remains outside this authorization. If implementation evidence shows that this authorization makes that condition reachable with current real registry data, stop and report rather than expanding scope.

AUTH-005 may be recorded in `docs/authorizations.md` with this implementation statement and the previously given §39 release statement. Recording AUTH-005 does not authorize anything beyond the exact scope AUTH-005 records."*

---

## Authorization Exercise and Closure

An authorization recorded in this register is a bounded, one-time grant.

This lifecycle rule governs the exercise and closure of entries recorded in this register. Its application to an existing entry does not determine, ratify, or generalize the register's subject-matter jurisdiction, including the unresolved question of whether future source-code authorizations generally belong in this register.

### 1. Grant state

At the time an authorization is granted and recorded, its operative lifecycle state is `GRANTED — NOT YET EXERCISED`.

Existing authorization records that express that grant-time state using formatting such as `granted; NOT YET EXERCISED` represent the same lifecycle state for purposes of this rule.

That state describes the authorization at the time of its grant. It does not constitute a perpetual assertion that the authorized act has never subsequently occurred.

### 2. Exercise and spend

For purposes of this rule, the `authoritative branch` is the repository branch whose landed state constitutes authoritative project history for the authorization at issue. Where an authorization does not expressly identify another branch or repository state for exercise, the authoritative branch is `main`.

An authorization becomes `EXERCISED AND SPENT` upon the first qualifying exercise: the first time any part of the authorized act, as scoped by that authorization, lands on the authoritative branch or otherwise reaches a repository state that the authorization expressly identifies as constituting exercise.

Exercise and spend are one atomic lifecycle transition. They are not separate sequential states.

There is no partial-exercise state. The first qualifying exercise spends the authorization in full. Any portion of the original authorized scope not exercised in that qualifying act carries no residual authority and requires independent authority before it may later be exercised.

Accordingly, where an authorization permits multiple edits, surfaces, components, tests, or other acts, the first qualifying exercise of any one or more of them spends the entire authorization unless that authorization expressly defines a different exercise condition.

Once an authorization is `EXERCISED AND SPENT`, the authority granted by that authorization may not be reused to authorize another edit, commit, merge, or governance act.

Any further act requires independent authority.

### 3. Closure recording

Exercise does not retroactively alter the historical fact that the authorization was unexercised when originally granted.

Accordingly, the original grant record, including its original `Status:` statement, must not be rewritten solely to reflect later exercise.

Exercise is recorded append-only within that authorization's entry by adding a closure record.

The closure record must identify:

* `Exercise status: EXERCISED AND SPENT`
* `Landed as:` the immutable commit SHA establishing the first qualifying exercise
* `Exercise recorded at:` the timestamp at which the closure record is added

Where the first qualifying exercise occurred through a pull request, the closure record should also identify:

* `Pull request:` the applicable PR number

Additional immutable repository evidence may be recorded when necessary to establish or preserve the exercise chain, but is not required merely because such evidence exists.

### 4. Exercise time and recording time

The act that exercises an authorization and the later act that records that exercise are distinct.

`Landed as:` identifies the repository event that first exercised and spent the authorization.

`Exercise recorded at:` identifies when that already-existing exercise was entered into this register.

A later closure record must not imply that the authorization remained operative between its actual exercise and the later recording of that exercise.

Absence or delay of a closure record does not preserve, restore, or reactivate authority that was already spent by a qualifying exercise.

### 5. Historical closure

An authorization exercised before adoption of this closure convention may be brought into conformity by appending a closure record supported by immutable repository evidence.

Such a record documents prior exercise; it does not newly exercise the authorization, recreate the authorization, extend it, or alter the scope originally granted.

Once this closure convention has been adopted by the operator, recording a historical closure whose first qualifying exercise is already established unambiguously by immutable repository evidence is a mechanical register-maintenance act and does not require a new operator acknowledgment for that individual closure.

Mechanical historical closure may record only what the immutable repository evidence establishes. It may not manufacture, presume, or supply missing evidence.

If the available repository evidence does not establish the first qualifying exercise unambiguously, the historical authorization must not be closed mechanically. The uncertainty must instead be surfaced for operator determination.

### 6. Scope and jurisdiction preservation

Closing an authorization does not amend, broaden, narrow, reinterpret, ratify, or supersede the authority originally granted.

The authorization's original scope, exclusions, conditions, acknowledgments, historical grant state, and any express unresolved questions remain part of the record.

Application of this lifecycle rule to an existing authorization establishes only that the recorded authorization was exercised and that its one-time authority is spent. It does not establish that the authorization's placement in this register resolved any previously open question about the register's general subject-matter jurisdiction or the proper placement of future authorizations.

### Adoption

Adopted by: Kevin Brown, operator
Adopted on: 2026-09-16 19:00 EDT

---

## Authorization Exercise and Closure — Amendment 1 (Closure Placement)

This is Amendment 1 to the `Authorization Exercise and Closure` rule adopted 2026-09-16. It
affects §3 ("Closure recording") only. The original September 16 text, and its own
`Adopted by: Kevin Brown, operator` / `Adopted on: 2026-09-16 19:00 EDT` block, remain
unedited and historically accurate as attesting to the rule as it read on that date. This
amendment does not retroactively alter what that adoption attested to.

### What this amendment adds

§3's general rule is unchanged and remains the default: a closure record is recorded
append-only within that authorization's own entry.

**Narrow exception.** Where recording a closure record within that authorization's own entry
would cause an existing citation — from a document that cannot itself be corrected, including
but not limited to a document carrying LOCKED status — to become a stranded citation (a
citation that would no longer accurately identify the material it presently identifies), the
closure record for that authorization may instead be recorded in a dedicated, append-only
closure section placed at the tail of this register, after every existing AUTH entry and after
this lifecycle rule's own text.

This exception does not apply merely because an insertion would change a line number. It
applies only where the shift would cause a citation to stop identifying its intended material,
and only where that citation cannot be corrected by a compliant, separately authorized edit to
the document that carries it. An ordinary citation in an editable, unattested document is not,
by itself, evidence that this exception applies.

Convenience, consistency of formatting, or ease of future maintenance are not evidence that
this exception applies and do not trigger it.

### Attribution requirement for a remotely placed closure

A closure record placed under this exception must identify, with no ambiguity, which
authorization it closes, by AUTH number, and must contain every field §3 already requires:
`Exercise status:`, `Landed as:`, `Exercise recorded at:`, and `Pull request:` where applicable.

### What this amendment does not do

It does not change the meaning of `GRANTED — NOT YET EXERCISED`, `EXERCISED AND SPENT`, first
qualifying exercise, the authoritative-branch definition, express alternate exercise
conditions, atomic exercise/spend, the no-partial-exercise/no-residual-authority rule,
`Landed as:`, `Exercise recorded at:`, PR evidence, or any historical-closure eligibility
requirement in §5. A closure record — whether placed in-entry or under this exception — may
still be added only for an authorization whose first qualifying exercise is already
established unambiguously by immutable repository evidence; this amendment supplies no
evidence and creates no new closure eligibility.

It does not authorize any edit to any document other than `docs/authorizations.md`, and no
edit to any LOCKED document under any circumstance. It creates no citation-repair authority
and no general reference-maintenance power.

It does not address, resolve, or imply resolution of the unresolved question preserved by this
rule's own opening paragraph and §6, concerning whether future source-code authorizations
generally belong in this register.

### Adoption

Adopted by: Kevin Brown, operator
Adopted on: 2026-09-16 20:36 EDT

---

## AUTH-006

```
Authorizes:        creation of one new top-level file, test_regression_case_001.py,
                   protecting Regression Case 001 against recurrence of the
                   unauthorized Hashirama Senju x William Vangeance profile
Target scope:      one new file, repository root; no existing file modified;
                   no existing-code hold other than the one scope determination
                   below is touched
Route:             operator determination (independent act; FE Requirements
                   §39 scope determination, recorded below) -> recorded here ->
                   implement on a dedicated branch -> verify against the
                   checklist below -> PR -> merge
Granted by:        Kevin Brown, operator
Granted at:        2026-10-24, in session
Basis:             Ruling 001 §6, Normalization Regression Case 001
                   (`ruling_001_canonicalization_policy.md`), naming
                   "Unknown character/power silently became GROUNDED" as
                   failure #1 under Invariant 1; the preserved exhibit
                   `docs/evidence/regression_case_001.json` (sha256
                   3fa4d990c7877b63a5796bf33c43c28a0dc0c66f7c1df91d0279ffcb50fb86ac,
                   see `docs/evidence/README.md`); AUTH-003 (Seam 1
                   conformance, implemented at `c7f0ab7`); FE Requirements
                   §39, whose hold is neither released nor modified by this
                   entry
Status:            granted; NOT YET EXERCISED — no file within the scope of
                   this authorization has been created as of this recording
```

**What actually authorizes this, and what this entry is.** Two operator acts and one record, kept
separate on purpose:

- **The §39 scope determination** is Kevin Brown's own act, stated in his own words below. It
  determines that one named additive file lies outside the existing-code hold. It releases nothing
  and grants no implementation permission.
- **The AUTH-006 authorization** is Kevin Brown's own act, stated in his own words below. It is
  what permits the one implementation slice.
- **This AUTH-006 record** is the archive of those acts — the durable, discoverable place recording
  that they were made, what they cover, and what they do not. It creates no authority. Appending
  this record is a documentation-only act; it is not the implementation slice and does not exercise
  AUTH-006.

**Preserved issuance record (outside the repository, not part of the corpus).** The operator's
issuance message was preserved verbatim in `WorldCraft-Evidence` before this entry was written:

- Path: `C:\Users\User\WorldCraft-Evidence\OPERATOR_ISSUANCE_FE_SECTION_39_SCOPE_AND_AUTH_006_20261024T210928-0400.txt`
- Size: 8768 bytes
- SHA-256: `29f6b124dbf4db0122e90f4a4430178493b9f9454581f9cd8db464e15b7d68ff`
- Written: 2026-10-24 21:09:49 -0400 (file modification time — when the record was written, not
  necessarily when the operator sent the message)
- Form: UTF-8, LF, no BOM, no trailing newline. Transcribed by Claude Code from the message as
  received in session; byte-level identity with the operator's original transmission is not
  independently verifiable from inside the session.

The quoted blocks below are generated from that file mechanically, not retyped.

### Operator statement

> I hereby issue the following two operator acts.

### FE Requirements §39 scope determination (operator, verbatim)

> I determine that creating the new top-level file `test_regression_case_001.py`, without modifying any existing repository file, is additive work outside the FE Requirements §39 hold on existing WorldCraft-Visuals code.
>
> This determination applies only to that named file.
>
> All existing-code holds remain unchanged. This determination alone grants no implementation permission.
>
> AUTH-004's treatment of additive files is precedent, not the source of this independent determination.

### AUTH-006 authorization (operator, verbatim)

> I authorize one implementation slice: creation of the new top-level file `test_regression_case_001.py` to protect Regression Case 001 against recurrence of the unauthorized Hashirama Senju × William Vangeance profile.
>
> This authorization is single-use and subject to the existing Authorization Exercise and Closure rule in `docs/authorizations.md`.
>
> ### Authorized scope
>
> - Create only `test_regression_case_001.py` in the repository root.
> - Read `docs/evidence/regression_case_001.json` without modifying it.
> - Use standard-library `unittest` and existing public functions.
> - Implement the permanent regression detector and separately named baseline test.
> - Work on a dedicated branch, verify the implementation, and prepare a PR.
>
> ### Required test behavior
>
> 1. Derive the exact character names and dominance value `50` from the preserved exhibit.
>
> 2. Reject the unauthorized `GROUNDED` classification with the `unknown` tag. Neither condition alone constitutes the prohibited combination.
>
> 3. Reject a `lore_summary` containing `"Unknown Entity"`.
>
> 4. Reject the exact Espionage / One-Inch Punch / Psychological Mastery power set. Do not reject an individual power or a larger set merely because it contains those powers. Document that this check is supplementary because the original power draw was random.
>
> 5. Use a generated-profile-field denylist for `CAUTIONARY` results, not a result-key allowlist. The denylist covers:
>    - `approved_powers`
>    - `power_families`
>    - `dominant_family`
>    - `signature_ability`
>    - `influence_pattern`
>    - `rhetorical_style`
>    - `lore_summary`
>    - `audit_log`
>    - `biome`
>
>    Do not prohibit a future `reason` field merely because it adds a key to the result.
>
> 6. Verify that the permanent detector identifies the preserved exhibit's failure signatures. The detector must not pass vacuously.
>
> 7. Keep the registry-absence precondition in the baseline test only. The permanent regression tests must not depend on either character remaining unregistered.
>
> 8. Keep permanent regression protection independent of the current `CAUTIONARY` baseline.
>
> 9. Include a separately named baseline test confirming the current `4cedae0` behavior: `CAUTIONARY`, no modality, and no generated profile. Its docstring must explain that a future authorized resolver change may require a separately authorized modification of this existing baseline test.
>
> 10. If randomness is involved, save the random state, seed deterministically, and restore the state afterward. Do not use repeated random trials as a substitute for deterministic verification.
>
> 11. Suppress console output during test execution using an appropriate standard-library mechanism.
>
> ### Explicit exclusions
>
> - No modifications to existing source files.
> - No modifications to existing test files.
> - No modifications to character registries, evidence, CI configuration, or lore.
> - Do not call `save_to_matrix` or `export_for_web`.
> - Do not modify `containment_matrix.json`.
> - Do not implement reason-travel remediation.
> - Do not modify dashboard rendering or case-detail behavior.
> - Do not implement a resolver.
> - Do not undertake successor-contract work.
> - Do not modify or release any other §39 hold.
> - No `Co-Authored-By` trailer in any commit.
> - No `"Generated with Claude Code"` line in the PR body.
>
> The implementation authorization covers one new test file only. The separate documentation-only recording act described below is not part of that implementation-file allowance.

### Implementation sequence after recording (operator, verbatim)

The operator's Stage A (preservation and recording of this entry) is the act that appends this
record. The operator's Stage B follows, and its gate is part of this authorization:

> Stage B may begin only after Stage A has been recorded, verified, pushed with my approval, and separately released to proceed.
>
> 1. **Create a dedicated implementation branch from `main` at the pushed Stage A documentation commit.**
>
> 2. Create only the authorized top-level file `test_regression_case_001.py`.
>
> 3. Implement the permanent regression detector and separately named baseline test according to §2.
>
> 4. Run:
>    - The new regression test.
>    - The existing `test_engine` suite.
>    - The existing `fusion_engine/tests` suite.
>    - The applicable CI test-discovery command.
>
> 5. Verify that `docs/evidence/regression_case_001.json` remains unchanged and has SHA-256:
>
>    `3fa4d990c7877b63a5796bf33c43c28a0dc0c66f7c1df91d0279ffcb50fb86ac`
>
> 6. Verify that `containment_matrix.json` remains byte-identical to its pre-test state.
>
> 7. Verify that the implementation diff against the pushed Stage A documentation commit contains exactly one added file, `test_regression_case_001.py`, and no modified or deleted files.
>
> 8. Commit without a `Co-Authored-By` trailer.
>
> 9. Obtain my explicit confirmation before pushing the implementation branch.
>
> 10. Obtain separate explicit confirmation before opening the PR.
>
> 11. Verify the PR's CI results and report the authorization's exercise status according to the existing Authorization Exercise and Closure rule.
>
> Do not claim AUTH-006 is spent merely because a branch commit exists. Apply the existing lifecycle rule to determine when the qualifying exercise occurs.

### Boundaries (operator, verbatim)

> The following issues remain outside AUTH-006:
>
> - The dashboard crash when `renderGrid()` encounters a `CAUTIONARY` result with `modality: null`.
> - The separate `openCase()` handling of nullable modality and future reason display.
> - The missing governed reason in the returned `CAUTIONARY` result.
> - Resolver implementation and domain/family resolution.
> - Successor-contract Draft v1 and its fidelity findings.
> - Any additional FE Requirements §39 hold release.
>
> The dashboard and reason-travel issues are candidates for a separately scoped future AUTH-007, not permission to change them now.
>
> Do not silently broaden AUTH-006 to repair related defects.
>
> Do not introduce additional governance work unrelated to the authorized regression test.

### Lifecycle

AUTH-006 is subject to the `Authorization Exercise and Closure` rule in this register
(`authorizations.md:833` onward) and defines no exercise condition of its own, so that rule's
defaults apply. Appending this entry is not a qualifying exercise. A commit on an implementation
branch is not, by itself, a qualifying exercise. Exercise status and any closure record are
determined under that rule when the time comes and are not asserted here.

### On `authorizations.md`'s own stated scope

Recorded explicitly, as AUTH-003 recorded it (`authorizations.md:359-377`):

1. `authorizations.md`'s introductory text (`authorizations.md:3-5`) describes the register as
   recording authorizations "to edit corpus text". Read strictly, that sentence does not mention
   source code or test files.
2. This entry does **not** determine that the register's subject matter generally encompasses source
   code or tests, and decides nothing about the register's jurisdiction over code.
3. This entry does **not** expand or amend the register's introductory definition, and does not
   depend on it being read broadly.
4. The §39 scope determination and the AUTH-006 authorization are independent operator acts; their
   authority comes from Kevin Brown's own determination, not from this register's jurisdiction.
5. Whether future code authorizations generally belong in this register, and under what definitional
   revision, is **not decided here** and remains open
   (`authorizations.md:837` records the same reservation).
6. AUTH-006's validity does not depend on resolving that question. If the register's scope is later
   formally extended to code, or code authorizations are later routed elsewhere, this entry's
   validity is unaffected either way.
7. AUTH-004's treatment of additive files (`authorizations.md:532-534`) is precedent only. The
   operator stated that it is not the source of the §39 scope determination above.

### Placement

This entry is appended after the final line of the register as it stood at `4cedae0` (line 980),
at the operator's direction, so that no existing line moves. Its position after the lifecycle rule
and Amendment 1 carries no meaning, and it amends neither.

### AUTH-006 — Closure record

```
Exercise status:        EXERCISED AND SPENT
Landed as:              2e5cba46ad75e07562d161a00b1f4bed48749553
Pull request:           #5
Exercise recorded at:   2026-10-24 22:27:38 -0400
```

The first qualifying exercise was the merge of PR #5 into `main`, a merge commit made
2026-10-25T02:23:57Z (2026-10-24 22:23:57 -0400). Under "Authorization Exercise and Closure" §2,
that is the first time any part of the authorized act landed on the authoritative branch. This
record was added later; per §4 it documents an exercise that had already occurred and does not
imply AUTH-006 remained operative between the merge and this recording.

Recorded because the merge SHA alone does not identify which reviewed commit was merged:

- Second parent of the merge: `8b9409e5c20e7edb343b6fbedc0216bf6f0ff677`, the implementation commit, landed unchanged.
- The merge adds exactly one file, `test_regression_case_001.py`, and modifies no existing file.
  Its SHA-256 on `main` is `5cebe62e734edaa200afb04b0398fa0651ff363c274f140bd4ba067489babe44`.

Per §6, this closure does not amend, broaden, narrow, reinterpret, ratify, or supersede
AUTH-006's scope. AUTH-006's grant record, including its original `Status:` line, is unchanged
and the question of the register's jurisdiction over code remains as the grant record left it.
This record authorizes nothing further, including any future AUTH-007 candidate.

---

## AUTH-007

```
Authorizes:        two bounded edits to dashboard.html and one new top-level test
                   file, so that a CAUTIONARY entry (modality: null) neither crashes
                   renderGrid() nor causes loadMatrix() to report a false
                   missing-file message
Target scope:      dashboard.html::renderGrid() (card template, entries whose
                   modality is null only)
                   dashboard.html::loadMatrix() (error handling only)
                   one new top-level test file under test_*.py discovery
Route:             operator determination (independent act; FE Requirements
                   §39 release, recorded below) -> implement on a dedicated
                   branch -> verify against the checklist below -> this entry lands
                   in the same PR as the fix -> operator review of the diff and
                   test evidence -> PR merge on the operator's explicit approval ->
                   closure record
Granted by:        Kevin Brown, operator
Granted at:        2026-10-25, in session
Basis:             Ruling 001 §4 (`ruling_001_canonicalization_policy.md:209-218`),
                   under which a CAUTIONARY result carries no modality and emits
                   no fusion output; `mythos_sync.py:159-165`, which returns
                   `{"fusion_name", "state": "CAUTIONARY", "modality": None}`;
                   `server.py:48-50`, which persists that result into
                   `containment_matrix.json`; the AUTH-006 boundaries
                   (`authorizations.md:1159-1168`), which named this crash as
                   outside AUTH-006 and as a candidate for a separately scoped
                   future AUTH-007; FE Requirements §39
                   (`fusion_engine_requirements_v0.1.md:1397`, `:1402`), whose
                   hold is released ONLY for the two surfaces named above
Status:            granted; NOT YET EXERCISED — no file within the scope of
                   this authorization has landed on main as of this recording
```

**What actually authorizes this, and what this entry is.** Three operator acts and one record, kept
separate on purpose:

- **Act 1 — the §39 release** is Kevin Brown's own act, stated in his own words below. It removes
  a prohibition and grants nothing.
- **Act 2 — the implementation authorization** is Kevin Brown's own act. It is what permits the two
  `dashboard.html` edits.
- **Act 3 — the new-file determination** is Kevin Brown's own act. It is what permits the one new
  test file.
- **This AUTH-007 record** is the archive of those acts. It creates no authority. Per the operator's
  issuance, the acts take effect on issue and the operator stated that implementation may begin
  before this entry lands; this entry lands in the same PR as the fix.

**Issuance record.** The operator's issuance message is quoted below as received in session. It was
not separately preserved outside the repository before this entry was written, so byte-level identity
with the operator's original transmission is not independently verifiable from inside the session.

### Operator statement

> AUTH-007 — issued by the operator, 2026-10-25. Three separate acts.

### Act 1 — §39 release (operator, verbatim)

> I release the FE §39 UNMODIFIED hold on dashboard.html, limited to two surfaces: (a) the renderGrid() card template’s handling of entries whose modality is null, and (b) loadMatrix()’s error handling. Every other function or section of dashboard.html, and all other §39-held code, remain held exactly as recorded. This release removes a prohibition and grants nothing.

### Act 2 — Implementation authorization (operator, verbatim)

> I authorize exactly:
>
> In renderGrid(), entries with modality == null get their own card: badge text from f.state, no signature or biome lines, no onclick, no invented reason text.
> In loadMatrix(), fetch failures and rendering failures are reported separately. The missing-file message appears only when the fetch fails or returns a non-OK response. A rendering exception is shown as a rendering failure and logged to the console with its error message. Neither kind of failure is silently discarded, and no cause is invented for either.

### Act 3 — New-file determination (operator, verbatim)

> I authorize one new top-level test file under test_*.py discovery. It runs the dashboard script under node in a vm with a fake DOM and in-memory fetch. It fails, and does not skip, if node is unavailable. Its fixture is the literal CAUTIONARY stub dict, not build_legacy_profile(). It never calls save_to_matrix or export_for_web and never touches containment_matrix.json. It asserts:
>
> for [normal entry, CAUTIONARY stub], one card renders per entry and no missing-file message appears;
> a forced rendering exception does not produce the missing-file message;
> a failed fetch still produces it.
>
> It must fail against the current dashboard.html and pass after the fix.

### Explicit exclusions (operator, verbatim)

> Exclusions: openCase() in full, including reason display; CAUTIONARY persistence in server.py; the governed CAUTIONARY reason (Contract 003 I5); the “Total” tile; the Hypothesis flake and all existing tests; CI config; resolver work; successor-contract work; every other §39 hold; AUTH-005 closure.

### Verification (operator, verbatim)

> Verification: all CI suites pass; the new test fails before the fix and passes after; containment_matrix.json is byte-identical; the diff touches only dashboard.html, the new test file, and docs/authorizations.md.

### Recording and attribution (operator, verbatim)

> Recording: this message is the authorization and takes effect on issue, so implementation may begin now. The AUTH-007 entry in docs/authorizations.md records it and lands in the same PR as the fix. A closure record follows the merge. If you find any provision requiring the register entry to land before implementation, stop and report it with the citation before writing code.
>
> Attribution: no Co-Authored-By trailer and no “Generated with Claude Code” line on AUTH-007 commits or PRs.
>
> AUTH-007 is exercised and spent on merge to main. It authorizes nothing further.

### Merge gate (operator instruction, same message)

> Before merging, stop and present the diff and test evidence (including the pre-fix failure) for operator review. Do not merge without my explicit approval

### Provision check required by the recording instruction

The operator directed that any provision requiring this entry to land before implementation be
reported before code was written. A pattern search across all of `docs/authorizations.md`, together with
full reads of the `Authorization Exercise and Closure` rule and its Amendment 1, AUTH-005 and AUTH-006,
found no such requirement. The "recorded, then implement" sequences in AUTH-005 and AUTH-006 are routes
stated in those entries and are not a general rule. AUTH-001 to AUTH-004 were searched by pattern but not
read in full, and the search covered `docs/authorizations.md` only; it was not an exhaustive sweep of the
governance corpus.

### Lifecycle

AUTH-007 is subject to the `Authorization Exercise and Closure` rule in this register
(`authorizations.md:833` onward). The operator's issuance states that AUTH-007 is exercised and spent on
merge to `main`, which is that rule's default exercise condition (§2). Appending this entry is not a
qualifying exercise. A commit on an implementation branch is not, by itself, a qualifying exercise. A
closure record follows the merge; exercise status is determined under that rule when the time comes and
is not asserted here.

### On `authorizations.md`'s own stated scope

Recorded explicitly, as AUTH-003 and AUTH-006 recorded it:

1. `authorizations.md`'s introductory text (`authorizations.md:3-5`) describes the register as
   recording authorizations "to edit corpus text". Read strictly, that sentence does not mention
   source code or test files.
2. This entry does **not** determine that the register's subject matter generally encompasses source
   code or tests, and decides nothing about the register's jurisdiction over code.
3. This entry does **not** expand or amend the register's introductory definition, and does not
   depend on it being read broadly.
4. The §39 release, the implementation authorization and the new-file determination are independent
   operator acts; their authority comes from Kevin Brown's own determination, not from this register's
   jurisdiction.
5. Whether future code authorizations generally belong in this register, and under what definitional
   revision, is **not decided here** and remains open (`authorizations.md:837` records the same
   reservation).
6. AUTH-007's validity does not depend on resolving that question.

### Placement

This entry is appended after the final line of the register as it stood at `40247cd` (line 1234), so
that no existing line moves. Its position after AUTH-006 and its closure record carries no meaning, and
it amends neither.

### Review clarifications — 2026-10-25 (not part of the original AUTH-007 authorization)

This note is a record of two operator directions given during review of the implementation diff, after
the three acts above were issued. It is separate from the verbatim issuance, which is unchanged. It
adds no scope to the issuance, and it releases no further hold. The two directions below were given by
the operator in the review response of 2026-10-25, quoted verbatim:

1. Fetch failures — console log:

> Fetch failures: add a console log of the fetch error inside loadMatrix(). The missing-file message stays unchanged.

   Implemented in `loadMatrix()`'s fetch stage only: the fetch exception's message is logged with
   `console.error`. The missing-file message text is unchanged. A non-OK response throws nothing and so
   logs nothing.

2. Test assertion — no case-detail trigger on a null-modality card:

> Add a test assertion that a null-modality card carries no onclick and no case-detail trigger. This verifies Act 2's existing requirement.

   Implemented as one added test in the AUTH-007 test file. It asserts that the CAUTIONARY card carries
   neither `onclick` nor `openCase`, and that the normal card does carry `onclick`, so the check cannot
   pass vacuously.

Nothing in this note changes the issuance's scope, exclusions or verification requirements.

### AUTH-007 — Closure record

```
Exercise status:        EXERCISED AND SPENT
Landed as:              cedc43fe37cba7d6ee658f28270b17f6ab1ae823
Pull request:           #6
Exercise recorded at:   2026-10-25 23:16:46 -0400
```

The first qualifying exercise was the merge of PR #6 into `main`, a merge commit made
2026-10-25T23:15:35-04:00 (2026-10-26T03:15:35Z; GitHub reports `mergedAt` 2026-10-26T03:15:36Z). Under
"Authorization Exercise and Closure" §2, that is the first time any part of the authorized act landed on
the authoritative branch. This record was added later; per §4 it documents an exercise that had already
occurred and does not imply AUTH-007 remained operative between the merge and this recording.

Recorded because the merge SHA alone does not identify which reviewed commits were merged:

- First parent of the merge: `40247cda7c251b0fb330512affe115396974e080`, the prior `main`.
- Second parent of the merge: `7edd947896b4fc18167e41f566c022db76a4a19f`, the PR head the operator
  approved for merging, landed unchanged. The PR carried two commits, `eb96b70` and `7edd947`, and no
  others. The merge was made as a merge commit, not a squash or rebase, as the operator's merge approval
  directed.
- The merge changes exactly three files relative to the prior `main`: `dashboard.html` (modified),
  `docs/authorizations.md` (appended; no existing line changed) and `test_dashboard_null_modality.py`
  (added). On `main`, `dashboard.html` has SHA-256
  `93555a8f8c3577b8e088d256b953fae304a9abfce2a682b8201f7f3cf9dc6122` and `test_dashboard_null_modality.py`
  has SHA-256 `af938607571c4636f51618a99df77aab09d5fda862291d3f4f49672022b8bc49`.
- CI: PR run 40262915948 on the approved head, and push run 40263186470 on the merge commit; `test (3.10)`,
  `test (3.11)` and `test (3.12)` completed with conclusion `success` in both runs.
- Neither commit in the PR nor the merge commit carries a `Co-Authored-By` trailer or a "Generated with"
  line, and the PR body carried none, as the operator's attribution instruction directed.
- `containment_matrix.json` is not tracked by git; its SHA-256 on the working machine was
  `3FA4D990C7877B63A5796BF33C43C28A0DC0C66F7C1DF91D0279FFCB50FB86AC` before the implementation and after
  the merge. That is a local observation, not repository evidence.

Per §6, this closure does not amend, broaden, narrow, reinterpret, ratify, or supersede AUTH-007's scope.
AUTH-007's grant record, including its original `Status:` line and the "Review clarifications" note, is
unchanged, and the question of the register's jurisdiction over code remains as the grant record left it.
This record authorizes nothing further, including any AUTH-008 or any other work.

---

## AUTH-008

```
Authorizes:        one escaping helper and its use in both card branches of
                   dashboard.html's renderGrid(), so that matrix-derived text
                   renders as text rather than being interpreted as HTML, plus one
                   new top-level test file
Target scope:      dashboard.html::renderGrid() (both card-template branches: the
                   null-modality card and the normal card)
                   dashboard.html Helpers section (one new helper, esc(v), only)
                   one new top-level test file under test_*.py discovery
Route:             operator determination (independent act; FE Requirements
                   §39 release, recorded below) -> implement on a dedicated
                   branch -> verify against the checklist below -> this entry lands
                   in the same PR as the fix -> operator review of the diff and
                   test evidence -> PR merge on the operator's explicit approval ->
                   closure record
Granted by:        Kevin Brown, operator
Granted at:        2026-10-27, in session
Basis:             a read-only AUTH-008 candidate assessment run in session on
                   2026-10-27, which found every matrix-derived value in
                   renderGrid()'s card template (`dashboard.html:485-505` at
                   `a910ecb`) inserted into HTML without escaping, with a
                   CAUTIONARY stub's `fusion_name` the one field reachable with
                   typed text (`modality_classifier.py:63-69`, `mythos_sync.py:161-165`,
                   `server.py:48-50`); GitHub issue #7 item 4 ("HTML escaping"),
                   which records the finding as backlog and grants nothing; AUTH-007
                   (`authorizations.md:1295`, `:1316`), whose §39 release and
                   exclusions left `openCase()` and every other section of
                   `dashboard.html` held and which is exercised and spent; FE
                   Requirements §39 (`fusion_engine_requirements_v0.1.md:1397`,
                   `:1402`), whose hold is released ONLY for the surfaces named above
Status:            granted; NOT YET EXERCISED — no file within the scope of
                   this authorization has landed on main as of this recording
```

**What actually authorizes this, and what this entry is.** Three operator acts and one record, kept
separate on purpose:

- **Act 1 — the §39 release** is Kevin Brown's own act, stated in his own words below. It removes
  a prohibition and grants nothing.
- **Act 2 — the implementation authorization** is Kevin Brown's own act. It is what permits the
  `dashboard.html` edits.
- **Act 3 — the new-file determination** is Kevin Brown's own act. It is what permits the one new
  test file.
- **This AUTH-008 record** is the archive of those acts. It creates no authority. Per the operator's
  issuance, the acts take effect on issue and the operator stated that implementation may begin
  before this entry lands; this entry lands in the same PR as the fix.

**Issuance record.** The operator's issuance message is quoted below as received in session. It was
not separately preserved outside the repository before this entry was written, so byte-level identity
with the operator's original transmission is not independently verifiable from inside the session.
Act 3 is quoted in a code fence so that the markup-like test string in it renders as text; its words
are verbatim.

### Operator statement

> AUTH-008 — issued by the operator, 2026-10-27. Three separate acts.

### Act 1 — §39 release (operator, verbatim)

> I release the FE §39 UNMODIFIED hold on dashboard.html, limited to: (a) both branches of the renderGrid() card template (the null-modality card and the normal card), and (b) the Helpers section, solely to add one escaping helper. openCase() and every other function or section of dashboard.html, and all other §39-held code, remain held exactly as recorded. This release removes a prohibition and grants nothing.

### Act 2 — Implementation authorization (operator, verbatim)

> I authorize exactly:
>
> One helper esc(v) in the Helpers section that returns String(v) with &, <, >, " and ' replaced by their HTML entities.
> In both renderGrid() card branches, wrap every matrix-derived value inserted into HTML text or attributes in esc(). Comparisons and logic keep using raw values. No other change to card structure, classes, onclick behavior or visible text.

### Act 3 — New-file determination (operator, verbatim)

```text
I authorize one new top-level test file under test_*.py discovery. It may import helper functions from test_dashboard_null_modality.py but must not modify that file. It fails, and does not skip, if node is unavailable. It never calls save_to_matrix or export_for_web and never touches containment_matrix.json. Using the hostile string <img src=x onerror=alert(1)>&"', it asserts:

for a CAUTIONARY stub with a hostile fusion_name: no raw <img in the grid, the escaped form present, the unescaped card-name text equals the hostile string, two cards render, and the stub card has no onclick;
for a normal card, as a subtest per field (fusion_name, signature_ability, biome, id): no raw <img and the escaped form present;
a hostile modality or state cannot break out of a class attribute;
a benign fixture including “Rhetoric & Legacy” renders the same visible text as before.

It must fail against the current dashboard.html and pass after the fix. The existing AUTH-007 tests must still pass unchanged.
```

### Explicit exclusions (operator, verbatim)

> Exclusions: openCase() in full (Slice B); server.py, including CORS, Content-Type handling, binding and CSP; the fusion engine; loadMatrix(); the stat tiles and every other issue #7 item; all existing tests; CI config; AUTH-005 closure; resolver and governed-reason work.

### Verification (operator, verbatim)

> Verification: all CI suites pass; the new test fails before the fix and passes after; containment_matrix.json is byte-identical; the diff touches only dashboard.html, the new test file and docs/authorizations.md.

### Recording and attribution (operator, verbatim)

> Recording: this message is the authorization and takes effect on issue. The AUTH-008 entry in docs/authorizations.md records it and lands in the same PR as the fix. A closure record follows the merge. If you find any provision requiring the entry to land before implementation, stop and report it with the citation before writing code.
>
> Attribution: no Co-Authored-By trailer and no “Generated with Claude Code” line on AUTH-008 commits or PRs.

### Merge gate (operator instruction, same message)

> Before merging, stop and present the diff and test evidence (including the pre-fix failure) for operator review. Do not merge without my explicit approval.
>
> AUTH-008 is exercised and spent on merge to main. It authorizes nothing further.

### Provision check required by the recording instruction

The operator directed that any provision requiring this entry to land before implementation be
reported before code was written. A pattern search across all of `docs/authorizations.md`, together with
full reads of the `Authorization Exercise and Closure` rule and its Amendment 1, AUTH-005, AUTH-006 and
the AUTH-007 entry, found no such requirement; the only match was AUTH-007's own quoted recording
instruction. The "recorded, then implement" sequences in AUTH-005 and AUTH-006 are routes stated in those
entries and are not a general rule. AUTH-001 to AUTH-004 were searched by pattern but not read in full,
and the search covered `docs/authorizations.md` only; it was not an exhaustive sweep of the governance
corpus.

### Lifecycle

AUTH-008 is subject to the `Authorization Exercise and Closure` rule in this register
(`authorizations.md:833` onward). The operator's issuance states that AUTH-008 is exercised and spent on
merge to `main`, which is that rule's default exercise condition (§2). Appending this entry is not a
qualifying exercise. A commit on an implementation branch is not, by itself, a qualifying exercise. A
closure record follows the merge; exercise status is determined under that rule when the time comes and
is not asserted here.

### On `authorizations.md`'s own stated scope

Recorded explicitly, as AUTH-003, AUTH-006 and AUTH-007 recorded it:

1. `authorizations.md`'s introductory text (`authorizations.md:3-5`) describes the register as
   recording authorizations "to edit corpus text". Read strictly, that sentence does not mention
   source code or test files.
2. This entry does **not** determine that the register's subject matter generally encompasses source
   code or tests, and decides nothing about the register's jurisdiction over code.
3. This entry does **not** expand or amend the register's introductory definition, and does not
   depend on it being read broadly.
4. The §39 release, the implementation authorization and the new-file determination are independent
   operator acts; their authority comes from Kevin Brown's own determination, not from this register's
   jurisdiction.
5. Whether future code authorizations generally belong in this register, and under what definitional
   revision, is **not decided here** and remains open (`authorizations.md:837` records the same
   reservation).
6. AUTH-008's validity does not depend on resolving that question.

### Placement

This entry is appended after the final line of the register as it stood at `a910ecb` (line 1441),
so that no existing line moves. Its position after AUTH-007 and its closure record carries no meaning, and
it amends neither.

### AUTH-008 — Closure record

```
Exercise status:        EXERCISED AND SPENT
Landed as:              145993281b70499bd7da8b8d0885dfc15d914771
Pull request:           #9
Exercise recorded at:   2026-10-27 21:20:37 -0400
```

The first qualifying exercise was the merge of PR #9 into `main`, a merge commit made
2026-10-27T21:17:48-04:00 (2026-10-28T01:17:48Z; GitHub reports `mergedAt` 2026-10-28T01:17:48Z). Under
"Authorization Exercise and Closure" §2, that is the first time any part of the authorized act landed on
the authoritative branch. This record was added later; per §4 it documents an exercise that had already
occurred and does not imply AUTH-008 remained operative between the merge and this recording.

Recorded because the merge SHA alone does not identify which reviewed commit was merged:

- Parents of the merge, read from the merge commit object itself and not from GitHub's description:
  exactly two. First parent `a910ecb26fe129c48daa122c554e9a0b8449a4ad`, the prior `main`. Second parent
  `536297420d505a5db9c013dedfb9d41513c5d208`, the PR head the operator approved for merging, landed
  unchanged. The PR carried one commit and no others. The merge was made as a merge commit, not a squash or
  rebase, as the operator's merge approval directed.
- The merge changes exactly three files relative to the prior `main`: `dashboard.html` (modified),
  `docs/authorizations.md` (appended; no existing line changed) and `test_dashboard_escaping.py` (added).
  The merged tree is identical to the approved head's tree, so nothing was added by the merge itself. On
  `main`, `dashboard.html` has SHA-256
  `69087767d85c2858d8a8893d799923dc641f4a965fd7acd95dfd88aa57d403a1` and `test_dashboard_escaping.py` has
  SHA-256 `dfeecbae0ebd6ff0bff502a17e1bcb797fdb35e0799837082f8ae6cf08c455f9`.
- CI: PR run 40613611351 (`pull_request`, head `5362974…`) and push run 40614176428 (the merge commit);
  `test (3.10)`, `test (3.11)` and `test (3.12)` completed with conclusion `success` in both runs. In the
  raw logs of the "Run full suite including property tests" step of each of those six jobs, all five
  `test_dashboard_escaping` methods appear and each is reported `ok`: the CAUTIONARY-stub card, the
  per-field normal-card test, the `modality` and `state` class-attribute breakout tests, and the benign
  visible-text test. No log line in those steps reports a skip, an expected failure, an unexpected success,
  a failure or an error, and each summary is `Ran 133 tests` followed by a bare `OK`. Passing subtests
  print no line of their own, so the logs establish the five methods passed but not how many subtests each
  ran.
- Neither the PR commit nor the merge commit carries a `Co-Authored-By` trailer or a "Generated with" line,
  and the PR body carried none, as the operator's attribution instruction directed.

**Scope exercised.** Relative to the prior `main`, the change to `dashboard.html` is five hunks and
nothing else: ten lines of the `renderGrid()` card template, in both branches (the null-modality card and
the normal card), on which twelve matrix-derived insertions are now wrapped in `esc()`; and one new
function, `esc(v)`, added at the end of the Helpers section, returning `String(v)` with `&`, `<`, `>`,
`"` and `'` replaced by entities. No matrix-derived field is left unwrapped in either card branch. The
new test file asserts, with the hostile string `<img src=x onerror=alert(1)>&"'`, that a CAUTIONARY stub's
`fusion_name` renders as text, that each of `fusion_name`, `signature_ability`, `biome` and `id` does on
the normal card, that a hostile `modality` or `state` cannot leave its class attribute, and that a benign
fixture including "Rhetoric & Legacy" shows the same visible text as before. It imports helper functions
from `test_dashboard_null_modality.py` and does not modify it.

**Excluded surfaces, confirmed untouched by the merge.** In `dashboard.html`, `loadMatrix()`,
`openCase()`, the markup and styles above `loadMatrix()`, and everything from `overlayClick()` to the end of
the script are byte-identical to their text at `a910ecb`; the Helpers section differs only by the added
`esc` function. The merge changes no path among `server.py`, `mythos_sync.py`, `modality_classifier.py`,
`logic_auditor.py`, `console.py`, `fusion_engine/`, `.github/`, `test_engine.py`,
`test_hypothesis_properties.py`, `test_regression_case_001.py`, `test_dashboard_null_modality.py` and
`docs/evidence/`. `openCase()`, the case-file modal, therefore remains unescaped, and the `server.py`
findings recorded in issue #8 are not addressed. `containment_matrix.json` is not tracked by git; its
SHA-256 on the working machine was `3FA4D990C7877B63A5796BF33C43C28A0DC0C66F7C1DF91D0279FFCB50FB86AC`
before the implementation and after the merge. That is a local observation, not repository evidence.

Per §6, this closure does not amend, broaden, narrow, reinterpret, ratify, or supersede AUTH-008's scope.
AUTH-008's grant record, including its original `Status:` line, is unchanged, and the question of the
register's jurisdiction over code remains as the grant record left it. This record authorizes nothing
further, including any AUTH-009, the deferred `openCase()` escaping, or any `server.py` change.

---

## AUTH-009

```
Authorizes:        bounded hardening changes to server.py (sections A-H below) and
                   one new top-level test file, test_server_hardening.py
Target scope:      server.py: production binding; removal of the wildcard CORS
                   header; endpoint-aware Content-Type, Origin, Host and
                   Content-Length validation; a GET/HEAD allowlist; controlled
                   request-validation errors; and one named startup-function
                   extraction, make_server()
                   one new top-level test file under test_*.py discovery
Route:             operator determination (independent act; FE Requirements
                   §39 release, recorded below) -> implement on a dedicated
                   branch in two commits -> verify against the checklist below ->
                   this entry lands in the same PR as the fix -> operator-performed
                   real-browser smoke test from a disposable copy outside the
                   repository -> operator review of the diff and test evidence ->
                   PR merge on the operator's explicit approval -> closure record
Granted by:        Kevin Brown, operator
Granted at:        2026-10-28, in session
Basis:             read-only AUTH-009 pre-issuance assessments run in session on
                   2026-10-28 at `cb946702d3856742f359ffb07dd0d90946ac0d40`, which
                   found `server.py` binding all interfaces (`server.py:80`),
                   answering with a wildcard CORS header (`server.py:29`), accepting
                   POSTs to `/fuse` and `/clear` with no Origin, Host or Content-Type
                   check (`server.py:33-36`, `server.py:55-59`), parsing JSON and
                   integers outside any error handling (`server.py:34-36`), and
                   serving its whole working directory on GET and HEAD; GitHub
                   issue #8, which records the `server.py` findings as backlog and
                   grants nothing; AUTH-007 (`authorizations.md:1316`), whose
                   exclusion of CAUTIONARY persistence in `server.py` this grant
                   preserves; AUTH-008 (`authorizations.md:1530`), whose exclusions
                   left `server.py`, including CORS, Content-Type handling, binding
                   and CSP, held and which is exercised and spent; FE Requirements
                   §39 (`fusion_engine_requirements_v0.1.md:1397`, `:1402`), whose
                   hold is released ONLY for the surfaces named below
Status:            granted; NOT YET EXERCISED — no file within the scope of
                   this authorization has landed on main as of this recording
```

**What actually authorizes this, and what this entry is.** Three operator acts and one record, kept
separate on purpose:

- **Act 1 — the §39 release** is Kevin Brown's own act, stated in his own words below. It removes
  a prohibition and grants nothing.
- **Act 2 — the implementation authorization** is Kevin Brown's own act. It is what permits the
  `server.py` changes.
- **Act 3 — the new-file determination** is Kevin Brown's own act. It is what permits the one new
  test file.
- **This AUTH-009 record** is the archive of those acts. It creates no authority. Per the operator's
  issuance, the acts take effect on issue and implementation may begin before this entry lands; this
  entry lands in the same PR as the fix.

**Issuance record.** The operator's issuance text is quoted below as it stood in session on 2026-10-28,
when the operator adopted it "exactly as presented, subject only to" two additions that are shown in
place. The text was drafted in session and then adopted by the operator, and the operator's issuance
message was not separately preserved outside the repository before this entry was written, so byte-level
identity with the operator's transmission is not independently verifiable from inside the session.
Every `server.py:NNN` citation in this entry is to `server.py` at the baseline `cb94670`, because the
file changes in the same PR and its line numbers move.

### Operator statement

> AUTH-009 — issued by the operator, 2026-10-28. Three separate acts.
>
> Baseline: `main` at `cb946702d3856742f359ffb07dd0d90946ac0d40`. An implementation branch must start from that SHA, or from a later `main` whose `server.py` is identical to it at the git blob level.

### Act 1 — §39 release (operator, verbatim)

> I release the FE §39 "Existing WorldCraft-Visuals code — UNMODIFIED" hold on `server.py`, limited to the changes enumerated in Act 2 and no others. Every other function or section of `server.py`, and all other §39-held code, remain held exactly as recorded. This release removes a prohibition and grants nothing.

### Act 2 — Implementation authorization (operator, verbatim)

> I authorize exactly the following changes to `server.py`.
>
> **A. Binding.** The production server binds to `127.0.0.1:8000`, not all interfaces.
>
> **B. CORS.** Remove `Access-Control-Allow-Origin: *` (`server.py:29`). No other CORS header is introduced. `OPTIONS` behavior is unchanged.
>
> **C. Content-Type.** `POST /fuse` requires media type `application/json` (case-insensitive; parameters such as `charset=utf-8` allowed), else HTTP 415. `POST /clear` requires no Content-Type and must keep accepting the dashboard's bodyless POST.
>
> **D. Origin.** On POST, a present `Origin` must equal exactly `http://localhost:8000` or `http://127.0.0.1:8000`, else HTTP 403. The literal `null` is a foreign Origin. A genuinely absent `Origin` is permitted and is a documented residual risk (local non-browser clients).
>
> **E. Host.** On GET, HEAD and POST, `Host` must equal exactly `localhost:8000` or `127.0.0.1:8000` (case-sensitive). Any other or missing Host gets HTTP 403. This check runs before path, Origin, Content-Type, Content-Length or body handling. The allowlist is a fixed production constant and is not derived from any bound port.
>
> **F. GET/HEAD allowlist.** Only `/dashboard.html` and `/containment_matrix.json` are served, matched on the parsed URL path with the query string removed, so `containment_matrix.json?t=123` keeps working. Everything else returns HTTP 404, including `/`, directory paths, dotfiles, `.git`, source files and docs. No redirect from `/` is introduced. Allowed paths are served by the existing handler behavior.
>
> **G. Request validation** (existing `{"error": …}` body form; existing successful response formats and the existing "Alpha and Beta are required." 400 are preserved). Order of checks: Host → path → Origin → Content-Type → Content-Length → body parsing → field validation.
> - Invalid, non-numeric or negative `Content-Length`: HTTP 400.
> - `Content-Length` above **65,536 bytes**: HTTP 413, decided before the body is read.
> - Absent `Content-Length`: permitted on `/clear` (no body is read); on `/fuse`, treated as an empty body, which fails JSON parsing with HTTP 400.
> - `Content-Length` validation applies to both `/fuse` and `/clear`.
> - Malformed JSON, or a body that is not a JSON object: HTTP 400.
> - `alpha` or `beta` not a string: HTTP 400.
> - `dominance` not convertible by the existing `int()` conversion: HTTP 400. No new range check is added.
>
> **H. Startup-function extraction (named exception, required by the Act 3 test design).** I permit extraction of server startup into one function, `make_server(host='127.0.0.1', port=8000)`, that constructs and returns the bound `HTTPServer` without serving. This extraction is required solely to support process-isolated startup and binding verification. The production `__main__` path calls it without host or port overrides. Conditions:
> 1. The production `__main__` path retains its existing startup behavior, `use_utf8_output()`, and `serve_forever()`, except for the authorized change from all-interface to `127.0.0.1` binding.
> 2. The production default port remains 8000.
> 3. The startup banner and dashboard URL are unchanged.
> 4. No lifecycle, routing, threading, persistence or architecture change is permitted.
> 5. The test confirms production defaults select `127.0.0.1:8000` and the isolated instance uses `127.0.0.1` with an ephemeral port.
> 6. Production Host validation is not weakened for testing. The test client sends the literal `Host: localhost:8000` to the ephemeral-port server and asserts that a Host carrying the ephemeral port is rejected.
>
> This is a specifically named exception, not general refactoring authority. I acknowledge that H's loopback default and the `__main__` call also implement A.
>
> **Exclusions.**
> - CSP, including the existing header, which stays byte-identical.
> - `dashboard.html`.
> - `openCase()` and all AUTH-010 work.
> - `mythos_sync.py`.
> - The resolver, classifier and fusion-engine modules.
> - CAUTIONARY-stub persistence. `server.py:46-53` (fusion generation, `save_to_matrix`, `export_for_web`, the 200 and 500 responses) keeps its behavior, per AUTH-007's exclusion (`authorizations.md:1316`).
> - Matrix format or storage behavior.
> - Existing test files and CI configuration.
> - Threading or server architecture.
> - Unrelated startup or lifecycle behavior.
> - Every other §39 hold.
>
> **Residual risks, accepted and not objectives.** Absent-Origin POSTs from local non-browser clients. Any local process can call the endpoints. A slow client can still block the single-threaded server. `server.py:47` prints raw input to the console.

### Act 3 — New-file determination (operator, verbatim)

> I authorize one new top-level file, `test_server_hardening.py`, under `test_*.py` discovery, using `unittest` and the standard library only. I do not authorize changes to any existing test file, CI configuration or unrelated module. It must fail, and not skip, if its subprocess cannot start.
>
> **Isolation.**
> - Each test server runs in a separate subprocess (`sys.executable`, `PYTHONDONTWRITEBYTECODE=1`) whose working directory is a fresh temporary directory.
> - The repository is made importable through an absolute path without changing the child's isolated working directory.
> - The test verifies that imports and module initialization do not read, write or create production data.
> - The child builds the server with `make_server('127.0.0.1', 0)`, prints its own `socket.getsockname()` as its first line, and then serves. The parent drains the child's remaining output.
> - The test asserts that the working directory is not the repository, both before launch and in the child.
> - The real matrix is never used as a fixture.
> - Every test that exercises `/clear` establishes its own temporary matrix fixture.
> - No test depends on another test having run first.
> - The real matrix's SHA-256, or its absence, is recorded before and after as an additional safeguard, not as a substitute for isolation.
> - Cleanup removes only the temporary directory, and the child is terminated in `tearDown`.
> - Each rejection test seeds its own temporary matrix fixture, sends the rejected request, and asserts that the fixture is byte-identical afterward. No rejection test may rely on execution order or state left by another test.
>
> **Binding.** The test asserts the bound address reported by the child's own socket is `127.0.0.1` with an ephemeral, non-8000 port. It does not bind port 8000. It checks production defaults through the `make_server` signature (`127.0.0.1`, `8000`) and an AST check that `__main__` calls `make_server` without host or port overrides. The AST check fails with a clear message if the expected startup structure changes.
>
> **Required cases.**
> - **Dashboard shapes:** the dashboard's exact `/fuse` and `/clear` requests succeed. Registered names persist to the temporary matrix, and unknown names persist a CAUTIONARY stub.
> - **GET/HEAD:**
>   - `dashboard.html` and `containment_matrix.json?t=123` return 200.
>   - `/`, `/server.py`, `/.hidden`, `/.git/config`, `/secret.txt`, `/docs/…` and `//dashboard.html` return 404.
>   - The `//dashboard.html` case asserts the HTTP 404 outcome only. It does not assert how the path is parsed.
> - **Host:** bad, missing and ephemeral-port Hosts return 403 on GET, HEAD and POST.
> - **Origin:** a foreign Origin and `Origin: null` return 403. An absent Origin is allowed, with the residual risk documented in the test.
> - **Allowlist acceptance:** POST `/fuse` and POST `/clear` succeed with `Origin: http://localhost:8000` and with `Origin: http://127.0.0.1:8000`. GET `/dashboard.html` succeeds with `Host: localhost:8000` and with `Host: 127.0.0.1:8000`. (Amendment 1 — mandatory positive regression tests, using the existing process-isolated harness, disposable matrix fixtures and the production Host/Origin allowlist values; production validation is not weakened to satisfy them.)
> - **Content-Type:** none, `text/plain` and `application/x-www-form-urlencoded` on `/fuse` return 415. `application/json; charset=utf-8` is accepted.
> - **Content-Length:**
>   - `/clear` with no Content-Length succeeds.
>   - `/fuse` with no Content-Length returns 400.
>   - A malformed value returns 400.
>   - A negative value returns 400.
>   - A value above 65,536 returns 413, with the body never read.
> - **JSON and fields:** malformed JSON, a list body, a non-string `alpha` and a non-numeric `dominance` return 400. An empty Alpha or Beta keeps its existing 400.
> - **Headers:** no response carries `Access-Control-Allow-Origin`, the CSP header is still present, and `OPTIONS` returns 501 with no CORS headers.

### Lifecycle, verification and recording (operator, verbatim)

> **Two commits on one dedicated branch and PR.**
>
> **Commit 1 — startup extraction and regression harness.**
> - Implement section H's `make_server()` extraction and create `test_server_hardening.py`.
> - I acknowledge that H's loopback default and the production `__main__` call also implement requirement A at this stage. Do not implement B–G.
> - Run the new regression tests and record the actual results.
> - Binding assertions may already pass at Commit 1. That is expected and must be reported accurately.
> - Demonstrate pre-hardening failures through the remaining security-behavior tests, not through artificial binding failures.
> - Do not alter the tests merely to force a particular failure result.
> - Commit 1 is expected to fail those tests. CI must be green at the PR head (Commit 2), not at Commit 1.
>
> **Commit 2 — remaining hardening.**
> - Implement B–G.
> - Complete any remaining verification of A without unnecessarily modifying already-correct binding behavior.
> - Run the new tests and the existing suite, and show the security-behavior tests that failed at Commit 1 now pass.
> - Confirm CI passes on Python 3.10, 3.11 and 3.12.
>
> The AUTH-009 register entry lands in the same PR.
>
> **Evidence exception for A.** I accept that A has no failing test before its implementation, because section H's extraction introduces loopback binding in Commit 1. This is an acknowledged exception to the pre-fix failure expectation, not a missing test. Evidence for A is:
> 1. The `make_server()` signature defaults to `127.0.0.1` and `8000`.
> 2. The AST check that `__main__` calls the function without host or port overrides.
> 3. The bound-socket assertion from the isolated subprocess, showing `127.0.0.1` and an ephemeral port.
> 4. Diff review confirming production binding changed from all interfaces to loopback only.
>
> Record these results accurately. Do not manufacture a failing binding test.
>
> **Pre-merge real-browser gate (operator-performed).**
> - Run against the PR branch head after Commit 2, from a **disposable copy outside the repository** with a disposable matrix, as in the 10/27 AUTH-007 observation.
> - Never launch it from the repository working tree or against the real matrix.
> - Because the Host allowlist is fixed to port 8000, the disposable server must listen on 8000, so stop any real instance first.
> - Exercise (1) Generate a fusion, (2) Clear Matrix, (3) reload and observe the resulting state, including whether the same-origin POSTs succeed under the new Origin and Host checks.
> - Record the observation in the AUTH-007 browser-verification format, claiming only what was directly observed. The record is an evidence-directory note written on my instruction after the observation. It is not a separate source-code authorization.
>
> **Verification.**
> - All CI suites pass at the PR head.
> - The new tests show the Commit 1 pre-hardening failures and the Commit 2 passes.
> - The real matrix hash is unchanged.
> - The diff touches only `server.py`, `test_server_hardening.py` and `docs/authorizations.md`.
> - `dashboard.html` is unchanged at the git blob level (identical blob hash at baseline and PR head). Committed blob identity is the authoritative comparison, not raw working-tree bytes.
>
> **Recording.**
> - This message is the authorization and takes effect on issue.
> - Before merging, stop and present the diff, the test evidence and the browser observation. Do not merge without my explicit approval.
> - AUTH-009 is exercised and spent on merge to `main`, and a closure record follows.
> - No `Co-Authored-By` trailer and no "Generated with Claude Code" line on AUTH-009 commits or PRs.
> - This issuance does not decide the register's jurisdiction over code authorizations, which remains open as AUTH-007 and AUTH-008 recorded.
> - AUTH-010 remains separate and unauthorized.

### Amendments and issuance (operator, verbatim)

> I adopt the complete text exactly as presented, subject only to the two additions below, which are incorporated into the issued authorization.
>
> Amendment 1 — Positive Allowlist Acceptance Tests. Under Act 3, Required cases, immediately after the existing Origin test requirement, add: "Allowlist acceptance: POST `/fuse` and POST `/clear` succeed with `Origin: http://localhost:8000` and with `Origin: http://127.0.0.1:8000`. GET `/dashboard.html` succeeds with `Host: localhost:8000` and with `Host: 127.0.0.1:8000`." These are mandatory positive regression tests. They must use the existing process-isolated test harness, disposable matrix fixtures, and production Host/Origin allowlist values. Do not weaken production validation to satisfy these tests.
>
> Amendment 2 — CSP Preservation. Under Act 2, Exclusions, restore the explicit wording: "CSP, including the existing header, which stays byte-identical." No CSP changes are authorized.
>
> I APPROVE, ADOPT, AND ISSUE AUTH-009 IN FULL, incorporating the two amendments above. [...] AUTH-009 takes effect upon this issuance. Proceed with the authorized implementation on a dedicated branch, following the required two-commit sequence. Create the AUTH-009 register entry within the authorized pull request. Do not expand scope, alter unrelated files, or modify the real matrix. After Commit 2, complete the authorized automated verification and prepare the pull request. Present the diff, Commit 1 failure evidence, Commit 2 passing results, CI status, and matrix-integrity evidence. STOP before merging. The browser smoke test is an operator-performed pre-merge gate. Do not claim it has been completed or independently approved. Await my browser observation and explicit merge approval.
>
> AUTH-009 IS ISSUED. AUTH-010 REMAINS UNAUTHORIZED.

### Supplemental authorization — `finish()` (operator, verbatim)

Issued by the operator in session on 2026-10-28, after review of the `finish()` override introduced in
the PR's second commit. It was issued as a separate act, after AUTH-009's original issuance.

> I accept the `finish()` review findings. I adopt the total-deadline correction and decline the removal alternative.
>
> **Supplemental authorization — `finish()` (operator).** I authorize, as a named lifecycle exception to the "Unrelated startup or lifecycle behavior" exclusion in AUTH-009 Act 2, exactly one `finish()` override in `MythosHandler` in `server.py`, and no other change. For POST requests only, it does the following, in order:
>
> 1. Half-closes the connection with `shutdown(SHUT_WR)`.
> 2. Discards at most 65,536 bytes received, under a total elapsed-time bound of 0.5 seconds measured with a monotonic deadline.
> 3. Ignores `OSError`.
> 4. Calls `super().finish()`.
>
> It parses nothing from the discarded bytes and changes no check order. It adds no threading, keep-alive, timeout or connection handling elsewhere. No test change is authorized or required by this supplement.
>
> **Corrective commit.** I authorize one additional commit on `fix/auth-009-server-hardening`, containing only:
>
> - The total-deadline diff to `finish()`, exactly as presented in the review.
> - The replacement of Implementation note 3, using the wording presented in the review.
> - This supplemental authorization block, added after the "Amendments and issuance" section of the AUTH-009 register entry.
>
> Do not change any other file or any other part of the register.
>
> **Verification.**
>
> - Run `test_server_hardening.py` three times and the full suite once.
> - Confirm the real matrix hash is unchanged.
> - Confirm `dashboard.html`'s blob hash matches the baseline.
> - Push, and report CI on Python 3.10, 3.11 and 3.12.
>
> Make the commit without attribution trailers.
>
> The idle-client wait of up to 0.5 seconds and the absence of a test that catches the TCP-reset defect are recorded residuals. They are not objectives.
>
> **Stop.** Do not merge. Merge approval follows my browser-gate observations. AUTH-010 remains unauthorized.

This supplement is archived as received in session; as with the original issuance, byte-level identity
with the operator's transmission is not independently verifiable from inside the session.

### Implementation notes (recorded at landing; not part of the operator's issuance)

These notes record how the authorized text was implemented where the issuance left a mechanism open, and
one defect found during verification. They add no scope. The operator reviews them with the diff.

1. **F matches the raw request-line target.** `_path_allowed()` reads the target from `self.requestline`
   and applies `urlsplit()` to it, then compares the parsed path, which excludes the query string, to the
   allowlist. It does not use `self.path` because `BaseHTTPRequestHandler.parse_request` rewrites a
   leading `//` to `/` in `self.path` before the handler runs (CPython gh-87389); that rewrite is present
   in the standard library source of the Python 3.12.10 used for development, and whether the other
   supported versions carry it was not checked. Matching `self.path` would therefore let
   `//dashboard.html` be served as `/dashboard.html` on some versions and return 404 on others.
   `urlsplit('//dashboard.html')` reads the leading `//` as a network location, so its path is empty and
   is not on the allowlist, which gives the required 404 whichever way the interpreter treats the prefix.
   `containment_matrix.json?t=123` still parses to `/containment_matrix.json`. The test asserts the 404
   outcome only, as the issuance directs.
2. **`_respond()` suppresses the body on HEAD.** With E and F, HEAD requests can reach `_respond()` (a
   403 for a bad Host, a 404 for an unapproved path). A HEAD response must not carry a body, and
   `_respond()` previously always wrote one. The change is one condition, `if self.command != 'HEAD'`,
   around the existing write; `Content-Length` and every header are unchanged. GET and POST bodies are
   untouched. Allowed files are served by the inherited `do_HEAD`, which already sends no body.
3. **A defect found in verification, repaired by a named lifecycle exception.** With B-G in place,
   `POST /fuse` rejected before its body was read failed intermittently on the development machine
   (Windows) with `ConnectionAbortedError` (10053): closing a socket that holds unread request bytes sends
   a TCP reset that can destroy the response. Measured outside the repository, without the repair 7 to 35%
   of such requests failed and with it 0 of 450 did. The repair is the `finish()` override authorized by
   the supplemental authorization above. It is not covered by Act 2, and the committed tests do not
   reliably detect its absence.
4. **Smaller choices.** The `else` branch of `do_POST` that returned 404 became unreachable once the path
   check moved ahead of Origin validation, so it was removed. The new error bodies use the existing
   `{"error": …}` form with messages the issuance did not specify. `Content-Length` is stripped of
   surrounding whitespace, then must be ASCII digits; a value of more than 18 significant digits is
   treated as oversize (413) without being converted to an integer.

### Lifecycle

AUTH-009 is subject to the `Authorization Exercise and Closure` rule in this register
(`authorizations.md:833` onward). The operator's issuance states that AUTH-009 is exercised and spent on
merge to `main`, which is that rule's default exercise condition (§2). Appending this entry is not a
qualifying exercise. A commit on an implementation branch is not, by itself, a qualifying exercise. A
closure record follows the merge; exercise status is determined under that rule when the time comes and
is not asserted here.

### On `authorizations.md`'s own stated scope

Recorded explicitly, as AUTH-003, AUTH-006, AUTH-007 and AUTH-008 recorded it:

1. `authorizations.md`'s introductory text (`authorizations.md:3-5`) describes the register as
   recording authorizations "to edit corpus text". Read strictly, that sentence does not mention
   source code or test files.
2. This entry does **not** determine that the register's subject matter generally encompasses source
   code or tests, and decides nothing about the register's jurisdiction over code.
3. This entry does **not** expand or amend the register's introductory definition, and does not
   depend on it being read broadly.
4. The §39 release, the implementation authorization and the new-file determination are independent
   operator acts; their authority comes from Kevin Brown's own determination, not from this register's
   jurisdiction.
5. Whether future code authorizations generally belong in this register, and under what definitional
   revision, is **not decided here** and remains open (`authorizations.md:837` records the same
   reservation).
6. AUTH-009's validity does not depend on resolving that question.

### Placement

This entry is appended after the final line of the register as it stood at `cb94670` (line 1658),
so that no existing line moves. Its position after AUTH-008 and its closure record carries no meaning, and
it amends neither.

### AUTH-009 — Closure record

```
Exercise status:        EXERCISED AND SPENT
Landed as:              ca5c6cb1fcef09051c394f4bf2ec690954643c18
Pull request:           #10
Exercise recorded at:   2026-10-28 16:45:03 -0400
```

The first qualifying exercise was the merge of PR #10 into `main`, a merge commit made
2026-10-28T16:42:06-04:00 (2026-10-28T20:42:06Z; GitHub reports `mergedAt` 2026-10-28T20:42:07Z). Under
"Authorization Exercise and Closure" §2, that is the first time any part of the authorized act landed on
the authoritative branch. This record was added later; per §4 it documents an exercise that had already
occurred and does not imply AUTH-009 remained operative between the merge and this recording.

Recorded because the merge SHA alone does not identify which reviewed commits were merged:

- Parents of the merge, read from the merge commit object itself and not from GitHub's description:
  exactly two. First parent `cb946702d3856742f359ffb07dd0d90946ac0d40`, the prior `main`. Second parent
  `b68363d5c55f96c5bdfead3510a641fed2c2e5c8`, the PR head the operator approved for merging, landed
  unchanged. The merged tree (`bb8fbb50769e247258cbe737c21e812bd434fc19`) is identical to the approved
  head's tree, so nothing was added by the merge itself. The PR carried three commits and no others:
  `1973f57` (commit 1, the `make_server()` extraction and the regression harness), `daa39c2` (commit 2,
  changes B-G and the register entry) and `b68363d` (the corrective commit under the operator's
  supplemental authorization for `finish()`). The merge was made as a merge commit, not a squash or
  rebase, as AUTH-007 and AUTH-008 were.
- The merge changes exactly three files relative to the prior `main`: `server.py` (modified),
  `docs/authorizations.md` (appended; no existing line changed, and the register's first 1658 lines are
  byte-identical to the prior `main`) and `test_server_hardening.py` (added). On `main`, `server.py` has
  SHA-256 `a34f8c7c061a11125be62e29a105015d83f93c805b018258dc6223009e630bf5` and
  `test_server_hardening.py` has SHA-256 `e3903268ae9dec00bfc3cc6d3ce227c52fbcc828d28e2944df9c8deff12a0e15`.
- CI: PR run 40755704170 (`pull_request`, head `daa39c2`), PR run 40758343352 (`pull_request`, head
  `b68363d`, the approved head) and push run 40765618161 (the merge commit); `test (3.10)`, `test (3.11)`
  and `test (3.12)` completed with conclusion `success` in the approved-head and merge-commit runs. In the
  raw logs of the full-suite step of each of those six jobs, all 43 `test_server_hardening` methods are
  reported `ok`, no log line reports a failure or an error, and each summary is `Ran 176 tests`. Passing
  subtests print no line of their own, so the logs establish that the 43 methods passed but not how many
  subtests each ran.
- None of the three PR commits, and not the merge commit, carries a `Co-Authored-By` trailer or a
  "Generated with" line, and the PR body carried none, as the operator's attribution instruction directed.

**Scope exercised.** Relative to the prior `main`, `server.py` now binds `127.0.0.1` by default through
the new `make_server(host='127.0.0.1', port=8000)` (section H, with A), which the production `__main__`
calls without overrides; no longer sends `Access-Control-Allow-Origin` (B); requires `application/json`
on `POST /fuse` (C); checks a present `Origin` against two exact values on POST (D); checks `Host`
against two exact values on GET, HEAD and POST (E); serves only `/dashboard.html` and
`/containment_matrix.json` on GET and HEAD, matched on the raw request-line target with the query string
removed (F); and returns controlled 400 and 413 errors for bad `Content-Length`, JSON and fields, with a
65,536-byte cap (G). It also carries the `finish()` override, authorized by the supplemental authorization
recorded in the AUTH-009 grant entry, which half-closes a POST connection and drains at most 65,536 bytes
under a total 0.5-second monotonic deadline. The new test file runs the server in a separate subprocess with
an isolated temporary working directory on an ephemeral port and asserts the behaviors above, including
the positive Origin and Host allowlist cases of Amendment 1.

**Excluded surfaces, confirmed untouched by the merge.** The merge changes no path other than the three
above. `dashboard.html` has the same git blob (`b1e8202bae330f9f9e76b0e988383598b4f40f3a`) on `main` as at
`cb94670`. The Content-Security-Policy header lines of `server.py` and the fusion-generation and
persistence block (from the `try:` through the 500 response) are identical to their text at `cb94670`,
compared programmatically. No path among `mythos_sync.py`, `modality_classifier.py`, `logic_auditor.py`,
`console.py`, `fusion_engine/`, `.github/`, `test_engine.py`, `test_hypothesis_properties.py`,
`test_regression_case_001.py`, `test_dashboard_null_modality.py`, `test_dashboard_escaping.py` or
`docs/evidence/` changed. `openCase()` therefore remains unescaped (AUTH-010 is not authorized), and
CAUTIONARY persistence in `server.py` is unchanged. `containment_matrix.json` is not tracked by git; its
SHA-256 on the working machine was `3FA4D990C7877B63A5796BF33C43C28A0DC0C66F7C1DF91D0279FFCB50FB86AC`
before the implementation, at each check made during verification and the browser gate, and after the merge. That is a
local observation, not repository evidence.

**Operator-performed browser gate.** The operator performed the real-browser gate on 2026-10-28 in
Chrome 156 on Windows against the approved head `b68363d`, served from a disposable copy outside the
repository with a disposable matrix. The operator reported what is listed in the evidence-directory note
`BROWSER_VERIFICATION_AUTH_009_20261028T164308-0400\BROWSER_VERIFICATION_OBSERVATION_NOTE_AUTH_009_20261028T164308-0400.txt`
(6946 bytes, SHA-256 `FBDEE823DE02B45E3A0F8BFF5BA45AC87D6D6356FB6CF6203F87FBCC391E4C0D`), which claims only those reports: CAUTIONARY cards for misspelled names that open nothing; `POST /fuse` returning
200 with `Origin: http://localhost:8000`, `Host: localhost:8000` and `Sec-Fetch-Site: same-origin` and the
Content-Security-Policy header; the case-file modal opening for a HIGH CONCEPT card; the matrix fetch
returning 200; Clear Matrix removing all cards, with the following matrix fetch erroring and new cards
numbered from `MSF-001`; and a successful generate after Clear. The operator did not perform the
`127.0.0.1:8000` generation or the browser check that `/` returns 404; those behaviors are covered by the
automated tests only and are not claimed as browser-verified.
**Recorded residuals.** Per the operator's issuance and supplemental authorization, these are accepted
and are not objectives: POSTs with no `Origin` header from local non-browser clients are allowed; any
local process can call the endpoints; a slow client can still block the single-threaded server; the
server prints raw request text to the console; a client that holds its connection open after a POST
response can delay the next request by up to 0.5 seconds; and no committed test reliably detects the
absence of the `finish()` repair (in a scratch copy with the drain disabled, the committed tests passed in
five of five runs).

Per §6, this closure does not amend, broaden, narrow, reinterpret, ratify, or supersede AUTH-009's scope.
AUTH-009's grant record, including its original `Status:` line, the supplemental authorization and the
Implementation notes, is unchanged, and the question of the register's jurisdiction over code remains as
the grant record left it. This record authorizes nothing further, including AUTH-010, the deferred
`openCase()` escaping, or any other `server.py` change.
