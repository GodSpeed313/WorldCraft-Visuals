# WorldCraft Contract 003 — Surfaced Payload Preservation

**DRAFT.** Title and filename finalized by operator determination, 2026-09-20. This
determination resolves the document's identity (title, number, filename) only; it does not
approve or adopt this document's substantive text, does not attest any §7 row, and does not
mark this document SIGNED or LOCKED.

**Type:** Resolution contract. Successor to Contract 002, superseding one division of it.
**Supersedes:** Contract 002 (`contract_002_domain_resolution_invariants.md`) §§3–4,
"Invariants carried forward from Contract 001 §6" and "New invariant — the GAP-4 obligation,"
lines 139–230, in full. No other division of Contract 002 is superseded by this document.

**Status:** **LOCKED (2026-09-20).** Binding. Supersession of Contract 002 §§3–4 is now
operative: this document is the operative source for the invariants Contract 002 §§3–4
previously carried. Contract 002 §§3–4's own text remains historically intact and unedited;
it no longer governs.

```
DRAFT
  →  every row of §7 attested and dated              (attestation completed)
  →  a separate operator act marking this document's Status line SIGNED
  →  SIGNED               (attested in full; not locked; not yet superseding anything)
  →  a separate, subsequent operator act marking this document's Status line LOCKED
  →  LOCKED                        (supersession of Contract 002 §§3–4 becomes operative)
```

**Each arrow above is a distinct act, on the same terms Contract 002's own status block
states for itself. No earlier stage substitutes for a later one, and none is automatic from
the one before it:**

- Attesting fewer than all seven rows of §7 activates nothing. This document remains DRAFT,
  with zero effect on Contract 002 §§3–4, for however long it persists in that state.
- Completing every row of §7 makes this document **eligible** to be marked SIGNED. Completing
  the final row does not, by itself, mark the document SIGNED.
- Marking this document SIGNED does not, by itself, mark it LOCKED, and does not supersede
  Contract 002 §§3–4. Contract 002 §§3–4 continue to govern in full until LOCK.
- LOCKED is reached only by a further, separate, subsequent operator act.
- Supersession of Contract 002 §§3–4 becomes operative only once this document reaches
  LOCKED.
- **Reaching LOCKED does not, by itself, close GAP-5 or authorize any implementation.**
  Recording GAP-5's closure in `open_contract_gaps.md` is a separate, later act under that
  register's own rules — the same separation Contract 002's own text observes for GAP-4
  (`contract_002_domain_resolution_invariants.md:63-65`) and the same separation actually
  exercised there: Contract 002's LOCK commit (`42427a6`) and GAP-4's closure-recording
  commit (`5a3ba9f`) are two distinct commits, both dated 2026-09-15. Implementation
  authorization is a further, independent operator act on top of that, following the AUTH-005
  pattern.

---

**Why this document exists.** GAP-5's closure condition, as restated operative on
2026-09-17, requires *"a contract division that supersedes the division currently carrying
the enforcement invariants for domain/family/grounding resolution"* to *"carr[y] an invariant
requiring every `SURFACED` result to preserve and report"* three named elements, *"without
permitting the accepted portion of a fusion to be discarded merely because another component
terminates unsuccessfully"* (`open_contract_gaps.md:882-891`). That same restatement
identifies the currently governing division by name: *"the currently governing enforcement
division is Contract 002 §§3–4, carrying I1–I8"* (`open_contract_gaps.md:893-894`). Contract
002 is LOCKED; `amendment_policy.md` §1 forecloses any amendment of locked text, without
exception. A locked Contract 002 cannot gain a ninth invariant directly; per
`amendment_policy.md` §3, supersession — naming the superseded division precisely, at the
granularity of an addressable division — is the only remaining route. This document is that
successor.

Its substantive content for the new invariant is Disposition 003
(`disposition_003_gap5_surfaced_payload_policy.md`), which records the operator's
determination of what GAP-5's eventual invariant must require. Disposition 003 is
authoritative operator input for this drafting; it is not itself the invariant, and this
document is what supplies the invariant Disposition 003 anticipated.

