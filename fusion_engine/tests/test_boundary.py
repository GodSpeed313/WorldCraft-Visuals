"""
Mechanical enforcement of the AUTH-004 / ADR-001 AD-1 architectural boundary.

This is a regression guard, not a one-time check: it fails loudly if any
future edit inside the fusion_engine package introduces a forbidden import
of an existing WorldCraft-Visuals application module, or a reference into
the legacy governance layer's registries or resolution functions.

Scoped to the known set of existing top-level application modules, not a
generalized import linter — new legacy modules would need to be added here
by name if the exclusion list this guards ever grows.
"""

import pathlib
import unittest

_LEGACY_MODULE_PREFIXES = (
    "logic_auditor",
    "modality_classifier",
    "mythos_sync",
    "console",
    "server",
    "fantasy_kingdom_generator",
)
_FORBIDDEN_REFERENCES = (
    "CHARACTER_REGISTRY",
    "POWER_REGISTRY",
    "classify_fusion(",
    "audit_power(",
    "ground_power(",
    "classify(",
)

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _imports_legacy_module(text: str) -> list[str]:
    hits = []
    for prefix in _LEGACY_MODULE_PREFIXES:
        if f"import {prefix}" in text or f"from {prefix}" in text or f"from .{prefix}" in text:
            hits.append(prefix)
    return hits


class TestArchitecturalBoundary(unittest.TestCase):
    def test_no_forbidden_imports_or_references(self):
        offenders = []
        for path in PACKAGE_ROOT.rglob("*.py"):
            relative_parts = path.relative_to(PACKAGE_ROOT).parts
            if "tests" in relative_parts:
                continue  # this file itself legitimately names the forbidden strings
            text = path.read_text(encoding="utf-8")

            for legacy_module in _imports_legacy_module(text):
                offenders.append((str(path), f"imports {legacy_module}"))
            for needle in _FORBIDDEN_REFERENCES:
                if needle in text:
                    offenders.append((str(path), needle))

        self.assertEqual(offenders, [], f"Forbidden references found: {offenders}")


if __name__ == "__main__":
    unittest.main()
