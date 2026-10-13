NO-GO

Verdict basis: EXECUTED. I read the round-4 packet at de49049c92c53f9bde7c6ba7451d4a84e1c814d9 and reviewed the executable target at 4c7056e524b16a8b0395d8853f71e4a9ac6982fc. I used the working tree for test/probe execution only after confirming that 4c7056e… → de49049… changes only the round-4 packet and has no .py / .ps1 differences. The remaining untracked files were other-seat artifacts; I did not open them. The committed suite is broadly healthy, but I found independent executable failures in the frozen state-binding invariant, the new ETW consumer, the flagged-constant doctrine, and the still-open production-signing-key gap. Any one of the first two is enough to withhold BUILD acceptance.

## Evidence read

- MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r4.md:13-32,45-69,78-98,105-183,195-257,259-305@de49049
- MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:7-40@4c7056e
- mbcx01_r13_packets.py:68-100,500-545,1270-1410@4c7056e
- mbcx01_r13_measurement.py:831-879,1370-1545@4c7056e
- mbcx01_r13_inference.py:130-215@4c7056e
- mbcx01_build_etw_consumer.py:81-222,853-1010,1288-1336,1495-1545,1645-1873@4c7056e
- mbcx01_build_win32.py:615-800,840-887@4c7056e
- mbcx01_build_windows_producer.py:342-415,433-519@4c7056e
- mbcx01_build_measurement_authority.py:735-765,790-925@4c7056e
- mbcx01_build_state_authority.py:750-825,900-1045@4c7056e
- mbcx01_build_exactness_authority.py:145-235@4c7056e
- mbcx01_build_trust_anchor.py:230-360,418-530,530-665@4c7056e
- MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:125-207@4c7056e
- MBCX-01-BUILD-SMOKE-RUNBOOK.md:1-112@4c7056e
- MBCX-01-OPEN-ISSUES.json:160-210@4c7056e
- the three BUILD test modules and frozen test_mbcx01_r13_*.py suites at the same pin

## WHY THIS EXISTS

1. **ALREADY-BUILT? — EXECUTED / SEARCHED.** The packet's internal-shelf log was non-vacuous; I independently spot-ran its ETW query over agentvault-mcp-bridge/src, Photon/crates, Gravity/src — all three returned zero files. Externally, Windows already supplies the Job Object, ETW, CSwitch, PMU and trace-control primitives this build composes; trust-root/current-time patterns have mature precedents (Go x509.VerifyOptions keeps roots and verification time in verifier-owned state). No reason to replace this experiment-specific authority/evidence composition wholesale.
2. **PRODUCT-FIT? — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES.** Yes: the customer need is a physical experiment result admitted only when its state, execution evidence, authority and provenance are mechanically defensible, otherwise it fails loudly. F1 violates that posture because the system silently fails to bind two fields the governing invariant says are part of the exact state.
3. **BIGGER-THAN-THE-BUG? — READ-ONLY.** No improper escalation. The ETW consumer exists because the collector had an explicitly unimplemented physical seam; legitimately subsystem-sized and brought through design/build review, not smuggled in as a leaf fix. The problem is not that it was built; the pinned implementation is not acceptance-ready.

## Execution record

- `python -m unittest test_mbcx01_build_measurement test_mbcx01_build_state test_mbcx01_build_integration` → 114 tests, OK
- `python -m unittest discover -s . -p 'test_mbcx01_r13_*.py'` → 145 tests, OK
- `python verify-build-bundle.py` → exit 0; seven sections PASS; ledger 44 invariants / 114 witnesses / two_way_total=true; readiness BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED
- Deliberate in-memory breaks of one public authority path each for measurement, state, exactness → targeted witness RED in each case. Q8 passes.

## SWEEP LOG

Queries run: PMU/TracePmcEventListInfo/CSwitch/InstructionRetired · job objects QueryInformationJobObject/JobObjectBasicProcessIdList/AssignProcessToJobObject · ControlTraceW EVENT_TRACE_CONTROL_QUERY/STOP · go.dev crypto x509 VerifyOptions CurrentTime Roots · "Recording Hardware Performance (PMU) Events" · "Thread_V2" ProcessId ETW · theupdateframework.io root keys out of band · cwe.mitre.org CWE-1291.

