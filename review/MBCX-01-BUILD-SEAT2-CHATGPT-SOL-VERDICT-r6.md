# MBCX-01 BUILD acceptance r6 — SEAT2 (ChatGPT sol) verdict

Banked by the driver from the seat thread (chatgpt.com project conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 23,176,
truncated: false, FINAL VERDICT line present). Packet
`MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r6.md @ b56892e`; review target content pin
`396752a`. Verdict verbatim below.

---

GO-WITH-FIXES(ETW_CSWITCH_SCOPE_TID_REUSE_DISAMBIGUATION + ETW_THREAD_EVENT_VERSION_GATE + SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION)

Verdict basis: EXECUTED. I read MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r6.md at packet commit b56892e3c3d73a60948b724e95d1e2dcc1ac0a9b and reviewed content commit 396752a680d5f057daef51704a2945ccd2735b41. The working-tree packet hashes to the exact pinned blob 778fe22a2b6c2335522e5d2f178ab89e87d91bbe; git diff --stat 396752a HEAD -- '*.py' is empty, there are no tracked working-tree modifications, and the only untracked current-seat execution log was seen by name and not opened. I used working-tree source only after confirming those bytes match the review target.

I read §0 first and held to it. Independent grep over the three governing design files returned zero hits for threat model|adversary|attacker|untrusted|api-caller|hostile. I am therefore treating this strictly as a scientific-validity review, not a security-boundary review.

Execution record

The bank is genuinely green on the pinned tree:

BUILD suites: 170/170 OK, direct execution.

Frozen r13.2 suites: 150/150 OK through verify-build-bundle.py's explicit frozen-suite gate. An earlier wildcard-discovery invocation was blocked by the tool layer before execution; I did not count that blocked call as evidence.

python verify-build-bundle.py: real exit 0, including pin_manifest: PASS.

Clean-room verify-build-pinned.ps1 -Commit 396752a… -ManifestBlob 97a02c13fba6c0f39a913659ff2719d868776154: real exit 0.

No real ETW session, Job Object, physical-enable environment variable, or smoke-cell execution was performed.

The green bank does not cover the three fresh shapes below.

Evidence read

Load-bearing pinned bytes:

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r6.md:7-34,45-98,100-217,273-350@b56892e3

MBCX-01-R13-CLOSURE-ARCHITECTURE.md:72-106@396752a

MBCX-01-R13-AMENDMENT-2-THREAD-IDENTITY-AND-PEM-TRANSPORT-2026-08-15.md@396752a

mbcx01_build_etw_consumer.py:1190-1265,1320-1735,1755-1895,2100-2265,2920-3005,3070-3118@396752a

mbcx01_build_win32.py:378-454,527-560,1171-1210@396752a

mbcx01_smoke_cell.py:459-617@396752a

mbcx01_build_measurement_authority.py:346-425,569-647,741-804@396752a

mbcx01_r13_measurement.py:833-1045@396752a

mbcx01_build_state_store.py:27-56,124-143,381-400,460-500,727-745@396752a

mbcx01_build_trust_anchor.py:272-343,630-792,900-948@396752a

MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:120-190@396752a

test_mbcx01_build_measurement.py:1768-1845,2391-2615,2940-3040@396752a

test_mbcx01_build_state.py:237-285,1421-1475@396752a

test_mbcx01_build_integration.py:707-800@396752a

MBCX-01-MEASUREMENT-CONTRACT-v7.json:33-46,165-195@396752a

Where older prose and the adopted amendment differ, AMENDMENT-2/current code wins under the role card's newer-owner-locked rule.

WHY THIS EXISTS

1. ALREADY-BUILT? — EXECUTED · SEARCHED. The low-level acquisition mechanism is established Windows prior art: Microsoft's WPT/WPR documentation explicitly supports collecting InstructionRetired hardware counters on CSwitch. The bespoke thing here is not "how to count instructions"; it is the signed Job-member attribution/evidence join needed by this experiment.

The packet contains a real internal-shelf log. I independently spot-ran InstructionRetired|TracePmc|CSwitch|ProcessSequenceNumber over bridge src/, Photon crates/, and Gravity src/; all three returned zero files. For key handling I opened the already-adopted bridge pattern at agentvault-mcp-bridge/src/crl/crl-authenticate.ts:15-20,109-123 and src/crl/der-reader.ts:210-235: raw SPKI plus structural DER parsing was already on the shelf and the BUILD correctly adopted that pattern. For writer serialization I opened Photon crates/aruna/src/writer_gate.rs:7-38; that mechanism exists, but it solves SEVER priority and an application concurrency model this experiment does not have.

