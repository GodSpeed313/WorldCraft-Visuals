"""External authored pairs (AUTH-018): pair files next to user characters, classified by `schema`.

The test pair is a renamed copy of a real authored pair, made from the real library at run time, so no
authored name is typed into this file and the copy passes the real loader. User files live in temporary
folders OUTSIDE the repository."""

import hashlib
import io
import json
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from fusion_synthesis.loader import DATA_DIR, load_library
from fusion_synthesis.schema import CHARACTER_SCHEMA, PAIR_SCHEMA

from fusion_viewer import build, character_check
from fusion_viewer.character_check import check_files, load_view
from fusion_viewer.viewmodel import EXTERNAL_AUTHORED_TEXT, NOT_SYNTHESIZED, build_view

from . import PACKAGE_DIR, REPO_ROOT, run_harness
from .test_original_characters import BASELINE_BYTES, BASELINE_SHA256, run_build, run_check, slug_of

NEW_A, NEW_B, NEW_FUSION = "Orsin Vale", "Pelle Drax", "Vera Tolliver"
FOLDER_NAME = "external_set"


def renamed_trio(library):
    """(file name, text) for two characters and one pair: a renamed copy of the first authored pair."""
    pair = library.pairs[0]
    a, b = library.characters[pair.a], library.characters[pair.b]
    mapping = [
        (pair.slug, f"{slug_of(NEW_A)}__{slug_of(NEW_B)}"),
        (a.slug, slug_of(NEW_A)), (a.name, NEW_A),
        (b.slug, slug_of(NEW_B)), (b.name, NEW_B),
        (pair.fusion_name, NEW_FUSION),
    ]

    def convert(text):
        for old, new in mapping:
            text = text.replace(old, new)
        return text

    out = []
    for kind, source, target in (("characters", a.slug, slug_of(NEW_A)), ("characters", b.slug, slug_of(NEW_B)), ("pairs", pair.slug, f"{slug_of(NEW_A)}__{slug_of(NEW_B)}")):
        out.append((f"{target}.json", convert((DATA_DIR / kind / f"{source}.json").read_text(encoding="utf-8"))))
    return out


class Folder:
    """An external folder with a fixed NAME, inside a private temporary parent."""

    def __init__(self, test):
        self._tmp = tempfile.TemporaryDirectory(prefix="fv-private-")
        test.addCleanup(self._tmp.cleanup)
        self.parent = Path(self._tmp.name)
        self.path = self.parent / FOLDER_NAME
        self.path.mkdir()

    def write(self, name, text):
        target = self.path / name
        target.write_text(text, encoding="utf-8", newline="\n")
        return target

    def snapshot(self):
        return {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in sorted(self.path.iterdir())}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.trio = renamed_trio(cls.library)
        cls.pair_name = cls.trio[2][0]

    def setUp(self):
        self.folder = Folder(self)

    def write_trio(self):
        return [self.folder.write(name, text) for name, text in self.trio]


