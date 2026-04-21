# =============================================================
#  MYTHOS-SYNC FRAMEWORK — CORE ENGINE V1.0
#  Connects: Classifier → Auditor → Generator → Data Persistence
#  This is the full intelligent simulation engine.
# =============================================================

import random
import json
import os
from datetime import datetime

# Import our two modules
from modality_classifier import classify_fusion, classify
from logic_auditor import audit_power, POWER_REGISTRY, MODALITY_RANK

# ------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------
MATRIX_FILE = "containment_matrix.json"  # persistent database file

BIOMES = {
    "LEGACY":       ["The Iron Forum", "Dust of Carthage", "The Underground Railroad", "Harlem Renaissance Streets"],
    "GROUNDED":     ["Neon Back-Alleys", "Cold War Safehouse", "Collapsed Industrial Zone", "The Borderlands"],
    "HIGH_CONCEPT": ["Sea of Rot", "Floating Sky-Islands", "Submerged Neon City", "Clockwork Labyrinth"],
}

POWER_POOL = {
    "LEGACY":       ["Strategic Genius", "Indomitable Will", "Rhetoric & Legacy", "Art of War", "The Scientific Method"],
    "GROUNDED":     ["Espionage", "Tactical Brilliance", "Kinetic Mastery", "One-Inch Punch", "Electromagnetic Pulse"],
    "HIGH_CONCEPT": ["Domain Expansion", "Cursed Energy", "Soul Resonance", "Reality Glitch", "Spiral Power", "Angelic Override"],
}

TAG_POWER_MAP = {
    "strategy":        ["Strategic Genius", "Art of War", "Tactical Brilliance"],
    "rhetoric":        ["Rhetoric & Legacy", "Tactical Brilliance"],
    "legacy":          ["Rhetoric & Legacy", "Indomitable Will"],
    "tactical":        ["Tactical Brilliance", "Espionage", "Art of War", "Strategic Genius"],
    "street_legend":   ["Indomitable Will", "Tactical Brilliance", "Espionage"],
    "underworld":      ["Espionage", "Tactical Brilliance", "Indomitable Will"],
    "martial_arts":    ["One-Inch Punch", "Kinetic Mastery"],
    "philosophy":      ["The Scientific Method", "Strategic Genius"],
    "kinetic":         ["Kinetic Mastery", "One-Inch Punch"],
    "inventor":        ["The Scientific Method", "Electromagnetic Pulse"],
    "electromagnetic": ["Electromagnetic Pulse"],
    "visionary":       ["The Scientific Method", "Strategic Genius"],
    "espionage":       ["Espionage", "Tactical Brilliance"],
    "resourceful":     ["Tactical Brilliance", "Espionage"],
    "warrior":         ["Indomitable Will", "Art of War", "Kinetic Mastery"],
    "historical":      ["Strategic Genius", "Indomitable Will"],
    "resilience":      ["Indomitable Will", "Strategic Genius"],
    "redemption":      ["Rhetoric & Legacy", "Indomitable Will"],
    "influence":       ["Rhetoric & Legacy", "Strategic Genius"],
    "pacifist":        ["Indomitable Will", "Rhetoric & Legacy"],
    "gunslinger":      ["Kinetic Mastery", "Tactical Brilliance"],
    "angelic_power":   ["Soul Resonance", "Angelic Override"],
    "soul_resonance":  ["Soul Resonance", "Spiral Power"],
    "meister":         ["Soul Resonance", "Kinetic Mastery"],
    "anti_demon":      ["Cursed Energy", "Soul Resonance"],
    "spiritual":       ["Cursed Energy", "Soul Resonance"],
    "cursed":          ["Cursed Energy", "Reality Glitch"],
    "ancient":         ["Art of War", "Strategic Genius"],
    "cyberpunk":       ["Reality Glitch", "Electromagnetic Pulse"],
    "investigator":    ["Tactical Brilliance", "The Scientific Method"],
    "android_adjacent":["Electromagnetic Pulse", "Reality Glitch"],
    "traveler":        ["Indomitable Will", "Strategic Genius"],
    "observer":        ["The Scientific Method", "Strategic Genius"],
    "survivalist":     ["Indomitable Will", "Tactical Brilliance"],
}

INFLUENCE_PATTERNS = [
    "rewrites the cultural memory of the realm",
    "bends the will of generals through presence alone",
    "leaves no fingerprints but reshapes every outcome",
    "strikes once — the shockwave lasts generations",
    "speaks in paradoxes that become prophecy",
    "moves through systems like water through cracks",
]

