"""
Fusion Viewer: view data (Path A, authored cards only).

Turns the existing fusion_synthesis library into one JSON-serialisable dict for
the page. Every card is the unmodified result of the existing, deterministic
load_library -> assemble_card -> finalize path, so it equals the operator-
approved golden JSON. Nothing is generated here and nothing is written.

The status block only states what the data supports. The card format has no
independent-validation field and no experimental-status field, so the viewer
reports both as "not recorded" instead of inventing a value.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Optional

from fusion_synthesis.assemble import assemble_card
from fusion_synthesis.loader import load_library
from fusion_synthesis.render import finalize

VIEW_SCHEMA = "fusion-viewer-data/1"

NOT_SYNTHESIZED = "Not yet synthesized — no authored result exists for this pair."
NOTICE = (
    "This viewer displays authored content only. It generates no new synthesis "
    "and does not claim demonstrated emergence."
)
COMPATIBILITY_CAVEAT = (
    "A compatibility result is a structural check of the authored data. "
    "It is not proof of genuine emergence."
)
NO_INDEPENDENT_VALIDATION = "None recorded. No independent validation record exists for this card."
EXPERIMENTAL_UNRECORDED = "Not recorded (unknown). The card format has no experimental-status field."


OWNERSHIP_VALUES = ("original", "public_domain", "third_party_ip", "licensed")
OWNERSHIP_LABELS = {
    "original": "original",
    "public_domain": "public domain",
    "third_party_ip": "third-party IP",
    "licensed": "licensed",
}
OWNERSHIP_NOT_RECORDED = "not recorded"


class ViewDataError(ValueError):
    """The authored data cannot be shown unambiguously (for example, both A x B and B x A are authored)."""


def pair_key(slug_a: str, slug_b: str) -> str:
    """Order-independent identifier of a character pair."""
    first, second = sorted((slug_a, slug_b))
    return f"{first}__{second}"


def _character_view(card) -> dict:
    return {
        "slug": card.slug,
        "name": card.name,
        "properties": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "contribution_type": p.contribution_type.name,
                "architectural_placement": p.architectural_placement.name,
                "is_hard_limitation": p.is_hard_limitation,
                "is_prohibition": p.is_prohibition,
            }
            for p in card.properties
        ],
        "visual_traits": [{"slot": t.slot, "descriptor": t.descriptor} for t in card.visual_traits],
        "exclusion_candidates": [{"item": item, "reason": reason} for item, reason in card.exclusion_candidates],
    }


def _bridge_summary(card: dict) -> str:
    provenances = {card["emergent_ability"]["provenance"], card["emergent_ability"]["governing_rule"]["provenance"]}
    if "INVENTED_BRIDGE" in provenances:
        return "Bridge invented"
    if provenances == {"DEFENSIBLY_DERIVED"}:
        return "Rule defensibly derived"
    return "Provenance: " + ", ".join(sorted(provenances))


EXTERNAL_FOLDER_FALLBACK = "External folder"
EXTERNAL_AUTHORED_TEXT = (
    "Authored: this card is manually authored, in a pair file kept in an external folder outside the repository. "
    "It was validated by the existing library loader (strict schema and cross-reference validation). "
    "It has no operator-approved golden snapshot. The file records no author and no date."
)


def build_status(card: dict, pair_slug: str, external_folder: Optional[str] = None) -> dict:
    """The status block for one authored card, derived only from the card itself.

    `external_folder` is None for a repository pair. For a pair from an external folder it is the folder's NAME
    (never a path); the status then says the card is manually authored, loader-validated and has no golden."""
    comp = card["compatibility"]
    ability = card["emergent_ability"]
    leak = card["leak_check"]
    if external_folder is None:
        authored = {
            "value": True,
            "source_file": f"pairs/{pair_slug}.json",
            "text": (
                "Authored: this result is a hand-written pair file in the repository's authored data. "
                "The file records no author and no date."
            ),
        }
    else:
        authored = {
            "value": True,
            "source_file": f"{EXTERNAL_FOLDER_FALLBACK} ({external_folder or 'name not recorded'}): {pair_slug}.json",
            "text": EXTERNAL_AUTHORED_TEXT,
        }
    status = {
        "authored": authored,
        "mechanical_checks": {
            "schema": "Passed: the pair file loaded and passed the strict schema and cross-reference validation.",
            "compatibility_status": comp["status"],
            "evaluated_conditions": comp["evaluated_conditions"],
            "contradiction": comp["contradiction"],
            "required_bridge": comp["required_bridge"],
            "unresolved_reason": comp["unresolved_reason"],
            "caveat": COMPATIBILITY_CAVEAT,
        },
        "independent_validation": {"recorded": False, "text": NO_INDEPENDENT_VALIDATION},
        "experimental": {"recorded": False, "text": EXPERIMENTAL_UNRECORDED},
        "emergent_provenance": {
            "ability": ability["provenance"],
            "governing_rule": ability["governing_rule"]["provenance"],
            "bridge_invented": "INVENTED_BRIDGE"
            in (ability["provenance"], ability["governing_rule"]["provenance"]),
        },
        "leak_check": {
            "detector": leak["detector"],
            "status": leak["status"],
            "findings": len(leak["findings"]),
            "claim": leak["claim"],
        },
        "dominance": card["dominance"],
    }
    status["summary"] = [
        "Authored",
        "Independently validated" if status["independent_validation"]["recorded"] else "Not independently validated",
        _bridge_summary(card),
    ]
    return status


COMPARISON_NOTE = (
    "Outcome labels (inherited, transformed, complementary, not carried) and every provenance link "
    "are the authors' own, copied from the card. This page does not measure how much of a trait carried over."
)
SLOT_NEW_NOTE = "Authored as new: its recorded parent is the fused ability, not either parent's slot."


def _label_index(char_a, char_b, ability: dict) -> dict:
    """id -> human-readable label, built only from names already in the authored data."""
    labels = {}
    for char in (char_a, char_b):
        for prop in char.properties:
            labels[prop.id] = f"{prop.name} ({char.name})"
        for trait in char.visual_traits:
            labels[trait.id] = f"{trait.slot.replace('_', ' ').capitalize()} ({char.name})"
    labels[ability["id"]] = f"{ability['name']} (fused ability)"
    labels[ability["governing_rule"]["id"]] = f"Governing rule of {ability['name']} (fused ability)"
    return labels


def build_comparison(card: dict, char_a, char_b) -> dict:
    """Parent-to-fusion comparison for one authored card.

    Every outcome, reason, parent link and design change is copied from the card. The only
    computed value is the tally, which is labelled as such. Ids with no known name keep the raw id as
    their label; no name is invented."""
    ability = card["emergent_ability"]
    labels = _label_index(char_a, char_b, ability)
    label = lambda ident: labels.get(ident, ident)  # noqa: E731
    chars = {"A": char_a, "B": char_b}
    props = {(side, p.id): p for side, c in chars.items() for p in c.properties}

    traits = []
    for t in sorted(card["traits"], key=lambda t: t["source"]):  # stable: A's traits, then B's, authored order kept
        prop = props.get((t["source"], t["property_id"]))
        traits.append(
            {
                "side": t["source"],
                "parent": t["character"],
                "property_id": t["property_id"],
                "label": label(t["property_id"]),
                "name": t["name"],
                "description": prop.description if prop else None,
                "outcome": t["outcome"],
                "result_text": t["result_text"],
                "reason": t.get("reason"),
            }
        )

    provenance = {r["slot"]: r for r in card["visual_provenance"]}
    slots = []
    for slot, fused in card["appearance"]["slots"].items():
        record = provenance[slot]
        slots.append(
            {
                "slot": slot,
                "a": next((v.descriptor for v in char_a.visual_traits if v.slot == slot), None),
                "b": next((v.descriptor for v in char_b.visual_traits if v.slot == slot), None),
                "fused": fused,
                "origin": record["origin"],
                "derived_from": [{"id": i, "label": label(i)} for i in record["parent_ids"]],
                "design_delta": record.get("design_delta"),
            }
        )

    tally = {}
    for t in traits:
        tally[t["outcome"]] = tally.get(t["outcome"], 0) + 1
    return {
        "parents": [{"side": "A", "name": card["sources"]["A"]}, {"side": "B", "name": card["sources"]["B"]}],
        "fusion_name": card["fusion_name"],
        "traits": traits,
        "tally": {"computed": True, "text": "Tally of the authors' outcome labels (computed here)", "counts": tally},
        "slots": slots,
        "ability": {"name": ability["name"], "derived_from": [{"id": i, "label": label(i)} for i in ability["direct_ancestor_ids"]]},
        "ancestry": [
            {"id": x["id"], "label": label(x["id"]), "kind": x["kind"], "character": x.get("character"), "provenance": x["provenance"]}
            for x in card["ancestry"]
        ],
        "note": COMPARISON_NOTE,
        "slot_new_note": SLOT_NEW_NOTE,
    }


def _ownership_view(slug: str, ownership: dict) -> dict:
    """Ownership shown for one character. `ownership` maps the slug of each user-supplied character to the
    value its file declared (or None). A character that is not in the map is an authored one: not recorded."""
    value = ownership.get(slug)
    return {
        "value": value,
        "label": OWNERSHIP_LABELS.get(value, OWNERSHIP_NOT_RECORDED),
        "user_supplied": slug in ownership,
    }


def build_view(data_dir: Optional[Path] = None, ownership: Optional[dict] = None, external_pairs: Optional[dict] = None) -> dict:
    """`ownership` is None for the normal viewer. When a dict is given (user characters are loaded), every
    character also carries an "ownership" entry; the values are self-declared and are never inferred.

    `external_pairs` maps the slug of each pair that came from a user's external folder to that folder's NAME.
    Those pairs get the external status text; every other pair is exactly as before."""
    external_pairs = external_pairs or {}
    library = load_library(data_dir)
    characters = list(library.characters.values())
    slug_of = {c.name: c.slug for c in characters}

    pairs: dict = {}
    for pair in library.pairs:
        key = pair_key(slug_of[pair.a], slug_of[pair.b])
        if key in pairs:
            raise ViewDataError(f"pair {pair.a!r} x {pair.b!r} is authored in both orders; the viewer treats pairs as unordered")
        card = finalize(
            assemble_card(library, pair), pair, library.characters[pair.a], library.characters[pair.b], library.allowlist
        )
        pairs[key] = {
            "key": key,
            "slugs": [slug_of[pair.a], slug_of[pair.b]],
            "names": [pair.a, pair.b],
            "card": card,
            "status": build_status(card, pair.slug, external_pairs[pair.slug] if pair.slug in external_pairs else None),
            "comparison": build_comparison(card, library.characters[pair.a], library.characters[pair.b]),
        }

    lookup = {c.slug: {} for c in characters}
    combos = []
    for first, second in combinations(characters, 2):
        key = pair_key(first.slug, second.slug)
        found = key if key in pairs else None
        lookup[first.slug][second.slug] = found
        lookup[second.slug][first.slug] = found
        combos.append({"a": first.slug, "b": second.slug, "pair": found})

    if pairs:
        default = list(next(iter(pairs.values()))["slugs"])
    else:
        default = [c.slug for c in characters[:2]]

    return {
        "schema": VIEW_SCHEMA,
        "not_synthesized": NOT_SYNTHESIZED,
        "notice": NOTICE,
        "characters": [
            dict(_character_view(c), ownership=_ownership_view(c.slug, ownership)) if ownership is not None else _character_view(c)
            for c in characters
        ],
        "pairs": pairs,
        "lookup": lookup,
        "combinations": combos,
        "default_selection": default,
    }


def resolve(view: dict, name_a: str, name_b: str) -> Optional[dict]:
    """The authored pair record for two character names, in either order, or None."""
    slug_of = {c["name"]: c["slug"] for c in view["characters"]}
    if name_a not in slug_of or name_b not in slug_of or name_a == name_b:
        return None
    key = view["lookup"][slug_of[name_a]][slug_of[name_b]]
    return None if key is None else view["pairs"][key]
