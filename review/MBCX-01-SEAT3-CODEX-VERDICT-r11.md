# NO-GO — reachable forged causal evidence and self-authorized ambiguous retry

**Verdict basis: EXECUTED.** This is not a NO-GO merely because the physical harness is absent. It is a NO-GO because the pinned executable scorer accepts a causal child that the production state path did not produce, the recovery ledger accepts an untrusted party’s self-minted route attestation to authorize retry after ambiguous acceptance, and the future physical receipt schema has no signature or evidence for its external-compute assertion.

**Fix classes:** trusted causal admission; authenticated route capability; signed physical provenance plus real isolation; independent semantic oracle; internal-shelf discharge. These are classes, not patches.

## Seat, scope, and seal

- Seat: independent fresh Codex EXEC seat.
- Model/checkpoint: Codex, GPT-5 family; the exact backend checkpoint identifier is not exposed to this seat.
- Harness: local Windows PowerShell, Git, Python, Node, vendored Ajv, and internet read access.
- Posture: fresh longitudinal pass; sealed from both browser seats. I did not inspect any current-round browser output, marker, log, or verdict.
- Applicability: the pinned single-writer, immutable-scope, serial `A0 → B → writer → cold A1` no-paid scientific instrument.
- Exclusions honored: no FD/FC/TN implementation, physical-harness build, provider/model/route call, paid call, coordination experiment, production-readiness claim, or concurrent-writer analysis.

## Pin authentication and reconstruction

**EXECUTED**

- Governing commit: `b56e450f8553b96f6121cb045b62eb604e4a0655`
- Manifest blob: `269dbb3fd905c3875616ac70434e333bcede0a1b`
- Launcher blob: `dca3d7951aeba3947af18978b88cc48028c1b572`
- Launcher SHA-384: `70698BBB3722302C0DCB356BF5C412AEA0336B59DE3801B7F28C3720B853A16CB88B7CCD3E9ECECED6A44BB332B5A791`

I extracted the launcher from the pinned blob, verified its Git object ID before execution, and then ran that copy. It reconstructed all 31 exact subjects and verified each commit:path blob, byte count, LF count, line count, SHA-384, exact subject set, and vendored Ajv closure. The authenticated verifier passed all 69 registered tests:

- State: 24
- Packet/DAG: 17
- Cohort: 4
- Measurement/recovery: 12
- Inference: 10
- Integration: 2

The top-level result remained `DESIGN_OR_IMPLEMENTATION_FAIL / PHYSICAL_HARNESS_UNAVAILABLE`.

Current repository `HEAD` is `3e2e336…`; the governing commit is its ancestor. I compared all 31 pinned paths against current `HEAD`: every subject blob matches the pin. Thus working-tree reads cited below match the governing bytes. The pinned artifact still governs.

Authentication attacks:

- CRLF-transformed launcher Git blob: `98f016ba714968a5b02139041c671c22b2222c81`, correctly not the pin.
- One-byte-substituted launcher blob: `50f3d965434d3bad36401947b8210891a22f3b9c`, correctly not the pin.
- Manifest omission changed the in-memory required set; launcher lines 66–69 reject missing, duplicate, or extra subjects.
- The working-tree launcher itself currently hashes to the pinned launcher blob.

The governing bootstrap is at [verify-r11-pinned.ps1](</<repo>/verify-r11-pinned.ps1:17>), with pin checks at lines 58–92 and validated cleanup at lines 94–100.

## Build-decision challenge

### 1. Already built?

**EXECUTED · SEARCHED**

I found no existing complete substitute for the whole Moonwalker instrument after searching all three internal repositories and the outside mechanisms. I did find components that should be adopted:

- Photon already refuses retry from `ACK_AMBIGUOUS/ISSUANCE_UNKNOWN`; see [attempt.rs](</<home>/source/Photon/crates/aruna/src/attempt.rs:149>) and lines 1158–1162, 1800–1808.
- Gravity has keyed, persisted transaction phases and idempotent resume; see [ActionTransactionManager.ts](</<home>/source/Gravity/src/control/ActionTransactionManager.ts:32>).
- The bridge audit code explicitly distinguishes append ordering from crash durability rather than calling an un-fsynced append durable; see [audit.ts](</<home>/source/agentvault-mcp-bridge/src/audit.ts:16>).
- PostgreSQL 18 has temporal `WITHOUT OVERLAPS` and `PERIOD` constraints, useful prior art for temporal keys but not a replacement for this journal’s bitemporal cut semantics. [PostgreSQL CREATE TABLE, temporal constraints](https://www.postgresql.org/docs/current/sql-createtable.html)
- Microsoft Job Objects provide process-tree accounting primitives, but not the complete isolation/provenance mechanism. [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)

The packet’s prior-art memo contains no Internal-shelf log: no exact queries, repos covered, files opened, or adopt/why-not disposition. The newer owner-locked shelf canon dated 2026-08-13 requires that log, and the current user instruction independently requires it. Those owner/process bytes govern that question; the pinned prior-art memo’s omission loses.

### 2. Product fit?

**READ-ONLY**

Customer need, in one sentence: **the owner needs a finite, fail-loud experiment that can determine whether bounded continuity is exact and affordable before authorizing model spend.**

That is governed-power / fail-loud / mirror-not-cop. The explicit physical red state, transport-inconclusive result, fixed transition region, and separate owner authorization fit the product posture. It is not selling proof that every continuity problem is solved or that bypass is impossible.

### 3. Bigger than the bug?

**READ-ONLY**

Yes. r11 grew reference and oracle reducers, a typed packet DAG, call ledger, physical-receipt evaluator, missingness DP, route theorem, reconstruction launcher, and repair ledger in response to review findings. That is a subsystem, not a leaf fix.

It has correctly re-entered a DESIGN council now, but its shelf gate is incomplete and the executable core still contains false-result paths.

## C1–C12 scoreboard

| Claim | Result | Basis |
|---|---|---|
| C1 — decomposition | **HOLDS — READ-ONLY** | The design keeps continuity, carrier mechanism, preference, and model usability as separate decisions. |
| C2 — state totality | **FALSE — READ-ONLY** | Registered traces agree, but the claimed independent reducers share semantic visibility, temporal, graph, and action-legality functions. |
| C3 — response/proposal integrity | **HOLDS — EXECUTED** | The actual state reducers rejected the registered pre-open, cross-scope, stale, replayed, aliased, worker-substituted, arbitrary-rejection, and stale-commit attacks. |
| C4 — packet/DAG validity | **FALSE — EXECUTED** | The scorer accepts an invented canonical child and a historical “postcommit” cut; it does not establish that the state engine applied the claimed event. |
| C5 — cohort authority | **HOLDS — EXECUTED** | Six motifs × 128, generator digest, domains, state/gold/action authority, mutations, and order checks passed. |
| C6 — physical honesty | **FALSE — EXECUTED/SEARCHED** | The current hardcoded red is honest, but the future schema has no signature fields and treats external-work denial as a self-asserted constant. Job Objects alone also do not contain every process-creation route. |
| C7 — recovery totality | **FALSE — EXECUTED** | An untrusted input can mint the exact attestation hash and re-enter `PREPARED` after ambiguous acceptance. |
| C8 — serial outcome totality | **HOLDS — EXECUTED** | Exact ordered pairs and identity-preserving missing IDs are enforced; Boolean outcomes and population substitution fail. |
| C9 — engineering fairness | **UNDERDETERMINED — READ-ONLY** | The design states the separation, but no FD/FC/TN implementation or Pareto analyzer is in the 31-subject bundle. |
| C10 — inference | **HOLDS — EXECUTED/SEARCHED** | Proposition 3.1 applicability, exact interval implementation, alpha split, DP hull, strict thresholds, fixed kappa, and Boolean rejection checked. |
| C11 — planning/reliability/cost | **HOLDS — EXECUTED/SEARCHED** | Frequencies reproduce exactly; the route theorem is correctly conditional and explicitly disclaims marginal-only or stationarity guarantees; scheduled cost units are explicit. |
| C12 — smallest decisive instrument | **FALSE — EXECUTED/READ-ONLY** | Causal admission, route authority, physical provenance, oracle independence, and the shelf discharge are blocking in addition to the unbuilt harness. |

## Findings

### P0-1 — Scorer accepts a causal child the production state path did not produce

**EXECUTED · UNSEARCHED — SETTLED-BY-PINNED-BYTES**

The architecture says the writer receipt carries the “exact applied” event and that invented children are rejected at [MBCX-01-R11-ARCHITECTURE-SPEC.md](</<repo>/MBCX-01-R11-ARCHITECTURE-SPEC.md:60>). The executable bytes do otherwise:

- [mbcx01_r11_packets.py](</<repo>/mbcx01_r11_packets.py:288>) invents a proposal ID and commit child when no actual writer event is supplied.
- Validation at lines 455–485 checks canonical spelling and only that the proposal ID starts with `EV.`. It does not prove the proposal exists, apply the event, or bind it to a state root.
- `score_exact` at lines 531–535 trusts that structural validator.
- The production counterpart at [mbcx01_r11_integration.py](</<repo>/mbcx01_r11_integration.py:105>) creates and applies a different real proposal and commit.

Fresh differential output:

```text
SCORER_DEFAULT_INVENTED_SCORE 1
PRODUCTION_COUNTERPART_RESULT APPLIED
CLAIMED_CHILD_EQUALS_ACTUAL False
CLAIMED_PROPOSAL EV.6ECF...
ACTUAL_PROPOSAL  EV.C8CD...
CLAIMED_CHILD_ID EV.2321...
ACTUAL_CHILD_ID  EV.C93F...
```

A second fresh attack substituted a canonical-looking nonexistent proposal, recomputed the canonical child ID and every downstream receipt/A1/call hash, and obtained:

```text
INVENTED_PROPOSAL_SCORE 1
INVENTED_PROPOSAL_ERRORS []
```

A third set `postcommit_cut.valid_time` to `2026-08-12`, before the child’s `valid_from` of `2026-08-13`, rebuilt all dependent bytes, and obtained:

```text
PRE_EFFECTIVE_A1_SCORE 1
PRE_EFFECTIVE_A1_ERRORS []
```

False-result path: a condition can score `1` based on a state transition that never occurred or on an A1 view that is not postcommit.

**Smallest repair class:** trusted applied-transition admission. The scorer must either replay the exact child against the exact authenticated pre-state or verify a writer-issued receipt binding proposal event, pre-state root, applied child bytes, post-state root, and cut. Canonical self-hashes are not proof of application.

### P0-2 — Ambiguous retry is authorized by a self-minted assertion

**EXECUTED · SEARCHED**

The ambiguous edge appears at [mbcx01_r11_measurement.py](</<repo>/mbcx01_r11_measurement.py:342>) and is authorized at lines 365–368. The “attestation” at lines 457–474 contains only caller-known ledger fields, a fixed semantic label, and an unkeyed SHA-384.

The fixture’s route contract is not a pinned contract artifact; [mbcx01_r11_packets.py](</<repo>/mbcx01_r11_packets.py:105>) uses `"D" * 96`.

I dispatched a ledger, moved it to `ACCEPTANCE_AMBIGUOUS`, independently constructed the six public attestation fields, calculated their public SHA-384, and requested retry:

```text
SELF_MINTED_ATTESTATION_ACCEPTED PREPARED
```

False-result path: the first request may have taken effect; the second request can duplicate the logical call while remaining a valid ledger transition.

AWS requires the service-side idempotency token and mutations to be an atomic durable operation, and stores the original parameters; a caller assertion is not enough. [AWS, “Making retries safe with idempotent APIs,” client identifier and ACID sections](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). Stripe similarly stores and returns the first result for a key and compares parameters. [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests). Internally, Photon already refuses retry from ambiguity.

**Smallest repair class:** delete `ACCEPTANCE_AMBIGUOUS → RETRY_REQUESTED` unless the actual pinned route supplies a verifier-backed, server-enforced idempotency contract. Otherwise ambiguity remains explicit `UNDETERMINED`.

### P0-3 — Future physical provenance is unsigned and external-work denial is a constant

**EXECUTED/READ-ONLY · SEARCHED**

The prose requires an external signer at [MBCX-01-R11-PHYSICAL-HARNESS-REQUIREMENTS.md](</<repo>/MBCX-01-R11-PHYSICAL-HARNESS-REQUIREMENTS.md:7>), especially line 16. The machine contract at [MBCX-01-MEASUREMENT-CONTRACT-v5.json](</<repo>/MBCX-01-MEASUREMENT-CONTRACT-v5.json:39>) has no signature, signer, algorithm, public-key identity, nonce, or replay domain.

`external_work_policy` is merely the constant `NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE`; the evaluator at [mbcx01_r11_measurement.py](</<repo>/mbcx01_r11_measurement.py:259>) checks only that string. I supplied the bundle’s unsigned synthetic rows; every content check passed, with only the unconditional red remaining:

```text
UNSIGNED_SYNTHETIC_EVAL ['PHYSICAL_HARNESS_UNAVAILABLE']
```

If the unconditional line 283 is lifted after building a harness without changing the schema, the evaluator cannot distinguish a signed OS receipt from those self-authored rows.

The platform contract is also incomplete:

- Microsoft documents that `Win32_Process.Create` children are not associated with the parent’s Job Object. It also says security limits must be set individually per process. [Job Objects, “Managing Processes in Jobs” and “Job Limits”](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- Completion-port delivery is generally not guaranteed, so the final accounting query—not notification receipt—must be authoritative. [JOBOBJECT_ASSOCIATE_COMPLETION_PORT, Remarks](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)
- Basic-and-I/O accounting does not contain peak memory; `PeakJobMemoryUsed` is in the extended-limit query. [Basic and I/O accounting](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_and_io_accounting_information), [extended limit information](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- ETW PMC profile sources are collected at profile events or configured system events; the contract needs backend capability, loss, multiplexing, and attribution acceptance evidence. [TRACE_QUERY_INFO_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class), [EVENT_TRACE_PROPERTIES buffer/loss behavior](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties)

MITRE classifies accepting data without verifying its origin/authenticity as CWE-345 and gives checksum-without-signature examples. [MITRE CWE-345](https://cwe.mitre.org/data/definitions/345.html)

**Smallest repair class:** authenticated physical receipt envelope plus isolation evidence. Add a pinned verification key, algorithm/domain/version, signature, anti-replay identity, complete signed payload, separate final basic/I/O and extended-limit queries, ETW capability/loss evidence, and an enforced/tested boundary against WMI, RPC/IPC, pre-existing helpers, and network work.

### P1 — The “independent” oracle shares load-bearing semantics

**READ-ONLY · UNSEARCHED — SETTLED-BY-PINNED-BYTES**

The architecture allows only shared structural validation at [MBCX-01-R11-ARCHITECTURE-SPEC.md](</<repo>/MBCX-01-R11-ARCHITECTURE-SPEC.md:37>). Yet [mbcx01_r11_state_oracle.py](</<repo>/mbcx01_r11_state_oracle.py:64>) calls shared semantic functions for:

- temporal visibility and closure: lines 64, 110–148;
- dependency reachability: line 286;
- action legality: lines 463–503.

Those implementations reside at [mbcx01_r11_common.py](</<repo>/mbcx01_r11_common.py:304>) and lines 312–325, 452–478, and the reference reducer uses them too.

Residual: both reducers can agree on the same semantic defect.

**Smallest repair class:** structural-only shared ingress; independently implement visibility, closure, reachability, and action legality after admission.

### P2 — Required Internal-shelf log is missing

**EXECUTED · SEARCHED**

[MBCX-01-R11-PRIOR-ART-MEMO.md](</<repo>/MBCX-01-R11-PRIOR-ART-MEMO.md:1>) contains external pointers but no internal queries, repo coverage, opened files, or adopt/why-not log. `git grep` at the governing commit confirmed the omission.

This matters because Photon already owns the exact no-retry-from-ambiguity policy that r11 reimplemented less safely.

**Smallest repair class:** evidence/process—add the required query/repo/file/adopt record before the next design gate.

### P3

No P3 finding needed to decide this round.

## Required attacks A–H

### A — Pin/reconstruction

**EXECUTED**

Input: pinned commit, manifest, and launcher blobs.

Method: blob extraction and authentication, exact reconstruction, manifest-set comparison, byte/LF/line/SHA-384 verification, Ajv execution, CRLF and one-byte launcher mutations, and omission-set comparison.

Output: authenticated reconstruction and all registered tests passed; mutated launcher identities differed; omitted manifest entries differ from the required set.

Interpretation: the reviewed bytes are authentic and reproducible.

Limitation: authentication proves which bytes ran, not that their claims are true.

### B — State/time

**EXECUTED**

The registered suite differentially exercised both reducers with explicit and inverted intervals, old cuts after late observations, future and retracted rows, duplicate and aliased responses, worker scope/action/manifest/time substitutions, reduced catalogs, arbitrary rejection hashes, stale commits, and identity replay. All 24 registered tests passed.

Fresh residual: the differential is not independent because both engines call the same semantic helpers.

### C — Causal graph

**EXECUTED**

The 17 registered packet tests rejected their known mutations. The fresh self-consistent attacks defeated the scorer:

- default invented child: score `1`, but production counterpart emitted a different child;
- nonexistent canonical proposal: score `1`, no errors;
- A1/postcommit valid-time before the child: score `1`, no errors.

The existing test at [test_mbcx01_r11_packets.py](</<repo>/test_mbcx01_r11_packets.py:186>) only changes an event ID without recomputing the canonical identity. Its precommit-A1 test at lines 193–200 copies A0 rather than constructing a self-consistent historical A1.

### D — Cohort/population

**EXECUTED**

Generator/digest, contract domains, motif, cuts, canonical state, gold/action authority, eligibility, retained order, and mutations passed. The retained cohort was exactly six motifs × 128 = 768. Complete and missing paths preserved the frozen SHA-256 scenario order.

Residual: this validates the synthetic cohort generator, not future FD/FC/TN candidates.

### E — Physical/ledger

**EXECUTED + READ-ONLY**

- Boolean axes, identity mixing, missing accounting, corrupt recovery, and label-only retry evidence failed as registered.
- Unsigned synthetic rows reached only `PHYSICAL_HARNESS_UNAVAILABLE`.
- Fresh public-field route attestation moved ambiguous acceptance back to `PREPARED`.
- Physical design audit found no signature schema, only a declarative external-work constant, an unclosed process-creation escape, and incomplete ETW acceptance criteria.

No physical harness was built or run.

### F — Inference and route theorem

**EXECUTED + SEARCHED**

Arbitrary missing positions `[0, 137, 511]`:

```text
DP_HULL    (-0.2766564151038233, -0.06176388383713938,
             0.4932055466883892,  0.6461552973825656)
BRUTE_HULL (-0.2766564151038233, -0.06176388383713938,
             0.4932055466883892,  0.6461552973825656)
MAX_ERROR  0.0
```

One reproduced interval, all 768 pairs `(1,1)`:

```text
delta = (-0.028724411075760736, 0.028724411075760736)
OM    = (0.9853779687132999, 1.0)
```

Boolean pairs raised `ValueError`.

Independent route arithmetic:

```text
P(Binomial(456,.02) <= 4)  = 0.049433329807588314
P(Binomial(456,.005) <= 4) = 0.919066874654946
good-route rejection max   = 0.08093312534505381
smallest registered plan   = (456, 4)
```

The pinned recurrence matched direct combination arithmetic within `1.2e-16`. Two hundred fresh history-dependent policies at a seven-trial test horizon respected the theorem’s extremal boundary.

The theorem is valid because acceptance is monotone in each next conditional failure probability. It does not establish that a real route satisfies either full-history hypothesis. The architecture correctly says so at [MBCX-01-R11-ARCHITECTURE-SPEC.md](</<repo>/MBCX-01-R11-ARCHITECTURE-SPEC.md:105>).

The exact-mixture source’s Proposition 3.1 applies to bounded observations and average conditional means without iid observations. [Chugg and Ramdas, Proposition 3.1](https://arxiv.org/html/2512.21300v1)

### G — Planning/cost

**EXECUTED**

The five 10,000-replicate deterministic frequencies reproduced exactly:

```text
OM90_EQUAL          0.9978
LOW_DISCORD_EQUAL   0.9975
DELTA_NEG20_OM90    0.9973
CEILING_OM70_EQUAL  0.9425
R10_COUNTEREXAMPLE  0.7068
```

These are deterministic point diagnostics for the five registered joint distributions—not true-probability lower bounds and not a rectangular-region guarantee.

- 768 pairs buy one fixed-size paired estimate of the average conditional BC–OM difference and OM floor at the registered alpha/margin, plus the displayed pointwise planning behavior.
- 4,608 is the scheduled logical position count: 768 scenarios × two conditions × three nodes.
- 456 route trials buy the stated bad-route/good-route error bounds only if the per-history hazard hypotheses hold.
- 2,736 is 456 complete six-call route trials before retries.
- More scientific pairs narrow intervals and may reduce transition-region indecision. More route trials can change the route test’s operating curve.
- More payment does not repair causal identity, authentication, missingness, physical accounting, route stationarity, or the false region-wide claim.

NIST’s standard `(n,c)` OC formula confirms the binomial acceptance arithmetic but assumes binomial sampling; it is not the source of the packet’s stronger conditional-hazard theorem. [NIST OC sampling-plan section](https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc232.htm)

### H — Deletion/boundary

**READ-ONLY**

- Remove now: the `ACCEPTANCE_AMBIGUOUS → RETRY_REQUESTED` edge and its `route_attestation_fixture` until an actual pinned route verifier exists. The remaining stages are load-bearing.
- Missing no-paid test: for every scorer-accepted writer receipt, replay the claimed child from the exact pre-state and require byte equality with the actual reducer-emitted event and post-state cut. Include a recomputed nonexistent proposal and `postcommit_cut.valid_time < child.valid_from`.
- Exact next gate: first close P0-1/P0-2, separate oracle semantics, and complete the shelf record; then implement a separately governed signed and isolated Windows measurement harness and adversarially verify its trust root, escape resistance, final accounting, peak-memory query, ETW availability/loss/attribution, and replay handling.
- Coordination boundary: coordination behavior remains out of scope unless deterministic carrier exactness/physical gates pass, the route passes 456/4, and the 768-pair scientific result selects `PROMOTE_TO_COORDINATION_STAGE`.

## Open questions

1. **HELPFUL WITH A NAMED FIX** — Shared structural ingress is the right boundary; move temporal visibility, graph reachability, and action legality out of common code.
2. **HELPFUL WITH A NAMED FIX** — Exact cuts and append-only closure are suitable for this single-writer experiment; require the scorer to prove the claimed child was applied at the claimed cut.
3. **HELPFUL WITH A NAMED FIX** — Canonical preimages close catalog substitution, but they do not prove application; add authenticated pre/post state roots and the exact proposal event.
4. **HELPFUL WITH A NAMED FIX** — One shared receipt shape is useful only when issued by the durable-store boundary. Boolean `fsynced/committed` fields plus a self-hash are not durability proof.
5. **HELPFUL WITH A NAMED FIX** — Job Object, completion, ETW, and signatures are proportionate, but add real process/IPC isolation, a signed machine schema, both accounting queries, and ETW loss/capability criteria.
6. **HELPFUL** — `n=768` is defensible after narrowing the claim to registered cells and publishing the 70.68% counterexample.
7. **HELPFUL WITH A NAMED FIX** — `(456,4)` is mathematically valid. Make it operational by pinning the actual schedule/route contract and removing caller-minted retry authority.
8. **HELPFUL** — `DESIGN_OR_IMPLEMENTATION_FAIL` is the correct current top-level state. It honestly says physical evidence is unavailable; it does not answer the research question negatively.

## Prior-art sweep log

### Internal shelf

Exact queries, applied to all three repos:

```text
idempot|retry|durab|receipt|attest
valid_from|valid_to|bitemporal|temporal|append(Event|_event)|evidence-before-effect
JobObject|completion.?port|ETW|retired.?instruction
```

Repositories:

- `agentvault-mcp-bridge@ba702fd6c7cc03a697862ed98b9f4d08cdf8d2bb`
- `Photon@f9aa2d9423676e02dd7f3497fd0bfb096b047ae1`
- `Gravity@1796fa602ea2f1202e6cc335b8603744eee16f9a`

Opened and disposition:

- Photon `attempt.rs:149–158,1158–1162,1800–1808`: **adopt** no-retry-from-ambiguity.
- Photon `aruna-jmap/src/transport.rs:2382–2404`: **adopt** mutation uncertainty as `ISSUANCE_UNKNOWN/ACK_AMBIGUOUS`, not refusal/no-effect.
- Gravity `ActionTransaction.ts:1–44` and `ActionTransactionManager.ts:32–80`: **adopt** keyed persisted phases where a serial durable transaction is needed.
- Bridge `src/audit.ts:1–29`: **adopt** explicit honesty about ordering versus crash persistence.
- No full experiment instrument found; the pieces do not replace the cohort, paired scientific design, or conditional route theorem.

### External exact queries

```text
site:learn.microsoft.com/en-us/windows/win32/procthread job objects completion port active process zero accounting breakaway
site:learn.microsoft.com ETW PMC retired instructions process attribution TracePmcCounterListInfo sampling
site:aws.amazon.com/builders-library making retries safe with idempotent APIs client request token same parameters
Chugg Ramdas Proposition 3.1 exact mixture empirical Bernstein arXiv 2512.21300
site:learn.microsoft.com/en-us/windows/win32/etw "TracePmcCounterListInfo"
site:learn.microsoft.com/en-us/windows/win32/etw "PMC" "PROFILE" kernel logger
site:learn.microsoft.com/en-us/windows/win32/api/evntrace TraceProfileSourceConfigInfo TracePmcCounterListInfo
site:learn.microsoft.com/en-us/windows/win32/api/winnt JOBOBJECT_EXTENDED_LIMIT_INFORMATION PeakJobMemoryUsed
site:postgresql.org/docs/current "WITHOUT OVERLAPS" "PERIOD" temporal constraints
site:docs.aws.amazon.com Builders Library making retries safe with idempotent APIs client request ID same parameters
site:learn.microsoft.com ETW lost events EventsLost BuffersWritten LogFileHeader
site:learn.microsoft.com ETW performance monitoring counters profile sampling interval retired instructions
site:cwe.mitre.org CWE insufficient verification data authenticity hash signature
site:cisa.gov software attestation self attestation signature trust root
site:learn.microsoft.com job object security limits individually process not sandbox
site:google.aip.dev idempotency retry unknown outcome request id
```

Opened at origin and decisive sections:

- Microsoft Job Objects: process inheritance/Win32_Process exception, job limits, notification guarantees, accounting.
- Microsoft completion-port structure: Remarks and `ACTIVE_PROCESS_ZERO`.
- Microsoft basic/I/O and extended-limit structures: accounting fields and peak memory.
- Microsoft ETW query classes and event-trace properties: sampling/event collection and loss/buffering.
- AWS Builders’ Library: caller token, server-side ACID operation, parameter mismatch.
- Stripe API docs: stored first result and parameter comparison.
- PostgreSQL 18 CREATE TABLE: `WITHOUT OVERLAPS` and temporal `PERIOD`.
- SLSA v1.2 artifact verification: signature, trusted builder identity, subject digest, and root of trust. [SLSA verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- Chugg/Ramdas v1: Proposition 3.1 and time-varying average conditional means.
- NIST OC sampling plan: `(n,c)` binomial acceptance formula and its binomial applicability condition.
- MITRE CWE-345: origin/authenticity verification and checksum-only examples.

What changed:

- Microsoft’s process-creation exception and security-limit statement changed C6 to FALSE.
- AWS, Stripe, and Photon established that safe retry depends on an actual server/route contract, not a caller-generated statement.
- SLSA and CWE confirmed that an unkeyed digest is integrity syntax, not provenance.
- Chugg/Ramdas confirmed C10 rather than refuting it.
- PostgreSQL confirmed temporal prior art exists but did not replace the custom single-writer journal.
- NIST confirmed the OC arithmetic while reinforcing that the packet’s non-iid theorem needed its own proof.

Why I stopped: these controlling first-party sources settle the narrow platform, retry, authenticity, temporal, and inference questions. The deciding artifact-behavior findings were then established by execution against the pin; more source count cannot override those bytes.

## What would I build?

**READ-ONLY**

I would still build the experiment, but only after the P0 closures.

1. **Applied-transition receipt — SEARCHED prior art.** A trusted state engine returns an opaque or signed receipt containing the proposal event digest, exact child event bytes, pre-state root, post-state root, and exact postcommit cut. The scorer verifies that envelope and replays the child. I would take the signature/root-of-trust structure from SLSA verification and the durable phase boundary from Gravity.
2. **Ambiguity parking — SEARCHED prior art.** Use Photon’s `ACK_AMBIGUOUS → adjudication only` rule by default. Enable retry only where the pinned service contract supplies AWS/Stripe-style server-enforced idempotency for the same token and parameters.
3. **Physical evidence broker — SEARCHED prior art.** Run the candidate under an individually restricted process identity plus Job accounting; block ungoverned IPC/process-creation paths; have a separate broker collect final basic/I/O and extended-limit data, ETW capability/loss/attribution evidence, and sign the canonical receipt under a key unavailable to candidate and evaluator.
4. Keep the exact-mixture inference, missingness DP, narrowed pointwise planning claims, and conditional-hazard route theorem.

## Would I design it differently?

**READ-ONLY**

Yes. I would use fewer self-describing hashes and one explicit trust boundary per claim:

- State application is attested by the state engine, not the scorer input.
- Retry capability is attested by the route/service contract, not the retrying ledger.
- Physical work is attested by the isolated measurement broker, not the candidate row.
- The oracle shares types and canonicalization only, not semantic helpers.
- Ambiguity remains loud unless a stronger authority resolves it.

That preserves the packet’s good finite experimental design while removing the circular evidence paths.

## Owner-language answer

As written, the experiment cannot yet safely answer its question even if someone merely “builds the harness.” The inference and route mathematics are credible, the cohort is reproducible, and the present red state is honest. But the evidence joins can currently declare a state transition that did not happen and can authorize a duplicate retry using a statement minted by the same input being checked. The future physical schema also cannot authenticate the signer it says is required.

The 768 pairs buy a fixed, preregistered paired comparison of BC against OM over the exact retained population, with explicit uncertainty, missingness handling, OM floor, and noninferiority margin. They schedule 4,608 logical model positions. They do not buy region-wide 90% power, physical correctness, route stationarity, or causal integrity.

The 456 route trials buy an at-most-5% bad-route acceptance bound and an at-most-about-8.09% good-route rejection bound under the stated full-past conditional-hazard hypotheses. They schedule 2,736 logical positions before retries. They do not prove those hypotheses or predict future stationarity.

Paying for more pairs may narrow intervals and reduce transition-region indecision. Paying for more route trials may improve the sampling plan. Neither repairs forged causal evidence, caller-minted authority, external-compute escape, missing signatures, or shared oracle semantics.

The current `DESIGN_OR_IMPLEMENTATION_FAIL` is honest engineering posture, not a negative scientific result. No physical evidence exists yet, so the research question has not been tested.

## Residual risks, non-claims, capability, and side effects

Residuals:

- A finite route sequence cannot itself prove the per-history hazard premise or future stationarity.
- ETW PMC availability, ownership/multiplexing, event loss, processor-specific source identity, and process attribution remain unexecuted.
- No search can prove that no full substitute exists; the three-repo and primary-source sweep found none.
- Floating-point `erf` and root-finding remain platform-sensitive at tiny ulp scale, although no tested decision boundary was near enough to change a result.
- FD/FC/TN exactness, physical performance, provider behavior, and coordination behavior remain undetermined.
- Single-writer success says nothing about concurrent writers.

Non-claims:

- No production readiness, completeness, unbypassability, provider/model quality, route stationarity, regional power, or coordination result.
- No law or jurisdictional claim was needed or made.
- Paid inference: **NONE**.

Capability/lateral seal:

- Git, PowerShell, Python, Node/Ajv, and web access were available.
- I remained sealed from the other seats and their current-round outputs.

Side effects:

- No repository or source file was edited, written, committed, pushed, labeled, or merged.
- The authenticated launcher created only its uniquely named temporary reconstruction and removed it through its validated cleanup path.
- The temporary extracted launcher was removed.
- Direct Python probes used bytecode suppression and produced console output only.
- No provider/model/route invocation or paid call occurred.
