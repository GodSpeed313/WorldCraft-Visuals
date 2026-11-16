"""
IMP-001 M2 evidence storage, secret scan and milestone-wide reservation. Standard library only.

Rules enforced here (AUTH IMP-001 M2 Harness Construction, A3 and A6):

  * the evidence root must already exist, be writable, resolve outside the repository,
    not be a link/junction, and resolve to exactly the configured path; otherwise stop.
    Nothing is created, and there is no fallback root;
  * every file is written ONCE (exclusive create), flushed, read back and hashed;
  * a proposed file containing the API key or the provider key prefix is never written
    (no redacted replacement);
  * ONE reservation covers the whole milestone. Any existing M2 attempt artifact blocks
    every new invocation. Nothing in this module deletes, resets or bypasses it.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Optional

from proposer.m2_config import PROVIDER_KEY_PREFIX

RESERVATION_NAME = "M2_RESERVATION.json"
ARTIFACT_PREFIX = "M2_"
# Dry-run reports are not attempts and never block the milestone.
NON_ATTEMPT_PREFIX = "M2_DRYRUN_"
_REPARSE_POINT = 0x400


class EvidenceError(RuntimeError):
    """An evidence operation failed. The milestone stays blocked if a reservation exists."""


class RootRejected(EvidenceError):
    """The configured evidence root failed verification."""


class SecretDetected(EvidenceError):
    """A proposed record contains a credential. Nothing was written."""


class ReservationExists(EvidenceError):
    """The milestone-wide reservation (or another M2 attempt artifact) already exists."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"


# --- secret scan --------------------------------------------------------------

def scan_for_secrets(data: bytes, api_key: Optional[str]) -> None:
    """Raise SecretDetected if `data` holds the configured key value or the provider key prefix."""
    if PROVIDER_KEY_PREFIX.encode("ascii") in data:
        raise SecretDetected(f"proposed record contains the provider key prefix {PROVIDER_KEY_PREFIX!r}; nothing was written")
    if api_key and api_key.encode("utf-8") in data:
        raise SecretDetected("proposed record contains the configured API key value; nothing was written")


# --- root verification --------------------------------------------------------

def _is_link_or_junction(path: str) -> bool:
    if os.path.islink(path):
        return True
    isjunction = getattr(os.path, "isjunction", None)
    if isjunction is not None and isjunction(path):
        return True
    try:
        attrs = getattr(os.lstat(path), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attrs & _REPARSE_POINT)


def _within(child: str, parent: str) -> bool:
    c, p = os.path.normcase(os.path.abspath(child)), os.path.normcase(os.path.abspath(parent))
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def _probe_writable(root: str) -> None:
    """Create and remove one uniquely named probe file. Raises OSError if the root is not writable."""
    probe = os.path.join(root, f".write_probe_{uuid.uuid4().hex}")
    fd = os.open(probe, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
    try:
        os.write(fd, b"probe")
    finally:
        os.close(fd)
        os.unlink(probe)


def verify_root(configured_root: str, repo_root) -> Path:
    """Return the verified root, or raise RootRejected. Never creates or repairs anything."""
    root = str(configured_root)
    if not os.path.isabs(root):
        raise RootRejected(f"evidence root {root!r} is not an absolute path")
    if not os.path.exists(root):
        raise RootRejected(f"evidence root {root!r} does not exist (the harness never creates it)")
    if not os.path.isdir(root):
        raise RootRejected(f"evidence root {root!r} is not a directory")
    if _is_link_or_junction(root):
        raise RootRejected(f"evidence root {root!r} is a symlink, junction or reparse point")
    real = os.path.realpath(root)
    if os.path.normcase(real) != os.path.normcase(os.path.abspath(root)):
        raise RootRejected(f"evidence root {root!r} resolves to {real!r}: it is redirected, so it is not the expected location")
    repo_real = os.path.realpath(str(repo_root))
    if _within(real, repo_real) or _within(root, repo_real):
        raise RootRejected(f"evidence root {root!r} is inside the repository working tree")
    try:
        _probe_writable(root)
    except OSError as exc:
        raise RootRejected(f"evidence root {root!r} is not writable ({type(exc).__name__})") from None
    return Path(real)


# --- write-once store ---------------------------------------------------------

class EvidenceStore:
    def __init__(self, root: Path, api_key: Optional[str]):
        self.root = Path(root)
        self._api_key = api_key

    def path_of(self, name: str) -> Path:
        if os.path.basename(name) != name or not name.startswith(ARTIFACT_PREFIX):
            raise EvidenceError(f"evidence file name {name!r} must be a bare name starting with {ARTIFACT_PREFIX!r}")
        return self.root / name

    def write_once(self, name: str, data: bytes) -> str:
        """Scan, exclusively create, flush, read back and hash. Returns the SHA-256 of `data`."""
        path = self.path_of(name)
        scan_for_secrets(data, self._api_key)          # before anything touches the disk
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        try:
            fd = os.open(path, flags, 0o600)
        except FileExistsError:
            raise EvidenceError(f"{name} already exists; evidence is never overwritten") from None
        except OSError as exc:
            raise EvidenceError(f"could not create {name} ({type(exc).__name__})") from None
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            raise EvidenceError(f"could not write {name} ({type(exc).__name__}); the file may be partial") from None
        digest = sha256_hex(data)
        if sha256_hex(path.read_bytes()) != digest:
            raise EvidenceError(f"{name} did not read back identically")
        return digest

    def write_json_once(self, name: str, obj) -> tuple:
        data = canonical_json(obj)
        return self.write_once(name, data), data

    # --- milestone-wide reservation (A6) ---

    def attempt_artifacts(self) -> list:
        """Names of every M2 artifact that proves an attempt was at least begun."""
        names = []
        for entry in os.listdir(self.root):
            if entry.startswith(ARTIFACT_PREFIX) and not entry.startswith(NON_ATTEMPT_PREFIX):
                names.append(entry)
        return sorted(names)

    def assert_milestone_open(self) -> None:
        found = self.attempt_artifacts()
        if found:
            raise ReservationExists(
                "IMP-001 M2 is blocked: attempt artifact(s) already exist in the evidence root "
                f"({', '.join(found[:5])}). Recovery or release needs separate operator authorization."
            )

    def reserve(self, payload: dict) -> tuple:
        """Atomically create THE milestone reservation. Returns (reservation_id, sha256)."""
        self.assert_milestone_open()
        reservation_id = uuid.uuid4().hex
        record = dict(payload, reservation_id=reservation_id)
        try:
            digest, _ = self.write_json_once(RESERVATION_NAME, record)
        except EvidenceError as exc:
            if self.path_of(RESERVATION_NAME).exists():
                raise ReservationExists(f"reservation already exists or is partial: {exc}") from None
            raise
        return reservation_id, digest


__all__ = [
    "EvidenceError",
    "EvidenceStore",
    "RESERVATION_NAME",
    "ReservationExists",
    "RootRejected",
    "SecretDetected",
    "canonical_json",
    "scan_for_secrets",
    "sha256_hex",
    "verify_root",
]