Preparation and review of this draft is permitted by the operator's 2026-09-20 determination,
archived in `ratification_002_gap5_successor_contract_process_opening_act.md`, narrowing FE
Requirements v0.1 §39's `Successor contract — ON HOLD` item solely for that purpose. That
determination does not itself approve this text, authorize signing or LOCK, or authorize
anything beyond preparation and review.

**What this document does not do.**

- It does not sign, attest, or lock itself. Every row in §7 is blank.
- It does not close GAP-5 in `open_contract_gaps.md`. Recording that closure — if and when
  this document locks — is a separate act under that register's own rules.
- It does not edit Contract 001 or Contract 002. Neither receives any edit, annotation, or
  mark of any kind as a result of this document's drafting, signing, or eventual lock.
  Contract 002 §§1, 2, 5, 6, 7 and their existing sign-off rows remain on the page exactly as
  attested, for as long as Contract 002 exists. Contract 001's surviving provisions (§§1–5,
  7, 8) are unaffected and continue to govern exactly as Contract 002 §1 already established.
- It does not amend, reopen, correct, or supersede Disposition 003. Disposition 003 remains
  the substantive policy source for the GAP-5 obligation below, unedited, exactly as
  acknowledged.
- It does not release, modify, or rely on any FE Requirements §39 hold other than the one
  Ratification 002 already narrows for this preparation-and-review purpose.
- It does not authorize any edit to `logic_auditor.py`, any other existing code file, or any
  registry. It does not authorize implementation of any kind.
- It does not decide Ruling 002 §10.3 / Seam 3, or §10.5 / §10.7's family/domain
  reclassification.
- It does not adopt any domain taxonomy, domain list, or domain count.
- It does not choose an implementation mechanism, schema, enum, field, or storage format for
  anything it requires.

---

## 1. Relationship to Contract 002 and Contract 001

Contract 002 §§1, 2, 5, 6, and 7 **remain governing and unchanged.** This document supersedes
§§3–4 only. Nothing in this document should be read as reopening, qualifying, or casting
doubt on any other division of Contract 002, including its own validity constraints (§2), its
exclusions (§5), its future-governance clause (§6), or its sign-off record (§7) — all of
which continue to bind exactly as signed.

Contract 001 §§1–5, 7, and 8 remain governing and unchanged, exactly as Contract 002 §1
already established (`contract_002_domain_resolution_invariants.md:85`); this document does
not restate, qualify, or reopen that relationship, and relies on it unaltered. Contract 001
§6 remains superseded by Contract 002, historically intact and unedited, exactly as before;
this document does not touch it.

Where this document references a state, transition, or terminal condition not redefined here
— `UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`, `RESOLVED_DOMAIN`, `UNRESOLVED_FAMILY`,
`GROUNDING_UNAVAILABLE`, `ADMITTED`, `SURFACED`, `CAUTIONARY`, `BLOCKED` — it relies on
Contract 001's own definition of that term, unaltered, and does not restate or redefine it.

## 2. Contract 003 validity constraints

**These bind this document only. They are not Contract 002's V1/V2, and Contract 002's V1/V2
do not automatically bind this document.** Contract 002 §2 itself explains why a successor
needs fresh constraints rather than inherited ones: its own V1/V2 bind only *"this
document"* (Contract 002), and *"a successor document needs its own, independently stated
constraints if it is to be checked the same way"*
(`contract_002_domain_resolution_invariants.md:100-102`). These are that statement, drafted
fresh for this document, not inherited.

Named **"Contract 003 V1"** and **"Contract 003 V2"** throughout, never bare "V1" or "V2", so
a citation into this section can never be mistaken for a citation into Contract 001 §2 or
Contract 002 §2.

### Contract 003 V1 — Cardinality independence

