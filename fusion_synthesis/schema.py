"""
Fusion Synthesis — data shapes and strict validation (AUTH-011 §2).

Three JSON shapes: character card, pair card, style allowlist. Parsing is
strict: unknown keys, wrong types, bad enums and unresolved references are
SchemaError, never coerced. Every message names the file and field path.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional

from fusion_engine.types import ArchitecturalPlacement, Condition, ContributionType

CHARACTER_SCHEMA = "fusion-synthesis-character/1"
PAIR_SCHEMA = "fusion-synthesis-pair/1"
STYLE_SCHEMA = "fusion-synthesis-style-allowlist/1"

SLOTS = ("build", "face", "hair", "clothing", "palette", "signature_element", "ability_manifestation")
SCENE_FIELDS = ("setting", "mood", "lighting", "style")
ORIGINS = ("A", "B", "transformed", "new")
OUTCOMES = ("inherited", "transformed", "complementary", "not_carried")
DELTA_CHANGED = ("form", "material", "color", "scale", "structure", "function", "placement")
INTERACTION_PROVENANCES = ("DEFENSIBLY_DERIVED", "INVENTED_BRIDGE")
COMPARATORS = ("==", ">", "<", ">=", "<=")
PROMPT_CEILING_RANGE = (200, 2000)
FIXED_DOMINANCE = 50

# Token-level denylist matching ignores these and tokens shorter than
# MIN_TOKEN_LEN. FULL-PHRASE matching never does (AUTH-011 amendment 3).
STOP_WORDS = frozenset(
    {"a", "an", "the", "and", "or", "of", "for", "with", "in", "on", "at", "to", "by", "de", "la", "le", "el"}
)
MIN_TOKEN_LEN = 2

_TOKEN_RE = re.compile(r"[^\W_]+")
_PARAM_RE = re.compile(r"^--[a-z]+ [A-Za-z0-9:._-]+( --[a-z]+ [A-Za-z0-9:._-]+)*$")
_STYLE_TERM_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9 -]{0,38}[A-Za-z0-9])?$")


class SchemaError(ValueError):
    """Authored data is malformed or inconsistent. Exit code 2 in the demo."""


class StyleAllowlistError(SchemaError):
    """The style allowlist is invalid or collides with a denylist entry."""


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def tokens(text: str) -> list[str]:
    """Lower-cased alphanumeric tokens, in order."""
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def phrase(text: str) -> str:
    """Token sequence joined by single spaces: the full-phrase match form."""
    return " ".join(tokens(text))


def match_tokens(text: str) -> list[str]:
    """Tokens eligible for individual-token matching (not stop words, long enough)."""
    return [t for t in tokens(text) if len(t) >= MIN_TOKEN_LEN and t not in STOP_WORDS]


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if not slug:
        raise SchemaError(f"name {name!r} has no usable characters for a file slug")
    return slug


# ---------------------------------------------------------------------------
# Parsed shapes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PropertyDef:
    id: str
    name: str
    description: str
    contribution_type: ContributionType
    architectural_placement: ArchitecturalPlacement
    is_hard_limitation: bool
    is_prohibition: bool
    activation_condition: Optional[Condition]


@dataclass(frozen=True)
class SourceVisualTrait:
    id: str
    slot: str
    descriptor: str
    derives_from: tuple[str, ...]


@dataclass(frozen=True)
class CharacterCard:
    name: str
    slug: str
    epistemic_status: str
    properties: tuple[PropertyDef, ...]
    visual_traits: tuple[SourceVisualTrait, ...]
    proper_nouns: tuple[str, ...]
    exclusion_candidates: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class DesignDelta:
    changed: str
    from_text: str
    to_text: str


@dataclass(frozen=True)
class VisualTrait:
    descriptor: str
    origin: str
    parent_ids: tuple[str, ...]
    design_delta: Optional[DesignDelta]


@dataclass(frozen=True)
class InteractionDef:
    id: str
    description: str
    dependency_ids: tuple[str, ...]
    provenance: str
    is_disclosed_modification: bool


@dataclass(frozen=True)
class EmergentDef:
    id: str
    name: str
    description: str
    direct_ancestor_ids: tuple[str, ...]
    contribution_type: ContributionType
    architectural_placement: ArchitecturalPlacement
    limitations: tuple[str, ...]
    activation: Optional[str]


@dataclass(frozen=True)
class TraitOutcome:
    property_id: str
    outcome: str
    result_text: str
    reason: Optional[str]


@dataclass(frozen=True)
class Exclusion:
    item: str
    source: str
    reason: str


@dataclass(frozen=True)
class VisualSpec:
    subject: VisualTrait
    slots: tuple[tuple[str, VisualTrait], ...]
    scene: tuple[tuple[str, VisualTrait], ...]
    parameters: str


@dataclass(frozen=True)
class PairCard:
    a: str
    b: str
    slug: str
    dominance: int
    fusion_name: str
    concept: str
    prompt_max_chars: Optional[int]
    interaction: InteractionDef
    emergent: EmergentDef
    trait_outcomes: tuple[TraitOutcome, ...]
    exclusions: tuple[Exclusion, ...]
    visual: VisualSpec


@dataclass(frozen=True)
class StyleAllowlist:
    terms: tuple[str, ...]


# ---------------------------------------------------------------------------
# Low-level parse helpers
# ---------------------------------------------------------------------------

def _obj(value: Any, where: str) -> dict:
    if not isinstance(value, dict):
        raise SchemaError(f"{where}: expected an object")
    return value


def _keys(obj: dict, required: tuple, optional: tuple, where: str) -> None:
    missing = [k for k in required if k not in obj]
    unknown = sorted(k for k in obj if k not in required and k not in optional)
    if missing:
        raise SchemaError(f"{where}: missing key(s) {missing}")
    if unknown:
        raise SchemaError(f"{where}: unknown key(s) {unknown}")


def _text(obj: dict, key: str, where: str) -> str:
    value = obj[key]
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(f"{where}.{key}: expected a non-empty string")
    if value != value.strip():
        raise SchemaError(f"{where}.{key}: must not have leading or trailing whitespace")
    if "\n" in value or "\r" in value:
        raise SchemaError(f"{where}.{key}: must be a single line")
    return value


def _opt_text(obj: dict, key: str, where: str) -> Optional[str]:
    if obj.get(key) is None:
        return None
    return _text(obj, key, where)


def _text_list(obj: dict, key: str, where: str, min_len: int = 0) -> tuple[str, ...]:
    value = obj[key]
    if not isinstance(value, list):
        raise SchemaError(f"{where}.{key}: expected a list")
    out = tuple(_text({"v": item}, "v", f"{where}.{key}[{i}]") for i, item in enumerate(value))
    if len(out) < min_len:
        raise SchemaError(f"{where}.{key}: needs at least {min_len} entr{'y' if min_len == 1 else 'ies'}")
    if len(set(out)) != len(out):
        raise SchemaError(f"{where}.{key}: duplicate entries")
    return out


def _bool(obj: dict, key: str, where: str, default: bool) -> bool:
    value = obj.get(key, default)
    if not isinstance(value, bool):
        raise SchemaError(f"{where}.{key}: expected true or false")
    return value


def _choice(obj: dict, key: str, allowed: tuple, where: str) -> str:
    value = obj[key]
    if value not in allowed:
        raise SchemaError(f"{where}.{key}: {value!r} is not one of {list(allowed)}")
    return value


def _enum(enum_cls: Any, obj: dict, key: str, where: str) -> Any:
    value = obj[key]
    if not isinstance(value, str) or value not in enum_cls.__members__:
        raise SchemaError(f"{where}.{key}: {value!r} is not one of {sorted(enum_cls.__members__)}")
    return enum_cls[value]


def _condition(raw: Any, where: str) -> Optional[Condition]:
    if raw is None:
        return None
    d = _obj(raw, where)
    _keys(d, ("variable", "comparator", "value"), (), where)
    value = d["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SchemaError(f"{where}.value: expected a number")
    return Condition(
        variable=_text(d, "variable", where),
        comparator=_choice(d, "comparator", COMPARATORS, where),
        value=float(value),
    )


def _check_schema(obj: dict, expected: str, where: str) -> None:
    if obj.get("schema") != expected:
        raise SchemaError(f"{where}.schema: expected {expected!r}, got {obj.get('schema')!r}")


# ---------------------------------------------------------------------------
# Character card
# ---------------------------------------------------------------------------

def parse_character(raw: Any, where: str = "<character>") -> CharacterCard:
    d = _obj(raw, where)
    _keys(
        d,
        ("schema", "name", "epistemic_status", "properties", "visual_traits", "proper_nouns", "exclusion_candidates"),
        (),
        where,
    )
    _check_schema(d, CHARACTER_SCHEMA, where)
    name = _text(d, "name", where)
    slug = slugify(name)
    if d["epistemic_status"] != "FICTIONAL":
        raise SchemaError(f"{where}.epistemic_status: only 'FICTIONAL' is accepted in Phase 1")

    if not isinstance(d["properties"], list) or not d["properties"]:
        raise SchemaError(f"{where}.properties: expected a non-empty list")
    props = []
    for i, rp in enumerate(d["properties"]):
        w = f"{where}.properties[{i}]"
        p = _obj(rp, w)
        _keys(
            p,
            ("id", "name", "description", "contribution_type", "architectural_placement"),
            ("is_hard_limitation", "is_prohibition", "activation_condition"),
            w,
        )
        props.append(
            PropertyDef(
                id=_text(p, "id", w),
                name=_text(p, "name", w),
                description=_text(p, "description", w),
                contribution_type=_enum(ContributionType, p, "contribution_type", w),
                architectural_placement=_enum(ArchitecturalPlacement, p, "architectural_placement", w),
                is_hard_limitation=_bool(p, "is_hard_limitation", w, False),
                is_prohibition=_bool(p, "is_prohibition", w, False),
                activation_condition=_condition(p.get("activation_condition"), f"{w}.activation_condition"),
            )
        )
    prop_ids = [p.id for p in props]
    if len(set(prop_ids)) != len(prop_ids):
        raise SchemaError(f"{where}.properties: duplicate property id")
    for pid in prop_ids:
        if not pid.startswith(slug + "."):
            raise SchemaError(f"{where}.properties: id {pid!r} must start with {slug + '.'!r}")

    if not isinstance(d["visual_traits"], list):
        raise SchemaError(f"{where}.visual_traits: expected a list")
    traits = []
    for i, rt in enumerate(d["visual_traits"]):
        w = f"{where}.visual_traits[{i}]"
        t = _obj(rt, w)
        _keys(t, ("id", "slot", "descriptor", "derives_from"), (), w)
        derives = _text_list(t, "derives_from", w)
        for ref in derives:
            if ref not in prop_ids:
                raise SchemaError(f"{w}.derives_from: {ref!r} is not a property id of {name!r}")
        traits.append(
            SourceVisualTrait(
                id=_text(t, "id", w),
                slot=_choice(t, "slot", SLOTS, w),
                descriptor=_text(t, "descriptor", w),
                derives_from=derives,
            )
        )
    trait_ids = [t.id for t in traits]
    if len(set(trait_ids)) != len(trait_ids):
        raise SchemaError(f"{where}.visual_traits: duplicate trait id")
    for tid in trait_ids:
        if not tid.startswith(slug + "."):
            raise SchemaError(f"{where}.visual_traits: id {tid!r} must start with {slug + '.'!r}")
    if set(trait_ids) & set(prop_ids):
        raise SchemaError(f"{where}: a visual trait id collides with a property id")
    by_slot = sorted(t.slot for t in traits)
    if by_slot != sorted(SLOTS):
        raise SchemaError(f"{where}.visual_traits: needs exactly one trait per slot {list(SLOTS)}; got {by_slot}")

    proper_nouns = _text_list(d, "proper_nouns", where)
    ex = []
    if not isinstance(d["exclusion_candidates"], list):
        raise SchemaError(f"{where}.exclusion_candidates: expected a list")
    for i, re_ in enumerate(d["exclusion_candidates"]):
        w = f"{where}.exclusion_candidates[{i}]"
        e = _obj(re_, w)
        _keys(e, ("item", "reason"), (), w)
        ex.append((_text(e, "item", w), _text(e, "reason", w)))

    return CharacterCard(
        name=name,
        slug=slug,
        epistemic_status="FICTIONAL",
        properties=tuple(props),
        visual_traits=tuple(traits),
        proper_nouns=proper_nouns,
        exclusion_candidates=tuple(ex),
    )


# ---------------------------------------------------------------------------
# Pair card
# ---------------------------------------------------------------------------

def _parse_trait(raw: Any, where: str) -> VisualTrait:
    d = _obj(raw, where)
    _keys(d, ("descriptor", "origin", "parent_ids"), ("design_delta",), where)
    origin = _choice(d, "origin", ORIGINS, where)
    parents = _text_list(d, "parent_ids", where, min_len=1)
    raw_delta = d.get("design_delta")
    delta = None
    if origin == "transformed":
        if raw_delta is None:
            raise SchemaError(f"{where}.design_delta: required when origin is 'transformed'")
        dd = _obj(raw_delta, f"{where}.design_delta")
        _keys(dd, ("changed", "from", "to"), (), f"{where}.design_delta")
        delta = DesignDelta(
            changed=_choice(dd, "changed", DELTA_CHANGED, f"{where}.design_delta"),
            from_text=_text(dd, "from", f"{where}.design_delta"),
            to_text=_text(dd, "to", f"{where}.design_delta"),
        )
    elif raw_delta is not None:
        raise SchemaError(f"{where}.design_delta: only allowed when origin is 'transformed'")
    return VisualTrait(descriptor=_text(d, "descriptor", where), origin=origin, parent_ids=parents, design_delta=delta)


def parse_pair(raw: Any, where: str = "<pair>") -> PairCard:
    d = _obj(raw, where)
    _keys(
        d,
        (
            "schema", "a", "b", "dominance", "fusion_name", "concept", "interaction",
            "emergent_ability", "trait_outcomes", "exclusions", "visual",
        ),
        ("prompt_max_chars",),
        where,
    )
    _check_schema(d, PAIR_SCHEMA, where)
    a, b = _text(d, "a", where), _text(d, "b", where)
    if a == b:
        raise SchemaError(f"{where}: a and b must be different characters")
    if isinstance(d["dominance"], bool) or d["dominance"] != FIXED_DOMINANCE:
        raise SchemaError(f"{where}.dominance: only {FIXED_DOMINANCE} is accepted in Phase 1")

    ceiling = d.get("prompt_max_chars")
    if ceiling is not None:
        lo, hi = PROMPT_CEILING_RANGE
        if isinstance(ceiling, bool) or not isinstance(ceiling, int) or not lo <= ceiling <= hi:
            raise SchemaError(f"{where}.prompt_max_chars: expected an integer from {lo} to {hi}")

    wi = f"{where}.interaction"
    i = _obj(d["interaction"], wi)
    _keys(i, ("id", "description", "dependency_ids", "provenance", "is_disclosed_modification"), (), wi)
    interaction = InteractionDef(
        id=_text(i, "id", wi),
        description=_text(i, "description", wi),
        dependency_ids=_text_list(i, "dependency_ids", wi, min_len=1),
        provenance=_choice(i, "provenance", INTERACTION_PROVENANCES, wi),
        is_disclosed_modification=_bool(i, "is_disclosed_modification", wi, False),
    )

    we = f"{where}.emergent_ability"
    e = _obj(d["emergent_ability"], we)
    _keys(
        e,
        ("id", "name", "description", "direct_ancestor_ids", "contribution_type", "architectural_placement",
         "limitations", "activation"),
        (),
        we,
    )
    emergent = EmergentDef(
        id=_text(e, "id", we),
        name=_text(e, "name", we),
        description=_text(e, "description", we),
        direct_ancestor_ids=_text_list(e, "direct_ancestor_ids", we, min_len=1),
        contribution_type=_enum(ContributionType, e, "contribution_type", we),
        architectural_placement=_enum(ArchitecturalPlacement, e, "architectural_placement", we),
        limitations=_text_list(e, "limitations", we, min_len=1),
        activation=_opt_text(e, "activation", we),
    )

    if not isinstance(d["trait_outcomes"], list) or not d["trait_outcomes"]:
        raise SchemaError(f"{where}.trait_outcomes: expected a non-empty list")
    outcomes = []
    for n, ro in enumerate(d["trait_outcomes"]):
        w = f"{where}.trait_outcomes[{n}]"
        o = _obj(ro, w)
        _keys(o, ("property_id", "outcome", "result_text"), ("reason",), w)
        outcome = _choice(o, "outcome", OUTCOMES, w)
        reason = _opt_text(o, "reason", w)
        if outcome == "not_carried" and reason is None:
            raise SchemaError(f"{w}.reason: required when outcome is 'not_carried'")
        outcomes.append(TraitOutcome(_text(o, "property_id", w), outcome, _text(o, "result_text", w), reason))

    if not isinstance(d["exclusions"], list):
        raise SchemaError(f"{where}.exclusions: expected a list")
    exclusions = []
    for n, rx in enumerate(d["exclusions"]):
        w = f"{where}.exclusions[{n}]"
        x = _obj(rx, w)
        _keys(x, ("item", "source", "reason"), (), w)
        exclusions.append(Exclusion(_text(x, "item", w), _choice(x, "source", ("A", "B"), w), _text(x, "reason", w)))

    wv = f"{where}.visual"
    v = _obj(d["visual"], wv)
    _keys(v, ("subject", "slots", "setting", "mood", "lighting", "style", "parameters"), (), wv)
    raw_slots = _obj(v["slots"], f"{wv}.slots")
    if sorted(raw_slots) != sorted(SLOTS):
        raise SchemaError(f"{wv}.slots: needs exactly the slots {list(SLOTS)}; got {sorted(raw_slots)}")
    parameters = _text(v, "parameters", wv)
    if not _PARAM_RE.match(parameters):
        raise SchemaError(f"{wv}.parameters: {parameters!r} is not valid Midjourney parameter syntax (--name value ...)")
    visual = VisualSpec(
        subject=_parse_trait(v["subject"], f"{wv}.subject"),
        slots=tuple((s, _parse_trait(raw_slots[s], f"{wv}.slots.{s}")) for s in SLOTS),
        scene=tuple((s, _parse_trait(v[s], f"{wv}.{s}")) for s in SCENE_FIELDS),
        parameters=parameters,
    )

    return PairCard(
        a=a, b=b, slug=f"{slugify(a)}__{slugify(b)}", dominance=FIXED_DOMINANCE,
        fusion_name=_text(d, "fusion_name", where), concept=_text(d, "concept", where),
        prompt_max_chars=ceiling, interaction=interaction, emergent=emergent,
        trait_outcomes=tuple(outcomes), exclusions=tuple(exclusions), visual=visual,
    )


def visual_traits_of(pair: PairCard) -> list[tuple[str, VisualTrait]]:
    """Every prompt-contributing trait, labelled, in prompt order."""
    return [("subject", pair.visual.subject), *pair.visual.slots, *pair.visual.scene]


def validate_pair(pair: PairCard, card_a: CharacterCard, card_b: CharacterCard) -> None:
    """Cross-validate a pair against its two character cards."""
    where = f"pair {pair.a} x {pair.b}"
    if pair.a != card_a.name or pair.b != card_b.name:
        raise SchemaError(f"{where}: character cards do not match the pair's a/b names")
    props = {p.id: p for p in (*card_a.properties, *card_b.properties)}
    scoped = pair.slug + "."
    for item_id, label in ((pair.interaction.id, "interaction"), (pair.emergent.id, "emergent ability")):
        if not item_id.startswith(scoped):
            raise SchemaError(f"{where}: {label} id {item_id!r} must start with {scoped!r}")
    if pair.interaction.id == pair.emergent.id:
        raise SchemaError(f"{where}: interaction and emergent ability need different ids")
    for ref in pair.interaction.dependency_ids:
        if ref not in props:
            raise SchemaError(f"{where}: interaction dependency {ref!r} is not a property of either character")
    for ref in pair.emergent.direct_ancestor_ids:
        if ref not in props:
            raise SchemaError(f"{where}: emergent ancestor {ref!r} is not a property of either character")

    seen = [o.property_id for o in pair.trait_outcomes]
    if len(set(seen)) != len(seen):
        raise SchemaError(f"{where}: a property appears more than once in trait_outcomes")
    if set(seen) != set(props):
        missing, extra = sorted(set(props) - set(seen)), sorted(set(seen) - set(props))
        raise SchemaError(f"{where}: trait_outcomes must cover every property exactly once (missing {missing}, unknown {extra})")

    src = {t.id: (t, card_a.name if t in card_a.visual_traits else card_b.name)
           for t in (*card_a.visual_traits, *card_b.visual_traits)}
    ids_a = {t.id for t in card_a.visual_traits}
    ids_b = {t.id for t in card_b.visual_traits}
    for label, trait in visual_traits_of(pair):
        w = f"{where}: visual trait {label!r}"
        if trait.origin in ("A", "B"):
            pool = ids_a if trait.origin == "A" else ids_b
            if len(trait.parent_ids) != 1 or trait.parent_ids[0] not in pool:
                raise SchemaError(f"{w}: origin {trait.origin} needs exactly one parent id from that character's visual traits")
            if trait.descriptor != src[trait.parent_ids[0]][0].descriptor:
                raise SchemaError(f"{w}: origin {trait.origin} must reuse its parent's descriptor verbatim")
        elif trait.origin == "new":
            if list(trait.parent_ids) != [pair.emergent.id]:
                raise SchemaError(f"{w}: origin 'new' must have exactly the emergent ability id as its parent")
        else:  # transformed — structural consistency only (AUTH-011 amendment: no similarity metric)
            for pid in trait.parent_ids:
                if pid not in ids_a and pid not in ids_b:
                    raise SchemaError(f"{w}: parent id {pid!r} is not a visual trait of either character")
            for pid in trait.parent_ids:
                if normalize(trait.descriptor) == normalize(src[pid][0].descriptor):
                    raise SchemaError(f"{w}: a transformed descriptor must differ from its parent descriptor")
            delta = trait.design_delta
            if normalize(delta.from_text) == normalize(delta.to_text):
                raise SchemaError(f"{w}: design_delta 'from' and 'to' must differ")
            if normalize(delta.to_text) not in normalize(trait.descriptor):
                raise SchemaError(f"{w}: design_delta 'to' value must appear in the transformed descriptor")


# ---------------------------------------------------------------------------
# Style allowlist and denylists
# ---------------------------------------------------------------------------

def parse_style_allowlist(raw: Any, where: str = "style_allowlist.json") -> StyleAllowlist:
    try:
        d = _obj(raw, where)
        _keys(d, ("schema", "terms"), (), where)
        _check_schema(d, STYLE_SCHEMA, where)
        if not isinstance(d["terms"], list):
            raise SchemaError(f"{where}.terms: expected a list")
        terms, seen = [], set()
        for i, term in enumerate(d["terms"]):
            w = f"{where}.terms[{i}]"
            if not isinstance(term, str) or not _STYLE_TERM_RE.match(term):
                raise StyleAllowlistError(
                    f"{w}: {term!r} must be 1-40 characters: letters, digits, spaces and hyphens, "
                    "with no leading or trailing space"
                )
            key = phrase(term)
            if key in seen:
                raise StyleAllowlistError(f"{w}: duplicate term {term!r}")
            seen.add(key)
            terms.append(term)
        return StyleAllowlist(terms=tuple(terms))
    except StyleAllowlistError:
        raise
    except SchemaError as exc:
        raise StyleAllowlistError(str(exc)) from None


def character_denylist(card: CharacterCard) -> list[tuple[str, str]]:
    entries = [(card.name, f"{card.name}: name")]
    entries += [(p.name, f"{card.name}: property name") for p in card.properties]
    entries += [(n, f"{card.name}: proper noun") for n in card.proper_nouns]
    return entries


def pair_denylist(pair: PairCard, card_a: CharacterCard, card_b: CharacterCard) -> list[tuple[str, str]]:
    entries = character_denylist(card_a) + character_denylist(card_b)
    entries.append((pair.fusion_name, f"{pair.slug}: fusion name"))
    entries.append((pair.emergent.name, f"{pair.slug}: emergent ability name"))
    return entries


def check_allowlist_against_denylist(allowlist: StyleAllowlist, entries: list[tuple[str, str]]) -> None:
    """Denylist precedence at load time: an allowlisted term that matches ANY
    denylist entry (full phrase, containment, or any shared significant token)
    is a validation failure. It is never treated as exempt."""
    for term in allowlist.terms:
        term_phrase, term_tokens = phrase(term), set(match_tokens(term))
        for entry, source in entries:
            entry_phrase = phrase(entry)
            if not entry_phrase:
                continue
            shared = term_tokens & set(match_tokens(entry))
            if term_phrase == entry_phrase or f" {entry_phrase} " in f" {term_phrase} " or shared:
                raise StyleAllowlistError(
                    f"style allowlist term {term!r} matches denylist entry {entry!r} ({source}); "
                    "the allowlist cannot override the denylist"
                )
