# Open Contract Gaps — requirements ruled but not yet enforceable

**Status:** REGISTER — a working ledger, not a governing document. Nothing here rules anything.

**Why it exists.** Under the operator's separation principle — **Ruling → what is true; Contract →
what implementations must obey** — a requirement stated in a Ruling is not yet enforceable until
Contract 001 carries it as an invariant. That propagation is the seam where WorldCraft's governance
has failed before: Ruling 002 §5.3 ruled a behavior into existence in the 2026-08-04 session and no
document carried it into machine-enforceable form, which is how the `SURFACED` state came to have no
name until 2026-08-05.

This register exists so that gap can never again depend on someone remembering it. Entries are
closed by Contract 001 gaining a corresponding invariant, not by discussion. **Amended 2026-08-16:**
the register also carries *ownership gaps* — topics an existing document excludes that no document
claims. These close when a document claims the topic, never by discussion. Each such entry must
state its own closure condition explicitly rather than borrow the rule above.

**Contract 001 was not to be edited until Ruling 002 is fully signed** (operator instruction,
2026-08-06). That condition was satisfied on 2026-08-15: Ruling 002's fifteenth and final section
was signed and the document is marked LOCKED. This records the condition as met. It decides nothing
about which entries, if any, should now be closed — entries are still closed only by Contract 001
gaining a corresponding invariant, not by the freeze lifting.

---

## GAP-1 — The validator's content-interpretation check

**Ruled in:** Ruling 001 §2, Invariant 3, as amended 2026-08-06 (Reading B).
**Contract invariant required:** none exists.

The amendment defines "mechanics" as any behavior, rule, or effect not derivable from the four
permitted fields by **lookup** against existing engine logic, and holds that a proposal violates the
invariant if content *within* an allowed field requires **interpretation** rather than resolution.

Ruling 001 §5 describes the validator as determining "whether the proposed family exists and whether
the classification is admissible under the current taxonomy." That is a lookup and field-membership
check — the Reading A validator. **Nothing authorizes or describes the content-interpretation check
that Reading B requires**, in either the Ruling or the Contract.

Also outstanding in §5: the proposal example reads `cost: 8` where the registry field is
`cost_factor` (`mythos_sync.py:187` — `"cost": result["cost_factor"]`, confirming `cost` is the
output field and `cost_factor` the registry field).

**Ownership ruled 2026-08-06 — Option 2.** §5 owns the provider authority boundary and taxonomy
existence validation only. **Contract 001 owns content-interpretation validation as a separate
invariant, alongside I7.** §5 has been scope-amended to say so explicitly and to state that the
validator it describes is not the whole validator. This entry closes when that Contract invariant
exists — not before.

**Resolved separately:** the `cost` → `cost_factor` correction in §5's proposal example was applied
2026-08-06 and is no longer outstanding.

## GAP-2 — Merge reversibility and provenance

**Ruled in:** Ruling 001 §3.4, signed as written 2026-08-06 with enforcement explicitly deferred.
**Contract invariant required:** none exists.

§3.4 requires that merges be recorded as **reversible, reviewable operations** — a merge must be
undoable without re-resolving everything downstream of it. Contract 001 contains nothing on merges
or reversibility; its nearest line is I6, which concerns epistemic states.

**Scope, per operator ruling 2026-08-06:** this entry covers merge reversibility and undo tracking
only. The provenance requirement that §3.4 states alongside it is tracked separately as GAP-3.

## GAP-3 — Authored-vs-learned provenance tracking

**Ruled in:** Ruling 001 §3.4 (provenance recorded separately from merge history), and made
load-bearing by the §3.2 amendment of 2026-08-06.
**Contract invariant required:** none exists.
**Split from GAP-2 by operator ruling, 2026-08-06.**

The §3.2 amendment exempts **operator-authored** concepts from requirement (b). That exemption is
keyed on a property — authored versus learned — which nothing in the system currently records.
Until provenance is tracked, no component can determine which concepts qualify for the exemption.

**GAP-3 is a precondition for correctly applying the §3.2 exemption** (operator ruling). It is not
merely a data-quality improvement: without it, the exemption is unenforceable, and a component
attempting to apply it would have to guess at authorship — which is the class of silent inference
Ruling 001 Invariant 1 exists to forbid.