> No predicate in I1 through I9 may name a specific domain. This document currently carries
> no invariant beyond I1–I9, and none may be added to it without a separate, explicit
> operator determination — made and recorded the same way I8's and I9's own determinations
> were, never by drafting alone. Any invariant added under such a determination is bound by
> this constraint on the same terms as I1–I9.

**Conformance check.** Substitute the domain set with any other domain set, of any size,
including a set of one. If any invariant's meaning, or I9's behavior, changes as a result,
this constraint is violated.

### Contract 003 V2 — Epistemic and causal distinction preservation

> Any epistemic or causal distinction that this document's own normative additions introduce
> or newly require — at minimum, the distinction I9 requires between components governed by
> an identical governed cause under I9(e) and those that are not — must remain recoverable,
> and must never be allowed to disappear merely because the conditions it distinguishes
> eventually surface through the same already-governed terminal classification or shared
> reason representation.

**This constraint governs Contract 003's own new normative additions only — currently, I9.**
It does not reach I1–I8 (carried forward, not introduced by this document), and it does not
reach, reinterpret, invalidate, prohibit, or supersede I8(f)'s own causal-preservation
requirement or Contract 001 §5.1's terminal mapping, both of which remain governed exactly as
previously signed/locked.

**Conformance check.** For any invariant this document itself introduces (currently: I9 only)
that relies on more than one distinguishable condition producing the same representation,
confirm that invariant also requires the originating condition to remain recoverable. I9(g)
is checked against this constraint directly; no other clause of this document currently
introduces such a collapse.

## 3. Invariants carried forward from Contract 002 §§3–4

**I1 through I8 below carry the substance of Contract 002 §§3–4 forward without weakening,
broadening, or rewriting.** Unlike Contract 001 §6's relocation into Contract 002, which
required three reference-qualification changes to I1 and I6 because those referenced this
document by bare, document-relative wording, **I1 through I8 as currently written in Contract
002 contain no such reference.** Every cross-reference inside I1–I8 — `Contract 001 §2, V1`
(I1); `Ruling 001`/`Ruling 002` throughout; `I5, I7 above` (I8(d)); `Contract 001 §§3–4`
(I8(a)) — already resolves correctly regardless of which document houses I1–I8, checked
individually against each occurrence. **I1 through I8 therefore carry forward byte-identical
to `contract_002_domain_resolution_invariants.md:168-230`, with zero textual changes.** This
is confirmed directly, not assumed from the absence of a defect found elsewhere.

**I1 — Cardinality independence.** Contract 001 §2, V1. No predicate may name a specific
domain.

**I2 — Resolution order is fixed.** Domain → family → grounding. Ruling 002 Addendum A.

**I3 — Ambiguity is preserved, never collapsed.** A concept with multiple domain candidates
stays in `AMBIGUOUS_DOMAIN` until evidence discharges it. Selecting arbitrarily is
prohibited.

**I4 — No cross-domain substitution.** No transition may produce a grounding candidate
outside the concept's domain. Ruling 002 §5.2.

**I5 — No silent terminal.** Every terminal state carries its reason to the output. Ruling
001 Invariant 1, Ruling 002 §5.3.

**I6 — Unknown is not false. Uncertain is not resolved.** The two principles that have
emerged across Ruling 001, Ruling 002 and Contract 001, stated as one invariant because they
fail together: both are violated by the same move — treating an absence of evidence as a
determination.

**I7 — `SURFACED` is terminal.** A `SURFACED` result is not a degraded `ADMITTED` result and
may not be auto-resolved through taxonomy expansion. Ruling 001 §4, Ruling 002 §5.2, §5.4.

**I8 — Grounding-Terminal Halting and Causal Preservation.**

