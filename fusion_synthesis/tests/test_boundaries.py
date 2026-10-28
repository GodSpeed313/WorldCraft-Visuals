"""Boundary scans over every .py file of the package and its tests (AUTH-011 §6 test 10).

Rules (AST-based, so comments cannot trip them):
  * No import, by any mechanism, of the legacy governance modules or the server,
    anywhere, INCLUDING inside the one file that holds the registry-binding exception.
  * The identifier for the character registry and the legacy module's file name
    may appear ONLY in test_registry_binding.py. Every other registry name is
    forbidden everywhere.
  * In that one file, additionally: no exec/eval/compile/importlib/runpy/__import__
    and no write-mode file access.
  * No randomness, network or subprocess use anywhere (so: no runtime model call).
  * Standard library, fusion_engine and this package only.
  * No authored character, ability, fusion or proper-noun name appears in any .py file.
  * fusion_engine never imports this package.

Every rule has a negative control that injects the defect and requires detection.
"""

import ast
import re
import sys
import unittest
from pathlib import Path

from fusion_synthesis.loader import load_library

from . import PACKAGE_DIR, REPO_ROOT

# Built by concatenation so this file does not contain the strings it forbids elsewhere.
LEG_CLASSIFIER = "modality_" + "classifier"
LEGACY_MODULES = ("logic_" + "auditor", LEG_CLASSIFIER, "mythos_" + "sync", "ser" + "ver")
CHAR_REG_NAME = "CHARACTER_" + "REGISTRY"
OTHER_REGISTRIES = ("POWER_" + "REGISTRY", "TRANSPOSITION_" + "MAP", "MODALITY_" + "RANK")
NO_RUNTIME_SERVICES = ("random", "socket", "http", "urllib", "subprocess")
DYNAMIC_MODULES = ("importlib", "runpy")
# NOTE: "exec" / "eval" / "compile" / "__import__" below are NAMES the scanner looks for in other
# files' ASTs, and the negative controls feed them to ast.parse() as TEXT. Nothing in this module
# ever calls exec(), eval() or compile(); the scan exists to guarantee the package never does.
DYNAMIC_CALLS = ("exec", "eval", "compile", "__import__")
WRITE_ATTRS = ("write_text", "write_bytes", "unlink", "rename", "replace", "touch", "mkdir", "rmdir")
EXCEPTION_FILE = "test_registry_binding.py"
ALLOWED_ROOTS = set(sys.stdlib_module_names) | {"fusion_engine", "fusion_synthesis"}


def _open_mode(call: ast.Call) -> str:
    if len(call.args) >= 2 and isinstance(call.args[1], ast.Constant) and isinstance(call.args[1].value, str):
        return call.args[1].value
    for kw in call.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return ""


