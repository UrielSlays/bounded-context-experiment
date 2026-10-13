# GO-WITH-FIXES(EPISODE↔OUTCOME LEDGER AUTHORITY JOIN + JOB `TotalTerminatedProcesses` SEMANTICS) — EXECUTED

The r13.1 repairs are largely sound, but two bounded no-paid defects remain. Neither changes the estimand, n=768, six-call episode, 456/4 route gate, inference method, physical grid, or stage order.

## Seat and posture

- Seat: independent Codex council reviewer.
- Model: Codex, GPT-5 family; exact backend checkpoint not exposed.
- Harness: Windows NT 10.0.26200; PowerShell 7.6.4; Python 3.11.9; Node 24.17.0; Git 2.54.0.
- Longitudinal posture: **FRESH r13.1 pass**; no own prior lane context used. The packet-required r13 verdicts and synthesis were read as prior council evidence.
- Lateral seal: maintained. I did not inspect either browser seat’s r13.1 output, verdict, chat, or logs.
- Paid inference: **NONE**.

## Pin and reconstruction

- Governing commit: `d9b054f9617bbeba2b55fa488736adf808f19457` — authenticated Git commit.
- Manifest blob: `e5d6e8f07d1602dac16f0d7df5e8c4ab1ecda4e4`.
- Launcher blob: `e22013a7be82c3e8899b9b0360e1215819859669`; extracted hash matched before execution.
- Manifest subject set: exactly 33 unique subjects.
- Reconstruction exit: `0`.
- Tests: **140/140 passed**:
  - state 34
  - packets 45
  - cohort 4
  - measurement 40
  - inference 14
  - integration 3
- Strict Draft 2020-12 AJV, 56 declared repair witnesses, all 768 retained joins, pipeline and integration: PASS.
- Correct fail-loud result remained:
  - `STATE_AUTHORITY_UNAVAILABLE`
  - `PHYSICAL_HARNESS_UNAVAILABLE`
  - `experiment_executed:false`
  - `provider_calls:0`
  - `paid_calls:0`
  - `physical_harness_executed:false`

Working-tree comparison found 32/33 subjects equal to the pin. Only `MBCX-01-R13.1-NO-PAID-VERIFICATION-REPORT.json` differed; I did not inspect or use that working copy. The pinned blob was used.

Side effects: no repository edits, commits, pushes, labels, experiment calls, physical execution, or persistent probe files. The authenticated temporary reconstruction was cleaned; custom attacks ran through stdin with bytecode writes disabled.

## R1–R6 scoreboard

| Repair | Result | Fresh executed evidence |
|---|---|---|
| R1 retained population / manifest cut | **HOLDS** | Rehashed `SCENARIO.FRESH.NONMEMBER` authority failed `RETAINED_SCENARIO_AUTHORITY_INVALID`. Same-cut state with a changed obligation and repaired state/projection/receipt hashes failed `MANIFEST_CUT_STATE_MISMATCH`. |
| R2 authenticated outcomes | **FALSE** | Direct bit flip plus repaired receipt hash correctly failed. But scorer-graph substitutions remained unbound to the six episode ledgers and drove opposite decisions over the identical 768 complete episodes. |
| R3 downstream non-launch | **HOLDS** | After `BC.B=ACCEPTANCE_AMBIGUOUS`, replacing the required BC.A1 skip with a valid launched terminal ledger and repairing the episode hash failed `EPISODE_PARTITION_MISMATCH`. |
| R4 physical evidence / Windows ABI | **FALSE** | Raw field, lifetime, and diagnostic-message attacks behaved correctly, but an official normal-exit BasicAccounting record with `TotalTerminatedProcesses=0` was falsely rejected. |
| R5 grid identity | **HOLDS** | Changing one signed cell’s host-environment digest, refreshing the envelope, and resigning produced `GRID_IDENTITY_MISMATCH`. |
| R6 engineering selection | **HOLDS** | Changing derived `accounting_complete` and repairing `evidence_hash` was rejected as `ENGINEERING_SELECTION_INVALID`. |

## Findings

### P0

None. Fixture authority still cannot mint scientific or physical eligibility.

### P1-1 — Outcome graphs are not joined to the six episode ledgers

**EXECUTED.**

Locations:

- `mbcx01_r13_packets.py:1205-1286@d9b054f9`
- `mbcx01_r13_inference.py:168-190@d9b054f9`
- `mbcx01_r13_measurement.py:1359-1461@d9b054f9`
- `mbcx01_r13_integration.py:155-165@d9b054f9`

`ScenarioOutcomeReceiptV1` contains scorer graphs and their hashes, but no `episode_hash` or six ordered ledger hashes. Its validator receives no episode receipt. Inference validates outcomes and episodes separately, then joins only by scenario ID/order.

