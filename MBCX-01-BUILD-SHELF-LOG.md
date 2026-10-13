# MBCX-01 production BUILD — shelf / prior-art log

Status: BUILD evidence artifact (handoff work-product 9). Driver-run sweep, 2026-08-14, per
BUILD-FROM-THE-SHELF-CANON (list-is-a-floor + query-log rules) and the r13.1 shelf query log
(which remains valid history; this log covers the BUILD-specific mechanisms).

Frozen revisions at sweep time:

- MBCX BUILD worktree base: `91329b2` (branch `codex/mbcx01-production-build`)
- bridge shelf: working tree at `origin/main` lineage of `ba702fd6`
- Photon shelf: `C:\Users\Kingo\source\Photon` working tree
- Gravity shelf: `C:\Users\Kingo\source\Gravity` working tree

## Internal-shelf log (queries actually run, 2026-08-14)

```text
grep -i "JobObject|CREATE_SUSPENDED|JOBOBJECT_|completion.?port|breakaway|AssignProcessToJobObject"  bridge/src        -> 0 files
grep -i "JobObject|CREATE_SUSPENDED|JOBOBJECT_|AssignProcessToJobObject|breakaway"                    Gravity/          -> 12 files (spikes/110-r2-uilimit, spikes/110-sentinel-slice0c, docs/evidence/slice0c-*)
grep    "ed25519|Ed25519"                                                                             Gravity/          -> 10 files (src/evidence/EvidenceSigner.ts, src/capture/CommitmentKeyProvider.ts, ...)
grep -i "single.?writer|writer_gate|readback|append.?first|evidence.?before.?effect"                  Photon/crates     -> 6 files (aruna: lib.rs, store_open.rs, writer_gate.rs, message_store.rs, read_coordinator.rs, message_header.rs)
grep -i "sqlite|WAL|fsync|FlushFileBuffers|durab"                                                     bridge/src        -> 20+ files (seal-durable-sink, seal-write-coordinator, seal-live-writer, muninn-log, ...)
grep -i "readback|read-after-write|postcommit|post-commit"                                            bridge/src        -> 10 files (registry-cut-transaction, muninn-object-container-v2, seal-ledger-schema, ...)
grep -i "record.?before.?effect|evidence.?before.?effect|append(Event|First)"                         bridge/src        -> 10 files (audit.ts, muninn-lifecycle-engine, muninn-content-wal-bounded, ...)
```

Files OPENED (not just listed):

| Shelf item | What it holds | Disposition |
|---|---|---|
| `Gravity/spikes/110-sentinel-slice0c/README.md` (+ its r8 evidence file lineage) | 8-round council-hardened Windows Job-Object containment harness: PID+start-key identity binding, delivered-handle (never bare-PID re-open) discipline, checked native returns with FAULT-vs-verdict exit separation, red witnesses banked as full transcripts, oracle-fault gating, measured A-RED (suspended-create leaves the process object outside the job pre-assign) | **ADOPT the patterns** for BUILD B: identity binding by PID+start key, checked-native-return discipline, FAULT≠verdict exits, red-witness transcript banking, honest-scope disclosure style. **Do NOT import as evidence** (r12 disposition: "containment scaffolding, not measurement evidence"). Note: slice0c prefers born-in-job `PROC_THREAD_ATTRIBUTE_JOB_LIST`; the MBCX contract FIXES suspended-create→configure→port→assign→resume with `created_suspended:true` in the signed schema — build to the contract; the suspended (never-resumed) process cannot run user code pre-assign, and supervisor-crash-in-window is a leak, not an escape. Recorded here as adopt-or-why-not, not silently substituted. |
| `Gravity/src/evidence/EvidenceSigner.ts` | Ed25519 signing via platform crypto, no third-party deps; persisted local key 0600; verify-against-public-key shape | **ADOPT the shape** (r12 disposition: "Ed25519 verifier/test shape, not key custody"): platform-native Ed25519, injected signer interface, fixture keys clearly fixture-only. Custody model comes from the MBCX trust-root manifests, not this file. |
| `Photon/crates/aruna/src/writer_gate.rs` (header + refusal sites) + `store_open.rs` (via BUILD-FROM-THE-SHELF bridge passage) | single-writer arbitration over an SQLite intent log; one-door verified-connection open chokepoint; typed refusals; gate refusal ≠ store error | **ADOPT the pattern** for BUILD A: SQLite-backed durable store behind a one-door open, single-writer gate, typed refusal vocabulary. Rust code itself not imported (BUILD A is Python beside the r13 verification machinery). |
| bridge `src/audit.ts` / seal family (per canon passage; grep-confirmed present) | evidence-before-effect (durable record BEFORE state change), durable append discipline, fail-closed completeness | **ADOPT the law** (T5 record-before-effect) in the BUILD A commit protocol: proposal+child persisted and fsynced in the same durable transaction BEFORE any receipt exists; crash windows produce no receipt. |
| `docs/167-3b-live-wiring-DESIGN-v14-2026-08-05.md:596-616` (bridge; opened by the r13.1 sweep and spot-confirmed by the r13.2 Sol seat) | independent durable receipt, supervisor-owned Job, operator/signer separation, crash/readback discipline | **ADOPT the authority/operator-independence pattern**; do not import its unrelated security lifecycle (r13.1 disposition, carried). |