2. PRODUCT-FIT? — READ-ONLY · UNSEARCHED — SETTLED-BY-PINNED-BYTES. Yes: this is governed, fail-loud measurement rather than prevention. In one sentence: the customer need is a defensible physical-work measurement for each experiment cell, or an explicit unavailable result when the machine cannot support that measurement.

3. BIGGER-THAN-THE-BUG? — READ-ONLY · UNSEARCHED — SETTLED-BY-PINNED-BYTES. No. The reviewed folds are changes inside existing acquisition, joining, parsing, and validation functions. The three fixes I name below are likewise bounded. I do not recommend a new writer gate, evidence engine, parser subsystem, or measurement machine.

4. PRIMARY-CONSUMER? — READ-ONLY · UNSEARCHED — SETTLED-BY-PINNED-BYTES. The engineering/scientific gate consumes the signed 100-cell physical evidence. A bounded read buys it actual retired-instruction/CPU/I/O/memory/time measurements and lets it compute the finite H-shape boundedness gates; for retired instructions the governing closure sets the max-minus-min limit at 500,000 before a carrier can survive into engineering selection (MBCX-01-R13-CLOSURE-ARCHITECTURE.md:89-106).

Findings
F1 — EXECUTED · SEARCHED — CSwitch scoping falsely refuses legitimate foreign TID reuse

Data consequence: REFUSES RIGHT EVIDENCE.

AMENDMENT-2 correctly made the downstream thread join TID+QPC aware. The preceding CSwitch scoper did not make the same transition.

scope_cswitch_records_to_members() builds a set of member TIDs at mbcx01_build_etw_consumer.py:1826-1830 and keeps a CSwitch whenever old_thread_id appears anywhere in that set at :1855, without asking whether the QPC lies inside a member lifetime.

I constructed the full machine-wide shape, not merely a naked row:

measured root PID 4100 / key 11, member TID 77 alive at QPC 20–30;

foreign PID 5000 / key 22, later reuses TID 77 at QPC 50–80;

partition_job_member_events() correctly separated that second TID-77 lifetime into excluded_thread_events;

CSwitch at QPC 25/TID77 is member evidence;

CSwitch at QPC 60/TID77 is known foreign evidence.

Current scoping result:

member_thread_events:
  TID 77 / PID 4100 / qpc 20..30

foreign_thread_events:
  TID 77 / PID 5000 / qpc 50..80

scope_kept:
  qpc 25 / TID 77
  qpc 60 / TID 77

scope_excluded:
  []

consume_cswitch:
  CollectorFault ETW_CSWITCH_UNATTRIBUTED_THREAD

Windows explicitly permits thread identifiers to be reused after a thread terminates.

This is important because the harness is not actually ambiguous in this probe: its own machine-wide Process/Thread stream already proved that the QPC-60 incarnation is the foreign PID. partition_job_member_events() retains that evidence; the later CSwitch function simply receives too little of it and reverts to global-TID membership.

The member-attributed accumulator arithmetic itself survived attack. In a mixed member/foreign sequence, foreign intervals were subtracted and the emitted member delta equaled raw current minus the immediate preceding raw CSwitch, exactly as the signed semantics require.

Fix class: ETW_CSWITCH_SCOPE_TID_REUSE_DISAMBIGUATION.

Bounded fix: let the existing CSwitch scope use the already-derived foreign/member TID lifetime intervals. A row that falls inside a known foreign reuse interval is a baseline; a row outside both known member and known foreign evidence can retain the current fail-loud posture. No signed-field semantic or schema change is required.

F2 — EXECUTED · SEARCHED — unverified ThreadStart/ThreadStop event versions are decoded and can feed a number

Data consequence: ADMITS WRONG/UNVERIFIED EVIDENCE and can produce a retired-instruction number from it.

The source explicitly declares:

KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED = {0, 1}

at mbcx01_build_etw_consumer.py:376.

ProcessStart/Stop decoding is version-gated. ThreadStart/Stop decoding at :2985-3003 is not: it takes any event version with at least eight payload bytes and interprets those bytes as <ProcessId, ThreadId>.

Fresh probe presented ThreadStart and ThreadStop with EventDescriptor.Version = 9, outside the verified set, plus an arbitrary unknown tail. Current code:

verified_thread_versions = [0, 1]
presented_version = 9

