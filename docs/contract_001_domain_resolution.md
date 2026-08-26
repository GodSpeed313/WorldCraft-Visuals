# WorldCraft Contract 001 — Domain Resolution

**Type:** Resolution contract. Defines states, transitions, terminal outcomes, and invariants.
**It is not an ontology document and not an implementation plan.**

**Status:** DRAFT — pending operator review and sign-off.

**Why it exists.** Rulings 001 and 002 introduced four separate state vocabularies across two
documents written in response to different questions — proposal outcomes, family outcomes, grounding
outcomes, and fusion result states. Ruling 002 §8.1 already needed a three-column table to reconcile
them. This contract consolidates what has been decided into one coherent state model, **before**
implementation, so that code does not become the place the remaining ontology decisions get made by
accident.

**Sequencing intent.** The contract is deliberately written while the taxonomy is unfinished. If it
can only be completed after the domains are named, it has failed its own purpose.

---

## 1. Scope boundary

**This contract defines only:**

- resolution states
- allowed transitions
- terminal outcomes
- invariants

**It does not define:**

| Excluded | Belongs to |
|---|---|
| domain names | lore — operator |
| domain count | lore — operator, informed by `audit_001` |
| provider choice | Ruling 001 §5 |
| prompts | unassigned — see GAP-7 |
| model usage | coupled to GAP-6 — no independent owner; resolves only if the document that claims caching/storage ownership also addresses model usage, not on GAP-6's closure alone |
| caching, storage strategy | unassigned — tracked as GAP-6 |
| registry expansion rules | Ruling 002 §3, §8 |

Anything from the left-hand column — a topic this contract has excluded — appearing as a normative
condition anywhere in this contract is a defect in this contract.

## 2. Contract validity constraints

**These are not features of the contract. They are conditions the contract must satisfy to be
valid.** The distinction matters: treated as features they become negotiable, and this document
becomes the place hidden assumptions creep back in.

**Scope.** V1 and V2 are conditions on the whole of this contract, §1 through §8. A signature on
either constraint attests that the document satisfies that condition as of that signature.

**Scoped term.** In this contract, *domain candidate* means a domain that is a defensible placement
for the concept currently being resolved. It is distinct from *candidate domain* as used in
`audit_001` Part 3 Q4 and Ruling 002 §10.1 — a cluster proposed for adoption into the taxonomy — and
from *grounding candidate* (§5, I4), a substitution target for a power. This contract uses the term
in the first sense only. Defensibility is evidence-relative: a placement stops qualifying as a domain candidate once current evidence justifies selecting a competing placement over it. A domain candidate need not be a registered domain.

### V1 — Cardinality independence

> **A valid domain resolution contract must produce identical state semantics regardless of the
> number of registered domains.**

The contract must behave identically at:

```
domain count: 1        domain count: 5        domain count: 20
```

At every count it must still distinguish:

- a domain candidate exists
- multiple domain candidates exist
- no domain candidate exists

**Invalid, and the canonical example of the failure:**

```
if supernatural domain exists:
    ...
else:
    ...
```

That is no longer resolution logic. **That is taxonomy.**

**Conformance check.** Substitute the domain set with any other domain set, of any size, including a
set of one. If any state definition, transition, or terminal condition changes, V1 is violated. No
state, transition, or terminal condition in this contract may contain a predicate that names a
specific domain.

**The contract must be able to run before the ontology is finalized.**

### V2 — Epistemic distinction preservation

The contract must at all times distinguish three knowledge conditions, and must never allow one to
be reported as another:

| The system must be able to say | State |
|---|---|
| *"I don't know what this is."* | `UNRESOLVED_DOMAIN` |
| *"I know what this could be, but not which interpretation wins."* | `AMBIGUOUS_DOMAIN` |
| *"I have enough evidence to continue."* | `RESOLVED_DOMAIN` |

**Those are three different realities.** Collapsing any pair destroys the operator's ability to know
what action is required. No case may be reported as one of these three unless it satisfies that
condition's stated definition. Where no condition's definition is satisfied, the case may not be
assigned to any of the three.

## 3. Domain resolution states

### 3.1 `UNRESOLVED_DOMAIN`