Not found on any shelf (confirming the r13.1 conclusion): an exact MBCX state-owner
transaction/readback receipt, the six-call episode join, or a complete signed Windows Job/ETW
evidence producer. Those are exactly the two BUILD artifacts this lane implements.

## External sweep (primaries OPENED this lane, 2026-08-14)

| Question | Primary opened | What it settled |
|---|---|---|
| SQLite durability for the BUILD A store | `https://sqlite.org/wal.html` (§2.3 Performance Considerations) | In WAL mode the writer syncs the WAL on every commit **only when `PRAGMA synchronous=FULL`**; NORMAL defers the barrier to checkpoint and "transactions are no longer durable and might rollback following a power failure." ⇒ BUILD A store config pins `journal_mode=WAL` + `synchronous=FULL`. Also: WAL is same-host-only (fine — single-box store) and the `-wal` file is part of persistent state. |
| Job accounting ABI + TotalTerminatedProcesses semantics | `learn.microsoft.com/.../ns-winnt-jobobject_basic_accounting_information` | Already opened and settled by the r13.2 council (both browser seats re-opened it 2026-08-14); carried as SEARCHED-by-council + pinned in the contract; the BUILD B ABI tests bind to the contract's 96-byte layout. |
| ETW PMC configuration classes | `learn.microsoft.com/.../ne-evntrace-trace_query_info_class` (r13.1 sweep) | `TracePmcCounterListInfo`/`TracePmcEventListInfo` are the counter/event configuration surface; pinned in MEASUREMENT-CONTRACT-v7 `capability_query` constants. Carried. |
| Producer/signature-vs-authority separation | `https://slsa.dev/spec/v1.2/verifying-artifacts` (r13 addendum) | Signature verification ≠ trusted producer identity; carried into the custody-separation design. |

(Queries for the Windows process-start-key acquisition API and any additional library adoption
will be appended here at the moment those implementation decisions are made — this log is
append-only for the BUILD lane.)

## Adopted dependency posture

- BUILD A store: **Python stdlib `sqlite3`** (no new dependency; durability config per the
  primary above; Photon aruna is the pattern precedent for SQLite-as-intent-log in this
  ecosystem).
- Signing: **Ed25519 via the platform crypto already used by the r13 fixture path** (no new
  algorithm; consistent with MeasurementTrustRootManifestV2 `ED25519` and the Gravity signer
  shape). Hash sites: SHA-384 everywhere (we control every new format — fips-crypto-inventory
  posture; no SHA-256 sites added).
- No other third-party dependencies planned; any addition gets its own row here with
  license/maintenance status BEFORE adoption.
