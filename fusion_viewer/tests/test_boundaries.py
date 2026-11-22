"""Boundary scan of the production modules of fusion_viewer (AST-based).

Rules for viewmodel.py, build.py and __init__.py:
  * standard library, fusion_synthesis and fusion_viewer only;
  * no network, randomness or subprocess use, and no model/provider modules;
  * no import of the legacy engine, the server or the proposer;
  * no dynamic code execution.
The test files may use subprocess (to run node) and are not scanned by these rules.
Each rule has a negative control that injects the defect and requires detection.
"""

import ast
import sys
import unittest

from . import PACKAGE_DIR

# NOTE: "exec" / "eval" / "compile" / "__import__" below are NAMES the scanner looks for in other
# files' ASTs, and the negative controls feed them to ast.parse() as TEXT. Nothing in this module
# ever calls exec() or eval(); the scan exists to guarantee the package never does.
FORBIDDEN = {
    "random", "socket", "http", "urllib", "subprocess", "ssl", "ftplib", "smtplib", "requests", "anthropic",
    "importlib", "runpy", "ctypes",
    "proposer", "server", "mythos_sync", "logic_auditor", "modality_classifier", "console",
}
DYNAMIC_CALLS = {"exec", "eval", "compile", "__import__"}
ALLOWED_ROOTS = set(sys.stdlib_module_names) | {"fusion_synthesis", "fusion_viewer"}
PRODUCTION = ("__init__.py", "viewmodel.py", "build.py", "character_check.py")


def scan(source: str, filename: str) -> list:
    problems = []
    for node in ast.walk(ast.parse(source)):
        roots = []
        if isinstance(node, ast.Import):
            roots = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots = [node.module.split(".")[0]]
        for root in roots:
            if root in FORBIDDEN:
                problems.append(f"{filename}:{node.lineno}: imports {root}")
            elif root not in ALLOWED_ROOTS:
                problems.append(f"{filename}:{node.lineno}: imports non-stdlib module {root}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CALLS:
            problems.append(f"{filename}:{node.lineno}: calls {node.func.id}()")
    return problems


class RealSourceTests(unittest.TestCase):
    def test_production_modules_respect_every_boundary(self):
        for name in PRODUCTION:
            with self.subTest(file=name):
                self.assertEqual(scan((PACKAGE_DIR / name).read_text(encoding="utf-8"), name), [])

    def test_the_production_list_is_complete(self):
        present = sorted(p.name for p in PACKAGE_DIR.glob("*.py"))
        self.assertEqual(present, sorted(PRODUCTION))


class NegativeControls(unittest.TestCase):
    def flagged(self, source):
        return scan(source, "x.py")

    def test_network_random_subprocess_and_provider_imports_are_flagged(self):
        for source in ("import socket\n", "import random\n", "import subprocess\n", "from urllib import request\n",
                       "import anthropic\n", "import requests\n", "from http.client import HTTPSConnection\n"):
            self.assertTrue(self.flagged(source), source)

    def test_legacy_server_and_proposer_imports_are_flagged(self):
        for source in ("import server\n", "from proposer import packet\n", "import mythos_sync\n", "import logic_auditor\n"):
            self.assertTrue(self.flagged(source), source)

    def test_third_party_and_dynamic_code_are_flagged(self):
        for source in ("import numpy\n", "eval('1')\n", "exec('x=1')\n", "__import__('os')\n", "import importlib\n"):
            self.assertTrue(self.flagged(source), source)

    def test_clean_source_is_not_flagged(self):
        self.assertEqual(self.flagged("import json\nfrom fusion_synthesis.loader import load_library\n"), [])


if __name__ == "__main__":
    unittest.main()
