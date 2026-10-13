NO-GO

Verdict basis: EXECUTED. The pinned artifact can refuse valid Windows evidence, admit an impossible process/thread attribution as a 30-instruction delta, refuse a standards-conforming owner key, and falsely certify a replaced frozen suite.

## Evidence read

- `git rev-parse HEAD` → `d122ee10e19a0fa9288c0aa8594494c1476a9fb4`.
- Packet read as committed at `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r5.md:1-251@d122ee10`.
- Review target confirmed as `fce7b3551d228e91b77814fdb3d3296c3d7ee08b` at packet lines 43-47.
- `git diff --name-status fce7b355… HEAD` shows only the r5 packet added and `MBCX-01-BUILD-PIN-MANIFEST.json` changed. All reviewed code, tests, and governing documents match the target pin byte-for-byte. I read those matching working-tree bytes after confirmation.
- Final status contained only two untracked prompt/log files; I made no repository writes.
- No-threat-model spot check against the three governing documents returned zero matches. This is a scientific-validity review, not a security review.
- Governing bytes:
  - `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:5-48,85-87@fce7b355`
  - `MBCX-01-EXPERIMENT-DESIGN-r9.md:7-48@fce7b355`
  - `MBCX-01-R13-CLOSURE-ARCHITECTURE.md:70-118@fce7b355`
  - `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:134-191@fce7b355`
- Load-bearing implementation:
  - `mbcx01_build_etw_consumer.py:895-1102,1318-1366,1626-1692@fce7b355`
  - `mbcx01_build_win32.py:386-560@fce7b355`
  - `mbcx01_r13_measurement.py:928-991@fce7b355`
  - `mbcx01_build_trust_anchor.py:276-305,316-412,547-626,646-719@fce7b355`
  - `mbcx01_build_measurement_authority.py:360-376@fce7b355`
  - `mbcx01_r13_packets.py:68-115@fce7b355`
  - `verify-build-bundle.py:49-60,120-132,251-267@fce7b355`
- Tests and shelf:
  - `test_mbcx01_r13_packets.py:117-196@fce7b355`
  - `test_mbcx01_build_measurement.py:1446-1725,2391-2690@fce7b355`
  - `MBCX-01-BUILD-SHELF-LOG.md:14-63@fce7b355`
  - Bridge prior art at `878e53a…`: `src/crl/crl-authenticate.ts:15-20,109-123`; `src/crl/der-reader.ts:203-239`.
- Installed vendor header: Windows SDK `10.0.26100.0/um/evntcons.h:51-69,148-157`, confirming PMC `0x0008`, event key `0x000A`, process start key `0x000D`, and classic-header flag `0x0100`.

## SWEEP LOG

Exact web queries:

- `site:learn.microsoft.com "After a thread has terminated, its ID may be reused"`
- `site:learn.microsoft.com TracePmcEventListInfo CSwitch EVENT_HEADER_EXT_TYPE_PMC_COUNTERS`
- `site:rfc-editor.org RFC 7468 CRLF parsers MUST handle different newline conventions`
- `site:cwe.mitre.org/data/definitions/1291 debug production key`
- `site:learn.microsoft.com/en-us/windows-hardware/test/wpt "Recording PMU Events" CSwitch`
- `site:learn.microsoft.com/en-us/windows-hardware/test/wpt WPR hardware performance counters CSwitch`
- `site:learn.microsoft.com/en-us/windows/win32/etw CSwitch old thread id`
- `site:learn.microsoft.com EVENT_TRACE_TYPE_START thread event process id thread id`

Opened at origin:

