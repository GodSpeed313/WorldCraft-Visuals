"""AUTH-013: save_to_matrix() fills a missing `reasons` key on a duplicate record.

Background (AUTH-012 residual): save_to_matrix() skips a profile whose
(fusion_name, signature_ability) matches a saved entry. A CAUTIONARY stub has no
signature_ability, so an older reason-less stub for a fusion used to shadow a newer stub
that carries `reasons`. The repair is fill-only: when the incoming profile has a non-empty
`reasons` list, every matching record that lacks the `reasons` key gains it. Nothing is
replaced, reordered, consolidated or appended.

Safety: every test points mythos_sync.MATRIX_FILE at a file inside its own temporary
directory and captures standard output, so no test depends on console encoding.
export_for_web() reads through MATRIX_FILE but writes the hard-coded relative path
`containment_matrix.json`, so the one helper that calls it runs in the temporary directory,
restores the previous working directory in a `finally` block, and asserts where it is
before calling. The real containment_matrix.json is never read or written. Do not run these
tests concurrently with other tests that change the working directory.
"""

import contextlib
import copy
import io
import json
import os
import tempfile
import unittest

import mythos_sync


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


OLD_STUB = {"fusion_name": "Zed x Vash", "state": "CAUTIONARY", "modality": None,
            "id": "MSF-001", "engine_version": "v3.0"}
NEW_REASONS = ["'Zed' (alpha) is not in the character registry."]
NEW_STUB = {"fusion_name": "Zed x Vash", "state": "CAUTIONARY", "modality": None,
            "dominant": None, "tags": [], "reasons": list(NEW_REASONS)}
RESOLVED = {"fusion_name": "Bruce Lee x Vash", "signature_ability": "Kinetic Mastery",
            "dominant_family": "COMBAT", "id": "MSF-009", "engine_version": "v3.0"}
OTHER_STUB = {"fusion_name": "Foo x Bar", "state": "CAUTIONARY", "modality": None,
              "id": "MSF-005", "engine_version": "v3.0"}


class MatrixReasonsCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._original = mythos_sync.MATRIX_FILE
        self.addCleanup(setattr, mythos_sync, "MATRIX_FILE", self._original)
        mythos_sync.MATRIX_FILE = os.path.join(self._tmp.name, "matrix.json")
        self.assertEqual(os.path.realpath(os.path.dirname(mythos_sync.MATRIX_FILE)),
                         os.path.realpath(self._tmp.name))

    # -- helpers -------------------------------------------------------------
    def seed(self, entries):
        with open(mythos_sync.MATRIX_FILE, "w", encoding="utf-8") as f:
            json.dump(copy.deepcopy(entries), f, indent=2)

    def save(self, profile):
        quiet(mythos_sync.save_to_matrix, copy.deepcopy(profile))

    def load(self):
        return mythos_sync.load_matrix()

    def raw(self):
        with open(mythos_sync.MATRIX_FILE, "rb") as f:
            return f.read()

    def export(self):
        """Run export_for_web() inside the temporary directory and return the exported records."""
        previous = os.getcwd()
        os.chdir(self._tmp.name)
        try:
            self.assertEqual(os.path.realpath(os.getcwd()), os.path.realpath(self._tmp.name))
            quiet(mythos_sync.export_for_web)
            exported_path = os.path.realpath("containment_matrix.json")
            self.assertEqual(os.path.dirname(exported_path), os.path.realpath(self._tmp.name))
            with open(exported_path, encoding="utf-8") as f:
                return json.load(f)
        finally:
            os.chdir(previous)

    @staticmethod
    def same_key(record, profile):
        return (record.get("fusion_name") == profile.get("fusion_name")
                and record.get("signature_ability") == profile.get("signature_ability"))

    @staticmethod
    def text(record):
        return json.dumps(record, indent=2)

    # -- T1 ------------------------------------------------------------------
    def test_t1_reasons_are_filled_into_an_older_reasonless_stub_and_exported(self):
        self.seed([OLD_STUB])
        self.save(NEW_STUB)
        saved = self.load()
        self.assertEqual(len(saved), 1)
        self.assertIn("reasons", saved[0])
        self.assertEqual(saved[0]["reasons"], NEW_STUB["reasons"])
        self.assertEqual({k: v for k, v in saved[0].items() if k != "reasons"}, OLD_STUB)

        exported = self.export()
        matches = [e for e in exported if self.same_key(e, NEW_STUB)]
        self.assertEqual(len(matches), 1)
        self.assertIn("reasons", matches[0])
        self.assertEqual(matches[0]["reasons"], saved[0]["reasons"])

    # -- T2 ------------------------------------------------------------------
    def test_t2_a_repeat_save_changes_nothing(self):
        self.seed([OLD_STUB])
        self.save(NEW_STUB)
        after_first = self.raw()
        self.save(NEW_STUB)
        self.assertEqual(self.raw(), after_first)
        self.assertEqual(len(self.load()), 1)

    # -- T3 ------------------------------------------------------------------
    def test_t3_existing_reasons_are_never_replaced(self):
        for existing in (["an older, different reason"], []):
            with self.subTest(existing=existing):
                record = dict(OLD_STUB, reasons=list(existing))
                self.seed([record])
                before = self.raw()
                self.save(NEW_STUB)
                self.assertEqual(self.load(), [record])
                self.assertEqual(self.raw(), before)

    # -- T4 ------------------------------------------------------------------
    def test_t4_unrelated_records_are_untouched(self):
        seeded = [RESOLVED, OLD_STUB, OTHER_STUB]
        self.seed(seeded)
        self.save(NEW_STUB)
        after = self.load()
        self.assertEqual(len(after), len(seeded))
        for i in (0, 2):
            self.assertEqual(self.text(after[i]), self.text(seeded[i]))
        self.assertEqual([r["id"] for r in after], [r["id"] for r in seeded])

    # -- T5 ------------------------------------------------------------------
    def test_t5_resolved_duplicates_are_still_skipped(self):
        self.seed([RESOLVED])
        before = self.raw()
        self.save(RESOLVED)
        self.assertEqual(self.raw(), before)
        self.assertNotIn("reasons", self.load()[0])

        self.save(dict(RESOLVED, signature_ability="Another Ability"))
        after = self.load()
        self.assertEqual(len(after), 2)
        self.assertEqual(after[0], RESOLVED)
        self.assertEqual(after[1]["signature_ability"], "Another Ability")

    # -- T6 ------------------------------------------------------------------
    def test_t6_empty_absent_or_non_list_reasons_change_nothing(self):
        absent = {k: v for k, v in NEW_STUB.items() if k != "reasons"}
        variants = {
            "empty list": dict(NEW_STUB, reasons=[]),
            "absent": absent,
            "none": dict(NEW_STUB, reasons=None),
            "string": dict(NEW_STUB, reasons="not a list"),
            "dict": dict(NEW_STUB, reasons={"a": 1}),
            "number": dict(NEW_STUB, reasons=5),
        }
        for label, incoming in variants.items():
            with self.subTest(incoming=label):
                self.seed([OLD_STUB])
                before = self.raw()
                self.save(incoming)
                self.assertEqual(self.raw(), before)
                self.assertNotIn("reasons", self.load()[0])

    # -- T7 ------------------------------------------------------------------
    def test_t7_every_matching_record_lacking_reasons_is_filled_and_others_are_not(self):
        keeper = dict(OLD_STUB, id="MSF-002", reasons=["kept as it was"])
        lacking = dict(OLD_STUB, id="MSF-003")
        seeded = [RESOLVED, keeper, lacking, OTHER_STUB]
        self.seed(seeded)
        self.save(NEW_STUB)
        after = self.load()

        self.assertEqual(len(after), len(seeded))
        self.assertEqual([r["id"] for r in after], [r["id"] for r in seeded])
        self.assertEqual(self.text(after[1]), self.text(keeper))
        self.assertIn("reasons", after[2])
        self.assertEqual(after[2]["reasons"], NEW_STUB["reasons"])
        self.assertEqual({k: v for k, v in after[2].items() if k != "reasons"}, lacking)
        self.assertEqual(self.text(after[0]), self.text(RESOLVED))
        self.assertEqual(self.text(after[3]), self.text(OTHER_STUB))


if __name__ == "__main__":
    unittest.main(verbosity=2)
