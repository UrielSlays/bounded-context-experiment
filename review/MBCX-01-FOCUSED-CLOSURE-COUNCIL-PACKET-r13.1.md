# MBCX-01 Focused Closure Council Packet r13.1

## 0. Seat command, seal, and immutable bundle

You are one longitudinal Moonwalker council seat reviewing the bounded r13.1 fold requested by the owner after r13. Read `<vault>`, then adjudicate repository `<repo>` read-only.

Maintain the lateral seal. Do not inspect another seat's r13.1 output, log, completion marker, or verdict. Your own prior lane context and your own r13 verdict are allowed and must be labeled.

Governing implementation commit: `d9b054f9617bbeba2b55fa488736adf808f19457`

Pin-manifest Git blob: `e5d6e8f07d1602dac16f0d7df5e8c4ab1ecda4e4`

Pinned reconstruction-launcher blob: `e22013a7be82c3e8899b9b0360e1215819859669`

Authenticate and execute the pinned launcher, never a working-tree substitute:

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r13.1-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','e22013a7be82c3e8899b9b0360e1215819859669') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git hash-object -- $launcher).Trim() -ne 'e22013a7be82c3e8899b9b0360e1215819859669') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit d9b054f9617bbeba2b55fa488736adf808f19457 -ManifestBlob e5d6e8f07d1602dac16f0d7df5e8c4ab1ecda4e4
```

The manifest has 33 exact subjects. The live no-paid verifier reports 140 total unit tests, 56 governed repair witnesses, strict Draft 2020-12 AJV admission, all 768 retained-source joins, and `experiment_executed:false`, `provider_calls:0`, `paid_calls:0`, `physical_harness_executed:false`.

Do not edit files. Do not run the experiment, a physical harness, route qualification, provider/model calls, or either future production adapter. Deterministic read-only reconstruction and fresh no-paid attacks are authorized.

## 1. Why this focused packet exists

The r13 council returned one `GO` and two `GO-WITH-FIXES`; no seat found a core conceptual `NO-GO`. The owner disposition accepted exactly one bounded r13.1 repair and prohibited reopening the estimand, n=768, six-call episode, 456/4 conditional-hazard route gate, inference method, physical grid, or three-stage stop order without a newly demonstrated reachable false result.

Read first:

- `MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r13.md`
- `MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r13.md`
- `MBCX-01-SEAT3-CODEX-VERDICT-r13.md`
- `MBCX-01-COUNCIL-R13-SYNTHESIS-AND-DISPOSITION.md`
- `MBCX-01-R13.1-NO-PAID-VERIFICATION-REPORT.json`
- `MBCX-01-R13.1-SHELF-QUERY-LOG.md`
- the r13 architecture, invariant matrix, physical requirements, four contracts, repair ledger, implementation, and tests pinned by the manifest.

This is a delta review. Recheck unchanged r13 machinery only where a delta can invalidate it.

## 2. The six accepted repairs

### R1 — source-owned retained population and exact manifest-cut state

`RetainedScenarioAuthorityV2` recomputes the pinned generator and selection, carries the complete selected candidate record, source provenance, exact retained position, candidate hash, and `retained_set_root` over all 768 ordered candidate hashes. A manifest cannot mint membership from its own fields. Integration executes candidate→manifest authority for all 768 retained scenarios.

`ManifestCutStateReceiptV1` separately binds the exact state bytes/hash, exact manifest cut, projected world, source candidate, and retained root. It is distinct from the later proposal-bearing precommit `StateAuthorityReceiptV1`.

Attack: create a self-consistent nonmember candidate; create a legal same-cut but divergent state receipt; repair their local hashes. Neither may join.

### R2 — authenticated scientific outcome bits

Inference no longer accepts rows containing naked `bc` and `om` bits. A complete scenario supplies `ScenarioOutcomeReceiptV1`, which embeds exact BC and OM scorer graphs and hashes. The validator recomputes both bits; valid zero outcomes are representable by binding the exact failing graph. Fixture receipts cannot cross the production-authority boundary.

Attack: flip a bit and rehash the receipt; substitute either scorer graph; supply a naked row; supply an outcome for a missing episode.

### R3 — explicit downstream non-launch

Every one of the six registered episode slots is an `EpisodeCallV2`: either a launched terminal `CallLedgerV3`, or `NOT_LAUNCHED_UPSTREAM_TERMINAL` bound to the exact prior failed ledger in the same condition. A caller cannot claim a downstream call launched after terminal ambiguity or preaccept failure.

Attack: launch after a failure, skip before a failure, or change the upstream ledger reference and repair the skip hash.

### R4 — raw physical evidence, correct Windows ABI, and diagnostic completion messages

The signed physical shape now carries process and thread QPC lifetimes, raw PMC capability/event-attachment records, ordered per-processor CSwitch counter observations, and recomputed deltas joined by PID/start-key/TID.

The 96-byte Windows Job Basic+I/O preimage is `4 × LARGE_INTEGER`, `4 × DWORD`, then `6 × ULONGLONG`. The four DWORDs are page faults, total processes, active processes, and total terminated processes. Completion-port message counts and active-zero notification are diagnostics because Microsoft does not guarantee ordinary message delivery; signed terminal lifetimes plus final active zero and final queries are load bearing.

Attack: change an ABI field/offset, raw counter/delta, lifetime, or PID/start-key join while repairing the envelope signature with the fixture key. It must fail the named semantic gate. Setting diagnostic message counts to zero must not falsely fail a valid final barrier.

### R5 — one complete grid identity

All 100 cells must share run, candidate, generator, harness artifact/build/configuration, host/environment, signing key, producer role, fixture kind, and trust policy. The cell coordinate remains individually signed; any mismatch is the `GRID_IDENTITY` failure surface.

Attack: change any one identity coordinate in one otherwise valid signed cell.

### R6 — evidence-derived engineering selection

`EngineeringCandidateEvidenceV1` embeds `CarrierExactnessReceiptV1` plus the exact signed 100-cell evidence. Gate Booleans and worst-cell metrics are derived. `engineering_selection` reconstructs the evidence before Pareto selection and rejects caller summaries or preferences.

Attack: substitute a metric or Boolean, repair the outer evidence hash, or add a preference field.

## 3. Primary-source and shelf corrections

The official Microsoft structure lists four DWORDs after the four time fields. The official completion-port documentation says ordinary messages are notifications whose delivery is not guaranteed. The official ETW query-info enum defines `TracePmcEventListInfo` and `TracePmcCounterListInfo` for event-attached PMC configuration. Exact URLs, internal queries, repository revisions, opened files, adoption decisions, and the future BUILD operator-independence witness are recorded in `MBCX-01-R13.1-SHELF-QUERY-LOG.md`.

Spot-run at least one internal query and open the controlling Microsoft pages yourself. Search results or packet prose are not source evidence.

## 4. Non-claims and stop boundary

The top-level readiness intentionally remains `DESIGN_OR_IMPLEMENTATION_FAIL` because `STATE_AUTHORITY_UNAVAILABLE` and `PHYSICAL_HARNESS_UNAVAILABLE` remain true. That is not a failed r13.1 fold; it is the honest BUILD boundary.

A focused `GO` means: stop numbered conceptual closure rounds and advance only to two separately reviewed BUILD artifacts—(1) production state-owner adapter/store/readback authority and (2) production Windows Job/ETW evidence producer with custody-separated signing. It does not authorize running either artifact, the 100-cell grid, route trials, 4,608 scientific calls, or spending.

Return `GO-WITH-FIXES` only for a bounded local no-paid defect in this delta. Return `NO-GO` only for a reachable false result, invalid inference/authority path, or practical inability to answer that remains even after the two published BUILD artifacts exist.

## 5. Required focused verdict

Return one self-contained report with:

1. `GO`, `GO-WITH-FIXES(reason)`, or `NO-GO(reason)` under the meanings above;
2. seat/model/checkpoint/harness and longitudinal posture;
3. exact pin/reconstruction result and side effects;
4. an R1–R6 scoreboard (`HOLDS`, `FALSE`, or `UNDERDETERMINED`) with executed evidence;
5. at least one fresh, fully rehashed adversarial case against each repair;
6. findings P0–P3 with exact file/function, reachable consequence, and smallest fix;
7. a direct answer: can the design answer the original question after the two BUILD prerequisites, and should conceptual rounds stop now?
8. `WHAT WOULD YOU BUILD?`, `WOULD YOU DESIGN IT DIFFERENTLY?`, internal shelf spot-run, external primary-source sweep, residuals, and paid inference `NONE`.

Do not soften a real blocker to obtain a GO. Do not reopen accepted design merely because another design is possible. Name the missing byte, identity, proof, receipt, formula, implementation, or cost.
