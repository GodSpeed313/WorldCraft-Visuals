# 🌌 WorldCraft-Visuals

**The Multiverse Logic & Character Synthesis Engine.**

WorldCraft-Visuals is a Python framework for fusing characters — historical figures, cinematic icons, anime leads — into a single "Legacy Profile," complete with powers, lore, and a home biome. Instead of picking outcomes at random, it runs every fusion through a modality system so the results stay internally consistent: a fusion of two grounded, real-world figures shouldn't casually wield reality-bending anime powers, and the engine enforces that.

### 🧬 Core Systems

- **Modality Classifier** (`modality_classifier.py`) — tags every character as `LEGACY` (real historical/cultural figures), `GROUNDED` (cinematic but physically realistic), or `HIGH_CONCEPT` (physics-bending, supernatural), and blends two characters' modalities into a single fusion profile.
- **Logic Auditor** (`logic_auditor.py`) — the enforcer. Checks every power against the fusion's modality ceiling and auto-transposes anything illegal down to a legal equivalent (e.g. `Domain Expansion` → `Strategic Genius` for a `LEGACY` fusion), so nothing breaks its own power-scaling rules.
- **Mythos-Sync Engine** (`mythos_sync.py`) — the full pipeline: classify → select thematic powers by tag → audit → generate lore, biome, rhetorical style, and influence pattern → persist to `containment_matrix.json`.
- **Fantasy Kingdom Generator** (`fantasy_kingdom_generator.py`) — the original, standalone lore generator. Lighter weight than Mythos-Sync; good for a quick taste of the anime/legend flavor text without the full fusion pipeline.
- **Live Dashboard** (`dashboard.html` + `server.py`) — a local web UI. Run `server.py` and it serves `dashboard.html`, which posts fusion requests to `/fuse` and renders the resulting Legacy Profile.

### 🚀 Getting Started

No third-party dependencies — everything runs on the Python standard library (3.10+).

**Quick lore sample:**
```bash
python fantasy_kingdom_generator.py
```

**Full fusion engine (command line):**
```bash
python mythos_sync.py
```

**Web dashboard:**
```bash
python server.py
# then open http://localhost:8000/dashboard.html
```

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![VS Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## 🚀 Project Status

The Mythos-Sync engine (classifier, auditor, tag-driven power selection, live dashboard) is functional end to end. Ongoing areas of interest: expanding the character registry (see the open "Legend Pool" issue for community suggestions) and further balancing the power-scaling rules between modalities.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## About

Repository for [replit.com/@lamontb778/WorldCraft-Visuals](https://replit.com/@lamontb778/WorldCraft-Visuals)