## GAP-4 — Grounding-target fallback authority

**Ruled in:** nothing rules it. Opened alongside the signing of Ruling 002 §2, 2026-08-06.
**Contract invariant required:** none exists.

**This entry covers two distinct fallback sites with distinct triggers.** Both return an arbitrary
grounding target rather than stopping.

**Naming status, updated 2026-08-08 on the signing of Ruling 002 §5.4.** `Indomitable Will` is now
**explicitly named by a ruling**: §5.4 records it as the terminal resolution policy for the
human-excellence domain. **That authorization is domain-scoped** — the same table rules that a
supernatural concept has no fallback and resolves to `GROUNDING_UNAVAILABLE`. **Neither implementation
site is domain-scoped.** Neither consults anything domain-shaped, because no domain layer exists, so
neither can distinguish the case §5.4's policy turns on. The sites are therefore **not authorized by
§5.4, cannot guarantee conformance to it, and remain debt-bearing.**

**Measured, not alarm — the debt is latent, not active.** `ground_power` has exactly one caller,
`audit_power`, which short-circuits to `⚠️ UNVERIFIED` for any power absent from `POWER_REGISTRY`
(`logic_auditor.py:203-204`, covered by `test_engine.py:100-102`), and every registered power carries
a family. **Both sites are unreachable by any existing call path with existing data.** What is
recorded here is what happens when either premise stops holding, not what the engine does today.

**The bound must govern the whole mechanism.** `DEFAULT_TRANSPOSITIONS` also contains
`Strategic Genius` and `Art of War`, neither named by any ruling. An authorization covering only
`Indomitable Will` would leave the mechanism unbounded.

| # | Site | Fires when |
|---|---|---|
| 1 | `logic_auditor.py:136` — `DEFAULT_TRANSPOSITIONS` (`Indomitable Will` / `Strategic Genius` / `Art of War`), returned by `_grounding_candidates` | a power has **neither** a curated `TRANSPOSITION_MAP` entry **nor** usable family kin |
| 2 | `logic_auditor.py:173-174` — the hardcoded `return "Indomitable Will"` in `ground_power` | the candidate list survives `_grounding_candidates` but is **emptied by the legality filter** (registry membership + `min_modality` ≤ fusion rank). This can catch a power that *does* carry a curated entry, if none of its destinations is legal for the fusion. |

**The triggers are not interchangeable and the sites are not redundant.** Site 1 is reached before
legality is considered; site 2 only after. A fix that bounds one leaves the other standing. Both are
the shape Ruling 002 §2 forbids at the family layer, sitting one layer down at the grounding layer.

**Scope, per operator ruling 2026-08-06.** Ruling 002 §2 was signed **narrow** — family assignment
only. Grounding-target fallback is a separate layer under Addendum A's fixed `domain → family →
grounding` sequencing, and belongs in contract tracking rather than in the taxonomy ruling. This
entry carries it. The same split was applied to Ruling 001 §5 on 2026-08-05.

### Verification — does §8.1 guarantee an unplaceable concept never reaches grounding?

Ordered by the operator before this entry could be finalized, because the answer determines whether
GAP-4 is dormant-but-safe or a live risk. **It was verified against the code and the governing
documents, not assumed.**

**Answer: the halt is stated in the specification, is not backed by any invariant, and is not
enforced anywhere in the implementation. It holds today only as a property of the authored registry.**

**At specification level the halt is stated three times, and ruled nowhere.**

| Where | What it says | Force |
|---|---|---|
| Ruling 002 §8 | a learned concept **may not enter the registry** unless `modality`, `family` and `cost_factor` are all valid | admission gate — the strongest of the three |
| Ruling 002 §8.1, row 2 | `UNRESOLVED_FAMILY` → Grounding column reads `—` | a table cell, not a prohibition |
| Contract 001 §5.1 | `UNRESOLVED_FAMILY` appears under the column header **Terminal condition** | the halt is carried by the word "terminal" |

Contract 001 **I2** fixes the resolution *order* — domain → family → grounding. **No invariant
states that a terminal condition at one stage forbids the next stage from running.** I4, I5 and I7
are explicit prohibitions; the terminal-halt property has no equivalent. It is inferable from the
word "terminal" and from §8's admission gate, and inference is exactly the standing this register
exists to eliminate.

**At code level there is no family-resolution stage at all, and nothing consults one.**
`ground_power` has exactly one call site — `logic_auditor.py:230` — inside the `else` branch of a
guard that returns `⚠️ UNVERIFIED` for any power absent from `POWER_REGISTRY` (`:204`). The property
"an unplaceable concept does not reach grounding" is therefore true today **because registry
membership and family possession are the same fact**, measured at 30/30 entries carrying a family.
That is a coincidence of authorship, not a check.

**Measured at the current commit:**

```
registry entries                                 : 30
entries missing a family                         : 0
powers that can ever require grounding           : 12
   of those, without a curated entry             : 0    → family fallback dead (Audit 001 M1)
