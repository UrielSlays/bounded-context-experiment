# MBCX-01 — RE-ENTRY, session close 2026-08-16c (the ACCEPTANCE + CODEX-GATE session)

**Supersedes `MBCX-01-RE-ENTRY-2026-08-16b.md` for STATE.** Its traps, the ENGINE-FIRST
ruling, and the no-adversary standing order still bind and are not repeated. Byte-check
anything you act on; resolve HEAD (`git rev-parse` vs origin) — never trust a SHA in prose.

## What this session did (verified statements)

1. **The cohort-BUILD acceptance council arc ran and CLOSED.** r1 (packet `@8432132`,
   content pin `f35851e`): 3/3 EXECUTED → **NO-GO** (GWF/NO-GO/NO-GO). Every finding
   driver-reproduced at the byte before synthesis (`driver_repro_cohortbuild_r1.py`,
   R1–R6 all confirmed; one driver harness fault caught and recorded). Five fold classes
   landed red-first: serve-boundary semantic re-derivation (seat 2's class — the
   derivation law moved to the packet sibling), per-scenario gold identity (768 distinct
   golds, floor-gated), the motif-codebook cross-tab (measured + DECLARED at 3, one
   reshaping attempt honestly discarded), plan-record totality, coverage numerator
   (150→151 with the rule declared), W14(b) declared-pins allowlist. r2 (packet
   `@210f1fa`, content pin `ad713b22`): 3/3 EXECUTED → **GO / GO / GO-WITH-FIXES** —
   seats re-ran their own r1 forgeries (refused by name), seat 1 CONCEDED its
   "owner-ruling-first" position on gold variety to the driver's BEFORE-YOU-ASK ruling,
   and seat 3's one CHANGE (a forged 289/289 coverage record binding into retained
   authority) was driver-reproduced and folded red-first (bc22, the coverage law moved to
   the authority sibling). **The council arc for the cohort engine CODE is closed.**
