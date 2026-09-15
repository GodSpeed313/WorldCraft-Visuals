# 🌌 WorldCraft-Visuals

**The Multiverse Logic & Character Synthesis Engine.**

WorldCraft-Visuals is a Python framework for fusing characters — historical figures, cinematic icons, anime leads — into a single "Legacy Profile," complete with powers, lore, and a home biome. Instead of picking outcomes at random, it runs every fusion through a modality system so the results stay internally consistent: a fusion of two grounded, real-world figures shouldn't casually wield reality-bending anime powers, and the engine enforces that.

### 🧬 Core Systems

- **Modality Classifier** (`modality_classifier.py`) — tags every character as `LEGACY` (real historical/cultural figures), `GROUNDED` (cinematic but physically realistic), or `HIGH_CONCEPT` (physics-bending, supernatural), and blends two characters' modalities into a single fusion profile.
- **Logic Auditor** (`logic_auditor.py`) — the enforcer. Checks every power against the fusion's modality ceiling and auto-transposes anything illegal down to a legal equivalent (e.g. `Domain Expansion` → `Strategic Genius` for a `LEGACY` fusion), so nothing breaks its own power-scaling rules.
- **Mythos-Sync Engine** (`mythos_sync.py`) — the full pipeline: classify → select thematic powers by tag → audit → generate lore, biome, rhetorical style, and influence pattern → persist to `containment_matrix.json`.
- **Fantasy Kingdom Generator** (`fantasy_kingdom_generator.py`) — the original, standalone lore generator. Lighter weight than Mythos-Sync; good for a quick taste of the anime/legend flavor text without the full fusion pipeline.
- **Live Dashboard** (`dashboard.html` + `server.py`) — a local web UI. Run `server.py` and it serves `dashboard.html`, which posts fusion requests to `/fuse` and renders the resulting Legacy Profile.

### 🧩 Fusion Engine (`fusion_engine/`) — new, separate, in progress

A second, additive reasoning layer, specified independently in `docs/fusion_engine_requirements_v0.1.md`
(**LOCKED**) and reconciled against this codebase in `docs/adr_001_fusion_engine_architecture_reconciliation.md`.
It does not replace or import the Mythos-Sync engine above — the two are architecturally isolated on
purpose, enforced by a standing regression test (`fusion_engine/tests/test_boundary.py`).

Currently implements the minimum C1→C2→C3 vertical slice, authorized by `AUTH-004`
(`docs/authorizations.md`):

- **C1 — Contribution/Placement Classifier** (`c1_classifier.py`) — admits and validates
  hand-authored source properties.
- **C2 — Provenance Ledger** (`c2_ledger.py`) — the single authoritative source of mechanic-derivation
  provenance (`Source-Derived > Defensibly Derived > Invented Bridge > Unresolved`), with weakest-link
  and multi-hop propagation.
- **C3 — Contradiction/Compatibility Evaluator** (`c3_compatibility.py`) — returns Compatible,
  Conditionally Compatible, Incompatible, or Unresolved for a proposed interaction, refusal included as
  a legitimate result rather than an error.

C4 (Dominance), C5 (Structured Reasoning Record), and C6 (Presentation) are not yet built.

```bash
python -m fusion_engine.demo             # structured, non-prose demonstration
python -m unittest discover -s fusion_engine/tests -p "test_*.py"   # 51 tests
```

### ⚖️ Governance (`docs/`)

The engine's behavior is governed by written rulings, not only by code. These are binding documents,
and they are the place to look before changing how concepts are named, classified, or grounded.

- **`ruling_001_canonicalization_policy.md`** — concept identity: when two names are the same concept,
  when they may be merged, and what a learned vocabulary is permitted to propose. **LOCKED.**
- **`ruling_002_family_taxonomy_integrity.md`** — what `family` is (a grounding behavior class, not an
  ontology), the domain layer, and what happens when a concept cannot be placed. **LOCKED.**
- **`contract_001_domain_resolution.md`** — the machine-enforceable form: domain resolution states,
  transitions, and invariants. **LOCKED.**
- **`fusion_engine_requirements_v0.1.md`** — the Fusion Engine's own spec: capabilities and invariants
  (provenance, compatibility, dominance, refusal) for the `fusion_engine/` package above. **LOCKED.**
- **`adr_001_fusion_engine_architecture_reconciliation.md`** — how the Fusion Engine's architecture
  coexists with this codebase without touching it. **ACCEPTED.**
- **`audit_001_…` / `audit_002_…`** — measured evidence the rulings are argued from.
- **`open_contract_gaps.md`** — the register, in two categories: requirements ruled but not yet
  enforceable, and *ownership gaps* — topics a document excludes that no document claims. GAP-4
  (grounding-target fallback authority) is open; its substantive terminal policy is recorded in
  `disposition_002_gap4_grounding_terminal_policy.md`, pending a successor contract to formally carry it.
- **`corrections.md`** — defects found in already-signed text. It records them and closes nothing, and
  authorizes no edit, so the text stays exactly as attested.
- **`authorizations.md`** — bounded, one-time permission to edit specific lines or create specific new
  files, with specific wording and scope.
- **`amendment_policy.md`** — what may be done to a locked document's text: nothing. A locked document
  is superseded, never amended.
- **`audit_method.md`** — how the corpus is swept for defects, never what a particular sweep found.
- **`disposition_001_…` / `disposition_002_…`** — dated operator determinations that close a narrow
  open question, or preserve authoritative input for a future governing text, without amending any
  locked document.
- **`evidence/`** — preserved exhibits, including Regression Case 001.

Each document carries its own sign-off checklist, which is the authority on what has been signed.
A ruling states what is true; it does **not** assert that the current implementation obeys it — the
gaps register is where those differences are tracked.

### 🚀 Getting Started

The engine has no third-party dependencies — it runs on the Python standard library (3.10+), and
`python -m unittest test_engine` needs no install step. The one exception is the Hypothesis property
suite, which is deliberately kept separate so that stays true: `pip install -r requirements-dev.txt`,
then `python -m unittest test_hypothesis_properties`.

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

The Mythos-Sync engine (classifier, auditor, tag-driven power selection, live dashboard) is functional end to end.

The Fusion Engine (`fusion_engine/`) is new: its v0.1 requirements are locked and reconciled against
this codebase, and the minimum C1→C2→C3 slice (contribution classification, provenance, compatibility)
is implemented, tested (51 tests), and merged. C4 (dominance), C5 (the full structured reasoning
record), and C6 (creative presentation) are not yet built.

Separately, the engine is being taken from a closed-world model — a hand-authored registry that is correct for the vocabulary it contains — toward one that can accept concepts it was never authored with. That transition is being specified in `docs/` before it is implemented, which is why much of the recent history is rulings rather than code.

Earlier plans listed here (growing the character registry, rebalancing power-scaling between modalities) are superseded by that work rather than abandoned.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## About

Repository for [replit.com/@lamontb778/WorldCraft-Visuals](https://replit.com/@lamontb778/WorldCraft-Visuals)
