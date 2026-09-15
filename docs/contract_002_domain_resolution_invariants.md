# WorldCraft Contract 002 — Domain Resolution Invariants

**Type:** Resolution contract. Successor to Contract 001, superseding one division of it.
**Supersedes:** Contract 001 (`contract_001_domain_resolution.md`) §6, "Invariants," lines 215–235,
in full. No other division of Contract 001 is superseded by this document.

**Status:** **LOCKED (2026-09-15).** Binding. Supersession of Contract 001 §6 is now operative: this
document is the operative source for the invariants Contract 001 §6 previously carried. Contract 001
§6's own text remains historically intact and unedited; it no longer governs.

```
DRAFT
  →  every row of §7 attested and dated              (attestation completed)
  →  a separate operator act marking this document's Status line SIGNED
  →  SIGNED               (attested in full; not locked; not yet superseding anything)
  →  a separate, subsequent operator act marking this document's Status line LOCKED
  →  LOCKED                        (supersession of Contract 001 §6 becomes operative)
```

**Each arrow above is a distinct act. No earlier stage substitutes for a later one, and none is
automatic from the one before it:**

- Attesting fewer than all seven rows of §7 activates nothing. This document remains DRAFT, with zero
  effect on Contract 001 §6, for however long it persists in that state.
- Completing every row of §7 makes this document **eligible** to be marked SIGNED. **Completing the
  final row does not, by itself, mark the document SIGNED** — reaching SIGNED requires a separate
  operator act, updating this document's own Status line, taken after, and only after, every row of §7
  is attested and dated.
- **Marking this document SIGNED does not, by itself, mark it LOCKED, and does not supersede Contract
  001 §6.** A document that is SIGNED but not yet LOCKED has no governing effect; Contract 001 §6
  continues to govern in full.
- **LOCKED is reached only by a further, separate, subsequent operator act** — a second, later update to
  this document's own Status line — taken after, and only after, the document is SIGNED. LOCKED is
  never reached automatically merely because the document was marked SIGNED, and is never reached
  without both completed §7 attestation and the prior SIGNED state.
- **Supersession of Contract 001 §6 becomes operative only once this document reaches LOCKED** — not at
  DRAFT, not at partial attestation, and not at SIGNED.

---

**Why this document exists.** Contract 001 locked 2026-08-25. `amendment_policy.md` §1 forecloses any
amendment of locked text, without exception, for any reason, including a defect the corpus has itself
recorded. GAP-4's closure condition (`open_contract_gaps.md:183-186`) requires that "Contract 001
carries an invariant" making terminal conditions halting and bounding or removing the two named
grounding-fallback sites. A locked Contract 001 cannot gain that invariant directly; per
`amendment_policy.md` §3, supersession — naming the superseded division precisely, at the granularity
of an addressable division — is the only remaining route. `open_contract_gaps.md`'s GAP-4
successor-contract restatement was approved by the operator as the operative routing target for that
closure on 2026-09-15. This document is the successor contract that restatement anticipated, opened by
a further, explicit operator act on the same date lifting the hold on beginning this governance
process. It supersedes only Contract 001 §6 — the division carrying the enforcement invariants — by
operator determination, not by inference from document structure.

Its substantive content for the new invariant is Disposition 002
(`disposition_002_gap4_grounding_terminal_policy.md`), which records the operator's determination of
what GAP-4's eventual invariant must require. Disposition 002 is authoritative operator input for this
drafting; it is not itself the invariant, and this document is what supplies the invariant Disposition
002 anticipated.

**What this document does not do.**

- It does not sign, attest, or lock itself. Every row in §7 is blank.
- It does not close GAP-4 in `open_contract_gaps.md`. Recording that closure — if and when this
  document locks — is a separate act under that register's own rules (the same separation GAP-8's and
  GAP-9's closures already observe), performed after LOCK, not by this document's drafting or
  existence.
- It does not touch, bundle, or reserve a place for GAP-5. GAP-5's own successor-contract restatement
  remains "proposed / not operative"; nothing here changes that, and no invariant number is reserved
  for it.