(a) Terminal conditions halt what follows; they do not merely imply that it should stop. A
terminal condition reached at any stage of domain → family → grounding resolution (I2)
actually prevents progression into a downstream stage that requires that stage to have
resolved successfully — rather than leaving that property to depend on what else does or
does not call into the next stage. Concretely, and consistently across the resolution
sequence: `UNRESOLVED_DOMAIN` and `AMBIGUOUS_DOMAIN` do not proceed into family resolution or
into grounding; `UNRESOLVED_FAMILY` does not proceed into grounding. This invariant invents no
new terminal state and changes the definition of none — it enforces the halting property of
states Contract 001 §§3–4 already define as terminal.

(b) Where family resolution has legitimately succeeded but grounding resolution finds no
legitimate grounding candidate for the resolved family, grounding halts.

(c) Where legitimate grounding candidates exist for the resolved family but none is legal
under the fusion's modality constraints, grounding halts on the same basis as (b).

(d) The terminal outcome for both (b) and (c) is `GROUNDING_UNAVAILABLE`, carrying the
terminal and surfacing behavior already established for that state (Ruling 002 §5.2, §5.3;
I5, I7 above). Neither condition may instead search further, substitute a candidate, or
manufacture one merely to return something concrete.

(e) No new generic or universal grounding fallback is authorized by this invariant, for
either (b) or (c). This is a separate matter from Ruling 002 §5.4, which **is not** a generic
or universal fallback, is not newly authorized by this invariant, and is governed solely by
its own existing predicates and by (g) below.

(f) The distinction between (b) and (c) — whether no legitimate grounding candidate ever
existed, or legitimate grounding candidates existed but were all illegal for the fusion —
must remain available in authoritative, machine-readable state, such that any downstream
component or authorized consumer that needs to act upon, surface, audit, or explain a
`GROUNDING_UNAVAILABLE` terminal governed by this invariant can recover which of the two
governed causal conditions occurred. No particular representation, schema, field, or storage
mechanism is prescribed by this invariant.

(g) Ruling 002 §5.4 is unaffected, exactly as governed there: the `Indomitable Will` fallback
it authorizes remains available only within the scope and under the predicates §5.4 itself
already states, on no other basis, and only once §5.4's own governing predicate is actually
established. This invariant neither broadens that fallback, nor extends it by analogy or
precedent to any case §5.4 does not already reach.

Ruling 002 §5.2, §5.3, §5.4; Disposition 002.

## 4. New invariant — the GAP-5 obligation

**Numbering note.** I1–I8 retain their existing numbers, carried forward unchanged (§3
above). No invariant numbered I9 exists anywhere in this corpus as of this drafting
(`Contract 003 V1` confirms this document currently carries none beyond I1–I8 until this
section). I9 is therefore the only number that introduces no collision, on the same
sequential convention I8 itself followed when Contract 002 added GAP-4's invariant as the
number after Contract 001's highest existing one.

**I9 — `SURFACED` Payload Preservation and Attribution.**

(a) This invariant governs only the payload of a fusion result already classified
`SURFACED` (Contract 001 §5.1). It does not itself classify a fusion's aggregate result as
`ADMITTED`, `SURFACED`, `CAUTIONARY`, or `BLOCKED`, and creates no rule, partial or implicit,
for deriving that classification from a set of mixed per-component terminal states. That
derivation is Ruling 002 §10.3 / Seam 3 (dispositional synthesis), ruled non-blocking and
separate by CR-007, and is unaffected by this invariant in either direction.

(b) Every `SURFACED` result preserves every component that resolved successfully through
domain, family, and grounding resolution (I2). Ruling 002 §5.3; Contract 001 §5.1.

(c) Every `SURFACED` result preserves every component that individually reaches
`GROUNDING_UNAVAILABLE` after its own domain and family resolution legitimately succeeded —
i.e., a component legitimately halted under I8(b) or I8(c). This clause does not reach a
component that individually halted earlier, at `UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`, or
`UNRESOLVED_FAMILY` — those map to `CAUTIONARY`, not `SURFACED` (Contract 001 §5.1; I8(a)) —
and does not decide how a fusion's overall result is classified when its components'
individual terminal states differ across stages (see (a)).

