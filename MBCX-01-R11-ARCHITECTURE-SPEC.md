# MBCX-01 r11 seam-closure architecture

Status: proposed governing design for no-paid verification  
Scope: one writer, one immutable experiment scope, one frozen model/route, one serial A0→B→writer→cold-A1 episode  
Non-scope: concurrent writers, coordination-stage behavior, provider/model evidence, paid calls, production readiness

## 1. Design decision

r11 keeps the experiment and repairs the joins. No larger scientific sample is authorized. The design owns all runtime semantics in r11 modules and treats historical artifacts as evidence, not executable substrate.

The dependency direction is:

```text
r11 contracts
  ├─ state reference reducer
  ├─ independently structured state oracle
  ├─ packet/DAG/scorer implementation
  ├─ cohort/provenance implementation
  ├─ physical-receipt evaluator
  └─ inference/missingness/route kernels

normative verifier → every implementation above + every repair-ledger witness
```

No r11 module imports an `r8`, `r9` or `r10` Python module.

## 2. State and identity

Every event ID is `EV.` plus uppercase SHA-256 over canonical JSON of the entire envelope without `event_id`. Schema-valid but noncanonical IDs fail with byte-identical state.

A fact row is visible/effective at cut `c` iff its assertion is known by the cut, no retraction event is known by the cut, `valid_from <= c.valid_time`, and `c.valid_time` precedes the earliest correction closure known by that cut (or the assertion's static upper bound). Correction and retraction evidence is append-only; later events never mutate an old row, so an old journal/knowledge cut keeps the answer it had when that cut existed.

Fact intervals are half-open and nonempty. Every new event must originate at the exact current journal-and-knowledge cut; exact replay is the sole exception. Corrections target the unique visible/effective unsuperseded version at that cut. `correction.valid_from` must be strictly inside the parent's interval; the correction event records the parent's cut-relative closure and the child inherits the parent's former upper bound unless an earlier explicit child bound is supplied. Assertions and corrections compute their complete proposed interval first and reject overlap with every currently known, unsuperseded interval. A future-effective version therefore does not block a disjoint current interval and supplies the inferred boundary only when the new assertion did not author an explicit `valid_to`; an authored interval is never silently truncated. No effect may create overlap or `valid_to <= valid_from`.

`record_call_response` binds `handoff_id`, scope, scenario, condition, node, task packet hash, exact served request SHA-256, request-parameters hash, idempotency token, raw response bytes and SHA-384, parsed worker-handoff SHA-384, immutable response reference, provider request ID, transaction/fsync durability receipt and route-contract hash. The one canonical durability receipt schema binds the full call-ledger identity, raw bytes hash, response/provider references and transaction and is consumed unchanged by packet, state and restart-ledger code. Recording is legal only after the exact same-scope handoff is open. Distinct response events remain distinct rows, and every response reference, provider ID and transaction ID is globally single-use even when bytes happen to match. `propose_handoff_result` succeeds only when exactly one durable row matches the open handoff's complete B identity. Commit rechecks the current target and rejects a stale proposal if the obligation changed after proposal. Rejection likewise requires an exact stored proposal hash; an open/no-response handoff cannot manufacture a rejected proposal.

Shared structural schema validation is allowed. The reference reducer and oracle must implement post-ingress guards and effects separately and agree over registered legal/illegal traces.

## 3. Typed causal packet graph

Each condition has the following distinct identities:

```text
ExpectedScenarioManifestV2
  └─ DecisionPacketV5(A0_PRECOMMIT)
       └─ exact served bytes SHA-256
            └─ A0ResultV3 + DurableCallRecordV1(A0)
                 └─ TaskPacketV1(B)
                      └─ exact served bytes SHA-256
                           └─ WorkerHandoffV5 + DurableCallRecordV1(B)
                                └─ WriterReceiptV2 + exact child event bytes
                                     └─ DecisionPacketV5(A1_POSTCOMMIT)
                                          └─ exact served bytes SHA-256
                                               └─ A1ResultV3 + DurableCallRecordV1(A1)
                                                    └─ ScorerInputV1
```

The expected manifest binds the candidate selector ID, exact BC selected object IDs/hash, gold read set, canonical world, action universe, unique recomputed A0/B gold action and the expected postcommit A1 actions. BC and OM builders accept no free object-selection argument: they consume only the bound manifest fields.

The scorer first performs structural admission for the composite and every nested object. It then recomputes manifest, object, packet, TaskPacket, served-byte, result, raw-response, receipt, child-event and postcommit-state hashes. The writer receipt carries the exact applied `commit_handoff_result` event bytes and the resulting current cut; the A1 packet must use that postcommit cut. The state handoff carries canonical TaskPacket and manifest preimages, independently recomputes both object hashes, and requires the TaskPacket requested-catalog hash, manifest catalog/hash and supplied state catalog to identify the same full bytes, not adapted subsets. It rejects unavailable actions, invented children, cross-scenario records, a precommit A1 packet, worker production after B acceptance, reused call/receipt identities, arbitrary common packet hashes and any extra field. Only then may it compute the exact binary condition score.

## 4. Cohort provenance

The source provenance manifest binds the content digest of `MBCX-01-R11-SYNTHETIC-COHORT-GENERATOR.json` and, for every scenario, its motif, complete cut-ID set/hash, canonical cut/state authority, gold map and complete action-universe hash. Selection validates the whole source before choosing a cut. The selector exposes no domain override: the one-cut and retention domains are read from the current measurement contract. Motif labels, cuts, state and action universes are authority data, not candidate-supplied hints.

## 5. Physical receipt

Every row belongs to one candidate ID and one generator digest across all 100 cells. H, D and F are exact non-Boolean integers from the registered axes.

Each row carries an OS-produced receipt binding:

- named Job Object identity and candidate process identity;
- root creation suspended, completion-port association and job assignment before resume;
- neither breakaway flag enabled;
- active-process-zero plus final `QueryInformationJobObject` collection;
- job-wide user/kernel CPU time, read/write/other operation counts and transferred bytes, peak committed memory, and monotonic elapsed nanoseconds;
- root/descendant retired instructions from one pinned backend with process attribution semantics;
- network egress denied and no external compute, or an explicit `EXTERNAL_WORK_UNMEASURED` failure.

The evaluator rejects missing, spliced or Boolean-poisoned receipts before boundedness/affordability evaluation. The r11 repository does not yet contain the required Windows Job/ETW harness or an external receipt-signing trust root. Its baseline rows are synthetic evaluator fixtures only. The no-paid verifier must therefore report `PHYSICAL_HARNESS_UNAVAILABLE` and the top-level design gate remains closed; synthetic rows cannot create a physical PASS.

## 6. Durable call ledger

Preparation requires nonempty, pattern-valid scenario/condition/node identity, TaskPacket hash, exact served-request SHA-256, request-parameters SHA-384, idempotency token and route-contract SHA-384. Every transition returns an immutable snapshot with a content digest.

`RESPONSE_BYTES_FSYNCED` requires raw response bytes, their SHA-384, immutable response reference, provider request ID and the same canonical `DurabilityReceiptV1` consumed by the packet scorer and state reducer. Recovery accepts only a serialized snapshot whose digest and nested response/durability digests all verify. A label-only preaccept receipt never authorizes retry; the only ambiguous retry edge requires the structured exact-route attestation below.

An ambiguous retry requires a structured route attestation whose digest matches the frozen route contract and whose declared semantics bind the identical idempotency token to identical request parameters. A Boolean cannot authorize retry.

## 7. Inference and missingness

The exact-mixture confidence-sequence implementation and exact missing-completion DP are retained in an r11-owned module. The exhaustive cross-check is explicitly limited to at most seven missing pairs; the DP itself has no missing-count ceiling. Both complete and missing-data entry points consume the frozen SHA-256 scenario order and reject Python Booleans as outcomes. `design_ok` is an exact Boolean, so a truthy string cannot bypass the highest-precedence design gate.

Decision precedence is:

1. `DESIGN_OR_IMPLEMENTATION_FAIL`
2. `TRANSPORT_INCONCLUSIVE`
3. `MODEL_OR_INTERFACE_CEILING`
4. `MODEL_INTERFACE_FAIL`
5. `PROMOTE_TO_COORDINATION_STAGE`
6. `INCONCLUSIVE_OR_UNDERFUNDED`

The scientific run remains 768 pairs. The frozen 10,000-replicate counter-stream outputs are reported only as deterministic planning frequencies for explicitly registered joint `(p00,p01,p10,p11)` cells. They are not called true-probability lower bounds, and no rectangular region-wide promise is made. The r10 counterexample `(0,.3,.1,.6)` remains a published diagnostic, including its substantial non-interface-fail frequency, rather than being hidden by narrowing the claim.

## 8. Route qualification without an iid claim

The frozen schedule contains 456 complete six-call trials allocated by a committed counter-stream permutation across declared UTC windows. Endpoint, model snapshot, auth path, transport settings and retry policy are identical to the contemplated scientific run. Any drift invalidates qualification.

Let `F_i` be trial-i failure and `H_{i-1}` the entire observed past.

- Bad-route hypothesis: `P(F_i=1 | H_{i-1}) >= 0.02` almost surely for every scheduled trial.
- Good-route hypothesis: `P(F_i=1 | H_{i-1}) <= 0.005` almost surely for every scheduled trial.

For the finite 456-trial horizon, backward conditional-expectation recursion shows that each history's lower-tail acceptance value is monotone in its next conditional failure probability. The bad-route maximum acceptance is therefore attained at `.02` at every history, and the good-route minimum acceptance at `.005` at every history. This produces the same binomial CDF values without assuming iid trials or requiring regular conditional kernels on an arbitrary full-history probability space: bad-route acceptance is at most `0.049433329807588314`; good-route acceptance is at least `0.9190668746549462`, so good-route rejection is at most `0.08093312534505381`.

The schedule defines the claim window; it does not prove either hazard hypothesis or future stationarity. An aborted, incomplete or unclassified launched trial counts as a failure, no trial is replaced, acceptance cannot occur before all 456 trials, and rejection may occur on the fifth failure. Intermediate or history-dependent hazards that cross the two stated bounds receive no guarantee.

This is an engineering qualification claim, not scientific evidence and not proof of future route stationarity.

## 9. Reconstruction and repair retention

The Ajv validator is a single vendored deterministic bundle and a governed subject. No absolute external `node_modules` path is used. Its registered UTC format performs calendar/range validation in addition to the lexical pattern, matching Python admission on impossible dates and times.

The council packet pins the governing commit, manifest blob and launcher blob. The prescribed bootstrap extracts the launcher from its pinned Git blob before execution; it never executes the working-tree launcher first.

`MBCX-01-R11-REPAIR-LEDGER.json` maps every adopted repair token to one or more executable witness IDs. Verification fails if a token lacks a passing witness or a reported witness lacks a ledger entry.

## 10. Stop conditions

No route/model/provider call may occur until r11 receives a council go, the owner separately freezes endpoint/model/pricing/token/retry/dollar ceilings, and the deterministic stages pass. The r11 packet is prepared but not dispatched while any council seat is unavailable.
