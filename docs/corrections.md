# Corrections

This file records defects discovered in already-signed corpus text. It does not amend, reopen, or
retroactively alter any signature. A signed row remains exactly what was attested on its signing
date; this file records what was later found wrong about it.

**What this file is not.** It is not a section or appendix of Contract 001, and it is not part of
the gap register (`open_contract_gaps.md`). A gap entry closes when a contract carries a new
invariant; a correction entry records a defect in text that is already signed, and closes nothing.
The two instruments answer different questions and neither substitutes for the other.

**Standing rule.** No entry in this file authorizes editing the text it describes. The corrected
reference lives here, beside the defect, and the signed text stays as attested.

---

## CR-001

```
Target:            Contract 001 §1, :273
Signed:            2026-08-16 (545d846)
Defect:            citation cites the wrong line for its stated source
Correct reference: ruling_001_canonicalization_policy.md:243
Classification:    factual/referential defect — the underlying proposition
                   ("Ruling 001 §5 owns provider choice") is unchanged;
                   only the line number is wrong.
Basis:             The corrected reference does not alter what §1 asserts —
                   only which line supports it.
Evidence:          ruling_001 locked at aa50070, 2026-08-06; unchanged since.
                   At 545d846 (§1's signing commit), ruling_001:243 already
                   read "Scope of this section — operator ruling, 2026-08-06.
                   §5 owns the provider authority boundary"; ruling_001:273
                   read "The core engine must know nothing about Anthropic" —
                   unrelated. Both lines confirmed unchanged in ruling_001
                   today. contract_001 was 263 lines at signing, so :273
                   could never have been a same-document reference either.
                   As of this recording contract_001 is 275 lines, so :273
                   now resolves within contract_001 to the §8 sign-off row —
                   a false same-document hit that did not exist at signing.
Effect:            None on §1's substantive proposition. §1's signed text
                   (:265) is untouched and remains exactly as attested.
Recorded:          2026-08-21
Historical status: §1 remains signed as of 2026-08-16, defect and all.
                   This record does not retroactively alter that signature.
```

**Acknowledgment** — an acknowledgment, not a section signature, and deliberately narrower than
what a Contract 001 row receives.

```
Acknowledged (operator): Kevin Brown
Acknowledged at: 2026-08-21 17:41 EDT
```

Statement: *"I confirm CR-001 correctly identifies a referential defect, not a substantive one —
it changes no proposition §1 asserts, only which line supports it. §1's signature is unaffected."*
