"""
Dashboard openCase() regression: the case-file modal must escape matrix text,
tolerate non-string modality without side effects, restrict modality class
tokens to an allowlist, render unknown parent modalities neutrally, and bound
dominance to 0-100.

Authorized by AUTH-010 (docs/authorizations.md). openCase() interpolated every
matrix-derived field into modal HTML unescaped, dereferenced `f.modality`
before checking it, passed any modality value into a class attribute, and
used the dominance value in a style and in labels without bounding it.

This file is self-contained: it runs dashboard.html's own <script> under
`node` in a vm with a fake DOM and an in-memory fetch, and does not import or
modify any other test file. The fake DOM provides the four elements openCase()
touches:

  modal-title   textContent
  modal-badge   textContent, className
  modal-body    innerHTML
  case-overlay  classList (add/remove are recorded, not applied)

Each element is pre-filled with a sentinel so that a partial mutation by an
early-return path is visible as a before/after difference. Entries enter
through the unchanged loadMatrix(); a case may then override a field on the
loaded entry (bypassing loadMatrix()'s own normalisation) before openCase(i)
is called. Nothing here calls save_to_matrix or export_for_web, and nothing
reads or writes containment_matrix.json. Fixtures are literal dicts.

Standard library only; `node` is a subprocess. If `node` is unavailable these
tests FAIL; they never skip, because a skipped regression test passes
vacuously.
"""

import copy
import html
import json
import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path


DASHBOARD_PATH = Path(__file__).resolve().parent / "dashboard.html"

HOSTILE = "<img src=x onerror=alert(1)>&\"'"

VALID_MODALITIES = ("LEGACY", "GROUNDED", "HIGH_CONCEPT")

# Runs under node. Reads a JSON list of cases from stdin and prints a JSON list
# of results. Each case gets a fresh vm context and fresh fake elements.
NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const cases = JSON.parse(fs.readFileSync(0, 'utf8'));
const html = fs.readFileSync(process.env.DASH_PATH, 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) { throw new Error('no <script> block found in dashboard.html'); }

// The page ends with a bare top-level loadMatrix() call. Drop it so the test
// controls when loading happens; fail loudly if it is not found.
const trailingCall = /\n\s*loadMatrix\(\);\s*$/;
if (!trailingCall.test(match[1])) { throw new Error('trailing loadMatrix() call not found'); }
const script = new vm.Script(match[1].replace(trailingCall, '\n'));

const SENTINEL = {
  title: 'SENTINEL-TITLE', badge: 'SENTINEL-BADGE',
  cls: 'SENTINEL-CLASS', body: 'SENTINEL-BODY',
};

async function runCase(c) {
  const els = {};
  function el(id) {
    if (!els[id]) {
      const e = { id, textContent: '', className: '', innerHTML: '', style: {}, value: '', ops: [] };
      e.classList = {
        add(n) { e.ops.push(['add', n]); },
        remove(n) { e.ops.push(['remove', n]); },
        toggle() {},
      };
      els[id] = e;
    }
    return els[id];
  }
  el('modal-title').textContent = SENTINEL.title;
  el('modal-badge').textContent = SENTINEL.badge;
  el('modal-badge').className = SENTINEL.cls;
  el('modal-body').innerHTML = SENTINEL.body;

  const quiet = () => {};
  const sandbox = {
    document: {
      getElementById: el,
      querySelector: () => el('__query'),
      querySelectorAll: () => [],
      addEventListener() {},
    },
    fetch: async () => ({ ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(c.matrix)) }),
    console: { log: quiet, info: quiet, warn: quiet, error: quiet, debug: quiet },
    setTimeout,
    alert() {}, confirm() { return true; },
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  script.runInContext(sandbox);
  await sandbox.loadMatrix();

  // Overrides run inside the page's own context, after loadMatrix() has
  // normalised the matrix, so a value can be set that loadMatrix() would
  // otherwise have replaced (NaN, a non-string modality, ...).
  for (const [i, field, js] of (c.overrides || [])) {
    vm.runInContext(`MATRIX[${i}].${field} = ${js};`, sandbox);
  }

  const snap = () => ({
    title: el('modal-title').textContent,
    badgeText: el('modal-badge').textContent,
    badgeClass: el('modal-badge').className,
    body: el('modal-body').innerHTML,
    overlayOps: el('case-overlay').ops.slice(),
  });
  const before = snap();
  let error = null;
  try { sandbox.openCase(c.open); } catch (e) { error = String((e && e.message) || e); }
  return { before, after: snap(), error };
}

