import random

def generate_world_lore():
    # 1. Define the separate "Pools" of characters and archetypes
    anime_pool = {
        "characters": ["The Medicine Seller", "Re-l Mayer", "Kino", "Vash", "Maka"],
        "powers": ["Equivalent Exchange", "Cursed Energy", "Spiral Power"],
        "abilities": ["Domain Expansion", "Titan-Shifting", "Reality Glitch"]
    }
    
    legend_pool = {
        "characters": ["Yasuke", "Bruce Lee", "Nikola Tesla", "James Bond", "Malcolm X", "Tookie Williams"],
        "powers": ["Strategic Genius", "Indomitable Will", "Kinetic Mastery", "The Scientific Method"],
        "abilities": ["One-Inch Punch", "Electromagnetic Pulse", "Art of War", "Espionage"]
    }
    
    biomes = ["Sea of Rot", "Floating Sky-Islands", "Submerged Neon City", "Clockwork Labyrinth"]
    
    # 2. Randomly decide if this generation is 'Anime' or 'Historical Legend'
    style = random.choice(["Anime", "Legend"])
    
    if style == "Anime":
        char = random.choice(anime_pool["characters"])
        power = random.choice(anime_pool["powers"])
        ability = random.choice(anime_pool["abilities"])
        prefix = "🌀 [ANIME]"
    else:
        # Create a "Merge" of two real-life figures
        char1, char2 = random.sample(legend_pool["characters"], 2)
        char = f"{char1} x {char2}"
        power = random.choice(legend_pool["powers"])
        ability = random.choice(legend_pool["abilities"])
        prefix = "📜 [LEGEND]"

    biome = random.choice(biomes)
    return f"{prefix} In the {biome}, the fusion of {char} manifests {ability} through {power}."

if __name__ == '__main__':
    print("═" * 60)
    print("  🌌 WORLD-CRAFT VISUALS: MULTIVERSE ENGINE V2.2 🌌  ")
    print("═" * 60)
    
    for _ in range(5):
        print(f" ► {generate_world_lore()}")
        
    print("═" * 60)
