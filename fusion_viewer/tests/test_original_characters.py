"""Original character authoring (AUTH-017): the checker, --characters-dir, the ownership label.

User files live in temporary folders OUTSIDE the repository. Existing character names and the
style allowlist terms are read from the real library, never typed into this file."""

import hashlib
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from fusion_synthesis.loader import DATA_DIR, load_library

from fusion_viewer import build, character_check
from fusion_viewer.build import render_html, strip_extensions
from fusion_viewer.character_check import check_files
from fusion_viewer.viewmodel import NOT_SYNTHESIZED, OWNERSHIP_VALUES

from . import PACKAGE_DIR, REPO_ROOT, run_harness

SLOTS = ("build", "face", "hair", "clothing", "palette", "signature_element", "ability_manifestation")
BASELINE_SHA256 = "0c44738a224c01cf50f21508579ec5fe2b15a9da83d03411f48f7e1e1c99aa98"
BASELINE_BYTES = 170033
TEMPLATE = PACKAGE_DIR / "original_character_template.json"


def character(name="Tamsin Wick", **changes):
    slug = name.lower().replace(" ", "_")
    data = {
        "schema": "fusion-synthesis-character/1",
        "name": name,
        "ownership": "original",
        "epistemic_status": "FICTIONAL",
        "properties": [
            {"id": f"{slug}.lantern_sense", "name": "Lantern Sense", "description": "Feels the age of any flame she touches.",
             "contribution_type": "ABILITY", "architectural_placement": "CORE_MECHANISM"},
            {"id": f"{slug}.borrowed_light", "name": "Borrowed Light", "description": "Cannot make fire, only read it.",
             "contribution_type": "MECHANISM", "architectural_placement": "LIMITATIONS", "is_hard_limitation": True},
        ],
        "visual_traits": [
            {"id": f"{slug}.v_{s}", "slot": s, "descriptor": f"a plain {s.replace('_', ' ')}", "derives_from": []} for s in SLOTS
        ],
        "proper_nouns": [],
        "exclusion_candidates": [],
    }
    data.update(changes)
    return data


def slug_of(name):
    return name.lower().replace(" ", "_")


class UserFolder:
    """A temporary folder outside the repository, with character files written into it."""

    def __init__(self, test):
        self._tmp = tempfile.TemporaryDirectory(prefix="fv-user-")
        test.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name)

    def write(self, file_name, data=None, raw=None):
        target = self.path / file_name
        target.write_bytes(raw if raw is not None else json.dumps(data, indent=2).encode("utf-8"))
        return target

    def snapshot(self):
        return {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in sorted(self.path.iterdir())}


