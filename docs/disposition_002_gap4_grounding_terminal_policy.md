# WorldCraft Operator Disposition 002 — GAP-4 Grounding-Unavailability Terminal Policy

**Type:** DISPOSITION. Not a ruling, not a contract, not a gap, not a correction, not an
authorization, not a proposal, and not the successor contract. Closes no register entry;
authorizes no edit to any code or document; determines no successor-contract name, number,
structure, or wording.

**What this file is.** A dated record of the operator's substantive determination on the two
grounding-failure conditions `open_contract_gaps.md` (`GAP-4`) tracks: (1) resolved family, no
legitimate grounding candidate, and (2) legitimate candidates that are all illegal for the
fusion's modality. It records what the eventual GAP-4 invariant must require, without drafting
that invariant, without opening the instrument that will carry it, and without touching any
locked text.

**Precedent and its limit.** This disposition follows the form Disposition 001 established —
dated, acknowledged rather than signed, preserving an operator determination without amending
locked text — extended here to carry substantive content rather than sequencing only. Disposition
001 itself declined that extension for Ruling 002 §10.5's classification question because a
precondition (a domain-taxonomy architecture) did not yet exist to make that question ripe. No
equivalent precondition blocks GAP-4's determinations below; they were independently validated as
answerable without an implemented domain layer. This disposition is not, by its existence,
authority for any other document to record substantive content this way — that remains an
extension made deliberately, for this case, on these facts.

**What this file is not.**

- Not a Ruling. It creates no invariant, states no new taxonomic truth, and undergoes none of
  the section-by-section evidentiary sign-off Rulings 001 and 002 carry.
- Not a Contract. It defines no state, transition, or terminal outcome; Contract 001 alone does
  that, and remains untouched.
- Not a gap-register entry. `open_contract_gaps.md` tracks where GAP-4 closes; this file records
  what the closing rule must require. The two questions are distinct, and this file answers only
  the second.
- Not a Correction. No defect is recorded in any signed text.
- Not an Authorization. No edit to any code or document is granted here.
- Not the successor contract. It does not open, name, number, structure, or draft that
  instrument, and creates no obligation that it be opened on any particular schedule.
- Does not amend Contract 001. Every cited invariant, state, and terminal mapping stands exactly
  as signed.
- Does not amend Ruling 002. Every cited section, including §5.4, stands exactly as signed.
- Does not authorize implementation of any kind. `logic_auditor.py` remains under the existing
  §39 UNMODIFIED hold; AUTH-003's express exclusion of GAP-4 resolution and of `logic_auditor.py`
  remains in force and unaffected.
- Does not alter GAP-4's status. GAP-4 remains **OPEN**.
- Does not touch GAP-5 or any other register entry. GAP-5's own closure condition (accepted and
  rejected components both reported, with reason) is unaffected and unaddressed here.

**Standing this instrument has, and does not have.** This is not presently governing authority —
no implementation is bound by it, and nothing described below is enforceable until a successor
contract carries it as an invariant. It is **authoritative operator input for future governing
text**: any successor-contract drafting that addresses GAP-4 must remain consistent with the
determinations below unless Kevin makes a further, explicit operator determination changing them.
Where in the successor contract such an invariant would eventually live is not decided here.

---

## 1. Scope

**Closes:** nothing in the gap register. **Determines:** the substantive content the future
GAP-4 invariant must carry, for the two grounding-failure conditions named in the gap register
as Site 1 (`logic_auditor.py:136`) and Site 2 (`logic_auditor.py:173-174`), and the terminal
propagation and exception-scope requirements that already govern them.

**Does not determine:** enum names, schema, API shape, function signatures, or any other
implementation mechanism; whether a third causal category (a domain's own designed terminal
refusal, as distinct from incidental exhaustion) must eventually be distinguished — not required
by any governing text at this time, and not foreclosed by §2.3 below; which Contract 001 division
a successor contract would supersede to carry this; or anything concerning GAP-5, GAP-6, GAP-7,
GAP-8, GAP-9, or Ruling 002 §10.3/Seam 3.

## 2. Determination