Opened at origin (deciding sections noted):
- Microsoft Learn AssignProcessToJobObject / QueryInformationJobObject / JOBOBJECT_BASIC_PROCESS_ID_LIST / Job Objects — assignment semantics, child inheritance/breakaway, JobObjectBasicProcessIdList. Job membership is an OS-owned fact and Windows exposes a direct process-list query.
- Microsoft Learn ControlTraceW — ControlCode: QUERY retrieves session statistics; STOP stops the session and leaves the session handle invalid. This turned Q5 from suspicion into a concrete lifecycle contradiction.
- Microsoft Learn EVENT_HEADER_EXTENDED_DATA_ITEM / Recording PMU Events / CSwitch — PMC counters carry current counter values; PMU values may be logged on CSwitch; OldThreadId is the outgoing thread.
- Go crypto/x509/verify.go — Roots is verifier configuration; CurrentTime is verifier-owned, defaults to real current time when zero. Confirms Q4's adopted pattern.
- TUF Roles and metadata + FAQ — root metadata, role keys/thresholds, expiration, out-of-band initial root. Independently established root plus separated role keys is mature prior art.
- MITRE CWE-1291 — supports the test/production key-reuse footgun class.

Stopped because these primaries settled the load-bearing Windows semantics, verifier-clock pattern, trust-root pattern and key-reuse class; further source-counting would not change the deciding local-byte findings.

## Findings

### F1 — EXECUTED — I02 silently underbinds the canonical experiment world — DECIDING
UNSEARCHED — SETTLED-BY-PINNED-BYTES.

MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:31-39 says CanonicalExperimentWorldV1 contains every visible obligation's subject, owner role, lifecycle, due time, critical flag and prerequisites. I02 (line 12) says a legal same-cut obligation change must yield MANIFEST_CUT_STATE_MISMATCH.

mbcx01_r13_packets.py:83-87 projects only lifecycle, critical, due_at, completion_action_id, prerequisite_obligation_ids. It does not project subject_id or owner_role.

Fresh probe: started from a valid OM scoring fixture; changed OBL.DECOY.owner_role to ROLE.FRESH.ADVERSARY; recomputed state_utf8, state hash, projected world/hash and receipt hash through the pinned implementation; called the pinned manifest-cut validator and invariant matrix.

```
validate_manifest_cut_state_receipt(...) -> []
I02 -> True
score_fixture_conformance_exact(...) -> 1
```

The banked I02 red witness changes `critical`, which happens to be one of the fields the reduced projection includes, so it does not close the field-omission class. Two states the DoR says are observably different are treated as the same canonical experiment world.

Fix class: CANONICAL_EXPERIMENT_WORLD_PROJECTION_COMPLETENESS / I02_STATE_BINDING. Changes an invariant consumer ⇒ fresh council required.

### F2 — EXECUTED — live ETW thread identity cannot satisfy its own lifetime join — DECIDING
SEARCHED. mbcx01_build_etw_consumer.py:1824-1833 decodes every ThreadStart/ThreadStop with `process_start_key = None`, but assemble_thread_lifetimes() at :937-966 canonicalizes that field and requires the (process_id, process_start_key) pair to exist in the signed process-member map.

```
decoded thread event: process_id=1234 thread_id=5678 process_start_key=None
assemble_thread_lifetimes(...) -> EtwConsumerFault: ETW_PROCESS_START_KEY_INVALID:None
```

Not a security bypass and it fails loudly — worse for acceptance in a simpler way: the newly added live consumer cannot complete the thread-lifetime join its contract requires. Microsoft documents process-start-key as a distinct 64-bit extended-data item when enabled, compatible with the consumer needing to capture/bind that identity rather than manufacture None.

Fix class: ETW_THREAD_IDENTITY_JOIN.

### F3 — EXECUTED — ETW finalization asks for loss statistics after it has stopped the session — DECIDING
SEARCHED. The production factory finalizer at :1308-1313 does `loss = consumer.stop()` then `capture = consumer.capture()`. stop() at :1513-1536 queries loss counters then sends EVENT_TRACE_CONTROL_STOP. capture() at :1857-1870 calls _query_loss() again. ControlTraceW's contract: QUERY retrieves statistics, STOP stops the session and the handle is no longer valid.

