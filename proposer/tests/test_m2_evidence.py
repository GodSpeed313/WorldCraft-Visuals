"""IMP-001 M2 evidence root, write-once files, secret scan and reservation: negative tests 2, 8, 9, 10."""

from __future__ import annotations

import os
import subprocess
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

from proposer import m2_evidence
from proposer.m2_config import COMMITTED_CONFIG
from proposer.m2_evidence import (EvidenceError, EvidenceStore, RESERVATION_NAME, ReservationExists, RootRejected,
                                  SecretDetected, scan_for_secrets, verify_root)
from proposer.packet import REPO_ROOT
from proposer.tests.m2_support import FAKE_KEY, M2TestCase


class CommittedConfigTests(unittest.TestCase):
    def test_evidence_root_is_the_fixed_committed_location_outside_the_repo(self):
        self.assertEqual(COMMITTED_CONFIG.evidence_root, r"C:\Users\User\WorldCraft-Evidence\imp-001-m2")
        self.assertFalse(str(REPO_ROOT).lower().replace("/", "\\") in COMMITTED_CONFIG.evidence_root.lower())

    def test_the_cli_offers_no_way_to_override_the_root(self):
        import contextlib
        import io
        from proposer import m2_harness
        for argv in (["dry-run", "--root", "/elsewhere"], ["run", "--authorization-ref", "x", "--evidence-root", "/elsewhere"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                m2_harness.main(argv)

    def test_committed_rates_are_the_verified_standard_opus_5_5_rates(self):
        rates = COMMITTED_CONFIG.rates
        self.assertEqual((rates.input_per_mtok, rates.output_per_mtok), (Decimal("4.00"), Decimal("20.00")))
        self.assertIs(rates.verified, True)
        self.assertEqual(rates.verified_on, "2026-11-15")
        self.assertEqual(rates.source, "https://platform.claude.com/docs/en/about-claude/pricing")


class RootVerificationTests(M2TestCase):
    # --- negative test 9 ---

    def test_a_good_root_is_accepted_and_the_probe_leaves_nothing_behind(self):
        self.assertEqual(os.path.normcase(str(verify_root(self.root, REPO_ROOT))), os.path.normcase(self.root))
        self.assertEqual(self.files(), [])

    def test_missing_root_is_rejected_and_not_created(self):
        missing = os.path.join(self.tmp, "does_not_exist")
        with self.assertRaisesRegex(RootRejected, "does not exist"):
            verify_root(missing, REPO_ROOT)
        self.assertFalse(os.path.exists(missing))

    def test_relative_and_non_directory_roots_are_rejected(self):
        with self.assertRaisesRegex(RootRejected, "absolute"):
            verify_root("evidence", REPO_ROOT)
        afile = os.path.join(self.tmp, "afile")
        Path(afile).write_text("x")
        with self.assertRaisesRegex(RootRejected, "not a directory"):
            verify_root(afile, REPO_ROOT)

    def test_unwritable_root_is_rejected(self):
        with mock.patch.object(m2_evidence, "_probe_writable", side_effect=PermissionError("read-only")):
            with self.assertRaisesRegex(RootRejected, "not writable"):
                verify_root(self.root, REPO_ROOT)

    def test_repository_internal_root_is_rejected(self):
        fake_repo = os.path.join(self.tmp, "repo")
        inside = os.path.join(fake_repo, "evidence")
        os.makedirs(inside)
        with self.assertRaisesRegex(RootRejected, "inside the repository"):
            verify_root(inside, fake_repo)

    def make_dir_link(self, link, target):
        """A directory symlink, or on Windows without that privilege a junction (`mklink /J`, no admin needed)."""
        try:
            os.symlink(target, link, target_is_directory=True)
            return "symlink"
        except (OSError, NotImplementedError):
            pass
        if os.name == "nt":
            done = subprocess.run(["cmd", "/c", "mklink", "/J", link, target], capture_output=True)
            if done.returncode == 0 and os.path.isdir(link):
                return "junction"
        self.skipTest("neither a symlink nor a junction can be created here")

    def test_symlink_or_junction_into_the_repository_is_rejected(self):
        fake_repo = os.path.join(self.tmp, "repo")
        os.makedirs(os.path.join(fake_repo, "evidence"))
        link = os.path.join(self.tmp, "looks_external")
        self.make_dir_link(link, os.path.join(fake_repo, "evidence"))
        with self.assertRaises(RootRejected):
            verify_root(link, fake_repo)

    def test_root_reached_through_a_redirected_parent_is_rejected(self):
        real = os.path.join(self.tmp, "real_parent")
        os.makedirs(os.path.join(real, "evidence"))
        link = os.path.join(self.tmp, "link_parent")
        self.make_dir_link(link, real)
        with self.assertRaisesRegex(RootRejected, "redirected"):
            verify_root(os.path.join(link, "evidence"), REPO_ROOT)

    def test_a_reparse_point_is_rejected_even_when_symlink_checks_say_no(self):
        with mock.patch.object(m2_evidence, "_is_link_or_junction", return_value=True):
            with self.assertRaisesRegex(RootRejected, "symlink, junction"):
                verify_root(self.root, REPO_ROOT)


class WriteOnceTests(M2TestCase):
    # --- negative test 10 ---

    def test_duplicate_evidence_cannot_overwrite(self):
        store = EvidenceStore(Path(self.root), self.key)
        store.write_once("M2_X.json", b"first")
        with self.assertRaisesRegex(EvidenceError, "never overwritten"):
            store.write_once("M2_X.json", b"second")
        self.assertEqual(Path(self.root, "M2_X.json").read_bytes(), b"first")

    def test_hash_is_of_the_exact_bytes_and_names_are_confined_to_the_root(self):
        store = EvidenceStore(Path(self.root), self.key)
        self.assertEqual(store.write_once("M2_H.bin", b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        for bad in ("../M2_escape", "sub/M2_x", "notprefixed.json", "M2_a\\b"):
            with self.assertRaises(EvidenceError):
                store.write_once(bad, b"x")

    # --- negative test 2 ---

    def test_a_credential_in_a_proposed_record_prevents_the_write(self):
        store = EvidenceStore(Path(self.root), self.key)
        for payload in (f"leaked {self.key}".encode(), b"only the prefix sk-ant-abc"):
            with self.assertRaises(SecretDetected):
                store.write_once("M2_SECRET.json", payload)
            self.assertNotIn("M2_SECRET.json", self.files(), "no file, redacted or otherwise, may be created")

    def test_the_exact_key_value_is_caught_even_without_the_provider_prefix(self):
        """The prefix scan would hide a broken exact-value scan if the test key started with sk-ant-."""
        odd_key = "no-provider-prefix-0123456789abcdef"
        store = EvidenceStore(Path(self.root), odd_key)
        with self.assertRaisesRegex(SecretDetected, "configured API key value"):
            store.write_once("M2_ODD.json", f'{{"echo": "{odd_key}"}}'.encode())
        self.assertEqual(self.files(), [])

    def test_json_records_are_scanned_too(self):
        store = EvidenceStore(Path(self.root), self.key)
        with self.assertRaises(SecretDetected):
            store.write_json_once("M2_REC.json", {"headers": {"x-api-key": self.key}})
        self.assertEqual(self.files(), [])

    def test_scan_has_no_false_positive_on_ordinary_text(self):
        scan_for_secrets(b'{"error": "invalid x-api-key"}', FAKE_KEY)   # a provider 401 body names the header, not the key


class ReservationTests(M2TestCase):
    def store(self):
        return EvidenceStore(Path(self.root), self.key)

    def test_reservation_is_created_once_and_blocks_a_second(self):
        rid, sha = self.store().reserve({"pair": ["ilse_marrow", "sable_quillon"]})
        self.assertEqual(self.read_json(RESERVATION_NAME)["reservation_id"], rid)
        with self.assertRaises(ReservationExists):
            self.store().reserve({"pair": ["ilse_marrow", "sable_quillon"]})

    def test_reservation_for_one_pair_blocks_a_different_pair(self):
        self.store().reserve({"pair": ["ilse_marrow", "sable_quillon"]})
        with self.assertRaises(ReservationExists):
            self.store().reserve({"pair": ["tamsin_vey", "pell_dunmore"]})

    def test_a_fresh_store_object_or_checkout_still_sees_the_reservation(self):
        self.store().reserve({"pair": ["a", "b"]})
        with self.assertRaises(ReservationExists):               # new object, nothing carried in memory
            EvidenceStore(Path(self.root), None).assert_milestone_open()

    def test_other_attempt_artifacts_also_block_but_dry_run_reports_do_not(self):
        self.store().write_once("M2_DRYRUN_20260101.json", b"{}")
        self.store().assert_milestone_open()                     # a dry run is not an attempt
        self.store().write_once("M2_RUN_RECORD.json", b"{}")     # a run record with no reservation still proves an attempt
        with self.assertRaises(ReservationExists):
            self.store().assert_milestone_open()

    def test_failed_reservation_write_still_blocks(self):
        with mock.patch.object(EvidenceStore, "write_json_once", side_effect=EvidenceError("disk full")):
            with self.assertRaises(EvidenceError):
                self.store().reserve({"pair": ["a", "b"]})
        Path(self.root, RESERVATION_NAME).write_bytes(b"{")      # what a crash mid-write leaves behind
        with self.assertRaises(ReservationExists):
            self.store().reserve({"pair": ["a", "b"]})

    def test_nothing_in_the_harness_can_delete_or_reset_evidence(self):
        for module in ("m2_evidence", "m2_harness", "m2_provider", "m2_request", "m2_validate", "m2_config"):
            text = Path(REPO_ROOT, "proposer", f"{module}.py").read_text(encoding="utf-8")
            for forbidden in ("rmtree", ".unlink(", "os.remove", "os.rename", "shutil.move", "os.replace"):
                if module == "m2_evidence" and forbidden == ".unlink(":
                    continue
                self.assertNotIn(forbidden, text, f"{module} contains {forbidden}")
        self.assertEqual(Path(REPO_ROOT, "proposer", "m2_evidence.py").read_text(encoding="utf-8").count("os.unlink("), 1,
                         "os.unlink may appear only in the writability probe")


if __name__ == "__main__":
    unittest.main()
