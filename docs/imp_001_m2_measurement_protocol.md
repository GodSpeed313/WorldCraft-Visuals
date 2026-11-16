# IMP-001 Milestone 2 — Measurement Protocol

**Status:** REVIEWED PROTOCOL — revision 2.1, approved by the operator for publication on 2026-11-15. **This is not an authorization.** Having this file in the repository grants no permission to call any API, spend money, run the proposer, or write code. M2 runs only under a separate operator authorization that names this protocol.

Basis: repo `main` at `891fa0e`; REQ-001 v1.0 §§3–5 (`proposer/inputs/req_001_v1.0_sections_1-5.md`).

## 1. Scope

- Exactly **one recorded attempt** on **one dev pair**, then stop for review.
- Proposed first pair (operator-approved selection, 2026-11-15): **Ilse Marrow × Sable Quillon**.
- Dev characters only (`dev_data/prop001/characters/`). The seven reserved pairs stay prohibited.
- The model input is the M1 packet (`proposer/packet.py`) plus a fixed instruction with no pair-specific text. Its `packet_sha256` is recorded.
- **No prompt contamination:** nothing sent to the model may suggest, hint at, or rank a fusion mechanism for this pair. The reasons for choosing the pair stay out of every model input.
- No rendering. Leak-check collisions stay deferred to the rendering milestone.

## 2. Three separate verdicts

An attempt gets three verdicts that are recorded separately and never merged:

| Verdict | Question | Decided by | Values |
|---|---|---|---|
| **VALID** | Does the output meet the mechanical requirements? | Script | VALID / INVALID |
| **DEFENSIBLE** | Is there a real fusion (or a correct no-fusion), at the levels claimed? | Operator review | per-test pass/fail + judged levels |
| **CREATIVE** | Is the result worth having as a character? | Operator | yes / maybe / no + one line |

A mechanically valid output can fail review. A defensible one can still be creatively flat.

**No-fusion results.** A no-fusion report can be VALID and DEFENSIBLE. That shows its stated rejections are correct. It does **not** show that the proposer found every possible interaction, and it is never recorded as evidence that no fusion exists for the pair.

## 3. Q1 — Validity (mechanical; gates everything else)

These are the REQ-001 §5 checks, applied by output type:

**Proposal:** follows the output template; the pair file passes `fusion_synthesis/schema.py`; every cited property id exists on the named parent; at least one cited property from each parent; every limitation cites a source; trait outcomes cover every property of both characters; shared-structure and emergence levels are present, with emergence ∈ {2, 3}; provenance ∈ {Defensibly Derived, Invented Bridge}.

**No-fusion:** follows the template; 1–3 distinct candidates, each naming its failed test(s) and property ids; an explanation if there are fewer than three.

INVALID → recorded as a failed attempt with the list of failed checks. No further review (REQ-001 §5).

## 4. Q2 — Emergence (operator review; only if VALID)

1. Strip the causal explanation and declarations, and review the card alone.
2. Record your own judgment before looking at the declarations: defensibility tests 1–4 (pass/fail each), whether any hard limitation or prohibition is contradicted, emergence 1/2/3, shared structure (meets level 3 or not), and provenance.
3. Then compare with the declarations, recording each as **match / inflated / understated**.
4. For a no-fusion report: check that each rejection reason is true, and note any defensible fusion the proposer missed.

The key emergence line comes from REQ-001 §3. Emergence 2 means an inherited ability works differently. Emergence 3 means a capability neither parent could reach alone. Inherited abilities placed side by side, such as one parent's effect simply placed under or after the other's, are level 1, which is not a fusion.

Known limitation: the single reviewer has already read both profiles, so the review is only partly blind. Record that limitation; M2 does not engineer around it.

## 5. Q3 — Reproducibility (record completeness)

Model output isn't deterministic, so the standard is that the run is **auditable**, not that it can be regenerated. The run record is written before any parsing and is never edited afterward. Later facts, such as billed cost, go in a separate addendum that references the record's SHA-256.

**Required contents:**

- [ ] repo commit SHA, harness version, UTC timestamps (request sent, response complete)
- [ ] pair, plus the packet bytes and `packet_sha256`
- [ ] the exact model ID string and every request parameter (system prompt text, temperature, max_tokens)
- [ ] the full request body as sent
- [ ] the raw response bytes and their SHA-256
- [ ] API metadata: request ID, stop_reason, input and output tokens
- [ ] **estimated cost**: tokens × per-token rates, with the rates and their source/date recorded
- [ ] **billed cost**: taken from the provider's billing record when it becomes available, in the addendum, marked PENDING until then; estimated and billed cost are never merged into one figure

Any required item missing → the attempt is marked **NOT REPRODUCIBLE**, whatever its other verdicts. Billed cost marked PENDING doesn't count as missing.

**Secrets exclusion:**

- Never persisted: the API key; `x-api-key`, `Authorization`, and any other credential or auth header; cookies; environment variables.
- Request headers are recorded from an **allowlist only** (for example `anthropic-version`, `content-type`), never by copying all headers and then removing sensitive ones.
- Before the record is written, the harness scans it for the configured key value and the provider key prefix. A match **aborts the write and stops the run**; the record is never written in redacted form.

## 6. Attempt counting and retries (declared in advance)

- Any model output counts as the attempt, including refusals and truncation (`stop_reason = max_tokens` is INVALID).
- **Automatic SDK and client retries are disabled** (`max_retries = 0`), so every send is one the harness can see and log.
- **Confirmed no-output failure** → doesn't count; at most 2 manual retries, each logged. This means either:
  - no request was sent (DNS, TLS, or connection refused before the request body was transmitted); or
  - the provider returned an explicit HTTP error response with no completion content.
- **Ambiguous failure → STOP, no retry.** Examples: a timeout after the request was sent, a connection dropped mid-response, a truncated or unparseable stream, or anything else where the provider may have generated output. The record is written with status **AMBIGUOUS**, and the operator decides next steps.
- No re-runs, prompt edits, or best-of-N within M2.

## 7. Declared at authorization (fill in before the run)

| Item | Value |
|---|---|
| Pair | Ilse Marrow × Sable Quillon |
| Model ID | _after API access check_ |
| Temperature / max_tokens | _ _ |
| Spend cap (estimated cost) | _ _ |
| API access verified (date, method, no paid call) | _ _ |
| Authorizing operator act | _reference_ |

**Spend-cap enforcement.** `max_tokens` limits output tokens only; it does not cap total spending. Before sending, the harness computes a conservative upper-bound cost: (input tokens counted for the exact request) × input rate + `max_tokens` × output rate, using the recorded rates. If that bound exceeds the declared spend cap, the harness refuses to send the request. The computed bound is saved in the run record.
