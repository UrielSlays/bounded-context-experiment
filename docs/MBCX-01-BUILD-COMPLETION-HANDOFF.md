> ⛔⛔ **SUPERSEDED 2026-08-14 — DO NOT READ THIS AS CURRENT STATE.** This document was written at
> commit `e6f7bdb` and is **27 commits stale**. It says 'BUILD suites: 76/76' (now 114/114), pins
> `df5bbee`/`2fd3897` (now regenerated), and its 'Remaining unavailable statuses' section predates the
> ENTIRE arc that followed: the r1 trust-bootstrap fold, the signature-carrier fold, the r2 fixture-isolation
> fold, the r3 door-contract saga (NO-GO → premise recut → void), the wiring freeze built-then-reverted, the
> fixture-key fold, and the ETW consumer build. **Current state and the ordered next steps live in
> `MBCX-01-RE-ENTRY-2026-08-14.md`; the tracker is `MBCX-01-OPEN-ISSUES.json`.** Preserved unedited below
> because it is the accurate record of what the BUILD task itself delivered.

# MBCX-01 production BUILD — senior completion handoff

Status: BUILD work-product 11. Implementation complete and verified; review gates follow.
Written 2026-08-14 by the BUILD-lane driver.

## What is actually built and verified

**IMPLEMENTED + FIXTURE-EXECUTED (all witnesses green, red-first):**

- **BUILD A — production state-owner adapter.** `mbcx01_build_state_store.py` (SQLite
  WAL+synchronous=FULL one-door single-writer store, schema v2; record-before-effect
  single-transaction commit of proposal+child+snapshot; PENDING/BROKEN distinguished
  terminals that cannot mint; durable anti-replay anchor block in the journal intent row) ·
  `mbcx01_build_state_adapter.py` (mints `StateAuthorityReceiptV2` only from a COMMITTED
  terminal, Ed25519-sealed via injected signer) · `mbcx01_build_state_operator_b.py`
  (independent second operator: own SQL, own hashing, byte-identical receipt-content gate,
  contaminated-finalizer disagreement detected) · `mbcx01_build_state_authority.py`
  (`verify_state_authority_receipt_v2` + `verify_production_scorer_input` with the
  subtractive sentinel discharge — every frozen check runs; the sentinel is discharged only
  on fully-clean, byte-bound V2 authority; fresh-process file-backed verification via
  `ReadOnlyStateStoreView` with operator-injected path).
- **BUILD B — Windows Job/ETW evidence producer + admission.**
  `mbcx01_build_windows_producer.py` (SignedMeasurementReceiptV2: V1 preimage discipline +
  signed nonce + QPC timing_cross_check; faithful-recorder posture) ·
  `mbcx01_build_measurement_authority.py` (custody-first production admission; evidence tree
  validated via the frozen validators, called not copied; V2-only tightenings incl. exact
  QPC/elapsed recomputation) · `mbcx01_build_exactness_authority.py`
  (CarrierExactnessReceiptV3 identity binding; relabeled fixtures refused) ·
  `mbcx01_build_win32.py` (the REAL collector as reviewable ctypes code — suspended-create →
  job configure → completion port → breakaway disabled → assign → resume, PID+start-key
  identity, checked native returns, FAULT≠verdict; **NOT executed**; double-gated behind
  `MBCX01_BUILD_ALLOW_PHYSICAL=1` + a marker-bearing authorization file).
- **Integration** (`mbcx01_build_integration.py` + bi01–bi04): the full connected authority
  graph admits end-to-end with test-only in-memory production roots; fixture evidence cannot
  cross production admission anywhere; no-execution posture proven mechanically;
  Python/Node canonicalization parity with a float-refusal control.
- **Trust-root manifests:** `StateTrustRootManifestV1` + `MeasurementTrustRootManifestV3`
  schemas (strict Draft 2020-12; 12 schema mutants rejected) + committed fixture instances,
  all `production_ready:false`. No production manifest exists or can be committed into
  authority (custody digests are recomputed against injected ceremony evidence).

