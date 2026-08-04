# =============================================================
#  MYTHOS-SYNC FRAMEWORK — MODULE 2: LOGIC AUDITOR
#  The Enforcer. Validates power assignments against modality
#  rules and transposes illegal combos to legal equivalents.
# =============================================================

import random

# Modality rank for comparison — how far a power can bend the world.
MODALITY_RANK = {"LEGACY": 1, "GROUNDED": 2, "HIGH_CONCEPT": 3}

# ------------------------------------------------------------------
# POWER FAMILIES — the semantic layer beneath modality
#
# Modality answers "how much can this person bend the world?". Family answers
# "what kind of excellence is this?". They are independent axes: Domain
# Expansion and Strategic Genius are the same KIND of power (imposing order on
# a battlefield) at wildly different scales, which is exactly why one grounds
# into the other.
#
# Family is what makes a power's neighbours computable instead of hand-listed.
# ------------------------------------------------------------------
COGNITION  = "COGNITION"    # strategy, invention, seeing the system
INFLUENCE  = "INFLUENCE"    # rhetoric, authority, moving people
DISCIPLINE = "DISCIPLINE"   # body, will, endurance, mastery of self
PERCEPTION = "PERCEPTION"   # reading rooms, people, situations

POWER_FAMILIES = (COGNITION, INFLUENCE, DISCIPLINE, PERCEPTION)


# ------------------------------------------------------------------
# POWER REGISTRY — every power tagged with its minimum modality and family
# ------------------------------------------------------------------
POWER_REGISTRY = {
    # HIGH_CONCEPT only
    "Domain Expansion":       {"min_modality": "HIGH_CONCEPT", "cost_factor": 9,  "family": COGNITION},
    "Titan-Shifting":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 8,  "family": DISCIPLINE},
    "Reality Glitch":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 10, "family": COGNITION},
    "Equivalent Exchange":    {"min_modality": "HIGH_CONCEPT", "cost_factor": 7,  "family": COGNITION},
    "Cursed Energy":          {"min_modality": "HIGH_CONCEPT", "cost_factor": 6,  "family": INFLUENCE},
    "Spiral Power":           {"min_modality": "HIGH_CONCEPT", "cost_factor": 8,  "family": DISCIPLINE},
    "Soul Resonance":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 5,  "family": DISCIPLINE},
    "Angelic Override":       {"min_modality": "HIGH_CONCEPT", "cost_factor": 9,  "family": INFLUENCE},

    # GROUNDED or higher — the body exceeds ordinary human limits
    "Espionage":              {"min_modality": "GROUNDED",     "cost_factor": 3,  "family": PERCEPTION},
    "Kinetic Mastery":        {"min_modality": "GROUNDED",     "cost_factor": 4,  "family": DISCIPLINE},
    "Electromagnetic Pulse":  {"min_modality": "GROUNDED",     "cost_factor": 4,  "family": COGNITION},
    "One-Inch Punch":         {"min_modality": "GROUNDED",     "cost_factor": 2,  "family": DISCIPLINE},

    # LEGACY or higher — human excellence, no rules bent. Anyone can have these.
    # Grouped by family: the tier was 3/5 COGNITION, which made 91% of LEGACY
    # fusions read as strategists regardless of who they were built from.

    # -- COGNITION: understanding the system
    "Strategic Genius":       {"min_modality": "LEGACY",       "cost_factor": 1,  "family": COGNITION},
    "The Scientific Method":  {"min_modality": "LEGACY",       "cost_factor": 1,  "family": COGNITION},
    "Art of War":             {"min_modality": "LEGACY",       "cost_factor": 2,  "family": COGNITION},
    "Pattern Recognition":    {"min_modality": "LEGACY",       "cost_factor": 1,  "family": COGNITION},
    "Mastermind Architecture": {"min_modality": "LEGACY",      "cost_factor": 2,  "family": COGNITION},
    # Understanding conflict better than anyone is human excellence; moving
    # faster than a human can is not. The name was ambiguous, the concept is
    # LEGACY. Reacting past human limits stays GROUNDED as Kinetic Mastery.
    "Tactical Brilliance":    {"min_modality": "LEGACY",       "cost_factor": 3,  "family": COGNITION},

    # -- INFLUENCE: moving people, and moving generations
    "Rhetoric & Legacy":      {"min_modality": "LEGACY",       "cost_factor": 1,  "family": INFLUENCE},
    "Cultural Resonance":     {"min_modality": "LEGACY",       "cost_factor": 2,  "family": INFLUENCE},
    "Diplomatic Mastery":     {"min_modality": "LEGACY",       "cost_factor": 1,  "family": INFLUENCE},
    "Symbolic Authority":     {"min_modality": "LEGACY",       "cost_factor": 2,  "family": INFLUENCE},

    # -- DISCIPLINE: the mind commands the body
    "Indomitable Will":       {"min_modality": "LEGACY",       "cost_factor": 1,  "family": DISCIPLINE},
    "Martial Perfection":     {"min_modality": "LEGACY",       "cost_factor": 2,  "family": DISCIPLINE},
    "Adaptive Combat":        {"min_modality": "LEGACY",       "cost_factor": 2,  "family": DISCIPLINE},
    "Iron Discipline":        {"min_modality": "LEGACY",       "cost_factor": 1,  "family": DISCIPLINE},

    # -- PERCEPTION: reading rooms, people, situations
    "Intuitive Insight":      {"min_modality": "LEGACY",       "cost_factor": 1,  "family": PERCEPTION},
    "Situational Awareness":  {"min_modality": "LEGACY",       "cost_factor": 1,  "family": PERCEPTION},
    "Psychological Mastery":  {"min_modality": "LEGACY",       "cost_factor": 2,  "family": PERCEPTION},
    "Memory Palace":          {"min_modality": "LEGACY",       "cost_factor": 1,  "family": PERCEPTION},
}


