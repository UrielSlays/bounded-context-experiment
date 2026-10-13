# MBCX-01 Targeted Closure Confirmation Packet r13.2

## 0. Command, seal, and immutable bundle

You are one longitudinal Moonwalker council seat confirming the three bounded repairs requested by the r13.1 council. Read `<vault>`, then adjudicate repository `<repo>` read-only.

Maintain the lateral seal. Do not inspect another seat's r13.2 chat, output, log, completion marker, or verdict. Your own earlier lane context and r13.1 finding are allowed and must be labeled.

Governing implementation commit: `d97d654e21918450994cfddb5a53dc5da2e962bb`

Pin-manifest Git blob: `407a1cd73197af7dbad767976f5c077d91986c87`

Pinned reconstruction-launcher blob: `1bb8c15d1fd14303fa0a10fa615a881cb65e0d96`

Authenticate and execute the pinned launcher, never a working-tree substitute:

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r13.2-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','1bb8c15d1fd14303fa0a10fa615a881cb65e0d96') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git hash-object -- $launcher).Trim() -ne '1bb8c15d1fd14303fa0a10fa615a881cb65e0d96') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit d97d654e21918450994cfddb5a53dc5da2e962bb -ManifestBlob 407a1cd73197af7dbad767976f5c077d91986c87
```

The manifest has 34 exact subjects. Both the live tree and clean Git-object reconstruction pass 145 unit tests, 61 governed repair witnesses, strict Draft 2020-12 AJV admission, all 768 retained-source joins, and the connected pipeline. The report says `experiment_executed:false`, `provider_calls:0`, `paid_calls:0`, and `physical_harness_executed:false`.

Do not edit files. Do not run the experiment, a physical harness, route qualification, provider/model calls, the 100-cell physical grid, or either future production adapter. Deterministic read-only reconstruction and fresh no-paid attacks are authorized.

## 1. Scope and stop rule

This is not r14 and not another open-ended design round. Opus returned `GO` at r13.1. The two OpenAI seats returned bounded fixes, not a conceptual `NO-GO`. r13.2 folds exactly their three controlling findings. Confirm only whether those repairs are closed in the pinned bytes and whether conceptual council rounds may stop.

Do not reopen the estimand, n=768, six-call episode, 456/4 conditional-hazard route gate, inference method, physical grid, three-stage stop order, or unrelated r13 machinery unless this delta creates a newly demonstrated reachable false result.

Read first:

- your own r13.1 verdict or longitudinal context;
- `MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json`;
- `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`, especially I10, I12, and I16;
- `MBCX-01-PACKET-SCHEMAS-v7.json` and `mbcx01_r13_packets.py`;
- `MBCX-01-MEASUREMENT-CONTRACT-v7.json` and `mbcx01_r13_measurement.py`;
- `mbcx01_r13_inference.py`, the three changed test modules, the repair ledger, and the pinned exactness suite.

## 2. C1 — exact EpisodeReceipt-to-outcome authority join

`ScenarioOutcomeReceiptV2` now carries the exact `episode_hash` and six ordered `call_bindings` (`BC.A0`, `BC.B`, `BC.A1`, `OM.A0`, `OM.B`, `OM.A1`). For every slot, validation recovers the corresponding `CallLedgerV3` and requires equality of the full call identity, raw response bytes/hash/reference, provider request identity, complete durability receipt, and call-record hash before recomputing BC/OM. Inference maps each retained scenario to exactly one EpisodeReceipt and rejects naked, missing, noncomplete, or alternate-episode outcomes.

Required fresh attack: build two independently valid complete episodes for the same retained scenario whose scorer graphs yield different outcomes. Repair every local descendant hash. An outcome derived from episode B must not validate against episode A or change inference over A. State the exact rejection.

Named witnesses include:

- `test_i10_adversarial_outcome_graph_must_equal_the_exact_episode_ledgers`
- `test_i10_adversarial_same_scenario_outcome_from_another_episode_is_rejected`

## 3. C2 — correct Windows TotalTerminatedProcesses semantics

The 96-byte Job Basic+I/O record remains four `LARGE_INTEGER`, four `DWORD`, then six `ULONGLONG`. The fourth DWORD, `TotalTerminatedProcesses`, is now treated as the count of processes terminated because of a Job limit violation—not the count of ordinary process exits. A clean accepted cell requires it to be zero. Normal completion is proved separately by signed PID/start-key terminal lifetimes plus the final query's `ActiveProcesses == 0`; completion-port notifications remain diagnostic.

Required fresh attacks:

1. A bounded clean run with one normal child exit, final `ActiveProcesses == 0`, terminal lifetime evidence, and `TotalTerminatedProcesses == 0` must pass this gate.
2. The same otherwise valid evidence with nonzero `TotalTerminatedProcesses` must fail as a Job-limit-violation termination.

Re-open the controlling Microsoft primary source rather than trusting packet prose: `https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information`.

Named witness: `test_i12_normal_exit_does_not_require_a_limit_violation_termination`.

## 4. C3 — carrier exactness authority and exact-build binding

`CarrierExactnessReceiptV2` replaces the self-authorable V1 shape. It binds the candidate, signed `candidate_artifact_digest`, exact 100-cell `measurement_grid_identity_hash`, pinned suite artifact/hash, pinned witness-set hash, fixture producer, and fixture trust-root policy. `MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json` is an exact pinned, fixture-only suite descriptor. r13.2 has no production activation path: relabeling a fixture receipt cannot grant authority, and production admission fails `CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE` until the separate physical BUILD supplies real authority.

Required fresh attacks:

1. Self-author an internally hashed `PASS`, alter the suite/witness digest, or flip `authority_mode` to production. It must fail.
2. Replay a valid fixture exactness receipt across a different carrier/candidate artifact digest, harness identity, or full-grid identity while repairing outer hashes. It must fail.

Named witnesses include:

- `test_i16_adversarial_self_authored_exactness_pass_has_no_authority`
- `test_i16_adversarial_exactness_receipt_cannot_replay_across_builds`

## 5. Honest residual and required verdict

The top-level readiness intentionally remains `DESIGN_OR_IMPLEMENTATION_FAIL` only because `STATE_AUTHORITY_UNAVAILABLE` and `PHYSICAL_HARNESS_UNAVAILABLE` are still true. That is the published BUILD boundary, not a hidden experiment result. A confirmation authorizes only moving to separately reviewed implementation of those two production artifacts. It does not authorize provider calls, route trials, physical trials, the 4,608 scientific calls, or spending.

Return one compact self-contained report with:

1. `CONFIRMED`, `NOT-CONFIRMED(C1|C2|C3: reason)`, or `UNDERDETERMINED(reason)`;
2. seat/model/checkpoint/harness and longitudinal posture;
3. exact pin/reconstruction result and side effects;
4. a C1/C2/C3 scoreboard (`HOLDS`, `FALSE`, or `UNDERDETERMINED`) with the fresh attack and exact observed rejection/pass;
5. any P0-P3 finding with exact file/function, reachable consequence, and smallest bounded fix;
6. direct answers: are the three r13.1 fixes actually closed, can conceptual council rounds stop, and is the next authorized step BUILD rather than experiment execution?

Do not soften a real failure. Equally, do not manufacture a new numbered round from an unrelated preference. If all three attacks hold, say `CONFIRMED` plainly.
