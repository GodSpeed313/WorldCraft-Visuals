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
from console import use_utf8_output
from modality_classifier import classify_fusion, classify
from logic_auditor import audit_power, family_of, POWER_REGISTRY

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
    "LEGACY": [
        # COGNITION
        "Strategic Genius", "The Scientific Method", "Art of War",
        "Pattern Recognition", "Mastermind Architecture", "Tactical Brilliance",
        # INFLUENCE
        "Rhetoric & Legacy", "Cultural Resonance", "Diplomatic Mastery",
        "Symbolic Authority",
        # DISCIPLINE
        "Indomitable Will", "Martial Perfection", "Adaptive Combat",
        "Iron Discipline",
        # PERCEPTION
        "Intuitive Insight", "Situational Awareness", "Psychological Mastery",
        "Memory Palace",
    ],
    "GROUNDED":     ["Espionage", "Kinetic Mastery", "One-Inch Punch", "Electromagnetic Pulse"],
    "HIGH_CONCEPT": ["Domain Expansion", "Cursed Energy", "Soul Resonance", "Reality Glitch", "Spiral Power", "Angelic Override"],
}

# Every power must be reachable from a tag, or it can only ever arrive through
# the single random universal slot — which produces more combinations that mean
# less. New powers were routed to the tags that already imply them.
TAG_POWER_MAP = {
    "strategy":        ["Strategic Genius", "Art of War", "Tactical Brilliance", "Mastermind Architecture", "Pattern Recognition"],
    "rhetoric":        ["Rhetoric & Legacy", "Symbolic Authority", "Cultural Resonance", "Psychological Mastery"],
    "legacy":          ["Rhetoric & Legacy", "Symbolic Authority", "Cultural Resonance", "Indomitable Will"],
    "tactical":        ["Tactical Brilliance", "Espionage", "Art of War", "Situational Awareness"],
    "street_legend":   ["Cultural Resonance", "Psychological Mastery", "Indomitable Will", "Symbolic Authority"],
    "underworld":      ["Espionage", "Psychological Mastery", "Situational Awareness", "Tactical Brilliance"],
    "martial_arts":    ["One-Inch Punch", "Kinetic Mastery", "Martial Perfection", "Adaptive Combat"],
    "philosophy":      ["The Scientific Method", "Intuitive Insight", "Iron Discipline", "Equivalent Exchange"],
    "kinetic":         ["Kinetic Mastery", "One-Inch Punch", "Martial Perfection"],
    "inventor":        ["The Scientific Method", "Electromagnetic Pulse", "Mastermind Architecture", "Pattern Recognition", "Equivalent Exchange"],
    "electromagnetic": ["Electromagnetic Pulse", "Pattern Recognition"],
    "visionary":       ["The Scientific Method", "Pattern Recognition", "Mastermind Architecture"],
    "espionage":       ["Espionage", "Situational Awareness", "Psychological Mastery"],
    "resourceful":     ["Adaptive Combat", "Situational Awareness", "Tactical Brilliance"],
    "warrior":         ["Martial Perfection", "Iron Discipline", "Art of War", "Kinetic Mastery", "Titan-Shifting"],
    "historical":      ["Memory Palace", "Symbolic Authority", "Strategic Genius"],
    "resilience":      ["Iron Discipline", "Indomitable Will"],
    "redemption":      ["Symbolic Authority", "Cultural Resonance", "Indomitable Will"],
    "influence":       ["Cultural Resonance", "Diplomatic Mastery", "Rhetoric & Legacy"],
    "pacifist":        ["Diplomatic Mastery", "Iron Discipline", "Indomitable Will"],
    "gunslinger":      ["Adaptive Combat", "Situational Awareness", "Kinetic Mastery"],
    "angelic_power":   ["Soul Resonance", "Angelic Override", "Symbolic Authority"],
    "soul_resonance":  ["Soul Resonance", "Spiral Power", "Intuitive Insight"],
    "meister":         ["Soul Resonance", "Adaptive Combat", "Kinetic Mastery"],
    "anti_demon":      ["Cursed Energy", "Soul Resonance", "Iron Discipline", "Titan-Shifting"],
    "spiritual":       ["Cursed Energy", "Soul Resonance", "Intuitive Insight", "Domain Expansion"],
    "cursed":          ["Cursed Energy", "Reality Glitch", "Domain Expansion"],
    "ancient":         ["Art of War", "Memory Palace", "Symbolic Authority"],
    "cyberpunk":       ["Reality Glitch", "Electromagnetic Pulse", "Pattern Recognition"],
    "investigator":    ["Pattern Recognition", "Situational Awareness", "Psychological Mastery"],
    "android_adjacent":["Electromagnetic Pulse", "Reality Glitch", "Memory Palace"],
    "traveler":        ["Situational Awareness", "Memory Palace", "Adaptive Combat"],
    "observer":        ["Intuitive Insight", "Situational Awareness", "Pattern Recognition"],
    "survivalist":     ["Adaptive Combat", "Situational Awareness", "Iron Discipline"],
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
    # Gather thematic powers from the fused tags. Powers that exceed this
    # fusion's modality ceiling are deliberately NOT filtered out here — they
    # go to the auditor, which grounds them into legal equivalents. Filtering
    # would silently discard a character's theme; transposing translates it.
    thematic_pool = set()
    for tag in fusion["tags"]:
        for power in TAG_POWER_MAP.get(tag, []):
            if power in POWER_REGISTRY:
                thematic_pool.add(power)

    thematic_pool = list(thematic_pool)
    random.shuffle(thematic_pool)

    approved_powers = []
    audit_log = []

    def audit_and_take(power: str):
        """Audit one power, log the verdict, and hold the result if it's new.

        Transposition can map several illegal powers onto the same legal one,
        so a power that gets audited is not necessarily a power that is gained.
        """
        result = audit_power(power, fusion)
        # Carry the auditor's three-state verdict. Deriving status from
        # transposed_to instead collapsed UNVERIFIED into "approved", because
        # transposed_to is None for both — an unregistered power was logged and
        # rendered as if the registry had cleared it.
        audit_log.append({
            "power": result["power"],
            "status": result["state"].lower(),
            "transposed_to": result["transposed_to"],
            "cost": result["cost_factor"],
            "reason": result["message"] if result["state"] != "APPROVED" else None
        })
        final = result["transposed_to"] or result["power"]
        if final not in approved_powers:
            approved_powers.append(final)

    # Pull thematic powers until we hold 2 distinct ones
    for power in thematic_pool:
        if len(approved_powers) >= 2:
            break
        audit_and_take(power)

    # Fill remaining slots from generic pool if the tags came up short
    if len(approved_powers) < 2:
        generic_pool = [p for p in POWER_POOL[modality] if p not in approved_powers]
        random.shuffle(generic_pool)
        for power in generic_pool:
            if len(approved_powers) >= 2:
                break
            audit_and_take(power)

    # Always try to add one universal LEGACY power
    universal_candidates = [p for p in POWER_POOL["LEGACY"] if p not in approved_powers]
    if universal_candidates:
        audit_and_take(random.choice(universal_candidates))

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
    # Which kinds of excellence this fusion actually embodies. The dominant
    # family is the closest thing the engine currently has to a disposition,
    # and is what a philosophy/tension layer would read from.
    families = [family_of(p) for p in approved_powers]
    dominant_family = max(set(families), key=families.count)

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
        "power_families":    {p: family_of(p) for p in approved_powers},
        "dominant_family":   dominant_family,
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
    print(f"  Dominant Family  : {profile['dominant_family']}")
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
    use_utf8_output()
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