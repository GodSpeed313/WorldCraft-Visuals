"""
Dashboard HTML escaping regression: matrix-derived text must render as text.

Authorized by AUTH-008 (docs/authorizations.md). dashboard.html's renderGrid()
inserted matrix-derived fields into its card template without escaping. The
one such field reachable with typed text is a CAUTIONARY stub's fusion_name:
any unregistered name becomes `"<alpha> x <beta>"` verbatim
(modality_classifier.py classify_fusion) and is persisted by server.py.

This file reuses the node harness in test_dashboard_null_modality.py (it
imports helper functions and constants from there and does not modify that
file): dashboard.html's own <script> runs under `node` in a vm with a fake DOM
and an in-memory fetch. Nothing here calls save_to_matrix or export_for_web,
and nothing reads or writes containment_matrix.json. Fixtures are literal
dicts. Standard library only; `node` is used as a subprocess. If `node` is
unavailable these tests FAIL; they never skip.

Scope is the two renderGrid() card branches. openCase() (the case-file modal)
is not covered and not changed.
"""

import copy
import html
import re
import shutil
import unittest

from test_dashboard_null_modality import (
    CAUTIONARY_STUB,
    NORMAL_ENTRY,
    count_cards,
    run_dashboard,
    split_cards,
)


HOSTILE = "<img src=x onerror=alert(1)>&\"'"

# Parts of the escaped form that must be present. The apostrophe's entity is
# deliberately not pinned (&#39; vs &#x27;); the round trip through
# html.unescape() below proves it is encoded as text either way.
ESCAPED_MARKERS = (
    "&lt;img src=x onerror=alert(1)&gt;",
    "&amp;",
    "&quot;",
)

# What the benign fixture below showed as visible text on the dashboard before
# AUTH-008, with tags stripped, entities decoded and whitespace collapsed.
BENIGN_MATRIX = [
    {
        "fusion_name": "Malcolm X x Vash",
        "modality": "LEGACY",
        "signature_ability": "Rhetoric & Legacy",
        "biome": "Dust Plains",
        "audit_log": [],
        "id": "MSF-001",
    },
    {
        "fusion_name": "Unregistered Alpha x Vash",
        "state": "CAUTIONARY",
        "modality": None,
        "id": "MSF-002",
    },
]
BENIGN_VISIBLE_TEXT = (
    "LEGACY Malcolm X x Vash Rhetoric & Legacy Dust Plains MSF-001 → "
    "CAUTIONARY Unregistered Alpha x Vash MSF-002"
)

CARD_NAME = re.compile(r'<p class="card-name">(.*?)</p>', re.S)


def visible_text(grid_html):
    stripped = re.sub(r"<[^>]+>", " ", grid_html)
    return " ".join(html.unescape(stripped).split())


def run_grid(matrix):
    return run_dashboard({"mode": "matrix", "matrix": matrix})["grid"]


class DashboardEscapingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fail, never skip: a skipped regression test passes vacuously.
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the dashboard regression tests and was not found on PATH"
            )

    def assert_escaped_once(self, grid):
        self.assertNotIn("<img", grid)
        for marker in ESCAPED_MARKERS:
            self.assertIn(marker, grid)

    def test_cautionary_stub_fusion_name_renders_as_text(self):
        stub = dict(CAUTIONARY_STUB, fusion_name=HOSTILE)
        matrix = [NORMAL_ENTRY, stub]
        grid = run_grid(matrix)
        self.assert_escaped_once(grid)
        self.assertEqual(count_cards(grid), len(matrix))
        stub_card = next(c for c in split_cards(grid) if "&lt;img" in c)
        self.assertEqual(html.unescape(CARD_NAME.search(stub_card).group(1)), HOSTILE)
        self.assertNotIn("onclick", stub_card)

    def test_normal_card_fields_render_as_text(self):
        for field in ("fusion_name", "signature_ability", "biome", "id"):
            with self.subTest(field=field):
                entry = dict(copy.deepcopy(NORMAL_ENTRY), **{field: HOSTILE})
                grid = run_grid([entry])
                self.assert_escaped_once(grid)
                self.assertEqual(count_cards(grid), 1)

    def test_hostile_modality_cannot_break_out_of_a_class_attribute(self):
        payload = 'GROUNDED" onmouseover="alert(1)'
        entry = dict(copy.deepcopy(NORMAL_ENTRY), modality=payload)
        grid = run_grid([entry])
        # The whole payload must stay inside the class attribute value: the
        # first double quote after `class="` must not end it early.
        for tag in ("div", "span"):
            with self.subTest(tag=tag):
                match = re.search(r'<%s class="([^"]*)"' % tag, grid)
                self.assertIsNotNone(match)
                self.assertIn("onmouseover", match.group(1))
        self.assertNotIn('" onmouseover="', grid)

    def test_hostile_state_cannot_break_out_of_a_class_attribute(self):
        payload = 'CAUTIONARY" onmouseover="alert(1)'
        stub = dict(CAUTIONARY_STUB, state=payload)
        grid = run_grid([stub])
        for tag in ("div", "span"):
            with self.subTest(tag=tag):
                match = re.search(r'<%s class="([^"]*)"' % tag, grid)
                self.assertIsNotNone(match)
                self.assertIn("onmouseover", match.group(1))
        self.assertNotIn('" onmouseover="', grid)

    def test_benign_fixture_keeps_the_same_visible_text(self):
        """'Rhetoric & Legacy' is the one engine string with a special character."""
        grid = run_grid(BENIGN_MATRIX)
        self.assertEqual(visible_text(grid), BENIGN_VISIBLE_TEXT)


if __name__ == "__main__":
    unittest.main()