(d) The governed reason for each component preserved under (c) must remain attributable to
that specific component. A `SURFACED` result may not carry an unattributed pool of reasons
alongside an unattributed set of components preserved under (c) such that which reason
governs which component cannot be determined. I5.

(e) A single reason representation may cover more than one component preserved under (c)
only where those components are governed by the identical governed cause — not merely the
same reason label or text, and not merely the same category of failure in the abstract. For
every component preserved under (c), an authorized consumer must be able to determine which
governed cause applies specifically to that component; aggregate knowledge that one of
several causes occurred somewhere within the preserved set, without resolving which
component had which, does not satisfy this clause.

(f) The failure, rejection, or unresolved status of a component preserved under (c) does not
permit a component preserved under (b) to be discarded, merely because another component
terminates unsuccessfully. This is a preservation rule only. It does not itself establish, and may
not be read to relax, broaden, or create an exception to, whether a component qualifies for
preservation under (b) — which requires the component to have already, independently, and
prior to this invariant's application, satisfied every applicable upstream validity
requirement, including I3, I4, and I6 — or under (c) — which requires the component's
`GROUNDING_UNAVAILABLE` halt to be already actually governed by I8, on I8(b) or I8(c)'s
basis, with I8(f)'s recoverability property intact. This clause preserves whichever status
under (b) or (c) a component already independently had before aggregation, and creates
neither status where it did not already exist.

(g) Where the governed reason for two or more components preserved under (c) collapses onto
the same representation under (e), the originating causal distinction between those
components' governed causes must remain recoverable from the authoritative, machine-readable
result for each affected component — not merely inferable, and not merely reconstructable by
an external process — without requiring that distinction to be duplicated into a dedicated
outward payload field. This clause applies, to this invariant's own reason-cardinality
requirement under (e), the same representation-neutral technique I8(f) already establishes
for the distinct causal distinction I8(f) itself governs; it does not extend I8(f)'s own
scope, and I8(f) continues to govern only the distinction between I8(b) and I8(c) exactly as
before.

(h) No field name, enum, class, JSON structure, API shape, serialization, storage format,
database representation, or other implementation mechanism is chosen or required by this
invariant, for (b) through (g) or for any part of this invariant.

Ruling 002 §5.3; Contract 001 §5.1; Disposition 003.

## 5. Exclusions

**This document does not govern, and any text elsewhere in this document that appears to
state a normative condition on any of the following is a defect in this document:**

| Excluded | Basis / where it belongs instead |
|---|---|
| domain names, domain count | lore — operator (Contract 001 §1, unchanged) |
| provider choice, prompts, model usage, caching/storage strategy | Ruling 001 §5, GAP-6, GAP-7 (unchanged) |
| registry expansion rules | Ruling 002 §3, §8 (unchanged) |
| any implementation mechanism, schema, enum, field, API shape, or storage format | not decided by this document; see I8(f), I9(g)-(h) |
| Ruling 002 §10.3 / Seam 3 (dispositional synthesis) | ruled non-blocking and separate by CR-007; untouched here |
| Ruling 002 §10.5 / §10.7 (family/domain reclassification) | reserved to a future dedicated ruling-level instrument per Disposition 001; untouched here |
| Fusion Engine C1–C6 architecture or implementation | FE Requirements v0.1, ADR-001; untouched here |
| GAP-5 closure itself | recording closure in `open_contract_gaps.md` is a separate act, performed after LOCK, not by this document's drafting or existence |
| implementation authorization | a separate, independent operator act, not supplied by this document or by GAP-5's eventual closure |
| any FE Requirements §39 hold other than the one Ratification 002 narrows for preparation and review | untouched; no other hold is released or modified |
| any edit to code, registries, or any other governance document | no authorization of any kind is granted by this document |

## 6. Future governance

