"""
Dashboard null-modality regression — CAUTIONARY entries must not hide the matrix.

Authorized by AUTH-007 (docs/authorizations.md). A CAUTIONARY result carries
`modality: None` (mythos_sync.py build_legacy_profile, Ruling 001 section 4).
server.py persists it into containment_matrix.json, and dashboard.html's
renderGrid() then threw on `f.modality.replace(...)`. loadMatrix() caught every
exception as "No matrix file found", so one CAUTIONARY entry hid the whole
matrix behind a false reason.

This file runs dashboard.html's own <script> under `node` in a vm, with a fake
DOM and an in-memory fetch. Nothing is read from or written to
containment_matrix.json, and nothing here calls save_to_matrix or
export_for_web. The CAUTIONARY fixture is the literal dict that
build_legacy_profile() returns, not a call to it, so these tests do not depend
on which characters are registered.

Standard library only (unittest, subprocess). The external dependency is the
`node` executable, used as a subprocess only: the engine's stdlib-only property
concerns Python imports and is unaffected. If `node` is unavailable these tests
FAIL; they never skip, because a skipped regression test passes vacuously.
"""

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path


DASHBOARD_PATH = Path(__file__).resolve().parent / "dashboard.html"

MISSING_FILE_MESSAGE = "No matrix file found"

NORMAL_ENTRY = {
    "fusion_name": "Normal Alpha x Normal Beta",
    "modality": "GROUNDED",
    "signature_ability": "Test Ability",
    "biome": "Test Biome",
    "audit_log": [],
}

# The exact shape mythos_sync.py build_legacy_profile() returns for CAUTIONARY.
CAUTIONARY_STUB = {
    "fusion_name": "Unregistered Alpha x Normal Beta",
    "state": "CAUTIONARY",
    "modality": None,
}

FORCED_RENDER_ERROR = "forced render failure for AUTH-007 test"

# Runs under node. Reads its scenario from the DASH_SCENARIO environment
# variable and prints one JSON result object to stdout.
NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const scenario = JSON.parse(process.env.DASH_SCENARIO);
const html = fs.readFileSync(process.env.DASH_PATH, 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) { throw new Error('no <script> block found in dashboard.html'); }

// The page ends with a bare top-level loadMatrix() call. Drop it so the test
// controls exactly when loading happens; fail loudly if it is not found.
const trailingCall = /\n\s*loadMatrix\(\);\s*$/;
if (!trailingCall.test(match[1])) { throw new Error('trailing loadMatrix() call not found'); }
const source = match[1].replace(trailingCall, '\n');

const consoleCalls = [];
const fakeConsole = {};
for (const level of ['log', 'info', 'warn', 'error', 'debug']) {
  fakeConsole[level] = (...args) => consoleCalls.push({
    level,
    text: args.map(a => (a && a.message) ? a.message : String(a)).join(' '),
  });
}

const elements = {};
function makeElement(id) {
  const el = {
    id, textContent: '', className: '', style: {}, value: '',
    classList: { add() {}, remove() {}, toggle() {} },
  };
  let inner = '';
  let thrown = false;
  Object.defineProperty(el, 'innerHTML', {
    get() { return inner; },
    set(v) {
      // Forced rendering exception: the first time the grid receives rendered
      // cards, throw. Later assignments (an error message) are allowed.
      if (scenario.mode === 'throw_render' && id === 'matrix-grid'
          && !thrown && String(v).includes('fusion-card')) {
        thrown = true;
        throw new Error(scenario.error);
      }
      inner = String(v);
    },
  });
  return el;
}
const getElement = id => (elements[id] = elements[id] || makeElement(id));

const sandbox = {
  document: {
    getElementById: getElement,
    querySelector: () => getElement('__query'),
    querySelectorAll: () => [],
    addEventListener() {},
  },
  fetch: async () => {
    if (scenario.mode === 'fetch_reject') { throw new TypeError('network down'); }
    if (scenario.mode === 'fetch_notok') {
      return { ok: false, status: 404, json: async () => { throw new Error('no body'); } };
    }
    return { ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(scenario.matrix)) };
  },
  console: fakeConsole,
  Date, Set, Map, Math, JSON, Promise, parseInt, setTimeout,
  alert() {}, confirm() { return true; },
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(source, sandbox);

(async () => {
  let loadError = null;
  try { await sandbox.loadMatrix(); } catch (e) { loadError = String(e && e.message || e); }
  const grid = elements['matrix-grid'] ? elements['matrix-grid'].innerHTML : '';
  process.stdout.write(JSON.stringify({ grid, consoleCalls, loadError }));
})();
"""


def run_dashboard(scenario):
    """Run dashboard.html's script under node for one scenario; return its result dict."""
    env = dict(os.environ)
    env["DASH_SCENARIO"] = json.dumps(scenario)
    env["DASH_PATH"] = str(DASHBOARD_PATH)
    proc = subprocess.run(
        ["node", "-e", NODE_HARNESS],
        env=env, capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    if proc.returncode != 0:
        raise AssertionError(f"node harness failed (exit {proc.returncode}): {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def count_cards(grid_html):
    return grid_html.count('class="fusion-card')


class DashboardNullModalityTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fail, never skip: a skipped regression test passes vacuously.
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the dashboard regression tests and was not found on PATH"
            )

    def test_cautionary_stub_does_not_hide_the_matrix(self):
        """One card per entry, and no false missing-file message."""
        matrix = [NORMAL_ENTRY, CAUTIONARY_STUB]
        result = run_dashboard({"mode": "matrix", "matrix": matrix})
        self.assertNotIn(MISSING_FILE_MESSAGE, result["grid"])
        self.assertEqual(count_cards(result["grid"]), len(matrix))

    def test_rendering_exception_is_not_reported_as_a_missing_file(self):
        """A rendering failure is shown as one, with its message logged, not as a missing file."""
        result = run_dashboard({
            "mode": "throw_render",
            "matrix": [NORMAL_ENTRY],
            "error": FORCED_RENDER_ERROR,
        })
        self.assertNotIn(MISSING_FILE_MESSAGE, result["grid"])
        self.assertRegex(result["grid"], r"(?i)render")
        logged = [c for c in result["consoleCalls"] if FORCED_RENDER_ERROR in c["text"]]
        self.assertTrue(
            logged, f"rendering error message was not logged to the console: {result['consoleCalls']}"
        )

    def test_failed_fetch_still_reports_a_missing_file(self):
        """Both fetch failure modes (rejected, non-OK) keep the missing-file message."""
        for mode in ("fetch_reject", "fetch_notok"):
            with self.subTest(mode=mode):
                result = run_dashboard({"mode": mode, "matrix": []})
                self.assertIn(MISSING_FILE_MESSAGE, result["grid"])


if __name__ == "__main__":
    unittest.main()