def family_of(power_name: str) -> str:
    """The family a power belongs to, or None if it isn't registered."""
    entry = POWER_REGISTRY.get(power_name)
    return entry["family"] if entry else None


def family_members(family: str, max_modality: str = "HIGH_CONCEPT") -> list:
    """Every registered power in `family` that is legal at `max_modality`."""
    ceiling = MODALITY_RANK[max_modality]
    return [
        name for name, entry in POWER_REGISTRY.items()
        if entry["family"] == family
        and MODALITY_RANK[entry["min_modality"]] <= ceiling
    ]

# ------------------------------------------------------------------
# TRANSPOSITION TABLE — illegal power → legal equivalents
#
# Each power lists several thematic descendants rather than a single fixed
# one, because a single target made every grounded fusion converge on the
# same handful of powers. Entries are ordered richest-first; the grounding
# rule below keeps the highest tier that is legal for the fusion, so a power
# is lowered only as far as it has to be.
#
# GROUNDED powers need entries too: they are illegal for a LEGACY fusion,
# and without a mapping they all fell through to the default.
# ------------------------------------------------------------------
TRANSPOSITION_MAP = {
    # HIGH_CONCEPT — battlefield control, transformation, rule-breaking
    "Domain Expansion":    ["Tactical Brilliance", "Mastermind Architecture", "Strategic Genius", "Art of War"],
    "Titan-Shifting":      ["Kinetic Mastery", "One-Inch Punch", "Martial Perfection", "Indomitable Will"],
    "Reality Glitch":      ["Electromagnetic Pulse", "Pattern Recognition", "The Scientific Method"],
    "Equivalent Exchange": ["Tactical Brilliance", "Art of War", "The Scientific Method"],
    "Cursed Energy":       ["Rhetoric & Legacy", "Symbolic Authority", "Cultural Resonance"],
    "Spiral Power":        ["Kinetic Mastery", "One-Inch Punch", "Iron Discipline", "Indomitable Will"],
    "Soul Resonance":      ["Kinetic Mastery", "Adaptive Combat", "Martial Perfection"],
    "Angelic Override":    ["Symbolic Authority", "Rhetoric & Legacy", "Diplomatic Mastery"],

    # GROUNDED — only illegal when the fusion is LEGACY. Every entry now stays
    # inside the source power's family: a perception-driven person grounds into
    # a different EXPRESSION of perception, not into somebody else's essence.
    "Espionage":             ["Situational Awareness", "Psychological Mastery"],
    "Kinetic Mastery":       ["Martial Perfection", "Iron Discipline", "Indomitable Will"],
    "Electromagnetic Pulse": ["The Scientific Method", "Pattern Recognition"],
    "One-Inch Punch":        ["Martial Perfection", "Iron Discipline", "Indomitable Will"],
}

# Last-resort fallback — universal, so legal at every modality.
DEFAULT_TRANSPOSITIONS = ["Indomitable Will", "Strategic Genius", "Art of War"]


def _grounding_candidates(power_name: str) -> list:
    """Where a power may ground to, curated entry first, family second.

    An explicit TRANSPOSITION_MAP entry is a deliberate authorial choice and
    wins. Without one, the power's own family supplies the neighbours — which
    is the point of families: a power no longer needs a hand-written mapping
    to ground somewhere thematically adjacent.
    """
    if power_name in TRANSPOSITION_MAP:
        return TRANSPOSITION_MAP[power_name]

    family = family_of(power_name)
    if family:
        kin = [p for p in family_members(family) if p != power_name]
        if kin:
            return kin

    return DEFAULT_TRANSPOSITIONS


