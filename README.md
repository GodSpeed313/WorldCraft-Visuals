# 🌌 WorldCraft-Visuals

**The Multiverse Logic & Character Synthesis Engine.**

WorldCraft-Visuals fuses characters (anime leads, cinematic icons, historical figures) into **original new characters with discoverable ancestry**. A fusion should stand on its own: you meet a new person first, and recognize where they came from through their abilities, rules and limits, not through a costume swap.

Every fusion card explains itself: what each parent contributed, what was transformed, what was deliberately left out, the one emergent ability that neither parent has alone, its limitations, and a copy-paste image prompt for bringing the character to life in Midjourney or any other image tool.

### ✨ Fusion Synthesis (`fusion_synthesis/`) — the new character cards

Authored synthesis cards, built on the Fusion Engine's C1→C2→C3 slice and authorized by `AUTH-011`. Each card carries:

- **Appearance** in seven slots (build, face, hair, clothing, palette, signature element, ability manifestation), plus a composed description.
- **Visual provenance**: every visual trait is labelled as from parent A, from parent B, transformed, or new.
- **Traits**: inherited, transformed, complementary and not-carried, each with its source.
- **One emergent ability**, with its governing rule, provenance, ancestry and real limitations.
- **Exclusions**: what was deliberately not imported, and why.
- **An image prompt** built only from name-free descriptors. A leak check blocks parent names, ability names and other character-specific proper nouns from the prompt, and the demo refuses to print a prompt that fails it.

```bash
python -m fusion_synthesis.demo                          # every authored card
python -m fusion_synthesis.demo "Maka" "Vash"            # one card
python -m fusion_synthesis.demo "Maka" "Vash" --prompt   # just the image prompt
python -m fusion_synthesis.demo "Maka" "Vash" --json     # the structured card
```

Five pairings are authored today: Maka × Vash, Re-l Mayer × Maka, Kino × Vash, James Bond × Kino, and The Medicine Seller × Re-l Mayer. The fifth was added with data files only, proving that new pairings need no code changes.

**What this is not (yet):** each pair's emergent ability is authored by a person and approved by the operator. The engine does not invent mechanics for arbitrary pairs, makes no runtime model call, and is not yet shown in the dashboard.

### 🧬 Legacy Engine: Mythos-Sync

- **Modality Classifier** (`modality_classifier.py`) — tags every character as `LEGACY` (real historical/cultural figures), `GROUNDED` (cinematic but physically realistic), or `HIGH_CONCEPT` (physics-bending, supernatural), and blends two characters' modalities into a single fusion profile.
- **Logic Auditor** (`logic_auditor.py`) — the enforcer. Checks every power against the fusion's modality ceiling and auto-transposes anything illegal down to a legal equivalent (e.g. `Domain Expansion` → `Strategic Genius` for a `LEGACY` fusion), so nothing breaks its own power-scaling rules.
- **Mythos-Sync Engine** (`mythos_sync.py`) — the full pipeline: classify → select thematic powers by tag → audit → generate lore, biome, rhetorical style, and influence pattern → persist to `containment_matrix.json`.
- **Fantasy Kingdom Generator** (`fantasy_kingdom_generator.py`) — the original, standalone lore generator. Lighter weight than Mythos-Sync; good for a quick taste of the anime/legend flavor text without the full fusion pipeline.
- **Live Dashboard** (`dashboard.html` + `server.py`) — a local web UI. Run `server.py` and it serves `dashboard.html`, which posts fusion requests to `/fuse` and renders the resulting Legacy Profile. Unrecognized names produce a `CAUTIONARY` card instead of a silent guess.

The server is hardened for local use (`AUTH-009`): it listens on `127.0.0.1` only, serves just the dashboard and its matrix file, rejects requests from foreign hosts and origins, and returns clean errors for malformed or oversized requests.

### 🧩 Fusion Engine (`fusion_engine/`)

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

C4 (Dominance) is not yet built. Minimal C5 (card assembly) and C6 (rendering) exist in `fusion_synthesis/` for authored pairings only.

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
  transitions, and invariants. **LOCKED.** Its §6 (the invariants) has since been superseded in full by
  Contract 002; the rest of Contract 001 stands.
- **`contract_002_domain_resolution_invariants.md`** — supersedes Contract 001 §6 in full; carries the
  grounding-terminal halting invariant (I8), which closed GAP-4. **LOCKED** (2026-09-15).
