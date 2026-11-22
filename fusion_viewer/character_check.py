"""
Fusion Viewer: check original character files and load them for the viewer (AUTH-017).

    python -m fusion_viewer.character_check <file> [<file> ...]

A user character file is validated by the existing fusion_synthesis loader, not by rules
copied here. For each run the checker makes a temporary copy of the complete authored data
directory, adds the user file(s) to the copy, strips the viewer-side `ownership` field from the
copy only, and calls fusion_synthesis.loader.load_library on the copy.

Failures are attributed by staging, never by reading file names out of an error message:
  1. the repository data alone must load;
  2. each user file is loaded on its own, in its own temporary library;
  3. all files that passed are then loaded together in one more library. A failure that appears
     only there is reported as a conflict between the files involved.

`ownership` (original, public_domain, third_party_ip, licensed) is the file author's own
statement. It is checked against the four values and kept beside the file; it is never inferred
and never verified. The user's folder is only read. Every temporary directory is removed on exit.

Exit codes: 0 every file passed; 2 a file failed, a conflict was found, or bad usage.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterator, Optional

from fusion_synthesis.loader import DATA_DIR, load_library, read_json
from fusion_synthesis.schema import SchemaError

from .viewmodel import OWNERSHIP_LABELS, OWNERSHIP_VALUES, build_view

EXIT_OK, EXIT_BAD = 0, 2

BOM_ADVICE = "starts with a UTF-8 byte-order mark (BOM). Save the file as plain UTF-8 without a BOM."


class UserCharacterError(ValueError):
    """One or more user character files failed. `messages` holds one plain line per problem."""

    def __init__(self, messages: list):
        super().__init__("\n".join(messages))
        self.messages = list(messages)


class _Collision(Exception):
    """Two files cannot be placed in one library because they have the same file name."""


@dataclass(frozen=True)
class _Prepared:
    path: Path
    staged: bytes  # exactly what is written into the temporary copy (ownership field removed)
    ownership: Optional[str]


@dataclass(frozen=True)
class CheckResult:
    errors: tuple  # plain messages; empty when every file passed
    files: tuple  # _Prepared, only for files that passed on their own


def _plain(name: str, raw: str) -> str:
    """A plain one-line message that names the file and keeps the loader's own cause."""
    if "UTF-8 BOM" in raw:
        return f"{name}: {BOM_ADVICE}"
    doubled = f"{name}: {name}"
    while raw.startswith(doubled):
        raw = raw[len(name) + 2 :]
    return raw if raw.startswith(name) else f"{name}: {raw}"


def _prepare(path: Path) -> "_Prepared | str":
    """Read one user file. Returns the staged file, or a plain error message."""
    name = path.name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return f"{name}: cannot be read ({exc.strerror or exc})"
    try:
        data = read_json(path)  # same reader as the loader, so duplicate keys and a BOM are seen the same way
    except SchemaError:
        return _Prepared(path, raw, None)  # let load_library report the cause; ownership cannot be read
    if not (isinstance(data, dict) and "ownership" in data):
        return _Prepared(path, raw, None)
    value = data["ownership"]
    if not isinstance(value, str) or value not in OWNERSHIP_VALUES:
        return f"{name}: ownership {value!r} is not one of {list(OWNERSHIP_VALUES)}"
    rest = {k: v for k, v in data.items() if k != "ownership"}
    return _Prepared(path, json.dumps(rest, ensure_ascii=False, indent=2).encode("utf-8"), value)


@contextmanager
def _staged_library(files: list) -> Iterator[Path]:
    """A temporary copy of the whole authored data directory plus the given user files.

    The directory is always removed, including when the body raises."""
    with tempfile.TemporaryDirectory(prefix="fv-check-") as tmp:
        root = Path(tmp) / "data"
        shutil.copytree(DATA_DIR, root)
        characters = root / "characters"
        placed: dict = {}
        for item in files:
            target = characters / item.path.name
            if target.exists():
                if item.path.name in placed:
                    raise _Collision(
                        f"{placed[item.path.name]} and {item.path} would both be {item.path.name}; "
                        "one library cannot hold two character files with the same file name"
                    )
                raise _Collision(
                    f"{item.path.name}: the authored data already has a character file with this name, "
                    "so this would replace an existing character. Use a different character name"
                )
            target.write_bytes(item.staged)
            placed[item.path.name] = item.path
        yield root


def _load(files: list) -> Optional[str]:
    """Load the library with these user files. None if it loads, else the raw failure text."""
    try:
        with _staged_library(files) as root:
            load_library(root)
    except (SchemaError, _Collision) as exc:
        return str(exc)
    return None


def check_files(paths: list) -> CheckResult:
    paths = [Path(p) for p in paths]
    problem = _load([])
    if problem is not None:
        raise RuntimeError(f"the repository's authored data does not load, so no file can be checked: {problem}")

    errors, passed = [], []
    for path in paths:
        prepared = _prepare(path)
        if isinstance(prepared, str):
            errors.append(prepared)
            continue
        failure = _load([prepared])
        if failure is not None:
            errors.append(_plain(path.name, failure))
        else:
            passed.append(prepared)

    if len(passed) > 1 and _load(passed) is not None:
        pair_failures = []
        for first, second in combinations(passed, 2):
            failure = _load([first, second])
            if failure is not None:
                pair_failures.append(f"conflict between {first.path.name} and {second.path.name}: {failure}")
        if pair_failures:
            errors.extend(pair_failures)
        else:
            names = ", ".join(item.path.name for item in passed)
            errors.append(f"conflict among {names}: each loads alone but not together: {_load(passed)}")
    return CheckResult(tuple(errors), tuple(passed))


def load_view(paths: list) -> dict:
    """The viewer's data with the user characters added, or UserCharacterError with every problem."""
    result = check_files(paths)
    if result.errors:
        raise UserCharacterError(list(result.errors))
    with _staged_library(list(result.files)) as root:
        # The library's own rule makes each file stem equal the character's slug.
        declared = {item.path.stem: item.ownership for item in result.files}
        return build_view(root, ownership=declared)


def main(argv: Optional[list] = None, stdout=None, stderr=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    if not args or any(a.startswith("--") for a in args):
        err.write("usage: python -m fusion_viewer.character_check <character file> [<character file> ...]\n")
        return EXIT_BAD
    try:
        result = check_files(args)
    except RuntimeError as exc:
        err.write(f"error: {exc}\n")
        return EXIT_BAD
    for item in result.files:
        label = OWNERSHIP_LABELS.get(item.ownership, "not recorded")
        out.write(f"OK: {item.path.name} (ownership: {label}; a self-declaration, not verified)\n")
    for message in result.errors:
        err.write(f"ERROR: {message}\n")
    return EXIT_BAD if result.errors else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
