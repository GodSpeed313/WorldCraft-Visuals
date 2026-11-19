"""
Test support for fusion_viewer.

Tests discover the real authored characters and pairs through the existing loader;
no authored name is written into any .py file of this package.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = REPO_ROOT / "fusion_viewer"
HARNESS = Path(__file__).resolve().with_name("harness.js")
GOLDEN_DIR = REPO_ROOT / "fusion_synthesis" / "data" / "golden"


def run_harness(html: str) -> dict:
    """Run the page's real script under node with a fake DOM and return what it rendered.

    The harness has no network objects and no innerHTML, so a page that uses either fails here."""
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("node is required to run the fusion_viewer page tests and was not found on PATH")
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_bytes(html.encode("utf-8"))
        proc = subprocess.run([node, str(HARNESS), str(page)], capture_output=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError("harness failed: " + proc.stderr.decode("utf-8", "replace"))
    return json.loads(proc.stdout.decode("utf-8"))
