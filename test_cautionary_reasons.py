"""
CAUTIONARY reasons regression — a CAUTIONARY fusion must carry its reasons.

Authorized by AUTH-012 (docs/authorizations.md). Contract 001 section 5.1 and
Contract 003 I5 require that a CAUTIONARY result's reason travel with the
result. classify_fusion() returns a `reasons` list (one string per
unregistered input, alpha first), build_legacy_profile() carries it, the
server persists and serves it, and dashboard.html renders each string on its
own line in the null-modality card.

This file is self-contained. Every expected value below is a literal written
here, never a value produced by the code under test. Engine and server checks
run in a subprocess whose working directory is an isolated temporary directory
outside the repository, so the repository's containment_matrix.json is never
read for writing; its SHA-256 is asserted unchanged around every such run.
The dashboard is run under `node` in a vm with a fake DOM and an in-memory
fetch, as in test_dashboard_null_modality.py.

Standard library only (unittest, subprocess, http.client). The external
dependency is the `node` executable, used as a subprocess only. If `node` is
unavailable these tests FAIL; they never skip, because a skipped regression
test passes vacuously.
"""

import hashlib
import html
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = str(Path(__file__).resolve().parent)
DASHBOARD_PATH = os.path.join(REPO, "dashboard.html")
REAL_MATRIX = os.path.join(REPO, "containment_matrix.json")

HOSTILE = "<img src=x onerror=alert(1)>&\"'"
HOSTILE_ESCAPED = "&lt;img src=x onerror=alert(1)&gt;&amp;&quot;&#39;"

# ----------------------------------------------------------------------------
# Python probe: runs in a subprocess with an isolated working directory.
# ----------------------------------------------------------------------------
_DRIVER = r'''
import contextlib, io, json, os, sys
repo = sys.argv[1]
cwd = os.path.normcase(os.path.realpath(os.getcwd()))
rp = os.path.normcase(os.path.realpath(repo))
if cwd == rp or cwd.startswith(rp + os.sep):
    raise SystemExit("probe must not run inside the repository")
sys.path.insert(0, repo)
import modality_classifier, mythos_sync
sc = json.loads(os.environ["PROBE_SCENARIO"])
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    if sc["op"] == "fusion":
        out = modality_classifier.classify_fusion(sc["alpha"], sc["beta"], sc.get("dominance", 50))
    elif sc["op"] == "profile":
        out = mythos_sync.build_legacy_profile(sc["alpha"], sc["beta"], sc.get("dominance", 50))
    elif sc["op"] == "persist":
        p = mythos_sync.build_legacy_profile(sc["alpha"], sc["beta"], sc.get("dominance", 50))
        mythos_sync.save_to_matrix(p)
        mythos_sync.export_for_web()
        with open("containment_matrix.json", encoding="utf-8") as f:
            out = json.load(f)
    else:
        raise SystemExit("unknown op")
sys.stdout.write(json.dumps(out))
'''

_SERVER_DRIVER = r'''
import json, os, sys
repo = sys.argv[1]
cwd = os.path.normcase(os.path.realpath(os.getcwd()))
rp = os.path.normcase(os.path.realpath(repo))
if cwd == rp or cwd.startswith(rp + os.sep):
    raise SystemExit("server must not run inside the repository")
sys.path.insert(0, repo)
import server
srv = server.make_server("127.0.0.1", 0)
print(json.dumps(srv.socket.getsockname()[1]), flush=True)
srv.serve_forever()
'''


