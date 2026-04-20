# =============================================================
#  MYTHOS-SYNC FRAMEWORK — MODULE 1: MODALITY CLASSIFIER
#  Tags every character with their operational "mode" so the
#  engine knows what rules apply to them.
# =============================================================

# The Master Registry — defines every known character's modality
CHARACTER_REGISTRY = {
    # --- LEGACY: Real historical/cultural figures (human limits only) ---
    "Yasuke":          {"modality": "LEGACY",       "tags": ["warrior", "historical", "resilience"]},
    "Bruce Lee":       {"modality": "LEGACY",       "tags": ["martial_arts", "philosophy", "kinetic"]},
    "Nikola Tesla":    {"modality": "LEGACY",       "tags": ["inventor", "electromagnetic", "visionary"]},
    "Malcolm X":       {"modality": "LEGACY",       "tags": ["rhetoric", "strategy", "legacy"]},
    "Tookie Williams": {"modality": "LEGACY",       "tags": ["street_legend", "redemption", "influence"]},

    # --- GROUNDED: Cinematic/fictional but physically realistic ---
    "James Bond":      {"modality": "GROUNDED",     "tags": ["espionage", "tactical", "resourceful"]},
    "Kino":            {"modality": "GROUNDED",     "tags": ["traveler", "observer", "survivalist"]},

    # --- HIGH_CONCEPT: Physics-bending, supernatural powers ---
    "The Medicine Seller": {"modality": "HIGH_CONCEPT", "tags": ["spiritual", "cursed", "ancient"]},
    "Re-l Mayer":      {"modality": "HIGH_CONCEPT", "tags": ["cyberpunk", "investigator", "android_adjacent"]},
    "Vash":            {"modality": "HIGH_CONCEPT", "tags": ["pacifist", "gunslinger", "angelic_power"]},
    "Maka":            {"modality": "HIGH_CONCEPT", "tags": ["soul_resonance", "meister", "anti_demon"]},
}

def classify(character_name: str) -> dict:
    """
    Returns the modality profile for a character.
    If unknown, defaults to GROUNDED so the Auditor stays conservative.
    """
    profile = CHARACTER_REGISTRY.get(character_name)
    if profile:
        return {"name": character_name, **profile}
    else:
        print(f"  [CLASSIFIER] ⚠️  '{character_name}' not in registry. Defaulting to GROUNDED.")
        return {"name": character_name, "modality": "GROUNDED", "tags": ["unknown"]}


def classify_fusion(alpha_name: str, beta_name: str, dominance: int = 50) -> dict:
    """
    Classifies a FUSION of two characters.
    dominance = 0–100, where 100 means Alpha fully dominates.
    Returns a blended modality profile.
    """
    alpha = classify(alpha_name)
    beta  = classify(beta_name)

    # Modality priority ranking (higher = more "powerful" classification)
    rank = {"LEGACY": 1, "GROUNDED": 2, "HIGH_CONCEPT": 3}

    alpha_rank = rank[alpha["modality"]]
    beta_rank  = rank[beta["modality"]]

    # The dominant character's modality wins IF dominance > 70
    if dominance >= 70:
        final_modality = alpha["modality"]
        dominant_label = f"{alpha_name} (dominant)"
    elif dominance <= 30:
        final_modality = beta["modality"]
        dominant_label = f"{beta_name} (dominant)"
    else:
        # Balanced blend — take the HIGHER modality rank
        if alpha_rank >= beta_rank:
            final_modality = alpha["modality"]
        else:
            final_modality = beta["modality"]
        dominant_label = "balanced blend"

    blended_tags = list(set(alpha["tags"] + beta["tags"]))

    return {
        "fusion_name": f"{alpha_name} x {beta_name}",
        "modality":    final_modality,
        "dominant":    dominant_label,
        "tags":        blended_tags,
    }


# --- Quick test when run directly ---
if __name__ == "__main__":
    print("\n🔬 CLASSIFIER TEST\n" + "─" * 40)
    print(classify("Bruce Lee"))
    print(classify("Vash"))
    print(classify("Unknown Hero"))
    print("\n🔬 FUSION TEST (dominance=80 → Alpha wins)\n" + "─" * 40)
    print(classify_fusion("Malcolm X", "Vash", dominance=80))
    print("\n🔬 FUSION TEST (dominance=50 → balanced)\n" + "─" * 40)
    print(classify_fusion("Bruce Lee", "Maka", dominance=50))