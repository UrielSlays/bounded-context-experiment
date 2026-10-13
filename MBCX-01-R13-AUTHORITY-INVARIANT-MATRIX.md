# MBCX-01 r13 Authority Invariant Matrix

Status: normative closure map, r13.2 targeted council closure

## 1. Rule

Every row represents one fact expressed in two places. Both sides may be structurally valid alone. The join is valid only when the listed equality is mechanically reproduced from independently admitted inputs. Each row requires a positive witness and an adversarial witness that keeps both sides locally valid while changing the shared truth.

| ID | Truth A | Truth B | Required mechanical equality | Positive witness | Adversarial witness | Failure |
|---|---|---|---|---|---|---|
| I01 | Pinned source + exact retained population | ExpectedScenarioManifest | `RetainedScenarioAuthorityV2` carries the full byte-exact candidate, source provenance, retained position and 768-set root; chosen cut/world/observation/gold/action universe equal the manifest | all 768 retained candidates independently resolve and join | a self-consistent nonmember candidate is rehashed | `RETAINED_SCENARIO_AUTHORITY_INVALID` |
| I02 | Exact manifest-cut state read | ExpectedScenarioManifest world | `ManifestCutStateReceiptV1` state bytes/hash, exact cut and canonical projection equal the source-bound manifest; the later proposal prestate is a separate receipt | exact manifest-cut and later precommit reads accepted | a legal same-cut state changes one obligation and is rehashed | `MANIFEST_CUT_STATE_MISMATCH` |
| I03 | A0 packet | ExpectedScenarioManifest | exact scope, cut, object projection, catalog bytes/hash and request contract | A0 built from admitted manifest | replace A0 object or cut and recompute packet hashes | `A0_MANIFEST_MISMATCH` |
| I04 | TaskPacket | A0 output | exact served A0 hash, requested action catalog, scenario/condition/node and request lineage | exact task accepted | substitute a valid TaskPacket from another A0 | `TASK_A0_MISMATCH` |
| I05 | B durable response | CallLedger durable terminal | exact scenario/condition/node, request hash, idempotency token, response bytes/hash/ref, provider request ID and transaction/receipt identity | six exact ledgers accepted | replay valid B response/receipt under another node or scenario | `B_LEDGER_MISMATCH` |
| I06 | Proposal | State-owner prestate journal | exact persisted proposal event ID, bytes, hash, scope, target, response FK, action IDs and originating cut | state-owner readback accepted | locally valid proposal not present in the receipt journal | `PROPOSAL_AUTHORITY_MISMATCH` |
| I07 | Commit child | Proposal and prestate | exact next event sequence, valid/effective time, target/action legality, proposal hash and prestate hash | both reducers apply exact child | jump sequence, stale prestate or alternate proposal | `COMMIT_AUTHORITY_MISMATCH` |
| I08 | Actual poststate | WriterReceipt | exact state bytes/hash, child bytes/hash, transaction/readback identity and postcommit cut | receipt derived from readback | recompute receipt over substituted poststate | `WRITER_POSTSTATE_MISMATCH` |
| I09 | Actual poststate | A1 packet | canonical poststate projection bytes/hash and recomputed due-action truth equal served A1 objects/gold | A1 built from admitted poststate | manifest-derived A1 disagrees with actual poststate | `A1_POSTSTATE_MISMATCH` |
| I10 | Episode schedule + exact call ledgers | Scientific partition and outcomes | every registered slot is a launched terminal ledger or an exact downstream `NOT_LAUNCHED_UPSTREAM_TERMINAL`; complete scenarios supply `ScenarioOutcomeReceiptV2`, whose episode hash and six ordered ledger/call-record bindings equal the BC/OM scorer graphs before bits are recomputed | derived ordered partition and exact episode-bound outcome accepted | caller supplies naked bits, omits ambiguity, claims a skipped call launched, or substitutes a same-scenario scorer graph from another episode | `EPISODE_PARTITION_MISMATCH` / `SCENARIO_OUTCOME_AUTHORITY_INVALID` |
| I11 | Physical requirements | Signed measurement schema | signed PID/start-key process and thread lifetimes, raw Job query bytes, raw PMC capability/attachment and CSwitch counter observations, environment, external enforcement and harness identity are representable | complete fixture schema validates but remains unavailable | signer omits or changes a lifetime/raw observation | `PHYSICAL_EVIDENCE_INCOMPLETE` / `INSTRUCTION_ACCOUNTING_INCOMPLETE` |
| I12 | Signed measurement schema | Evaluator | exact 64-bit Windows Job ABI (four `LARGE_INTEGER`, four `DWORD`, six `ULONGLONG`); `TotalTerminatedProcesses` means Job-limit-violation terminations and is zero for a clean normal exit; signed lifetimes plus final active zero prove membership completion; one full grid identity, final terminal barrier, and all gates are recomputed | bounded normal-exit grid has only unavailable sentinel | ABI offset, nonzero limit termination, grid identity, raw delta or load-bearing evidence changes | named evidence failure |
| I13 | Signed receipt | Trust root | signature, producer role, key class, run/cell, subject digest, environment and policy are bound to an independently configured root; signer cannot edit root | fixture conformance only | inject real key/root or flip production flag | `MEASUREMENT_TRUST_ROOT_INVALID` / unavailable |
| I14 | State authority receipt | State trust root | store/namespace/version, transaction/commit/readback and subject hashes bind to independently configured state-owner identity | fixture conformance only | packet builder self-signs/injects its root | `STATE_AUTHORITY_UNAVAILABLE` |
| I15 | Reference reducer | Oracle reducer | same admitted event yields byte-identical result/state while replay, persistence, sequencing and effects are independently implemented | full 17-event matrix | poison either engine's finalization/effects; other must disagree | `REDUCER_DIVERGENCE` |
| I16 | Signed exactness + measurement evidence | Engineering selection | `CarrierExactnessReceiptV2` binds the pinned suite/witness set, exact carrier artifact digest and exact measured grid identity; fixture mode cannot activate production. `EngineeringCandidateEvidenceV1` then derives gates and worst-cell metrics before frozen Pareto comparison | pinned fixture exactness plus its exact grid yields the expected nondominated set | caller substitutes a metric/Boolean, self-authors PASS, flips production mode, replays across another build, or adds owner preference | `ENGINEERING_SELECTION_INVALID` / `CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE` |
| I17 | Authenticated verifier run | Any retained report | report is produced from or byte-compared to the current authenticated run; otherwise it is nonnormative | fresh output matches | stale schema ID/numbers with green reconstruction | `REPORT_FRESHNESS_INVALID` |