```
pre-stop QUERY -> success
STOP -> success
capture() -> second QUERY after stop -> ERROR_WMI_INSTANCE_NOT_FOUND -> EtwConsumerFault
```

The pinned control flow contradicts the session lifecycle it calls. Fails loudly rather than signing degraded evidence, but makes the physical consumer nonfunctional as wired.

Fix class: ETW_SESSION_LIFECYCLE / LOSS_CAPTURE_SEQUENCING.

### F4 — EXECUTED — Q9 gap #2 is reachable: a committed test signing pair can authorize production-shaped measurement evidence
SEARCHED. test_mbcx01_build_measurement.py:74-84 contains a committed Ed25519 private/public signing pair; :180-241 constructs a production_ready:true, fixture_only:false production-shaped trust-root manifest using that committed public half; custody documents at :147-170 assert private_key_never_leaves_custody: True; the positive production-shaped grid is signed by the corresponding committed private key at :387-404.

Fresh probe kept the owner/root anchor independent and newly generated in memory, then used the committed test signing pair as the production measurement signing root:

```
root_fixture_only = False
production_ready = True
root_is_committed_test_public = True
custody_claim_private_never_left = True
production_admission_errors = []
```

MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:168-177 correctly says each production signing key must be newly generated in custody and never copied from fixture material, but the mechanical admission path does not enforce it for this signing-key class. Q9's own rule resolves to reachable ⇒ must close before ceremony.

Gap #1 — disclosure sufficient: FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM cannot authenticate owner activation merely by existing; banked wrong-signer probes refuse it. Gap #3 — disclosure sufficient: the OS-config committed-anchor path raises a named PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL exception; exception-versus-code is interface ergonomics, not an authority bypass.

Fix class for gap #2: PRODUCTION_SIGNING_KEY_FIXTURE_ISOLATION / CEREMONY_PRECHECK.

### F5 — EXECUTED + READ-ONLY — Q6's "wrong unpublished values fault loudly and are all in the smoke verification set" claim is false
SEARCHED. The source marks many values unpublished/FLAGGED (WNODE_FLAG_TRACED_GUID :94-101; EVENT_TRACE_CONTROL_* :127-136; PROCESS_TRACE_MODE_* :138-148; EVENT_HEADER_* :150-175; Kernel-Process GUID/keywords/event IDs :193-210; provider enable/control properties :212-222), but MBCX-01-BUILD-SMOKE-RUNBOOK.md:85-106 enumerates a much smaller physical-verification set and does not include them.

More importantly, "a wrong value faults loudly" is not true by construction for the ControlTrace class. I changed only EVENT_TRACE_CONTROL_QUERY in memory from the QUERY code to the valid STOP code, with a fake API obeying the real state machine:

```
wrong QUERY ordinal invoked actual STOP
_query_loss() returned EventsLost=0 LogBuffersLost=0 RealTimeBuffersLost=0
session_still_running = False
```

No fault: a wrong unverified ordinal aliased another valid operation and manufactured apparently clean zero-loss evidence. The currently pinned ordinal may be correct; that is not the claim under attack — Q6 claims protection against a future maintainer/platform-value mistake, and that protection is incomplete.

Fix class: FLAGGED_CONSTANT_VERIFICATION_SET_COMPLETENESS / NUMERIC-ALIAS FAIL-LOUDNESS.

### F6 — EXECUTED — the provisional "unrelated ETW process becomes signable Job work" bypass does NOT survive differential admission
UNSEARCHED — SETTLED-BY-PINNED-BYTES. Recorded because it was a plausible attack and the negative result matters. assemble_member_lifetimes() at :853-934 does label every supplied ProcessStart/Stop pair with the supplied Job ID and assigned_before_resume=True, so a synthetic stream containing the root plus an unrelated process produced a two-row roster and the pure CSwitch join could count the unrelated thread. Running that artifact through production admission with the actual Job accounting bytes unchanged:

