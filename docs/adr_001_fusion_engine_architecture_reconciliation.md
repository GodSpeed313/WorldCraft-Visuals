# WorldCraft Architecture Decision Record — ADR-001: Fusion Engine v0.1 Architecture Reconciliation

**Type:** ARCHITECTURE DECISION RECORD, per Fusion Engine spec §37. Not a ruling, not a contract, not a gap entry. Rules nothing outside the Fusion Engine's own architecture; authorizes no implementation.

**Status:** ACCEPTED (2026-09-13). Implementation remains unauthorized — see §6.

**Governs:** How the Fusion Engine v0.1 (LOCKED) requirements are structured as architecture, given the current WorldCraft-Visuals codebase and Ruling 001/002/Contract 001. Does not modify any of those documents.

**Citation convention.** Per `audit_method.md` M8, references to this document from elsewhere in the corpus must be filename-qualified (`adr_001_fusion_engine_architecture_reconciliation.md:NNN`) — a bare `:NNN` anchor resolves to `contract_001_domain_resolution.md` by house convention (M3) and would misresolve here. This is the corpus's first Architecture Decision Record; no prior naming or numbering convention existed for this document type before this file.

---

## 0. Explicit prohibition on this ADR's own scope

This ADR **does not resolve, adjudicate, or take a position on**:

1. **Unknown → GROUNDED** — the live violation of Ruling 001 Invariant 1 in `modality_classifier.py:34-42`. Not fixed here. Not ruled here.
2. **GAP-4** — the grounding-target fallback authority gap. Not adjudicated here.
3. **Ruling 002 §10.3** — what replaces `dominant_family` as a disposition field. Not decided here.

Each of these is instead threaded through the architecture below as a **named seam**: a boundary the architecture defines precisely enough to build against today, whose *filling* is deferred to a future ruling or authorization. An architecture that could only be built after all three were settled would not be an architecture — it would be a wait. The purpose of this ADR is to show that none of the three block the Fusion Engine's internal design; they only block certain of its *inputs* and one *unconnected downstream consumer*.

---

## 1. Top-level boundary: unchanged, reaffirmed

Per FE spec §4.1, the pipeline is sequential, not parallel:

```
Governance Resolution → Eligible/Resolved Source State → Fusion Engine Reasoning → Fusion Compatibility Result
```

**Architecture decision AD-1:** The Fusion Engine does not read `POWER_REGISTRY`, `CHARACTER_REGISTRY`, `TRANSPOSITION_MAP`, or `MODALITY_RANK` directly, and does not call `classify()`, `classify_fusion()`, `audit_power()`, or `ground_power()` as part of its own reasoning. Those remain entirely on the governance side of the boundary. The Fusion Engine receives sources only after governance resolution has run, via the interface named in **Seam 1** below.

This decision is what makes Seams 1 and 2 legitimately separable from the Engine's internal design rather than internal defects of it: the Engine's architecture can be fully specified without knowing how governance resolution is fixed, because the Engine only ever consumes the *output* of that boundary, never its internals.

## 2. New components required (none of which exist today)

These are conceptual components — responsibilities and boundaries, not classes, schemas, or APIs.

**C1 — Contribution/Placement Classifier.** Assigns each substantive source property a Contribution Type (§7) and Architectural Placement (§8). New; no existing code does this. Operates only on already-admitted sources (post-Seam-1).

**C2 — Provenance Ledger.** The structural home of INV-01 through INV-11: one authoritative mechanic-derivation state per substantive property/interaction/emergent property, a dependency graph over them, and the weakest-link computation (INV-05/06) that lets a descendant's provenance be read off its ancestry rather than asserted independently. This is new; nothing in the current codebase tracks derivation-of-a-mechanic at all (confirmed: zero occurrences of "provenance" anywhere in `.py`/`.html`). The Ledger is the single place INV-02 (Representation Consistency) is enforced — every other component reads from it and writes nothing that contradicts it.

**C3 — Contradiction/Compatibility Evaluator.** Implements §14's four-state result (Compatible/Conditionally Compatible/Incompatible/Unresolved) and INV-11 (Contradiction Refusal). Structurally distinct from `ground_power()`: this component's contract permits refusal and Unresolved as first-class successful outcomes, where the existing auditor's contract guarantees a substitution always succeeds (`logic_auditor.py:173-174`'s hardcoded terminal fallback). These are not the same shape of function and C3 is not an extension of `ground_power()`.

