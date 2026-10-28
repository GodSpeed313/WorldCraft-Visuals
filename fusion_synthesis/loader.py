"""
Fusion Synthesis — data discovery and loading (AUTH-011 §1, §2).

Everything under data/ is found by glob. Nothing is registered in code, so a
new character or pair is added by authoring data files only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from fusion_engine.types import EpistemicStatus, Source, SourceProperty

from .schema import (
    CharacterCard,
    PairCard,
    SchemaError,
    StyleAllowlist,
    StyleAllowlistError,
    character_denylist,
    check_allowlist_against_denylist,
    pair_denylist,
    parse_character,
    parse_pair,
    parse_style_allowlist,
    slugify,
    validate_pair,
)

DATA_DIR = Path(__file__).resolve().parent / "data"


@dataclass(frozen=True)
class Library:
    data_dir: Path
    characters: dict  # name -> CharacterCard
    pairs: tuple  # PairCard, in file-name order
    allowlist: StyleAllowlist


def _no_duplicate_keys(pairs: list) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise SchemaError(f"duplicate key {key!r}")
        out[key] = value
    return out


def read_json(path: Path) -> Any:
    try:
        text = path.read_bytes().decode("utf-8")
        return json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except FileNotFoundError:
        raise SchemaError(f"{path.name}: file not found") from None
    except (UnicodeDecodeError, json.JSONDecodeError, SchemaError) as exc:
        raise SchemaError(f"{path.name}: not valid JSON data ({exc})") from None


def load_library(data_dir: Optional[Path] = None) -> Library:
    root = Path(data_dir) if data_dir is not None else DATA_DIR

    allowlist_path = root / "style_allowlist.json"
    if not allowlist_path.is_file():
        raise StyleAllowlistError(f"style_allowlist.json: file not found in {root}")
    try:
        allowlist = parse_style_allowlist(read_json(allowlist_path))
    except StyleAllowlistError:
        raise
    except SchemaError as exc:
        raise StyleAllowlistError(str(exc)) from None

    characters: dict = {}
    for path in sorted((root / "characters").glob("*.json")):
        try:
            card = parse_character(read_json(path), path.name)
        except SchemaError as exc:
            raise SchemaError(f"{path.name}: {exc}") from None
        if path.stem != card.slug:
            raise SchemaError(f"{path.name}: file name must be {card.slug}.json for character {card.name!r}")
        if card.name in characters:
            raise SchemaError(f"{path.name}: character {card.name!r} is defined twice")
        characters[card.name] = card

    pairs = []
    for path in sorted((root / "pairs").glob("*.json")):
        try:
            pair = parse_pair(read_json(path), path.name)
        except SchemaError as exc:
            raise SchemaError(f"{path.name}: {exc}") from None
        if path.stem != pair.slug:
            raise SchemaError(f"{path.name}: file name must be {pair.slug}.json for pair {pair.a} x {pair.b}")
        for name in (pair.a, pair.b):
            if name not in characters:
                raise SchemaError(f"{path.name}: no character card named {name!r}")
        try:
            validate_pair(pair, characters[pair.a], characters[pair.b])
        except SchemaError as exc:
            raise SchemaError(f"{path.name}: {exc}") from None
        pairs.append(pair)

    entries: list = []
    for card in characters.values():
        entries += character_denylist(card)
    for pair in pairs:
        entries += pair_denylist(pair, characters[pair.a], characters[pair.b])
    check_allowlist_against_denylist(allowlist, entries)

    return Library(data_dir=root, characters=characters, pairs=tuple(pairs), allowlist=allowlist)


def find_pair(library: Library, a: str, b: str) -> Optional[PairCard]:
    for pair in library.pairs:
        if pair.a == a and pair.b == b:
            return pair
    return None


def build_source(card: CharacterCard) -> Source:
    """A character card as a Fusion Engine Source (C1 admits it unchanged)."""
    return Source(
        name=card.name,
        properties=tuple(
            SourceProperty(
                id=p.id,
                description=p.description,
                contribution_type=p.contribution_type,
                architectural_placement=p.architectural_placement,
                epistemic_status=EpistemicStatus.FICTIONAL,
                is_hard_limitation=p.is_hard_limitation,
                is_prohibition=p.is_prohibition,
                activation_condition=p.activation_condition,
            )
            for p in card.properties
        ),
    )


def golden_paths(data_dir: Path, pair: PairCard) -> tuple:
    base = Path(data_dir) / "golden"
    return base / f"{pair.slug}.txt", base / f"{pair.slug}.json"


__all__ = ["DATA_DIR", "Library", "build_source", "find_pair", "golden_paths", "load_library", "read_json", "slugify"]
