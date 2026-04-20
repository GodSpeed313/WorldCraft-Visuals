import random

def generate_world_lore():
    # Character Data with Traits
    legends = {
        "Yasuke": {"trait": "Honorary Samurai", "element": "Steel"},
        "Bruce Lee": {"trait": "Fluid Philosopher", "element": "Water"},
        "Nikola Tesla": {"trait": "Mad Scientist", "element": "Lightning"},
        "James Bond": {"trait": "Suave Operative", "element": "Shadow"},
        "Malcolm X": {"trait": "Revolutionary Firebrand", "element": "Fire"},
        "Tookie Williams": {"trait": "Redeemed Architect", "element": "Earth"}
    }

    anime_pool = {
        "characters": ["The Medicine Seller", "Re-l Mayer", "Kino", "Vash", "Maka"],
        "powers": ["Equivalent Exchange", "Cursed Energy", "Spiral Power"],
        "abilities": ["Domain Expansion", "Titan-Shifting", "Reality Glitch"]
    }

    biomes = ["Sea of Rot", "Floating Sky-Islands", "Submerged Neon City", "Clockwork Labyrinth"]
    style = random.choice(["Anime", "Legend"])

    if style == "Anime":
        char = random.choice(anime_pool["characters"])
        power = random.choice(anime_pool["powers"])
        ability = random.choice(anime_pool["abilities"])
        lore = f"🌀 [ANIME] {char} uses {power} to trigger a {ability}."
    else:
        # Pick two legends and combine their traits
        name1, name2 = random.sample(list(legends.keys()), 2)
        t1, t2 = legends[name1]["trait"], legends[name2]["trait"]
        e1, e2 = legends[name1]["element"], legends[name2]["element"]
        
        char = f"{name1} x {name2}"
        lore = f"📜 [LEGEND] The fusion of {char} ({t1} & {t2}) commands the power of {e1}-{e2}."

    biome = random.choice(biomes)
    return f"In the {biome}, {lore}"

if __name__ == '__main__':
    print("═" * 65)
    print("  🌌 WORLD-CRAFT VISUALS: TRAIT-SYNC ENGINE V2.3 🌌  ")
    print("═" * 65)
    for _ in range(5):
        print(f" ► {generate_world_lore()}")
    print("═" * 65)
