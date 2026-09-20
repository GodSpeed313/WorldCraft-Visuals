# WorldCraft Operator Disposition 003 — GAP-5 `SURFACED` Payload Substantive Policy

**Type:** DISPOSITION. Not a ruling, not a contract, not a gap, not a
correction, not an authorization, not a proposal, and not the successor contract. Closes no
register entry; authorizes no edit to any code or document; determines no successor-contract name,
number, structure, or wording. Follows the form and limits established by
`disposition_001_ruling_002_10_5_sequencing.md` and `disposition_002_gap4_grounding_terminal_policy.md`,
extended here to GAP-5 on the same basis Disposition 002 extended it to GAP-4: independently
answerable substantive content, without waiting on an implemented domain/fusion layer.

**What this file is.** A record of the operator's substantive determination of what the eventual
GAP-5 invariant must require of a `SURFACED` result's *payload* — as distinct from the *routing*
question (which document/division the invariant must live in), already settled operatively by the
2026-09-17 restatement in `open_contract_gaps.md`. This draft supplies the second, separate thing
that restatement explicitly left undecided: reason cardinality, and whether I8(f)'s causal
distinction must appear in the outward payload.

---

## 0. Baseline this draft was prepared against

Verified by fresh fetch immediately before drafting:

- `origin/main` = `7973643` (`79736431bdff36e6e0fbece60674a11fd3445f24`), local `main` identical,
  zero ahead/behind.
- GAP-5 routing made operative by `8de5b5f` (2026-09-17); recorded in `open_contract_gaps.md:846-916`.
- CR-008 citation corrections recorded by `7973643`; recorded in `docs/corrections.md`.
- GAP-5's status: **OPEN** (`open_contract_gaps.md:848`, `:914-916` — routing is operative,
  closure is not).
- Untracked `scratch_ruling002_10.5_worksheet.md` present, unread for substance and untouched by
  this draft.
- No commit, push, sign, acknowledgment, lock, `open_contract_gaps.md` edit, successor-contract
  draft, or implementation authorization has been made in preparing this file.

## 1. Scope