registry powers reaching DEFAULT_TRANSPOSITIONS  : 0
smallest family (PERCEPTION)                     : 5 members → kin is never empty
curated lists emptied by the legality filter     : 0 at fusion ranks 1, 2 and 3
   → site 2's hardcoded return is unreachable today
```

### Classification — live risk on implementation, not dormant-but-safe

**GAP-4 is not the same shape as Audit 001 (M1).** M1's family-fallback branch is dead because of
registry *contents*: every groundable power happens to carry a curated entry. `DEFAULT_TRANSPOSITIONS`
is dead for that reason **and** for a second one — every family happens to hold enough members that
`kin` is never empty — and it sits behind an **unenforced ordering assumption** on top of both. Three
guards, none of them a check, all three properties of the authored registry rather than of the
algorithm.

Each guard fails to a different learned-vocabulary case:

- a learned power with a **resolved** family and no curated entry → activates the family fallback (M1's branch)
- a learned power in a **sparse** family → empties `kin`
- a learned power with an **`UNRESOLVED_FAMILY`** result → reaches `DEFAULT_TRANSPOSITIONS`, *iff*
  anything calls grounding without first checking the family terminal — **which nothing currently
  prevents by construction**
- a learned power whose curated destinations are **all illegal for the fusion's modality** → empties
  the candidate list after filtering and reaches site 2's hardcoded `Indomitable Will`

**This entry closes when Contract 001 carries an invariant that (a) makes terminal conditions halting
rather than advisory, and (b) for **each** of the two sites above, either authorizes the fallback with
an explicit bound or removes it.** Not before, and not by the registry continuing to be authored in a
way that hides them.

---

## GAP-5 — `SURFACED` payload completeness

**Ruled in:** Ruling 002 §5.3, signed 2026-08-08. Contract 001 §5.1 states the requirement in its
terminal-mapping cell.
**Contract invariant required:** none exists.

§5.3 requires a surfaced fusion to preserve three things: the accepted components, the unresolved
components, and the reason for exclusion. **Contract 001 §6 carries two of the three.**

| §5.3 requirement | Invariant | Status |
|---|---|---|
| the reason travels to the output | **I5** — no silent terminal | carried |
| `SURFACED` is terminal, not a degraded `ADMITTED` | **I7** | carried |
| accepted components reported alongside rejected ones | — | **not carried** |

**Why the third is not covered by the first two.** I5 governs the reason, not the payload; I7 governs
the result's standing, not its contents. Neither states that a `SURFACED` output must still contain
what resolved. An implementation may therefore emit `SURFACED` carrying only the rejected component
and its reason, discard the accepted components, and violate no invariant — **which is the hard
fusion failure §5.3 explicitly rejects**, on the ground that it *"discards the work that did
resolve."*

**The requirement is stated, but not where enforcement lives.** It appears in §5.3's prose and in
Contract 001 §5.1's terminal-mapping cell (*"accepted and rejected components both reported, with
reason"*). Contract 001 §5 opens by describing itself as a consolidation of already-ruled material —
**§6 is the enforcement layer, and §6 is silent.** This is the seam shape recorded on 2026-08-05: a
ruling brings a behavior into existence and nothing states which document must carry it into
machine-enforceable form.

**Load-bearing as of 2026-08-25:** Contract 001 is signed in full and marked LOCKED, so the
condition that made this entry latent no longer holds. It remains open on its own terms.

**This entry closes when Contract 001 carries an invariant requiring a `SURFACED` result to preserve
the accepted components, the rejected components, and the reason for rejection.** Not before.

Opened 2026-08-08.

---

## GAP-6 — Caching and storage strategy is unowned

**Type:** ownership gap. **Ruled in:** nothing — no Ruling states a caching or storage requirement.
**Contract invariant required:** none exists, and Contract 001 §1 excludes the topic.

Contract 001 §1's exclusion table routed *caching, storage strategy* to Ruling 001 §5. §5's scope
amendment of 2026-08-06 states that §5 owns **the provider authority boundary and taxonomy existence
validation only**. Caching appears in §5 twice and neither is an ownership assignment: a Cost
paragraph observing that the result "is cached permanently," and an illustrative file tree listing
`cache.py`. Ruling 001 §1 makes one substantive claim about cache behaviour — a false identity "is
hidden behind the cache, which makes it invisible precisely where it does the most damage" — but
that is an argument for conservative canonicalization, not a grant of ownership over storage
strategy. A corpus-wide search finds no other document claiming the topic.

The exclusion therefore had no destination. Contract 001 §1 states that "anything in the right-hand
column appearing as a condition in this contract is a defect in this contract," which makes the
right-hand column load-bearing, and the row pointed at a section that by its own signed scope does
not own what it was sent.

**Historical note (added 2026-08-16).** The paragraph above quotes Contract 001 §1's self-test as it
read when this entry was opened, and derives the defect from it. That sentence was subsequently
corrected to test the **left-hand** column — an excluded topic appearing as a normative condition —
and under the corrected text it no longer reaches a misaddressed destination. Both the quotation and
the derivation are preserved as the record of what was reasoned on 2026-08-16, and neither is
restated as current. **This entry's finding is unaffected:** that no document claims caching and
storage strategy was established by corpus search, independently of the self-test.

**This entry does not close the way GAP-1 through GAP-5 close.** Those are requirements ruled in a
Ruling and awaiting a Contract 001 invariant, so the register's standing closure rule reaches them.
This is not a ruled requirement. **This is not a sixth Contract 001 invariant in waiting. Contract
001 §1 forbids it from becoming one.** The standing rule therefore cannot reach this entry.

**Closure condition: a document claims ownership of caching and storage strategy.**

Opened 2026-08-16.

**Dependency note (added 2026-08-16):** Contract 001 §1's "model usage" row is coupled to this
gap's resolution pending further definition. Closing this gap does not automatically resolve
model usage. Model usage resolves only if the document that claims caching/storage ownership
also explicitly addresses model usage — closure on caching/storage strategy alone leaves model
usage open.

---

## GAP-7 — Prompts is unowned

**Type:** ownership gap. **Ruled in:** nothing — no Ruling states a prompt-design or
prompt-content requirement.
**Contract invariant required:** none exists, and Contract 001 §1 excludes the topic.

Contract 001 §1's exclusion table routed *provider choice, model usage, prompts* to Ruling 001
§5 as a single bundled row. §5's scope amendment of 2026-08-06 states that §5 owns **the provider
authority boundary and taxonomy existence validation only**. A corpus-wide search for "prompt"
across all governance documents returns exactly one hit outside this register: Contract 001 §1's
own exclusion table. Ruling 001 §5 does not use the word "prompt" anywhere in its text — not in
the resolver diagram, not in the cost paragraph, not in the dependencies sketch. No document
claims this topic.

The exclusion therefore had no destination, for the same reason GAP-6 did. An exclusion table must
route each excluded topic to a document that owns it; this row routed *prompts* to a section whose
signed scope does not cover it, and no other document covers it either. That is a defect in the
table on its own terms. **This entry does not rest that conclusion on §1's self-test.** As corrected,
that test governs an excluded topic leaking back in as a normative condition, which is a different
failure from a misaddressed destination, and it does not reach this one.

**This entry does not close the way GAP-1 through GAP-5 close.** Those are requirements ruled in
a Ruling and awaiting a Contract 001 invariant, so the register's standing closure rule reaches
them. This is not a ruled requirement. **This is not a sixth Contract 001 invariant in waiting —
nor a seventh. Contract 001 §1 forbids it from becoming one.** The standing rule therefore cannot
reach this entry.

**Distinct from GAP-6.** GAP-6 concerns *caching, storage strategy* only. Its supporting sentence,
Ruling 001 §5:251, bundles two observations — that "2–3 calls per novel concept is reasonable" and
that "the result is cached permanently" — and GAP-6 draws only the caching clause from it. The
call-volume clause is not within GAP-6's scope and GAP-6 makes no claim about it. This entry
concerns *prompts*, a topic with no candidate owner and no supporting sentence anywhere in the
corpus to dispute. The two are not merged and do not share a closure condition.

**Closure condition: a document claims ownership of prompt design or content.**

Opened 2026-08-16.

---

## GAP-8 — §8's normative requirement is unclassified

**Type:** classification gap. **Ruled in:** nothing — no Ruling states a requirement about Contract
001's own extensibility. §8's clause originates in the contract.
**Contract invariant required:** none, and an invariant is probably the wrong instrument — see the
closure condition below.

Contract 001 §8 states a normative requirement at `contract_001_domain_resolution.md:252-254`:
*"This contract must permit additional resolution states without invalidating existing states,
provided new states preserve the distinction between unknown, ambiguous, and resolved knowledge
conditions."* Nothing in the contract says what kind of instrument that "must" is.

Every other normative element in the document carries scaffolding that §8's clause lacks:

| | §2 (V1/V2) | §6 (I1–I7) | §8 |
|---|---|---|---|
| Self-classification | `:46-48` — *"not features… conditions the contract must satisfy to be valid"* | §6's heading names them invariants; each is numbered | none |
| Scope declaration | `:50` — *"conditions on the whole of this contract, §1 through §8"* | carried by the contract's own definition list, `:24-27` | none |
| Operational test | V1 `:87-90` conformance check, with a stated violation condition at `:88`; V2 `:99-103` plus `:106-108` | GAP-4 and GAP-5 record which are enforced and which are not | none |
| Membership in a named set | V1, V2 | I1 through I7 | belongs to no set |

**There is no V3.** A search for `V3` across all of `docs/` returns nothing. §8's requirement is not
a third validity constraint, is not among §6's seven invariants, and is not reached by `:50`, which
names V1 and V2 only. The contract therefore contains exactly one normative requirement that no
scope clause governs, no set contains, and no procedure tests.

**§1's signature routed this question here.** `contract_001_domain_resolution.md:265` records, as
not attested by §1: *"whether §1's 'defines only' list reaches §8, which states a normative
requirement on the contract without the reconciling clause §2 carries for itself — that belongs to
§8's signature."* The clause §1 refers to is `:46-48`. §2 faces the same objection §8 faces — a
normative statement in a document whose §1 says it *defines only* states, transitions, terminals and
invariants — and §2 answers it in text. §8 does not.

**Related, and not filed separately:** §8's proviso restates V2's substance in V2's own coined term
without citing V2. *knowledge conditions* occurs exactly twice in the contract, at `:96` (V2) and
`:253` (§8). Whether that is duplication to remove, a cross-reference to add, or correct as written
is part of what closing this entry must decide.

### This is an absence, not a violation

**§8 breaks no rule this contract states.** It passes §1's self-test: `:41-42` catches an excluded
topic appearing as a normative condition, and §8's subject is the contract itself — every one of the
seven excluded topics at `:33-39` was checked against §8's full text and none appears. No rule
anywhere requires a normative statement to be classified, scoped, or testable.

**This entry is therefore not the same shape as §7's defects.** CR-002 and CR-003 record text that
asserts something the source does not support, or states a condition about a subject the contract
excludes. Those are defects in what is written. This is the absence of something that was never
written. **A reader must not conclude from this entry that §8 failed the test §7 failed.** §7 failed
`:41-42`; §8 passes it. They fail differently, and only one of them fails at all.

**Nearest precedent, and how it differs.** Ruling 001 §7.4 (`ruling_001_canonicalization_policy.md:358-364`)
leaves `SURFACED` component-neutral and says so — *"Deferred deliberately: gating a state on a
`required` predicate today would make the state machine depend on an undefined component model"*
(`ruling_001_canonicalization_policy.md:363`). That is a **recorded** deferral: it names the absence, the reason, and what must happen
once the prerequisite exists. §8's absence is **unrecorded** — nothing states that leaving the clause
unclassified was a decision. This entry exists to convert an unrecorded absence into a recorded one.
It does not assert the absence was accidental; it records that the corpus does not say either way.

### This entry does not close the way GAP-1 through GAP-5 close

Those are requirements ruled in a Ruling and awaiting a Contract 001 invariant, so the register's
standing closure rule reaches them. This is not a ruled requirement, and an invariant is not what it
needs — adding I8 would create an eighth member of a set §8's clause does not belong to, without
saying what the clause itself is. Per the register's 2026-08-16 amendment, this entry states its own
closure condition.

**Closure condition — Contract 001 §8 gains text that does all three:**

1. **Classifies its own requirement** — states what kind of instrument `:252-254` is, mirroring what
   `:46-48` does for §2, or states that it is a fourth thing and names it.
2. **Is reached by a scope statement** — either brought under an amended `:50`, or given its own
   scope clause stating what the requirement binds and what a signature on it attests.
3. **Is testable, or says why not** — an operational check in V1's form (`:87-90`), including what
   violating the requirement looks like; or an explicit statement that no such test exists and why,
   in the manner of Ruling 001 §7.4's recorded deferral.

Partial satisfaction does not close this entry. Discussion never closes it.

### Dependency chain — this entry cannot close in one step

Closing GAP-8 requires **authored new text**, not a wording substitution. It therefore requires, in
order:

1. **AUTH-002** — a new authorization. **AUTH-001 does not cover this.** AUTH-001 is bounded to
   `:245`, `:246` and `:248`, and to specific From/To wording specimens at each; new authored text at
   §8 falls outside both bounds.
2. **Drafted text**, produced under that authorization.
3. **Operator wording review** of that text before it lands — AUTH-style authorization clears the
   permission question only, never the wording question.
4. **The commit**, after which this entry closes.

Opened 2026-08-23.

Closed 2026-08-25 by `696738e`. See **Closed** below.

---

## Closed

### GAP-8 — §8's normative requirement is unclassified

**Closed 2026-08-25 by `696738e`**, which inserted 49 lines into Contract 001 §8 under AUTH-002
(`authorizations.md:153-314`) after `:259`. This is the register's first closure.

The entry's three-part closure condition is met:

1. **Classifies its own requirement.** `:252-254` is named a fourth kind of thing — an *amendment
   condition*, a condition on the act of extending the contract rather than on the document's
   present state, which is what V1 and V2 are. Not V3, not an invariant, and no set is created.
2. **Is reached by a scope statement.** Its own, on the second of the two routes the closure
   condition offers. A signature on §8 attests that the requirement is classified and scoped as
   stated and that no amendment made before that signature violated it; it does not attest that a
   future amendment will comply.
3. **Is testable in part, and says why not for the rest.** The second limb is V2 carried forward and
   is tested by V2's own checks; the first limb is tested on the narrow reading — a state removed,
   contradicted, or left with a definition no case can satisfy — and the wide reading, a state
   invalidated by losing cases to a new state, is a recorded deferral in Ruling 001 §7.4's form
   (`ruling_001_canonicalization_policy.md:358-364`).

**Recorded rather than left to be discovered: this closed on a partial test.** The entry holds that
partial satisfaction does not close it. The closing text was accepted on the reading that the rule
bites at the level of the three parts, and that part 3's *"or says why not"* is satisfied by one
limb tested and the other deferred with its reason and its prerequisite stated. That reading was put
to the operator at the wording review and accepted. A reader who takes the rule to bite limb by limb
should know the question was seen and decided, not missed.

**The `knowledge conditions` question** the entry left to closure is decided on the cross-reference
branch, the only branch AUTH-002 permits: the new text cites V2 at `:96`, and `:252-254` is
unchanged.

**What this closure does not do.** It does not sign §8 — the box at `:322` still reads `- [ ]`, and
extension and signature are separate acts. It does not repair CR-004, which AUTH-002 does not reach
and which never blocked §8. GAP-4 and GAP-5 remain open exactly as recorded. This register rules
nothing, and this entry records a closure rather than performing one; the commit does that.

Opened 2026-08-06.
