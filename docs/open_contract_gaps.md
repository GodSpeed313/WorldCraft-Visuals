# Open Contract Gaps — requirements ruled but not yet enforceable

**Status:** REGISTER — a working ledger, not a governing document. Nothing here rules anything.

**Why it exists.** Under the operator's separation principle — **Ruling → what is true; Contract →
what implementations must obey** — a requirement stated in a Ruling is not yet enforceable until
Contract 001 carries it as an invariant. That propagation is the seam where WorldCraft's governance
has failed before: Ruling 002 §5.3 ruled a behavior into existence in the 2026-08-04 session and no
document carried it into machine-enforceable form, which is how the `SURFACED` state came to have no
name until 2026-08-05.

This register exists so that gap can never again depend on someone remembering it. Entries are
closed by Contract 001 gaining a corresponding invariant, not by discussion.

**Contract 001 is not to be edited until Ruling 002 is fully signed** (operator instruction,
2026-08-06). These entries are therefore expected to remain open until then.

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
grounding target rather than stopping; neither is authorized, bounded, or named by any ruling.

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

**Not yet load-bearing:** Contract 001 is unsigned in full, so no implementation has been authorized
against the incomplete set.

**This entry closes when Contract 001 carries an invariant requiring a `SURFACED` result to preserve
the accepted components, the rejected components, and the reason for rejection.** Not before.

Opened 2026-08-08.

---

## Closed

*(none yet)*

Opened 2026-08-06.