def ground_power(power_name: str, fusion_rank: int) -> str:
    """Pick a legal stand-in for a power that exceeds the fusion's ceiling.

    Keeps the richest tier still legal for the fusion — Soul Resonance
    becomes Kinetic Mastery for a GROUNDED fusion but has to fall further,
    to Art of War or Rhetoric & Legacy, for a LEGACY one — then prefers a
    stand-in from the power's own family, and chooses at random among what
    remains so grounded fusions don't all look alike.
    """
    candidates = [
        p for p in _grounding_candidates(power_name)
        if p in POWER_REGISTRY
        and MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] <= fusion_rank
    ]
    if not candidates:
        return "Indomitable Will"  # universal — legal at every modality

    # Fall as little as possible: keep the richest legal tier.
    best = max(MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] for p in candidates)
    candidates = [
        p for p in candidates
        if MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] == best
    ]

    # Then stay in the family if this tier offers a relative.
    kin = [p for p in candidates if family_of(p) == family_of(power_name)]
    return random.choice(kin or candidates)


# ------------------------------------------------------------------
# CORE AUDIT FUNCTION
# ------------------------------------------------------------------
def audit_power(power_name: str, fusion_profile: dict) -> dict:
    """
    Checks if a power is legal for the fusion's modality.
    Returns an audit result with status, cost, and any transposition.
    
    fusion_profile = output from classify_fusion() in modality_classifier.py
    """
    fusion_modality = fusion_profile.get("modality", "GROUNDED")
    fusion_name     = fusion_profile.get("fusion_name", "Unknown Fusion")

    power = POWER_REGISTRY.get(power_name)

    # Power not in registry — flag as UNVERIFIED, allow cautiously
    if not power:
        return {
            "fusion":       fusion_name,
            "power":        power_name,
            "status":       "⚠️  UNVERIFIED",
            "message":      f"'{power_name}' is not in the Power Registry. Add it to enforce rules.",
            "cost_factor":  "?",
            "transposed_to": None
        }

    required_rank = MODALITY_RANK[power["min_modality"]]
    fusion_rank   = MODALITY_RANK[fusion_modality]

    # ✅ LEGAL — fusion modality meets the power's requirement
    if fusion_rank >= required_rank:
        return {
            "fusion":        fusion_name,
            "power":         power_name,
            "status":        "✅ APPROVED",
            "message":       f"'{power_name}' is legal for {fusion_modality} modality.",
            "cost_factor":   power["cost_factor"],
            "transposed_to": None
        }

    # ❌ ILLEGAL — power exceeds fusion's modality ceiling
    else:
        transposed = ground_power(power_name, fusion_rank)
        return {
            "fusion":        fusion_name,
            "power":         power_name,
            "status":        "❌ FLAGGED → TRANSPOSED",
            "message":       (
                f"'{power_name}' requires {power['min_modality']} but fusion is {fusion_modality}. "
                f"Grounding Filter activated."
            ),
            "cost_factor":   POWER_REGISTRY[transposed]["cost_factor"],
            "transposed_to": transposed
        }


# ------------------------------------------------------------------
# FULL PROFILE AUDIT — audits ALL powers for a fusion at once
# ------------------------------------------------------------------
def audit_profile(fusion_profile: dict, powers_to_test: list) -> list:
    """
    Runs audit_power() on a list of powers for one fusion.
    Returns a full audit report as a list of results.
    """
    print(f"\n{'═'*55}")
    print(f"  🔍 AUDIT REPORT: {fusion_profile['fusion_name']}")
    print(f"  Modality: {fusion_profile['modality']} | Dominant: {fusion_profile['dominant']}")
    print(f"{'═'*55}")

    results = []
    for power in powers_to_test:
        result = audit_power(power, fusion_profile)
        results.append(result)

        print(f"\n  Power Tested : {result['power']}")
        print(f"  Status       : {result['status']}")
        print(f"  Message      : {result['message']}")
        print(f"  Cost Factor  : {result['cost_factor']}")
        if result["transposed_to"]:
            print(f"  ⚡ Transposed : {result['power']} → {result['transposed_to']}")

    print(f"\n{'═'*55}\n")
    return results


# ------------------------------------------------------------------
# QUICK TEST
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Simulate fusion profiles (normally these come from classifier)
    legacy_fusion = {
        "fusion_name": "Malcolm X x Bruce Lee",
        "modality":    "LEGACY",
        "dominant":    "Malcolm X (dominant)",
        "tags":        ["rhetoric", "martial_arts", "strategy"]
    }

    high_concept_fusion = {
        "fusion_name": "Maka x Vash",
        "modality":    "HIGH_CONCEPT",
        "dominant":    "balanced blend",
        "tags":        ["soul_resonance", "pacifist", "angelic_power"]
    }

    # Test 1: Try giving a LEGACY fusion supernatural powers → should flag & transpose
    audit_profile(legacy_fusion, [
        "Domain Expansion",   # ❌ too powerful for LEGACY
        "Cursed Energy",      # ❌ too powerful for LEGACY
        "Art of War",         # ✅ legal
        "Strategic Genius",   # ✅ legal
    ])

    # Test 2: HIGH_CONCEPT fusion — everything should pass
    audit_profile(high_concept_fusion, [
        "Soul Resonance",     # ✅
        "Reality Glitch",     # ✅
        "Angelic Override",   # ✅
        "Strategic Genius",   # ✅ (universal)
    ])