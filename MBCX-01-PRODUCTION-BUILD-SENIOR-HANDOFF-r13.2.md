# MBCX-01 Production BUILD Senior Handoff — r13.2

Copy this entire document into a fresh coding task. It is an implementation commission, not another design-council round.

## Role and objective

You are the senior implementation owner for MBCX-01. Build the two production authority prerequisites required by the unanimously confirmed r13.2 design:

1. a production state-owner adapter/store/readback authority; and
2. a production Windows Job Object/ETW evidence producer with custody-separated signing and exact-build carrier authority.

Then connect both production interfaces to the existing r13 conformance and verification machinery without changing the approved experiment, estimand, inference, sample size, route gate, six-call episode, or three-stage stop order.

This is a governed experimental harness, not a general agent framework such as Hermes or OpenClaw. Your job is to implement the missing authority and measurement machinery so the existing instrument can eventually answer its registered question. You are not authorized to run that experiment in this task.

## Repository and frozen baseline

Repository:

`C:\Users\Kingo\Downloads\moonwalker-bounded-continuity-design-council-2026-08-11`

Council branch at handoff:

`codex/mbcx01-design-council`

Council handoff base commit:

`ede22ede5dbf29381397a99e201f7f7f1b119942`

Governing r13.2 implementation commit:

`d97d654e21918450994cfddb5a53dc5da2e962bb`

Pin-manifest Git blob:

`407a1cd73197af7dbad767976f5c077d91986c87`

Authenticated launcher blob:

`1bb8c15d1fd14303fa0a10fa615a881cb65e0d96`

The governing bundle contains 34 exact subjects. Its authenticated clean reconstruction passed 145/145 tests, 61 governed repair witnesses, strict Draft 2020-12 AJV admission, all 768 retained-source joins, the connected pipeline, and integration. The three independent confirmation seats—Claude Opus 5, ChatGPT GPT-5.6 Sol, and Codex EXEC—each returned `CONFIRMED`, with no P0–P3 finding.

Preserve all frozen r13/r13.2 subjects byte-for-byte. Do not “upgrade” them in place. Add versioned BUILD artifacts, adapters, schemas, tests, and documentation alongside them. If the production interface requires a new contract version, create one and document the compatibility boundary explicitly.

The existing checkout contains historical untracked council logs that belong to the owner. Do not delete, overwrite, stage, or normalize them. Prefer a fresh Git worktree and a new branch such as `codex/mbcx01-production-build` from the documentation commit containing this handoff. If you work in the existing checkout, stage only files you intentionally own.

## Mandatory workflow context

Read these canonical workflow artifacts completely before implementation. They were written for security work, so apply their workflow, evidence, authority, drift, and escalation rules to this scientific-engineering task; do not import irrelevant security claims.

From `C:\AgentVault\Moonwalker`:

1. `CC-DEV-WORKFLOW-GUIDE.md`
2. `ANTI-DRIFT-PLAYBOOK.md`
3. `TAR-PIT-PROTOCOL.md`
4. `BUILD-FROM-THE-SHELF-CANON.md`
5. `DESIGN-SHELF-MAP.md`
6. `BEFORE-YOU-ASK-THE-OWNER.md`

For Moonwalker/operator mechanics, read:

`C:\Users\Kingo\source\agentvault-mcp-bridge\MOONWALKER_DRIVING_GUIDE.md`

Also read the prior senior closeout for research intent and history:

`C:\Users\Kingo\Downloads\moonwalker-bounded-continuity-design-council-2026-08-11\MBCX-01-SESSION-CLOSEOUT-2026-08-12.md`

Run the shelf and prior-art sweep before choosing libraries or creating new infrastructure. Prefer existing reviewed Windows, cryptographic, durable-store, receipt, and process-supervision components when they satisfy the exact contract. Record every adopted/rejected candidate, version, source, license, and reason in a BUILD shelf log.

## Mandatory design reading order

Read current artifacts, not the superseded numbered-round packets, unless a current artifact explicitly points backward.

1. `MBCX-01-TARGETED-CLOSURE-CONFIRMATION-PACKET-r13.2.md`
2. `MBCX-01-SEAT3-CODEX-VERDICT-r13.2.md`
3. `MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json`
4. `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`
5. `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`
6. `MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md`
7. `MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md`
8. `MBCX-01-R13.1-SHELF-QUERY-LOG.md`
9. `MBCX-01-STATE-TRANSITION-CONTRACT-v8.json`
10. `MBCX-01-PACKET-SCHEMAS-v7.json`
11. `MBCX-01-MEASUREMENT-CONTRACT-v7.json`
12. `MBCX-01-INFERENCE-CONTRACT-v8.json`
13. `MBCX-01-R13-REPAIR-LEDGER.json`
14. `MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json`
15. `MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json`
16. `MBCX-01-R13-PIN-MANIFEST.json`