### 2.1 — No legitimate grounding candidate (Site 1)

Where domain and family resolution have legitimately succeeded but the authorized grounding
mechanisms — a curated transposition entry or family-kin substitution, per Ruling 002 §1 — produce
no legitimate grounding candidate:

**Grounding halts.** The terminal condition is `GROUNDING_UNAVAILABLE`, and its already-governed
terminal/surfacing behavior applies (Ruling 002 §5.2, §5.3; Contract 001 §5.1, I5, I7).
WorldCraft must not continue searching, or manufacture a concrete grounding target, merely to
return something. No new generic or universal fallback mechanism is authorized.

**Basis.** Ruling 002 §5.2: *"A concept may not resolve into a grounding candidate outside its
domain. If a domain has no valid grounding member, the terminal state is: `GROUNDING_UNAVAILABLE`."*
Contract 001 §5.1 already maps this terminal to `SURFACED` — *"accepted and rejected components
both reported, with reason... none required; a valid ontology state, terminal."*

### 2.2 — Legitimate candidates, all illegal (Site 2)

Where legitimate grounding candidates exist but every one is illegal under the fusion's modality
constraints:

**Grounding halts.** The terminal condition is `GROUNDING_UNAVAILABLE`, and its already-governed
terminal/surfacing behavior applies, on the same basis as §2.1. WorldCraft must not enter an
ungoverned second-stage search, or substitute any candidate outside the source's domain, merely
to produce a concrete target. No generic second-stage fallback mechanism is authorized.

**Basis.** Same as §2.1, read to cover "no member is a *usable* grounding member" as well as "no
member exists" — both are cases in which the domain (or, in the current single-layer
architecture, the family) supplies nothing grounding may honestly return. Contract 001 I4
(*"No cross-domain substitution... Ruling 002 §5.2"*) independently forbids any candidate this
determination might otherwise reach for from outside the source's domain.

### 2.3 — Causal distinction preserved

Although §2.1 and §2.2 share the same terminal outcome, the eventual governing text must require
that enough machine-readable causal information be preserved to distinguish:

1. no legitimate grounding candidate existed; from
2. legitimate grounding candidates existed, but all were illegal for the fusion.

**Basis.** Contract 001 I5: *"No silent terminal. Every terminal state carries its reason to the
output."* Contract 001 §5.1 already performs the identical move for a different collapsed
terminal — *"the fusion result states are lossy. Three distinct terminal conditions map onto
`CAUTIONARY`, and each calls for a different operator action. The reason must therefore travel
with the result and may never be discarded."* §2.1 and §2.2 collapsing to one terminal outcome
without preserving which of the two occurred would reproduce, at the grounding layer, the exact
loss of information I5 and §5.1 exist to prevent one layer up.

**What this does not require.** No enum name, schema, field, or storage mechanism is chosen here.
No third causal category is required — Ruling 002 §5.4's own table names a domain's designed
terminal refusal as a further, conceptually distinct condition from either case above, but no
governing text currently requires it be machine-distinguishable from §2.1, and nothing here
forecloses adding that distinction later if governance comes to require it.

### 2.4 — Upstream terminal propagation

This determination is not a new substantive ruling. It records that existing governance already
requires:

- `UNRESOLVED_DOMAIN` must not proceed into family resolution or grounding.
- `UNRESOLVED_FAMILY` must not proceed into grounding.

**Basis.** Contract 001 I2: *"Resolution order is fixed. Domain → family → grounding."* Contract
001 §3.1: an `UNRESOLVED_DOMAIN` case's operator implication is *"do not ground."* Ruling 002
Addendum A, points 1 and 3: *"Family is only meaningful inside a domain"*; *"Learned concepts
require domain resolution before family grounding."* Ruling 002 §2 and §8.1 row 2: an unsanctioned
family must resolve to `UNRESOLVED_FAMILY`, never a coerced or best-guess category, and maps to
`CAUTIONARY`, not to grounding. What is missing is not this substance but its enforcement — that
a terminal condition at one stage actually, rather than merely advisably, prevents the next stage
from executing. Supplying that enforcement, in whatever instrument eventually carries it, is
directed here as a consequence of already-decided governance, not as a new choice among
alternatives.