**Meaning:** the system cannot currently establish a domain candidate.

```
Unknown ability
      ↓
No matching domain evidence
      ↓
UNRESOLVED_DOMAIN
```

**Operator implication:** gather more evidence · enrich vocabulary · **do not ground**.

### 3.2 `AMBIGUOUS_DOMAIN`

**Meaning:** multiple domain candidates are defensible, and current evidence does not justify
selecting one.

```
Cursed Energy
      ↓
Domain candidate A
Domain candidate B
      ↓
AMBIGUOUS_DOMAIN
```

**Operator implication:** preserve alternatives · **do not collapse identity** · await additional
criteria.

**Ambiguity is not failure. It is a valid epistemic state.** A concept in this state is fully
understood; what is undetermined is which of several legitimate placements is correct. Forcing the
choice would be an unsupported assertion, not a resolution.

The contract does not decide *how* ambiguity is later discharged. A future ruling may introduce a
second criterion beyond thematic similarity — fusion locality, i.e. *which placement minimizes
cross-domain leakage* — but that requires more registry evidence and is out of scope here.

### 3.3 `RESOLVED_DOMAIN`

**Meaning:** exactly one domain candidate is defensible.

**This is the only state that proceeds into family resolution.**

## 4. Transition graph

```
                 ┌─────────────────┐
                 │  Input Concept  │
                 └────────┬────────┘
                          │
                          v
                 ┌─────────────────┐
                 │  Domain Resolve │
                 └────────┬────────┘
                          │
          ┌───────────────┼────────────────┐
          v               v                v
 UNRESOLVED_DOMAIN  AMBIGUOUS_DOMAIN  RESOLVED_DOMAIN
          │               │                │
          │               │                v
          │               │       Family Resolution
          │               │                │
          │               │                v
          │               │      Grounding Resolution
          │               │
          └───────────────┴──────────────>
             terminal / evidence required
```

**Two branches terminate without proceeding.** Neither is an error path; both are states that
require evidence the system does not have. Only `RESOLVED_DOMAIN` continues, per Ruling 002
Addendum A: *family is only meaningful inside a domain.*

## 5. Downstream states — consolidated

The stages below are already ruled; they are collected here so the full pipeline exists in one place.

| Stage | States | Source |
|---|---|---|
| Domain resolution | `UNRESOLVED_DOMAIN` · `AMBIGUOUS_DOMAIN` · `RESOLVED_DOMAIN` | this contract §3 |
| Family resolution | `UNRESOLVED_FAMILY` · resolved | Ruling 002 §2, §8 |
| Grounding resolution | grounded candidate · `GROUNDING_UNAVAILABLE` · grounding not required | Ruling 002 §5.2, §5.3 |
| Fusion result | `ADMITTED` · `SURFACED` · `CAUTIONARY` · `BLOCKED` | Ruling 001 §4 |

### 5.1 Terminal mapping

| Terminal condition | Fusion result | Operator action |
|---|---|---|
| Concept could not be identified at all | `BLOCKED` | resolve the name |
| `UNRESOLVED_DOMAIN` | `CAUTIONARY` | gather evidence / enrich vocabulary |
| `AMBIGUOUS_DOMAIN` | `CAUTIONARY` | preserve alternatives, await criteria |
| `UNRESOLVED_FAMILY` | `CAUTIONARY` | extend the taxonomy |
| `GROUNDING_UNAVAILABLE` | `SURFACED` — accepted and rejected components both reported, with reason | none required; a valid ontology state, terminal |
| All stages resolved | `ADMITTED` | none |

**Critical property: the fusion result states are lossy.** Three distinct terminal conditions map onto
`CAUTIONARY`, and each calls for a *different* operator action. **The reason must therefore travel
with the result and may never be discarded on the way out** — this is Ruling 002 §5.3 applied to the
whole pipeline rather than to grounding alone. A `CAUTIONARY` without its reason is indistinguishable
from the silent-default failure both rulings exist to eliminate.

## 6. Invariants

**I1 — Cardinality independence.** §V1. No predicate may name a specific domain.

**I2 — Resolution order is fixed.** Domain → family → grounding. Ruling 002 Addendum A.

