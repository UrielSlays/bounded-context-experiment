# NO-GO — EXECUTED

Reason: the pinned machine can accept invented state authority, can serve an A1 packet that contradicts its admitted poststate, and—after the physical sentinel is retired—its signed-receipt schema can accept invented physical evidence. It also lacks the machine join from terminal call ambiguity to whole-pair missingness. These are reachable false-result paths, not merely the honestly unbuilt physical harness.

Fix classes: **authoritative state-store receipt and poststate projection**, **authority-bearing physical evidence contract**, **episode-ledger-to-inference completeness join**, **reducer independence**, and **preregistered Pareto/preference rule**.

## Seat and scope

- Seat: independent Codex EXEC council reviewer.
- Model: GPT-5-based Codex; exact service checkpoint is not exposed, therefore **UNDETERMINED**.
- Harness: Windows, PowerShell 7.6.4, Git, Python 3.11, Node.
- Review checkpoint: 2026-08-13, governing commit `235f37bcbf213e6700c30333d6fee6a68f0886b6`.
- Longitudinal posture: fresh sealed r12 pass. No current-round council output contents were opened or relied upon. Historical synthesis was read only because it is one of the pinned normative subjects.
- Paid inference/model/provider/route calls: **NONE**.
- Scientific experiment, FD/FC/TN candidates, route qualification, and physical harness: **NOT RUN**.

All relative repository citations below refer to:

`<repo>`

and, for the 31 subjects, to commit `235f37b…`.

## Pin and reconstruction

**EXECUTED — HOLDS for reconstruction integrity.**

- Authenticated object types: governing object is a commit; manifest and launcher are blobs.
- Extracted the launcher from blob `2b575b10f3c00c7a3ac79a39e54693104443f330`; `git hash-object` matched before execution.
- The manifest blob `bd84a65b7b85530345a82a552d7c47f9e148f1a7` contains exactly 31 subjects.
- The authenticated launcher reconstructed all subjects as `235f37b…:path` and verified path safety, Git blob, byte length, LF count, line count, and SHA-384 before import.
- Complete run: exit `0`, about 83 seconds. It passed 87 named tests: 26 state, 22 packet, 4 cohort, 22 measurement/ledger, 10 inference, and 3 integration, plus strict Ajv compilation/mutants, bootstrap guard, pipeline checks, and repair-ledger totality.
- Vendored Ajv blob `fb4622d…` compiled with `AJV_R12_STRICT_COMPILE_OK`. Search found no external package/network/process dependency in the bundle; its `new Function` use is Ajv’s internal schema compiler.
- At final recheck, all 31 working-tree subjects still matched their pinned blobs exactly: `Mismatches=0`.

A concurrent process moved repository `HEAD` from `b0480d4…` to `23a736d…` during this review. I did not cause that transition. The packet blob remained `40fa4a…`, and all 31 subject bytes remained identical to the owner-pinned commit. Therefore the owner-locked pin governs; there is no subject-byte conflict.

## Build-decision challenge

### 1. Already built?

**EXECUTED / SEARCHED.**

Components exist and should be adopted:

- Photon’s fail-closed ambiguity policy.
- Gravity’s built-in Node Ed25519 verification/test shape.
- Existing Gravity/bridge Job Object scaffolding.
- PostgreSQL temporal range/exclusion constraints for non-overlap.
- Windows Job Objects, ETW PMC collection, and job accounting APIs.
- Provider-enforced idempotency patterns from Stripe and AWS.

No searched component supplies the complete MBCX-specific transaction:

`authoritative prestate → exact proposal → committed child → independently retrievable poststate → A1 projection`

or the complete signed Windows physical harness. Adopt the components; do not adopt the packet’s self-authored authority substitute.

### 2. Product fit?

**READ-ONLY.**

Customer need, in one sentence:

> Let an owner test whether exact continuity can be preserved with bounded physical work and whether bounded model context is noninferior, while failing loudly whenever state, transport, or measurement authority cannot be verified.

That need fits **GOVERNED POWER / FAIL-LOUD / MIRROR-NOT-COP**. The current sentinel and fixture-only trust root follow that posture. The state and future-receipt paths do not: they allow self-consistent assertions to substitute for the authority that owns the fact.

### 3. Bigger than the bug?

**READ-ONLY.**