### 2.5 — Existing narrow exceptions preserved

Nothing in §2.1 through §2.4 repeals, broadens, or generalizes Ruling 002 §5.4. Specifically:

- §5.4 remains exactly as narrow as written: fallback to `Indomitable Will` is authorized only
  for the human-excellence domain, on the basis §5.4 itself states — *"coherent, because the
  domain is itself grounded in human capability."*
- `Indomitable Will` is not converted into a universal or generic fallback by §2.1 or §2.2's
  prohibition on new generic fallbacks; §5.4 is an existing, already-governed exception, not a
  new one, and is unaffected by that prohibition.
- No equivalent fallback is created, by analogy or otherwise, for any other domain. §5.4's own
  reasoning is scoped to the one domain named; Ruling 002's terminal-policy table (§5.4) names a
  second domain — *"supernatural phenomenon"* — whose policy is refusal, not fallback, and that
  policy is likewise unaffected.
- §5.4 may operate only when its governing predicate — that the concept resolves within the
  human-excellence domain — can actually be established. The absence of an implemented domain
  signal does not authorize treating that predicate as satisfied. Until a domain-resolution
  capability exists to prove it, §5.4 remains a correctly dormant, not a repealed or unavailable,
  exception.

## 3. Relationship to the gap register

`open_contract_gaps.md` GAP-4 remains open, and its operative closure condition — approved as the
successor-contract routing target on 2026-09-15 — remains exactly as recorded. This disposition
supplies the substantive content a future invariant addressing that condition must carry; it does
not itself supply the invariant, does not close the entry, and is not cited by this disposition
as authority for §2's determinations — the authority is Ruling 002 and Contract 001, cited above.

## 4. What this document explicitly does not do

- It does not draft, open, name, number, or structure the successor contract.
- It does not draft final invariant language, choose enum names, or specify any schema, API, or
  implementation mechanism.
- It does not authorize any edit to `logic_auditor.py` or any other code or document. The §39
  UNMODIFIED hold on `logic_auditor.py`, and AUTH-003's express exclusion of GAP-4 resolution,
  remain in force exactly as recorded.
- It does not close GAP-4, and does not alter GAP-4's OPEN status.
- It does not touch GAP-5, GAP-6, GAP-7, GAP-8, GAP-9, or Ruling 002 §10.3/Seam 3.
- It does not supersede, amend, or reopen any signed section of Contract 001 or Ruling 002.
- It does not decide which Contract 001 division a future successor contract would supersede to
  carry this determination.
- It binds no implementation, today, to any behavior — no implementation is authorized to exist
  yet for this behavior to bind.

## 5. Acknowledgment

```
Acknowledged (operator): Kevin Brown
Acknowledged at:          2026-09-15 01:22 EDT
```

Statement: *"I determine, for GAP-4, that grounding halts to `GROUNDING_UNAVAILABLE` — with its
already-governed terminal/surfacing behavior — both when no legitimate grounding candidate exists
and when legitimate candidates exist but are all illegal for the fusion, and that no new generic
or universal fallback is authorized in either case. I determine that the two conditions must
remain machine-distinguishable in whatever eventually implements this, without deciding the
schema or mechanism now. I determine that this is enforcement of already-governed terminal
propagation, not new policy, for `UNRESOLVED_DOMAIN` and `UNRESOLVED_FAMILY`. I determine that
Ruling 002 §5.4 remains exactly as narrow as written, is not broadened or made universal by
anything above, and may operate only once its domain predicate is actually provable.

This is authoritative operator input for the eventual GAP-4 governing text, not that text itself.
GAP-4 remains OPEN. The successor contract remains unopened, unnamed, and unstructured by this
determination. No implementation is authorized; `logic_auditor.py` remains under its existing
hold. GAP-5 and every other register entry are untouched."*

---

Recorded 2026-09-15, by operator instruction. Not locked, not signed in the sense Ruling 002's
checklist uses that word — acknowledged, per the pattern in `corrections.md`, `authorizations.md`,
and Disposition 001.
