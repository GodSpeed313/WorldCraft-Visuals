"""
IMP-001 M2 mechanical validity (the VALID verdict only). Standard library only.

Implements the REQ-001 section 5 checks named in Protocol Revision 2.1 section 3, reusing
`fusion_synthesis.schema.parse_pair` / `validate_pair` for the pair file. This module never
repairs, rewrites, regenerates or retries output: an output that fails any check is INVALID,
with the failed checks listed.

It makes no judgment about whether a fusion is DEFENSIBLE or CREATIVE. Those verdicts belong
to the operator and are recorded separately by the harness.
"""

from __future__ import annotations

import json
import re
from typing import Optional

from fusion_synthesis.schema import SchemaError, parse_pair, validate_pair

VALID = "VALID"
INVALID = "INVALID"
PROVENANCES = ("defensibly derived", "invented bridge")

PROPOSAL_MARKERS = ("PAIR FILE", "CAUSAL EXPLANATION", "DECLARED LEVELS", "DECLARED PROVENANCE",
                    "LIMITATION SOURCES", "DISCLOSED UNCERTAINTIES")
CAUSAL_LABELS = (("parent_1", r"Parent 1 contribution \(property ids\)"),
                 ("parent_2", r"Parent 2 contribution \(property ids\)"),
                 ("interaction", r"Interaction(?=\s*:)"),
                 ("beyond_either_parent", r"Beyond either parent\?"))

_CANDIDATE_RE = re.compile(r"^\s*CANDIDATE\s+(\d+)\s*:\s*(.*)$", re.IGNORECASE)
_CANDIDATE_BODY_RE = re.compile(
    r"^(?P<mech>.*?);\s*failed\s+tests?(?:\(s\))?\s*:\s*(?P<failed>.*?);\s*property\s+ids\s*:\s*(?P<ids>.*)$",
    re.IGNORECASE | re.DOTALL)
_LEVELS_RE = re.compile(r"shared\s+structure\s*(\d+)\s*;\s*emergence\s*(\d+)", re.IGNORECASE)
_BULLETS = re.escape("-*" + chr(0x2022))      # hyphen, asterisk, bullet; built at run time to keep this file ASCII
_LIMITATION_RE = re.compile(rf"^\s*(?:[{_BULLETS}]\s*)?(?P<lim>.+?)\s*->\s*(?P<src>.+?)\s*$")