(async () => {
  const results = [];
  for (const c of cases) { results.push(await runCase(c)); }
  process.stdout.write(JSON.stringify(results));
})();
"""


def run_cases(cases):
    """Run each case under node; return one result dict per case."""
    env = dict(os.environ)
    env["DASH_PATH"] = str(DASHBOARD_PATH)
    proc = subprocess.run(
        ["node", "-e", NODE_HARNESS],
        input=json.dumps(cases), env=env,
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    if proc.returncode != 0:
        raise AssertionError(f"node harness failed (exit {proc.returncode}): {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def run_one(case):
    return run_cases([case])[0]


def full_entry():
    """A benign entry that exercises every section and every audit status."""
    return {
        "id": "MSF-001",
        "fusion_name": "Malcolm X x Vash",
        "modality": "GROUNDED",
        "dominant": "balanced blend",
        "alpha": {"name": "Malcolm X", "modality": "LEGACY"},
        "beta": {"name": "Vash", "modality": "HIGH_CONCEPT"},
        "dominance": 60,
        "tags": ["rhetoric", "pacifist"],
        "biome": "Dust Plains",
        "approved_powers": ["Oratory", "Quick Draw"],
        "signature_ability": "Oratory",
        "influence_pattern": "rally the crowd",
        "rhetorical_style": "Rhetoric & Legacy",
        "lore_summary": "Where two legends collide.",
        "engine_version": "v3.0",
        "created_at": "2026-10-30 12:00:00",
        "audit_log": [
            {"power": "Reality Warp", "status": "transposed", "transposed_to": "Illusion",
             "cost": "high", "reason": "R-transposed"},
            {"power": "Mystery Power", "status": "unverified", "transposed_to": None,
             "cost": "?", "reason": "R-unverified"},
            {"power": "Time Stop", "status": "grounding_unavailable", "transposed_to": None,
             "cost": None, "reason": "R-halted", "unavailable_cause": "no_legal_equivalent"},
            {"power": "Oratory", "status": "approved", "transposed_to": None,
             "cost": "low", "reason": None},
        ],
    }


def set_path(obj, path, value):
    for key in path[:-1]:
        obj = obj[key]
    obj[path[-1]] = value


def visible_text(fragment):
    stripped = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(html.unescape(stripped).split())


# Every matrix-derived value openCase() interpolates into HTML.
HOSTILE_FIELDS = (
    ("alpha.name", ("alpha", "name")),
    ("beta.name", ("beta", "name")),
    ("transposed.power", ("audit_log", 0, "power")),
    ("transposed.transposed_to", ("audit_log", 0, "transposed_to")),
    ("transposed.cost", ("audit_log", 0, "cost")),
    ("transposed.reason", ("audit_log", 0, "reason")),
    ("unverified.power", ("audit_log", 1, "power")),
    ("unverified.cost", ("audit_log", 1, "cost")),
    ("unverified.reason", ("audit_log", 1, "reason")),
    ("halted.power", ("audit_log", 2, "power")),
    ("halted.reason", ("audit_log", 2, "reason")),
    ("approved.power", ("audit_log", 3, "power")),
    ("approved.cost", ("audit_log", 3, "cost")),
    ("lore_summary", ("lore_summary",)),
    ("approved_powers[0]", ("approved_powers", 0)),
    ("influence_pattern", ("influence_pattern",)),
    ("rhetorical_style", ("rhetorical_style",)),
    ("tags[0]", ("tags", 0)),
    ("id", ("id",)),
    ("engine_version", ("engine_version",)),
    ("created_at", ("created_at",)),
    ("biome", ("biome",)),
    ("dominant", ("dominant",)),
)

PILL = re.compile(
    r'<span class="src-pill" style="(?P<style>[^"]*)">\s*'
    r'<span class="dot" style="(?P<dot>[^"]*)"></span>\s*'
    r'(?P<label>.*?)\s*</span>',
    re.S,
)
DOM_FILL = re.compile(r'<div class="dom-fill" style="width:(?P<w>[^"]*)%"></div>')
DOM_PCTS = re.compile(r'<div class="dom-pcts"><span>(?P<a>.*?)%</span><span>(?P<b>.*?)%</span></div>')
ROW_REASON = '<p class="audit-reason">'
NUMBER = re.compile(r"^\d+(\.\d+)?$")

OVERLAY_OPENED = [["add", "open"]]


class OpenCaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fail, never skip: a skipped regression test passes vacuously.
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the dashboard regression tests and was not found on PATH"
            )

    # ---- AC1: escaping ----------------------------------------------------

    def test_every_interpolated_field_renders_as_text(self):
        cases = []
        for label, path in HOSTILE_FIELDS:
            token = f"TOKEN_{label}"
            for value in (token, HOSTILE):
                entry = full_entry()
                set_path(entry, path, value)
                cases.append({"matrix": [entry], "open": 0})
        results = run_cases(cases)
        for n, (label, _path) in enumerate(HOSTILE_FIELDS):
            benign, hostile = results[2 * n], results[2 * n + 1]
            with self.subTest(field=label):
                self.assertIsNone(benign["error"])
                self.assertIsNone(hostile["error"])
                # Non-vacuity: the field is rendered at all.
                self.assertIn(f"TOKEN_{label}", benign["after"]["body"])
                body = hostile["after"]["body"]
                self.assertNotIn("<img", body)
                self.assertIn("&lt;img src=x onerror=alert(1)&gt;", body)
                self.assertIn(HOSTILE, html.unescape(body))

    # ---- AC2: guard -------------------------------------------------------

    def test_missing_entry_or_non_string_modality_returns_without_mutation(self):
        scenarios = {
            "missing entry": {"matrix": [full_entry()], "open": 99},
            "null": {"matrix": [dict(full_entry(), modality=None)], "open": 0},
            "CAUTIONARY stub": {
                "matrix": [{"fusion_name": "Unregistered Alpha x Vash",
                            "state": "CAUTIONARY", "modality": None}],
                "open": 0,
            },
            "undefined": {"matrix": [full_entry()], "open": 0,
                          "overrides": [[0, "modality", "undefined"]]},
            "number": {"matrix": [full_entry()], "open": 0,
                       "overrides": [[0, "modality", "5"]]},
            "object": {"matrix": [full_entry()], "open": 0,
                       "overrides": [[0, "modality", "{}"]]},
            "array": {"matrix": [full_entry()], "open": 0,
                      "overrides": [[0, "modality", "[]"]]},
        }
        names = list(scenarios)
        results = run_cases([scenarios[n] for n in names])
        for name, result in zip(names, results):
            with self.subTest(modality=name):
                self.assertIsNone(result["error"])
                self.assertEqual(result["after"], result["before"])
                self.assertEqual(result["after"]["overlayOps"], [])

    # ---- AC3: valid badges ------------------------------------------------

    def test_valid_modalities_keep_their_badge_class_and_text(self):
        results = run_cases([
            {"matrix": [dict(full_entry(), modality=m)], "open": 0} for m in VALID_MODALITIES
        ])
        for modality, result in zip(VALID_MODALITIES, results):
            with self.subTest(modality=modality):
                self.assertIsNone(result["error"])
                self.assertEqual(result["after"]["badgeClass"], f"card-badge {modality}")
                self.assertEqual(result["after"]["badgeText"], modality.replace("_", " "))
                self.assertEqual(result["after"]["overlayOps"], OVERLAY_OPENED)

    # ---- AC4: class allowlist (string inputs only) ------------------------

    def test_unknown_string_modality_gets_no_class_token_and_raw_text(self):
        values = (
            "FOO", "FOO_BAR", "legacy", "", "GROUNDED extra",
            'GROUNDED" onmouseover="x', "__proto__", "constructor", "toString",
            HOSTILE,
        )
        results = run_cases([
            {"matrix": [dict(full_entry(), modality=v)], "open": 0} for v in values
        ])
        for value, result in zip(values, results):
            with self.subTest(modality=value):
                self.assertIsNone(result["error"])
                # The class token set is exactly {card-badge}: no modality token
                # and no token taken from the value.
                self.assertEqual(result["after"]["badgeClass"].split(), ["card-badge"])
                # Shown raw through textContent (no underscore substitution).
                self.assertEqual(result["after"]["badgeText"], value)
                self.assertEqual(result["after"]["overlayOps"], OVERLAY_OPENED)

    # ---- AC5: reasons -----------------------------------------------------

    def test_reason_presence_is_unchanged(self):
        def entry_with_reasons(values):
            e = full_entry()
            for row, value in zip(e["audit_log"][:3], values):
                row["reason"] = value
            return e

        absent = ((None, None, None), ("", "", ""), (0, 0, 0))
        cases = [{"matrix": [entry_with_reasons(v)], "open": 0} for v in absent]
        # An undefined reason: drop the key rather than set it.
        e = full_entry()
        for row in e["audit_log"][:3]:
            del row["reason"]
        cases.append({"matrix": [e], "open": 0})
        # Present reasons, one hostile, and a non-empty reason on the approved row.
        present = full_entry()
        present["audit_log"][0]["reason"] = HOSTILE
        present["audit_log"][3]["reason"] = "R-approved-ignored"
        cases.append({"matrix": [present], "open": 0})
        results = run_cases(cases)

        for result in results[:4]:
            self.assertIsNone(result["error"])
            self.assertEqual(result["after"]["body"].count(ROW_REASON), 0)
        with_reasons = results[4]
        self.assertIsNone(with_reasons["error"])
        body = with_reasons["after"]["body"]
        # One row paragraph per transposed/unverified/halted row; the approved
        # row has never rendered a reason.
        self.assertEqual(body.count(ROW_REASON), 3)
        self.assertNotIn("R-approved-ignored", body)
        self.assertIn("R-unverified", body)
        self.assertIn("R-halted", body)
        self.assertNotIn("<img", body)
        self.assertIn(HOSTILE, html.unescape(body))

    # ---- AC6: dominance ---------------------------------------------------

    def test_dominance_is_numeric_and_clamped(self):
        # (label, JS literal applied after loadMatrix(), expected width)
        overridden = (
            ("negative", "-10", 0),
            ("over 100", "150", 100),
            ("numeric string", '"70"', 70),
            ("fractional, not rounded", "42.5", 42.5),
            ("NaN", "NaN", 50),
            ("Infinity", "Infinity", 50),
            ("-Infinity", "-Infinity", 50),
            ("null", "null", 50),
            ("non-numeric string", '"abc"', 50),
            ("object", "{}", 50),
        )
        cases = [
            {"matrix": [full_entry()], "open": 0, "overrides": [[0, "dominance", js]]}
            for _label, js, _expected in overridden
        ]
        # Already normalised by loadMatrix() before openCase() runs: null and
        # 0 are falsy, so `if (!f.dominance) f.dominance = 50` replaces them.
        normalised = ((None, 50), (0, 50))
        cases += [
            {"matrix": [dict(full_entry(), dominance=v)], "open": 0} for v, _e in normalised
        ]
        results = run_cases(cases)

        labelled = [(label, expected) for label, _js, expected in overridden]
        labelled += [(f"normalised by loadMatrix: {v!r}", expected) for v, expected in normalised]
        for (label, expected), result in zip(labelled, results):
            with self.subTest(dominance=label):
                self.assertIsNone(result["error"])
                body = result["after"]["body"]
                fill = DOM_FILL.search(body)
                pcts = DOM_PCTS.search(body)
                self.assertIsNotNone(fill)
                self.assertIsNotNone(pcts)
                for text in (fill.group("w"), pcts.group("a"), pcts.group("b")):
                    self.assertRegex(text, NUMBER)
                self.assertEqual(float(fill.group("w")), expected)
                self.assertEqual(float(pcts.group("a")), expected)
                self.assertEqual(float(pcts.group("b")), 100 - expected)

    # ---- AC7: normal rendering --------------------------------------------

    def test_normal_case_file_renders_intact(self):
        result = run_one({"matrix": [full_entry()], "open": 0})
        self.assertIsNone(result["error"])
        after = result["after"]
        self.assertEqual(after["title"], "Malcolm X x Vash")
        self.assertEqual(after["badgeText"], "GROUNDED")
        self.assertEqual(after["badgeClass"], "card-badge GROUNDED")
        self.assertEqual(after["overlayOps"], OVERLAY_OPENED)
        body = after["body"]
        for title in ("01 — Audit Trail", "02 — Legacy Profile", "03 — Sync Status"):
            self.assertIn(title, body)
        self.assertIn('<span class="power-pill sig">Oratory ★</span>', body)
        self.assertIn('<span class="power-pill">Quick Draw</span>', body)
        self.assertEqual(visible_text(body), NORMAL_VISIBLE_TEXT)

    # ---- AC8: parent pills ------------------------------------------------

    def test_valid_parents_render_exactly_as_before(self):
        result = run_one({"matrix": [full_entry()], "open": 0})
        pills = list(PILL.finditer(result["after"]["body"]))
        self.assertEqual(len(pills), 2)
        expected = (
            ("Malcolm X · LEGACY", "legacy"),
            ("Vash · HIGH_CONCEPT", "high"),
        )
        for pill, (label, token) in zip(pills, expected):
            self.assertEqual(html.unescape(pill.group("label")), label)
            self.assertEqual(
                pill.group("style"),
                f"background:var(--{token}-bg);color:var(--{token});border:0.5px solid var(--{token}-bd);",
            )
            self.assertEqual(pill.group("dot"), f"background:var(--{token});")

    def test_unresolved_parent_modality_renders_a_neutral_pill(self):
        # Fusion modality is GROUNDED; a missing or unknown parent modality
        # must not inherit it and must not default to HIGH_CONCEPT.
        parents = {
            "null": {"name": "Malcolm X", "modality": None},
            "missing key": {"name": "Malcolm X"},
            "unknown string": {"name": "Malcolm X", "modality": "FOO"},
            "non-string": {"name": "Malcolm X", "modality": 5},
            "hostile": {"name": "Malcolm X", "modality": HOSTILE},
        }
        names = list(parents)
        cases = []
        for name in names:
            entry = full_entry()
            entry["alpha"] = parents[name]
            cases.append({"matrix": [entry], "open": 0})
        results = run_cases(cases)
        for name, result in zip(names, results):
            with self.subTest(parent=name):
                self.assertIsNone(result["error"])
                body = result["after"]["body"]
                self.assertNotIn("<img", body)
                pills = list(PILL.finditer(body))
                self.assertEqual(len(pills), 2)
                alpha = pills[0]
                self.assertEqual(html.unescape(alpha.group("label")), "Malcolm X · —")
                for text in (alpha.group("style"), alpha.group("dot")):
                    self.assertIn("var(--muted)", text)
                    for forbidden in ("--high", "--ground", "--legacy"):
                        self.assertNotIn(forbidden, text)
                # The other parent is unaffected.
                self.assertEqual(html.unescape(pills[1].group("label")), "Vash · HIGH_CONCEPT")


# Captured from the unmodified openCase() on the baseline (67af9ef) for
# full_entry(), then reviewed by eye: AC7 pins that benign output is unchanged.
NORMAL_VISIBLE_TEXT = (
    "01 — Audit Trail Malcolm X · LEGACY + Vash · HIGH_CONCEPT Dominance calibration "
    "Malcolm X Vash 60% 40% Grounding filter log Reality Warp → transposed to Illusion "
    "R-transposed cost high Mystery Power unverified — not in the Power Registry "
    "R-unverified cost ? Time Stop grounding unavailable — halted, not transposed "
    "R-halted — Oratory cost low 1 power(s) could not be verified against the Power "
    "Registry. Not an approval. 1 power(s) had grounding unavailable — halted, not an "
    "approval or a transposition. 02 — Legacy Profile Lore summary Where two legends "
    "collide. Approved powers Oratory ★ Quick Draw Influence pattern "
    "\"rally the crowd\" Rhetorical style Rhetoric & Legacy Tags rhetoric pacifist "
    "03 — Sync Status Fusion ID MSF-001 Engine v3.0 Created 2026-10-30 12:00:00 "
    "Biome Dust Plains Dominant balanced blend Transpositions 1"
)


if __name__ == "__main__":
    unittest.main()