**Once this document reaches LOCKED status, it is fully subject to `amendment_policy.md`,
exactly as any other locked document in this corpus is.** This statement is declarative, not
creative — `amendment_policy.md` §2 already binds every LOCKED document in this corpus
automatically, whether or not this section existed.

Concretely, and without creating any exception `amendment_policy.md` does not already state:

- Once LOCKED, no part of this document's text is amended, for any reason, including a
  defect this or any future corpus instrument records against it. There is no minor-edit
  exception, no repair exception, no emergency exception, and no convenience exception, now
  or ever.
- The only way any part of this document stops governing is **supersession** — a future
  document stating in its own text that it supersedes identified text in this one, at the
  granularity of an addressable division, precisely enough to resolve without inference.
- This document, once superseded in whole or in part, is never itself touched, edited,
  annotated, or corrected on that account. It remains on the page exactly as attested.

## 7. Sign-off checklist

**Every row below is blank. Attestation text is written at the time each row is actually
attested, per this corpus's established practice. Attesting every row here is what completes
§7 and makes this document eligible to be marked SIGNED; it is not itself the act that marks
it SIGNED. No row's box is filled in during this drafting pass.**

- [x] §1 Relationship to Contract 002 and Contract 001 — signed 2026-09-20. Verified: Contract
  002 §§1, 2, 5, 6, and 7 are correctly named as the complete set of Contract 002's
  non-superseded divisions — mechanically confirmed (Contract 002 carries §§1–7; superseded
  here is §§3–4; the remaining five are exactly the five named, none omitted or duplicated).
  Contract 001 §§1–5, 7, and 8 are correctly stated as remaining governing via Contract 002 §1
  (`contract_002_domain_resolution_invariants.md:85`), unaltered by this document; Contract
  001 §6 is correctly stated as historically superseded and untouched. No state, transition,
  or terminal-condition term is redefined; each relies on Contract 001's own definition.
  **Not attested by this signature:** the correctness of V1/V2, I1–I9's own content, the
  exclusions list, or the future-governance clause — those are separate rows below.
