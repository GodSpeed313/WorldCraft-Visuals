"""
Fusion Viewer: check original character files and authored pair files, and load them for the viewer
(AUTH-017 characters, AUTH-018 pairs, AUTH-019 promoted profiles).

    python -m fusion_viewer.character_check <file> [<file> ...]

A user file is validated by the existing fusion_synthesis loader, not by rules copied here. For
each run the checker makes a temporary copy of the complete authored data directory, adds the user
file(s) to the copy, strips the viewer-side `ownership` field from a character copy only, and calls
fusion_synthesis.loader.load_library on the copy.

The kind of each file comes from its `schema` field and nothing else: exactly
`fusion-synthesis-character/1` is a character, exactly `fusion-synthesis-pair/1` is an authored
fusion pair. A file name, including a `__` in it, is never used to guess the kind. Any other schema
value is refused with a message that names the file. A file whose JSON cannot be read has no
readable schema, so it is passed to the loader as a character and the loader reports the cause.

Failures are attributed by staging, never by reading file names out of an error message:
  1. the repository data alone must load;
  2. each character file is loaded on its own, in its own temporary library;
  3. the character files that passed are loaded together in one more library; a failure that
     appears only there is reported as a conflict between the files involved;
  4. each pair file is loaded on its own with the character files that passed (a pair needs its
     two characters, which may be repository characters or user characters);
  5. the pair files that passed are then loaded together; a failure that appears only there is
     reported as a conflict between the files involved. A pair authored in both orders (A x B and
     B x A) is one such failure, because the viewer treats pairs as unordered.
  6. origin verification (AUTH-019), only for a character file that carries `fusion_origin`, and only
     once, against the library loaded with every file that passed. It is never part of stages 2-5.

`fusion_origin` ({"pair": "<pair slug>"}) says which authored fusion pair a character profile was
written from. It is a viewer-side field, removed from the staged copy as `ownership` is, so the loader
never sees it. Reading a file checks its shape only. Stage 6 then compares the profile with that pair,
word for word: the profile's name with the pair's fusion name, its seven appearance slots with the
pair's, and its ability's name and description with the pair's. That is all it shows. It does not show
that the profile inherits everything the origin card records, and it adds no origin parent's proper
nouns to the profile's denylist. Slice 1 records first-generation promotions only: a pair that has a
promoted parent cannot be an origin.

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
from fusion_synthesis.schema import CHARACTER_SCHEMA, PAIR_SCHEMA, SchemaError

from .viewmodel import OWNERSHIP_LABELS, OWNERSHIP_VALUES, build_view, pair_key

CHARACTER, PAIR = "character", "pair"

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
    kind: str = CHARACTER  # CHARACTER or PAIR, taken from the file's schema field
    origin: Optional[str] = None  # the pair slug a promoted profile names in `fusion_origin` (AUTH-019)


@dataclass(frozen=True)
class CheckResult:
    errors: tuple  # plain messages; empty when every file passed
    files: tuple  # _Prepared, only for files that passed (characters first, then pairs)


def _plain(name: str, raw: str) -> str:
    """A plain one-line message that names the file and keeps the loader's own cause."""
    if "UTF-8 BOM" in raw:
        return f"{name}: {BOM_ADVICE}"
    doubled = f"{name}: {name}"
    while raw.startswith(doubled):
        raw = raw[len(name) + 2 :]
    return raw if raw.startswith(name) else f"{name}: {raw}"


def _origin_slug(value, name: str) -> "tuple[Optional[str], Optional[str]]":
    """(the pair slug, None) from a `fusion_origin` value, or (None, a plain message naming the file).

    Shape only. Whether the pair exists, and whether it matches the profile, is stage 6's question."""
    where = f"{name}: fusion_origin"
    if not isinstance(value, dict):
        return None, f'{where} must be an object like {{"pair": "<pair slug>"}}'
    if set(value) != {"pair"}:
        extra = sorted(str(k) for k in value if k != "pair")
        detail = f"unexpected key(s) {extra}" if extra else 'the key "pair" is missing'
        return None, f'{where} must have exactly one key, "pair"; {detail}'
    slug = value["pair"]
    if not isinstance(slug, str) or not slug.strip():
        return None, f"{where}.pair must be a non-empty string (the slug of an authored fusion pair)"
    return slug, None


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
    schema = data.get("schema") if isinstance(data, dict) else None
    if schema == PAIR_SCHEMA:
        return _Prepared(path, raw, None, PAIR)
    if schema != CHARACTER_SCHEMA:
        shown = "has no schema field" if not (isinstance(data, dict) and "schema" in data) else f"has an unknown schema {schema!r}"
        return f"{name}: {shown}; a character file uses {CHARACTER_SCHEMA!r} and an authored fusion pair uses {PAIR_SCHEMA!r}"
    if "ownership" not in data and "fusion_origin" not in data:
        return _Prepared(path, raw, None)
    value = None
    if "ownership" in data:
        value = data["ownership"]
        if not isinstance(value, str) or value not in OWNERSHIP_VALUES:
            return f"{name}: ownership {value!r} is not one of {list(OWNERSHIP_VALUES)}"
    origin = None
    if "fusion_origin" in data:
        origin, problem = _origin_slug(data["fusion_origin"], name)
        if problem is not None:
            return problem
    rest = {k: v for k, v in data.items() if k not in ("ownership", "fusion_origin")}
    return _Prepared(path, json.dumps(rest, ensure_ascii=False, indent=2).encode("utf-8"), value, CHARACTER, origin)


