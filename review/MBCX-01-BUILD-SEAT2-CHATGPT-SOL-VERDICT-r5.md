NO-GO

Verdict basis: EXECUTED. I read the r5 packet at d122ee10e19a0fa9288c0aa8594494c1476a9fb4 and reviewed the content target fce7b3551d228e91b77814fdb3d3296c3d7ee08b. I used the working tree for execution only after verifying that fce7b355… → 7af17752… changes only MBCX-01-BUILD-PIN-MANIFEST.json, 7af17752… → d122ee10… adds only the r5 packet, and there are no tracked working-tree changes. Two untracked r5 seat-execution files were visible by name only; I did not open them. I also independently ran verify-build-pinned.ps1 against fce7b355… with manifest blob 60d75d627a7753390f701faf0c2cd91d2fd57e99; it returned PINNED RECONSTRUCTION COMPLETE, exit 0.

The r4 folds close substantial ground, including my I02 finding. They are not acceptance-ready yet. I found one wrong-evidence admission and two false refusals of right evidence, all within section 0's scientific-validity model and none depending on a hostile actor.

## Evidence read

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r5.md:7-34,43-83,85-175,177-237@d122ee10 · MBCX-01-R13-AMENDMENT-1-CANONICAL-WORLD-BINDING-2026-08-15.md:9-109@fce7b355 · MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:7-40@fce7b355 · mbcx01_r13_packets.py:68-95,500-545 · mbcx01_r13_measurement.py:834-990 · mbcx01_build_etw_consumer.py:979-1085,1412-1443,1626-1692,1955-2066 · mbcx01_build_win32.py:527-560 · mbcx01_build_trust_anchor.py:282-297,373-389,473-626,629-732 · mbcx01_build_measurement_authority.py + mbcx01_build_state_authority.py production-signing-key refusal paths · mbcx01_build_exactness_authority.py:168-234 · mbcx01_build_ceremony_fixture.py in-memory owner/signing-key generation · test_mbcx01_build_measurement.py:1639-1725,2391-2615 · test_mbcx01_build_state.py:1384-1425 · verify-build-bundle.py:49-60,251-267 · MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:134-190 · MBCX-01-BUILD-SMOKE-RUNBOOK.md:42-112 — all @fce7b355.

I independently repeated the section-0 threat-model grep over the three governing design files at the pin: zero hits in all three.

## Execution record

```
BUILD suites       125 / 125 OK
Frozen r13 suites  147 / 147 OK
verify-build-bundle.py
  exit 0 · 46 invariants / 125 witnesses · two_way_total = true
  readiness = BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED
verify-build-pinned.ps1
  content fce7b355… · manifest blob 60d75d62… · PINNED RECONSTRUCTION COMPLETE · exit 0
```

Those greens are real. The findings below are fresh inputs outside the existing green net.

## WHY THIS EXISTS

**ALREADY-BUILT — EXECUTED / SEARCHED.** I spot-ran the internal shelf. `spki|subjectPublicKeyInfo|der[_ -]?reader` found the bridge CRL machinery and nothing corresponding in Photon or Gravity; I opened agentvault-mcp-bridge/src/crl/crl-authenticate.ts:15-20,109-123 and src/crl/der-reader.ts:221-239. The r4 key fold did in fact adopt that structural/raw-SPKI pattern. A separate `EVENT_TRACE|TracePmc|CSwitch|ProcessTrace` query returned zero files across bridge src/, Photon crates/, and Gravity src/. Externally, Microsoft WPR already knows how to collect InstructionRetired on CSwitch; what is bespoke here is MBCX's signed, Job-scoped scientific-evidence join, not basic PMU acquisition.

**PRODUCT-FIT — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES.** Yes. This is directly the experiment's measurement instrument: accept defensible measurements, refuse unverifiable ones, and say why. All three findings below matter precisely because they break that contract.