**STATICALLY VERIFIED:** `mbcx01_build_win32.py` struct layouts equal the frozen 96/144-byte
ABI packer; ETW ordinals byte-checked against the Microsoft TRACE_QUERY_INFO_CLASS primary
(TracePmcEventListInfo=8, TracePmcCounterListInfo=9). `ProcessTelemetryIdInformation=64`
remains flagged in-source as a smoke-stage check item (it is a cross-check whose
disagreement faults loudly, so a wrong ordinal cannot pass silently).

**PRODUCTION-UNAVAILABLE (honest, by design):** `STATE_AUTHORITY_UNAVAILABLE`,
`PHYSICAL_HARNESS_UNAVAILABLE`, and carrier-exactness production authority all remain red
absent real roots/hardware; readiness reports
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.

**NOT RUN:** the experiment, provider/model calls, spending, the 456 route trials, the
4,608 scientific calls, the physical 100-cell grid, any real Job/ETW execution, any signing
ceremony or trust-root activation, the per-witness exactness suite execution (deferred to
the physical stage per MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md §3).

## Exact pins

Branch `codex/mbcx01-production-build` (worktree of the council repo; base = council
branch @ `91329b2`, which banked the r13.2 3/3 CONFIRMED verdicts).

| Commit | Content |
|---|---|
| `c25e355` | shelf/prior-art log + design notes |
| `6c3bc2a` | red witnesses + fail-loud skeletons (69 witnesses red, transcripts banked) |
| `18864ac` | BUILD A green + custody ceremony spec |
| `db02735` | BUILD B green + smoke runbook + real collector |
| `2fd3897` | **content-final**: folds (durable anti-replay, fresh-process verification) + integration + repair ledger + BUILD verifier + clean-room pair + exactness spec |
| `df5bbee` | pin manifest (28 BUILD subjects + 32 frozen dependencies at `2fd38972…`) |

## Test results (all driver re-run before each commit)

- BUILD suites: **76/76** (state 28 · measurement 44 · integration 4), every witness
  red-first with banked transcripts (`MBCX-01-BUILD-A-RED-WITNESS-RUN…`, `…-B-RED…`,
  green runs, and the fold reds inside `MBCX-01-BUILD-INTEGRATION-RUN-2026-08-14.txt`),
  plus three discrimination probes (reader-independence, limit-violation gate, QPC
  recomputation) proven load-bearing.
- Frozen r13.2: **145/145** unchanged; all 61 governed witnesses mapped; zero frozen
  files touched in any commit (`git diff` scoped adds only).
- Repair ledger: 34 rows / 76 witnesses, two-way totality mechanically enforced by
  `verify-build-bundle.py`.
- Clean-room: `verify-build-pinned.ps1 -Commit 2fd38972ca40820e5e4ac049b18ca480f29392c8
  -ManifestBlob 5f5cd20b0fc526edca81bd285920ee52bf374b36` → **exit 0**, all sections PASS,
  reconstructed from git objects alone.

## Work products index

1–2. adapters/producers (above) · 3. production verification adapters
(`verify_production_scorer_input`, `evaluate_production_measurement`,
`verify_production_carrier_exactness`) · 4. config = injected-parameter model, no secrets
anywhere (fixture keys clearly labeled; committed manifests production_ready:false) ·
5. `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` · 6. `MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md`
+ implementation · 7. test suites + `MBCX-01-BUILD-REPAIR-LEDGER.json` ·
8. `verify-build-bundle.py` + `generate-build-pin-manifest.ps1`/`verify-build-pinned.ps1` ·
9. `MBCX-01-BUILD-SHELF-LOG.md` · 10. `MBCX-01-BUILD-SMOKE-RUNBOOK.md` · 11. this handoff.

## Remaining unavailable statuses and the precise next authorization

Everything below requires a NEW, explicit, bounded owner authorization — nothing in this
BUILD authorizes it:

1. **BUILD acceptance review** (next gate, no spend): council depth-check + codex gate over
   this branch, then owner acceptance.
2. **One-cell smoke proof** (first physical execution): per
   `MBCX-01-BUILD-SMOKE-RUNBOOK.md` §3 — named binary, host, cell, evidence destination,
   cleanup; fixture-kind evidence; its pass criterion is an honest RED at admission.
3. **Custody ceremony** (production keys/roots): per `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md`.
4. **Route freeze** (endpoint/model/prices; couples to the startup-credits decision) →
   route qualification → the experiment. Each separately owner-authorized.
