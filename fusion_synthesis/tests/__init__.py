"""
Test support for fusion_synthesis (AUTH-011 §6).

Builders for SYNTHETIC, invented characters and pairs, used to exercise
validation and failure paths in a temporary data directory. The names here are
invented and are never authored data: tests that must cover the real authored
cards discover them by glob from the real data directory.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from fusion_synthesis.schema import SCENE_FIELDS, SLOTS, slugify

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = REPO_ROOT / "fusion_synthesis"
REAL_DATA_DIR = PACKAGE_DIR / "data"

_ADJECTIVES = {
    "build": "stout broad-shouldered frame",
    "face": "wide pale eyes and a crooked grin",
    "hair": "braided copper hair",
    "clothing": "a patched leather vest and heavy gloves",
    "palette": "rust, ochre and slate grey",
    "signature_element": "a notched iron lantern on a chain",
    "ability_manifestation": "slow orange embers drifting upward",
}
_ADJECTIVES_B = {
    "build": "narrow, stooped frame",
    "face": "sharp dark eyes and a thin smile",
    "hair": "close-cropped silver hair",
    "clothing": "a hooded grey cloak over pressed linen",
    "palette": "ash, indigo and bone white",
    "signature_element": "a glass vial of shifting liquid",
    "ability_manifestation": "cold blue frost spreading across the ground",
}


def synthetic_character(name: str, second: bool = False) -> dict:
    slug = slugify(name)
    words = _ADJECTIVES_B if second else _ADJECTIVES
    return {
        "schema": "fusion-synthesis-character/1",
        "name": name,
        "epistemic_status": "FICTIONAL",
        "properties": [
            {
                "id": f"{slug}.core",
                "name": f"{name} Core",
                "description": "The main working mechanism of this invented character.",
                "contribution_type": "ABILITY",
                "architectural_placement": "CORE_MECHANISM",
            },
            {
                "id": f"{slug}.bound",
                "name": f"{name} Bound",
                "description": "A hard limit on the main mechanism.",
                "contribution_type": "MECHANISM",
                "architectural_placement": "LIMITATIONS",
                "is_hard_limitation": True,
            },
        ],
        "visual_traits": [
            {"id": f"{slug}.v_{slot}", "slot": slot, "descriptor": words[slot], "derives_from": []}
            for slot in SLOTS
        ],
        "proper_nouns": [name],
        "exclusion_candidates": [{"item": "invented baggage", "reason": "not a mechanic"}],
    }


def synthetic_pair(a: str, b: str) -> dict:
    sa, sb = slugify(a), slugify(b)
    scope = f"{sa}__{sb}"
    trait_new = {"origin": "new", "parent_ids": [f"{scope}.emergent"]}
    return {
        "schema": "fusion-synthesis-pair/1",
        "a": a,
        "b": b,
        "dominance": 50,
        "fusion_name": "Pell Marrowind",
        "concept": "An invented test concept that exists only to exercise the validators.",
        "interaction": {
            "id": f"{scope}.rule",
            "description": "An invented rule combining the two core mechanisms.",
            "dependency_ids": [f"{sa}.core", f"{sb}.core"],
            "provenance": "INVENTED_BRIDGE",
            "is_disclosed_modification": False,
        },
        "emergent_ability": {
            "id": f"{scope}.emergent",
            "name": "Hollow Chorus",
            "description": "An invented emergent ability for tests.",
            "direct_ancestor_ids": [f"{sa}.core", f"{sb}.core", f"{sa}.bound"],
            "contribution_type": "ABILITY",
            "architectural_placement": "EMERGENT_PROPERTY",
            "limitations": ["It fails whenever the test says it fails."],
            "activation": None,
        },
        "trait_outcomes": [
            {"property_id": f"{sa}.core", "outcome": "inherited", "result_text": "Carried."},
            {"property_id": f"{sa}.bound", "outcome": "inherited", "result_text": "Carried."},
            {"property_id": f"{sb}.core", "outcome": "transformed", "result_text": "Reshaped."},
            {"property_id": f"{sb}.bound", "outcome": "not_carried", "result_text": "Dropped.", "reason": "Unused."},
        ],
        "exclusions": [{"item": "invented baggage", "source": "A", "reason": "not a mechanic"}],
        "visual": {
            "subject": {
                "descriptor": "a lean wanderer with an ember-lit lantern",
                "origin": "transformed",
                "parent_ids": [f"{sa}.v_build", f"{sb}.v_build"],
                "design_delta": {"changed": "form", "from": "stout frame; narrow frame", "to": "lean wanderer"},
            },
            "slots": {
                "build": {
                    "descriptor": _ADJECTIVES["build"],
                    "origin": "A",
                    "parent_ids": [f"{sa}.v_build"],
                },
                "face": {
                    "descriptor": _ADJECTIVES_B["face"],
                    "origin": "B",
                    "parent_ids": [f"{sb}.v_face"],
                },
                "hair": {
                    "descriptor": "braided silver hair tied with a copper ring",
                    "origin": "transformed",
                    "parent_ids": [f"{sa}.v_hair", f"{sb}.v_hair"],
                    "design_delta": {
                        "changed": "color",
                        "from": "braided copper hair; close-cropped silver hair",
                        "to": "braided silver hair tied with a copper ring",
                    },
                },
                "clothing": {
                    "descriptor": "a patched grey cloak worn over a leather vest",
                    "origin": "transformed",
                    "parent_ids": [f"{sa}.v_clothing", f"{sb}.v_clothing"],
                    "design_delta": {
                        "changed": "structure",
                        "from": "vest and gloves; hooded cloak over linen",
                        "to": "a patched grey cloak worn over a leather vest",
                    },
                },
                "palette": {
                    "descriptor": "rust, indigo and bone white with ochre trim",
                    "origin": "transformed",
                    "parent_ids": [f"{sa}.v_palette", f"{sb}.v_palette"],
                    "design_delta": {
                        "changed": "color",
                        "from": "rust, ochre and slate grey; ash, indigo and bone white",
                        "to": "rust, indigo and bone white with ochre trim",
                    },
                },
                "signature_element": {
                    "descriptor": "a lantern of frosted glass holding a slow ember",
                    "origin": "transformed",
                    "parent_ids": [f"{sa}.v_signature_element", f"{sb}.v_signature_element"],
                    "design_delta": {
                        "changed": "material",
                        "from": "a notched iron lantern; a glass vial",
                        "to": "a lantern of frosted glass holding a slow ember",
                    },
                },
                "ability_manifestation": dict(
                    trait_new, descriptor="pale vapour curling off the shoulders and pooling underfoot"
                ),
            },
            "setting": dict(trait_new, descriptor="a quiet salt flat under a wide sky"),
            "mood": dict(trait_new, descriptor="calm, watchful, faintly wistful"),
            "lighting": dict(trait_new, descriptor="soft overcast light with a single warm point"),
            "style": dict(trait_new, descriptor="detailed illustrated character study, full-length view"),
            "parameters": "--ar 3:4",
        },
    }


def deep(obj: dict) -> dict:
    return copy.deepcopy(obj)


def write_library(root: Path, characters: list, pairs: list, terms=("Baroque", "Art Nouveau")) -> Path:
    """Write a data directory. Files are named from their content, so a test
    can add a character or pair by writing files only."""
    root = Path(root)
    (root / "characters").mkdir(parents=True, exist_ok=True)
    (root / "pairs").mkdir(parents=True, exist_ok=True)
    (root / "style_allowlist.json").write_text(
        json.dumps({"schema": "fusion-synthesis-style-allowlist/1", "terms": list(terms)}, indent=2), encoding="utf-8"
    )
    for card in characters:
        (root / "characters" / f"{slugify(card['name'])}.json").write_text(json.dumps(card, indent=2), encoding="utf-8")
    for pair in pairs:
        name = f"{slugify(pair['a'])}__{slugify(pair['b'])}.json"
        (root / "pairs" / name).write_text(json.dumps(pair, indent=2), encoding="utf-8")
    return root


A_NAME, B_NAME, C_NAME = "Zorblax", "Quillon", "Thessaly Brae"


def default_cards() -> tuple:
    return synthetic_character(A_NAME), synthetic_character(B_NAME, second=True)


__all__ = [
    "A_NAME", "B_NAME", "C_NAME", "PACKAGE_DIR", "REAL_DATA_DIR", "REPO_ROOT", "SCENE_FIELDS", "SLOTS",
    "deep", "default_cards", "synthetic_character", "synthetic_pair", "write_library",
]