def _real_matrix_state():
    try:
        with open(REAL_MATRIX, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None


class IsolatedCase(unittest.TestCase):
    """Base: an isolated temp working directory and an untouched-real-matrix guard."""

    @classmethod
    def setUpClass(cls):
        # Fail, never skip: a skipped regression test passes vacuously.
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the CAUTIONARY reasons tests and was not found on PATH"
            )

    def setUp(self):
        before = _real_matrix_state()
        self.addCleanup(lambda: self.assertEqual(
            before, _real_matrix_state(), "the repository's containment_matrix.json changed"))
        tmp = tempfile.TemporaryDirectory(prefix="auth012_", ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name
        rp = os.path.normcase(os.path.realpath(REPO))
        tp = os.path.normcase(os.path.realpath(self.root))
        self.assertFalse(tp == rp or tp.startswith(rp + os.sep),
                         "temporary directory must be outside the repository")

    def probe(self, **scenario):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8",
                   PROBE_SCENARIO=json.dumps(scenario))
        proc = subprocess.run([sys.executable, "-B", "-c", _DRIVER, REPO],
                              cwd=self.root, env=env, capture_output=True,
                              text=True, encoding="utf-8", timeout=60)
        if proc.returncode != 0:
            raise AssertionError("probe failed (exit %d): %s" % (proc.returncode, proc.stderr.strip()))
        return json.loads(proc.stdout)


def reason(name, role):
    """The operator's template, written out literally."""
    return "'" + name + "' (" + role + ") is not in the character registry."


# ----------------------------------------------------------------------------
# AC1, AC2, AC3, AC14: classify_fusion()
# ----------------------------------------------------------------------------
class ClassifyFusionReasonsTests(IsolatedCase):

    def test_ac1_only_alpha_unregistered(self):
        r = self.probe(op="fusion", alpha="Zed", beta="Vash")
        self.assertEqual(r["reasons"], ["'Zed' (alpha) is not in the character registry."])

    def test_ac1_only_beta_unregistered(self):
        r = self.probe(op="fusion", alpha="Vash", beta="Zed")
        self.assertEqual(r["reasons"], ["'Zed' (beta) is not in the character registry."])

    def test_ac1_names_carried_verbatim(self):
        cases = [
            ("O'Brien", "'O'Brien' (alpha) is not in the character registry."),
            (HOSTILE, "'<img src=x onerror=alert(1)>&\"'' (alpha) is not in the character registry."),
            ("Zoë 影", "'Zoë 影' (alpha) is not in the character registry."),
            ("", "'' (alpha) is not in the character registry."),
            ("  Padded  ", "'  Padded  ' (alpha) is not in the character registry."),
            ("vash", "'vash' (alpha) is not in the character registry."),
        ]
        for name, expected in cases:
            with self.subTest(name=name):
                r = self.probe(op="fusion", alpha=name, beta="Vash")
                self.assertEqual(r["reasons"], [expected])

    def test_ac2_both_unregistered_alpha_then_beta(self):
        r = self.probe(op="fusion", alpha="Zed", beta="Yara")
        self.assertEqual(r["reasons"], [
            "'Zed' (alpha) is not in the character registry.",
            "'Yara' (beta) is not in the character registry.",
        ])

    def test_ac2_same_name_in_both_roles_gives_two_entries(self):
        r = self.probe(op="fusion", alpha="Zed", beta="Zed")
        self.assertEqual(r["reasons"], [
            "'Zed' (alpha) is not in the character registry.",
            "'Zed' (beta) is not in the character registry.",
        ])

    def test_ac3_resolved_fusion_has_no_reasons_key(self):
        r = self.probe(op="fusion", alpha="Bruce Lee", beta="Vash", dominance=70)
        self.assertNotIn("reasons", r)
        self.assertEqual(sorted(r), ["dominant", "fusion_name", "modality", "tags"])

    def test_ac3_cautionary_reasons_is_nonempty_list_of_strings(self):
        for alpha, beta, n in (("Zed", "Vash", 1), ("Vash", "Zed", 1), ("Zed", "Yara", 2)):
            with self.subTest(alpha=alpha, beta=beta):
                r = self.probe(op="fusion", alpha=alpha, beta=beta)
                self.assertIsInstance(r["reasons"], list)
                self.assertEqual(len(r["reasons"]), n)
                for item in r["reasons"]:
                    self.assertIsInstance(item, str)

    def test_ac14_cautionary_equals_baseline_plus_exactly_reasons(self):
        # Baseline literals captured from commit 0f1ea8e2d9bcd7eb4657963188b0be762f2b55fb.
        cases = [
            ("Zed", "Vash",
             {"fusion_name": "Zed x Vash", "state": "CAUTIONARY", "modality": None,
              "dominant": None, "tags": []},
             ["'Zed' (alpha) is not in the character registry."]),
            ("Vash", "Zed",
             {"fusion_name": "Vash x Zed", "state": "CAUTIONARY", "modality": None,
              "dominant": None, "tags": []},
             ["'Zed' (beta) is not in the character registry."]),
            ("Zed", "Zed",
             {"fusion_name": "Zed x Zed", "state": "CAUTIONARY", "modality": None,
              "dominant": None, "tags": []},
             ["'Zed' (alpha) is not in the character registry.",
              "'Zed' (beta) is not in the character registry."]),
        ]
        for alpha, beta, baseline, expected_reasons in cases:
            with self.subTest(alpha=alpha, beta=beta):
                expected = dict(baseline)
                expected["reasons"] = expected_reasons
                self.assertEqual(self.probe(op="fusion", alpha=alpha, beta=beta), expected)