decoded:
  START pid=4100 tid=900 qpc=20
  STOP  pid=4100 tid=900 qpc=30

assembled member lifetime:
  pid=4100 / key=11 / tid=900 / 20..30

CSwitch counters:
  1000 -> 1080

admitted deltas = [0, 80]
aggregate = 80

Microsoft's ETW contract makes the provider + Event.Id + Event.Version combination the schema identity; Microsoft specifically says a version revision may change field types or add fields. Therefore the fact that v0/v1 have the desired first eight bytes does not authorize decoding invented/unknown v9 as the same layout.

This also conflicts with the BUILD's own invariant that unverifiable platform facts fault loudly. The supported-environment contract is generic WINDOWS_64BIT; it does not pin one Windows build forever, so event-schema evolution is not excluded by the experiment.

Fix class: ETW_THREAD_EVENT_VERSION_GATE.

Bounded fix: before decoding ThreadStart/ThreadStop, require EventDescriptor.Version to belong to KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED; unknown revisions fault by name, just as the Process event path already does. No subsystem.

F3 — EXECUTED · UNSEARCHED — SETTLED-BY-PINNED-BYTES — smoke "independent validity" is presence-only, so wrong physical evidence can pass

Data consequence: ADMITS WRONG EVIDENCE as a successful physical-smoke result.

mbcx01_smoke_cell._evidence_section_errors() at :459-510 checks that the expected evidence blocks and fields exist. It does not judge the load-bearing semantics inside them.

validate_produced_envelope() then defines valid=True from: envelope structure, those presence checks, signature verification.

The full semantic validator already exists at mbcx01_build_measurement_authority._receipt_errors() (:741-804), which calls the frozen _validate_physical_evidence().

Fresh probe started with a legitimate fixture-signed smoke envelope, changed exactly one load-bearing physical fact:

process_membership.membership_complete = False

then recomputed the receipt preimage/hash and legitimately re-signed the envelope.

Current smoke result:

structure_errors = []
evidence_errors = []
signature_verified = True
envelope_independently_valid = True

full existing per-receipt validator:
  PROCESS_MEMBERSHIP_INVALID

expected_red_present = True
pass_criterion_met = True

So the elevated run can bank "pass" even though the harness's own full scientific validator says the physical membership evidence is invalid.

I also tested the false-refusal inverse demanded by this round: the unchanged honest smoke envelope gives:

full per-receipt semantic errors = []
current smoke pass = True

So using the already-existing per-receipt semantic check does not reject the legitimate positive control.

Fix class: SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION.

Bounded fix: preserve the conjunction, but make "independently valid envelope" mean valid structure + signature + complete per-receipt physical semantics, using the existing receipt validator. Do not run grid coverage or production trust admission as part of that first half.

Non-findings / attacks that held

Root ProcessSequenceNumber — EXECUTED · SEARCHED. I scripted ProcessTelemetryIdInformation with different ProcessStartKey and ProcessSequenceNumber values. query_process_start_key() returned the sequence number; the ETW process stream carrying that sequence joined successfully. Replacing it with the old boot-tagged start-key value failed ETW_PROCESS_LIFETIME_ROOT_ABSENT. Microsoft's telemetry structure independently exposes ProcessStartKey, ProcessSequenceNumber, and BootId as distinct fields. Current joined semantics are internally coherent.

SQLite no-door — EXECUTED · SEARCHED. Three separate processes each did BEGIN IMMEDIATE, allocated MAX(seq)+1 while holding the write transaction, paused, inserted, and committed. Durable sequences were exactly [1,2,3]; the unique index remained present. SQLite documents that only one write transaction may be active at a time and that BEGIN IMMEDIATE begins that write transaction. A stronger Photon writer gate would add concurrency/priority policy the experiment does not need.

Amendment-2 PEM decisions — EXECUTED · SEARCHED. Fresh LF, CRLF/bare-CR, and absent-final-EOL forms all produced the same decoded key identity; the anchor normalized them to one LF carrier. RFC 7468 defines lines using CRLF, CR, or LF and its ABNF makes the post-boundary EOL optional. Normalization did not weaken committed-key identity.

Touching lifetimes — EXECUTED · SEARCHED. Touching [20,30] and [30,40] lifetimes fault ETW_THREAD_LIFETIME_OVERLAPPING_REUSE; that is a defensible fail-loud call rather than a false refusal. Windows documents ±1-tick ordering from different threads as ambiguous, which reinforces refusing an instant that cannot be assigned uniquely at the timestamp resolution.