Fresh differential:

- Same 768 complete episode receipts.
- Exact episode-set hash:  
  `46DE7E219778858D59C7C8790CE392450ADFC03703807EC0F7EAEB73F2E1E87DB254AC5F1C25A1A57601BB81C0FF625C`
- 768 admitted `(1,1)` outcome receipts: `PROMOTE_TO_COORDINATION_STAGE`.
- 768 substituted `(0,0)` scorer-graph receipts: `MODEL_OR_INTERFACE_CEILING`.
- Validation failures across both sets: **0**.
- First episode BC.A0 raw-response hash: `653AE7AB…ED9405`.
- Corresponding outcome graph raw-response hash: `5AADD571…06F01`.
- Outcome receipt carries neither the episode hash nor ledger hashes.

For each substituted receipt, the receipt-owned scorer-input and receipt hashes were recomputed. The validator accepted a caller-mutated failing graph without proving it came from the authenticated episode call bytes.

Reachable consequence: once production state authority exists, a caller can associate a separately constructed scorer graph with a valid same-scenario episode and alter the primary scientific conclusion.

Smallest fix class: **bounded authority join**.

- Add the exact `EpisodeReceiptV1.episode_hash` and six ordered position/ledger hashes to `ScenarioOutcomeReceiptV1`.
- Validate every A0/B/A1 `DurableCallRecordV1` against its corresponding `CallLedgerV3`: request hashes, token, route, raw response, response reference, provider ID, durability transaction and receipt.
- Reconstruct parsed scorer results from the exact ledger raw bytes.
- Pass the matching episode receipt into outcome validation; scenario ID alone is insufficient.

### P1-2 — Correct normal-exit Job accounting is rejected

**EXECUTED / SEARCHED.**

Location:

- `mbcx01_r13_measurement.py:721-772@d9b054f9`, especially lines 754-760.

The four-DWORD layout is now correct. However, the evaluator requires the fourth DWORD, `TotalTerminatedProcesses`, to equal the signed membership count.

Microsoft defines that field as the number of processes terminated because of a limit violation—not the number of normally exited Job members. `TotalProcesses` includes associated processes over the Job lifetime, while `ActiveProcesses` is the current count. [Microsoft BasicAccounting structure, Syntax and Members](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information).

Fresh signed case:

- membership count: 1;
- all member lifetimes terminal;
- `TotalProcesses=1`;
- `ActiveProcesses=0`;
- `TotalTerminatedProcesses=0`;
- official 96-byte layout regenerated;
- raw SHA-384 repaired;
- fixture signature regenerated and verified.

Result: `JOB_QUERY_EVIDENCE_INVALID`.

Reachable consequence: a correctly completed physical run with normal process exit cannot pass the future harness gate.

Smallest fix class: **Windows ABI semantic correction**.

- Compare raw `TotalTerminatedProcesses` only with the corresponding scalar.
- Do not equate it with membership count.
- Final completeness remains governed by signed lifetimes, `ActiveProcesses=0`, final queries, and membership evidence.

### P2 / P3

None.

## Other fresh attacks

- R2 direct bit flip `(1,1)→(0,1)` with repaired outcome receipt hash: `SCENARIO_OUTCOME_AUTHORITY_INVALID`.
- R4 fourth DWORD changed `1→2`, raw digest repaired and envelope resigned: `JOB_QUERY_EVIDENCE_INVALID`.
- R4 signed thread lifetime ended at QPC 19 while the second observation occurred at QPC 20: `INSTRUCTION_ACCOUNTING_INCOMPLETE`.
- R4 completion messages/counts set false/zero and resigned: only `PHYSICAL_HARNESS_UNAVAILABLE`; diagnostic status correctly remained non-load-bearing.
- R5 one-cell host identity substitution: signature valid, `GRID_IDENTITY_MISMATCH`.
- R6 caller gate-Boolean substitution with repaired evidence hash: rejected.

## Build-decision challenge

1. **ALREADY-BUILT? — EXECUTED / SEARCHED.**  
   Existing primitives should be adopted: Windows Job Objects and ETW PMC configuration; internal receipt/operator separation; supervisor-owned containment; closed evidence mutation tests. No internal shelf item supplies the exact MBCX retained-source, episode/outcome, state-readback, or signed PMC joins.

2. **PRODUCT-FIT? — READ-ONLY.**  
   Customer need: determine whether bounded context improves six-call coordination while refusing to let self-authored state, unaccounted calls, or unverifiable physical work masquerade as evidence. This is governed-power / fail-loud / mirror-not-cop work.

3. **BIGGER-THAN-THE-BUG? — READ-ONLY.**  
   No. These findings are two local equality checks missing or misapplied inside an already owner-gated scientific instrument. They do not justify a new subsystem or scientific redesign.