- It does not edit Contract 001. Contract 001 receives no edit, annotation, or mark of any kind as a
  result of this document's drafting, signing, or eventual lock. Contract 001 §6's text and its
  existing sign-off row remain on the page exactly as attested, per `amendment_policy.md:80-82`, for as
  long as Contract 001 exists.
- It does not authorize any edit to `logic_auditor.py`, any other existing code file, or any registry.
  It does not authorize implementation of Seam 2, C4, C5, or C6, or any other Fusion Engine work.
- It does not decide Ruling 002 §10.3 / Seam 3, or §10.5 / §10.7's family/domain reclassification.
- It does not adopt any domain taxonomy, domain list, or domain count.
- It does not choose an implementation mechanism, schema, enum, field, or storage format for anything
  it requires.

---

## 1. Relationship to Contract 001

Contract 001 §§1–5, 7, and 8 **remain governing and unchanged.** This document supersedes §6 only.
Nothing in this document should be read as reopening, qualifying, or casting doubt on any other section
of Contract 001, including its V1/V2 validity constraints (§2), its state and transition definitions
(§3, §4), its consolidated pipeline and terminal mapping (§5), its conservative-principle discussion
(§7), or its own future-extensibility clause (§8) — all of which continue to bind exactly as signed.

Where this document references a state, transition, or terminal condition not redefined here —
`UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`, `RESOLVED_DOMAIN`, `UNRESOLVED_FAMILY`,
`GROUNDING_UNAVAILABLE`, `ADMITTED`, `SURFACED`, `CAUTIONARY`, `BLOCKED` — it relies on Contract 001's
own definition of that term, unaltered, and does not restate or redefine it.

## 2. Contract 002 validity constraints

**These bind this document only. They are not Contract 001's V1 and V2, and Contract 001's V1 and V2
do not automatically bind this document.** Contract 001 `:50` scopes V1 and V2 to "the whole of this
contract, §1 through §8" — meaning Contract 001, not any other document. A successor document needs its
own, independently stated constraints if it is to be checked the same way. These are that statement,
drafted fresh for this document, not inherited.

To avoid the exact defect this document's own §3 corrects in I1 — a bare, document-relative reference
that misresolves once read outside its home document — these constraints are named **"Contract 002 V1"**
and **"Contract 002 V2"** throughout, never bare "V1" or "V2", so a citation into this section can never
be mistaken for a citation into Contract 001 §2.

### Contract 002 V1 — Cardinality independence

> No predicate in I1 through I8 may name a specific domain. This document currently carries no
> invariant beyond I1–I8, and none may be added to it without a separate, explicit operator
> determination — made and recorded the same way I8's own determination was, never by drafting alone.
> Any invariant added under such a determination is bound by this constraint on the same terms as I1–I8.

**Conformance check.** Substitute the domain set with any other domain set, of any size, including a
set of one. If any invariant's meaning, or I8(b)/(c)/(d)/(f)'s behavior, changes as a result, this
constraint is violated.

### Contract 002 V2 — Epistemic and causal distinction preservation

> Any epistemic or causal distinction that this document's own normative additions introduce or newly
> require — at minimum, the distinction I8(f) requires between (b) and (c) — must remain recoverable,
> and must never be allowed to disappear merely because the conditions it distinguishes eventually
> surface through the same already-governed terminal classification.

**This constraint governs Contract 002's own new normative additions only — currently, I8.** It does
not reach I1–I7 (carried forward, not introduced by this document), and it does not reach, reinterpret,
invalidate, prohibit, or supersede **Contract 001 §5.1's existing terminal mapping**, including that
mapping's deliberate collapse of `UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`, and `UNRESOLVED_FAMILY` onto
the single `CAUTIONARY` fusion result. That mapping is unsuperseded by this document, remains governed
by Contract 001 I5 exactly as signed, and is neither tested against nor violated by this constraint.

**Conformance check.** For any invariant this document itself introduces (currently: I8 only) that
relies on more than one distinguishable condition producing the same terminal state, confirm that
invariant also requires the originating condition to remain recoverable. I8(f) is checked against this
constraint directly; no other clause of this document currently introduces such a collapse.