def run_check(*paths):
    out, err = io.StringIO(), io.StringIO()
    code = character_check.main([str(p) for p in paths], stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def run_build(*args):
    out, err = io.StringIO(), io.StringIO()
    code = build.main([str(a) for a in args], stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


class CheckerCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.existing = next(iter(cls.library.characters.values()))
        cls.allowlist_term = cls.library.allowlist.terms[0]

    def setUp(self):
        self.folder = UserFolder(self)

    def assert_fails(self, path, *needles):
        code, out, err = run_check(path)
        self.assertEqual(code, 2, err)
        self.assertNotIn("OK:", out)
        self.assertIn(path.name, err)  # names the responsible file
        for needle in needles:
            self.assertIn(needle, err)  # and the cause
        return err

    def test_a_valid_file_is_ok(self):
        path = self.folder.write("tamsin_wick.json", character())
        code, out, err = run_check(path)
        self.assertEqual((code, err), (0, ""))
        self.assertIn("OK: tamsin_wick.json", out)
        self.assertIn("ownership: original", out)
        self.assertIn("self-declaration", out)

    def test_a_utf8_bom_is_explained_in_plain_words(self):
        path = self.folder.write("tamsin_wick.json", raw=b"\xef\xbb\xbf" + json.dumps(character()).encode("utf-8"))
        err = self.assert_fails(path, "byte-order mark", "without a BOM")
        self.assertNotIn("Unexpected UTF-8", err)

    def test_bad_json_names_the_file_and_the_cause(self):
        path = self.folder.write("tamsin_wick.json", raw=b'{"schema": "x",}')
        self.assert_fails(path, "not valid JSON")

    def test_a_missing_visual_slot_names_the_field(self):
        data = character()
        data["visual_traits"] = data["visual_traits"][:-1]
        self.assert_fails(self.folder.write("tamsin_wick.json", data), "visual_traits", "ability_manifestation")

    def test_a_file_name_that_is_not_the_slug_is_rejected(self):
        self.assert_fails(self.folder.write("tamsin.json", character()), "file name must be tamsin_wick.json")

    def test_multi_line_text_is_rejected(self):
        data = character()
        data["properties"][0]["description"] = "line one\nline two"
        self.assert_fails(self.folder.write("tamsin_wick.json", data), "single line")

    def test_an_allowlist_collision_is_attributed_to_the_file(self):
        data = character()
        data["properties"][0]["name"] = f"{self.allowlist_term} Sense"
        self.assert_fails(self.folder.write("tamsin_wick.json", data), "allowlist", self.allowlist_term)

    def test_a_character_that_would_replace_an_existing_one_is_rejected(self):
        name = self.existing.name
        path = self.folder.write(f"{self.existing.slug}.json", character(name))
        self.assert_fails(path, "already has a character file with this name", "replace an existing character")

    def test_the_same_name_under_another_file_name_is_rejected_by_the_loader(self):
        path = self.folder.write("second_copy.json", character(self.existing.name))
        self.assert_fails(path, f"file name must be {self.existing.slug}.json")

    def test_a_bad_ownership_value_is_rejected_and_the_values_are_listed(self):
        for bad in ("mine", "Original", "", None, 7, ["original"]):
            with self.subTest(value=bad):
                path = self.folder.write("tamsin_wick.json", character(ownership=bad))
                self.assert_fails(path, "ownership", "public_domain")

    def test_all_four_ownership_values_are_accepted(self):
        self.assertEqual(OWNERSHIP_VALUES, ("original", "public_domain", "third_party_ip", "licensed"))
        for value in OWNERSHIP_VALUES:
            with self.subTest(value=value):
                path = self.folder.write("tamsin_wick.json", character(ownership=value))
                code, out, err = run_check(path)
                self.assertEqual(code, 0, err)

    def test_a_missing_ownership_is_accepted_and_reported_as_not_recorded(self):
        data = character()
        del data["ownership"]
        code, out, err = run_check(self.folder.write("tamsin_wick.json", data))
        self.assertEqual(code, 0, err)
        self.assertIn("ownership: not recorded", out)

    def test_two_files_that_each_pass_alone_conflict_only_in_the_combined_run(self):
        other = UserFolder(self)
        first = self.folder.write("tamsin_wick.json", character())
        second = other.write("tamsin_wick.json", character(ownership="licensed"))
        for alone in (first, second):
            self.assertEqual(run_check(alone)[0], 0)  # each loads on its own
        code, out, err = run_check(first, second)
        self.assertEqual(code, 2)
        self.assertIn("conflict between tamsin_wick.json and tamsin_wick.json", err)
        self.assertIn(str(first), err)
        self.assertIn(str(second), err)
        self.assertEqual(out.count("OK:"), 2)  # each file did pass on its own; only the combination fails

    def test_a_conflict_is_not_blamed_on_a_file_that_failed_alone(self):
        other = UserFolder(self)
        good = self.folder.write("tamsin_wick.json", character())
        bad = other.write("rowan_pike.json", character("Rowan Pike", ownership="nope"))
        code, out, err = run_check(good, bad)
        self.assertEqual(code, 2)
        self.assertIn("rowan_pike.json", err)
        self.assertNotIn("conflict", err)
        self.assertIn("OK: tamsin_wick.json", out)

    def test_different_files_with_different_names_load_together(self):
        a = self.folder.write("tamsin_wick.json", character())
        b = self.folder.write("rowan_pike.json", character("Rowan Pike", ownership="public_domain"))
        code, out, err = run_check(a, b)
        self.assertEqual((code, err), (0, ""))
        self.assertIn("OK: rowan_pike.json", out)

    def test_a_missing_file_and_bad_usage_are_reported(self):
        self.assert_fails(self.folder.path / "nope.json", "cannot be read")
        self.assertEqual(run_check()[0], 2)
        self.assertEqual(run_check("--json")[0], 2)

    def test_the_template_is_valid_once_it_is_named_after_its_character(self):
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(data["ownership"], "original")
        path = self.folder.write("your_character_name.json", raw=TEMPLATE.read_bytes())
        code, out, err = run_check(path)
        self.assertEqual((code, err), (0, ""))

    def test_the_template_unrenamed_fails_clearly_on_the_file_name(self):
        code, _out, err = run_check(TEMPLATE)
        self.assertEqual(code, 2)
        self.assertIn("file name must be your_character_name.json", err)


class ReuseAndSafetyTests(unittest.TestCase):
    def setUp(self):
        self.folder = UserFolder(self)

    def test_library_rules_are_not_copied_into_the_viewer(self):
        source = (PACKAGE_DIR / "character_check.py").read_text(encoding="utf-8")
        for name in ("parse_character", "slugify", "check_allowlist_against_denylist", "character_denylist", "SLOTS", "validate_pair"):
            self.assertNotIn(name, source, name)
        self.assertIn("load_library", source)

    def test_the_user_folder_is_only_read(self):
        a = self.folder.write("tamsin_wick.json", character())
        self.folder.write("rowan_pike.json", character("Rowan Pike", ownership="licensed"))
        self.folder.write("broken.json", raw=b"{")
        before = self.folder.snapshot()
        run_check(a)
        run_check(*sorted(self.folder.path.iterdir()))
        run_build("--out", self.folder.path.parent / "never.html", "--characters-dir", self.folder.path)
        self.assertEqual(self.folder.snapshot(), before)  # bytes and mtimes, and no new file

    def test_the_ownership_field_is_removed_from_the_temporary_copy_only(self):
        path = self.folder.write("tamsin_wick.json", character(ownership="licensed"))
        before = path.read_bytes()
        result = check_files([path])
        self.assertEqual(result.errors, ())
        self.assertEqual([item.ownership for item in result.files], ["licensed"])
        self.assertNotIn(b"ownership", result.files[0].staged)
        self.assertIn(b"ownership", path.read_bytes())
        self.assertEqual(path.read_bytes(), before)

    def test_authored_data_is_not_changed(self):
        def tree():
            return {str(p.relative_to(DATA_DIR)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA_DIR.rglob("*")) if p.is_file()}

        before = tree()
        run_check(self.folder.write("tamsin_wick.json", character()))
        run_check(self.folder.write("bad.json", raw=b"{"))
        run_build("--out", self.folder.path.parent / "never.html", "--characters-dir", self.folder.path)
        self.assertEqual(tree(), before)


class CleanupTests(unittest.TestCase):
    """No temporary directory survives, whether the check or the build passes or fails."""

    def setUp(self):
        self.folder = UserFolder(self)
        self.watch = tempfile.TemporaryDirectory(prefix="fv-watch-")
        self.addCleanup(self.watch.cleanup)
        self.good = self.folder.write("tamsin_wick.json", character())
        self.bad_dir = UserFolder(self)
        self.bad = self.bad_dir.write("rowan_pike.json", character("Rowan Pike", ownership="nope"))
        self.broken = self.bad_dir.write("kit_vale.json", raw=b"{")

    def left_behind(self):
        return sorted(p.name for p in Path(self.watch.name).iterdir())

    def test_nothing_is_left_after_a_passing_a_failing_and_a_conflicting_check(self):
        twin = UserFolder(self)
        twin_file = twin.write("tamsin_wick.json", character())
        with mock.patch.object(tempfile, "tempdir", self.watch.name):
            run_check(self.good)
            run_check(self.bad, self.broken)
            run_check(self.good, twin_file)
        self.assertEqual(self.left_behind(), [])

    def test_nothing_is_left_after_a_failed_and_a_passing_build(self):
        out = self.folder.path.parent / "fv-out.html"
        self.addCleanup(lambda: out.unlink(missing_ok=True))
        with mock.patch.object(tempfile, "tempdir", self.watch.name):
            self.assertEqual(run_build("--out", out, "--characters-dir", self.bad_dir.path)[0], 2)
            self.assertEqual(run_build("--out", out, "--characters-dir", self.folder.path)[0], 0)
        self.assertEqual(self.left_behind(), [])

    def test_nothing_is_left_when_validation_raises_unexpectedly(self):
        with mock.patch.object(tempfile, "tempdir", self.watch.name), mock.patch.object(
            character_check, "load_library", side_effect=RuntimeError("boom")
        ):
            with self.assertRaises(RuntimeError):
                check_files([self.good])
        self.assertEqual(self.left_behind(), [])

    def test_the_temporary_copy_really_exists_while_it_is_in_use(self):
        seen = []
        real = character_check.load_library

        def spy(root):
            seen.append((Path(root) / "characters").is_dir())
            return real(root)

        with mock.patch.object(tempfile, "tempdir", self.watch.name), mock.patch.object(character_check, "load_library", side_effect=spy):
            check_files([self.good])
        self.assertTrue(seen and all(seen))
        self.assertEqual(self.left_behind(), [])


class BuildWithCharactersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.existing = list(cls.library.characters.values())
        cls.folder_holder = tempfile.TemporaryDirectory(prefix="fv-user-")
        cls.addClassCleanup(cls.folder_holder.cleanup)
        cls.user = Path(cls.folder_holder.name)
        (cls.user / "tamsin_wick.json").write_bytes(json.dumps(character(), indent=2).encode("utf-8"))
        cls.out_holder = tempfile.TemporaryDirectory(prefix="fv-out-")
        cls.addClassCleanup(cls.out_holder.cleanup)
        cls.out = Path(cls.out_holder.name) / "viewer.html"
        code, _o, err = run_build("--out", cls.out, "--characters-dir", cls.user)
        assert code == 0, err
        cls.html = cls.out.read_text(encoding="utf-8")
        cls.snap = run_harness(cls.html)
        cls.by_selection = {(p["x"], p["y"]): p for p in cls.snap["pairs"]}

    def test_the_new_character_has_a_tile(self):
        slugs = {s for p in self.snap["pairs"] for s in p["selected"]}
        self.assertIn("tamsin_wick", slugs)
        self.assertEqual(len(slugs), len(self.existing) + 1)

    def test_it_is_not_yet_synthesized_against_every_existing_character(self):
        self.assertEqual(len(self.existing), 6)
        for other in self.existing:
            for x, y in (("tamsin_wick", other.slug), (other.slug, "tamsin_wick")):
                page = self.by_selection[(x, y)]
                with self.subTest(selection=f"{x} then {y}"):
                    self.assertEqual(page["missingText"], NOT_SYNTHESIZED)
                    self.assertIsNone(page["fusionName"])
                    self.assertFalse(page["comparisonPresent"])
                    self.assertIn("tamsin_wick", page["sourceNames"])

    def test_the_source_panel_shows_the_ownership_label_with_a_self_declaration_note(self):
        page = self.by_selection[("tamsin_wick", self.existing[0].slug)]
        mine = next(o for o in page["ownership"] if o["slug"] == "tamsin_wick")
        self.assertIn("Ownership: original", mine["text"])
        self.assertIn("self-declared", mine["text"])
        self.assertIn("not verified", mine["text"])

    def test_existing_characters_show_not_recorded_and_no_self_declaration(self):
        for other in self.existing:
            page = self.by_selection[(other.slug, "tamsin_wick")]
            theirs = next(o for o in page["ownership"] if o["slug"] == other.slug)
            self.assertEqual(theirs["text"], "Ownership: not recorded")

    def test_existing_authored_pairs_are_unchanged(self):
        default = render_html(__import__("fusion_viewer.viewmodel", fromlist=["build_view"]).build_view())
        old = [p for p in run_harness(default)["pairs"]]
        new = {(p["x"], p["y"]): p for p in self.snap["pairs"]}
        for page in old:
            if page["fusionName"]:
                mine = new[(page["x"], page["y"])]
                self.assertEqual(mine["fusionName"], page["fusionName"])
                self.assertEqual(mine["comparisonTraits"], page["comparisonTraits"])
                self.assertEqual(mine["comparisonSlots"], page["comparisonSlots"])

    def test_two_builds_with_user_characters_are_byte_identical(self):
        again = Path(self.out_holder.name) / "again.html"
        self.assertEqual(run_build("--out", again, "--characters-dir", self.user)[0], 0)
        self.assertEqual(again.read_bytes(), self.out.read_bytes())

    def test_ownership_values_are_not_inferred_from_the_name_or_the_fictional_status(self):
        folder = UserFolder(self)
        data = character("Original Public Domain")
        del data["ownership"]
        folder.write("original_public_domain.json", data)
        out = Path(self.out_holder.name) / "inferred.html"
        self.assertEqual(run_build("--out", out, "--characters-dir", folder.path)[0], 0)
        snap = run_harness(out.read_text(encoding="utf-8"))
        texts = [o["text"] for p in snap["pairs"] for o in p["ownership"] if o["slug"] == "original_public_domain"]
        self.assertTrue(texts)
        self.assertEqual(set(texts), {"Ownership: not recorded"})  # FICTIONAL status and the words in the name decide nothing

    def test_a_bad_character_file_fails_the_build_and_writes_nothing(self):
        folder = UserFolder(self)
        folder.write("tamsin_wick.json", character(ownership="nope"))
        out = Path(self.out_holder.name) / "failed.html"
        code, _o, err = run_build("--out", out, "--characters-dir", folder.path)
        self.assertEqual(code, 2)
        self.assertIn("tamsin_wick.json", err)
        self.assertIn("ownership", err)
        self.assertFalse(out.exists())

    def test_folder_problems_are_reported_without_writing(self):
        empty = UserFolder(self)
        out = Path(self.out_holder.name) / "folder.html"
        for target, text in ((empty.path, "no .json"), (empty.path / "missing", "not a folder"), (REPO_ROOT / "fusion_viewer", "inside the repository")):
            with self.subTest(folder=str(target)):
                code, _o, err = run_build("--out", out, "--characters-dir", target)
                self.assertEqual(code, 2)
                self.assertIn(text, err)
                self.assertFalse(out.exists())

    def test_the_option_syntax_is_strict(self):
        out = Path(self.out_holder.name) / "syntax.html"
        for args in (["--characters-dir", str(self.user)], ["--out", str(out), "--characters-dir"],
                     ["--out", str(out), "--out", str(out)], ["--out", str(out), "--characters-dir", str(self.user), "extra"]):
            with self.subTest(args=args):
                self.assertEqual(run_build(*args)[0], 2)
        self.assertFalse(out.exists())
        self.assertEqual(run_build("--characters-dir", self.user, "--out", out)[0], 0)  # either order


class DefaultBuildTests(unittest.TestCase):
    def test_the_default_build_is_byte_identical_to_the_baseline(self):
        from fusion_viewer.viewmodel import build_view

        html = render_html(build_view()).encode("utf-8")
        self.assertEqual((len(html), hashlib.sha256(html).hexdigest()), (BASELINE_BYTES, BASELINE_SHA256))

    def test_the_default_page_contains_no_trace_of_the_option(self):
        from fusion_viewer.viewmodel import build_view

        html = render_html(build_view())
        for text in ("FV-EXT", "ownershipRow", "Ownership:", "self-declared", "data-ownership"):
            self.assertNotIn(text, html)

    def test_the_default_build_through_the_command_matches_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "x.html"
            self.assertEqual(run_build("--out", out)[0], 0)
            self.assertEqual(hashlib.sha256(out.read_bytes()).hexdigest(), BASELINE_SHA256)

    def test_the_default_view_carries_no_ownership_data(self):
        from fusion_viewer.viewmodel import build_view

        self.assertTrue(all("ownership" not in c for c in build_view()["characters"]))

    def test_stripping_removes_whole_marked_lines_only(self):
        template = "a\nb // FV-EXT-LINE\n// FV-EXT-BEGIN x\nc\n\n// FV-EXT-END x\nd"
        self.assertEqual(strip_extensions(template), "a\nd")
        self.assertEqual(strip_extensions("no markers\nhere"), "no markers\nhere")

    def test_the_ownership_code_is_in_the_page_only_when_characters_are_loaded(self):
        from fusion_viewer.viewmodel import build_view

        with_ownership = render_html(build_view(ownership={}))
        self.assertIn("ownershipRow", with_ownership)
        self.assertNotIn("ownershipRow", render_html(build_view()))


if __name__ == "__main__":
    unittest.main()