Fixture-key material — EXECUTED · SEARCHED. The remaining non-anchor private-key gap is mechanically real: I derived its public half in a transient probe, confirmed it is absent from the committed-key census, and showed that if one deliberately substitutes that committed private key into a fully production-shaped ceremony universe, admission can clear. But the actual ceremony generates the production key in its custody backend and never chooses that source literal. Under this round's no-adversary boundary, that remains a named residual rather than a reason to add source-scanning machinery. MITRE's underlying key-separation principle is real — different production/debug keys is its Implementation mitigation — but the threat model does not expand merely because that prior art exists.

Omission attack

The strongest unnamed omission was F2, the missing ThreadStart/ThreadStop version gate. The source had already done the hard work of declaring {0,1} as the verified set, but only the Process event decoder consumed the event version. That is exactly the class the omission lane is meant to catch: a "verified platform layout" claim whose sibling live consumer silently ignores its verification discriminator.

I additionally compared two different machine-wide streams with different excluded-CSwitch provenance:

A: 1 foreign CSwitch, 50 foreign instructions
B: 2 foreign CSwitches, 80 foreign instructions

After correct foreign-work subtraction, both produced the identical signed member stream and identical member delta. That supports treating the dropped exclusion counts as diagnostics rather than part of the scientific number.

Seven explicit rulings

1. ACCEPT — member-attributed counter_value. The accumulator is the correct meaning for the one signed field: fresh mixed-stream arithmetic preserved the actual member interval. F1 is a scope-classification defect, not evidence that the signed-field semantic needs a raw-counter schema slot.

2. ACCEPT — ProcessSequenceNumber as root identity of record, retaining the historical field spelling. The fresh root-query/ETW differential joins with ProcessSequenceNumber and cannot join with the old boot-tagged ProcessStartKey. Microsoft's telemetry structure also confirms these are distinct quantities. Older generic "ProcessStartKey" wording is superseded here by the owner-adopted Amendment-2/current bytes.

3. ACCEPT — no new writer door. SQLite's write serialization + unique sequence index + sequence allocation inside BEGIN IMMEDIATE is sufficient for this single-harness scientific instrument. A Photon-style writer gate would solve a different priority/concurrency problem.

4. ACCEPT the six Amendment-2 judgment calls, with one packet-record correction.

4.1 ACCEPT bare-CR PEM parsing: RFC 7468 parser latitude supports it.

4.2 ACCEPT storing the normalized carrier: identity is unchanged; downstream sees one stable spelling.

4.3 ACCEPT the narrowed fault vocabulary. CHANGE the packet's statement that no witness pins ETW_THREAD_LIFETIME_INCOMPLETE: current pinned test_mbcx01_build_measurement.py:3012-3017 already asserts that name. No new witness is owed.

4.4 ACCEPT refusing touching intervals: boundary ownership is not uniquely reproducible at that instant; fail-loud is preferable to choosing one.

4.5 ACCEPT distinct ETW_PROCESS_INCARNATION_AMBIGUOUS: ambiguity and absence are different observed facts.

4.6 ACCEPT stop-less incarnation as open-ended for binding while roster completeness later refuses it. Fresh probe bound the interim event but assemble_member_lifetimes() then failed ETW_PROCESS_LIFETIME_INCOMPLETE; no incomplete member roster reaches evidence.

5. ACCEPT/CHANGE the three fixture-key residuals as follows.

5.1 ACCEPT-AS-RESIDUAL FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM: mechanical substitution is possible, but it is not on the honest ceremony's key-generation/copy path. Do not add a Node/private-key census for a phantom actor.

5.2 CHANGE — this is no longer an open gap at the reviewed bytes. Fresh exact flipped committed measurement manifest returns PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL in addition to custody/root errors, and the key resolves to MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json. This is a packet/ledger correction, not a code fix.

5.3 ACCEPT-AS-RESIDUAL OS-config committed anchor raising rather than returning a code. Fresh OS-config probe raised PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL:<anchor>:<document>. It loudly refuses wrong material; it neither admits wrong evidence nor refuses a legitimate owner key.

6. CHANGE — retain the conjunction, strengthen its first half. A smoke pass must require the existing semantic per-receipt physical-evidence validation, not merely presence/shape + signature. membership_complete=False currently passes the smoke while the existing full validator says PROCESS_MEMBERSHIP_INVALID.