Yes. A real state-authority adapter and a custody-separated Windows receipt producer are subsystems, not leaf fixes. r12 correctly re-entered a design/shelf gate, but the proposed closures remain incomplete. They must not ride forward as bounded review repairs.

## Controlling findings

### P0 — invented authority and poststate/A1 contradiction

**EXECUTED — UNSEARCHED, SETTLED-BY-PINNED-BYTES.**

Evidence:

- `mbcx01_r12_packets.py:319-380` constructs the alleged authority in memory, with a fixture-state fallback.
- `mbcx01_r12_packets.py:524-665` verifies only self-contained state, hashes, and replay; it receives no independently retrieved state-store transaction/readback receipt.
- `MBCX-01-PACKET-SCHEMAS-v6.json:71-74` has no store identity, transaction commit authority, signature, namespace/version, or readback record.
- `mbcx01_r12_integration.py:59-84` calls an event copied from that same input “actual.”
- `mbcx01_r12_packets.py:185-215,410-430` builds A1 objects from `_postcommit_world(manifest)`, not from `transition_authority.postcommit_state`.
- The packet itself says hashes prove integrity, not authority, and requires NO-GO for invented authority: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r12.md:54,72`.

Fresh witnesses:

1. I constructed a new `SCENARIO.ADVERSARIAL.SELF` graph entirely in memory. It had no external authority receipt and scored `1`.

2. I poisoned the genuinely shared `finish_applied` seam so both reducers returned `APPLIED` but left the target obligation `OPEN`. The scorer still served A1 as `COMPLETED` and returned:

```json
{"a1_packet_target_lifecycle":"COMPLETED","poststate_target_lifecycle":"OPEN","reducers_agreed":true,"score":1}
```

This is a reachable false scientific success through the claimed poison boundary.

Smallest repair class:

- Remove scorer acceptance of graph-supplied “authority.”
- Require a state-owner-produced transactional receipt binding store identity, immutable scope/version, exact prestate read, persisted proposal bytes, child commit transaction, and postcommit readback.
- Build A1 by projecting the admitted postcommit state at its exact cut. Compare that projection to the gold expectation; never synthesize the served state from the expectation.

### P0 — physical receipt signs assertions the schema cannot evidence

**EXECUTED / SEARCHED.**

Evidence:

- Architecture requires membership, completion diagnostics, separate final queries, external enforcement, and host/harness identity at `MBCX-01-R12-ARCHITECTURE-SPEC.md:82-94`.
- Exact harness requirements are at `MBCX-01-R12-PHYSICAL-HARNESS-REQUIREMENTS.md:9-22,40-44,59-67`.
- The closed schema at `MBCX-01-MEASUREMENT-CONTRACT-v6.json:53-109` contains only scalar aggregates and booleans.
- `mbcx01_r12_measurement.py:305-346` manufactures every asserted field in memory.
- External-work enforcement is accepted by comparing a constant string at `mbcx01_r12_measurement.py:484-485`.
- The only current ultimate barrier is the unconditional sentinel at `mbcx01_r12_measurement.py:519-521`.

The schema cannot represent:

- network enforcement receipt;
- IPC/broker enforcement receipt;
- Basic+I/O query status/class/size/version/raw evidence;
- Extended-Limit query status/class/size/version/raw evidence;
- process-start-key membership/lifetimes;
- completion messages and loss diagnostics;
- harness build digest;
- host/environment facts.

I signed 100 invented `PHYSICAL_HARNESS_RECEIPT` rows with the pinned deterministic private test key, simulated the documented future production-root classification, and ran the real evaluator. The only error was the unconditional sentinel; without it the grid would be green despite all nine evidence classes being absent.

Microsoft’s current documentation confirms that Job notifications can be lost, PIDs can be reused, ETW exposes loss counters, and Job inheritance has broker/breakaway exceptions. Those facts must be present as evidence, not signed claims about evidence. [Job completion-port caveats](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port), [ETW loss fields](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties), [Job Object inheritance/accounting](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects).

SLSA’s approved v1.2 verification guidance likewise distinguishes a valid envelope from trusted producer identity, subject binding, and expected parameters. [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts).

Smallest repair class:

- Redesign `MeasurementReceiptV2` to bind the separately originated enforcement/query/membership/trace records and their success/status/structure metadata.
- Bind harness build digest, host facts, signer role, and trust-root identity across all cells.
- Execute red witnesses showing that an authorized signer still cannot omit or replace those records.

### P0 — ambiguity is terminal locally but not joined to scientific missingness

**EXECUTED — UNSEARCHED, SETTLED-BY-PINNED-BYTES.**

Evidence:

- `mbcx01_r12_measurement.py:578-606` correctly gives `ACCEPTANCE_AMBIGUOUS` no outgoing edge.
- `MBCX-01-MEASUREMENT-CONTRACT-v6.json:140-145` calls it “terminal whole-pair missing.”
- `mbcx01_r12_inference.py:118-134,250-258` accepts caller-supplied observations and missing IDs; it accepts no call/episode ledger evidence.
- No pinned runtime implements a six-call episode receipt or derives the missing set from ledger terminals.

Fresh witness:

```json
{
  "ledger_state":"ACCEPTANCE_AMBIGUOUS",
  "terminal_missing_reason":"ACCEPTANCE_AMBIGUOUS",
  "complete_pairs_supplied_despite_ambiguity":768,
  "missing_positions_supplied":[],
  "scientific_result":"PROMOTE_TO_COORDINATION_STAGE"
}
```

The ambiguity machine itself is sound, but the scientific machine can ignore it.

Smallest repair class:

- Add a closed six-position episode receipt per scenario.
- Derive the complete/whole-pair-missing partition exclusively from the six authenticated call ledgers.
- Make inference reject any observation/missing partition not reproduced from those receipts.

### P1 — dual reducers share transition effects

**EXECUTED — UNSEARCHED, SETTLED-BY-PINNED-BYTES.**

Evidence:

- `mbcx01_r12_common.py:286-301` owns replay, event persistence, idempotency persistence, next sequence, and last-observed time.
- Both reducers invoke it: `mbcx01_r12_state_reference.py:387-398` and `mbcx01_r12_state_oracle.py:613-627`.
- Architecture says shared code may not own transition effects: `MBCX-01-R12-ARCHITECTURE-SPEC.md:30-32`.
- The official poison test omits these shared functions: `test_mbcx01_r12_state.py:618-686`.

Fresh poison made both reducers return byte-identical `APPLIED` states while failing to persist the event and leaving `next_seq=1` instead of `2`.

Smallest repair class: independently implement replay, event/idempotency persistence, and finalization in both reducers; extend poison tests to both paths. Treat dual agreement as defense-in-depth, not external authority.

### P1 — Pareto/carrier-preference decision is not specified

**READ-ONLY — UNSEARCHED, SETTLED-BY-PINNED-BYTES.**

A search across every normative design, contract, and r12 module found no occurrence of `Pareto`, `carrier preference`, or an equivalent decision rule. `MBCX-01-EXPERIMENT-DESIGN-r9.md:42-44` says comparisons are conditional on gates, but does not define objective coordinates, dominance, ties, or how preference is kept out of the mechanism result.

This creates avoidable practical indecision even if all physical data are valid.

Smallest repair class: preregister the engineering objective vector, hard-gate order, Pareto dominance/tie rules, and a separately labeled owner-preference step.

### P2 — the normative no-paid report is stale and asserts unmeasured facts

**EXECUTED — UNSEARCHED, SETTLED-BY-PINNED-BYTES.**

- `verify-r12-normative-bundle.py:88-99` returns `post_ingress_semantics_shared:false` as a hardcoded literal after only checking one agreeing event.
- The actual bytes share finalization.
- `MBCX-01-R12-NO-PAID-VERIFICATION.json:72` records `MBCX01R11DeterministicPlanningFrequencyV1`, while the pinned generator currently emits `MBCX01R12DeterministicPlanningFrequencyV1`.
- The verifier does not reproduce or byte-compare the pinned static report.

Smallest repair class: remove the derived report from the normative subject set, or regenerate and verify it byte-for-byte/digest-for-digest from the authenticated run. Never hardcode empirical properties such as independence.

### P3 — nonblocking inference residual

**EXECUTED / SEARCHED.**

The arbitrary-missing DP matched exhaustive enumeration for fresh sets through six missing positions, and 128 deterministic completions at `m=20` all lay within its hull. That `m=20` check remains a property spot check, not proof for every missing pattern. The bundle labels this honestly, so it does not control the verdict.

## C1–C12 scoreboard

| Claim | Result | Basis |
|---|---|---|
| C1 decomposition | **HOLDS** | READ-ONLY: phases and stop gates are separated, although C9 lacks its rule. |
| C2 state totality | **FALSE** | EXECUTED: shared replay/finalization permits correlated false agreement. |
| C3 response/proposal integrity | **HOLDS** | EXECUTED for internal byte identity/replay attacks only; provider authority remains non-scope. |
| C4 packet/application validity | **FALSE** | EXECUTED: self-authored transition authority and manifest-derived A1 can score `1`. |
| C5 cohort authority | **HOLDS** | EXECUTED: exact 768, six×128, SHA-256 order, provenance mutations rejected. |
| C6 physical claim honesty | **FALSE** | EXECUTED: future production-signed scalar assertions can pass without required evidence. |
| C7 recovery totality | **HOLDS** | EXECUTED locally: ambiguity has no outgoing edge; durable responses are immutable. |
| C8 serial outcome totality | **FALSE** | EXECUTED: no ledger-to-whole-pair-missing join; inference can ignore ambiguity. |
| C9 engineering fairness | **UNDERDETERMINED** | No normative Pareto/preference mechanism exists. |
| C10 inference | **HOLDS** | EXECUTED / SEARCHED: formula, DP, alpha, type guards, and κ match the opened source and probes. |
| C11 planning/reliability/cost | **HOLDS** | EXECUTED: pointwise frequencies and route tails reproduce; language remains conditional. |
| C12 smallest decisive instrument | **FALSE** | Physical harness is not the sole blocker; state authority, episode join, independence, and Pareto rule also block. |

## Attacks A–H

### A — pin/reconstruction

- Input: pinned commit, manifest blob, and launcher blob.
- Method: authenticated extraction, reconstruction, hash/length/LF/line checks, full launcher execution, Ajv compile, final worktree comparison.
- Output: 31/31 exact; 87 tests plus special witnesses passed.
- Interpretation: reconstruction integrity holds.
- Limitation: this proves the reviewed bytes, not the truth of claims made by those bytes.

### B — state/independence

- Inputs: pinned temporal/cut/scope/action/catalog/identity/rejection mutations plus fresh shared-finalizer poisons.
- Output: registered mutations rejected; fresh poison produced correlated `APPLIED` states with missing journal effects, and a separate poison produced score `1` with poststate `OPEN` versus A1 `COMPLETED`.
- Interpretation: local rules are broad, but reducer independence and final causal authority fail.
- Limitation: no independent production state store exists in the bundle for differential testing; that absence is itself P0.

### C — causal graph

- Inputs: proposal ID/bytes/hash, cut/digest, sequence, effective time, child, poststate/cut, and A1 mutations; fresh self-authored scenario.
- Output: registered mutants failed, but a newly synthesized graph with no authority receipt scored `1`.
- Interpretation: descendant hash binding is strong; external authority and state-derived A1 are absent.
- Limitation: no provider/model was invoked.

### D — cohort

- Inputs: generator bytes/digest, motif, cut, state, gold, action, source ID, order, and missing-ID changes.
- Output: every provenance mutation failed; retained set was exactly 768 with 128 per motif and SHA-256 order. Unknown missing ID failed.
- Limitation: this proves the synthetic frozen population, not external representativeness.

### E — signed physical/ledger

- Inputs: unsigned/tampered/wrong-key/wrong-algorithm/replay/test-key envelopes, mixed run/candidate/generator rows, containment/PMC/loss/I/O mutations, fresh simulated production root, and every outgoing ambiguity event.
- Output: registered attacks failed; all ambiguity transitions failed. The fresh signed 100-cell invented grid would be green if the sentinel were removed.
- Interpretation: signature admission works; evidence authority does not.
- Limitation: physical execution was forbidden and not attempted.

### F — inference

- Small exhaustive comparisons: maximum error `0.0` for fresh missing sets of sizes 1, 2, 3, and 6.
- `m=20`: 128/128 completions inside DP hull, zero violations.
- One complete all-success interval: delta `[-0.0287244111, 0.0287244111]`, OM `[0.9853779687,1]`, promotion.
- Route recursion: bad acceptance `0.04943332980758838`; good acceptance `0.9190668746549461`.
- Independent binomial arithmetic reproduced the same values.
- Boolean/type/duplicate-missing/marginal-hazard poisons raised `ValueError`.
- Limitation: the arXiv source is v1, and the route guarantee depends on the full-past conditional-hazard premise.

### G — planning/cost

Reproduced all five frozen 10,000-stream frequencies:

- `OM90_EQUAL`: `0.9978`
- `LOW_DISCORD_EQUAL`: `0.9975`
- `DELTA_NEG20_OM90`: `0.9973`
- `CEILING_OM70_EQUAL`: `0.9425`
- `(0,.3,.1,.6)` counterexample: `0.7068`

These are pointwise deterministic planning diagnostics, not a region-wide or true-probability guarantee.

### H — omission/build decision

- Artifact to remove: `MBCX-01-R12-NO-PAID-VERIFICATION.json` as a normative static artifact; it is derived and already stale.
- Missing no-paid red witness: an authorized production-role signer supplies schema-valid rows without independent query, enforcement, membership, harness, or host evidence. My simulation shows only the sentinel prevents success.
- Second missing witness: an ambiguous call ledger must mechanically force its frozen scenario into whole-pair missingness before inference.
- Smallest next BUILD artifact after no-paid redesign: a single-cell supervisor-owned Windows harness proof producing one schema-complete signed receipt, including raw query records, membership/start keys, completion diagnostics, ETW configuration/loss, egress/IPC enforcement, harness identity, and host facts.
- Bigger than the bug: yes—both a transactional state-authority adapter and evidence-producing physical supervisor are subsystems.

## Open questions

1. **HELPFUL WITH A NAMED FIX** — Dual replay is useful only after the pre/post state comes from an independently authenticated transaction/readback, and finalization is independently implemented.

2. **HELPFUL** — Terminal ambiguity is the correct rule without authenticated provider replay capability.

3. **HELPFUL WITH A NAMED FIX** — The closed envelope and separate trust root define the cryptographic shape, but the signed payload must contain the required evidence records and producer identity.

4. **HELPFUL WITH A NAMED FIX** — The Windows requirements are proportionate, but the receipt must encode them and the exact CSwitch-delta/OldThread attribution must pass physical red witnesses. Microsoft documents collection at CSwitch, not the packet’s entire attribution inference.

5. **HELPFUL** — Retired instructions should remain primary and fail loud; silently dropping them changes the research question.

6. **HELPFUL** — Total I/O bytes and operations are appropriate H-shape axes. Use checked sums from final Basic+I/O accounting and reject overflow/inconsistent subtotals.

7. **HELPFUL WITH A NAMED FIX** — The oracle does not yet cross the boundary because replay and final transition effects remain shared.

8. **HELPFUL WITH A NAMED FIX** — `456/4` is the executed smallest route plan for the stated risks. Keep `768` as a frozen preregistered scientific size unless a pinned objective/search proves it is mathematically smallest.

## What would I build?

**READ-ONLY / SEARCHED.**

I would build three authority-separated artifacts:

1. A transactional append-only state journal with compare-and-set cut/version, persisted proposal bytes, commit transaction ID, and postcommit readback receipt. The scorer retrieves by receipt; the packet builder cannot manufacture it.

2. A six-call episode receipt that binds every BC/OM A0/B/A1 ledger and deterministically derives either one complete pair or one whole-pair-missing frozen ID.

3. A Windows evidence producer whose signer is outside candidate/evaluator custody and whose payload includes the raw/canonical OS and enforcement records—not booleans paraphrasing them.

Prior art I would adopt:

- **SEARCHED:** PostgreSQL 18 `WITHOUT OVERLAPS`/GiST temporal constraints for range integrity. [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- **SEARCHED:** AWS’s requirement that idempotency-token recording and mutation be one ACID operation. [AWS Builders’ Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- **SEARCHED:** Stripe’s server-enforced same-key/same-parameters/first-result semantics when an approved provider actually offers them. [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)
- **SEARCHED:** SLSA’s root/producer/subject/expectation verification model.
- **SEARCHED:** Microsoft Job Object, job-accounting, completion-port, ETW loss, and PMU configuration APIs.
- **SEARCHED:** Photon’s terminal ambiguity rule and Gravity’s Ed25519 verifier/test shape from the internal shelf.

## Would I design it differently?

**READ-ONLY. Yes.**

I would keep three distinct layers:

`authority acquisition → pure verification → scientific decision`

The current design lets builders generate objects called “authority” and lets expected manifest state generate A1. I would make dual-reducer replay a conformance check only; actual authority would come from the state owner. I would also remove the derived static report from the normative set and pre-register the Pareto/preference rule before any candidate measurement.

## Plain-language owner answer

The experiment’s statistical ruler and frozen cohort appear capable of answering the scientific comparison, but the complete machine cannot yet answer honestly. Today it can declare success from a self-authored state graph, can show A1 as completed when its own poststate says open, can ignore a terminally ambiguous call when constructing the final dataset, and would accept signed physical assertions that omit the evidence the design says is mandatory.

The 768 pairs buy one preregistered paired comparison over the frozen population, split into 4,608 scheduled logical model-call positions: 768 scenarios × two conditions × three nodes. They do not promise 4,608 accepted responses or bound retries. The 456 route trials buy the stated `456/4` consumer/producer risks under the full-past conditional-hazard assumptions, with 2,736 scheduled positions before retries. They do not prove stationarity, hazards in the transition region, or provider idempotency.

More money could fund the authority adapter, the one-cell physical proof, and later capped route/scientific calls. It cannot turn hashes into authority, repair the missing episode join, establish region-wide operating characteristics, or resolve ambiguity by buying replacement calls. Enlarging samples would change the preregistration and still would not fix these defects.

The current red readiness is honest in one important respect: the trust root is explicitly `production_ready:false`, fixture-only, and the unconditional sentinel prevents a test signature from becoming a physical pass. It is incomplete because `PHYSICAL_HARNESS_UNAVAILABLE` is not the sole blocker.

## External sweep log

### Exact queries

- `arXiv 2512.21300 Chugg Ramdas Proposition 3.1 average conditional mean empirical Bernstein exact mixture`
- `site:slsa.dev spec v1.2 verifying artifacts trust root provenance subject digest`
- `site:docs.stripe.com/api/idempotent_requests same key same parameters result`
- `site:aws.amazon.com/builders-library making retries safe idempotent APIs same client request token different parameters`
- `site:postgresql.org/docs current temporal constraints range exclusion constraints`
- `site:itl.nist.gov acceptance sampling binomial single sampling plan`
- `site:learn.microsoft.com TracePmcCounterListInfo TracePmcEventListInfo InstructionRetired CSwitch ETW PMC`
- `site:learn.microsoft.com JobObjectAssociateCompletionPort guaranteed delivery messages active process zero`
- `site:learn.microsoft.com Process Start Key ETW PID reuse ProcessStartKey Windows event tracing`
- `site:learn.microsoft.com/en-us/windows/win32/procthread/job-objects Win32_Process Create job object breakaway`
- `site:learn.microsoft.com/en-us/windows/win32/cimwin32prov/create-method-in-class-win32-process job object breakaway`
- `site:learn.microsoft.com JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION total operation count transfer count`
- `site:learn.microsoft.com JOBOBJECT_EXTENDED_LIMIT_INFORMATION peak job memory`
- `site:learn.microsoft.com "TracePmcEventListInfo" "CSwitch"`
- `site:learn.microsoft.com "TracePmcCounterListInfo" "InstructionRetired"`
- `site:learn.microsoft.com "PmcCounter" "OldThreadId"`
- `Microsoft PerfView PMC CSwitch InstructionRetired counter attribution`
- `Windows ETW PMC counter CSwitch OldThreadId retired instructions`

### Opened and deciding sections

- **SEARCHED:** Chugg/Ramdas arXiv v1, Proposition 3.1 and recommended predictable estimator. It confirms the implemented exact-mixture formula and applicability to average conditional means without iid, subject to the past-filtration premise. It is a December 2025 arXiv v1 preprint, not a final standard. [Paper](https://arxiv.org/html/2512.21300v1)
- **SEARCHED:** SLSA v1.2, “How to verify” and Steps 1–2. It confirmed that signature validity alone is insufficient without trusted producer identity, subject digest, and expectations.
- **SEARCHED:** Microsoft Job Objects, Job completion-port structure, Basic+I/O accounting, `IO_COUNTERS`, Extended Limit, `EVENT_TRACE_PROPERTIES`, `TRACE_QUERY_INFO_CLASS`, PMU recording, and CSwitch. These confirmed aggregate axes and the required failure/loss caveats. [PMU recording](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events), [IO counters](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-io_counters), [CSwitch](https://learn.microsoft.com/en-us/windows/win32/etw/cswitch)
- **SEARCHED:** Stripe and AWS idempotency sections. They confirmed that safe replay is service-enforced, parameter-bound, and—in AWS’s design—atomically joined to the mutation.
- **SEARCHED:** PostgreSQL 18 `CREATE TABLE`, temporal `WITHOUT OVERLAPS` and exclusion-constraint sections. It confirmed adoptable temporal integrity primitives, not a complete MBCX state machine.
- **SEARCHED:** NIST Single Sample Acceptance Plan, `(n,c)` and producer/consumer risk sections. It confirmed the acceptance-sampling framing. The MBC conditional-hazard recursion, not NIST’s binomial example, governs the non-iid route claim. [NIST](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/singsamp.htm)

Microsoft has a real documentation conflict: the current Job Objects page says `Win32_Process.Create` children are not associated with the job, while the older WMI Create page says they are limited unless breakaway is requested. The newer, directly topical Job Objects page is the conservative winner for this design; the harness must explicitly red-test WMI/broker escape.

Why I stopped: current primary sources settled the narrow inference, trust, retry, temporal, and Windows API questions. They did not establish the exact CSwitch-delta attribution inference; that remains a named physical witness, and physical execution was forbidden.

## Internal-shelf sweep log

The packet contains a substantive log with queries, repositories, opened files, and dispositions. I independently spot-ran three queries:

1. `rg -n "ACK_AMBIGUOUS|ISSUANCE_UNKNOWN|No retry|no retry|adjudicat|readback" <home>\source\Photon\crates\aruna\src`

   Opened Photon `attempt.rs:140-165,1148-1165,1788-1810`; HEAD `f9aa2d9…`. Adopt terminal ambiguity; do not adopt the larger adjudication subsystem.

2. `rg -n "Ed25519|compact JWS|createPrivateKey|createPublicKey|signature|verify" <home>\source\Gravity\src\evidence\EvidenceSigner.ts <home>\source\Gravity\src\evidence\EvidenceSigner.test.ts`

   Opened both files; Gravity HEAD `1796fa6…`. Adopt verifier/test shape, not key custody.

3. `rg -n "Job Object|CreateJobObject|SetInformationJobObject|AssignProcessToJobObject|ExtendedLimit|JOB_OBJECT" <home>\source\Gravity\spikes\110-sentinel-slice0c <home>\source\agentvault-mcp-bridge\docs\167-3b-live-wiring-DESIGN-v10-2026-08-05.md`

   Opened the Gravity spike and bridge Job supervisor design; bridge HEAD `ba702fd…`. Reuse scaffolding only. No complete ETW/egress/signed-receipt harness exists there.

I found no internal exact state-authority adapter or complete physical harness to adopt.

## Residual risks and non-claims

- A production signature will always leave a root-of-trust/custody assumption; signatures cannot prove an authorized producer is honest.
- Exact ETW retired-instruction availability and attribution remain host/CPU/OS/privilege dependent.
- Full-past route hazard premises are not established by the route sample and imply no future stationarity.
- The frozen synthetic population does not establish external validity.
- Concurrent writers and coordination-stage behavior remain excluded.
- The arbitrary-missing DP’s `m=20` witness is not a proof for every pattern.
- No actual provider/model response, route, physical measurement, candidate performance, or dollar cost was verified.

## Seal, side effects, and cleanup

- Current-round lateral seal maintained; no other verdict/output contents inspected.
- No repository file was edited. `git diff --stat` remained empty.
- A first launcher invocation hit the shell timeout and left transient output in:

  - `<home>\AppData\Local\Temp\verify-r12-pinned-seat3-current.ps1`
  - `<home>\AppData\Local\Temp\mbcx01-r12-9e560a8b189242d594f7eaaec153c126`

- I validated both exact paths are beneath the Windows temp directory and attempted native PowerShell cleanup. The execution policy blocked deletion, so they remain. The later successful launcher cleaned its own reconstruction.
- Paid inference: **NONE**.
