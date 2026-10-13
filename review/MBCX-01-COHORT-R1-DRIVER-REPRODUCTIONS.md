# Cohort-content design council r1 — driver byte-reproductions (2026-08-16)

Script: `driver-repro-cohort-r1.py` (run read-only from the lane root, `PYTHONPATH=$PWD python -B`,
against working-tree bytes both seats confirmed byte-identical to the pin `b18d7ab58f6a…`).
Every finding acted on in the r2 fold is reproduced here by the driver, per the standing
seat-verdict-is-a-pointer law. Labels honest; partials named.

## P1 — restoration is not expressible by retract-the-correction: REPRODUCED (EXECUTED)

`assert V1 → correct V1→V2 (valid_from T1) → retract V2`: all three APPLIED, reference and
oracle byte-identical. End state: V1 carries a `closure_events` entry from the correction
(`valid_to = T1`) which the retraction does NOT remove; V2 carries a `retraction_events` entry.
At any cut with `valid_time ≥ T1`: V1 closed, V2 retracted — **no visible fact**. The design's
CORRECTION_RESTORATION phrase ("restores the prior visible head") is false at the frozen bytes.
⚠ Harness note (prove-the-harness, recorded): the first run used `valid_from = T0` for the
correction and was refused `FACT_PARENT_NOT_HEAD` by both engines — a wrong-harness red, not a
finding; corrected input reproduced the seats' scenario exactly.

## P2 — ghost FACT row + contradictory observation admitted: REPRODUCED (EXECUTED)

From `packet_fixture_manifest()`: appended a `FACT.NEVER.IN.JOURNAL` world row and set the
world OBSERVATION code to `WORLD_SAYS_FALSE` while the manifest top-level observation says
`TOP_LEVEL_SAYS_TRUE`; recomputed world/read-set/manifest hashes. `validate_expected_manifest`
returned `[]` — admitted. Confirms both seats' C2/F1: FACT and OBSERVATION rows have no
authority law; replay/I15 cannot see them.

## P3 — catalog has no candidate-carried authority: REPRODUCED (EXECUTED)

Over the frozen retained 768: `manifest_for_retained_candidate` yields **one** distinct
`action_catalog_hash` across all 768 (3 stamped rows each); no candidate carries a catalog
field; candidates' `action_ids_by_cut` at the chosen cut hold exactly 1 id. Confirms seat 3's
finding 3: variable multi-action catalogs need a candidate-carried, provenance-bound catalog.

## P4 — 64 KiB envelope: PARTIAL (harness refused at BC selection; remedy adopted on convergent seat evidence)

My hand-built 30-obligation manifest was refused `BC_SELECTION_INVALID` before rendering (the
fixture's BC-selection fields don't extend to a rebuilt world without further construction I
did not perform). NOT a refutation of either seat: seat 2 (EXECUTED) measured fits up to
52 obligations with headroom; seat 3 (EXECUTED) overflowed by 14 bytes at 30 obligations with
4 source-events/row and 128-char IDs. Both are consistent: the bound is input-shape-sensitive.
The r2 remedy — render BC and OM during generation and make envelope fit an ADMISSION
condition — is adopted on that convergent executed evidence; the build's witness will produce
the overflow red under its own harness.

## P5 — pin-subject totality (C7): CONFIRMED at the byte (READ)

`verify-build-bundle.py:408-481 reconcile_pin_manifest` iterates rows FROM the manifest and
byte-checks them; `:321` checks `REQUIRED` files exist on disk. **Nothing equates the manifest
subject set with `REQUIRED`** — a module registered in `BUILD_MODULES`/`BUILD_TEST_MODULES`
but omitted from `$buildSubjects` runs green in-tree and silently vanishes from the pinned
reconstruction. Seat 3's C7-DEFECTIVE stands; seat 2's C7-SOUND was conditional on perfect
registration and does not survive the missed-step route. r2 fold: the bundle asserts
REQUIRED == manifest-subjects set equality (data-accuracy, same class as the discharged #6).

## Driver defect, recorded (not hidden)

The r1 dispatch message and the seat-3 promptfile carried a FABRICATED full SHA
(`b18d7ab196…` = the short design pin welded to the tail of a DIFFERENT commit's full SHA —
the records commit `982ebfd196…`). Violates the standing a-short-sha-expanded-by-hand-is-a-
fabrication law; both surviving seats caught it and correctly resolved via the packet's
committed short pin (real full: `b18d7ab58f6ae45c2e5d309f071db79ead9d4886`). Every future pin
in this lane is emitted from `git rev-parse` output only.

## Round state at this record

Seat 2 (ChatGPT): NO-GO, EXECUTED — banked `MBCX-01-COHORT-SEAT2-CHATGPT-VERDICT-r1.md`.
Seat 3 (codex-exec r1b): NO-GO, EXECUTED — banked stdout log (r1 first attempt died verdictless
after real execution; both logs committed). Seat 1: the account behind the standing Opus seat
ran out of credits mid-round; its in-flight verdict is lost. The replacement seat (new account,
conversation `<id>`, same <council-browser-port> Chrome) reviews the SAME pinned
r1 packet blind to complete the round — 2/3 is not rolled on. Blocked at this writing by a
wedged CDP attach on <council-browser-port> (Dogfood entry 2026-08-16); §1c graceful restart proposed to the owner.
