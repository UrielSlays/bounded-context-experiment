# MBCX-01 — RE-ENTRY, session close 2026-08-15 (second session of the day)

For a session that arrives cold. **Supersedes `MBCX-01-RE-ENTRY-2026-08-15.md` for STATE**; that
file's requirement block and traps still bind and are not repeated in full here, and
`MBCX-01-RE-ENTRY-2026-08-14.md`'s traps still bind beneath both. Byte-check anything you act on.

## ⛔⛔ REQUIRED FIRST (unchanged, owner-ordered): READ THE FULL DoR SET

Design r9 · R10 ARCHITECTURE SPEC · R10 PRIOR-ART MEMO · R13 CLOSURE ARCHITECTURE · the
INVARIANT MATRIX · AMENDMENT-1 · AMENDMENT-2 — in full, grepping does not count. And the lane
still has **NO adversary**: the only yardstick is *does a change stop the experiment producing a
wrong number, admitting wrong evidence, or refusing right evidence*. When a class recurs, the
honest level-up is usually DELETING a wrong restriction, not adding machinery — it was, again,
this session (the bundle arm's false authentication claim died by subtraction).

## Where the lane is

Branch `codex/mbcx01-production-build`. ⛔ RESOLVE HEAD (`git rev-parse --short HEAD` vs origin);
equal at close. Remote `<private-repo>`, private, verified.

**Gates at close:** BUILD **170/170** · frozen **150/150** (untouched all session) · repair
ledger **65 invariants / 170 witnesses**, two-way total · `verify-build-bundle.py` REAL exit 0
(now including the pin-manifest reconciliation arm) · `verify-build-pinned.ps1` prints
`PINNED RECONSTRUCTION COMPLETE` (and the reconstruction is now BYTE-reconciled against the
manifest, not waved through) · readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
**Zero spend, zero provider calls, no ceremony, no experiment, no frozen file touched.**

## What this session did

**1. The engine gap was diagnosed and filed.** Everything built before today is the instrument's
VERIFICATION half; the PRODUCING half — scenario content generator (six real motifs, multi-action
universes, H-scaled histories; the selection pipeline already exists and is ADOPTED), carriers
FD/FC/TN, grid runner, route client — is ZERO lines. **Issues #17–#22** are those slices, with
byte-verified corrections on #17 (read its comments before designing). #23 is the DoR
reconciliation sweep (owner ratifies amendments; A-1/A-2 pattern).

**2. The codex-CLI gate ran for the first time (issue #1): THREE rounds, 25 defects closed
red-first, plus 2 driver-accepted riders.** Full logs committed:
`MBCX-01-CODEXCLI-r{1,2,3}-FULL-LOG-2026-08-15.log`. Every red was re-run by the driver against
hash-proven pre-fix bytes; every fold has ledger rows. Highlights a fresh session must know:

- **The live measurement path was full of refuse-right-evidence defects** — retired instructions
  signed as ZERO into an admission gate requiring nonzero; a root identity (boot-tagged
  ProcessStartKey) that appears in NO ETW payload ever emitted; the telemetry query rejected
  outright by ntdll (48-byte buffer, needs OS sizing — real-ntdll witnessed); an elapsed-time
  cross-check no live run could pass; machine-wide provider events aborting on any busy host.
  All closed. **The smoke run is far safer than it was this morning.**
- **Kernel-Process payload layouts are now decoded per the provider's own versioned manifest,
  verified via TDH** (`wevtutil` emits empty templates; the TDH dump is in the r3 fold's
  evidence). Unknown/old versions fault by name.
- **⚠⚠ TWO SIGNED-FIELD SEMANTIC CHANGES were introduced, flagged, and NOT council-blessed yet:**
  (a) `counter_value` is now a member-attributed accumulator (raw counter minus foreign work per
  processor) — the only reading under which the signed attribution string is true;
  (b) `root_process_start_key` now carries the ETW-published ProcessSequenceNumber.
  Both correct in the driver's judgment; **neither is the driver's to bless alone.**
- **Deliberately NOT built** (each recorded): an interprocess single-producer door for the state
  store (SQLite's own writer serialization + in-transaction seq allocation + unique index closed
  the named harm; "exactly one producer process" is a design decision) · a second value in the
  root-identity receipt · version gates on thread events (both published versions verified
  identical for the fields read).

**3. Process facts a fresh session should inherit:** the finding count ROSE across rounds
(5→7→10) — that is codex re-deriving classes on ground the council never ruled, and it is why the
next gate is the COUNCIL, not codex r4. The gates also policed the driver three times: the
clean-room refused a fix built on a wrong premise about its own layout; the ledger gate refused a
dangling covered-by pointer; and the driver's own probe-harness lied twice (POSIX-style PYTHONPATH
silently swallowing output; a probe needing argv read as "empty output") — **empty output is a
broken harness until proven otherwise, never a pass.**

## Do this next, in this order

1. **COUNCIL ROUND on current bytes — issue #24.** First complete review of the folded tree
   (r4/r5 reviewed older bytes; three fold commits + two amendments landed since). FIRST AGENDA:
   the two signed-field semantic changes above; then the writer-door question, the six A-2
   judgment calls (#8), the fixture-key gaps (#14), the smoke-criterion conjunction, the dropped
   live-path provenance (no receipt slot for exclusion counts). Neutral CS register, validity
   framing, `packet:check` green, ROUND LEDGER, no threat declaration (no adversary exists —
   grep-verify per the -15 re-entry's command).
2. **codex-CLI r4 to literal GREEN** — after the seats, serialized, sol at xhigh. The last local
   gate.
3. **Draft PR into Selene + `@codex review`** (owner-authorized; destination has no workflows).
4. **Relocation — issue #26:** clone Selene → `<repo>`, recreate the build
   worktree, run the pinned clean-room THERE (proves path-independence), then retire the
   Downloads copies. Owner-approved 2026-08-15. Both ps1 helpers now survive paths with spaces.
5. **The elevated smoke run (#2)** — owner action; #3's fix is built and witnessed but only the
   run proves it. Pass criterion is now a CONJUNCTION: envelope independently valid AND the
   honest sentinel red; a failed criterion exits nonzero.

## New traps (the old ones all still bind)

- ⛔ **Empty output from a probe/grep is a BROKEN HARNESS signal, not a pass.** Two of the
  driver's own verification wrappers failed silently this session (Git-Bash POSIX path in
  PYTHONPATH; missing argv). Run the probe raw and read the traceback before concluding anything.
- ⚠ **The repair ledger's `positive_covered_by` must point at a row that itself CARRIES a
  positive** — the bundle gate enforces it (it caught the driver).
- ⚠ **The bundle verifier now REFUSES a no-manifest-no-git directory by name**
  (`PIN_MANIFEST_ABSENT_OUTSIDE_A_GIT_WORK_TREE`) and BYTE-reconciles a reconstruction that
  carries the manifest. `verify-build-pinned.ps1` exports the manifest into the reconstruction —
  that is the expected layout, not an anomaly.
- ⚠ **A `codex review` base must be a branch-ish ref** (`--base codex/mbcx01-design-council`,
  whose merge-base with the build branch is exactly the r13.2 council base), and the model rides
  `-c model="gpt-5.6-sol"`, never `-m`.
- ⚠ **Worker folds in one worktree in parallel work, with discipline:** disjoint src files,
  probes load pre-fix bytes from `git show HEAD:` (never the tree), targeted tests only, the
  driver runs global gates once at assembly, witness numbers collide (bw63/bw65 forced renumber
  twice) — have workers declare reserved ranges.

## ANTI-DRIFT §1 audit of this session

**FIRED — claim outran its witness (×1, caught same day):** issue #17's "nothing manufactures the
scenario population" was overstated — `synthetic_candidates_r13()` + the full selection pipeline
exist; the real gap is scientific CONTENT. Corrected on the issue at the byte.
**FIRED — broken harness read as verdict (×2, both mine, both caught before reporting):** the
POSIX-PYTHONPATH and missing-argv probe failures above.
**FIRED — wrong gate order:** codex before council; caught by the rising-count symptom, corrected
in the next-order above.
**FIRED — self-inflicted machinery (×1, caught by the next gate):** the r2 reconstruction-arm
refused the clean-room's own layout and carried a false `authenticated_by` claim; both died in
r3, one by byte-reconciliation, one by subtraction.
**HANDLED CORRECTLY:** every worker result driver-reproduced against hash-proven pre-fix bytes
before any commit · riders got their own reds · both semantic changes flagged for council, never
silent · the no-adversary line held — nothing built this session is a wall, a census, or a
scanner; 23 of 25 defects were fixes that make the instrument ACCEPT more true evidence or stop
lying to itself.

## Claim ceiling — moved, honestly

The verification half is exercised, clean-room reproducible, and now reconciles its own pin
manifest. The measurement half has STILL never executed against a live ETW session — but its
known constants are now manifest-verified where the platform publishes anything (TDH, installed
SDK headers), its live-path logic has survived three execution-armed review rounds, and every
remaining platform unknown faults loudly by name. The smoke run remains the only thing that can
settle the rest — and four of its would-have-been failure modes were closed today.
