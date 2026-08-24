# Audit Method — standing pre-sweep checklist

**Status:** CHECKLIST — a working instrument, not a governing document. Nothing here rules anything,
and no entry is a finding about any document's content.

**What this file is.** A list of checks to run **before and during** any citation or anchor sweep of
this corpus. Each item exists because skipping it has already let a wrong anchor or a missed match
through. Read the list before starting a sweep, not after finishing one.

**What this file is not.** It is not a log of what any particular audit found. Findings about corpus
text go to `corrections.md`; things a contract must gain go to `open_contract_gaps.md`; permission to
edit text goes to `authorizations.md`. This file records only *how to look*, never *what was seen*.

**How to append.** A new item earns a slot here when a sweep technique fails in a way that would
recur. Add it as one short checkable line, followed by the evidence that it is not hypothetical.
Keep items imperative and mechanical — something a reader can execute, not a principle they must
interpret. Do not narrate the session that produced it.

**Items are never closed.** Unlike a gap, a method item does not resolve; it stays on the list and
gets run every time.

---

## The checklist

### M1 — Resolve anchors by content, not by range

Extract every `:NNN` reference from the text you are about to commit **programmatically**, re-resolve
each against its target file, and **print the resolved line's content** beside it. A reference that
is merely in range is not verified.

*Evidence:* a draft cited `ruling_002_family_taxonomy_integrity.md:95` for a proposition; that line
is blank and the text is at `ruling_002_family_taxonomy_integrity.md:96`. In range, wrong content,
and a bounds-only check passes it.

### M2 — Match across blockquote and list markers, not just line breaks

`grep -n "some phrase"` misses any phrase a line-wrap splits inside a blockquote, because the
continuation line begins with `> `. When testing whether a term occurs, match across the marker
(`term[\s>]+term`) or search the file as one string.

*Evidence:* *knowledge conditions* occurs twice in `contract_001_domain_resolution.md` — at `:96` and
at `:253`. Line-based grep returns only `:96`, because `:253`'s occurrence reads `knowledge\n>
conditions`. A term-collision finding was nearly missed on that basis.

### M3 — Qualify every cross-document anchor

A bare `:NNN` means `contract_001_domain_resolution.md` by house convention. Inside a paragraph about
any other document, a bare anchor resolves silently to the wrong file. Always write
`filename.md:NNN` when the target is not the contract.

*Evidence:* a draft paragraph about Ruling 002's mechanism amendment carried a bare `:107-108`, which
by convention pointed at the contract rather than the ruling.

### M4 — Re-resolve every anchor after any edit that can shift lines

An edit that adds or removes a line invalidates every anchor below it, in every document that cites
the edited file. After such an edit, re-run M1 across the citing documents — not only the edited one.

*Evidence:* the corpus's standing amendment practice is to verify that every line other than the
edited one is byte-identical, precisely so anchors do not shift (`0c83577`'s commit message).

### M5 — Query the remote ref before reporting a commit as landed

`git log` proves a commit exists locally. It does not prove it is on `origin/main`. Run
`git ls-remote origin main` and compare against `git rev-parse HEAD`.

*Evidence:* an entry was reported as filed while it existed only in the local repository.

### M6 — Enumerate by extraction, never by recall

When a check requires "every X" — every excluded topic, every occurrence of a term, every unticked
box — produce the list mechanically from the file. Do not list from memory of having read it, and do
not trust a summary of the file in place of the file.

*Evidence:* this is the corpus's standing verification discipline; every sweep in the register that
found something found it by extraction.

### M7 — Re-verify your own anchors when your analysis is folded into a record

An anchor you supplied in analysis is inherited by any record that quotes it. The record does not
re-derive it. Check your own citations again at drafting time, at the same standard applied to the
text being audited.

*Evidence:* a wrong anchor supplied in analysis reached a filed entry and had to be recorded as a
defect inside that entry's own Recording note.

---

Opened 2026-08-23.
