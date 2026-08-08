# Evidence

Artifacts preserved because a governing document depends on them. Files here are **exhibits, not
runtime state** — nothing in the engine reads or writes this directory.

## `regression_case_001.json`

**The exhibit Ruling 001 §6 relies on**, and the case Ruling 002 §9 is built on.

Ruling 001 §6 is titled *"Normalization Regression Case 001 — preserved permanently"* and refers to
the artifact by its runtime filename, `containment_matrix.json`. **That file is gitignored**
(`.gitignore:3`), and for a good reason: `export_for_web()` in `mythos_sync.py` rewrites it on every
fusion run, so tracking it would make the working tree dirty on ordinary use of the app.

The consequence was that the evidence a **locked** ruling was signed against existed only on one
machine, in a file the engine overwrites. This copy closes that.

| | |
|---|---|
| Copied from | `containment_matrix.json` |
| Copied on | 2026-08-08 |
| Artifact created | 2026-08-03 21:15:01 (`created_at` in the record) |
| `sha256` | `3fa4d990c7877b63a5796bf33c43c28a0dc0c66f7c1df91d0279ffcb50fb86ac` |
| Size | 1781 bytes |
| Verified | byte-identical to the source at copy time |

**Read the runtime filename in Ruling 001 §6 as pointing here.** Ruling 001 is locked and was not
reopened to repoint it; this note carries the mapping instead.

### Why this artifact matters

It is `MSF-001`, Hashirama Senju × William Vangeance — both inputs unrecognized, both silently
defaulted to `GROUNDED` with `tags: ["unknown"]`, and a full profile emitted anyway. Its own
`lore_summary` names `Unknown Entity (Neutral)` **twice** and proceeds. It wrote the ignorance down
and continued.

Ruling 002 §9 records the two distinct defects it demonstrates and requires that they stay separate:
a **normalization bug** (unknown input silently became `GROUNDED`) and an **ontology boundary**
failure (the registry has no honest place for non-human-excellence abilities). Fixing the first does
not fix the second.

**This file must not be regenerated.** Its value is that it is the original output of the engine at
`v3.0`, before any of the governance work. A re-run would produce a different record — the same
inputs yield different power-sets on different runs, which is itself part of what the case
demonstrates.
