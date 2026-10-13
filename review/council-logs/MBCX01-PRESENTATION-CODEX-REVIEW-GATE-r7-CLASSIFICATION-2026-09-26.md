# MBCX-01 presentation — codex-CLI review gate r7 — CLASSIFICATION (2026-09-26)
Source log: <lane-logs> (367587 B; final codex block at lines 4829-4850)
Reviewed head: f1dc46c (the council r1 fold c3fe2b6 + the verdict bank; START 04:46:38 local, after f1dc46c)
Track: VALIDITY (CC-DEV step 0; labels per step 6: STRUCTURAL / BUILD-MATERIAL / THEATER)

| id | severity | title (verbatim from the log) | file:line | label | fold |
|---|---|---|---|---|---|
| r7-1 | P2 | Fit long headings within the exported figure bounds | <repo>/docs/presentation/make_figures.py:72-74 | BUILD-MATERIAL | folded at 625c553 (the title helper wraps; figure 4's counts moved to the subtitle; figure 2's panel top lowered) |
| r7-2 | P2 | Scope the execution claim to the current witness set | <repo>/docs/presentation/make_figures.py:287-288 | BUILD-MATERIAL | folded at 625c553 (caption, legend and write-up line 62; byte-reproduced: the witness is in the ledger at e89168b, deleted at fd26275, absent from HEAD's tests, present at HEAD only in a ledger note) |