class ClassifyBySchemaTests(Base):
    def prepared(self, name, data=None, raw=None):
        path = self.folder.path / name
        path.write_bytes(raw if raw is not None else json.dumps(data).encode("utf-8"))
        return character_check._prepare(path)

    def test_exactly_the_pair_schema_is_a_pair_and_exactly_the_character_schema_is_a_character(self):
        self.assertEqual(self.prepared("anything.json", {"schema": PAIR_SCHEMA}).kind, character_check.PAIR)
        self.assertEqual(self.prepared("anything2.json", {"schema": CHARACTER_SCHEMA}).kind, character_check.CHARACTER)

    def test_the_file_name_never_decides_the_kind_even_with_a_double_underscore(self):
        pair_like = self.prepared("looks__like_a_pair.json", {"schema": CHARACTER_SCHEMA})
        plain = self.prepared("plain_name.json", {"schema": PAIR_SCHEMA})
        self.assertEqual(pair_like.kind, character_check.CHARACTER)
        self.assertEqual(plain.kind, character_check.PAIR)

    def test_an_unknown_schema_is_refused_with_the_file_named(self):
        for name, data in (
            ("a.json", {"schema": "fusion-synthesis-pair/2"}),
            ("b.json", {"schema": "fusion-synthesis-style-allowlist/1"}),
            ("c.json", {"schema": "Fusion-Synthesis-Pair/1"}),
            ("d.json", {"schema": PAIR_SCHEMA + " "}),
            ("e.json", {"schema": 7}),
            ("f.json", {"name": "no schema at all"}),
            ("g__h.json", {"schema": None}),
        ):
            with self.subTest(file=name):
                path = self.folder.path / name
                path.write_bytes(json.dumps(data).encode("utf-8"))
                code, out, err = run_check(path)
                self.assertEqual(code, 2)
                self.assertNotIn("OK:", out)
                self.assertIn(name, err)
                self.assertIn("schema", err)
                self.assertIn(CHARACTER_SCHEMA, err)
                self.assertIn(PAIR_SCHEMA, err)

    def test_a_json_list_has_no_schema_and_is_refused_by_name(self):
        path = self.folder.path / "list.json"
        path.write_bytes(b"[1, 2]")
        code, _out, err = run_check(path)
        self.assertEqual(code, 2)
        self.assertIn("list.json", err)

    def test_a_bad_schema_in_a_folder_stops_the_build_and_writes_nothing(self):
        self.write_trio()
        self.folder.write("mystery.json", json.dumps({"schema": "x/9"}))
        out = self.folder.parent / "viewer.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 2)
        self.assertIn("mystery.json", err)
        self.assertFalse(out.exists())