# ----------------------------------------------------------------------------
# AC3, AC4, AC5: build_legacy_profile() and persistence
# ----------------------------------------------------------------------------
class LegacyProfileReasonsTests(IsolatedCase):

    RESOLVED_BASELINE_KEYS = [
        "alpha", "approved_powers", "audit_log", "beta", "biome", "created_at",
        "dominance", "dominant", "dominant_family", "fusion_name",
        "influence_pattern", "lore_summary", "modality", "power_families",
        "rhetorical_style", "signature_ability", "tags",
    ]

    def test_ac3_resolved_profile_has_no_reasons_key_and_baseline_keys(self):
        r = self.probe(op="profile", alpha="Bruce Lee", beta="Vash", dominance=70)
        self.assertNotIn("reasons", r)
        self.assertEqual(sorted(r), self.RESOLVED_BASELINE_KEYS)

    def test_ac4_cautionary_profile_exact_keys_and_values(self):
        r = self.probe(op="profile", alpha="Zed", beta="Vash")
        self.assertEqual(r, {
            "fusion_name": "Zed x Vash",
            "state": "CAUTIONARY",
            "modality": None,
            "reasons": ["'Zed' (alpha) is not in the character registry."],
        })

    def test_ac4_two_reasons_in_order(self):
        r = self.probe(op="profile", alpha="Zed", beta="Yara")
        self.assertEqual(r["reasons"], [
            "'Zed' (alpha) is not in the character registry.",
            "'Yara' (beta) is not in the character registry.",
        ])

    def test_ac5_persistence_and_export_keep_reasons(self):
        r = self.probe(op="persist", alpha="Zed", beta="Yara")
        self.assertEqual(r, [{
            "fusion_name": "Zed x Yara",
            "state": "CAUTIONARY",
            "modality": None,
            "reasons": [
                "'Zed' (alpha) is not in the character registry.",
                "'Yara' (beta) is not in the character registry.",
            ],
            "id": "MSF-001",
            "engine_version": "v3.0",
        }])


# ----------------------------------------------------------------------------
# AC6: the HTTP API, in an isolated server subprocess
# ----------------------------------------------------------------------------
class ServerReasonsTests(IsolatedCase):

    def setUp(self):
        super().setUp()
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        self.proc = subprocess.Popen(
            [sys.executable, "-B", "-c", _SERVER_DRIVER, REPO],
            cwd=self.root, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.addCleanup(self._stop)
        line = self.proc.stdout.readline()
        if not line:
            raise AssertionError("isolated server did not start")
        self.port = json.loads(line)

    def _stop(self):
        self.proc.kill()
        self.proc.wait(timeout=10)
        self.proc.stdout.close()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=20)
        try:
            conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            conn.putheader("Host", "localhost:8000")
            for k, v in (headers or {}).items():
                conn.putheader(k, v)
            if body is not None:
                conn.putheader("Content-Length", str(len(body)))
            conn.endheaders(body)
            resp = conn.getresponse()
            return resp.status, resp.read()
        finally:
            conn.close()

    def test_ac6_fuse_response_and_served_matrix_carry_reasons(self):
        payload = json.dumps({"alpha": "Zed", "beta": "Yara", "dominance": 50}).encode()
        status, body = self.request(
            "POST", "/fuse", payload,
            {"Content-Type": "application/json", "Origin": "http://localhost:8000"})
        self.assertEqual(status, 200)
        expected = [
            "'Zed' (alpha) is not in the character registry.",
            "'Yara' (beta) is not in the character registry.",
        ]
        self.assertEqual(json.loads(body)["profile"]["reasons"], expected)

        status, body = self.request("GET", "/containment_matrix.json")
        self.assertEqual(status, 200)
        matrix = json.loads(body)
        self.assertEqual(len(matrix), 1)
        self.assertEqual(matrix[0]["reasons"], expected)