**I3 — Ambiguity is preserved, never collapsed.** A concept with multiple domain candidates stays
in `AMBIGUOUS_DOMAIN` until evidence discharges it. Selecting arbitrarily is prohibited.

**I4 — No cross-domain substitution.** No transition may produce a grounding candidate outside the
concept's domain. Ruling 002 §5.2.

**I5 — No silent terminal.** Every terminal state carries its reason to the output. Ruling 001
Invariant 1, Ruling 002 §5.3.

**I6 — Unknown is not false. Uncertain is not resolved.** The two principles that have emerged across
001, 002 and this contract, stated as one invariant because they fail together: both are violated by
the same move — treating an absence of evidence as a determination.

**I7 — `SURFACED` is terminal.** A `SURFACED` result is not a degraded `ADMITTED` result and may not
be auto-resolved through taxonomy expansion. Ruling 001 §4, Ruling 002 §5.2, §5.4.

## 7. The conservative principle at three levels

This contract is the third application of one idea, and recording the pattern is worth more than any
single rule:

| Level | Ruling | The rule | What is preserved |
|---|---|---|---|
| Concept identity | 001 §1 | minting is cheap, merging is expensive | distinctions between concepts |
| Category integrity | 002 §3 | family threshold higher than power threshold | the integrity of what members inherit from a family |
| Epistemic state | this contract, I3 | ambiguity is preserved, never collapsed; selecting arbitrarily is prohibited | the honest description of what is known |

Each of the three rules accepts a less resolved result rather than a wrongly resolved one: a duplicate left unmerged, a family left unadmitted, a domain left unselected.

## 8. Future extensibility

> **This contract must permit additional resolution states without invalidating existing states,
> provided new states preserve the distinction between unknown, ambiguous, and resolved knowledge
> conditions.**

Not because further states are expected immediately, but because **the entire purpose of this layer
is preventing forced classification.** A contract that could not itself be extended without a
rewrite would reproduce, at the level of the state machine, exactly the closed-world assumption
Ruling 002 §1.1 identifies as the thing WorldCraft is leaving behind.

### What kind of requirement this is

**This is not a feature of the contract, and it is not one of §2's validity constraints. It is
a condition on an act — extending this contract — and it is named here as such: an amendment
condition.** The distinction matters. V1 and V2 are conditions this document satisfies, or fails,
as it stands on a given date, and `:50` scopes them on exactly that footing. Read the same way,
the requirement at `:252-254` is satisfied by any contract nobody has yet tried to extend —
which is the one circumstance in which it does no work.

**It is not a third validity constraint.** `:50` names V1 and V2. A V3 that `:50` did not reach
would leave this requirement governed by no scope clause — the condition this text exists to
end — under a name suggesting otherwise.

**It is not an invariant.** §6's seven are numbered members of one set, each stating what
must hold of resolution: of its predicates, its order, its transitions, its terminals. This
requirement states what must hold of an edit to this document. An eighth number would place
the clause without saying what it is.

**Nothing is numbered here, and no set is created.** This contract states exactly one amendment
condition. If a second is ever written, what the two share can be decided then, on the two.

**Scope.** This condition binds any amendment to this contract that adds a resolution state,
wherever in the document that amendment's text lands. It does not bind the present text, which
no amendment has extended. A signature on §8 attests that the requirement is classified and
scoped as stated here, and that no amendment made before that signature violated it. **It does
not attest that a future amendment will comply.** That is attested by the amending signature,
on the date of the amendment, under this condition.

**The proviso is V2, carried forward.** *knowledge conditions* at `:253` is V2's term, used
at `:96` in V2's sense; the proviso requires of an amended contract what V2 requires of this
one. The citation is placed here rather than in the clause, and the clause is unchanged.

**Conformance check.** Compare the contract as amended against the contract as it stood immediately
before the amendment. The first limb — *without invalidating existing states* — is violated
if a state defined before the amendment is, after it, removed, contradicted by the amended text,
or left with a definition no case can satisfy. The second limb is violated whenever the amended
contract violates V2, and is tested by V2's own checks (`:99-103`, `:106-108`); a new state
that takes cases from `AMBIGUOUS_DOMAIN` and reports them as resolved violates both.