**C4 — Dominance / Substantive-Participation Evaluator.** Implements INV-15/16 and the §30 Counterfactual Contribution Test, operating per-mechanic ("if this contribution were removed, would the fused mechanics materially change?"). Reuses the existing `dominance` input concept from `classify_fusion()` (a 0–100 weighting is already plumbed through the pipeline) but not its categorical `>=70/<=30/balanced` logic, which cannot express a removal test.

**C5 — Structured Reasoning Record.** §24/§25's pre-presentation structured state. Holds C1–C4's outputs in one place before any creative prose is generated. This is the direct architectural generalization of the *pattern* already proven at small scale in `logic_auditor.py`'s `state`/`status` split (INV-18 — see AD-2 below) and in `mythos_sync.py`'s existing discipline of building a complete `profile` dict before `lore_templates` renders from it.

**C6 — Presentation Renderer.** Consumes C5 only. May vary tone/terminology/style; may not alter classifications (INV-18). This is a generalization of `display_profile()`/`dashboard.html`'s existing role, not a replacement for them — those remain the legacy Mythos-Sync presentation layer; C6 is the Fusion Engine's own, parallel to it.

**Architecture decision AD-2:** INV-18 (State/Presentation Separation) is **Already Supported as a principle** and is adopted wholesale as the design discipline governing C2 → C5 → C6: reason into C2/C5 first, render via C6 second, and no component downstream of C5 may re-decide a classification. This mirrors, and is licensed by, FE §26's own instruction to preserve the *principle* behind `logic_auditor.py`'s `state`/`status` split without requiring reuse of the component itself.

## 3. Explicit non-mappings (required by §4.4's State-Identity Principle)

Recorded here because leaving them unstated is exactly the failure mode §4.4 warns about — shared vocabulary silently read as shared semantics.

- **`family` (Ruling 002 grounding concept) ≠ Contribution Type (C1) ≠ Proposal 001 P2's four-layer split.** Three unrelated classification schemes that happen to sit near the word "family" or "capability layer." None is derived from, supersedes, or is validated by either of the others.
- **"Mechanism" in FE §7 (a Contribution Type) ≠ "Mechanism" in Proposal 001 P3's `System → Mechanism → Technique → Effect` layering.** Same word, unrelated concepts; C1 does not consult or constrain P3-shaped taxonomies.
- **FE §5's source-kind examples ≠ any domain taxonomy** — not Ruling 002 §5/§10.1/§10.9's domain layer, not Proposal 001 P4's sketched domain list. C1/C2 do not assume, require, or produce a domain classification of any kind. This is deliberate: it keeps the Engine's architecture from silently pre-empting Ruling 002 §10.1/§10.9, which Proposal 001 itself already warned against doing via P4.
- **Governance state families (`UNRESOLVED_DOMAIN`, `UNRESOLVED_FAMILY`, `ADMITTED/SURFACED/CAUTIONARY/BLOCKED`) ≠ Fusion Engine state families (`Source-Derived/Defensibly Derived/Invented Bridge/Unresolved`, `Compatible/Conditionally Compatible/Incompatible/Unresolved`).** Per FE §4.4 verbatim, restated as architecture: C2/C3's internal state identities are namespaced and separate from governance's, regardless of natural-language overlap in the word "unresolved."

None of these non-mappings requires a ruling — §4.4 already mandates the distinction; this section only discharges the ADR-drafting obligation the prior reconciliation pass identified.

## 4. The three seams

This is the core of the ADR. Each seam is specified as: **what the architecture requires at this boundary**, **what currently occupies it**, and **what a future decision must supply** — without proposing what that decision should say.

### Seam 1 — Source Admission Interface *(where Unknown → GROUNDED lives)*

**What the architecture requires:** Per AD-1, the Fusion Engine's first action on any source is to receive an already-resolved, eligible source state from governance. FE §4.1 states this as a precondition, not a step the Engine performs itself: *"The Fusion Engine must not substitute its own compatibility classification for an unresolved governance question."*

**What currently occupies it:** Nothing compliant. `classify()` is the closest existing function to this interface, but it does not satisfy the contract the Engine needs — instead of returning "unresolved" for an unrecognized character, it silently manufactures a resolved `GROUNDED` state (the Ruling 001 Invariant 1 violation). This means **the seam currently has no valid implementation to call**, for *any* source that isn't already in `CHARACTER_REGISTRY`. This is a real architectural fact, not a cosmetic one: it is recorded here rather than papered over with a placeholder, per this ADR's own no-silent-resolution obligation.

**What future implementation/authorization must supply:** a source-resolution implementation conforming to Ruling 001 §4's already-locked resolve-then-proceed state model, including CAUTIONARY/BLOCKED behavior for unresolved or rejected normalization. No new semantic ruling is required to prohibit unknown→GROUNDED; only the concrete implementation path and scoped authorization remain open.

