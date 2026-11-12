"""
Proposer input packet (IMP-001, Milestone 1). Standard library only.

A packet is built from EXACTLY four inputs, each named by explicit path:

  * two development character files, from dev_data/prop001/characters/;
  * the REQ-001 v1.0 Sections 1-5 file, proposer/inputs/req_001_v1.0_sections_1-5.md;
  * fusion_synthesis/schema.py, as the pair-file schema reference.

Nothing is discovered. No folder is ever listed or read recursively, so a file
added to any folder cannot enter a packet. Any other input is rejected,
whatever its name or content.

Canonical serialization: UTF-8 JSON, sorted keys, no insignificant whitespace,
every embedded text normalized to "\\n" line endings. packet_sha256 is the
SHA-256 of exactly those bytes. Paths inside the packet are repo-relative with
forward slashes, so the hash does not depend on where the repository sits.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from fusion_synthesis.loader import read_json
from fusion_synthesis.schema import SchemaError, parse_character

REPO_ROOT = Path(__file__).resolve().parents[1]

PACKET_SCHEMA = "proposer-packet/1"
CHARACTER_DIR = Path("dev_data") / "prop001" / "characters"
REQUIREMENTS_PATH = Path("proposer") / "inputs" / "req_001_v1.0_sections_1-5.md"
SCHEMA_PATH = Path("fusion_synthesis") / "schema.py"

# The four development characters frozen in DEV-CHAR-001 Revision 3.
AUTHORIZED_CHARACTERS = ("ilse_marrow", "sable_quillon", "tamsin_vey", "pell_dunmore")

# REQ-001's reviewer appendix must never reach a proposer-facing packet.
APPENDIX_MARKER = "Reviewer appendix"
REQUIREMENTS_FIRST_LINE = "## 1. "


class PacketInputError(ValueError):
    """An input is not one of the permitted packet inputs."""


@dataclass(frozen=True)
class Packet:
    data: dict
    canonical_bytes: bytes
    packet_sha256: str


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _expect_file(path, repo_root: Path, expected: Path, label: str) -> Path:
    """The path must be a regular file that resolves to exactly `expected` under repo_root."""
    p = Path(path)
    if not p.is_file():
        raise PacketInputError(f"{label}: {str(path)!r} is not a file; folders and missing paths are never accepted")
    if p.resolve() != (repo_root / expected).resolve():
        raise PacketInputError(f"{label}: {str(path)!r} is not the permitted file {expected.as_posix()}")
    return p.resolve()


def _read_text(path: Path, label: str) -> str:
    try:
        return _normalize(path.read_bytes().decode("utf-8"))
    except UnicodeDecodeError:
        raise PacketInputError(f"{label}: {path.name} is not valid UTF-8") from None


def _entry(rel: Path, text: str) -> dict:
    return {
        "path": rel.as_posix(),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "text": text,
    }


def _character_entry(path, repo_root: Path) -> tuple:
    p = Path(path)
    if not p.is_file():
        raise PacketInputError(f"character: {str(path)!r} is not a file; folders and missing paths are never accepted")
    resolved = p.resolve()
    char_dir = (repo_root / CHARACTER_DIR).resolve()
    if resolved.parent != char_dir:
        raise PacketInputError(f"character: {str(path)!r} is not directly inside {CHARACTER_DIR.as_posix()}")
    if resolved.suffix != ".json" or resolved.stem not in AUTHORIZED_CHARACTERS:
        raise PacketInputError(
            f"character: {resolved.name!r} is not one of the authorized development characters "
            f"{', '.join(c + '.json' for c in AUTHORIZED_CHARACTERS)}"
        )
    try:
        card = parse_character(read_json(resolved), resolved.name)
    except SchemaError as exc:
        raise PacketInputError(f"character: {resolved.name} is not a valid character card ({exc})") from None
    if card.slug != resolved.stem:
        raise PacketInputError(f"character: {resolved.name} holds {card.name!r}, whose file name would be {card.slug}.json")
    return card.slug, _entry(CHARACTER_DIR / resolved.name, _read_text(resolved, "character"))


def build_packet(character_a, character_b, requirements, schema_reference, *, repo_root=REPO_ROOT) -> Packet:
    """Build a packet from exactly the four permitted inputs, each given by explicit path."""
    root = Path(repo_root)

    slug_a, entry_a = _character_entry(character_a, root)
    slug_b, entry_b = _character_entry(character_b, root)
    if slug_a == slug_b:
        raise PacketInputError("character: a packet needs two different characters")

    req_path = _expect_file(requirements, root, REQUIREMENTS_PATH, "requirements")
    req_text = _read_text(req_path, "requirements")
    if APPENDIX_MARKER in req_text:
        raise PacketInputError(f"requirements: the text contains {APPENDIX_MARKER!r}; only Sections 1-5 are permitted")
    if not req_text.startswith(REQUIREMENTS_FIRST_LINE):
        raise PacketInputError(f"requirements: the text must begin with Section 1 ({REQUIREMENTS_FIRST_LINE.strip()!r})")

    schema_path = _expect_file(schema_reference, root, SCHEMA_PATH, "schema reference")

    data = {
        "schema": PACKET_SCHEMA,
        "characters": [entry_a, entry_b],
        "requirements": _entry(REQUIREMENTS_PATH, req_text),
        "pair_schema_reference": _entry(SCHEMA_PATH, _read_text(schema_path, "schema reference")),
    }
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return Packet(data=data, canonical_bytes=canonical, packet_sha256=hashlib.sha256(canonical).hexdigest())


__all__ = [
    "AUTHORIZED_CHARACTERS",
    "CHARACTER_DIR",
    "Packet",
    "PacketInputError",
    "REPO_ROOT",
    "REQUIREMENTS_PATH",
    "SCHEMA_PATH",
    "build_packet",
]
