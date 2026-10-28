"""
Fusion Synthesis — C6-min: composed paragraph, image prompt, leak check, and
text / JSON rendering (AUTH-011 §3, §4).

The image prompt is built ONLY from authored, name-free descriptors, in one
fixed order. There is exactly one prompt format and no name-including variant.
Nothing is ever truncated: a prompt over its ceiling is an error.

LEAK-CHECK CLAIM. A passing check establishes only that the prompt, the
descriptors and the composed paragraph pass the implemented detector (full-phrase
and token denylist matching, plus a capitalized-word heuristic that may skip
style-allowlist terms). It is NOT a guarantee that no recognizable proper noun,
character reference or franchise reference is present. Descriptive phrasing
that evokes a character without naming it is outside what the detector sees.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Optional

from .schema import (
    SLOTS,
    CharacterCard,
    PairCard,
    StyleAllowlist,
    match_tokens,
    pair_denylist,
    phrase,
    tokens,
    visual_traits_of,
)

DEFAULT_PROMPT_MAX_CHARS = 900  # project convention, not a provider specification
DETECTOR_LABEL = "implemented detector"
LEAK_CLAIM = (
    "A pass establishes compliance with the implemented detector only. It is not a guarantee that "
    "no recognizable proper noun, character reference or franchise reference is present."
)

_SLOT_LABELS = {
    "build": "Build",
    "face": "Face",
    "hair": "Hair",
    "clothing": "Clothing",
    "palette": "Palette",
    "signature_element": "Signature element",
    "ability_manifestation": "Ability in use",
}


class PromptTooLongError(ValueError):
    """The image prompt exceeds its ceiling. Never truncated. Exit code 2."""


# ---------------------------------------------------------------------------
# Paragraph and prompt
# ---------------------------------------------------------------------------

def compose_paragraph(pair: PairCard) -> str:
    """Deterministic, descriptor-only paragraph (name-free by construction)."""
    subject = pair.visual.subject.descriptor
    parts = [subject[:1].upper() + subject[1:] + "."]
    for slot, trait in pair.visual.slots:
        parts.append(f"{_SLOT_LABELS[slot]}: {trait.descriptor}.")
    scene = dict((field, trait.descriptor) for field, trait in pair.visual.scene)
    parts.append(
        f"Setting: {scene['setting']}. Mood: {scene['mood']}. "
        f"Lighting: {scene['lighting']}. Style: {scene['style']}."
    )
    return " ".join(parts)


@dataclass(frozen=True)
class PromptBuild:
    text: str
    body: str
    parameters: str
    length: int
    ceiling: int
    components: tuple  # ((label, descriptor), ...) in prompt order


def effective_ceiling(pair: PairCard) -> int:
    return pair.prompt_max_chars if pair.prompt_max_chars is not None else DEFAULT_PROMPT_MAX_CHARS


def build_prompt(pair: PairCard) -> PromptBuild:
    """subject, key features (the seven slots in fixed order), setting, mood,
    lighting, style, parameters."""
    components = tuple((label, trait.descriptor) for label, trait in visual_traits_of(pair))
    body = ", ".join(descriptor for _label, descriptor in components)
    text = f"{body} {pair.visual.parameters}"
    ceiling = effective_ceiling(pair)
    if len(text) > ceiling:
        sizes = ", ".join(f"{label}={len(d)}" for label, d in components)
        raise PromptTooLongError(
            f"image prompt for {pair.a} x {pair.b} is {len(text)} characters, over its ceiling of {ceiling}; "
            f"component lengths: {sizes}, parameters={len(pair.visual.parameters)}. "
            "Shorten a descriptor or raise prompt_max_chars (200-2000); nothing is truncated."
        )
    return PromptBuild(text, body, pair.visual.parameters, len(text), ceiling, components)


# ---------------------------------------------------------------------------
# Leak detector
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Leak:
    where: str
    kind: str  # "phrase" | "token" | "capitalized"
    token: str
    entry: str
    source: str

    def as_dict(self) -> dict:
        return {"where": self.where, "kind": self.kind, "token": self.token, "entry": self.entry, "source": self.source}


def find_denylist_leaks(text: str, entries: list, where: str) -> list:
    """Full-phrase matching is mandatory and never weakened. Token matching
    additionally ignores stop words and tokens shorter than two characters.
    The style allowlist plays no part here."""
    toks = tokens(text)
    token_set = set(toks)
    padded = " " + " ".join(toks) + " "
    leaks, seen = [], set()
    for entry, source in entries:
        entry_phrase = phrase(entry)
        if not entry_phrase:
            continue
        if f" {entry_phrase} " in padded:
            key = ("phrase", entry_phrase)
            if key not in seen:
                seen.add(key)
                leaks.append(Leak(where, "phrase", entry, entry, source))
            continue
        for tok in match_tokens(entry):
            if tok in token_set:
                key = ("token", tok, entry_phrase)
                if key not in seen:
                    seen.add(key)
                    leaks.append(Leak(where, "token", tok, entry, source))
    return leaks


def find_capitalized(text: str, allowlist_terms: tuple, where: str) -> list:
    """Capitalized words are suspected proper nouns unless they sit inside a
    style-allowlist term. This heuristic is the ONLY thing the allowlist can
    skip; it can never reduce a denylist finding."""
    spans = [(m.group(0), m.start()) for m in re.finditer(r"[^\W_]+", text)]
    lowered = [w.lower() for w, _ in spans]
    covered = set()
    for term in allowlist_terms:
        term_tokens = tokens(term)
        n = len(term_tokens)
        if not n:
            continue
        for i in range(len(lowered) - n + 1):
            if lowered[i : i + n] == term_tokens:
                covered.update(range(i, i + n))
    leaks = []
    for i, (word, _pos) in enumerate(spans):
        if word[0].isupper() and i not in covered:
            leaks.append(Leak(where, "capitalized", word, "", "capitalized-word heuristic"))
    return leaks


def check_text(text: str, entries: list, allowlist_terms: tuple, where: str, capitalized: bool = True) -> list:
    leaks = find_denylist_leaks(text, entries, where)
    if capitalized:
        leaks += find_capitalized(text, allowlist_terms, where)
    return leaks


# ---------------------------------------------------------------------------
# Finalize: prompt, paragraph, leak check
# ---------------------------------------------------------------------------

def finalize(record: dict, pair: PairCard, card_a: CharacterCard, card_b: CharacterCard,
             allowlist: StyleAllowlist) -> dict:
    """Add the composed paragraph, the image prompt and the leak check.

    PromptTooLongError propagates (data error). On a leak anywhere in the
    prompt, any descriptor or the paragraph, the prompt is suppressed
    (image_prompt.text is None) in the record, so no output mode can emit it."""
    entries = pair_denylist(pair, card_a, card_b)
    terms = allowlist.terms
    build = build_prompt(pair)
    paragraph = compose_paragraph(pair)

    leaks = []
    leaks += find_denylist_leaks(build.text, entries, "prompt")
    leaks += find_capitalized(build.body, terms, "prompt")
    for label, trait in visual_traits_of(pair):
        leaks += check_text(trait.descriptor, entries, terms, f"descriptor:{label}")
    leaks += find_denylist_leaks(paragraph, entries, "paragraph")

    failed = bool(leaks)
    out = dict(record)
    out["appearance"] = dict(record["appearance"], composed_paragraph=paragraph)
    out["image_prompt"] = {
        "text": None if failed else build.text,
        "suppressed": failed,
        "order": [label for label, _ in build.components] + ["parameters"],
        "length": build.length,
        "ceiling": build.ceiling,
    }
    out["leak_check"] = {
        "detector": DETECTOR_LABEL,
        "status": "FAIL" if failed else "PASS",
        "findings": [l.as_dict() for l in leaks],
        "claim": LEAK_CLAIM,
    }
    return out


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_json(card: dict) -> str:
    return json.dumps(card, indent=2, ensure_ascii=False) + "\n"


def render_prompt_line(card: dict) -> Optional[str]:
    return card["image_prompt"]["text"]


def _parents_text(row: dict) -> str:
    return " + ".join(f"{p['id']} ({p['character']})" for p in row["parents"])


def render_text(card: dict) -> str:
    L = []
    a, b = card["sources"]["A"], card["sources"]["B"]
    dom = card["dominance"]
    L.append(f"{card['fusion_name']}   ({a} x {b})   dominance: {dom['value']}/{100 - dom['value']} ({dom['note']})")
    L.append("")
    L.append("CONCEPT")
    L.append(f"  {card['concept']}")
    L.append("")
    L.append("APPEARANCE")
    ap = card["appearance"]
    L.append(f"  subject: {ap['subject']}")
    for slot in SLOTS:
        L.append(f"  {slot}: {ap['slots'][slot]}")
    for field, value in ap["scene"].items():
        L.append(f"  {field}: {value}")
    L.append("  composed paragraph:")
    L.append(f"    {ap['composed_paragraph']}")
    L.append("")
    L.append("VISUAL PROVENANCE")
    for row in card["visual_provenance"]:
        line = f"  {row['slot']} | {row['descriptor']} | {row['origin']} | {_parents_text(row)}"
        L.append(line)
        if "design_delta" in row:
            d = row["design_delta"]
            L.append(f"      design change ({d['changed']}): {d['from']}  ->  {d['to']}")
    L.append("")
    L.append("TRAITS")
    for outcome in ("inherited", "transformed", "complementary", "not_carried"):
        group = [t for t in card["traits"] if t["outcome"] == outcome]
        label = outcome.replace("_", " ")
        L.append(f"  {label}:")
        if not group:
            L.append("    (none)")
        for t in group:
            L.append(f"    - {t['name']} [{t['source']}: {t['character']}] ({t['provenance']}, {t['epistemic_status']})")
            L.append(f"      {t['result_text']}")
            if "reason" in t:
                L.append(f"      not carried because: {t['reason']}")
    L.append("")
    em = card["emergent_ability"]
    L.append("EMERGENT ABILITY")
    L.append(f"  {em['name']}  [{em['provenance']}]")
    L.append(f"  {em['description']}")
    gr = em["governing_rule"]
    L.append(f"  governing rule ({gr['provenance']}): {gr['description']}")
    L.append(f"  derived from: {', '.join(em['direct_ancestor_ids'])}")
    if em["activation"]:
        L.append(f"  activation: {em['activation']}")
    L.append("  limitations:")
    for lim in em["limitations"]:
        L.append(f"    - {lim}")
    L.append("  inherited limitations:")
    if not em["inherited_limitations"]:
        L.append("    (none)")
    for lim in em["inherited_limitations"]:
        L.append(f"    - {lim['name']} [{lim['character']}] ({lim['kind']}): {lim['description']}")
    L.append("")
    L.append("EXCLUSIONS")
    if not card["exclusions"]:
        L.append("  (none)")
    for x in card["exclusions"]:
        L.append(f"  - {x['item']} [{x['source']}: {x['character']}]: {x['reason']}")
    L.append("")
    comp = card["compatibility"]
    L.append("COMPATIBILITY")
    L.append(f"  {comp['status']} ({comp['evaluated_conditions']} activation conditions evaluated)")
    for key in ("contradiction", "required_bridge", "unresolved_reason"):
        if comp[key]:
            L.append(f"  {key.replace('_', ' ')}: {comp[key]}")
    L.append("")
    L.append("ANCESTRY")
    for item in card["ancestry"]:
        who = f" [{item['character']}]" if "character" in item else ""
        L.append(f"  - {item['id']} ({item['kind']}{who}, {item['provenance']})")
    L.append("")
    ip = card["image_prompt"]
    L.append("IMAGE PROMPT")
    if ip["suppressed"]:
        L.append("  [suppressed: the leak check failed]")
    else:
        L.append(f"  {ip['text']}")
    L.append(f"  ({ip['length']} / {ip['ceiling']} characters)")
    L.append("")
    lc = card["leak_check"]
    L.append(f"LEAK CHECK ({lc['detector']}): {lc['status']}")
    for f in lc["findings"]:
        entry = f" matches '{f['entry']}'" if f["entry"] else ""
        L.append(f"  - {f['where']}: {f['kind']} '{f['token']}'{entry}")
    return "\n".join(L) + "\n"