## 3. Invariants carried forward from Contract 001 §6

**I1 through I7 below carry the substance of Contract 001 §6 forward without weakening, broadening, or
rewriting.** Three textual changes distinguish this section's text from Contract 001's, all in I1 and
I6, and all are **reference-qualification changes made necessary by relocating this text out of the
document that originally made those references resolve correctly** — none alters what any invariant
requires:

1. **I1:** `§V1` → `Contract 001 §2, V1`. Read inside Contract 001, `§V1` means Contract 001's own §2
   V1; read anywhere else, it resolves to nothing.
2. **I6:** `001` → `Ruling 001`, and `002` → `Ruling 002`. Read inside Contract 001, whose own
   introduction establishes "Rulings 001 and 002" as the local shorthand's referent, the bare numerals
   are locally unambiguous. Relocated into a document itself named "Contract 002," the same bare
   numerals risk misreading as "Contract 001, Contract 002" — every other invariant in this section
   (I2, I4, I5, I7) already spells "Ruling 001"/"Ruling 002" in full, and this qualification brings I6
   into line with that pattern rather than leaving it the one holdout.
3. **I6:** `this contract` → `Contract 001`. Read inside Contract 001, `this contract` means Contract
   001; copied verbatim into a different document, it would wrongly mean that document instead.

No other word of I1–I7 differs from `contract_001_domain_resolution.md:217-235`.

**I1 and Contract 002 V1 are not duplicates, despite stating the same rule.** I1, below, is a
**behavioral/runtime invariant governing the resolution system** — carried forward from Contract 001
§6, where it already served that role alongside V1 rather than merely restating it. Contract 002 V1
(§2 above) is a **validity/conformance constraint governing this document's own normative text** —
freshly drafted for this document, mirroring the distinct role Contract 001's own V1 plays for Contract
001's text. The two check different things and neither substitutes for the other, exactly as V1 and I1
did not substitute for each other inside Contract 001.

**I1 — Cardinality independence.** Contract 001 §2, V1. No predicate may name a specific domain.

**I2 — Resolution order is fixed.** Domain → family → grounding. Ruling 002 Addendum A.

**I3 — Ambiguity is preserved, never collapsed.** A concept with multiple domain candidates stays
in `AMBIGUOUS_DOMAIN` until evidence discharges it. Selecting arbitrarily is prohibited.

**I4 — No cross-domain substitution.** No transition may produce a grounding candidate outside the
concept's domain. Ruling 002 §5.2.

**I5 — No silent terminal.** Every terminal state carries its reason to the output. Ruling 001
Invariant 1, Ruling 002 §5.3.

**I6 — Unknown is not false. Uncertain is not resolved.** The two principles that have emerged across
Ruling 001, Ruling 002 and Contract 001, stated as one invariant because they fail together: both are
violated by the same move — treating an absence of evidence as a determination.

**I7 — `SURFACED` is terminal.** A `SURFACED` result is not a degraded `ADMITTED` result and may not
be auto-resolved through taxonomy expansion. Ruling 001 §4, Ruling 002 §5.2, §5.4.

## 4. New invariant — the GAP-4 obligation

**I8 — Grounding-Terminal Halting and Causal Preservation.**

(a) Terminal conditions halt what follows; they do not merely imply that it should stop. A terminal
condition reached at any stage of domain → family → grounding resolution (I2) actually prevents
progression into a downstream stage that requires that stage to have resolved successfully — rather
than leaving that property to depend on what else does or does not call into the next stage.
Concretely, and consistently across the resolution sequence: `UNRESOLVED_DOMAIN` and `AMBIGUOUS_DOMAIN`
do not proceed into family resolution or into grounding; `UNRESOLVED_FAMILY` does not proceed into
grounding. This invariant invents no new terminal state and changes the definition of none — it
enforces the halting property of states Contract 001 §§3–4 already define as terminal.

(b) Where family resolution has legitimately succeeded but grounding resolution finds no legitimate
grounding candidate for the resolved family, grounding halts.

(c) Where legitimate grounding candidates exist for the resolved family but none is legal under the
fusion's modality constraints, grounding halts on the same basis as (b).