2. **The codex-CLI gate (#1) ran FIVE rounds (r5–r9) and is NOT yet literal green.**
   Counts 4→5→4→3→4; severity floor dropped to P2-only at r9. Every finding was folded
   red-first by workers, every red re-run or independently reproduced under driver
   discipline, all logs committed in-tree (`MBCX-01-CODEXCLI-r{5..9}-FULL-LOG-*.log`).
   Two tar-pit closes were made along the way: the closed-list-escape class (3rd
   recurrence → the wholesale malformed-input boundary at both public validators, with a
   WITNESSED honesty carve-out — internal defects still fault loud) and the
   CreateProcessW resolution semantics (documented-set close from the Learn page,
   including the 16-bit `System` search step NO round ever reported). **A codex r10 has
   NOT been run** — the owner ordered closeout first.
3. **What the codex arc actually bought (not referee-polishing):** ~27 data-accuracy
   defects on the live path the elevated smoke run rides, several of which would have
   aborted or corrupted the one elevated session — PMC attached after CSwitch enable
   (whole-run rejection), a SQLite URI metacharacter opening a DIFFERENT database than
   the identity check inspected (the read-only door was silently writable through the
   swallowed fragment), zero-instruction admission, store-mutation-before-identity-check,
   misattributed thread lifetimes, installed-vs-runtime hypervisor evidence.
4. **Gates at close** (driver-run): frozen **156/156** · BUILD **289/289** ·
   `verify-build-bundle.py` REAL exit 0 (ledger **118 invariants / 289 witnesses**,
   two-way) · clean-room `verify-build-pinned.ps1 -Commit d3475536 -ManifestBlob
   7a8abc11` → **PINNED RECONSTRUCTION COMPLETE, real exit 0** (`final-gates-r9fold.log`).
   Readiness unchanged: `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
   **Zero spend, zero provider calls, no ceremony, no experiment, no physical run, zero
   frozen `.py` files touched.**
5. **The owner-ordered ANTI-DRIFT / TAR-PIT / no-adversary audit — run, findings honest:**
   - *Four-partial-fixes fired at least twice on the driver* (closed-list escapes; the
     PMC ordering — r7's fold was itself partial, r8 enumerated the enable set). Both
     were then set-closed, but one round later than the law demands. The habit is live;
     the next driver should enumerate the SET at the FIRST fold, from the API/doc.
   - *The instrument's own gates policed the driver FIVE times this session* (ledger
     carrier rule ×2, pin-freshness arm, W14 unregistered-module, witness-namespace,
     ExecutionPosture catching the undeclared WMI spawn) — each refusal was the
     mechanism working and is banked in the commit messages.
   - *Discriminator sweep over everything built this session:* every refusal stops a
     wrong number/record; none gates a person. TWO judgment calls flagged for the
     owner's eyes rather than buried: (a) `SMOKE_COMMAND_INCONSISTENT_WITH_CANDIDATE_
     IDENTITY` (r9-F4) refuses signing a LYING record — a non-default command under the
     fixed exit-0 identity — with all five documented spellings of the real invocation
     guard-proven untouched; the #28-shadow audit is in ledger row BI-18's note. (b) the
     new preflight abort `HYPERVISOR_RUNTIME_POSTURE_UNDETERMINED` — an unanswerable
     probe refuses to sign a bare-metal claim; it has NEVER fired elevated, and the live
     host was verified to classify HYPER_V_ROOT_PARTITION (the owner's run is not
     walled). If the owner reads either as a person-gate, the mirror shape is the revert.
   - *No new machine.* The largest builds were one validator call at one boundary and
     one identity-derivation function; the census/scanner class was avoided throughout.

## THE OPEN D-CLASS QUESTION FOR THE OWNER (plain language)

The codex gate is not yet literal green after five rounds, but its findings have moved
entirely onto the physical/live path that only the elevated smoke run can truly settle,
and the known would-have-killed-the-run failure modes are now closed and witnessed. Two
honest paths, owner's risk-appetite call:
- **(A) One more codex round (r10) next session, then smoke.** My recommendation: if r10
  is not green or near-empty, stop the gate and let the smoke run become the next judge —
  the #800 lesson says a review loop pointed at ground only execution can settle keeps
  finding plausible work forever.
- **(B) Smoke run first, codex after.** The run now has real protection it did not have
  this morning; its evidence would also settle the several UNVERIFIED_UNTIL_ELEVATED_RUN
  items no review can.

## Traps for the next driver (new this session; -15b/-16/-16b still bind)

- ⛔ The bundle's ledger gates refuse: a row with an empty axis and no carrier · a
  carrier row that itself lacks that axis · a witness id over two digits (module-
  qualified REUSE is the sanctioned mechanism; `bw` is EXHAUSTED) · a ledger row naming
  an unregistered module (hardware-side smoke-cell rows carry NO modules field — the
  BI-12 convention) · an undeclared spawned executable (declare it at the fence with its
  one-line why).
- ⛔ A worker's "suites green individually" is NOT discover-green: two cross-suite
  refusals surfaced only in the one-process discover run.
- ⚠ The pinned clean-room only materializes PINNED subjects + the exported manifest — a
  witness depending on any other repo file refuses a RIGHT reconstruction (the bc14
  probe-file lesson; use the pin manifest itself as the always-present unpinned file).
- ⚠ `verify-build-pinned.ps1` takes the manifest's GOVERNING commit (full 40-hex), not
  HEAD, and needs pwsh 7.
- ⚠ Bash heredocs in this harness can break on long Python bodies — Write the script to
  a file and run it.

## Residuals carried (each with its home)

- Provenance does not FIELD-bind `generation`/`scope_id` per candidate row (bounded by
  the retained authority's full-row hash; measured by the r6-fold worker) → board #31.
- `_root_errors` sibling at `:863` homogeneous-by-construction (named, not folded) ·
  ENVELOPE refusal class zero members · single-motif signature residual pinned at 3 ·
  SCA unconstrained lower bound · W14(d) half-mechanical · shared-reducer pseudo-oracle ·
  UNC store paths loudly refused (not silently wrong) → #31 / in-module declarations.
- All UNVERIFIED_UNTIL_ELEVATED_RUN items (ControlTraceW UPDATE, WMI probe in an
  elevated session, TDH offsets, the 16-bit System mirror) — the smoke run settles them.
- Two ResourceWarnings in `test_mbcx01_build_integration.py:696,703` — cosmetic.

## NEXT (first block of the next session)

1. Owner rules the D-class question above (codex r10 vs smoke-first).
2. If codex r10: serialize it, fold red-first, same discipline; then draft PR + `@codex`
   bot (owner-authorized; Selene has no workflows).
3. #26 relocation out of Downloads to `source/Selene` (clean-room re-proof there).
4. Owner buttons unchanged, blocking nothing: #2 elevated smoke run (conjunction
   criterion, now far safer) · credits pick → route freeze.

## The bytes

At this doc's records commit: HEAD == origin (resolve it); pin manifest governing
`d3475536`, blob `7a8abc11`; every codex log r5–r9 committed in-tree; all three r1/r2
council verdict sets + syntheses + dispatch receipts committed.