- [x] §2 Contract 003 V1 (cardinality independence) — signed 2026-09-20. Verified: the
  conformance check was run by extraction against I1 through I9 as currently written — a
  full-document scan for domain names (`human-excellence`, `supernatural`) returned zero hits.
  This constraint is independently stated for this document, drafted fresh per Contract 002
  §2's own stated rationale for why a successor needs its own constraints
  (`contract_002_domain_resolution_invariants.md:100-102`), and does not rely on Contract
  002's own V1. **Not attested by this signature:** I1–I8's fidelity to Contract 002 §§3–4
  (§3's row), I9's sufficiency against GAP-5 (§4's row), or Contract 003 V2 (the next row).
- [x] §2 Contract 003 V2 (epistemic/causal distinction preservation) — signed 2026-09-20.
  Verified: the scope-narrowing to Contract 003's own new normative additions (currently I9
  only) is correctly stated and does not reach I1–I8. I9(g) is the only clause introducing a
  same-representation collapse — confirmed by scanning I9(a)-(h) for collapse/same-
  representation language, found only within (g) — and I9(g) requires the originating
  condition to remain recoverable. I8(f)'s own pre-existing causal-preservation requirement
  and Contract 001 §5.1's terminal mapping are correctly stated as unreached and ungoverned
  by this constraint. **Not attested by this signature:** I1–I8's fidelity to Contract 002
  §§3–4 (§3's row), I9's sufficiency against GAP-5 (§4's row).
- [x] §3 I1–I8, carried forward — signed 2026-09-20. Verified: I1 through I8 are byte-identical
  to Contract 002 §§3–4 (`contract_002_domain_resolution_invariants.md:168-230`) — confirmed
  by content-anchored, whitespace-normalized comparison, with zero textual changes required,
  unlike the three reference-qualification changes needed when Contract 001 §6 relocated into
  Contract 002. No substance weakened, broadened, or rewritten anywhere. **Not attested by
  this signature:** I9's content or its sufficiency against GAP-5 (§4's row), or the
  exclusions/future-governance sections (§5, §6's rows).
- [x] §4 I9, the GAP-5 invariant — signed 2026-09-20. Verified: I9 is a single invariant
  carrying (a) the `SURFACED`-only applicability trigger, with Seam 3/§10.3 dispositional
  synthesis expressly excluded; (b) preservation of successfully resolved components; (c)
  preservation of components legitimately halted to `GROUNDING_UNAVAILABLE` under I8(b)/(c),
  expressly scoped per Disposition 003 §2.2 and excluding `UNRESOLVED_DOMAIN`/
  `AMBIGUOUS_DOMAIN`/`UNRESOLVED_FAMILY`; (d) per-component reason attribution; (e)
  reason-cardinality limited to identical governed cause, not label alone; (f) partial-success
  preservation, tracking the operative closure condition's own causal language ("merely
  because another component terminates unsuccessfully") rather than a narrower paraphrase,
  and creating neither accepted nor `GROUNDING_UNAVAILABLE` status where it did not already
  independently exist; (g) causal recoverability where reasons collapse, applying I8(f)'s
  established representation-neutral technique without extending I8(f)'s own scope; (h) no
  implementation mechanism chosen or required. Confirmed: I9 maps to every element of the
  operative closure condition (`open_contract_gaps.md:882-891`), tested against eight
  simulated payload cases with one unambiguous obligation each, and passes Contract 003 V1's
  conformance check (no domain named anywhere in (a)-(h)). This approval and signature do not
  themselves supersede Contract 002 §§3–4, close GAP-5, mark this document SIGNED or LOCKED,
  or authorize implementation of any kind. **Not attested by this signature:** the exclusions
  list (§5's row) or the future-governance clause (§6's row).
- [x] §5 Exclusions — signed 2026-09-20. Verified: each of the eleven excluded topics routes
  to its actual existing authority. The self-test — that none of these topics appears
  elsewhere in this document as a live normative condition — passes: I9(a)'s and I9(h)'s
  references to Seam 3 and implementation mechanisms are disclaimers only, not normative
  conditions on those subjects, consistent with how I8(f) already uses the identical pattern
  in already-signed text. This approval does not expand Contract 003's authority into any
  excluded subject. **Not attested by this signature:** the future-governance clause (§6's
  row).
- [x] §6 Future governance — signed 2026-09-20. Verified: this section grants Contract 003
  nothing new — `amendment_policy.md` §2 already binds every LOCKED document in this corpus
  automatically, and this row restates that plainly. No minor-edit, repair, emergency, or
  convenience exception is created; the text forecloses all four, matching `amendment_policy.md`
  §1's own rule. The supersession mechanism is restated correctly: addressable-division
  granularity, must resolve without inference, superseded text never touched. **Not attested
  by this signature:** nothing further — this is the final §7 row.

---

**Drafted, not signed, not locked.** This document supersedes nothing until a separate
operator act marks it SIGNED, and a further separate operator act marks it LOCKED. GAP-5
remains open against `open_contract_gaps.md`. This draft's existence, by itself, satisfies and
records nothing. If this document later reaches LOCKED status, the supersession defined above
becomes operative; and if the LOCKED text then actually conforms to GAP-5's operative closure
condition, that substantive closure condition becomes satisfied as a factual matter at that
time, subject to verification — satisfaction, if it occurs, occurs at LOCK, not later. GAP-5's
recorded status in `open_contract_gaps.md` nonetheless remains OPEN regardless of LOCK, until a
separate, subsequent act verifies that conformance and records the closure there; that act
confirms a fact already true and does not itself create it.

---

**Drafting note on naming.** "Contract 003" and the filename
`contract_003_gap5_surfaced_payload_preservation.md` were finalized by operator determination,
2026-09-20. This determination fixes the document's identity only; it does not itself attest
any §7 row or mark this document SIGNED or LOCKED.