```
PROCESS_MEMBERSHIP_INVALID
JOB_QUERY_EVIDENCE_INVALID
INSTRUCTION_ACCOUNTING_INCOMPLETE
PHYSICAL_HARNESS_UNAVAILABLE
```

Downstream authority catches the false member through independent Job accounting and parent/member checks (mbcx01_build_measurement_authority.py:735-761, mbcx01_r13_measurement.py:865-879). Not a deciding bypass; the pure assembler's semantics remain misleading/fragile.

## Claims that survived my attacks

- Q1 / I01 — EXECUTED: fresh self-consistent nonmember candidate with repaired hashes refused RETAINED_SCENARIO_AUTHORITY_INVALID.
- Q2 / I05/I10 — EXECUTED: a byte-changing same-scenario scorer graph substitution validated against its own new episode but was refused SCENARIO_OUTCOME_AUTHORITY_INVALID against the original episode; a missing-position episode with class flipped to COMPLETE_PAIR and rehashed refused EPISODE_PARTITION_MISMATCH.
- Q3 — EXECUTED: the committed fixture owner anchor resolves to ANCHOR_FIXTURE_ONLY; relabeling document and anchor ID does not change key identity, refused PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL.
- Q4 — EXECUTED / SEARCHED: manifest valid 2000–2001 verified at verifier-owned time 2050 refused TRUST_ROOT_VALIDITY_EXPIRED; Go's implementation independently uses this verifier-owned CurrentTime pattern.
- Q7 / I16 — EXECUTED: a production exactness receipt claiming result:"PASS" without execution refused CARRIER_EXACTNESS_SUITE_NOT_EXECUTED. (The packet's parenthetical AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED is the value emitted for a legitimate binding-only result; the refusal code for a fraudulent PASS is the former. Semantics hold.)
- Q8 — EXECUTED: targeted measurement, state and exactness witnesses all went RED when I disabled the mechanism each claimed to protect.

## Residual risks / accepted non-claims

- READ-ONLY / SEARCHED: real ETW/PMU behavior remains physically unproven — same-session SystemTraceProvider + manifest-provider behavior, PMU availability/ownership, platform payload layout, and the flagged unpublished constants are next-gate questions, not source-review closes.
- READ-ONLY / SEARCHED: the first per-processor PMC sample is assigned delta 0 by the current pure join. The sources I opened do not establish enough about the session's initial counter baseline to call that an executed undercount — keeping it a physical-smoke question rather than laundering it into a finding.
- READ-ONLY: the per-witness production exactness suite runner is still intentionally unbuilt; no current byte may be read as suite-executed PASS.
- READ-ONLY: no production signing/custody ceremony has occurred; current green results are fixture/simulated authority evidence only.
- READ-ONLY: the accepted T2/in-process rewiring residual remains outside this artifact's scientific-validity premise.
- READ-ONLY: Q9 gaps #1 and #3 remain disclosed residuals as described.

## Fix class / re-review trigger

Not a leaf-fix acceptance. Required classes before I would re-review:
1. CANONICAL_EXPERIMENT_WORLD_PROJECTION_COMPLETENESS / I02_STATE_BINDING
2. ETW_THREAD_IDENTITY_JOIN
3. ETW_SESSION_LIFECYCLE / LOSS_CAPTURE_SEQUENCING
4. PRODUCTION_SIGNING_KEY_FIXTURE_ISOLATION / CEREMONY_PRECHECK
5. FLAGGED_CONSTANT_VERIFICATION_SET_COMPLETENESS / NUMERIC-ALIAS FAIL-LOUDNESS

The first changes a frozen invariant consumer; the next two change the ETW consumer's fault/unavailability behavior; the fourth changes production admission/ceremony protection. All inside the packet's explicit fresh-council trigger.

Bottom line: the round-4 BUILD is substantially better than a superficial green-suite reading suggests, and several repaired classes held under fresh attack. But acceptance still fails at the byte: I02 omits state fields the governing DoR says are canonical, and the new ETW consumer has two deterministic lifecycle/join failures before any physical unknown is reached. Q9 also proves its own named signing-key gap is ceremony-reachable. NO-GO.
