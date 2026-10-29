"""
Fusion Synthesis — demo command (AUTH-011 §4).

    python -m fusion_synthesis.demo                  all authored pairs, in file-name order
    python -m fusion_synthesis.demo "<A>" "<B>"      one card (names exact, in authored order)
        --json                                       the JSON card (a list when no pair is given)
        --prompt                                     only the image prompt line(s)

Exit codes: 0 success; 2 invalid data, unknown pair, invalid style allowlist or
prompt over its ceiling; 3 a leak was detected (the prompt is never printed for
a card that fails the check, in any output mode).

Deterministic: no clock, no randomness, no network. Output is UTF-8 with LF line
endings, byte-identical across runs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

from .assemble import assemble_card
from .loader import find_pair, load_library
from .render import PromptTooLongError, finalize, render_json, render_text
from .schema import SchemaError

EXIT_OK, EXIT_INVALID, EXIT_LEAK = 0, 2, 3
_RULE = "=" * 72


def _write(stream, text: str) -> None:
    if hasattr(stream, "buffer"):
        stream.buffer.write(text.encode("utf-8"))
    else:
        stream.write(text)
    stream.flush()


def main(argv: Optional[list] = None, stdout=None, stderr=None, data_dir: Optional[Path] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr

    flags = [a for a in args if a.startswith("--")]
    names = [a for a in args if not a.startswith("--")]
    unknown = [f for f in flags if f not in ("--json", "--prompt")]
    if unknown or len(names) not in (0, 2) or ("--json" in flags and "--prompt" in flags):
        _write(err, 'usage: python -m fusion_synthesis.demo ["<A>" "<B>"] [--json | --prompt]\n')
        return EXIT_INVALID
    want_json, want_prompt = "--json" in flags, "--prompt" in flags

    try:
        library = load_library(data_dir)
        if names:
            pair = find_pair(library, names[0], names[1])
            if pair is None:
                listing = ", ".join(f"{p.a} x {p.b}" for p in library.pairs) or "(none)"
                _write(err, f"error: no authored pair {names[0]!r} x {names[1]!r}. Authored pairs: {listing}\n")
                return EXIT_INVALID
            pairs = [pair]
        else:
            pairs = list(library.pairs)
        cards = [
            finalize(assemble_card(library, p), p, library.characters[p.a], library.characters[p.b], library.allowlist)
            for p in pairs
        ]
    except (SchemaError, PromptTooLongError) as exc:
        _write(err, f"error: {exc}\n")
        return EXIT_INVALID

    leaked = [c for c in cards if c["leak_check"]["status"] == "FAIL"]

    if want_prompt:
        for c in cards:
            if c["leak_check"]["status"] == "FAIL":
                tokens_ = ", ".join(sorted({f["token"] for f in c["leak_check"]["findings"]}))
                _write(err, f"leak detected for {c['fusion_name']}: {tokens_}; no prompt printed\n")
            else:
                _write(out, c["image_prompt"]["text"] + "\n")
    elif want_json:
        payload = cards[0] if names else cards
        _write(out, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    else:
        chunks = [render_text(c) for c in cards]
        _write(out, ("\n" + _RULE + "\n\n").join(chunks))
        if not names:
            _write(out, f"\n{len(cards)} cards, {len(leaked)} leaks\n")

    return EXIT_LEAK if leaked else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