(d) The terminal outcome for both (b) and (c) is `GROUNDING_UNAVAILABLE`, carrying the terminal and
surfacing behavior already established for that state (Ruling 002 §5.2, §5.3; I5, I7 above). Neither
condition may instead search further, substitute a candidate, or manufacture one merely to return
something concrete.

(e) No new generic or universal grounding fallback is authorized by this invariant, for either (b) or
(c). This is a separate matter from Ruling 002 §5.4, which **is not** a generic or universal fallback,
is not newly authorized by this invariant, and is governed solely by its own existing predicates and by
(g) below.

(f) The distinction between (b) and (c) — whether no legitimate grounding candidate ever existed, or
legitimate grounding candidates existed but were all illegal for the fusion — must remain available in
authoritative, machine-readable state, such that any downstream component or authorized consumer that
needs to act upon, surface, audit, or explain a `GROUNDING_UNAVAILABLE` terminal governed by this
invariant can recover which of the two governed causal conditions occurred. No particular
representation, schema, field, or storage mechanism is prescribed by this invariant.

(g) Ruling 002 §5.4 is unaffected, exactly as governed there: the `Indomitable Will` fallback it
authorizes remains available only within the scope and under the predicates §5.4 itself already states,
on no other basis, and only once §5.4's own governing predicate is actually established. This invariant
neither broadens that fallback, nor extends it by analogy or precedent to any case §5.4 does not already
reach.

Ruling 002 §5.2, §5.3, §5.4; Disposition 002.

## 5. Exclusions

**This document does not govern, and any text elsewhere in this document that appears to state a
normative condition on any of the following is a defect in this document:**

| Excluded | Basis / where it belongs instead |
|---|---|
| domain names, domain count | lore — operator (Contract 001 §1, unchanged) |
| provider choice, prompts, model usage, caching/storage strategy | Ruling 001 §5, GAP-6, GAP-7 (unchanged) |
| registry expansion rules | Ruling 002 §3, §8 (unchanged) |
| any implementation mechanism, schema, enum, field, API shape, or storage format | not decided by this document; see I8(f) |
| GAP-5 (`SURFACED` payload completeness) | tracked separately; its successor-contract routing is not operative and is not addressed here |
| Ruling 002 §10.3 / Seam 3 (dispositional synthesis) | ruled non-blocking and separate by CR-007; untouched here |
| Ruling 002 §10.5 / §10.7 (family/domain reclassification) | reserved to a future dedicated ruling-level instrument per Disposition 001; untouched here |
| Fusion Engine C1–C6 architecture or implementation | FE Requirements v0.1, ADR-001; untouched here |
| any edit to code, registries, or any other governance document | no authorization of any kind is granted by this document |

## 6. Future governance

**Once this document reaches LOCKED status, it is fully subject to `amendment_policy.md`, exactly as
any other locked document in this corpus is.** This statement is declarative, not creative: it does not
grant this document that treatment and does not need to, because `amendment_policy.md` §2 already binds
"every document in this corpus carrying a LOCKED status, whatever their number, including a set of
one" — this document included, automatically, whether or not this section existed. It is stated here
only so a reader of this document does not have to consult a second document to learn it.

Concretely, and without creating any exception `amendment_policy.md` does not already state:

- Once LOCKED, no part of this document's text is amended, for any reason, including a defect this or
  any future corpus instrument records against it. There is no minor-edit exception, no repair
  exception, no emergency exception, and no convenience exception, now or ever.
- The only way any part of this document stops governing is **supersession** — a future document
  stating in its own text that it supersedes identified text in this one, at the granularity of an
  addressable division, precisely enough to resolve without inference.
- This document, once superseded in whole or in part, is never itself touched, edited, annotated, or
  corrected on that account. It remains on the page exactly as attested.

## 7. Sign-off checklist