Then read every current r13 implementation and test file:

- `mbcx01_r13_common.py`
- `mbcx01_r13_state_reference.py`
- `mbcx01_r13_state_oracle.py`
- `mbcx01_r13_packets.py`
- `mbcx01_r13_measurement.py`
- `mbcx01_r13_inference.py`
- `mbcx01_r13_integration.py`
- `test_mbcx01_r13_state.py`
- `test_mbcx01_r13_packets.py`
- `test_mbcx01_r13_measurement.py`
- `test_mbcx01_r13_inference.py`
- `test_mbcx01_r13_integration.py`
- `verify-r13-normative-bundle.py`
- `verify-r13-schema-ajv.mjs`
- `verify-r13-receipt-signature.mjs`
- `verify-r13-pinned.ps1`
- `test-r13-normative-bundle.ps1`

Do not use the historical r1–r12 implementations as authority. They are useful only as archaeology when a current repair-ledger entry names one.

## Authenticate the baseline before changing code

Extract and authenticate the launcher from Git rather than executing a working-tree substitute:

```powershell
$repo = 'C:\Users\Kingo\Downloads\moonwalker-bounded-continuity-design-council-2026-08-11'
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r13.2-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','1bb8c15d1fd14303fa0a10fa615a881cb65e0d96') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git -C $repo hash-object -- $launcher).Trim() -ne '1bb8c15d1fd14303fa0a10fa615a881cb65e0d96') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit d97d654e21918450994cfddb5a53dc5da2e962bb -ManifestBlob 407a1cd73197af7dbad767976f5c077d91986c87
```

Record the exit code and section totals. If this reconstruction is not green, stop and diagnose the environment before building.

## Fixed design decisions

These are inputs, not invitations to redesign:

- one writer, one immutable experiment scope, one frozen model/route;
- serial `A0 → B → writer → cold A1` episodes;
- exactly six registered call positions per scenario;
- retained cohort size 768 and its pinned deterministic selection;
- exact episode/outcome authority joins;
- current route conditional-hazard gate and registered inference;
- fail-loud separation between fixture conformance and production authority;
- reference/oracle reducer independence;
- state authority and physical measurement authority are separate roots;
- no scientific result may be produced while either production authority is unavailable;
- existing r13.2 `ScenarioOutcomeReceiptV2`, `EpisodeReceiptV1`, and `CarrierExactnessReceiptV2` joins remain load bearing.

If implementation evidence proves one of these impossible, do not silently substitute a different design. Produce a minimal executed counterexample and escalate to the owner.

## BUILD A — production state-owner adapter

Implement a real production adapter behind the published state-authority boundary. It must emit a production form of `StateAuthorityReceiptV1` or an explicitly versioned successor and be independently verifiable by the packet/scientific admission path.

The receipt and verifier must bind at minimum:

- closed domain and version;
- independently configured store ID, namespace, and namespace version;
- immutable transaction/commit ID;
- exact prestate read bytes, hash, and cut;
- exact persisted proposal event bytes, event ID, hash, and persistence identity;
- exact applied child event bytes, event ID, hash, and next sequence;
- exact postcommit readback bytes, hash, and current cut;
- signer/key/producer identity, role, algorithm, policy, validity/revocation state, subject identity, and signature;
- receipt digest and anti-replay identity.

Required behavioral properties:

1. The writer commits proposal, child, and state atomically according to the approved single-writer model.
2. Postcommit authority comes from a durable store readback after commit, not from the writer's in-memory object.
3. The production readback path is independently identified. A writer self-attestation or fixture constructor cannot become production evidence.
4. Both independent reducers replay the exact persisted child from the exact read prestate and reproduce the exact readback state/cut.
5. Wrong store, namespace, version, transaction, cut, proposal, child, sequence, state, hash, role, signature, subject, or replay identity fails loudly.
6. Fixture receipts continue to fail scientific admission with `STATE_AUTHORITY_UNAVAILABLE`.
7. When no configured production adapter/root exists, behavior remains fail-loud and backward compatible.
8. Crash/restart windows cannot produce a receipt for an uncommitted or partially committed transition.

Do not place a production private key in the repository, test fixtures, environment logs, packet, or receipt. Use an appropriate OS-backed or external key-custody interface. Define configuration and dependency injection so tests can use a clearly fixture-only key without creating a production activation path.

