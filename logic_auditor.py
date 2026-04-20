# =============================================================
#  MYTHOS-SYNC FRAMEWORK — MODULE 2: LOGIC AUDITOR
#  The Enforcer. Validates power assignments against modality
#  rules and transposes illegal combos to legal equivalents.
# =============================================================

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
# TRANSPOSITION TABLE — illegal power → legal human-scale equivalent
# ------------------------------------------------------------------
TRANSPOSITION_MAP = {
    "Domain Expansion":    "Strategic Genius",
    "Titan-Shifting":      "Indomitable Will",
    "Reality Glitch":      "The Scientific Method",
    "Equivalent Exchange": "Art of War",
    "Cursed Energy":       "Rhetoric & Legacy",
    "Spiral Power":        "Indomitable Will",
    "Soul Resonance":      "Kinetic Mastery",
    "Angelic Override":    "Indomitable Will",
}

# Modality rank for comparison
MODALITY_RANK = {"LEGACY": 1, "GROUNDED": 2, "HIGH_CONCEPT": 3}


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
        transposed = TRANSPOSITION_MAP.get(power_name, "Indomitable Will")
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