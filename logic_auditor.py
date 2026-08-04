# =============================================================
#  MYTHOS-SYNC FRAMEWORK — MODULE 2: LOGIC AUDITOR
#  The Enforcer. Validates power assignments against modality
#  rules and transposes illegal combos to legal equivalents.
# =============================================================

import random

# ------------------------------------------------------------------
# POWER REGISTRY — Every power tagged with its minimum modality
# ------------------------------------------------------------------
POWER_REGISTRY = {
    # HIGH_CONCEPT only
    "Domain Expansion":      {"min_modality": "HIGH_CONCEPT", "cost_factor": 9},
    "Titan-Shifting":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 8},
    "Reality Glitch":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 10},
    "Equivalent Exchange":    {"min_modality": "HIGH_CONCEPT", "cost_factor": 7},
    "Cursed Energy":          {"min_modality": "HIGH_CONCEPT", "cost_factor": 6},
    "Spiral Power":           {"min_modality": "HIGH_CONCEPT", "cost_factor": 8},
    "Soul Resonance":         {"min_modality": "HIGH_CONCEPT", "cost_factor": 5},
    "Angelic Override":       {"min_modality": "HIGH_CONCEPT", "cost_factor": 9},

    # GROUNDED or higher
    "Espionage":              {"min_modality": "GROUNDED",     "cost_factor": 3},
    "Tactical Brilliance":    {"min_modality": "GROUNDED",     "cost_factor": 3},
    "Kinetic Mastery":        {"min_modality": "GROUNDED",     "cost_factor": 4},
    "Electromagnetic Pulse":  {"min_modality": "GROUNDED",     "cost_factor": 4},
    "One-Inch Punch":         {"min_modality": "GROUNDED",     "cost_factor": 2},

    # LEGACY or higher (universal — anyone can have these)
    "Strategic Genius":       {"min_modality": "LEGACY",      "cost_factor": 1},
    "Indomitable Will":       {"min_modality": "LEGACY",      "cost_factor": 1},
    "The Scientific Method":  {"min_modality": "LEGACY",      "cost_factor": 1},
    "Rhetoric & Legacy":      {"min_modality": "LEGACY",      "cost_factor": 1},
    "Art of War":             {"min_modality": "LEGACY",      "cost_factor": 2},
}

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
    "Domain Expansion":    ["Tactical Brilliance", "Strategic Genius", "Art of War"],
    "Titan-Shifting":      ["Kinetic Mastery", "One-Inch Punch", "Indomitable Will"],
    "Reality Glitch":      ["Electromagnetic Pulse", "Espionage", "The Scientific Method"],
    "Equivalent Exchange": ["Tactical Brilliance", "Art of War", "The Scientific Method"],
    "Cursed Energy":       ["Espionage", "Rhetoric & Legacy", "Indomitable Will"],
    "Spiral Power":        ["Kinetic Mastery", "One-Inch Punch", "Indomitable Will"],
    "Soul Resonance":      ["Kinetic Mastery", "Art of War", "Rhetoric & Legacy"],
    "Angelic Override":    ["Rhetoric & Legacy", "Indomitable Will", "Strategic Genius"],

    # GROUNDED — only illegal when the fusion is LEGACY
    "Espionage":             ["Strategic Genius", "Art of War"],
    "Tactical Brilliance":   ["Strategic Genius", "Art of War"],
    "Kinetic Mastery":       ["Indomitable Will", "Art of War"],
    "Electromagnetic Pulse": ["The Scientific Method", "Strategic Genius"],
    "One-Inch Punch":        ["Indomitable Will", "Art of War"],
}

# Used when a power has no entry above — universal, so always legal.
DEFAULT_TRANSPOSITIONS = ["Indomitable Will", "Strategic Genius", "Art of War"]

# Modality rank for comparison
MODALITY_RANK = {"LEGACY": 1, "GROUNDED": 2, "HIGH_CONCEPT": 3}


def ground_power(power_name: str, fusion_rank: int) -> str:
    """Pick a legal stand-in for a power that exceeds the fusion's ceiling.

    Keeps the richest tier still legal for the fusion — Soul Resonance
    becomes Kinetic Mastery for a GROUNDED fusion but has to fall further,
    to Art of War or Rhetoric & Legacy, for a LEGACY one — then chooses at
    random within that tier so grounded fusions don't all look alike.
    """
    candidates = [
        p for p in TRANSPOSITION_MAP.get(power_name, DEFAULT_TRANSPOSITIONS)
        if p in POWER_REGISTRY
        and MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] <= fusion_rank
    ]
    if not candidates:
        return "Indomitable Will"  # universal — legal at every modality

    best = max(MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] for p in candidates)
    return random.choice(
        [p for p in candidates
         if MODALITY_RANK[POWER_REGISTRY[p]["min_modality"]] == best]
    )


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