7. ACCEPT — no receipt slot for exclusion counts, as a named diagnostic residual. Fresh streams with materially different foreign exclusion counts/work yielded the same correct signed member number. I therefore do not justify a third frozen amendment solely for those diagnostics. The packet should not imply the elevated smoke will magically answer their value, however: the current signed receipt has no slot and _trace_facts() does not surface them.

SWEEP LOG

Queries:

site:learn.microsoft.com "thread ID may be reused" Windows
site:learn.microsoft.com EVENT_DESCRIPTOR Version event version provider event ID version fields
site:learn.microsoft.com PROCESS_TELEMETRY_ID_INFORMATION ProcessSequenceNumber ProcessStartKey
site:learn.microsoft.com QueryPerformanceCounter different threads one tick ambiguous ordering
site:learn.microsoft.com Windows PMU InstructionRetired CSwitch HardwareCounter
site:sqlite.org BEGIN IMMEDIATE one writer write transaction
site:rfc-editor.org RFC 7468 newline CR LF CRLF parsers
site:cwe.mitre.org 1291 production debug keys different keys

Opened at origin and deciding sections:

learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information — dwThreadId: identifier may be reused after the thread object is freed; confirms F1 is a legitimate Windows lifecycle.

Microsoft PsGetThreadId documentation — Remarks explicitly says thread ID is not boot-session unique and may be reused after termination.

learn.microsoft.com/en-us/windows/win32/api/evntprov/ns-evntprov-event_descriptor — Id/Version: provider+ID+version defines manifest event field schema; versions may alter field details. Deciding source for F2.

learn.microsoft.com/en-us/windows/win32/devnotes/process_telemetry_id_information_type — structure exposes ProcessStartKey and ProcessSequenceNumber independently. Confirmed item 2.

learn.microsoft.com/en-us/windows-hardware/test/wpt/counters — official InstructionRetired on CSwitch example. Settled external prior art for WHY-THIS-EXISTS.

learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps — ±1 QPC tick across threads has ambiguous ordering. Informed the touching-interval judgment.

sqlite.org/lang_transaction.html — one simultaneous writer; BEGIN IMMEDIATE starts the write transaction. Settled item 3.

rfc-editor.org/rfc/rfc7468.html — §§2–3 newline conventions and optional terminal EOL. Settled item 4.1.

cwe.mitre.org/data/definitions/1291.html — Implementation mitigation uses distinct production/debug keys. Confirmed prior-art class but did not widen this lane's threat model.

I stopped because the remaining open platform questions are exactly the packet's physical-smoke residuals; more documentation cannot substitute for the owner-authorized elevated run.

Residual risks

The ETW consumer still has never run against a live PMC session. Same-session provider behavior, actual PMU grant/ownership, physical loss behavior, CREATE_SUSPENDED root delivery, target-host ABI behavior, and other explicitly listed smoke facts remain unresolved until the elevated run. Those are named non-claims, not failures inferred from absence.

The first member CSwitch interval per processor remains a declared zero-delta baseline/undercount. I found no additional silent undercount after it in the arithmetic I exercised.

The old field name root_process_start_key now means ProcessSequenceNumber. I accept the semantics but this is nomenclature debt; any future external consumer must read the current amendment rather than infer the old telemetry meaning from the name.

Fixture private material whose public half appears nowhere in the JSON census remains a ceremony-discipline residual. Under the explicit no-threat-model boundary I do not escalate that into a source scanner or key-derivation subsystem.

Exclusion provenance remains unsigned diagnostic information. I did not demonstrate that omission changing a scientific number, so it does not satisfy §0 as a blocker.

Fix class / disposition

Three bounded fixes are required before the elevated smoke run:

ETW_CSWITCH_SCOPE_TID_REUSE_DISAMBIGUATION — use the already-known member/foreign TID lifetime intervals while scoping CSwitch records.

ETW_THREAD_EVENT_VERSION_GATE — refuse ThreadStart/Stop versions outside the verified version set.

SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION — include the already-existing complete per-receipt physical-evidence validator in the independent-valid half of the smoke conjunction.

None requires a new machine, receipt slot, writer door, or signed-field semantic change. Under packet §13 these are bounded BUILD fixes rather than another design amendment. Do not run the one elevated smoke on the current bytes: F3 can falsely certify it, and F1 can burn a valid machine-wide capture on ordinary Windows TID reuse.

FINAL VERDICT: GO-WITH-FIXES(ETW_CSWITCH_SCOPE_TID_REUSE_DISAMBIGUATION + ETW_THREAD_EVENT_VERSION_GATE + SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION).