# ----------------------------------------------------------------------------
# AC7, AC8: dashboard.html under node
# ----------------------------------------------------------------------------
NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');
const scenario = JSON.parse(process.env.DASH_SCENARIO);
const html = fs.readFileSync(process.env.DASH_PATH, 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) { throw new Error('no <script> block found in dashboard.html'); }
const trailingCall = /\n\s*loadMatrix\(\);\s*$/;
if (!trailingCall.test(match[1])) { throw new Error('trailing loadMatrix() call not found'); }
const source = match[1].replace(trailingCall, '\n');
const elements = {};
function makeElement(id) {
  return { id, textContent: '', innerHTML: '', className: '', style: {}, value: '',
           classList: { add() {}, remove() {}, toggle() {} } };
}
const getElement = id => (elements[id] = elements[id] || makeElement(id));
const sandbox = {
  document: {
    getElementById: getElement,
    querySelector: () => getElement('__query'),
    querySelectorAll: () => [],
    addEventListener() {},
  },
  fetch: async () => ({ ok: true, status: 200,
                        json: async () => JSON.parse(JSON.stringify(scenario.matrix)) }),
  console: { log() {}, info() {}, warn() {}, error() {}, debug() {} },
  Date, Set, Map, Math, JSON, Promise, parseInt, setTimeout,
  alert() {}, confirm() { return true; },
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(source, sandbox);
(async () => {
  let loadError = null;
  try { await sandbox.loadMatrix(); } catch (e) { loadError = String(e && e.message || e); }
  process.stdout.write(JSON.stringify({ grid: getElement('matrix-grid').innerHTML, loadError }));
})();
"""

NORMAL_ENTRY = {
    "fusion_name": "Normal Alpha x Normal Beta",
    "modality": "GROUNDED",
    "signature_ability": "Test Ability",
    "biome": "Test Biome",
    "audit_log": [],
}


def stub(name="Zed x Vash", **extra):
    entry = {"fusion_name": name, "state": "CAUTIONARY", "modality": None}
    entry.update(extra)
    return entry


# Grid HTML for [NORMAL_ENTRY, stub()] captured from the unmodified
# dashboard.html at commit 0f1ea8e2d9bcd7eb4657963188b0be762f2b55fb.
BASELINE_GRID = '\n      <div class="fusion-card GROUNDED" onclick="openCase(0)">\n        <span class="card-badge GROUNDED">GROUNDED</span>\n        <p class="card-name">Normal Alpha x Normal Beta</p>\n        <p class="card-sig">Test Ability</p>\n        <p class="card-biome">Test Biome</p>\n        \n        <div class="card-footer">\n          <span class="card-id">MSF-001</span>\n          <span class="card-arrow">→</span>\n        </div>\n      </div>\n    \n      <div class="fusion-card CAUTIONARY">\n        <span class="card-badge CAUTIONARY">CAUTIONARY</span>\n        <p class="card-name">Zed x Vash</p>\n        <div class="card-footer">\n          <span class="card-id">MSF-002</span>\n        </div>\n      </div>\n    '


def split_cards(grid_html):
    return grid_html.split('<div class="fusion-card')[1:]


REASON_LINE = re.compile(r'<p class="audit-reason">(.*?)</p>', re.S)


class DashboardReasonsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the CAUTIONARY reasons tests and was not found on PATH"
            )

    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="auth012_dash_", ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name

    def render(self, matrix):
        env = dict(os.environ, DASH_SCENARIO=json.dumps({"matrix": matrix}),
                   DASH_PATH=DASHBOARD_PATH)
        proc = subprocess.run(["node", "-e", NODE_HARNESS], cwd=self.root, env=env,
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
        if proc.returncode != 0:
            raise AssertionError("node harness failed (exit %d): %s"
                                 % (proc.returncode, proc.stderr.strip()))
        result = json.loads(proc.stdout)
        self.assertIsNone(result["loadError"])
        self.assertNotIn("No matrix file found", result["grid"])
        self.assertNotIn("Matrix could not be rendered", result["grid"])
        return result["grid"]

    def stub_card_reasons(self, grid, index=0):
        return REASON_LINE.findall(split_cards(grid)[index])

    def test_ac7_one_reason_one_line(self):
        grid = self.render([stub(reasons=["'Zed' (alpha) is not in the character registry."])])
        self.assertEqual(self.stub_card_reasons(grid),
                         ["&#39;Zed&#39; (alpha) is not in the character registry."])

    def test_ac7_two_reasons_separate_lines_in_order(self):
        grid = self.render([stub("Zed x Yara", reasons=[
            "'Zed' (alpha) is not in the character registry.",
            "'Yara' (beta) is not in the character registry.",
        ])])
        self.assertEqual(self.stub_card_reasons(grid), [
            "&#39;Zed&#39; (alpha) is not in the character registry.",
            "&#39;Yara&#39; (beta) is not in the character registry.",
        ])

    def test_ac7_hostile_name_is_escaped(self):
        hostile_reason = "'<img src=x onerror=alert(1)>&\"'' (alpha) is not in the character registry."
        grid = self.render([stub(HOSTILE + " x Vash", reasons=[hostile_reason])])
        self.assertNotIn("<img", grid)
        self.assertIn(HOSTILE_ESCAPED, grid)
        lines = self.stub_card_reasons(grid)
        self.assertEqual([html.unescape(x) for x in lines], [hostile_reason])

    def test_ac7_stub_card_not_clickable_and_one_card_per_entry(self):
        matrix = [NORMAL_ENTRY, stub(reasons=["'Zed' (alpha) is not in the character registry."])]
        grid = self.render(matrix)
        cards = split_cards(grid)
        self.assertEqual(len(cards), 2)
        self.assertNotIn("onclick", cards[1])
        self.assertIn('onclick="openCase(0)"', cards[0])

    def test_ac8_mixed_array_renders_exactly_the_strings_in_order(self):
        mixed = ["first <b>", 1, None, {"x": "y"}, ["nested"], True, "second & last"]
        grid = self.render([stub(reasons=mixed)])
        self.assertEqual(self.stub_card_reasons(grid),
                         ["first &lt;b&gt;", "second &amp; last"])
        for leaked in ("nested", "[object Object]", ">1<", ">true<", ">null<"):
            self.assertNotIn(leaked, grid)

    def test_ac8_non_array_reasons_render_no_reason_lines(self):
        for value in ([], None, "a string", 5, {"a": "b"}, True):
            with self.subTest(reasons=value):
                grid = self.render([stub(reasons=value)])
                self.assertEqual(self.stub_card_reasons(grid), [])
                self.assertEqual(len(split_cards(grid)), 1)

    def test_ac8_entry_without_reasons_is_byte_identical_to_baseline(self):
        self.assertEqual(self.render([NORMAL_ENTRY, stub()]), BASELINE_GRID)

    def test_ac8_normal_card_unchanged_beside_a_reasoned_stub(self):
        with_reasons = self.render([NORMAL_ENTRY, stub(reasons=["'Zed' (alpha) is not in the character registry."])])
        baseline_normal_card = split_cards(BASELINE_GRID)[0]
        self.assertEqual(split_cards(with_reasons)[0], baseline_normal_card)


if __name__ == "__main__":
    unittest.main()