@contextmanager
def _staged_library(files: list) -> Iterator[Path]:
    """A temporary copy of the whole authored data directory plus the given user files.

    Character files go into characters/ and pair files into pairs/. The directory is always removed,
    including when the body raises."""
    with tempfile.TemporaryDirectory(prefix="fv-check-") as tmp:
        root = Path(tmp) / "data"
        shutil.copytree(DATA_DIR, root)
        placed: dict = {}
        for item in files:
            folder = "characters" if item.kind == CHARACTER else "pairs"
            what = "character" if item.kind == CHARACTER else "pair"
            target = root / folder / item.path.name
            if target.exists():
                if (folder, item.path.name) in placed:
                    raise _Collision(
                        f"{placed[(folder, item.path.name)]} and {item.path} would both be {item.path.name}; "
                        f"one library cannot hold two {what} files with the same file name"
                    )
                raise _Collision(
                    f"{item.path.name}: the authored data already has a {what} file with this name, "
                    f"so this would replace an existing {what}. Use a different {what} name"
                )
            target.write_bytes(item.staged)
            placed[(folder, item.path.name)] = item.path
        yield root


def _load(files: list) -> Optional[str]:
    """Load the library with these user files. None if it loads, else the raw failure text."""
    try:
        with _staged_library(files) as root:
            library = load_library(root)
            slug_of = {card.name: card.slug for card in library.characters.values()}
            seen: dict = {}
            for pair in library.pairs:
                key = pair_key(slug_of[pair.a], slug_of[pair.b])
                if key in seen:
                    return (
                        f"pair {pair.a!r} x {pair.b!r} is authored in both orders ({seen[key]} and {pair.slug}.json); "
                        "the viewer treats pairs as unordered"
                    )
                seen[key] = f"{pair.slug}.json"
    except (SchemaError, _Collision) as exc:
        return str(exc)
    return None


def _combined(items: list, base: list, errors: list) -> None:
    """Load `items` together on top of `base`; if that fails, name the pairs of files that conflict."""
    if len(items) < 2 or _load(base + items) is None:
        return
    found = []
    for first, second in combinations(items, 2):
        failure = _load(base + [first, second])
        if failure is not None:
            found.append(f"conflict between {first.path.name} and {second.path.name}: {failure}")
    if found:
        errors.extend(found)
    else:
        names = ", ".join(item.path.name for item in items)
        errors.append(f"conflict among {names}: each loads alone but not together: {_load(base + items)}")


