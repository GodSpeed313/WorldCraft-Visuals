"""
Fusion Viewer: build the single-file HTML page.

    python -m fusion_viewer.build --out <file>

Documented output location for normal use: a folder OUTSIDE the repository, for
example %USERPROFILE%\\WorldCraft-Viewer\\fusion_viewer.html (create the folder first;
this script creates nothing but the output file). The page is generated on demand
and is never committed.

The only file this script writes is the path given to --out. It refuses a path
inside the repository tree, because the repository has no ignored output location
for generated HTML. Output is deterministic: the same inputs give the same bytes.
Exit codes: 0 written; 2 bad usage, bad output path, or invalid authored data.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Optional

from fusion_synthesis.schema import SchemaError

from .viewmodel import ViewDataError, build_view

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = Path(__file__).resolve().with_name("template.html")
PLACEHOLDER = "__FV_DATA__"

EXIT_OK, EXIT_BAD = 0, 2

_JSON_ESCAPES = {
    "<": "\\u003c",
    ">": "\\u003e",
    "&": "\\u0026",
    " ": "\\u2028",
    " ": "\\u2029",
}


def embed_json(data: dict) -> str:
    """JSON text that is safe inside a <script type="application/json"> block.

    The characters that could end the block or open markup are written as \\u escapes,
    which JSON.parse reads back to the original text."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for char, escape in _JSON_ESCAPES.items():
        text = text.replace(char, escape)
    return text


def render_html(data: dict, template: Optional[str] = None) -> str:
    if template is None:
        template = TEMPLATE_PATH.read_bytes().decode("utf-8")
    template = template.replace("\r\n", "\n")
    if template.count(PLACEHOLDER) != 1:
        raise ValueError(f"template must contain {PLACEHOLDER} exactly once")
    return template.replace(PLACEHOLDER, embed_json(data))


def check_output_path(out: Path) -> Optional[str]:
    """None if the path is acceptable, else the reason it is refused."""
    resolved = out.resolve()
    if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
        return f"{out} is inside the repository tree; choose a location outside it"
    if resolved.is_dir():
        return f"{out} is a directory; give a file path"
    if not resolved.parent.is_dir():
        return f"{resolved.parent} does not exist; create the folder first"
    return None


def main(argv: Optional[list] = None, stdout=None, stderr=None, data_dir: Optional[Path] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    out_stream = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr

    if len(args) != 2 or args[0] != "--out" or args[1].startswith("--"):
        err.write("usage: python -m fusion_viewer.build --out <file outside the repository>\n")
        return EXIT_BAD
    out = Path(args[1])
    problem = check_output_path(out)
    if problem:
        err.write(f"error: {problem}\n")
        return EXIT_BAD

    try:
        html = render_html(build_view(data_dir))
    except (SchemaError, ViewDataError, ValueError) as exc:
        err.write(f"error: {exc}\n")
        return EXIT_BAD

    payload = html.encode("utf-8")
    out.resolve().write_bytes(payload)
    out_stream.write(f"wrote {len(payload)} bytes, sha256 {hashlib.sha256(payload).hexdigest()}\n")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