def scan_source(source: str, filename: str) -> list:
    problems = []
    is_exception = filename == EXCEPTION_FILE
    tree = ast.parse(source)

    def check_root(root: str, line: int) -> None:
        if root in LEGACY_MODULES:
            problems.append(f"{filename}:{line}: imports a legacy module ({root})")
        elif root in NO_RUNTIME_SERVICES:
            problems.append(f"{filename}:{line}: imports {root} (no randomness, network or subprocess)")
        elif root in DYNAMIC_MODULES:
            problems.append(f"{filename}:{line}: imports {root} (no dynamic loading)")
        elif root not in ALLOWED_ROOTS:
            problems.append(f"{filename}:{line}: imports non-stdlib module {root}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                check_root(alias.name.split(".")[0], node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                check_root(node.module.split(".")[0], node.lineno)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DYNAMIC_CALLS:
                    problems.append(f"{filename}:{node.lineno}: calls {node.func.id}()")
                if is_exception and node.func.id == "open" and set(_open_mode(node)) & set("wax+"):
                    problems.append(f"{filename}:{node.lineno}: opens a file for writing")
            elif isinstance(node.func, ast.Attribute) and is_exception and node.func.attr in WRITE_ATTRS:
                problems.append(f"{filename}:{node.lineno}: calls .{node.func.attr}() (read-only exception)")
        if isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            name = node.value
        else:
            continue
        for forbidden in OTHER_REGISTRIES:
            if forbidden in name:
                problems.append(f"{filename}:{getattr(node, 'lineno', 0)}: references {forbidden}")
        if not is_exception:
            if CHAR_REG_NAME in name:
                problems.append(f"{filename}:{getattr(node, 'lineno', 0)}: references the character registry")
            if LEG_CLASSIFIER in name:
                problems.append(f"{filename}:{getattr(node, 'lineno', 0)}: references the legacy classifier module")
    return problems


def package_files() -> list:
    return sorted(PACKAGE_DIR.rglob("*.py"))


class RealSourceTests(unittest.TestCase):
    def test_no_file_violates_a_boundary_rule(self):
        files = package_files()
        self.assertGreater(len(files), 10)
        for path in files:
            with self.subTest(file=str(path.relative_to(REPO_ROOT))):
                self.assertEqual(scan_source(path.read_text(encoding="utf-8"), path.name), [])

    def test_the_registry_binding_exception_is_exercised_and_only_there(self):
        holders = [p.name for p in package_files() if LEG_CLASSIFIER in p.read_text(encoding="utf-8")]
        self.assertEqual(holders, [EXCEPTION_FILE])
        text = (PACKAGE_DIR / "tests" / EXCEPTION_FILE).read_text(encoding="utf-8")
        self.assertIn("ast.parse", text)
        self.assertIn("ast.literal_eval", text)

    def test_no_authored_name_appears_in_any_python_file(self):
        library = load_library()
        names = set()
        for card in library.characters.values():
            names.add(card.name)
            names.update(p.name for p in card.properties)
            names.update(card.proper_nouns)
        for pair in library.pairs:
            names.update((pair.fusion_name, pair.emergent.name))
        for path in package_files():
            source = path.read_text(encoding="utf-8")
            for name in sorted(names):
                with self.subTest(file=path.name, name=name):
                    self.assertIsNone(re.search(rf"\b{re.escape(name)}\b", source, re.IGNORECASE),
                                      f"{path.name} contains the authored name {name!r}")

    def test_the_fusion_engine_never_imports_this_package(self):
        for path in sorted((REPO_ROOT / "fusion_engine").rglob("*.py")):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    self.assertFalse(any(a.name.split(".")[0] == "fusion_synthesis" for a in node.names), path.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotEqual(node.module.split(".")[0], "fusion_synthesis", path.name)


class NegativeControls(unittest.TestCase):
    """Each rule must be able to fail."""

    def flagged(self, source, filename="other.py"):
        return scan_source(source, filename)

    def test_legacy_imports_are_flagged_everywhere_including_the_exception_file(self):
        for module in LEGACY_MODULES:
            for filename in ("other.py", EXCEPTION_FILE):
                with self.subTest(module=module, file=filename):
                    self.assertTrue(self.flagged(f"import {module}\n", filename))
                    self.assertTrue(self.flagged(f"from {module} import x\n", filename))

    def test_dynamic_loading_is_flagged(self):
        for source in ("import importlib\n", "import runpy\n", "__import__('os')\n", "exec('1')\n", "eval('1')\n",
                       "compile('1', 'f', 'exec')\n"):
            with self.subTest(source=source):
                self.assertTrue(self.flagged(source))
                self.assertTrue(self.flagged(source, EXCEPTION_FILE))
        self.assertEqual(self.flagged("import re\nre.compile('x')\n"), [])

    def test_randomness_network_and_subprocess_are_flagged(self):
        for module in NO_RUNTIME_SERVICES:
            with self.subTest(module=module):
                self.assertTrue(self.flagged(f"import {module}\n"))
                self.assertTrue(self.flagged(f"from {module}.x import y\n"))

    def test_non_stdlib_imports_are_flagged_but_the_engine_and_package_are_allowed(self):
        self.assertTrue(self.flagged("import requests\n"))
        self.assertEqual(self.flagged("from fusion_engine.types import Source\nfrom . import x\nimport json\n"), [])

    def test_the_legacy_file_name_and_character_registry_are_allowed_only_in_the_exception_file(self):
        literal = LEG_CLASSIFIER + ".py"
        for source in (f"x = {literal!r}\n", f"{CHAR_REG_NAME} = 1\n", f"y = {CHAR_REG_NAME!r}\n"):
            with self.subTest(source=source):
                self.assertTrue(self.flagged(source, "other.py"))
                self.assertEqual(self.flagged(source, EXCEPTION_FILE), [])

    def test_other_registries_are_flagged_even_in_the_exception_file(self):
        for registry in OTHER_REGISTRIES:
            with self.subTest(registry=registry):
                self.assertTrue(self.flagged(f"x = {registry}\n", EXCEPTION_FILE))
                self.assertTrue(self.flagged(f"x = {registry!r}\n", "other.py"))

    def test_write_access_is_flagged_in_the_exception_file_only(self):
        for source in ("open('f', 'w')\n", "open('f', mode='a')\n", "p.write_text('x')\n", "p.unlink()\n"):
            with self.subTest(source=source):
                self.assertTrue(self.flagged(source, EXCEPTION_FILE))
        self.assertEqual(self.flagged("open('f')\np.read_text()\n", EXCEPTION_FILE), [])
        self.assertEqual(self.flagged("p.write_text('x')\n", "other.py"), [])

    def test_clean_source_is_not_flagged(self):
        self.assertEqual(self.flagged("import json\nfrom pathlib import Path\nx = 1\n"), [])


if __name__ == "__main__":
    unittest.main()