## 2. Canonical world projection

`CanonicalExperimentWorldV1` is a closed, sorted projection of one scope at one exact bitemporal cut:

- schema/domain/version;
- scope ID and exact cut;
- all visible obligation IDs with subject, owner role, lifecycle, due time, critical flag and sorted prerequisite IDs;
- all visible fact IDs/keys/values and valid intervals used by the scenario;
- full legal action catalog and its hash;
- due, unblocked expected action IDs recomputed from the projection;
- projection hash over the complete canonical preimage.

The projection is computed from authoritative state. A manifest may carry the projection but may not define a conflicting one. A1 is projected from authoritative poststate, never from expected gold.

## 3. Authority modes

- `FIXTURE_ONLY`: may test parsers, signatures, reducers and join logic; cannot create an experiment-eligible score or physical pass.
- `PRODUCTION`: requires an independently configured state-owner or measurement trust root, producer role, custody policy, exact subject identity and sentinel retirement approval. No r13 fixture implements this mode.

Until the respective production boundary exists, the machine returns `STATE_AUTHORITY_UNAVAILABLE` or `PHYSICAL_HARNESS_UNAVAILABLE`.

## 4. Episode derivation

For each frozen scenario, an `EpisodeReceiptV1` binds exactly six nodes in registered order: BC A0/B/A1 and OM A0/B/A1. The receipt is derived from authenticated call ledgers, not caller-supplied outcome arrays.

- complete: six durable terminals and all packet/response identities join;
- whole-pair missing: any node is terminally ambiguous or otherwise lacks an admissible durable terminal;
- invalid: duplicate/missing node, cross-scenario identity, mutable response reference, or caller partition disagreement.

Inference consumes the manifest plus episode receipts and derives its ordered observed/missing streams internally.
For a complete scenario, `ScenarioOutcomeReceiptV2` additionally names the exact
episode hash and six ordered `{position, ledger_hash, call_record_hash}` joins. A
same-scenario scorer graph from another valid episode therefore cannot change the
decision under the original episode receipts.

## 5. Engineering decision

Candidates first pass exactness, accounting completeness, finite H-shape boundedness and absolute affordability. Failed candidates are never ranked.

Exactness is not a caller Boolean. The receipt is admitted only when its suite
artifact and witness-set hashes equal the pinned exactness suite, its carrier
artifact digest equals every signed cell, and its full-grid identity equals the
measurement evidence. The fixture receipt proves verifier conformance only; the
future physical BUILD owns production exactness authority.

For each survivor, compute the preregistered worst-cell vector:

1. retired instructions;
2. aggregate user+kernel CPU ns;
3. monotonic elapsed ns;
4. peak committed bytes;
5. total I/O transfer bytes;
6. total I/O operations.

Candidate X dominates Y only if X is no worse on every coordinate and strictly better on at least one. Report the complete nondominated set. If it contains more than one carrier, the result is `OWNER_SELECTION_REQUIRED`; any later owner preference is policy, not experimental evidence.

## 6. Completion condition

Closure is green only if all seventeen rows are exercised in the authenticated verifier and the repair ledger maps every row to its positive and adversarial witness in both directions.
