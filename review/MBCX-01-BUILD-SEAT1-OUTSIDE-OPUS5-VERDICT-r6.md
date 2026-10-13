# MBCX-01 BUILD acceptance r6 — SEAT1 (outside Opus 5) verdict

Banked by the driver from the seat thread (claude.ai conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 22,220,
truncated: false). Packet `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r6.md @ b56892e`; review
target content pin `396752a`. Seat model verified at re-prime: Opus 5 Extra. Verdict verbatim
below (two provider-UI noise lines stripped).

---

GO-WITH-FIXES(SMOKE-PREFLIGHT-NODE · LIVE-PATH-TID-REUSE-PROVENANCE · CONTRACT-SEMANTIC-RIPPLE · LEDGER-NAME-COVERAGE)

Label: EXECUTED. Both signed-field semantic changes ACCEPT. Two false-refusal findings that would burn the one-shot elevated session — both leaf fixes inside existing functions. No finding on the pinned bytes produces a wrong number.

What I read and at which commit. Packet at b56892e. I read the CODE from the working tree and confirm it matches the §2 content pin 396752a: git diff --stat 396752a HEAD -- '*.py' is empty, and the full 396752a..HEAD diff is exactly two files — the r6 packet and the regenerated MBCX-01-BUILD-PIN-MANIFEST.json. HEAD is 8a15c55 (one commit past the packet; manifest regeneration only). Three untracked seat-3 r6 artefacts sit in the tree (…SEAT3-CODEX-EXEC-PROMPT-r6.txt, …-EXEC-r6.log, generate-seat3-build-r6-prompt.ps1); I did not open any of them — the round is sealed.

Read-only compliance: no repository byte created, edited or deleted. Probe scripts and scratch databases live in %TEMP%. No ETW session, no Job Object, no MBCX01_BUILD_ALLOW_PHYSICAL, no run-smoke-cell.ps1. I called mbcx01_smoke_cell.verify_envelope() directly — the pure layer §6 permits.

Baseline reproduced, raw (not through a pipe): BUILD Ran 170 tests … OK, exit 0 · frozen Ran 150 tests … OK, exit 0 · verify-build-bundle.py real exit 0 — tests: 170, expected: 150 / tests: 150, invariants: 65 / witnesses: 170 / two_way_total: true, reconciliation_performed: true / subjects_reconciled: 70, trust_root_activated: false, top_level_readiness: BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED. §0's no-threat-model grep re-run at the pin blobs (not the tree): 0 hits in all three governing docs. The declared adversary is absent from the design of record; this is a validity review.

Evidence read

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r6.md:1-366@b56892e · mbcx01_build_etw_consumer.py:1755-1878 (scope_cswitch_records_to_members), :1881-1894 (provenance), :1525-1532 (lifetime balance faults), :1005 (RECORD_FIELDS), :2145-2146, :2249-2250 (the two scoping call sites) · mbcx01_build_win32.py:380-420 (PROCESS_TELEMETRY_ID_INFORMATION, query_process_start_key), :460-479 (resolve_thread_lifetime), :623-666 (consume_cswitch) · mbcx01_r13_measurement.py:1011-1042 (frozen _validate_physical_evidence), :520-534 (_invoke_signature_verifier) · mbcx01_build_state_store.py:29-46, :88, :139-143, :328-341 · mbcx01_smoke_cell.py:492-510, :513-566, :569-617, :157, :720-746 · mbcx01_build_trust_anchor.py resolve path · mbcx01_build_measurement_authority.py:478 · mbcx01_build_state_authority.py:476 · test_mbcx01_build_measurement.py:2969-3022 (bw59) · MBCX-01-MEASUREMENT-CONTRACT-v7.json /physical_receipt/containment · MBCX-01-BUILD-REPAIR-LEDGER.json · MBCX-01-OPEN-ISSUES.json (MBCX01-BUILD-R1-WIN32-ORDINAL) · MBCX-01-R13-AMENDMENT-2-…-2026-08-15.md:49-189.

SWEEP LOG

I can reach the web this session.