## BUILD B — Windows Job/ETW evidence producer

Implement the production Windows evidence producer described by `MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md`. Its canonical signed output must be consumable by the existing r13 measurement evaluator or an explicitly versioned compatible adapter.

Required process-control behavior:

1. Create the candidate root process suspended.
2. Create/configure the Job while inactive.
3. Associate the completion port before resume.
4. Disable normal and silent breakaway.
5. Assign the root to the Job before resume, then resume.
6. Bind every root and descendant to PID plus 64-bit process start key and retain signed process/thread QPC lifetimes, including terminated members.
7. Treat completion messages as diagnostics. Prove completion with signed terminal lifetimes, a final `ActiveProcesses == 0`, and final queries.
8. Enforce and evidence no network egress, no external compute broker, no preexisting-helper delegation, and no breakaway using supervisor-owned controls established before resume.

Required Job accounting:

- separate final `JobObjectBasicAndIoAccountingInformation` and `JobObjectExtendedLimitInformation` queries;
- exact 64-bit ABI decoding;
- Basic+I/O preimage exactly 96 bytes: four signed 64-bit time fields, four 32-bit fields, then six unsigned 64-bit I/O fields;
- the fourth DWORD is `TotalTerminatedProcesses`, meaning Job-limit-violation terminations; a clean admitted run requires zero;
- normal exit is proved by member lifetimes plus final active zero, not by incrementing that field;
- retain raw bytes, sizes, information classes, call status/error, structure version, and raw SHA-384 digests;
- recompute and check canonical CPU, I/O operations/bytes, peak committed memory, and elapsed monotonic time.

Required retired-instruction evidence:

- strict `ETW_PMC_EVENT_ATTACHED_V1`;
- `InstructionRetired` attached to `CSwitch` through the documented PMC counter/event information classes;
- raw capability query and event-attachment evidence;
- ordered raw per-processor counter observations;
- consecutive counter deltas attributed to outgoing `OldThreadId` and joined to signed Job-member PID/start-key/TID lifetimes;
- no multiplexing, scaling ambiguity, owner conflict, missing attribution, `EventsLost`, `LogBuffersLost`, or `RealTimeBuffersLost`;
- unsupported or incomplete instruction accounting is a hard failure, never a guessed metric.

Required signed authority and exactness:

- bind run, candidate, candidate/carrier artifact digest, generator, cell coordinate, harness artifact/build/configuration, host/environment, signing key, producer role, fixture kind, policy, subject, and nonce in the signed preimage;
- establish one exact full-grid identity across all 100 registered cells, but do not execute that grid in this task;
- provide production carrier-exactness authority bound to the pinned suite/witness set, exact carrier artifact, exact harness build, and exact grid identity;
- the signing-key custodian must not be able to edit or approve the evaluator trust-root manifest;
- trust-root approval must be held by an authority disjoint from the signer;
- candidate and evaluator processes must never receive the private key;
- self-generated keys, repository edits, relabeling fixture evidence, or replay across a build/grid must not create production authority.

Supported environments and capability gates must match the contract. Nested virtualization remains unsupported. Do not paper over missing PMU/ETW support with synthetic data.

## Integration boundary

Connect the two BUILD artifacts to the current fail-loud APIs without weakening them:

- production state receipts can satisfy `verify_state_authority_receipt(..., require_production=true)` only through the reviewed production adapter/root;
- fixture state receipts remain conformance-only;
- physical measurement admission can clear `PHYSICAL_HARNESS_UNAVAILABLE` only for a fully valid production signed envelope from the reviewed producer/root;
- production exactness can clear its unavailable status only for the exact carrier artifact, exact harness build, pinned witness suite, and exact measurement grid identity;
- absence, ambiguity, unsupported hardware, incomplete evidence, signature/root failure, custody-policy failure, or join mismatch remains red;
- no caller Boolean, label, self-hash, or outer receipt repair may bypass recomputation.

Add one connected BUILD integration fixture that exercises the complete authority graph without making provider/model calls or running the scientific experiment. Clearly label simulated/fixture evidence and ensure it cannot cross production admission.

## Development method and required tests

Use red/green TDD. Before implementing each authority path, add named positive and adversarial witnesses that fail on the current baseline for the intended reason.

At minimum add tests for:

### State authority

- exact production receipt positive path using a test-only adapter/root;
- fixture receipt rejected by production admission;
- self-authored signer/root injection;
- signer and trust-root editor not disjoint;
- writer-owned readback masquerading as independent readback;
- wrong store/namespace/version/transaction;
- stale or future cut;
- proposal/child/event-ID/sequence substitution;
- prestate/poststate substitution with every attacker-controlled hash repaired;
- receipt replay across scope, transaction, subject, or run;
- crash before commit, after partial persistence, and before readback;
- independent reducer disagreement remains fatal.

