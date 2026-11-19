"""Build: determinism, safe embedding, output-path rules, and no change to tracked files."""

import copy
import hashlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

from fusion_viewer import build
from fusion_viewer.viewmodel import build_view

from . import REPO_ROOT, run_harness

INJECTION = '</script><img src=x onerror="alert(1)"><!-- &    '
DATA_BLOCK = re.compile(r'<script id="fv-data" type="application/json">([\s\S]*?)</script>')


def watched_hashes() -> dict:
    """Hashes of the code, data and pages the viewer reads or must never change."""
    roots = [REPO_ROOT / "fusion_synthesis", REPO_ROOT / "fusion_engine", REPO_ROOT / "proposer", REPO_ROOT / "fusion_viewer"]
    files = [REPO_ROOT / "server.py", REPO_ROOT / "dashboard.html"]
    for root in roots:
        files += [p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    return {str(p.relative_to(REPO_ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


class BuildTests(unittest.TestCase):
    def run_main(self, args):
        out, err = io.StringIO(), io.StringIO()
        code = build.main(args, stdout=out, stderr=err)
        return code, out.getvalue(), err.getvalue()

    def test_repeated_builds_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "a.html", Path(tmp) / "b.html"
            self.assertEqual(self.run_main(["--out", str(first)])[0], 0)
            self.assertEqual(self.run_main(["--out", str(second)])[0], 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertNotIn(b"\r", first.read_bytes())

    def test_build_writes_only_the_given_file_and_changes_no_tracked_file(self):
        before = watched_hashes()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "viewer.html"
            code, stdout, _ = self.run_main(["--out", str(out)])
            self.assertEqual(code, 0)
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["viewer.html"])
            self.assertIn(hashlib.sha256(out.read_bytes()).hexdigest(), stdout)
        self.assertEqual(watched_hashes(), before)

    def test_output_inside_the_repository_is_refused_and_nothing_is_written(self):
        for target in (REPO_ROOT / "fv_should_not_exist.html", REPO_ROOT / "fusion_viewer" / "fv_should_not_exist.html"):
            with self.subTest(target=target.name):
                code, _out, err = self.run_main(["--out", str(target)])
                self.assertEqual(code, 2)
                self.assertIn("inside the repository", err)
                self.assertFalse(target.exists())

    def test_output_path_must_be_an_explicit_file_in_an_existing_folder(self):
        for args in ([], ["--out"], ["--out", "x", "y"], ["x"], ["--out", "--json"]):
            with self.subTest(args=args):
                self.assertEqual(self.run_main(args)[0], 2)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main(["--out", tmp])[0], 2)
            missing = Path(tmp) / "no_such_folder" / "x.html"
            self.assertEqual(self.run_main(["--out", str(missing)])[0], 2)
            self.assertFalse(missing.parent.exists())

    def test_invalid_authored_data_fails_with_exit_2_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as empty:
            out = Path(tmp) / "x.html"
            err = io.StringIO()
            code = build.main(["--out", str(out)], stdout=io.StringIO(), stderr=err, data_dir=Path(empty))
            self.assertEqual(code, 2)
            self.assertFalse(out.exists())


class EmbeddingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = build_view()
        cls.hostile = copy.deepcopy(cls.view)
        key = next(iter(cls.hostile["pairs"]))
        card = cls.hostile["pairs"][key]["card"]
        card["fusion_name"] = INJECTION
        card["concept"] = INJECTION
        cls.hostile["characters"][0]["name"] = INJECTION
        cls.hostile["notice"] = INJECTION
        cls.html = build.render_html(cls.hostile)

    def test_embedded_json_cannot_close_the_script_block_or_open_markup(self):
        match = DATA_BLOCK.search(self.html)
        block = match.group(1)
        for raw in ("</script", "<", ">", "&", " ", " "):
            self.assertNotIn(raw, block)
        # exactly two script blocks: the data block and the page script
        self.assertEqual(self.html.count("</script>"), 2)
        self.assertEqual(self.html.lower().count("<script"), 2)

    def test_embedded_json_round_trips_exactly(self):
        block = DATA_BLOCK.search(self.html).group(1)
        self.assertEqual(json.loads(block), self.hostile)

    def test_hostile_text_is_rendered_as_text_by_the_page(self):
        snap = run_harness(self.html)
        key = next(iter(self.hostile["pairs"]))
        a, b = self.hostile["pairs"][key]["slugs"]
        shown = [p for p in snap["pairs"] if {p["x"], p["y"]} == {a, b}]
        self.assertEqual(len(shown), 2)
        for page in shown:
            self.assertEqual(page["fusionName"], INJECTION)
            self.assertIn(INJECTION, page["resultText"])
        self.assertEqual(snap["initial"]["footerText"], INJECTION)

    def test_template_placeholder_must_appear_exactly_once(self):
        with self.assertRaises(ValueError):
            build.render_html(self.view, template="no placeholder")
        with self.assertRaises(ValueError):
            build.render_html(self.view, template="__FV_DATA__ __FV_DATA__")


if __name__ == "__main__":
    unittest.main()