**One reading is not tested, and that is recorded here rather than left to be discovered.**
Whether an existing state is invalidated by losing cases to a new state — as against being
removed, contradicted or made unsatisfiable — is settled nowhere in this corpus, and the
check above is stated on the narrower reading only. Deciding the wider one would fix what
a future amendment may take from an existing state: a rule about amendment mechanics that
`:252-254` does not state, and that classifying `:252-254` does not require. Ruling 001 §7.4
(`ruling_001_canonicalization_policy.md:358-364`) is the form followed — the absence named,
the reason given, and the prerequisite stated: the wider reading becomes testable when a ruling
or an amendment defines what invalidating an existing state means.

---

## Sign-off checklist

- [x] §1 Scope boundary — states/transitions/terminals/invariants only — signed 2026-08-16, after the bundled provider row was split three ways (`2dac6ff`). Every destination in the exclusion table was verified to own what it is sent, or to name a register entry recording that no document does: `audit_001` Part 3 Q4 (`:181`) informs domain count and deliberately refuses a number; Ruling 001 §5 owns *provider choice* under its 2026-08-06 scope amendment (`:273`); Ruling 002 §3 and §8 own *registry expansion rules* substantively — §3 the family admission threshold, §8 the registry entry condition. *prompts* routes to GAP-7 and *caching, storage strategy* to GAP-6, each recording that no document claims the topic; *model usage* is coupled to GAP-6 without merging into it, carrying the register's stricter semantics — closure on caching/storage alone does not resolve it. The self-test sentence was corrected to name the **left-hand** column, an excluded topic appearing as a **normative** condition, so that observational citation is not caught; the corrected test was then run against this document and returns nothing. **Not attested by this signature:** whether §1's "defines only" list reaches §8, which states a normative requirement on the contract without the reconciling clause §2 carries for itself — that belongs to §8's signature; §7's observational citation of Ruling 002 §3 is recorded on §7's own line and not adjudicated here. Correcting §1's self-test removed the stated authority GAP-6's derivation rested on; that derivation is preserved and marked historical in the register rather than restated as current. No gap is closed and no invariant is added.
- [x] §2 V1 cardinality independence, with conformance check — signed 2026-08-19. The conformance check at `:87-90` was run against the whole document by extraction rather than spot-check: every domain name appearing in the registry (`audit_001`) was searched against this file, and the only occurrence in any position is `:79`, inside the fence opened at `:76` as the labeled *"Invalid, and the canonical example of the failure"* — a counter-example, not a live predicate. No state definition, transition, or terminal condition contains a predicate naming a specific domain. The substitution test holds at any domain count, including a set of one, because §3's state definitions reference *domain candidate* in `:57`'s scoped sense, whose closing clause decouples candidacy from registration; `474f16e` normalized `:114`, `:128`, `:153` and I3 `:221` onto that one term, so the test now runs against a single term rather than four. Recorded as passing rather than omitted: `:132`'s *Cursed Energy* is a concept name inside §3.2's illustrative diagram, not a domain name, and V1's rule reaches predicates that name a specific **domain**; that diagram's outputs are lettered `Domain candidate A`/`B` precisely so no domain is named. **Not attested by this signature:** `:114`'s undefined *valid*, placed on the record by `474f16e` and routed to §3's signature; and the I1/`:217` attestation-boundary question, which is outside the corpus by its own terms. No gap is closed and no invariant is added.
- [x] §2 V2 epistemic distinction preservation — signed 2026-08-19, as to mutual exclusivity and non-misreporting only. §3.1-3.3's three states are mutually exclusive on their stated definitions: `:114` is the zero case, its diagram at `:118` reading *No matching domain evidence*; `:128` requires *multiple*; `:153` requires *one* with *sufficient support*. `:106-108` forbids reporting a case as one of the three unless it satisfies that condition's stated definition, which is what V2's *never allow one to be reported as another* requires. §5.1's mapping of both `UNRESOLVED_DOMAIN` and `AMBIGUOUS_DOMAIN` onto a single `CAUTIONARY` does not violate V2: that collapse is at the fusion-result layer, not the knowledge-condition layer, and `:210-211` together with I5 (`:227`) hold the originating reason to the output, so no condition is reported as another. **Not attested by this signature — exhaustiveness.** A single domain candidate with insufficient support satisfies none of the three definitions: not zero, not multiple, not sufficient. `:106-108` leaves such a case unassigned and names no fourth state; it forbids papering the case over without giving it a destination. Whether that is a live gap or no gap at all depends on the reading of `:114`'s *valid* — if *valid* means *has sufficient support*, §3.1 absorbs the case and the set is exhaustive; if it means *well-formed*, the case has no home. That word is excluded from this signature and routed to §3's, and the exhaustiveness question is routed with it. *sufficient support* occurs once in this document (`:153`) and is not defined. **Also not attested:** the I1/`:217` attestation-boundary question, outside the corpus by its own terms. No gap is closed and no invariant is added.
- [x] §3 Three domain states, with operator implications — signed 2026-08-19. Verified as a clean partition on domain-candidate count: `:114` (0 candidates), `:153` (exactly 1), `:128-129` (≥2), following the amendment making defensibility evidence-relative at `:57`. Checked `:128-129`'s second conjunct — "current evidence does not justify selecting one" — against the case of two defensible candidates where evidence now justifies selecting one: per `:57`'s amended text, using the identical *justifies selecting* test, the disfavored candidate stops qualifying as a domain candidate at the same moment, so `:128-129`'s first conjunct ("multiple ... are defensible") fails together with its second, and the count drops to one, which `:153` catches. Both conjuncts fail together rather than the second failing independently, so the second conjunct is provably explanatory, not an independent condition, and no case falls outside all three states — this discharges the exhaustiveness question `:267` routed here, alongside the `:114` wording question routed by both `:266` and `:267`. Operator implications: `:124` and `:140-141` are explicit; `:155` ("the only state that proceeds into family resolution") is signed as functionally serving that role for §3.3, corroborated by `:207`'s mapping of "All stages resolved" to `ADMITTED` with operator action "none" — consistent with §3.3 reading as pipeline flow rather than an instruction — though it carries no matching `**Operator implication:**` label, which exists only at `:124` and `:140`; recorded as a structural asymmetry, not a defect requiring text change. `:132`'s `Cursed Energy` example was already checked under `:266`'s V1 attestation and isn't re-litigated here. `:143-145`'s *valid* — "It is a valid epistemic state" — is confirmed still present and unchanged: `425aa09` deliberately retired *valid* only from `:114`'s criterial sense, and `:143-145`'s legitimacy sense was never in scope of that retirement. **Not attested by this signature:** `:148`'s *thematic similarity*, presupposed by `:147-149` as an established first criterion for discharging ambiguity but undefined anywhere in the corpus (`audit_001:117`'s "thematic overlap" is a different phrase and glosses nothing). This is left deliberately unrouted, not merely unowned — unlike §1's precedent, where unowned topics still received a register entry recording the absence (`prompts` → GAP-7, `caching, storage strategy` → GAP-6), no entry is created here, because doing so would assert the term needs a home in the same way those do, and that assertion is itself unadjudicated. The absence is the recorded outcome, not a placeholder awaiting one. Also not attested: whether `:266` and `:267`'s own text should be corrected to reflect that the questions they routed are now answered, left as recorded per the standing disposition that a signature is true as of its date; the "second criterion beyond thematic similarity" `:147-149` reserves for a future ruling, untouched here; and the I1/`:217` attestation-boundary question, outside the corpus by its own terms.
- [x] §4 Transition graph — two terminal branches, one continuing — signed 2026-08-20. `RESOLVED_DOMAIN` → Family Resolution → Grounding Resolution confirmed as the only continuing branch. `UNRESOLVED_DOMAIN`'s termination is fully supported by the citation at `:184-185`: Addendum A Point 1 (`ruling_002:477`, quoted verbatim) requires a domain for family to be meaningful inside one, and zero candidates means no domain exists. `AMBIGUOUS_DOMAIN`'s termination is correct on the merits but is not what Point 1 says — Point 1's condition is satisfiable by any one of several candidates, so as written the citation covers only one of the two branches it's attached to. The branch's actual support — Point 4 ("Cross-domain fallback is prohibited." `:481`) together with this contract's own I3 (`:221-222`) forbidding arbitrary selection among ambiguous candidates — is real and present in the corpus, just not cited at `:185`. No text amended. Ruling 002 Addendum A's own signature (`ruling_002:635`) declined this question outright — "outside this addendum's jurisdiction." Declining left the question unowned; this signature takes it up on its own authority, not `:635`'s, and answers only the branch-coverage question Point 1 raises. `:635`'s stated ground is that each downstream citation "cites a three-node 'domain → family → grounding' compression not stated in that form in this addendum's five-node diagram or in Point 3's learned-concept-scoped wording." That ground, as worded, does not reach §4: the three-node form appears nowhere in `:157-185` — only at I2 (`:219`), which belongs to §6's row. Not attested by this signature: whether §4's diagram — four of Addendum A's five nodes, dropping fusion compatibility — is an adequate compression, a question `:635` did not raise in that form and this signature does not decide; and whether extending the order to concepts other than learned ones is supported, Point 3 being scoped to learned concepts. Also not attested: `:635`'s own pointer to this citation (`:171`) is stale, now landing at `:184-185` — recorded, not corrected, per the standing disposition that a signature is true as of its date.
- [x] §5 Consolidated pipeline + four-state fusion result + terminal mapping; reasons are lossless — signed 2026-08-20. The stage table (`:191-196`) and its four source citations verified: Domain resolution → this contract §3; Family resolution → Ruling 002 §2, §8 (`UNRESOLVED_FAMILY` / resolved, complete for the family stage — §8.1's third proposal outcome, *unresolved*, maps to the pre-pipeline `BLOCKED` row, not to family resolution); Grounding resolution → Ruling 002 §5.2, §5.3; Fusion result → Ruling 001 §4, corroborated by §8.1's own heading, *"Mapping to Ruling 001 §4 result states"*. Recorded rather than passed over: `:194`'s *resolved* is a coined success-state name, not quoted from either cited source — §2's single use of the word (`ruling_002:78`) is the failure construction *"a concept whose family could not be resolved,"* and §8.1 names the success case *accepted*; coined in the same way `RESOLVED_DOMAIN` was, and recorded here rather than carried as verbatim. §5.1's table (`:200-207`) confirmed against those sources. The closing claim (`:209-213`) that a terminal's reason must travel with it and may never be discarded is backed by I5 and holds as written. **Not attested by this signature — two of §5.1's six rows, on different grounds.** `UNRESOLVED_FAMILY` → `CAUTIONARY` (`:205`) is a reachability gap, not a content gap: the mapping itself is fully backed by Ruling 002 §8.1 row 2. What's unenforced is whether the pipeline actually stops there. GAP-4 (`open_contract_gaps.md:130-142`) already found this: the halt is stated three times across the spec — Ruling 002 §8's admission gate, §8.1's table cell, and this contract's own `:205`, under `:200`'s **Terminal condition** header, where the halt is *"carried by the word 'terminal'"* alone — and ruled nowhere. I2 fixes resolution order; no invariant makes a terminal condition halting. I4, I5 and I7 are explicit prohibitions; this property has no equivalent. Stated, not enforced by this contract. `GROUNDING_UNAVAILABLE` → `SURFACED` — accepted and rejected components both reported, with reason (`:206`) is a payload gap, near-verbatim from Ruling 002 §8.1 row 3. GAP-5's own table gives the exact split: I5 carries the reason, I7 carries terminality, but no invariant requires the accepted set reported alongside the rejected set. Stated, not enforced by this contract. Both rows correctly transcribe what Ruling 002 requires. Neither currently reflects an invariant of this contract. §6 is where that would change, and both gap entries already state what closing them requires — GAP-4 (`:183-186`): an invariant making terminal conditions halting, plus an explicit bound or removal for each of the two fallback sites; GAP-5 (`:222-223`): an invariant requiring a `SURFACED` result to preserve the accepted components, the rejected components, and the reason for rejection — one invariant covering all three, not merely the uncarried third. §6's signature is being told in advance what to check for, not left to discover it. No text amended.
- [x] §6 Invariants I1–I7 — signed 2026-08-21 as-is, without amendment, each invariant re-pulled and verified individually against the corpus rather than against any summary of it. `I1` (`:217`) is carried directly by V1, whose conformance check (`:89-90`) states that no state, transition or terminal condition in this contract may contain a predicate naming a specific domain. `I2` (`:219`) fixes resolution order and establishes nothing beyond it; GAP-4 (`open_contract_gaps.md:138-139`) names I2 by number for precisely this reason — *"No invariant states that a terminal condition at one stage forbids the next stage from running"* — so I2 passes as written while leaving that gap untouched. `I3` (`:221-222`) is verified as **both** of its sentences: the second, *"Selecting arbitrarily is prohibited,"* is the operative prohibition and is the text signed §4 cited at `:221-222`; the invariant is not reducible to its first sentence. `I4` (`:224-225`) prohibits the outcome the unscoped fallback sites can produce, but supplies neither half of GAP-4's closure condition (`open_contract_gaps.md:183-186`): it does not make terminal conditions halting, and it places no bound on either site. A site can violate I4 with nothing stopping it from running — which is GAP-4's own complaint that the property is *"inferable"* rather than enforced. `I5` (`:227-228`) carries the terminal's reason to the output and nothing further: GAP-4 (`open_contract_gaps.md:139-140`) counts it among the explicit prohibitions that have no halting equivalent, and GAP-5's table (`open_contract_gaps.md:201`) records it as carrying one of Ruling 002 §5.3's three requirements. `I6` (`:230-232`) states the epistemic distinction directly and is verified as written. `I7` (`:234-235`) establishes `SURFACED` as terminal; GAP-5 (`open_contract_gaps.md:205-206`) records that I7 *"governs the result's standing, not its contents,"* so preservation of the accepted components alongside the rejected ones is not required by it (`open_contract_gaps.md:203`). **The two gaps remain open separately, each on its own stated condition.** GAP-4 closes only when this contract carries an invariant that (a) makes terminal conditions halting rather than advisory and (b) for **each** of the two fallback sites either authorizes it with an explicit bound or removes it (`open_contract_gaps.md:183-186`). GAP-5 closes only when this contract carries an invariant requiring a `SURFACED` result to preserve the accepted components, the rejected components, and the reason for rejection (`open_contract_gaps.md:222-223`) — one invariant preserving all three, where §6 today carries two (`open_contract_gaps.md:197`). **Signing §6 does not constitute an invariant closing GAP-4 or GAP-5; both remain open exactly as recorded, and closing either requires future text this signature does not supply.** **Amendment before signature was considered and not taken.** `:57` (`0c83577`, 2026-08-19) is the standing precedent that the route is available in this corpus when the defect is a local, definitional repair — one line, changed in place, before §3 was signed — whereas GAP-4 and GAP-5 call for substantive invariant design with implementation consequences, which is why that route was not taken here. **Not attested by this signature:** that the terminal-halt property GAP-4 identifies is enforced anywhere in the implementation. GAP-4 (`open_contract_gaps.md:127-128`) records that it is not — *"the halt is stated in the specification, is not backed by any invariant, and is not enforced anywhere in the implementation. It holds today only as a property of the authored registry."* The implementation status of I1–I7 themselves was not examined in this session; this signature neither attests nor denies it.
- [x] §7 The conservative principle at three levels — signed 2026-08-23, on the text as amended by `c0f7ec7`, which repaired at `:245`, `:246` and `:248`, under AUTH-001, the defects recorded in CR-002 (findings 1, 2 and 3) and CR-003. **Those entries are not closed by this signature, and were not closed by the amendment.** `corrections.md:9` defines a correction entry as one that closes nothing; CR-002 and CR-003 stand exactly as recorded, and their quotations of the prior wording are historical as of `c0f7ec7` — a status CR-005 records for CR-004 on the same ground. This signature attests the amended text and does not re-narrate those findings, each of which has a canonical home carrying its own verification. §1's self-test (`:41-42`) was re-run against the amended section by extraction — each of the seven excluded topics at `:33-39` searched against `:237-248` — and returns zero hits, so the jurisdiction defect CR-003 recorded at `:248` is not present in the text signed here. Recorded rather than left to be rediscovered: `:246`'s *prohibited*, which the amendment introduced, does not reopen that question — CR-003 localized the defect in the quantifier distributing a norm over an excluded row, "not in the deontic vocabulary and not in the table," and row 3's subject is this contract's own I3, which is not an excluded topic. **Not attested by this signature:** whether §7 asserts ownership of Ruling 002 §3's threshold, or restates it as a binding condition of this contract. That is the proposition `:272` carried before this row replaced it — written by `2dac6ff`, attested by no signature, and rejected as clearance by CR-003. This signature does not inherit it and deliberately does not re-establish it on its own authority; settling the ownership question is a separate act, and this row is not it. **Also not attested:** the "one idea" / "two principles" / "inversion" reconciliation across `:239`, I6 (`:230-232`) and `ruling_002_family_taxonomy_integrity.md:110-112`, parked by CR-002 as an unresolved conceptual reconciliation and untouched by the amendment; row 3's "what is preserved" cell at `:246`, which Beat 1 assessed only as to the rule cell and which AUTH-001 expressly did not authorize changing; and whether row 3 raises a jurisdiction question of its own, which CR-003 left untested and unbounded by its own terms. No gap is closed and no invariant is added.
- [ ] §8 Future extensibility clause — signed 2026-08-__, on the text as extended by `696738e`, which added 49 lines at `:260-308` under AUTH-002 (`authorizations.md:153-314`). **This signature answers the question §1 routed here.** `:314` records as not attested by §1 *"whether §1's 'defines only' list reaches §8, which states a normative requirement on the contract without the reconciling clause §2 carries for itself."* It does not reach it, and §8 now carries that clause: `:263-268` classifies `:252-254` as an **amendment condition** — a condition on the act of extending this contract rather than on the document's present state — which is not a state, transition, terminal outcome or invariant, and so is not an item §1's list purports to define. `:270-280` records what it is not, and why nothing is numbered; `:282-287` states what the requirement binds and what a signature on it attests, mirroring for §8 what `:46-48` and `:50` do for §2. §1's self-test (`:41-42`) was re-run against `:250-308` by extraction — each of the seven excluded topics at `:33-39` searched — and returns zero hits, as it did against `:250-259` before the extension. **GAP-8 was closed by `696738e` and recorded closed by `20f2a43`**, the register's first closure; extension, closure and signature are three separate acts and this row performs only the third. **Recorded rather than left to be discovered — three things.** First, this row's box was ticked by `c38ba9e`, a GitHub web-UI commit of 2026-08-25, **before any attestation text existed**, and that commit's own message states *"Section 8 remains unapproved"* while describing edits to sections 4 to 7 that it does not contain; the text of this row was spliced afterwards, and the sequence is recorded rather than smoothed over, on the disclosure practice `:314`, `:315`, `:317` and `:321` already establish. Second, GAP-8 closed on a partial test: `open_contract_gaps.md:390` holds that partial satisfaction does not close it, and closure was taken on the reading that it bites at the level of the three closure parts rather than limb by limb. This signature attests that the reading was taken deliberately and is recorded in the register; **it does not attest that a limb-by-limb reading is wrong.** Third, `:300-308` defers the wide reading of *invalidating an existing state* in Ruling 001 §7.4's form (`ruling_001_canonicalization_policy.md:358-364`); this signature attests that deferral **as a deferral**, and decides nothing about what invalidation means. **Not attested by this signature:** CR-004, the valence gloss `:258-259` places on Ruling 002 §1.1, which stands unrepaired, which AUTH-002 expressly did not reach, which never blocked §8, and which is not closed here; whether the conformance check at `:293-298` is enforced anywhere in the implementation, which was not examined; and the I1/`:217` attestation-boundary question, outside the corpus by its own terms. GAP-4 and GAP-5 remain open exactly as recorded. No gap is closed by this signature and no invariant is added.

Drafted 2026-08-04. Not binding until signed off and marked LOCKED.