def _verify_origins(library, promoted: list) -> list:
    """Stage 6 (AUTH-019): compare each promoted profile with the pair it names, in the complete staged library.

    Returns (profile, message) for every failed check; empty when every profile matches. Authored data only:
    nothing is assembled. Each message names the profile file and begins "<file>: origin:"."""
    by_slug = {card.slug: card for card in library.characters.values()}
    pairs = {pair.slug: pair for pair in library.pairs}
    promoted_slugs = {item.path.stem for item in promoted}
    failures = []
    for item in promoted:
        name, origin = item.path.name, item.origin
        card = by_slug[item.path.stem]  # a file that passed has a card whose slug is its file stem
        pair = pairs.get(origin)
        if pair is None:
            failures.append((item, f"{name}: origin: the pair {origin!r} is not in the library"))
            continue
        if card.name != pair.fusion_name:
            failures.append((item, f"{name}: origin: the character name {card.name!r} is not the fusion name {pair.fusion_name!r} of pair {origin}"))
        for parent in (library.characters[pair.a], library.characters[pair.b]):
            if parent.slug == card.slug:
                failures.append((item, f"{name}: origin: the profile is a parent of its own origin pair {origin}"))
            elif parent.slug in promoted_slugs:
                failures.append((item, f"{name}: origin: a parent of pair {origin} ({parent.name!r}) is itself a promoted profile; only first-generation promotions are recorded"))
        own = {trait.slot: trait.descriptor for trait in card.visual_traits}
        differing = [slot for slot, trait in pair.visual.slots if own.get(slot) != trait.descriptor]
        if differing:
            failures.append((item, f"{name}: origin: appearance slot(s) {', '.join(differing)} differ from pair {origin}"))
        ability = pair.emergent
        named = [prop for prop in card.properties if prop.name == ability.name]
        if not named:
            failures.append((item, f"{name}: origin: no property is named {ability.name!r}, the ability name in pair {origin}"))
        elif not any(prop.description == ability.description for prop in named):
            failures.append((item, f"{name}: origin: the property {ability.name!r} does not carry the ability description of pair {origin}"))
    return failures


def check_files(paths: list) -> CheckResult:
    paths = [Path(p) for p in paths]
    problem = _load([])
    if problem is not None:
        raise RuntimeError(f"the repository's authored data does not load, so no file can be checked: {problem}")

    errors, prepared = [], []
    for path in paths:
        item = _prepare(path)
        if isinstance(item, str):
            errors.append(item)
        else:
            prepared.append(item)

    characters = [item for item in prepared if item.kind == CHARACTER]
    pairs = [item for item in prepared if item.kind == PAIR]

    passed_characters = []
    for item in characters:
        failure = _load([item])
        if failure is not None:
            errors.append(_plain(item.path.name, failure))
        else:
            passed_characters.append(item)
    before = len(errors)
    _combined(passed_characters, [], errors)
    characters_conflict = len(errors) > before

    passed_pairs = []
    for item in pairs:
        if characters_conflict:
            errors.append(f"{item.path.name}: not checked, because the character files above conflict with each other")
            continue
        failure = _load(passed_characters + [item])
        if failure is not None:
            errors.append(_plain(item.path.name, failure))
        else:
            passed_pairs.append(item)
    pairs_conflict = False
    if not characters_conflict:
        before = len(errors)
        _combined(passed_pairs, passed_characters, errors)
        pairs_conflict = len(errors) > before

    promoted = [item for item in passed_characters if item.origin is not None]
    if promoted:
        if characters_conflict or pairs_conflict:
            failures = [(item, f"{item.path.name}: origin not checked, because the files above conflict with each other") for item in promoted]
        else:
            # The files that passed have already loaded together in stages 3-5, so this load cannot fail.
            with _staged_library(passed_characters + passed_pairs) as root:
                failures = _verify_origins(load_library(root), promoted)
        errors.extend(message for _item, message in failures)
        failed = {item.path for item, _message in failures}
        passed_characters = [item for item in passed_characters if item.path not in failed]
    return CheckResult(tuple(errors), tuple(passed_characters + passed_pairs))


def load_view(paths: list) -> dict:
    """The viewer's data with the user characters added, or UserCharacterError with every problem."""
    result = check_files(paths)
    if result.errors:
        raise UserCharacterError(list(result.errors))
    with _staged_library(list(result.files)) as root:
        # The library's own rule makes each file stem equal the character's (or pair's) slug.
        declared = {item.path.stem: item.ownership for item in result.files if item.kind == CHARACTER}
        # Only the folder's NAME is kept for a pair; the page never gets a full path.
        external = {item.path.stem: item.path.resolve().parent.name for item in result.files if item.kind == PAIR}
        promotions = {item.path.stem: item.origin for item in result.files if item.kind == CHARACTER and item.origin}
        return build_view(root, ownership=declared, external_pairs=external, promotions=promotions)


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
        if item.kind == PAIR:
            out.write(f"OK: {item.path.name} (authored fusion pair)\n")
            continue
        label = OWNERSHIP_LABELS.get(item.ownership, "not recorded")
        origin = ""
        if item.origin is not None:
            origin = f"; origin: recorded from pair {item.origin}; only the seven appearance slots and the ability name and description were compared"
        out.write(f"OK: {item.path.name} (ownership: {label}; a self-declaration, not verified{origin})\n")
    for message in result.errors:
        err.write(f"ERROR: {message}\n")
    return EXIT_BAD if result.errors else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