**Closes:** nothing in the gap register. **Determines:** the substantive payload semantics the
future GAP-5 invariant must carry for a `SURFACED` result, given the routing already made operative
on 2026-09-17 (the invariant must live in a division superseding "Contract 002 §§3–4, carrying
I1–I8" — `open_contract_gaps.md:882-896`).

**Does not determine:** enum names, schema, field names, JSON/API shape, serialization, storage
format, database representation, or any other implementation mechanism; whether a third causal
category beyond I8(b)/(c) must ever be distinguished; which Contract 002 division a successor
contract would supersede beyond what the 2026-09-17 routing already names; or anything concerning
GAP-4, GAP-6, GAP-7, GAP-8, GAP-9, or Ruling 002 §10.5/§10.7.

**This determination begins only after a fusion-level result has already been determined.** It
takes as given that some existing or future mechanism has already classified the fusion as one of
`ADMITTED`, `SURFACED`, `CAUTIONARY`, or `BLOCKED` (Contract 001 §5.1), and speaks only to what a
`SURFACED` result's payload must then preserve. It creates no rule, and no partial or implicit rule,
for *deriving* any of those four fusion-result classifications from a set of mixed per-component
terminal states — that derivation question is Ruling 002 §10.3 / Seam 3 (dispositional synthesis),
ruled non-blocking and separate by CR-007, and untouched by Contract 002 §5's exclusion table. This
determination would apply identically, and unchanged, under any future resolution of §10.3.

## 2. Determination

### 2.1 — Accepted components must be preserved

Every `SURFACED` result must preserve the components that resolved successfully through domain,
family, and grounding resolution (Contract 001 §5, I2).

**Basis.** Ruling 002 §5.3: fusion output must preserve "accepted powers ... unresolved powers ...
the reason for exclusion." Contract 001 §5.1: `GROUNDING_UNAVAILABLE` maps to `SURFACED` —
"accepted and rejected components both reported, with reason." Contract 001 §5.1 remains directly
governing text — Contract 002 supersedes only Contract 001 §6 (`contract_002_domain_resolution_invariants.md:3-5, 85`);
§5, carrying this table, is expressly listed as continuing to bind "exactly as signed"
(`contract_002_domain_resolution_invariants.md:88`). `open_contract_gaps.md:199-206` records that no
existing invariant currently requires this preservation — I5 carries the reason, I7 carries
terminality, neither carries the payload.

### 2.2 — Unresolved/rejected components must be preserved

Every `SURFACED` result must preserve the components that did not resolve or were rejected. Ruling
002 §5.3 describes these as "unresolved powers"; Contract 001 §5.1 describes the same `SURFACED`
payload obligation using "rejected components"; and GAP-5's operative closure condition deliberately
preserves both formulations — "did not resolve or were rejected" (`open_contract_gaps.md:887`). For
this disposition's GAP-5 payload purpose, those formulations are treated together wherever they
refer to a component whose grounding path legitimately terminates in `GROUNDING_UNAVAILABLE`. This
does not declare the terms globally synonymous outside that governed context.

**Scope note, made explicit to avoid narrowing or broadening Ruling 002.** "Unresolved/rejected"
here means, specifically, a component that individually reached `GROUNDING_UNAVAILABLE` after its
own domain and family resolution legitimately succeeded (I8(b)/(c); Ruling 002 §5.2, §5.3). It does
not reach a component that individually halted earlier, at `UNRESOLVED_DOMAIN`, `AMBIGUOUS_DOMAIN`,
or `UNRESOLVED_FAMILY` — those map to `CAUTIONARY`, not `SURFACED` (Contract 001 §5.1), and I2
requires those terminal conditions to halt before grounding is ever reached (I8(a)). This
determination does not decide, and does not need to decide, how a fusion's overall result is
classified when its components' individual terminal states differ across stages — see §1's scope
exclusion of Ruling 002 §10.3.

**Basis.** Same citations as 2.1.

### 2.3 — Per-component reason attribution required

The governed reason for each unresolved/rejected component must remain attributable to that
specific component. A `SURFACED` result may not carry an unattributed pool of reasons alongside an
unattributed set of rejected components such that which reason governs which component cannot be
determined.

**Basis.** Contract 001 I5: "No silent terminal. Every terminal state carries its reason to the
output." A reason that cannot be traced to the component it governs is functionally silent as to
that component, reproducing the defect I5 exists to prevent, one level down from the terminal to
the payload.

### 2.4 — Reason cardinality: shared representation permitted only under exact causal identity

A single reason representation may cover more than one unresolved/rejected component **only** when
those components are governed by the same causally identical failure. Per-component attribution
(2.3) is not satisfied by mere adjacency or by both components sharing a category of failure in the
abstract — the failure must be the identical governed cause, not merely of the same kind.

**Identical labels are not sufficient.** Two components carrying the same reason *label* or *text*
are not thereby shown to share a reason representation legitimately under this section — the label
is evidence of nothing on its own. What must actually be identical is the governed underlying
cause itself. A representation that assigns matching labels to components governed by different
causes does not satisfy this section merely because the labels match; it violates it.

Sharing a reason representation must not erase the ability to determine which reason applies to
which component. Concretely: **for every affected component, an authorized consumer must be able
to determine which governed cause applies specifically to that component** — not merely that one of
several possible causes occurred somewhere within the rejected set. Aggregate knowledge of that
weaker form (*"one of causes A or B occurred among these components"*, without resolving which
component had which) does not satisfy per-component attribution and does not satisfy this section,
regardless of how the representation is shaped. A shared representation must still resolve, for
every component it covers, to one determinate governed cause, recoverable per component.

**Basis and adversarial check.** No governing text was found requiring one reason instance per
component, nor forbidding a shared representation. Ruling 002 §5.3's own illustrative example
supports the shared case directly: "rejected components : Y — no valid grounding domain" attaches
one reason line to a *set* Y, not one reason per member of Y (`ruling_002_family_taxonomy_integrity.md:298-301`).
That example does not by itself establish the *exact-causal-identity* limit stated above — the
example does not test a case where Y's members fail for different reasons — so that limit is this
disposition's own determination, not a reading already compelled by §5.3, made to keep 2.3's
attribution requirement from being satisfied in name only by a representation broad enough to
paper over distinct causes.

### 2.5 — Partial-success preservation

The failure, rejection, or unresolved status of one component must not cause an independently
accepted/resolved component to be discarded merely because the fusion's aggregate result is
`SURFACED`. This is a preservation rule applied *given* a `SURFACED` classification already exists
for the fusion; it does not itself supply, or depend on, the mechanism by which that classification
is reached when components carry mixed terminal states (reserved to Ruling 002 §10.3, per §1).

**Basis.** Ruling 002 §5.3's rejected alternative, "a hard fusion failure discards the work that did
resolve" — the exact defect this rule exists to prevent from re-entering through the payload layer
even once terminal-state enforcement (I8(a)) and payload-attribution (2.1–2.4) both hold.

**This is a preservation rule only. It is not a validity rule, and it does not gate what counts as
"accepted," "independently resolved," or legitimately unresolved/rejected in the first place.**
Two distinct upstream gates are in play, and this rule creates neither:

- **"Accepted" / "independently resolved"** means, and can only mean, a component that has
  *already, independently, and prior to this determination's application*, satisfied every
  applicable upstream validity requirement — including, without limitation, I3 (ambiguity
  preserved, never collapsed — a component with multiple live domain candidates is not "accepted,"
  it is `AMBIGUOUS_DOMAIN`, and stays there until evidence discharges it; selecting arbitrarily
  among candidates to manufacture an "accepted" component is exactly what I3 prohibits), I4 (no
  cross-domain substitution — a component may not be counted as "accepted" on the strength of a
  grounding candidate manufactured from outside its own domain merely to give the preservation rule
  something to preserve), and I6 (unknown is not false, uncertain is not resolved — a component
  whose domain, family, or grounding status is not yet established is not "accepted" merely because
  treating it as accepted would be more convenient for this rule).
- **Where a component instead terminates through grounding** rather than being accepted, its status
  as legitimately unresolved/rejected under 2.2 depends on I8 — not on I3/I4/I6, and not on the same
  footing as those three. I8 is not an "acceptance gate" alongside I3/I4/I6; it governs a different
  outcome (the component's terminal halt to `GROUNDING_UNAVAILABLE`, on the basis in I8(a)–(d), with
  the causal-preservation property in I8(f)). A component's `GROUNDING_UNAVAILABLE` termination is
  legitimate for this determination's purposes only when it is already actually governed by I8 —
  halted rather than merely stopped, on one of I8(b)/(c)'s two bases, with I8(f)'s recoverability
  property intact.

**This determination creates neither status.** It does not convert a component that has not
satisfied all applicable upstream resolution requirements, including I3/I4/I6, into an "accepted"
one, and it does not convert a component whose halt is not actually governed by I8 into a
legitimately unresolved/rejected one. It **preserves whatever independently valid status — accepted
after satisfying all applicable upstream resolution requirements, including I3/I4/I6, or
legitimately halted under I8 — the component already had before aggregation**, and does nothing
else. A reading that treats "don't discard accepted
components" as license to relax I3, I4, I6, or I8's own requirements — in either direction, to
manufacture an easier "accepted" status or to wave through a halt I8 does not actually govern — in
order to have more to preserve, or to avoid an `AMBIGUOUS_DOMAIN`/`CAUTIONARY` outcome, is a
misreading this determination forecloses expressly, not merely by omission.

**Adversarial check.** This is the risk named directly by the fourth item on the adversarial
checklist this disposition was tested against: "any way the partial-success rule could accidentally
authorize a component that should have been excluded under another invariant." No governing text
was found that this paragraph's foreclosure conflicts with; I3, I4, and I6 stand in Contract 002 §3
unweakened (`contract_002_domain_resolution_invariants.md:172-183`), and I8 stands in Contract 002
§4 unweakened (`:188-230`) — and nothing in 2.1–2.5 as originally drafted purported to touch them
or to blur the two gates together — this paragraph makes that
non-effect explicit in the text itself, rather than leaving it to be inferred correctly by every
future reader.

### 2.6 — I8(f) causal preservation, extended by pattern, not by scope

Where the governed reason for two or more unresolved/rejected components collapses onto the same
representation under 2.4, the originating causal distinction between those components' governed
causes must remain recoverable from the authoritative, machine-readable result — not merely
inferable, not merely reconstructable by an external process. This disposition does **not** require
that distinction to be duplicated into a dedicated outward payload field. It requires only that an
authorized consumer of the authoritative result be able to recover, for each affected component,
the governed cause applicable specifically to that component — consistent with 2.4's per-component
recoverability requirement, and subject to the same limit: aggregate knowledge that one of several
governed causes occurred somewhere within the affected set, without resolving which component had
which, does not satisfy this section.

**Basis and relationship to I8(f) — stated precisely to avoid conflating two different things.**
Contract 002 I8(f) governs a different distinction (whether no legitimate grounding candidate ever
existed, versus legitimate candidates existed but were all illegal — I8(b)/(c)) at a different layer
(the grounding-terminal cause itself, prior to and independent of any multi-component fusion
payload). I8(f) is cited here **as pattern, not as source of obligation**: it establishes, as
already-adopted governance, that a causal distinction collapsing onto one terminal state may be
required to remain recoverable in authoritative state without being required to appear as a
dedicated outward field — "must remain available in authoritative, machine-readable state ...
No particular representation, schema, field, or storage mechanism is prescribed"
(`contract_002_domain_resolution_invariants.md:217-222`). This determination applies that same
representation-neutral technique to GAP-5's reason-cardinality question, on its own basis (2.3,
2.4), not by extending I8(f)'s own scope. Contract 002 V2 independently confirms this technique is
already the corpus's accepted way to reconcile a same-terminal collapse with preserved causal
information (`contract_002_domain_resolution_invariants.md:120-137`), without reaching or being
reached by GAP-5 (V2's own text confirms it "governs Contract 002's own new normative additions
only — currently, I8" — `:127`).

**Adversarial check.** No text was found requiring I8(f)'s cause, or any analogous cause, to be
literally present in the outward payload rather than merely recoverable; to the contrary, the
2026-09-17 GAP-5 routing determination expressly left this question open and undecided
("whether I8(f)'s causal distinctions must appear in the outward payload or may remain in
machine-readable internal state" — `open_contract_gaps.md:905-906`). This determination resolves
that open question, for GAP-5 specifically, in the recoverable-not-duplicated direction.

### 2.7 — Representation neutrality

No field name, enum, class, JSON structure, API shape, serialization, storage format, database
representation, or implementation mechanism is chosen by this determination. No code is drafted or
authorized by it.

### 2.8 — What this determination does not do

- Does not draft, open, name, number, or structure the successor contract that will carry the
  eventual GAP-5 invariant.
- Does not decide which Contract 002 division beyond the 2026-09-17 routing's own terms a successor
  contract would supersede.
- Does not close GAP-5, and does not alter GAP-5's OPEN status.
- Does not amend, reopen, or supersede any part of Contract 001 or Contract 002. Every citation
  above is to text as currently signed/locked.
- Does not decide Ruling 002 §10.3 (how a fusion's overall result is derived from mixed per-component
  terminal states) or Ruling 002 §10.5/§10.7 (family/domain reclassification).
- Does not authorize any edit to `logic_auditor.py`, `mythos_sync.py`, any registry, or any other
  code or document.
- Does not affect GAP-4, GAP-6, GAP-7, GAP-8, or GAP-9.
- Does not relax, narrow, or create an exception to I3, I4, or I6 as applicable upstream validity
  requirements for an "accepted" or "independently resolved" component; and does not relax, narrow,
  or create an exception to I8's requirements governing a legitimate `GROUNDING_UNAVAILABLE` halt,
  including its halting basis and causal-preservation requirements. 2.5 presupposes those statuses
  were already validly established and governs only their preservation; it creates no alternate or
  lower-bar route to either accepted status or legitimately unresolved/rejected status.

## 3. Relationship to the gap register

`open_contract_gaps.md` GAP-5 remains open, and its operative routing (approved 2026-09-17,
`:846-916`) remains exactly as recorded. This disposition supplies the substantive payload content a
future invariant addressing that routing's closure condition must carry; it does not itself supply
the invariant, does not close the entry, and cites Ruling 002 and Contract 001/002 as authority, not
itself.

## 4. What this document explicitly does not do

- It does not draft final invariant language, choose enum names, or specify any schema, API, or
  implementation mechanism.
- It does not authorize any edit to any code or document.
- It does not close GAP-5, and does not alter GAP-5's OPEN status.
- It does not touch GAP-4, GAP-6, GAP-7, GAP-8, GAP-9, Ruling 002 §10.3, or Ruling 002 §10.5/§10.7.
- It does not supersede, amend, or reopen any signed section of Contract 001, Contract 002, or
  Ruling 002.
- It binds no implementation, today, to any behavior.
- It is acknowledged per §5, recorded rather than locked in the sense Ruling 002's checklist uses
  that word, per the pattern in Disposition 001 and Disposition 002. It is not itself committed or
  pushed as of this conversion.

## 5. Acknowledgment

```
Acknowledged (operator): Kevin Brown
Acknowledged at:          2026-09-19 23:28 EDT
```

Statement:

*"I determine, for GAP-5, that a `SURFACED` result must preserve the components that resolved
successfully, and must also preserve the components that legitimately terminate at the grounding
stage as unresolved or rejected under `GROUNDING_UNAVAILABLE`.

I determine that the governed reason for each such unresolved/rejected component must remain
attributable to that specific component. I determine that a single reason representation may be
shared by multiple components only where the same governed underlying cause actually applies to
each of them — identical labels or wording alone are insufficient — and that the applicable
governed cause must remain recoverable per component, not merely as aggregate knowledge that some
cause occurred somewhere within the set.

I determine that this partial-success preservation is preservation-only. It creates no
accepted/resolved status and no legitimately unresolved/rejected status. An accepted/resolved
component must already have satisfied all applicable upstream resolution requirements, including
I3, I4, and I6; a `GROUNDING_UNAVAILABLE` component must already be legitimately governed by I8.
This determination preserves whichever of those independently valid statuses a component already
had before aggregation, and does not lower any requirement for establishing either status.

I determine that where causal distinctions collapse into the same outward result or shared
representation, the applicable governed cause must remain recoverable from authoritative,
machine-readable state for each affected component. GAP-5 does not require that causal distinction
to be duplicated into a dedicated outward payload field. This determination chooses no field, enum,
schema, API shape, serialization, storage format, database representation, or implementation
mechanism.

I determine that this determination begins only after a fusion-level result has already been
determined. It creates no rule for deriving `ADMITTED`, `SURFACED`, `CAUTIONARY`, or `BLOCKED` from
mixed component states, and does not decide Ruling 002 §10.3.

This is authoritative operator input for the eventual GAP-5 governing invariant only, not that
invariant itself. GAP-5 remains OPEN. This determination does not amend Contract 001 or Contract
002, does not authorize any implementation, and does not affect GAP-4, GAP-6, GAP-7, GAP-8, GAP-9,
or Ruling 002 §10.5/§10.7."*

---

Recorded 2026-09-19, by operator instruction. Not locked, not signed in the sense Ruling 002's
checklist uses that word — acknowledged, per the pattern in `corrections.md`, `authorizations.md`,
Disposition 001, and Disposition 002.
