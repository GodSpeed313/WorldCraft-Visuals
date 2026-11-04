"""
Dashboard non-string-modality regression - one bad record must not blank the grid.

Authorized by AUTH-014 (docs/authorizations.md). renderGrid() sent a record to
the stub-card branch only when `f.modality == null`. A non-string, non-null
modality (number, boolean, object, array) took the card branch, where
`f.modality.replace(...)` threw inside MATRIX.map(), so no card rendered and
loadMatrix() showed "Matrix could not be rendered".

This file reuses the node harness in test_dashboard_null_modality.py (it
imports helpers and constants from there and does not modify that file):
dashboard.html's own <script> runs under `node` in a vm with a fake DOM and an
in-memory fetch. Nothing is read from or written to containment_matrix.json.

Standard library only (unittest). The external dependency is the `node`
executable, used as a subprocess only. If `node` is unavailable this test
FAILS; it never skips, because a skipped regression test passes vacuously.
"""

import shutil
import unittest

from test_dashboard_null_modality import (
    MISSING_FILE_MESSAGE,
    NORMAL_ENTRY,
    run_dashboard,
    split_cards,
)

RENDER_FAILURE_MESSAGE = "could not be rendered"

BAD_FUSION_NAME = "Bad Modality Alpha x Normal Beta"

NON_STRING_MODALITIES = {
    "number": 42,
    "boolean": True,
    "object": {"x": 1},
    "array": ["GROUNDED"],
}


class DashboardNonStringModalityTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fail, never skip: a skipped regression test passes vacuously.
        if shutil.which("node") is None:
            raise AssertionError(
                "node is required to run the dashboard regression tests and was not found on PATH"
            )

    def test_non_string_modality_does_not_blank_the_grid(self):
        """A record with a non-string modality renders as a stub card; the other cards still render."""
        for label, value in NON_STRING_MODALITIES.items():
            with self.subTest(modality=label):
                bad = {
                    "fusion_name": BAD_FUSION_NAME,
                    "state": "CAUTIONARY",
                    "modality": value,
                }
                matrix = [NORMAL_ENTRY, bad]
                result = run_dashboard({"mode": "matrix", "matrix": matrix})
                grid = result["grid"]

                self.assertNotIn(RENDER_FAILURE_MESSAGE, grid)
                self.assertNotIn(MISSING_FILE_MESSAGE, grid)

                cards = split_cards(grid)
                self.assertEqual(len(cards), len(matrix))

                normal_card = next(c for c in cards if NORMAL_ENTRY["fusion_name"] in c)
                bad_card = next(c for c in cards if BAD_FUSION_NAME in c)
                # Non-vacuity: the normal card does carry the trigger, so the check below can fail.
                self.assertIn("onclick", normal_card)
                self.assertNotIn("onclick", bad_card)
                self.assertNotIn("openCase", bad_card)


if __name__ == "__main__":
    unittest.main()