RHETORICAL_STYLES = {
    "LEGACY":       ["Socratic dismantling", "Call-and-response", "Iron-fist rhetoric", "Legacy manifesto"],
    "GROUNDED":     ["Tactical misdirection", "Cold precision", "Kinetic storytelling", "Street-level truth"],
    "HIGH_CONCEPT": ["Reality inversion", "Soul-frequency broadcast", "Dimensional proclamation", "Cursed verse"],
}


# ------------------------------------------------------------------
# PERSISTENCE — Load & Save Containment Matrix
# ------------------------------------------------------------------
def load_matrix() -> list:
    if os.path.exists(MATRIX_FILE):
        with open(MATRIX_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_matrix(profile: dict):
    matrix = load_matrix()
    
    # Check if a duplicate already exists
    is_duplicate = any(
        m.get("fusion_name") == profile.get("fusion_name") and 
        m.get("signature_ability") == profile.get("signature_ability") 
        for m in matrix
    )
    
    if not is_duplicate:
        matrix.append(profile)
        with open(MATRIX_FILE, 'w') as f:
            json.dump(matrix, f, indent=2)
        print(f" ✅ [SERVER] Saved new fusion: {profile['fusion_name']}")
    else:
        print(f" ⚠️ [SERVER] Duplicate fusion detected. Skipping save.")


# ------------------------------------------------------------------
# CORE: BUILD A FULL LEGACY PROFILE
# ------------------------------------------------------------------
def build_legacy_profile(
    alpha: str,
    beta: str,
    dominance: int = 50
) -> dict:
    """
    Full pipeline:
    1. Classify the fusion
    2. Pick powers from the correct modality pool
    3. Audit every power (auto-transpose if illegal)
    4. Generate lore, biome, rhetorical style, influence pattern
    5. Package into a rich Legacy Profile dict
    """

    print(f"\n{'═'*60}")
    print(f"  🌌 MYTHOS-SYNC ENGINE — SYNTHESIZING FUSION")
    print(f"  Alpha: {alpha}  |  Beta: {beta}  |  Dominance: {dominance}%")
    print(f"{'═'*60}")

    # --- STEP 1: Classify ---
    fusion = classify_fusion(alpha, beta, dominance)
    modality = fusion["modality"]
    print(f"\n  [CLASSIFIER] Modality resolved → {modality}")
    print(f"  [CLASSIFIER] Dominant         → {fusion['dominant']}")

    # --- STEP 2 & 3: Thematic power selection + audit ---
    # Gather thematic powers from the fused tags first
    thematic_pool = set()
    for tag in fusion["tags"]:
        for power in TAG_POWER_MAP.get(tag, []):
            if power in POWER_REGISTRY:
                required_rank = MODALITY_RANK[POWER_REGISTRY[power]["min_modality"]]
                if MODALITY_RANK[modality] >= required_rank:
                    thematic_pool.add(power)
    
    thematic_pool = list(thematic_pool)
    random.shuffle(thematic_pool)
    
    approved_powers = []
    audit_log = []
    
    # Pull up to 2 thematic powers
    for power in thematic_pool[:2]:
        result = audit_power(power, fusion)
        audit_log.append({
            "power": result["power"],
            "status": "transposed" if result["transposed_to"] else "approved",
            "transposed_to": result["transposed_to"],
            "cost": result["cost_factor"],
            "reason": result["message"] if result["transposed_to"] else None
        })
        approved_powers.append(result["transposed_to"] or result["power"])
    
    # Fill remaining slots from generic pool if needed
    if len(approved_powers) < 2:
        generic_pool = [p for p in POWER_POOL[modality] if p not in approved_powers]
        needed = 2 - len(approved_powers)
        extras = random.sample(generic_pool, min(needed, len(generic_pool)))
        for power in extras:
            result = audit_power(power, fusion)
            audit_log.append({
                "power": result["power"],
                "status": "transposed" if result["transposed_to"] else "approved",
                "transposed_to": result["transposed_to"],
                "cost": result["cost_factor"],
                "reason": result["message"] if result["transposed_to"] else None
            })
            approved_powers.append(result["transposed_to"] or result["power"])
    
    # Always try to add one universal LEGACY power
    universal_candidates = [p for p in POWER_POOL["LEGACY"] if p not in approved_powers]
    if universal_candidates:
        power = random.choice(universal_candidates)
        result = audit_power(power, fusion)
        audit_log.append({
            "power": result["power"],
            "status": "transposed" if result["transposed_to"] else "approved",
            "transposed_to": result["transposed_to"],
            "cost": result["cost_factor"],
            "reason": result["message"] if result["transposed_to"] else None
        })
        approved_powers.append(result["transposed_to"] or result["power"])
    
    approved_powers = list(dict.fromkeys(approved_powers))

    # --- STEP 4: Generate lore components ---
    biome             = random.choice(BIOMES[modality])
    signature_ability = approved_powers[0]
    influence         = random.choice(INFLUENCE_PATTERNS)
    rhetoric          = random.choice(RHETORICAL_STYLES[modality])

    # Character-aware lore (uses traits/elements from registry)
    alpha_data = classify(alpha)
    beta_data  = classify(beta)
    a_trait = alpha_data.get("trait", alpha)
    b_trait = beta_data.get("trait", beta)
    a_elem  = alpha_data.get("element", "Neutral")
    b_elem  = beta_data.get("element", "Neutral")
    
    lore_templates = [
        f"Where {alpha}, the {a_trait} ({a_elem}), collides with {beta}, the {b_trait} ({b_elem}), a new force crystallizes. In {biome}, this fusion wields {signature_ability} to {influence}. Their doctrine: {rhetoric}.",
        f"Born from the tension between the {a_trait} ({a_elem}) and the {b_trait} ({b_elem}), this fusion haunts {biome} with singular intent. They channel {signature_ability} to {influence}, their voice carrying only {rhetoric}.",
    ]
    lore_summary = random.choice(lore_templates)

    # --- STEP 5: Build the full Legacy Profile ---
    profile = {
        "fusion_name":       fusion["fusion_name"],
        "modality":          modality,
        "dominant":          fusion["dominant"],
        "alpha":             {"name": alpha, "modality": classify(alpha)["modality"]},
        "beta":              {"name": beta, "modality": classify(beta)["modality"]},
        "dominance":         dominance,
        "tags":              fusion["tags"],
        "biome":             biome,
        "approved_powers":   approved_powers,
        "signature_ability": signature_ability,
        "influence_pattern": influence,
        "rhetorical_style":  rhetoric,
        "lore_summary":      lore_summary,
        "audit_log":         audit_log,
        "created_at":        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return profile


# ------------------------------------------------------------------
# DISPLAY — Print a Legacy Profile beautifully
# ------------------------------------------------------------------
def display_profile(profile: dict):
    print(f"\n{'═'*60}")
    print(f"  📜 LEGACY PROFILE: {profile['fusion_name']}")
    print(f"{'═'*60}")
    print(f"  Modality         : {profile['modality']}")
    print(f"  Dominant         : {profile['dominant']}")
    print(f"  Biome            : {profile['biome']}")
    print(f"  Approved Powers  : {', '.join(profile['approved_powers'])}")
    print(f"  Signature Ability: {profile['signature_ability']}")
    print(f"  Influence Pattern: {profile['influence_pattern']}")
    print(f"  Rhetorical Style : {profile['rhetorical_style']}")
    print(f"\n  📖 LORE:")
    print(f"  {profile['lore_summary']}")
    print(f"\n  🕓 Created: {profile['created_at']}")
    print(f"{'═'*60}\n")


# ------------------------------------------------------------------
# DISPLAY — Print the full Containment Matrix
# ------------------------------------------------------------------
def display_matrix():
    matrix = load_matrix()
    if not matrix:
        print("\n  [MATRIX] No fusions stored yet.\n")
        return

    print(f"\n{'═'*60}")
    print(f"  🗃️  CONTAINMENT MATRIX  ({len(matrix)} fusions stored)")
    print(f"{'═'*60}")
    for i, entry in enumerate(matrix, 1):
        print(f"\n  [{i}] {entry['fusion_name']}")
        print(f"       Modality  : {entry['modality']}")
        print(f"       Signature : {entry['signature_ability']}")
        print(f"       Biome     : {entry['biome']}")
        print(f"       Created   : {entry['created_at']}")
    print(f"\n{'═'*60}\n")


# ------------------------------------------------------------------
# WEB EXPORT — Adds IDs and engine version for dashboard.html
# ------------------------------------------------------------------
def export_for_web():
    """Exports containment_matrix.json with IDs — the dashboard reads this file."""
    matrix = load_matrix()
    for i, entry in enumerate(matrix):
        if "id" not in entry:
            entry["id"] = f"MSF-{str(i+1).zfill(3)}"
        if "engine_version" not in entry:
            entry["engine_version"] = "v3.0"
    with open("containment_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)
    print(f"\n  🌐 Web export ready → open dashboard.html in your browser")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "═"*60)
    print("   🌌 MYTHOS-SYNC FRAMEWORK — MULTIVERSE ENGINE V3.0 🌌")
    print("═"*60)

    test_fusions = [
        ("Malcolm X",  "Vash",      80),
        ("Bruce Lee",  "Maka",      50),
        ("James Bond", "Nikola Tesla", 40),
    ]

    profiles = []
    for alpha, beta, dominance in test_fusions:
        profile = build_legacy_profile(alpha, beta, dominance)
        display_profile(profile)
        save_to_matrix(profile)
        profiles.append(profile)

    display_matrix()
    export_for_web()