**Every row below is blank. Attestation text — what was checked, what is and is not attested, and any
carve-outs — is written at the time each row is actually attested, per this corpus's established
practice (cf. `contract_001_domain_resolution.md`'s per-section rows). Attesting every row here is what
completes §7 and makes this document eligible to be marked SIGNED (see the status block above); it is
not itself the act that marks it SIGNED. None is pre-written here, and no row's box is filled in during
this drafting pass.**

- [x] §1 Relationship to Contract 001 — signed 2026-09-15. Verified: Contract 001 receives no edit as
  a result of this document (`git diff` against `contract_001_domain_resolution.md` empty at every
  audit pass this session); §§1–5, 7, 8 remain governing and unchanged, and this document supersedes §6
  only, matching the operator's explicit determination that §6 is the target division. Every
  state/terminal condition this document references elsewhere (`UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`,
  `RESOLVED_DOMAIN`, `UNRESOLVED_FAMILY`, `GROUNDING_UNAVAILABLE`, `ADMITTED`, `SURFACED`, `CAUTIONARY`,
  `BLOCKED`) was checked and none is redefined anywhere in this document. **Not attested by this
  signature:** the correctness of I1–I8's own content, or of V1/V2 — those are separate rows below.
- [x] §2 Contract 002 V1 (cardinality independence) — signed 2026-09-15. Verified: the conformance
  check was run by extraction against I1 through I8 as currently written — a full-document scan for
  domain names (`human-excellence`, `supernatural`) returned zero hits, and each invariant was checked
  individually; no predicate names a specific domain. This constraint is independently stated for this
  document and does not rely on Contract 001's own V1, which by its own `:50` scope binds Contract 001
  only. The self-restriction on adding future invariants (requiring a separate, explicit operator
  determination, never mere drafting) is accurately stated, and this document currently carries no
  invariant beyond I1–I8. **Not attested by this signature:** I1–I7's fidelity to Contract 001 §6 (§3's
  row), I8's sufficiency against GAP-4 (§4's row), or Contract 002 V2 (the next row).
- [x] §2 Contract 002 V2 (epistemic/causal distinction preservation) — signed 2026-09-15. Verified: the
  scope-narrowing to Contract 002's own new normative additions (currently I8 only) is correctly stated
  and does not reach I1–I7. The non-disturbance claim about Contract 001 §5.1's existing terminal
  mapping — including its deliberate collapse of `UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`, and
  `UNRESOLVED_FAMILY` onto `CAUTIONARY` — was checked directly against the live, unedited text of
  `contract_001_domain_resolution.md` §5.1 (`git diff` empty for that file at every check this session)
  and is accurate; this constraint neither tests nor governs that mapping. The conformance check passes:
  I8(f) is the only clause introducing a same-terminal-state collapse ((b)/(c) onto
  `GROUNDING_UNAVAILABLE`), and I8(f) requires the originating condition to remain recoverable; I8(a)'s
  treatment of `UNRESOLVED_DOMAIN`/`AMBIGUOUS_DOMAIN` does not collapse them into a shared state and so
  falls outside this check; no other clause introduces an uncovered collapse. **Not attested by this
  signature:** I1–I7's fidelity to Contract 001 §6 (§3's row), I8's sufficiency against GAP-4 (§4's
  row).
- [x] §3 I1–I7, carried forward — signed 2026-09-15. Verified: I1 through I7 are byte-identical to
  Contract 001 §6 (`contract_001_domain_resolution.md:217-235`) except exactly three textual changes —
  I1's `§V1` → `Contract 001 §2, V1`; I6's `001` → `Ruling 001` and `002` → `Ruling 002`; I6's
  `this contract` → `Contract 001` — checked programmatically by word-level diff against the live
  Contract 001 text; I2, I3, I4, I5, and I7 confirmed byte-identical, with no substance weakened,
  broadened, or rewritten anywhere. The disclosure paragraph (140–157) accurately and completely
  enumerates all three changes, and the I1-vs-Contract-002-V1 note (159–165) correctly distinguishes the
  two without either substituting for the other. **Not attested by this signature:** I8's content or its
  sufficiency against GAP-4 (§4's row), or the exclusions/future-governance sections (§5, §6's rows).
