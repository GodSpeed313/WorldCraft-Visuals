"""
Fusion Viewer: build the single-file HTML page.

    python -m fusion_viewer.build --out <file> [--characters-dir <folder>]

Documented output location for normal use: a folder OUTSIDE the repository, for
example %USERPROFILE%\\WorldCraft-Viewer\\fusion_viewer.html (create the folder first;
this script creates nothing but the output file). The page is generated on demand
and is never committed.

--characters-dir loads the user's own character files (*.json) from a folder OUTSIDE the
repository and adds them to the viewer (AUTH-017). The same folder may also hold authored fusion
pair files (AUTH-018); each file's kind is read from its `schema` field, never from its name. They
are checked with the existing loader by fusion_viewer.character_check; the folder is only read, and
the page shows only the folder's NAME, never a path. Without the option nothing changes: the output
is byte-identical to a build that never heard of it.

A character file in that folder may also carry `fusion_origin` ({"pair": "<pair slug>"}), recording the
authored fusion pair it was written from (AUTH-019). The checker compares the profile with that pair,
word for word, on its seven appearance slots and its ability's name and description, and on nothing
else; a profile that does not match stops the build. The card of any fusion with a promoted parent
says what was compared. This is a record of origin, not a claim that the profile inherits from it.

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

from .character_check import UserCharacterError, load_view
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


EXT_BEGIN, EXT_END, EXT_LINE = "FV-EXT-BEGIN", "FV-EXT-END", "FV-EXT-LINE"


def strip_extensions(template: str) -> str:
    """The template without its optional (ownership) lines: whole lines only, so what is left is
    byte-for-byte the page that existed before the option."""
    kept, inside = [], False
    for line in template.split("\n"):
        if EXT_BEGIN in line:
            inside = True
        if not inside and EXT_LINE not in line:
            kept.append(line)
        if EXT_END in line:
            inside = False
    return "\n".join(kept)


def render_html(data: dict, template: Optional[str] = None) -> str:
    if template is None:
        template = TEMPLATE_PATH.read_bytes().decode("utf-8")
    template = template.replace("\r\n", "\n")
    if not any("ownership" in c for c in data.get("characters", ())):
        template = strip_extensions(template)
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


def character_files(folder: Path) -> tuple:
    """(the *.json files of a user's character folder, or None) and a problem text (or None)."""
    resolved = folder.resolve()
    if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
        return None, f"{folder} is inside the repository tree; keep your own characters in a folder outside it"
    if not resolved.is_dir():
        return None, f"{folder} is not a folder"
    files = sorted(p for p in resolved.glob("*.json") if p.is_file())
    if not files:
        return None, f"{folder} has no .json character files"
    return files, None


def main(argv: Optional[list] = None, stdout=None, stderr=None, data_dir: Optional[Path] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    out_stream = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr

    usage = "usage: python -m fusion_viewer.build --out <file outside the repository> [--characters-dir <folder outside the repository>]\n"
    options = {}
    rest = list(args)
    while rest:
        if len(rest) < 2 or rest[0] not in ("--out", "--characters-dir") or rest[0] in options or rest[1].startswith("--"):
            err.write(usage)
            return EXIT_BAD
        options[rest[0]] = rest[1]
        rest = rest[2:]
    if "--out" not in options:
        err.write(usage)
        return EXIT_BAD
    out = Path(options["--out"])
    problem = check_output_path(out)
    if problem:
        err.write(f"error: {problem}\n")
        return EXIT_BAD

    try:
        if "--characters-dir" in options:
            files, problem = character_files(Path(options["--characters-dir"]))
            if problem:
                err.write(f"error: {problem}\n")
                return EXIT_BAD
            view = load_view(files)
        else:
            view = build_view(data_dir)
        html = render_html(view)
    except UserCharacterError as exc:
        for message in exc.messages:
            err.write(f"error: {message}\n")
        return EXIT_BAD
    except (SchemaError, ViewDataError, ValueError, RuntimeError) as exc:
        err.write(f"error: {exc}\n")
        return EXIT_BAD

    payload = html.encode("utf-8")
    out.resolve().write_bytes(payload)
    out_stream.write(f"wrote {len(payload)} bytes, sha256 {hashlib.sha256(payload).hexdigest()}\n")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