- **`contract_003_gap5_surfaced_payload_preservation.md`** — supersedes Contract 002 §§3–4 in full;
  carries the surfaced-payload-preservation invariant (I9), which closed GAP-5. **LOCKED** (2026-09-20).
- **`ruling_003_fusion_level_result_derivation.md`** — how a fusion's overall result is derived when its
  components resolved at different stages. **LOCKED.**
- **`fusion_engine_requirements_v0.1.md`** — the Fusion Engine's own spec: capabilities and invariants
  (provenance, compatibility, dominance, refusal) for the `fusion_engine/` package above. **LOCKED.**
- **`adr_001_fusion_engine_architecture_reconciliation.md`** — how the Fusion Engine's architecture
  coexists with this codebase without touching it. **ACCEPTED.**
- **`audit_001_…` / `audit_002_…`** — measured evidence the rulings are argued from.
- **`open_contract_gaps.md`** — the register, in two categories: requirements ruled but not yet
  enforceable, and *ownership gaps* — topics a document excludes that no document claims. GAP-4
  (grounding-target fallback authority) and GAP-5 (`SURFACED` payload completeness) are closed, by
  Contract 002 and Contract 003 respectively, as are GAP-8 and GAP-9; GAP-1, GAP-2, GAP-3, GAP-6 and
  GAP-7 remain open.
- **`corrections.md`** — defects found in already-signed text. It records them and closes nothing, and
  authorizes no edit, so the text stays exactly as attested.
- **`authorizations.md`** — bounded, one-time permission to edit specific lines or create specific new
  files, with specific wording and scope (AUTH-001 through AUTH-011, with AUTH-010 reserved and not yet issued), together with the standing rule for
  when an authorization counts as exercised and closed.
- **`amendment_policy.md`** — what may be done to a locked document's text: nothing. A locked document
  is superseded, never amended.
- **`audit_method.md`** — how the corpus is swept for defects, never what a particular sweep found.
- **`disposition_001_…` through `disposition_003_…`** — dated operator determinations that close a narrow
  open question, or preserve authoritative input for a future governing text, without amending any
  locked document.
- **`ratification_001_…` through `ratification_003_…`** — dated archival records of operator acts
  (contract lifecycle acts, the GAP-5 process-opening act) that already had independent force. They add
  nothing to, and subtract nothing from, the acts they record, and authorize no edit.
- **`proposals/`** — non-binding proposals (currently
  `proposal_001_compositional_capability_ontology.md`) that rule nothing, close nothing, and authorize
  no edit.
- **`evidence/`** — preserved exhibits, including Regression Case 001.

Each document carries its own sign-off checklist, which is the authority on what has been signed.
A ruling states what is true; it does **not** assert that the current implementation obeys it — the
gaps register is where those differences are tracked.

### 🚀 Getting Started

No third-party dependencies: everything runs on the Python standard library (3.10+). The one exception is the Hypothesis property suite, kept separate on purpose; install it with `pip install -r requirements-dev.txt`.

**Character cards:**
```bash
python -m fusion_synthesis.demo
```

**Legacy fusion engine (command line):**
```bash
python mythos_sync.py
```

**Web dashboard:**
```bash
python server.py
# then open http://localhost:8000/dashboard.html
```

**Quick lore sample:**
```bash
python fantasy_kingdom_generator.py
```

**Full test suite** (as CI runs it on Python 3.10, 3.11 and 3.12):
```bash
pip install -r requirements-dev.txt
python -m unittest discover -p "test_*.py"
```

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![VS Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## 🚀 Project Status

- **Fusion Synthesis cards:** working for five authored pairings, tested and merged (`AUTH-011`).
- **Fusion Engine C1–C3:** implemented and tested (`AUTH-004`).
- **Mythos-Sync engine and dashboard:** functional, with grounding-terminal halting (`AUTH-005`), CAUTIONARY handling and escaping (`AUTH-006` to `AUTH-008`) and a hardened local server (`AUTH-009`).

**Next up:**
- selectable art styles at prompt time (live-action, painterly, anime, pixel art and more), from one style-neutral character description
- visual states per character: a resting look and an ability-in-action look
- a short backstory field on each card
- escaping in the dashboard's case-file view (`AUTH-010`, reserved), then showing the new cards in the dashboard

The longer-term direction is unchanged: moving from a closed, hand-authored registry toward an engine that can accept concepts it was never authored with, specified in `docs/` before it is implemented.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## About

Repository for [replit.com/@lamontb778/WorldCraft-Visuals](https://replit.com/@lamontb778/WorldCraft-Visuals)