class CheckerPairTests(Base):
    def test_the_renamed_trio_passes_and_the_pair_is_reported_as_a_pair(self):
        paths = self.write_trio()
        code, out, err = run_check(*paths)
        self.assertEqual(code, 0, err)
        self.assertIn(f"OK: {self.pair_name} (authored fusion pair)", out)
        self.assertEqual(out.count("OK:"), 3)

    def test_a_pair_is_checked_with_the_characters_that_passed_whatever_the_argument_order(self):
        paths = self.write_trio()
        for ordered in (paths, list(reversed(paths))):
            code, _out, err = run_check(*ordered)
            self.assertEqual(code, 0, err)

    def test_a_pair_whose_characters_are_missing_names_the_pair_file(self):
        pair_path = self.folder.write(*self.trio[2])
        code, out, err = run_check(pair_path)
        self.assertEqual(code, 2)
        self.assertNotIn("OK:", out)
        self.assertIn(self.pair_name, err)
        self.assertIn("no character card named", err)

    def test_a_character_that_fails_is_blamed_and_the_pair_that_needs_it_names_its_own_file(self):
        a, b, pair = self.write_trio()
        a.write_bytes(b"{")
        code, _out, err = run_check(a, b, pair)
        self.assertEqual(code, 2)
        self.assertIn(a.name, err)
        self.assertIn(pair.name, err)
        self.assertNotIn(f"ERROR: {b.name}", err)

    def test_a_pair_that_would_replace_an_existing_pair_file_is_refused(self):
        existing = self.library.pairs[0]
        source = (DATA_DIR / "pairs" / f"{existing.slug}.json").read_text(encoding="utf-8")
        path = self.folder.write(f"{existing.slug}.json", source)
        code, _out, err = run_check(path)
        self.assertEqual(code, 2)
        self.assertIn(path.name, err)
        self.assertIn("already has a pair file", err)

    def test_a_pair_that_fails_a_loader_rule_is_attributed_to_its_file(self):
        a, b, pair = self.write_trio()
        data = json.loads(pair.read_text(encoding="utf-8"))
        data["trait_outcomes"] = data["trait_outcomes"][:-1]
        pair.write_text(json.dumps(data), encoding="utf-8")
        code, _out, err = run_check(a, b, pair)
        self.assertEqual(code, 2)
        self.assertIn(pair.name, err)

    def test_a_pair_authored_in_both_orders_is_one_conflict_naming_both_files(self):
        first = SimpleNamespace(a="One", b="Two", slug="one__two")
        second = SimpleNamespace(a="Two", b="One", slug="two__one")
        fake = SimpleNamespace(
            characters={"One": SimpleNamespace(name="One", slug="one"), "Two": SimpleNamespace(name="Two", slug="two")},
            pairs=(first, second),
        )
        with mock.patch.object(character_check, "load_library", return_value=fake):
            failure = character_check._load([])
        self.assertIsNotNone(failure)
        self.assertIn("one__two.json", failure)
        self.assertIn("two__one.json", failure)
        self.assertIn("both orders", failure)

    def test_one_pair_in_each_order_is_not_a_conflict_when_the_pairs_are_different(self):
        fake = SimpleNamespace(
            characters={"One": SimpleNamespace(name="One", slug="one"), "Two": SimpleNamespace(name="Two", slug="two"),
                        "Three": SimpleNamespace(name="Three", slug="three")},
            pairs=(SimpleNamespace(a="One", b="Two", slug="one__two"), SimpleNamespace(a="Two", b="Three", slug="two__three")),
        )
        with mock.patch.object(character_check, "load_library", return_value=fake):
            self.assertIsNone(character_check._load([]))

    def test_a_conflict_between_characters_means_pairs_are_not_checked_and_say_so(self):
        a, b, pair = self.write_trio()
        original = character_check._load

        def fake(files):
            if len(files) == 2 and all(item.kind == character_check.CHARACTER for item in files):
                return "a made-up clash"
            return original(files)

        with mock.patch.object(character_check, "_load", side_effect=fake):
            result = check_files([a, b, pair])
        self.assertTrue(any("conflict between" in e and "a made-up clash" in e for e in result.errors))
        self.assertTrue(any(pair.name in e and "not checked" in e for e in result.errors))

    def test_two_pair_files_that_each_pass_alone_conflict_only_in_the_combined_run(self):
        a, b, pair = self.write_trio()
        other = self.folder.write("second_pair.json", json.dumps({"schema": PAIR_SCHEMA}))

        def fake(files):
            return "a made-up pair clash" if sum(item.kind == character_check.PAIR for item in files) >= 2 else None

        with mock.patch.object(character_check, "_load", side_effect=lambda files: fake(files) if files else None):
            result = check_files([a, b, pair, other])
        self.assertEqual(len(result.errors), 1)
        self.assertIn("conflict between", result.errors[0])
        self.assertIn(pair.name, result.errors[0])
        self.assertIn(other.name, result.errors[0])
        self.assertIn("a made-up pair clash", result.errors[0])

    def test_the_checker_still_copies_no_library_rule(self):
        source = (PACKAGE_DIR / "character_check.py").read_text(encoding="utf-8")
        for name in ("parse_pair", "validate_pair", "pair_denylist", "slugify", "SLOTS"):
            self.assertNotIn(name, source, name)