- [x] §4 I8, the GAP-4 invariant — signed 2026-09-15. Verified: I8 is a single invariant carrying
  (a) terminal-halting, including `AMBIGUOUS_DOMAIN` per the operator's explicit determination extending
  Disposition 002's named states, and stating plainly that no new terminal state is invented; (b)/(c) the
  two fallback sites, described behaviorally, no file/line/function reference; (d) both resolving to
  `GROUNDING_UNAVAILABLE`, carrying Ruling 002 §5.2/§5.3 and I5/I7's existing terminal/surfacing
  behavior; (e) no new generic/universal fallback, with Ruling 002 §5.4 stated as a separate matter, not
  characterized as an instance of that category; (f) the (b)/(c) causal distinction required in
  authoritative, machine-readable state, defined functionally, no schema/enum/field/storage mechanism
  prescribed; (g) Ruling 002 §5.4 preserved by citation only, no domain name inlined, scoped to §5.4's
  own predicates, not broadened or extended by analogy. Confirmed: I8 is both necessary and sufficient
  for GAP-4's closure condition (`open_contract_gaps.md:183-186`), carried as one invariant per
  `open_contract_gaps.md:717-719`'s explicit requirement; every one of Disposition 002 §§2.1–2.5's
  determinations is represented; no implementation mechanism is chosen anywhere in I8; I8 passes Contract
  002 V1's own conformance check (no domain named anywhere in (a)–(g), confirmed by full-document scan
  after the I8(g) fix). This approval and signature do not themselves close GAP-4, mark this document
  SIGNED or LOCKED, or authorize implementation of any kind. **Not attested by this signature:** the
  exclusions list (§5's row) or the future-governance clause (§6's row).
- [x] §5 Exclusions — signed 2026-09-15. Verified: each of the nine excluded topics routes to its
  actual existing authority — domain names/count to Contract 001 §1; provider choice/prompts/model
  usage/caching to Ruling 001 §5, GAP-6, GAP-7; registry expansion rules to Ruling 002 §3, §8;
  implementation mechanism/schema/enum/field/API/storage to "not decided by this document" (narrowed
  from an earlier overclaim); GAP-5 to its own, not-yet-operative routing; Ruling 002 §10.3/Seam 3 to
  CR-007's non-blocking determination; Ruling 002 §10.5/§10.7 to the future dedicated ruling-level
  instrument named in Disposition 001; Fusion Engine C1–C6 to FE Requirements v0.1/ADR-001; any code,
  registry, or other governance-document edit to no authorization granted here. The self-test — that
  none of these topics appears elsewhere in this document as a live normative condition — passes,
  confirmed by this session's repeated audits: no domain taxonomy content, no code/registry edits, no
  implementation mechanism chosen, no GAP-5 content, nothing touching Seam 3/§10.3/§10.5/§10.7 anywhere
  in the document; Contract 001, `open_contract_gaps.md`, and every other governance file remain
  untouched. This approval does not expand Contract 002's authority into any excluded subject. **Not
  attested by this signature:** the future-governance clause (§6's row).
- [x] §6 Future governance — signed 2026-09-15. Verified: this section grants Contract 002 nothing new —
  `amendment_policy.md` §2 already binds every LOCKED document in this corpus automatically, and this row
  restates that plainly rather than leaving it to be inferred. No minor-edit, repair, emergency, or
  convenience exception is created; the text forecloses all four, matching `amendment_policy.md` §1's own
  "no bounded exception" rule. The supersession mechanism is restated correctly: addressable-division
  granularity, must resolve without inference, superseded text never touched. The one NON-BLOCKING
  finding under this row — `amendment_policy.md`'s own supersession granularity not clearly foreclosing a
  future document superseding a single lettered sub-clause of I8 in isolation — was consciously accepted
  by the operator as pre-existing governance debt outside this document's authority to fix, not a defect
  in this row's own text, and this signature does not attempt to compensate for it inside Contract 002.
  **Not attested by this signature:** nothing further — this is the final §7 row.

---

Drafted 2026-09-15. **LOCKED 2026-09-15 — attested in full, binding, and superseding Contract 001 §6 as
of this date.** Contract 001's own text is untouched and historically intact; its §6 no longer governs.
GAP-4 remains open against `open_contract_gaps.md` — this document's existence and lock do not
themselves close it; recording that closure is a separate, later act.