## Internal shelf spot-run

**EXECUTED / SEARCHED.**

Exact query:

```text
rg -l -i "JobObject|completion port|ETW|TracePmc|state owner|state-owner|receipt|Ed25519" <home>/source/agentvault-mcp-bridge -g "*.md" -g "*.py" -g "*.ps1" -g "*.js" -g "*.ts"
```

Bridge revision: `ba702fd6c7cc03a697862ed98b9f4d08cdf8d2bb`.

Opened:

- `docs/167-3b-live-wiring-DESIGN-v14-2026-08-05.md`: independent receipts, operator separation, supervisor Job ownership and explicit cross-store disagreement.
- `docs/_archive/m3-live-proof/m3.2-live-proof-harness-design.md`: ordering, rollback and isolation test shape.
- `tests/capture-evidence-record.test.ts`
- `tests/capture-conformance-evaluator.test.ts`
- `<vault>`
- `<vault>`

Disposition: adopt authority/operator separation and evidence-test style; do not import unrelated lifecycle machinery or CDP evidence semantics. No exact state adapter or Windows PMC producer exists on the shelf.

## External sweep log

**SEARCHED.**

Queries:

```text
site:learn.microsoft.com/en-us/windows/win32/api/winnt JOBOBJECT_BASIC_ACCOUNTING_INFORMATION TotalPageFaultCount TotalProcesses ActiveProcesses TotalTerminatedProcesses
site:learn.microsoft.com/en-us/windows/win32/procthread job objects completion port messages guaranteed delivery
site:learn.microsoft.com/en-us/windows/win32/api/evntrace TRACE_QUERY_INFO_CLASS TracePmcEventListInfo TracePmcCounterListInfo
```

Opened at origin:

- [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information), Syntax/Members: confirmed four DWORDs and exposed the `TotalTerminatedProcesses` semantic defect.
- [JOBOBJECT_ASSOCIATE_COMPLETION_PORT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port), Remarks: confirms ordinary messages—including active-zero—are notifications whose delivery is not guaranteed.
- [TRACE_QUERY_INFO_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class), Constants: confirms `TracePmcEventListInfo` configures triggering events and `TracePmcCounterListInfo` configures counters collected on them.

Why stopped: these are the controlling current platform definitions. The remaining defects are settled by pinned implementation bytes and executed differentials.

## Direct answer

Can the current r13.1 bytes answer the original question merely after the two BUILD artifacts appear? **No**: the episode/outcome substitution can still alter the scientific result, and correct normal-exit Job evidence is rejected.

After these two bounded no-paid fixes and separately reviewed:

1. `ProductionStateAuthorityAdapterV1`, and
2. `WindowsPhysicalHarnessV1`,

the design can answer the intended bounded question.

Scientific conceptual redesign should stop. Closure verification should not be marked complete today: land these two local repairs, execute the new red/green witnesses, then stop numbered conceptual rounds and advance only to the two BUILD reviews.

## WHAT WOULD YOU BUILD?

**READ-ONLY / SEARCHED.**

First, the smallest closure repair:

- `ScenarioEpisodeOutcomeBindingV1`, or an extension of `ScenarioOutcomeReceiptV1`, binding one episode hash and six exact ledger identities to the two scorer graphs.
- One corrected Job decoder/evaluator rule that preserves the official fourth DWORD but does not treat limit-violation terminations as all exited membership.

Then:

- a thin production state-owner adapter over an authoritative transactional store, producing distinct manifest-cut and later precommit/postcommit receipts under operator-separated authority;
- a one-cell-first Windows supervisor harness producing official Job bytes, raw ETW PMC evidence, one signed identity, and custody-separated signatures.

## WOULD YOU DESIGN IT DIFFERENTLY?

**READ-ONLY.**

Locally, yes: make the episode receipt the aggregate root for outcome derivation. A separate outcome receipt should reference that root and be unable to validate without it. Two independently valid objects joined only by scenario ID are exactly the authority gap this closure architecture was meant to eliminate.

I would otherwise keep the retained population, estimand, n=768, six-call schedule, missingness rule, inference, route gate, physical grid, sentinels, and Pareto/owner separation.

## Residuals and non-claims

- Production state authority remains unbuilt.
- Production Windows evidence collection and key custody remain unbuilt.
- No physical candidate, route, provider/model call, scientific experiment, or paid work ran.
- Fixture signatures prove verifier behavior only.
- The 100 cells remain a finite registered grid, not an asymptotic claim.
- n=768 does not guarantee a decision at every near-threshold distribution.
- One model/route would not establish cross-model generality.
- Paid inference: **NONE**.