Query: Microsoft Learn thread identifiers reused after thread terminated GetThreadId uniqueness → OPENED at origin: learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-psgetthreadid, Remarks. Deciding sentence: a thread ID is not unique for a boot session, and after a thread terminates its ID may be reused — and the same section states the ID is unique system-wide, not merely per-process. Applicability checked: page live, Last updated 2024-02-24, minimum client Windows XP, no supersession notice. This is what F1 rests on and it is the primary that makes TID recycling a normal platform event rather than a corner case. SEARCHED.
Query: sqlite.org file locking and concurrency BEGIN IMMEDIATE reserved lock one writer at a time → OPENED at origin: sqlite.org/lockingv3.html, §5.0 Writing to a database file: only one process at a time can hold a RESERVED lock; a writer that cannot obtain it fails with SQLITE_BUSY. Applicability caveat, and it bites: the page's own header states it describes rollback-mode only and that WAL locking is documented separately — and mbcx01_build_state_store.py:88 pins journal_mode=WAL. So this primary is authentic and adjacent, not governing. The single-writer invariant holds in WAL too, but I did not open sqlite.org/wal.html, and my own probe (below) ran in rollback mode, not WAL. My item-3 ruling therefore rests on my executed probe plus the store's own honest docstring, with the vendor page as corroboration. SEARCHED, with a stated applicability gap.
ETW Kernel-Process payload versioning / ProcessSequenceNumber — RECALLED / UNSEARCHED (SETTLED-BY-PINNED-BYTES). The packet's §10 opened the repnz Win10-17134 manifest at origin; I verified the consequence in the bytes instead (mbcx01_build_win32.py:389-401 states the two struct members are different numbers and gives the measured example; KERNEL_PROCESS_PAYLOAD_LAYOUTS version-gates the decode). I am not resting any finding on the manifest's contents, so I did not re-open it.
CWE-1291, RFC 7468, RFC 4648 — RECALLED from r4/r5 where I opened CWE-1291 and RFC 4648 at their origins. Carried as argument only; nothing in this verdict turns on them.

Why I stopped: the one claim my new findings actually rest on (TID reuse) was settled at a Microsoft primary opened at origin; the SQLite claim was settled by my own execution with the doc as corroboration and its gap declared. Everything else this round is arithmetic on our own bytes or execution, where no further reading changes anything.

Findings
F1 — EXECUTED · item 1(b) · REFUSES RIGHT EVIDENCE

A host thread that recycles a dead member TID is KEPT by the scoping and then aborts the entire collection.

scope_cswitch_records_to_members:1855 keeps any record whose old_thread_id appears anywhere in the roster, ignoring QPC. consume_cswitch:648-651 then calls resolve_thread_lifetime, which returns None for a QPC outside every lifetime of that TID → ETW_CSWITCH_UNATTRIBUTED_THREAD. Executed against the pinned bytes:

roster: member TID 700 alive [10,40]
stream: (qpc 11, TID 700), (qpc 14, TID 700), (qpc 90, TID 700)   <- 90 is after the member thread died
scope  -> kept 3, excluded 0
  qpc=11 -> lifetime found
  qpc=14 -> lifetime found
  qpc=90 -> None => ETW_CSWITCH_UNATTRIBUTED_THREAD (collection ABORTS)

This is the exact failure mode the scoping was built to remove (:1762-1765 — "aborts the collection by name … after the candidate has already run, which is a wrong diagnosis of right evidence"), reintroduced through the one channel scoping cannot filter. Microsoft's PsGetThreadId page makes reuse a normal boot-session event, and CSwitch is machine-wide, so on a busy host a member TID recycled into a host thread mid-capture is an ordinary occurrence, not a corner case.

The posture itself I accept. The docstring at :1806-1815 names it, and the two cases genuinely are indistinguishable from inside the stream; refusing beats guessing, especially given §3.6 where an attribution error can flip a boundedness verdict. What is missing is the count. Every other exclusion the scoping performs is a number in record_cswitch_scope_provenance — this one is not. After an abort the owner cannot distinguish "the host recycled a TID" from "our roster is incomplete," and those need opposite responses.

Fix class: LIVE-PATH-TID-REUSE-PROVENANCE — one additional counter in the existing provenance dict (records kept on roster-TID match whose QPC lies in no lifetime of that TID). Existing function, existing dict, no new mechanism. Explicitly not proposed: any attempt to disambiguate the two causes — that would be a new machine and it re-enters the design gate.

F2 — EXECUTED · item 6(b) · REFUSES RIGHT EVIDENCE

The smoke conjunction falsely fails when node is not resolvable, and preflight never checks for it.

validate_produced_envelope:553-565 requires signature_verified is True for valid. measurement._invoke_signature_verifier:522-528 converts a missing node (OSError) into ValueError, which :560-562 maps to VERIFIER_UNAVAILABLE:… and valid=False; verify_envelope:608-610 then computes pass_criterion_met = envelope_independently_valid AND errors AND expected_red_present → False. Executed:

PATH cleared -> ValueError: receipt signature verifier unavailable
empty envelope -> structure_errors ['MEASUREMENT_ENVELOPE_INVALID'],
                  evidence_errors ['RECEIPT_SECTION_ABSENT'], valid False

The half (a) attack fails cleanly — an evidentially empty envelope cannot pass: _evidence_section_errors:492-510 requires exact key sets on the query bundle, trace, environment, completion and external-enforcement sections, and an empty envelope trips both structure and evidence. The conjunction discriminates.

Half (b) lands. preflight (mbcx01_smoke_cell.py:157, run-smoke-cell.ps1:90-92) probes elevation, virtualization and static ABI — the only node mention anywhere in the smoke path is a docstring at :532. Elevation commonly changes PATH resolution. A perfect producer run then fails its pass criterion for a reason that has nothing to do with the measurement, and #2/#3 record that this session is the one chance to settle seven platform facts.

Fix class: SMOKE-PREFLIGHT-NODE — add node availability (and the verifier script's presence) to the existing preflight report. One probe in an existing function.

F3 — EXECUTED + READ-ONLY · item 2 ripple · no wrong number today; wrong belief at the audit boundary

Two committed artefacts still carry the OLD root-identity semantics; AMENDMENT-2 names neither.

MBCX-01-MEASUREMENT-CONTRACT-v7.json → /physical_receipt/containment: "Signed membership uses PID plus 64-bit ProcessStartKey for root and every descendant." The instrument now reads ProcessSequenceNumber (mbcx01_build_win32.py:412-420), and :389-401 states at the byte that the two members are different numbers. I walked the whole contract: the field names (root_process_start_key, process_start_key, parent_process_start_key) are consistent, but this sentence names the Windows quantity and is now false. Grepping AMENDMENT-2 for CONTRACT|MEASUREMENT-CONTRACT|containment|ProcessStartKey|ProcessSequenceNumber returns nothing on this document.
MBCX-01-OPEN-ISSUES.json → MBCX01-BUILD-R1-WIN32-ORDINAL, status open_smoke_stage_check, still framed as "uses ProcessTelemetryIdInformation = 64 … for ProcessStartKey acquisition." Post-fold the ordinal is used to read a different member of the same struct, so the issue's discharge condition now verifies the wrong thing.

No code reads either, so no number moves. But item 2's ruling deliberately keeps the old field spelling, which means the receipt alone can never correct a reader who believes the contract sentence. That combination — unamended prose plus deliberately-unchanged spelling — is how this lane lost three rounds to a phantom api-caller. Fix class: CONTRACT-SEMANTIC-RIPPLE. The contract sentence is a frozen-layer edit ⇒ amendment treatment, owner ratifies; the issue text is a records edit.

F4 — EXECUTED · item 4(3) · the packet's own claim is false at the byte

The packet states two-starts-one-stop yields ETW_THREAD_LIFETIME_INCOMPLETE and that "no banked test asserts that name." It does: test_mbcx01_build_measurement.py:3013-3017, inside test_bw59_adversarial_overlapping_lifetimes_for_one_tid_still_fault, feeds exactly START 20, STOP 30, START 60 and asserts the name; it runs in the 170 and it discriminates against its sibling ETW_THREAD_LIFETIME_UNMATCHED_STOP at :3018-3022.

What is missing is one layer up: the name is absent from MBCX-01-BUILD-REPAIR-LEDGER.json while all three siblings are present —

ETW_THREAD_LIFETIME_INCOMPLETE        in ledger: False
ETW_THREAD_LIFETIME_OVERLAPPING_REUSE in ledger: True
ETW_THREAD_LIFETIME_DUPLICATE_START   in ledger: True
ETW_PROCESS_INCARNATION_AMBIGUOUS     in ledger: True

Consequence: none for the data. It says the two_way_total is total over witnesses, not over fault names — a distinction worth knowing when the ledger is read as coverage. Fix class: LEDGER-NAME-COVERAGE, a records row.

F5 — EXECUTED · item 7 supporting · misleads the auditor, no wrong number

The two provenance numbers have different denominators. excluded_foreign_cswitch_records counts every excluded record; foreign_instructions_excluded accumulates only steps taken after that processor's first member record (:1870-1875, deliberately — foreign work before the first member switch is outside the emitted chain). Probe A: 3 excluded records, foreign_instructions 130 where the pre-member interval contributed nothing. An auditor dividing one by the other gets a number that means nothing, and the dict says so nowhere. Leaf: name the second field for what it counts.

F6 — EXECUTED · item 5(3) · REFUSES RIGHT EVIDENCE, wrong shape

Confirmed at the byte through the OS-config door:

committed-key anchor  -> RAISED TrustAnchorError:
    PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL:<anchor_id>:<committed document>
fixture-flagged anchor -> returned (None, 'ANCHOR_FIXTURE_ONLY')
missing anchor path    -> returned (None, 'ANCHOR_UNAVAILABLE')

The refusal is fully named — but in the exception channel while its two siblings use the return channel, and neither authority catches it (mbcx01_build_measurement_authority.py:478, mbcx01_build_state_authority.py:476 call resolve_production_verifier_context bare). A ceremony misconfiguration therefore surfaces as a traceback rather than a named code in the operator's log. It fires only on something the ceremony forbids, so this is a residual, not a defect.

Verified correct (no finding)
Item 1 arithmetic — EXECUTED. Probe A over an interleaved member/foreign stream: every emitted delta equals raw(this switch) − raw(the record immediately before it) exactly as :1779-1783 claims (0 / 30 / 40 vs truth 0 / 30 / 40), with baseline_records = 1 per processor as declared. Probe C: a raw counter going backwards at a member record does surface — the accumulator cannot mask it, because foreign_offset is monotone non-decreasing, so delta = raw(this) − raw(previous record) and negativity is preserved into consume_cswitch:654-655. No schema or contract anywhere asserts counter_value is the raw MSR value.
Both downstream recomputations agree. consume_cswitch:652-656 and the frozen _validate_physical_evidence:1031-1039 compute the identical rule and both refuse a negative delta.
Item 3 — EXECUTED. Two connections, BEGIN IMMEDIATE + unique index: second writer → OperationalError: database is locked; after the first commits the second allocates 2; a duplicate seq → IntegrityError: UNIQUE constraint failed: journal.seq. The named harm is closed by SQLite itself. (Caveat: my probe ran rollback-journal mode; the store pins WAL at :88.)
The seven rulings

1 — counter_value as a member-attributed accumulator: ACCEPT.
The frozen observation schema has one counter slot, both independent recomputations define the delta as previous emitted value on the same processor, and Probe A shows the accumulator is the only reading under which that delta equals the interval the member thread actually ran. A raw-value slot would be an amendment buying nothing the provenance dict does not already carry.

2 — ProcessSequenceNumber as root identity, old field spelling retained: ACCEPT, with F3 owed.
:389-401 establishes at the byte that the two struct members are different numbers and that only the sequence number appears in a ProcessStart payload; reading the other guaranteed ETW_PROCESS_LIFETIME_ROOT_ABSENT on every physical run. A PID-reuse mis-root is not constructible: sequence numbers are per-boot monotone and unique, which is precisely why they are a better identity than the PID. Keeping the spelling is right — renaming a signed field to fix prose is the larger change — but the two stale artefacts in F3 must be corrected, or the retained spelling makes the stale sentence unfalsifiable.

3 — SQLite serialization as sufficient, no writer door: ACCEPT no-door.
Executed above; and there is no adversary in the model to give sever priority to. Photon's writer_gate.rs solves multi-writer sever priority under a concurrency model this single-harness instrument does not have — declining it is right, and building it would be a new subsystem. Residual, and it is already the packet's own #25: the busy path surfaces as a raw sqlite3.OperationalError (no busy_timeout pragma in the store; Python's 5 s default applies) rather than a named refusal — that red is owed, and it is the one thing standing between "no door" and "no door, honestly."

4 — the six AMENDMENT-2 judgment calls:
(1) bare-CR PEM accepted — ACCEPT. RFC 7468 §2 parser guidance governs a parser; being broader than one emitter is the correct asymmetry, and generosity in reading never becomes generosity in identity.
(2) the anchor stores the normalised carrier — ACCEPT. Identity is the key; byte-identity with a source document was never the claim, and storing the normalised form is what makes one key have one carrier downstream.
(3) ETW_THREAD_LIFETIME_INCOMPLETE for two-starts-one-stop — ACCEPT the vocabulary; CHANGE the driver's premise. A witness is not owed: test_mbcx01_build_measurement.py:3013-3017 already asserts it (F4). A ledger row is owed.
(4) touching intervals refused in both layers — ACCEPT. Inclusive containment at both ends means a shared instant puts one QPC in two lifetimes; refusing is what keeps the join a function, and resolve_thread_lifetime:479 returns None on two matches for the same reason.
(5) ETW_PROCESS_INCARNATION_AMBIGUOUS as its own name — ACCEPT. "I cannot tell which incarnation" and "no incarnation explains this" are different facts for the operator reading an aborted capture, and this lane's whole posture is that different facts get different names.
(6) stop-less incarnation OPEN-ENDED for the binder, roster completeness owned by assemble_member_lifetimes — ACCEPT. One fact, one owner; duplicating the completeness check in the binder would put the same row in two consumers and invite exactly the divergence the matrix rule §1 forbids.

5 — the three fixture-key gaps:
(1) FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM — ACCEPT as residual. Its public half is in no committed document, so nobody reaches it by copying a file; putting a Node subprocess on the production construction path to close it is a larger change than the gap.
(2) committed test SIGNING key refused as MEASUREMENT_CUSTODY_EVIDENCE_INVALID rather than as committed material — ACCEPT as residual. I did not find a ceremony path that reaches it: §3 step 3's manifest is authored from step 2's freshly generated keys, and the harvest now keys on content. Reachability unshown ⇒ the disclosure is sufficient.
(3) raise-instead-of-code on the OS-config path — ACCEPT as residual, with F6's note. The refusal is named; only its channel is asymmetric, and no authority catches it, so the ceremony gets a traceback instead of a log line.

6 — the conjunction as the smoke criterion of record: ACCEPT, with F2 fixed first.
Both halves discriminate — an empty envelope fails structure and evidence, and the honest red only counts for an independently validated envelope. But do not run elevated until preflight probes node, or a valid producer run can fail on a PATH difference and burn the session.

7 — exclusion counts in the receipt: ACCEPT as a named residual; do NOT amend now.
A third frozen amendment to add a slot, before a single live capture has ever produced these numbers, is machinery ahead of evidence — the packet's own §9 standard. The counts exist in the capture provenance and can be banked alongside the smoke output. Revisit once the elevated run says whether they carry diagnostic weight. But fix F5 (the denominator mismatch) and add F1's counter to the provenance dict first — an amendment that freezes a number nobody can interpret is worse than no slot.

Residual risks
F1 is a real operational risk on a busy host, and it compounds #3 (machine-wide Kernel-Process abort). Two independent machine-wide-stream abort paths now gate the same one-shot session.
My item-3 evidence has a stated gap: the store runs WAL; my probe and the opened SQLite page describe rollback mode. The single-writer invariant holds in both, but I did not verify it under WAL.
Item 2's PID-reuse attack is unconstructible by design, not by test. I reasoned it from sequence-number uniqueness rather than executing it; that half is READ-ONLY.
I did not probe items 4(1), 4(2), 4(6) or 5(2) with fresh inputs — those four rulings are READ-ONLY, reasoned from the bytes and the amendment record.
§8.5 stands unchanged: the consumer has never run against a live session; every green here means the logic is right if the platform behaves as documented.
#25 remains red-owed and is the honest completion of ruling 3.
Fix class
#	Class	Scope	Gate
F2	SMOKE-PREFLIGHT-NODE	one probe in preflight (mbcx01_smoke_cell.py:157)	Leaf + witness. Before the elevated run.
F1	LIVE-PATH-TID-REUSE-PROVENANCE	one counter in record_cswitch_scope_provenance (:1881-1894) + one witness	Leaf; codex r4 gate. Before the elevated run.
F3	CONTRACT-SEMANTIC-RIPPLE	MEASUREMENT-CONTRACT-v7.json /physical_receipt/containment (frozen ⇒ amendment, owner ratifies); MBCX01-BUILD-R1-WIN32-ORDINAL issue text (records)	Split gate.
F4	LEDGER-NAME-COVERAGE	one row in MBCX-01-BUILD-REPAIR-LEDGER.json	Records; codex r4 gate.
F5	leaf rename/doc of foreign_instructions_excluded	provenance dict	Codex r4 gate.
F6	ACCEPT as residual; optional leaf — catch TrustAnchorError at the two authority call sites so the refusal reaches the log as a code	:478 / :476	Owner's call; not blocking.

On the GO. EXECUTED, so this can serve as a deciding vote. GO-WITH-FIXES rather than NO-GO because nothing here makes the instrument produce a wrong number or admit wrong evidence on the pinned bytes: items 1 and 2 are correct at the byte, and the four real findings are two false refusals and two records gaps, all fixable inside existing functions. If any part of this round is read as authorising the elevated smoke run, my vote is NO-GO until F2 lands — the session is one-shot, and a missing node on the elevated PATH would spend it on nothing.