- [Microsoft PsGetThreadId, Remarks](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-psgetthreadid): thread IDs may be reused after termination. This converted TID reuse from a hypothetical into an applicable Windows sequence.
- [Microsoft Thread Handles and Identifiers](https://learn.microsoft.com/en-us/windows/win32/procthread/thread-handles-and-identifiers): identifier validity ends at thread termination.
- [Microsoft TRACE_QUERY_INFO_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class): confirms `TracePmcEventListInfo=8` and `TracePmcCounterListInfo=9`.
- [Microsoft EVENT_HEADER_EXTENDED_DATA_ITEM](https://learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header_extended_data_item): confirms current PMC snapshots and boot-unique process start keys.
- [Microsoft CloseTrace](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-closetrace): confirms real-time draining behavior after `ERROR_CTX_CLOSE_PENDING`.
- [Microsoft WPR Counters](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/counters), Example: WPR already attaches `InstructionRetired` to `CSwitch`. It confirms external acquisition prior art, but not the experiment’s signed membership/evidence join.
- [RFC 7468](https://www.rfc-editor.org/info/rfc7468/), status plus §§2, 3, 13, 14: current Standards Track; parsers must handle newline conventions, and its ABNF permits CRLF, CR, or LF. Canonicalization should occur after decoding.
- [RFC 8410](https://www.rfc-editor.org/info/rfc8410/), §§3-4: Ed25519 SPKI structure and absent parameters. [RFC 9295](https://www.rfc-editor.org/info/rfc9295/) updates certificate key-usage semantics, not this SPKI encoding rule.
- [RFC 4648](https://www.rfc-editor.org/info/rfc4648/), §3.5: confirms canonical base64 pad-bit handling.
- [MITRE CWE-1291](https://cwe.mitre.org/data/definitions/1291.html), Potential Mitigations: use different production and debug keys at implementation time. This confirms the committed-key refusal’s intended class.

Internal shelf spot-run:

`rg -il -e 'EVENT_TRACE|TracePmc|CSwitch|ProcessTrace' -- <root>`

Across bridge `src/` at `878e53a…`, Photon `crates/` at `0b916f3…`, and Gravity `src/` at `c16bd03…`: zero files in all three. I also opened the bridge’s structural SPKI reader. The packet carries a substantive internal-shelf log; this independent query confirmed its ETW result.

Stopped because Microsoft settles thread-ID lifetime and ETW ABI, the RFC Editor settles PEM/SPKI applicability and status, MITRE settles the cited key-reuse class, and the remaining platform behavior requires the expressly prohibited elevated live run.

## Build-decision challenge

1. **ALREADY-BUILT — EXECUTED; SEARCHED.** Structural SPKI parsing already existed internally and was adopted. WPR already supplies CSwitch-attached PMCs externally, but it does not supply the signed Job-member/lifetime/authority join this experiment requires. No internal ETW counterpart was found by the spot-run, so the bounded custom join is justified.

2. **PRODUCT-FIT — READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES.** Customer need, in one sentence: this instrument gives the owner a defensible measurement or an explicit UNDETERMINED result when the evidence cannot support one. That is governed-power/fail-loud/mirror-not-cop, although the current false refusals violate that posture in execution.

3. **BIGGER-THAN-THE-BUG — READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES.** No new subsystem was introduced; the folds are bounded changes inside existing projection, ETW, trust, authority, fixture, and verifier functions. Amendment-1 has a recorded owner ruling. The required fixes below can remain bounded.

## Execution

Baseline:

- BUILD suites: `125/125 OK`.
- Frozen suites: `147/147 OK`.
- `verify-build-bundle.py`: real exit `0`; 46 invariants, 125 witnesses, `two_way_total=true`, readiness unchanged.
- These ran from the working tree, whose verifier inputs were confirmed identical to `fce7b355…`; the two differing HEAD files are not verifier inputs.

Fresh probes:

- Amendment: changing only `subject_id` and `owner_role` changed exactly those projected fields and the world hash, while legal actions remained identical.
- ETW faults: event loss, absent PMC data, and malformed PMC data refused by name.
- TID reuse: two sequential lifetimes for TID 777 bound to the correct two process start keys, then failed `ETW_THREAD_LIFETIME_DUPLICATE_START:777`.
- Process gap: a thread at QPC 25–27 was bound to a process that ended at QPC 20 and contributed an admitted delta of 30.
- Key inverse: Node generated a fresh Ed25519 key. Its LF and CRLF PEM forms produced the same decoded identity; OpenSSL 3.5.6 accepted CRLF, while the harness returned `OWNER_TRUST_ANCHOR_INVALID`.
- Harvest: five current fixture keys found; the committed anchor mapped to its fixture document; a fresh key was absent.
- Positive-lane swap: fresh in-memory signing material produced no admission errors; committed signing material produced `PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL`.
- Frozen guard: an in-memory module containing 147 unrelated no-op tests returned `status: PASS`.

## Findings

1. **EXECUTED; SEARCHED — valid TID reuse refuses right evidence.**

   `assemble_thread_lifetimes` stores starts and stops solely by TID and rejects a second start (`mbcx01_build_etw_consumer.py:1052-1102`). `consume_cswitch` and the frozen validator also map solely by TID (`mbcx01_build_win32.py:536-556`; `mbcx01_r13_measurement.py:946-960`). Microsoft explicitly permits TID reuse after termination.

   Data consequence: a legitimate Windows capture containing sequential TID reuse is rejected, so the experiment refuses right physical evidence and cannot produce a number for that cell.

2. **EXECUTED; SEARCHED — start-only binding admits a thread outside its process lifetime and produces a wrong number.**

   `bind_thread_start_keys` claims PID+QPC interval binding but considers only starts and selects the last non-future start (`mbcx01_build_etw_consumer.py:992-1036`). It does not use ProcessStop. The assembler checks only that the PID/start-key pair exists, and the frozen validator never checks that a thread lifetime is nested inside its process lifetime.

   The fresh sequence bound QPC 25–27 to a process ending at QPC 20 and admitted a 30-instruction delta.

   Data consequence: inconsistent cross-stream evidence is admitted and produces a wrong number instead of `UNAVAILABLE`.

   Governing-source conflict: the packet says “PID + QPC interval”; the pinned implementation bytes and executed result win on what the artifact actually does.

3. **EXECUTED; SEARCHED — a legitimate CRLF owner-key carrier is falsely refused.**

   `OwnerTrustAnchor` and `strict_public_key_carrier_ok` require literal LF framing (`mbcx01_build_trust_anchor.py:282-297,592-626`). RFC 7468’s strict grammar still permits CRLF, CR, or LF, and the ceremony contract says SPKI PEM without narrowing it to LF.

   The fresh LF and CRLF values carried the identical Ed25519 point; OpenSSL parsed CRLF successfully; the harness rejected it.

   Data consequence: a legitimate owner anchor can be refused during ceremony activation, preventing right evidence from entering the experiment at all.

   Governing-source conflict: the pinned bytes decide that rejection occurs; current RFC 7468 plus the non-narrowed ceremony contract decide that CRLF is legitimate.

4. **EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES — the frozen guard does not detect arbitrary same-count changes.**

   `check_frozen_suites` runs the configured modules and compares only `testsRun` with 147 (`verify-build-bundle.py:251-267`). It has no module-byte, test-name, or hash binding. A wholly replaced 147-test suite passed.

   Data consequence: the verifier admits wrong evidence that the frozen suite is unchanged; a same-count removal or replacement of an invariant witness can pass and permit a changed join to produce a wrong number.

   Governing-source conflict: packet item 7 says the guard fails on any frozen-suite change; the pinned function and executed replacement prove that claim false.

## Claims cleared, with residuals

- **Item 1 — EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES:** amended fields bind and did not change legal actions in the fresh probe. Residual: this establishes the enumerated consumers, not semantic completeness beyond the frozen net.
- **Item 2 — EXECUTED; SEARCHED:** loss, absent PMC, and malformed PMC paths fail by name; CloseTrace/drain code agrees with Microsoft’s documented behavior. Residual: no live session was run.
- **Item 5 — EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES:** the present five-key harvest and fresh-key inverse behaved as claimed. Residual: the function scans the runtime directory, not Git objects; extra or omitted `*.fixture.json` files can make the runtime set differ from the committed set.
- **Item 6 — EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES:** fresh positive signing keys passed and committed signing material failed by name. Residual: this covers current authority gates, not unenumerated future witnesses.

## Residual risks

- **READ-ONLY; SEARCHED:** live ETW acquisition, real buffer ordering, PMC baseline semantics, capability truthfulness, and final drain/loss timing remain UNDETERMINED because the authorized lane forbids starting a session.
- **READ-ONLY; UNSEARCHED — COULD-NOT:** no real HSM export or owner ceremony was available; Node and OpenSSL covered only the key-carrier boundary.
- **READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES:** the per-witness exactness executor remains unbuilt, as expressly non-claimed.
- **READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES:** the known machine-wide Kernel-Process/foreign-process abort risk remains; no evidence here shows it silently corrupting a count.

Fix class: **THREAD-LIFETIME-INTERVAL-IDENTITY/JOIN + PEM-EOL-NORMALIZATION + FROZEN-SUITE-BYTE-BINDING**.

Bounded correction required:

- Represent non-overlapping repeated TID lifetimes and resolve each CSwitch by `(TID, QPC)`; require the selected thread interval to be nested in the same PID/start-key process interval.
- Normalize permitted PEM EOL conventions before canonical base64/DER/SPKI validation.
- Bind frozen suite module bytes or authenticated blob hashes, not only the total test count.