### Seam 2 — Governance Resolution Input *(where GAP-4 lives)*

**What the architecture requires:** The same §4.1 sequencing, one stage further in: once a source is admitted, its *family/modality-grounding* eligibility must also arrive as a resolved-or-unresolved state before C2 (Provenance Ledger) can honestly compute a descendant's provenance per INV-07 (*"if any required dependency... is Unresolved, the descendant remains Unresolved"*).

**What currently occupies it:** `_grounding_candidates`/`ground_power`'s fallback chain, confirmed by `test_hypothesis_properties.py::Gap4UnresolvedFamilyTests` to always terminate in a concrete, legal power with no distinguishable "unresolved" signal. **C2 cannot consume this fallback's output as an Unresolved-dependency input, because the fallback never produces one.** This is a hard structural block on INV-07 specifically (confirmed in the prior reconciliation pass), not merely an inconvenience.

**What a future decision must supply:** Whatever GAP-4's eventual ruling authorizes as the grounding layer's honest Unresolved/CAUTIONARY output. C2's dependency-graph design does not need to know what that ruling says — it only needs the ruling to produce *some* input that is distinguishably Unresolved when grounding cannot be honestly determined. The Ledger's contract at this seam is: *accept an Unresolved marker if one is ever supplied; until then, treat any input arriving through the current fallback as ineligible to seed Fusion Engine reasoning* — which, combined with Seam 1's gap, means **components upstream of both seams currently cannot honestly hand the Engine anything for an unregistered or ambiguously-classified source.**

### Seam 3 — Disposition Synthesis *(where §10.3 lives)*

**What the architecture requires:** Nothing, structurally — this is the seam's defining property. C4 (Dominance/Substantive-Participation Evaluator) is self-contained: it evaluates per-mechanic removal-counterfactuals (§30) and does not need `dominant_family`, a replacement disposition field, or any Ruling 002 §7 concept to function on its own terms.

**What currently occupies it:** `dominant_family` (`mythos_sync.py:242-243`), a plurality vote over `family` values, consumed only by legacy display code (`display_profile`, `dashboard.html`) — never by any decision logic, and never by anything C4 depends on.

**What a future decision must supply:** *Nothing is required for the Fusion Engine to function.* This seam only becomes load-bearing if a future Ruling 002 §10.3 decision chooses to derive a fusion-level disposition summary *from* C4's per-mechanic results (one candidate direction, unadopted, floated only informally by Proposal 001 P2) — or chooses some unrelated design. **Architecture decision AD-3:** until §10.3 is ruled, `dominant_family` and C4 remain parallel and non-communicating; neither may be used to compute the other, and C4's design must not be shaped in anticipation of a particular §10.3 outcome.

## 5. What this ADR explicitly does not decide

Mirroring the corpus's own convention (Ruling 001 §7, Proposal 001 §3) of stating exclusions plainly rather than leaving them to be inferred:

- Does not fix `modality_classifier.py`, does not authorize editing it, does not specify what it should return instead.
- Does not adjudicate GAP-4, does not choose a bound for `DEFAULT_TRANSPOSITIONS`, does not decide whether cross-domain grounding should be refused or redirected.
- Does not decide what replaces `dominant_family`, does not adopt Proposal 001 P2's scale/expression disposition candidate, does not adopt FE INV-16/§30 as a *replacement* for §7's open question — only as C4's own internal mechanism.
- Does not adopt Proposal 001 P4's domain list or any other domain taxonomy.
- Does not specify implementation language, data structures, or whether C2's dependency graph is literal graph storage — per FE §35, all of that remains open.
- Does not authorize implementation. FE §38's Pre-Implementation Gate items (conflicts with existing governance ruled on; implementation responsibilities identified) are not satisfied by this ADR — items 1–3 above are exactly the unruled conflicts §38 has in mind.

## 6. Status and next steps

Accepted by the operator as the architecture decision record for Fusion Engine v0.1, 2026-09-13. Acceptance attests that the architecture described in §§1–4 is the agreed design direction and that the non-mappings in §3 hold; it does not attest that any implementation exists or conforms to it.

Implementation remains unauthorized until the §38 pre-implementation gate is satisfied. Seam 1 requires compliant implementation/authorization, Seam 2 remains dependent on GAP-4 resolution, while Seam 3 does not block Fusion Engine implementation unless a future §10.3 decision chooses to connect disposition synthesis to C4. Nothing in this document should be cited as settling Unknown→GROUNDED, GAP-4, or §10.3; each remains exactly as open as the governance record already states.