**BIGGER-THAN-THE-BUG — READ-ONLY.** The r4 folds are generally bounded. I do not recommend any new engine or subsystem. F1/F2 require repairing the existing thread-lifetime interval join; F3 requires relaxing one textual-carrier parser to the actual RFC grammar while retaining the decoded-key identity and canonical DER checks.

## SWEEP LOG

Exact external queries:
```
site:rfc-editor.org RFC 7468 newline conventions CRLF final eol PUBLIC KEY
site:rfc-editor.org RFC 8410 Ed25519 SubjectPublicKeyInfo parameters absent
site:learn.microsoft.com Windows ThreadId reused after thread termination UniqueThreadId TTD
site:learn.microsoft.com CloseTrace ERROR_CTX_CLOSE_PENDING ProcessTrace real time ETW
site:learn.microsoft.com Recording Hardware Performance PMU Events InstructionRetired CSwitch
```

Opened at origin:
- **RFC 7468, §§2–3** (https://www.rfc-editor.org/rfc/rfc7468.html): parsers must handle differing newline conventions; CRLF, CR and LF are recognized, and the standard ABNF permits the final post-boundary EOL to be absent. This changed item 4 from "strictness choice" to an executed false-refusal finding.
- **RFC 8410, §4** (https://www.rfc-editor.org/rfc/rfc8410.html): Ed25519 SPKI uses OID 1.3.101.112 with absent parameters and a BIT STRING carrying the public key. Confirms the fold's structural DER/key-identity half; my objection is the outer textual PEM grammar, not its SPKI parsing.
- **Microsoft TTD Memory Objects, ThreadId/UniqueThreadId**: ordinary Windows thread IDs can be reused during a process lifetime; TTD has a separate UniqueThreadId precisely because ordinary TIDs are not trace-lifetime unique. This makes the duplicate-TID refusal a real false-refusal path.
- **Microsoft CloseTrace**: ERROR_CTX_CLOSE_PENDING is successful for a real-time trace and means ProcessTrace drains queued events before stopping. This CONFIRMED the repaired drain logic rather than producing a finding.
- **Microsoft WPT / PMU recording**: official examples use InstructionRetired + CSwitch. Confirms the external-shelf baseline.

Installed Windows SDK header, opened directly:
```
evntcons.h:58   PMC_COUNTERS       = 0x0008
evntcons.h:60   EVENT_KEY          = 0x000A
evntcons.h:63   PROCESS_START_KEY  = 0x000D
evntcons.h:148  EXTENDED_INFO      = 0x0001
evntcons.h:156  CLASSIC_HEADER     = 0x0100
winerror.h:18367 ERROR_CTX_CLOSE_PENDING = 7007L
```
That confirms the r4 constant corrections. I stopped because the remaining unresolved OS facts are exactly the packet's owner-authorized physical-smoke questions.

## Findings

### F1 — EXECUTED / SEARCHED — valid Windows TID reuse is falsely refused
**Data consequence: REFUSES RIGHT EVIDENCE.**

`assemble_thread_lifetimes()` is still globally keyed by thread_id; a second START for a previously terminated TID raises `ETW_THREAD_LIFETIME_DUPLICATE_START`. `mbcx01_build_win32.EtwPmcSession.consume_cswitch()` likewise builds one dictionary entry per thread_id, and the frozen evaluator at mbcx01_r13_measurement.py:946-960 explicitly rejects a second lifetime carrying the same TID. Windows does not give this uniqueness guarantee.

```
process 4242 / start-key AA: qpc 10..100
TID 77 lifetime #1: START 20, STOP 30
TID 77 lifetime #2: START 60, STOP 70
bind_thread_start_keys: both lifetimes correctly bind to process AA
assemble_thread_lifetimes: ETW_THREAD_LIFETIME_DUPLICATE_START:77
```

Through the signed production-shaped admission path with two non-overlapping lifetimes for the same legitimate TID:
```
production admission: INSTRUCTION_ACCOUNTING_INCOMPLETE / PHYSICAL_HARNESS_UNAVAILABLE
```
That is not attacker hardening. It means an ordinary Windows cell whose OS recycles a terminated TID can never produce admissible evidence.

Fix class: **ETW_THREAD_LIFETIME_REUSE_BINDING** — permit disjoint lifetimes for one TID and resolve each CSwitch by TID + observation QPC inside exactly one lifetime. No new subsystem. Because the frozen evaluator carries the same uniqueness assumption, this requires the appropriate owner-gated frozen-layer amendment/re-review.

### F2 — EXECUTED / UNSEARCHED — SETTLED-BY-PINNED-BYTES — thread/process interval containment is not checked
**Data consequence: ADMITS WRONG EVIDENCE, with a direct route to wrong instruction attribution.**

`bind_thread_start_keys()` claims to bind by PID + QPC interval, but mechanically it only chooses the latest ProcessStart for that PID whose start is not later than the thread event. It never asks whether that process incarnation has already stopped.

```
PID 5000 / key AA: ProcessStart qpc 10, ProcessStop qpc 40
PID 5000 / key BB: ProcessStart qpc 60, ProcessStop qpc 90
Thread 303: START qpc 50, STOP qpc 55        <- no incarnation alive at 50-55

bind_thread_start_keys -> binds thread 303 to stale incarnation AA
assemble_thread_lifetimes -> ADMITTED {5000, AA, 303, 50, 55}
```

The same omission exists downstream: the frozen validator checks the (process_id, process_start_key) pair exists and that the thread lifetime is monotonic, but never `process.started_qpc <= thread.started_qpc` and `thread.ended_qpc <= process.ended_qpc`.

Attacking the signed production-shaped verifier directly — an otherwise valid collection with the thread start moved 1,000 QPC ticks before its signed process start, then signed:
```
process interval = 1000000 .. 1020000
thread interval  =  999000 .. 1019990
production_admission_errors = []
WRONG_EVIDENCE_ADMITTED = True
```
That is the round's north-star failure in its cleanest form: an impossible process/thread relationship accepted as production evidence.

Fix class: **ETW_PROCESS_THREAD_INTERVAL_CONTAINMENT** — the binder/assembler and the frozen physical-evidence validator must require a thread lifetime to fit inside exactly one matching PID/start-key process lifetime. No new machine.

### F3 — EXECUTED / SEARCHED — valid RFC 7468 PEM carriers can block the owner ceremony
**Data consequence: REFUSES RIGHT EVIDENCE; a correct owner root can be rejected before the experiment can activate.**

The decoded-key identity fold itself is good: `public_key_identity()` extracts the Ed25519 public point, so textual re-encoding does not change key identity. The newly added carrier restriction goes too far — `OwnerTrustAnchor.__init__` and `strict_public_key_carrier_ok()` effectively require one exact textual form (BEGIN line + `\n`, one canonical base64 line + `\n`, END line + `\n`).

RFC 7468 requires parsers to handle different newline conventions including CRLF, and its ABNF permits the final post-boundary EOL to be absent.

Fresh Ed25519 SPKI generated with node:crypto — the same mechanism the BUILD itself uses — and not in the committed-key census:
```
Native export:                       strict_public_key_carrier_ok = True; OS-config production context ADMITTED
Same decoded point, LF -> CRLF only: same_identity = True; OS-config path -> OWNER_TRUST_ANCHOR_INVALID
Same decoded point, no final EOL:    same_identity = True; OS-config path -> OWNER_TRUST_ANCHOR_INVALID
```
Tested through the actual `MBCX01_BUILD_OWNER_TRUST_ANCHOR` configuration path using transient temp files, not merely the helper function. The defect is treating a permissible text transport spelling as scientific authority.

Fix class: **RFC7468_OWNER_KEY_TEXT_NORMALIZATION** — accept the RFC-permitted line endings/final-EOL forms, normalize internally, and retain the decoded Ed25519-point identity, canonical base64/DER semantics, committed-key check and every authority check. No new parser subsystem.

## Claims that survived fresh attack

- **Item 1 — AMENDMENT-1: EXECUTED.** Fresh owner_role and subject_id same-cut substitutions now produce I02=False and score 0. Removing the two newly bound fields from a control copy of the canonical world did not change legal-action derivation or the gold action. No score/gold ripple defect.
- **Item 2 — ETW drain/loss: EXECUTED / SEARCHED.** A fresh fake real-time API returning legitimate ERROR_CTX_CLOSE_PENDING drained, queried loss before STOP, stopped and captured successfully. A CloseTrace error produced ETW_TRACE_DRAIN_INCOMPLETE, still performed STOP, and capture remained refused. A post-stop loss query is refused by name.
- **Item 3 — PID reuse: EXECUTED.** For ordinary PID reuse with two distinct incarnations and correctly timed thread events, the binder chose AA for the first and BB for the second even when process-event arrival order was scrambled. The class is nevertheless not closed because F1 and F2 expose the missing TID-reuse and full-interval axes.
- **Items 4–5 — key identity/harvest: EXECUTED.** A fresh in-memory production signing key was absent from the five-key committed census and admitted normally. The known committed measurement signing key was identified as coming from MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json and refused PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL. The identity/harvest direction works; F3 is specifically its false-refusal inverse.
  - I also note `committed_fixture_key_material()` derives its census from the LIVE MODULE DIRECTORY, not Git objects. Under the currently defined run path this is not a finding: the pinned reconstruction contains the committed fixture documents and the ceremony/smoke workflow operates from that artifact. **If a future packaged deployment strips fixture files, this class must be re-reviewed** because "committed-key census" would no longer mean the pinned committed census.
- **Item 6 — positive-lane swap: EXECUTED.** I disabled `committed_fixture_key_document()` in memory and reran bw57 and ba36. Both went RED because the formerly refused committed signing key admitted. The positive-lane move to fresh in-memory keys did not make those witnesses decorative.
- **Item 7 — frozen count: EXECUTED.** Forcing the frozen-suite count to 146 produced `VerificationFailure: frozen r13.2 suite total changed: 146 != 147`; 147 passes. The count is what the packet says it is — a declaration gate, not a byte-authenticator. Byte identity is separately handled by the pin manifest, which I independently reconstructed at fce7b355…, exit 0.

## Residual risks

- The physical ETW consumer remains unexecuted against a real Windows session; that is the packet's explicit non-claim.
- The machine-wide Kernel-Process provider / non-idle-host abort remains the packet's named open risk. I did not promote it because I did not demonstrate a wrong number, wrong admission, or false refusal beyond the already-declared behavior.
- The production exactness witness runner remains unbuilt and honestly labelled.
- In-process mutation/evasion remains outside the threat model and I did not use it as review evidence.
- WPR/Xperf demonstrates that InstructionRetired→CSwitch acquisition is established Windows functionality; the remaining physical questions are about this harness's evidence semantics and the target platform.

## Fix class

Three bounded classes block acceptance:
1. **ETW_THREAD_LIFETIME_REUSE_BINDING** — allow legitimate recycled TIDs and select lifetimes by TID + QPC interval.
2. **ETW_PROCESS_THREAD_INTERVAL_CONTAINMENT** — require every thread lifetime to lie inside exactly one matching process incarnation.
3. **RFC7468_OWNER_KEY_TEXT_NORMALIZATION** — do not reject a correct owner key solely for CRLF or an omitted final EOL.

F1/F2 change the ETW/frozen evidence-consumer semantics; F3 changes the production anchor admission parser. Under the packet's §13 trigger, these require a fresh council round on the folded bytes.

Bottom line: AMENDMENT-1 is good, the drain/loss repair is good, the committed-signing-key isolation is materially better, and the rebuilt witnesses discriminate. But the instrument still accepts an impossible process/thread evidence relation, rejects legitimate Windows TID reuse, and can reject a standards-valid owner key before the ceremony starts. Those are exactly the wrong-evidence / right-evidence failures section 0 makes load-bearing. **NO-GO.**