### Windows/measurement authority

- exact ABI size and field-offset tests using authoritative Windows structures;
- ordinary child exit with `TotalTerminatedProcesses == 0` accepted at the Job-accounting gate;
- nonzero limit-violation termination rejected;
- missing descendant or PID-reuse/start-key substitution;
- breakaway, network, broker, preexisting-helper, and external-worker attempts;
- final-query ordering and active-process race;
- completion-message loss remains diagnostic;
- raw query/scalar mismatch;
- ETW source unavailable, wrong event attachment, multiplexing, conflict, counter wrap/error, loss, or incomplete thread attribution;
- candidate/carrier artifact, harness build, host/environment, cell, run, key, role, policy, or grid replay;
- self-authored production root and fixture-to-production relabel;
- signer/root-editor custody collision;
- malformed evidence returns a closed error instead of throwing unexpectedly.

### Compatibility and integration

- all 145 frozen r13.2 tests still pass;
- all 61 governed r13.2 witnesses remain mapped and green;
- all new BUILD witnesses have two-way repair-ledger coverage;
- strict Draft 2020-12 schemas compile;
- JSON and canonicalization parity holds across Python/Node/production implementation boundaries;
- clean-room reconstruction from pinned or committed artifacts succeeds;
- tests prove no experiment, provider, route, paid, or 100-cell execution occurred.

Run deterministic unit/integration tests, schema validation, compilation, static analysis, and fixture-only conformance freely. A real production signing ceremony, real production trust-root activation, actual candidate physical execution, ETW/Job smoke run, 100-cell grid, route qualification, or scientific calls require a separate explicit owner authorization after BUILD review.

## Explicit prohibitions

Do not:

- run the MBCX-01 scientific experiment;
- make provider/model calls for experiment evidence;
- spend credits or money;
- run 4,608 scientific calls;
- run the 456 route-qualification trials;
- run the physical 100-cell grid;
- activate a production trust root or signing ceremony;
- create or expose production private keys;
- convert fixture evidence into production evidence;
- weaken a sentinel or error merely to obtain green tests;
- change the estimand, sample size, route math, inference, episode shape, or stop order;
- edit frozen r13.2 subjects in place;
- delete or stage the owner's unrelated/untracked files.

If real physical execution is needed to finish validation, stop after the implementation is reviewable and request a separate, bounded authorization naming the exact binary, host, cells, evidence destination, cleanup, and expected side effects.

## Work products

Produce:

1. versioned production state-adapter implementation and closed schema/contract;
2. versioned Windows Job/ETW producer implementation and closed schema/contract;
3. production verification adapters that preserve the fixture/production boundary;
4. configuration templates with no secrets;
5. trust-root and key-custody ceremony specification, including role separation, validity, revocation, and audit evidence;
6. carrier-exactness production-verifier specification/implementation;
7. positive/adversarial test suites and repair-ledger entries;
8. deterministic BUILD verifier and clean-room pin/reconstruction script;
9. BUILD shelf/prior-art log with exact sources and adoption decisions;
10. operator runbook for later authorized smoke testing and cleanup;
11. a concise senior completion handoff naming exact commits, files, test results, remaining unavailable statuses, and the precise next authorization needed.

Keep commits narrow and intentional. Recommended checkpoints are:

1. state-adapter red witnesses;
2. state adapter + verifier green;
3. Windows producer red witnesses;
4. Windows producer + verifier green under fixture/simulated tests;
5. connected integration and clean-room verifier;
6. documentation, custody ceremony, and operator runbook.

Do not push, open a PR, or activate external systems unless the owner explicitly asks.

## Definition of done for this coding task

The task is complete only when:

- both production artifacts are implemented as reviewable code;
- the current r13.2 suite remains green;
- every new authority claim has an executed positive and adversarial witness;
- fixture evidence still cannot create production/scientific authority;
- absent real roots/hardware/execution still fails loudly;
- no experiment or physical/scientific run occurred;
- the implementation is pinned to exact commits/artifacts and reconstructs cleanly;
- the remaining step is a separately authorized BUILD acceptance/smoke review, not another conceptual design round.

Lead your final response with what is actually built and verified. Distinguish `IMPLEMENTED`, `FIXTURE-EXECUTED`, `STATICALLY VERIFIED`, `PRODUCTION-UNAVAILABLE`, and `NOT RUN`. Name blockers plainly. Do not call the harness production-ready merely because fixture tests pass.