def _norm(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


class _Checks:
    def __init__(self):
        self.items: list = []

    def add(self, name: str, passed: bool, detail: str = "") -> bool:
        self.items.append({"name": name, "passed": bool(passed), "detail": detail})
        return bool(passed)

    @property
    def failed(self) -> list:
        return [c["name"] for c in self.items if not c["passed"]]


def _marker_lines(lines: list, name: str) -> list:
    pattern = re.compile(rf"^\s*{re.escape(name)}\s*:(.*)$", re.IGNORECASE)
    return [(i, m.group(1)) for i, line in enumerate(lines) if (m := pattern.match(line))]


def _sections(lines: list, names: tuple) -> Optional[dict]:
    """Each marker must occur exactly once and in the given order; returns {name: section text}."""
    found = {}
    for name in names:
        hits = _marker_lines(lines, name)
        if len(hits) != 1:
            return None
        found[name] = hits[0]
    order = [found[n][0] for n in names]
    if order != sorted(order):
        return None
    starts = order + [len(lines)]
    out = {}
    for pos, name in enumerate(names):
        body = [found[name][1]] + lines[starts[pos] + 1:starts[pos + 1]]
        out[name] = "\n".join(l for l in body if not l.strip().startswith("---")).strip()
    return out


def _labelled(text: str, labels: tuple) -> dict:
    """Split a block into labelled sub-fields; a label's value runs to the next label."""
    marks = []
    for key, pattern in labels:
        m = re.search(rf"^\s*{pattern}\s*:?(.*)$", text, re.IGNORECASE | re.MULTILINE)
        if m:
            marks.append((m.start(), m.start(1), key))
    marks.sort()
    out = {}
    for n, (start, value_start, key) in enumerate(marks):
        end = marks[n + 1][0] if n + 1 < len(marks) else len(text)
        out[key] = text[value_start:end].strip()
    return out


def _json_from_block(block: str):
    body = block.strip()
    fence = re.match(r"^```[A-Za-z]*\s*\n(.*?)\n?```$", body, re.DOTALL)
    if fence:
        body = fence.group(1).strip()
    value, end = json.JSONDecoder().raw_decode(body)
    if body[end:].strip():
        raise ValueError("text follows the JSON pair file")
    return value


def validate_output(text: str, card_a, card_b, stop_reason: Optional[str]) -> dict:
    """Mechanical validity of one proposer output. `card_a`/`card_b` are the two parsed CharacterCards."""
    checks = _Checks()
    props = {p.id: ("A" if p in card_a.properties else "B") for p in (*card_a.properties, *card_b.properties)}
    id_re = re.compile(rf"(?<![A-Za-z0-9_.])(?:{re.escape(card_a.slug)}|{re.escape(card_b.slug)})\.[A-Za-z0-9_]+")

    def ids_in(s: str) -> tuple:
        found = id_re.findall(s)
        return [i for i in found if i in props], [i for i in found if i not in props]

    checks.add("complete_output", stop_reason == "end_turn", f"stop_reason={stop_reason!r}; only 'end_turn' is a complete output")

    lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    first = next((l for l in lines if l.strip()), "")
    head = re.match(r"^OUTCOME:\s*(proposal|no-fusion)\s*$", first.strip(), re.IGNORECASE)
    if not head:
        checks.add("template_structure", False, "the first non-empty line must be 'OUTCOME: proposal' or 'OUTCOME: no-fusion'")
        return _result(checks, None, None)
    kind = head.group(1).lower()
    has_proposal = any(_marker_lines(lines, m) for m in PROPOSAL_MARKERS)
    has_nofusion = bool(_marker_lines(lines, "STATEMENT")) or any(_CANDIDATE_RE.match(l) for l in lines)
    if not checks.add("single_output_type", not (has_proposal and has_nofusion),
                      "the text contains both proposal and no-fusion sections; exactly one output is allowed"):
        return _result(checks, kind, None)

    parsed = _proposal(lines, card_a, card_b, checks, ids_in, props) if kind == "proposal" else _no_fusion(lines, checks, ids_in)
    return _result(checks, kind, parsed)


def _result(checks: _Checks, kind: Optional[str], parsed: Optional[dict]) -> dict:
    failed = checks.failed
    return {"verdict": INVALID if failed else VALID, "outcome_type": kind, "checks": checks.items,
            "failed_checks": failed, "parsed": None if failed else parsed}


# --- proposal -----------------------------------------------------------------

def _proposal(lines, card_a, card_b, checks, ids_in, props) -> Optional[dict]:
    sec = _sections(lines, PROPOSAL_MARKERS)
    if not checks.add("template_structure", sec is not None,
                      "every proposal heading must appear exactly once, in template order: " + "; ".join(PROPOSAL_MARKERS)):
        return None

    parsed = {"pair_file": None, "causal_explanation": {}, "declared_levels": {}, "declared_provenance": None,
              "limitation_sources": [], "disclosed_uncertainties": sec["DISCLOSED UNCERTAINTIES"]}

    # pair file: parse, schema, cross-validation against the two character cards
    pair = None
    raw = None
    try:
        raw = _json_from_block(sec["PAIR FILE"])
        checks.add("pair_file_parses", isinstance(raw, dict), "the pair file must be one JSON object")
    except (ValueError, json.JSONDecodeError) as exc:
        checks.add("pair_file_parses", False, f"pair file is not valid JSON: {exc}")
    if isinstance(raw, dict):
        parsed["pair_file"] = raw
        try:
            pair = parse_pair(raw, "proposed pair file")
            checks.add("pair_file_schema", True)
        except SchemaError as exc:
            checks.add("pair_file_schema", False, str(exc))
    if pair is not None:
        by_name = {card_a.name: card_a, card_b.name: card_b}
        if pair.a in by_name and pair.b in by_name and pair.a != pair.b:
            try:
                validate_pair(pair, by_name[pair.a], by_name[pair.b])
                checks.add("pair_file_cross_validation", True)
            except SchemaError as exc:
                checks.add("pair_file_cross_validation", False, str(exc))
        else:
            checks.add("pair_file_cross_validation", False, f"pair file names {pair.a!r}/{pair.b!r} are not exactly the two packet characters")
        deps = set(pair.interaction.dependency_ids)
        side_a = any(props.get(d) == "A" for d in deps)
        side_b = any(props.get(d) == "B" for d in deps)
        checks.add("interaction_depends_on_both_parents", side_a and side_b,
                   "interaction.dependency_ids must include at least one property from each parent")
        covered = {o.property_id for o in pair.trait_outcomes}
        missing = sorted(set(props) - covered)
        checks.add("trait_outcomes_cover_all_properties", not missing and len(covered) == len(pair.trait_outcomes),
                   f"missing: {missing}" if missing else "each property exactly once")

    # causal explanation: valid property ids, both parents cited
    causal = _labelled(sec["CAUSAL EXPLANATION"], CAUSAL_LABELS)
    parsed["causal_explanation"] = causal
    have = all(causal.get(k) for k, _ in CAUSAL_LABELS)
    checks.add("causal_explanation_complete", have, "Parent 1, Parent 2, Interaction and Beyond-either-parent must all be filled in")
    p1, bad1 = ids_in(causal.get("parent_1", ""))
    p2, bad2 = ids_in(causal.get("parent_2", ""))
    checks.add("parent_contributions_cite_valid_ids", bool(p1) and bool(p2) and not bad1 and not bad2,
               f"unknown ids: {sorted(set(bad1 + bad2))}" if bad1 or bad2 else "each contribution must cite at least one property id")
    cited = set(p1 + p2)
    checks.add("citations_from_both_parents", any(props[i] == "A" for i in cited) and any(props[i] == "B" for i in cited),
               "the cited property ids must include at least one from each parent")

    # declared levels and provenance
    lv = _LEVELS_RE.search(sec["DECLARED LEVELS"])
    shared, emergence = (int(lv.group(1)), int(lv.group(2))) if lv else (None, None)
    parsed["declared_levels"] = {"shared_structure": shared, "emergence": emergence}
    checks.add("declared_levels_present", lv is not None and shared in (1, 2, 3) and emergence in (2, 3),
               "need 'shared structure <1-3>; emergence <2|3>'")
    prov = _norm(sec["DECLARED PROVENANCE"])
    parsed["declared_provenance"] = sec["DECLARED PROVENANCE"].strip()
    checks.add("provenance_declared", prov in PROVENANCES, "must be 'Defensibly Derived' or 'Invented Bridge'")
    checks.add("disclosed_uncertainties_present", bool(sec["DISCLOSED UNCERTAINTIES"].strip()), "write 'none' if there are none")

    # every limitation carries a source
    entries = []
    for line in sec["LIMITATION SOURCES"].split("\n"):
        m = _LIMITATION_RE.match(line)
        if m:
            entries.append({"limitation": m.group("lim"), "source": m.group("src")})
    parsed["limitation_sources"] = entries
    _, bad_src = ids_in(" ".join(e["source"] for e in entries))
    unmatched = []
    if pair is not None:
        for limitation in pair.emergent.limitations:
            n = _norm(limitation)
            if not any(_norm(e["limitation"]) == n or (len(n) >= 10 and (n in _norm(e["limitation"]) or _norm(e["limitation"]) in n))
                       for e in entries):
                unmatched.append(limitation)
    checks.add("limitations_sourced", pair is not None and not unmatched and not bad_src and bool(entries),
               (f"limitations with no 'limitation -> source' line: {unmatched}" if unmatched else "")
               + (f" unknown property ids in sources: {sorted(set(bad_src))}" if bad_src else "")
               or "every emergent-ability limitation needs a 'limitation -> source' line")
    return parsed


# --- no-fusion ----------------------------------------------------------------

def _no_fusion(lines, checks, ids_in) -> Optional[dict]:
    statement = _marker_lines(lines, "STATEMENT")
    ok_statement = len(statement) == 1 and _norm(statement[0][1]) == "no defensible fusion found"
    if not checks.add("template_structure", ok_statement, "need exactly one 'STATEMENT: no defensible fusion found'"):
        return None

    candidates = []
    for i, line in enumerate(lines):
        m = _CANDIDATE_RE.match(line)
        if m:
            body = m.group(2)
            j = i + 1
            while j < len(lines) and not (_CANDIDATE_RE.match(lines[j]) or _marker_lines([lines[j]], "FEWER THAN THREE BECAUSE")
                                          or lines[j].strip().startswith("---")):
                body += "\n" + lines[j]
                j += 1
            candidates.append((int(m.group(1)), body.strip()))
    numbers = [n for n, _ in candidates]
    checks.add("candidate_count_and_numbering", 1 <= len(candidates) <= 3 and numbers == list(range(1, len(candidates) + 1)),
               f"need 1-3 candidates numbered 1..n in order; got {numbers}")

    parsed_c, rejected_ok, ids_ok, details = [], True, True, []
    for n, body in candidates:
        m = _CANDIDATE_BODY_RE.match(body)
        if not m:
            rejected_ok = ids_ok = False
            details.append(f"candidate {n}: need '<mechanism>; failed test(s): <...>; property ids: <...>'")
            continue
        mech, failed, ids = m.group("mech").strip(), m.group("failed").strip(), m.group("ids").strip()
        good, bad = ids_in(ids)
        if not mech or not failed:
            rejected_ok = False
            details.append(f"candidate {n}: mechanism and failed test(s) must both be stated")
        if not good or bad:
            ids_ok = False
            details.append(f"candidate {n}: property ids must be real and non-empty (unknown: {sorted(set(bad))})")
        parsed_c.append({"candidate": n, "mechanism": mech, "failed_tests": failed, "property_ids": good})
    checks.add("candidates_each_rejected", rejected_ok and bool(candidates), "; ".join(details))
    checks.add("candidate_property_ids_valid", ids_ok and bool(candidates), "; ".join(details))
    norms = [_norm(c["mechanism"]) for c in parsed_c]
    checks.add("candidates_distinct", len(set(norms)) == len(norms), "candidate mechanisms must not be restatements of identical text")

    fewer = _marker_lines(lines, "FEWER THAN THREE BECAUSE")
    explained = bool(fewer) and bool(fewer[0][1].strip() or any(l.strip() for l in lines[fewer[0][0] + 1:]))
    checks.add("fewer_than_three_explained", len(candidates) >= 3 or explained, "fewer than three candidates need 'FEWER THAN THREE BECAUSE: ...'")
    return {"statement": "no defensible fusion found", "candidates": parsed_c,
            "fewer_than_three_because": fewer[0][1].strip() if fewer else None}


# --- reproducibility (Q3) -----------------------------------------------------

BASE_REQUIRED = ("repo_commit_sha", "harness_version", "request_sent_utc", "pair", "packet_sha256", "packet_bytes_file",
                 "model_id", "request_parameters", "request_body_sha256", "estimated_cost", "billed_cost_addendum",
                 "attempt_history", "retry_policy", "reservation")
RESPONSE_REQUIRED = ("response_complete_utc", "raw_response_sha256", "provider_request_id", "stop_reason",
                     "usage_input_tokens", "usage_output_tokens")


def assess_reproducibility(record: dict, status: str) -> dict:
    """REPRODUCIBLE unless a required audit field is absent. A PENDING billed cost is not absence."""
    required = BASE_REQUIRED + (RESPONSE_REQUIRED if status == "COMPLETE" else ())
    if status == "NO_OUTPUT_PRE_TRANSMISSION_EXHAUSTED":      # nothing was ever sent, so there is no send time
        required = tuple(k for k in required if k != "request_sent_utc")
    missing = [k for k in required if record.get(k) in (None, "", {}, [])]
    return {"verdict": "NOT REPRODUCIBLE" if missing else "REPRODUCIBLE", "missing_fields": missing}


__all__ = ["INVALID", "VALID", "assess_reproducibility", "validate_output"]