class BuildWithExternalPairTests(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.holder = tempfile.TemporaryDirectory(prefix="fv-private-")
        cls.addClassCleanup(cls.holder.cleanup)
        cls.parent = Path(cls.holder.name)
        cls.user = cls.parent / FOLDER_NAME
        cls.user.mkdir()
        for name, text in cls.trio:
            (cls.user / name).write_text(text, encoding="utf-8", newline="\n")
        cls.out = cls.parent / "viewer.html"
        code, _o, err = run_build("--out", cls.out, "--characters-dir", cls.user)
        assert code == 0, err
        cls.html = cls.out.read_text(encoding="utf-8")
        cls.view = load_view(sorted(cls.user.glob("*.json")))
        cls.snap = run_harness(cls.html)
        cls.by_selection = {(p["x"], p["y"]): p for p in cls.snap["pairs"]}
        cls.slug_a, cls.slug_b = slug_of(NEW_A), slug_of(NEW_B)

    def test_the_counts_are_the_repository_plus_the_files(self):
        base = len(self.library.characters)
        n = base + 2
        self.assertEqual(len(self.view["characters"]), n)
        self.assertEqual(len(self.view["combinations"]), n * (n - 1) // 2)
        self.assertEqual(len(self.view["pairs"]), len(self.library.pairs) + 1)

    def test_the_fusion_exists_only_as_a_card_never_as_a_character(self):
        names = [c["name"] for c in self.view["characters"]]
        self.assertNotIn(NEW_FUSION, names)
        self.assertIn(NEW_A, names)
        self.assertIn(NEW_B, names)
        self.assertEqual(self.view["pairs"][f"{self.slug_a}__{self.slug_b}"]["card"]["fusion_name"], NEW_FUSION)

    def test_the_pair_resolves_to_the_fusion_in_both_selection_orders(self):
        for x, y in ((self.slug_a, self.slug_b), (self.slug_b, self.slug_a)):
            page = self.by_selection[(x, y)]
            with self.subTest(selection=(x, y)):
                self.assertEqual(page["fusionName"], NEW_FUSION)
                self.assertIsNone(page["missingText"])
                self.assertEqual(sorted(page["selected"]), sorted([self.slug_a, self.slug_b]))

    def test_the_comparison_panel_shows_both_parents(self):
        page = self.by_selection[(self.slug_a, self.slug_b)]
        self.assertTrue(page["comparisonPresent"])
        self.assertIn(NEW_A, page["comparisonText"])
        self.assertIn(NEW_B, page["comparisonText"])
        self.assertTrue(page["comparisonTraits"])

    def test_an_unauthored_pair_still_reads_not_yet_synthesized(self):
        other = next(c["slug"] for c in self.view["characters"] if c["slug"] not in (self.slug_a, self.slug_b))
        page = self.by_selection[(self.slug_a, other)]
        self.assertEqual(page["missingText"], NOT_SYNTHESIZED)

    def test_the_status_says_manually_authored_loader_validated_and_no_golden(self):
        text = EXTERNAL_AUTHORED_TEXT.lower()
        self.assertIn("manually authored", text)
        self.assertIn("validated by the existing library loader", text)
        self.assertIn("no operator-approved golden snapshot", text)
        page = self.by_selection[(self.slug_a, self.slug_b)]
        for needle in ("manually authored", "validated by the existing library loader", "no operator-approved golden snapshot"):
            self.assertIn(needle, page["detailsText"])
        self.assertIn(FOLDER_NAME, page["detailsText"])
        self.assertNotIn("repository's authored data", page["detailsText"])

    def test_no_external_card_makes_a_golden_equivalence_claim(self):
        record = self.view["pairs"][f"{self.slug_a}__{self.slug_b}"]
        blob = json.dumps(record["status"]).lower()
        for word in ("equals the golden", "matches the golden", "identical to the golden", "operator-approved golden json"):
            self.assertNotIn(word, blob)
        self.assertEqual(blob.count("golden"), 1)  # the one mention is "no operator-approved golden snapshot"
        self.assertFalse((DATA_DIR / "golden" / f"{self.slug_a}__{self.slug_b}.json").exists())

    def test_repository_cards_keep_their_status_byte_for_byte(self):
        plain = build_view()
        for key, record in plain["pairs"].items():
            with self.subTest(pair=key):
                self.assertEqual(json.dumps(self.view["pairs"][key]["status"], sort_keys=True), json.dumps(record["status"], sort_keys=True))
                self.assertIn("repository's authored data", record["status"]["authored"]["text"])
                self.assertIn(record["status"]["authored"]["source_file"], {f"pairs/{p.slug}.json" for p in self.library.pairs})

    def test_two_builds_are_byte_identical(self):
        again = self.parent / "again.html"
        code, _o, err = run_build("--out", again, "--characters-dir", self.user)
        self.assertEqual(code, 0, err)
        self.assertEqual(again.read_bytes(), self.out.read_bytes())


class NoPrivatePathTests(Base):
    """AUTH-018 amendment 1: no absolute local path anywhere in the built page."""

    def forbidden(self, folder):
        parent = folder.parent
        needles = {
            str(folder), str(folder.resolve()), folder.as_posix(), folder.resolve().as_posix(),
            str(parent), parent.as_posix(), str(parent.resolve()), parent.resolve().as_posix(),
            str(Path.home()), Path.home().as_posix(), tempfile.gettempdir(), Path(tempfile.gettempdir()).as_posix(),
            str(REPO_ROOT), REPO_ROOT.as_posix(), "fv-private-", "fv-check-",
        }
        escaped = {n.replace("\\", "\\\\") for n in needles}
        return {n.lower() for n in needles | escaped if n}

    def test_a_page_built_from_an_external_folder_contains_no_absolute_local_path(self):
        self.write_trio()
        out = self.folder.parent / "viewer.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 0, err)
        html = out.read_text(encoding="utf-8")
        low = html.lower()
        for needle in self.forbidden(self.folder.path):
            self.assertNotIn(needle, low, f"page contains {needle!r}")
        self.assertIsNone(re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", html), "a drive-letter path is in the page")
        self.assertIsNone(re.search(r"\\\\[A-Za-z0-9_.$-]+\\[A-Za-z0-9_.$-]+", html), "a network path is in the page")
        self.assertIsNone(re.search(r"(?<![A-Za-z0-9:/.])/(users|home|tmp|var|private|mnt)/", low), "a unix-style path is in the page")
        self.assertIn(FOLDER_NAME, html)  # only the folder's NAME is shown

    def test_the_page_data_holds_no_path_either(self):
        self.write_trio()
        view = load_view(sorted(self.folder.path.glob("*.json")))
        data = json.dumps(view).lower()
        for needle in self.forbidden(self.folder.path):
            self.assertNotIn(needle, data)

    def test_the_path_scan_would_catch_a_leaked_path(self):
        leaked = f"<p>Source: {self.folder.path}</p>"
        self.assertTrue(any(n in leaked.lower() for n in self.forbidden(self.folder.path)))
        self.assertIsNotNone(re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", "see C:\\Users\\someone\\file"))

    def test_the_default_page_passes_the_same_scan(self):
        html = build.render_html(build_view())
        low = html.lower()
        for needle in self.forbidden(self.folder.path):
            self.assertNotIn(needle, low)
        self.assertIsNone(re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", html))


class SafetyAndBaselineTests(Base):
    def test_the_user_folder_is_only_read_with_pairs_in_it(self):
        self.write_trio()
        self.folder.write("broken.json", "{")
        before = self.folder.snapshot()
        run_check(*sorted(self.folder.path.iterdir()))
        run_build("--out", self.folder.parent / "never.html", "--characters-dir", self.folder.path)
        self.assertEqual(self.folder.snapshot(), before)

    def test_authored_data_is_not_changed_by_checking_or_building_a_pair(self):
        def tree():
            return {str(p.relative_to(DATA_DIR)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA_DIR.rglob("*")) if p.is_file()}

        before = tree()
        self.write_trio()
        run_check(*sorted(self.folder.path.iterdir()))
        run_build("--out", self.folder.parent / "x.html", "--characters-dir", self.folder.path)
        self.assertEqual(tree(), before)

    def test_nothing_is_left_behind_after_a_pair_check_passes_or_fails(self):
        before = set(Path(tempfile.gettempdir()).glob("fv-check-*"))
        paths = self.write_trio()
        run_check(*paths)
        run_check(paths[2])
        self.assertEqual(set(Path(tempfile.gettempdir()).glob("fv-check-*")), before)

    def test_the_default_build_is_still_byte_identical_to_the_baseline(self):
        html = build.render_html(build_view()).encode("utf-8")
        self.assertEqual((len(html), hashlib.sha256(html).hexdigest()), (BASELINE_BYTES, BASELINE_SHA256))

    def test_a_build_without_the_option_is_byte_identical_through_the_command(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(build.main(["--out", str(self.folder.parent / "d.html")]), 0)
        self.assertEqual(hashlib.sha256((self.folder.parent / "d.html").read_bytes()).hexdigest(), BASELINE_SHA256)


if __name__ == "__main__":
    unittest.main()
