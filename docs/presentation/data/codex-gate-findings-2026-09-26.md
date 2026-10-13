# The codex-CLI gate: the final findings block of each of the nine rounds

Excerpted for this public copy from the nine gate logs of the working repository at commit e47c1c5, at the line ranges the data record names (`codex_cli_gate.findings_block_lines`). The raw logs are withheld from the public copy because their tool output quotes private repositories; each excerpt below is the log's own final findings block, passed through the same redaction as the rest of this copy. Line numbers are the raw log's.


## r1 — `MBCX-01-CODEXCLI-r1-FULL-LOG-2026-08-15.log` lines 12202-12214

```text
- [P1] Bind exactness to the current envelope preimage — <repo>-build\mbcx01_build_exactness_authority.py:135-139
  When a signed envelope's `receipt` is edited after signing, this code verifies the unchanged `receipt_preimage_b64` and signature, but `_production_envelope_bindings` derives the returned binding from the edited receipt. A stale signed payload can therefore authorize an arbitrary current carrier/grid binding; compare the supplied preimage and digest to `producer.production_receipt_preimage(envelope)` before deriving these fields.

- [P1] Derive valid parent identities for live ProcessStart events — <repo>-build\mbcx01_build_etw_consumer.py:2053-2055
  For every live ProcessStart this assigns an integer parent ID and `None` parent key, including the measured root. The physical-evidence validator requires both root parent fields to be `None` and every descendant's exact parent tuple to identify a roster member, so live captures produce `PROCESS_MEMBERSHIP_INVALID`; special-case the root and resolve descendant parent start keys from the process-incarnation stream.

- [P1] Scope process events to the measured Job — <repo>-build\mbcx01_build_etw_consumer.py:1891-1895
  When unrelated processes or threads emit events during the live session, this machine-wide provider has no PID or Job filter, while the callback forwards every event to member/thread assembly. Foreign processes then disagree with the Job's `TotalProcesses`, and foreign threads can fault as `ETW_THREAD_START_KEY_UNBINDABLE`, so normal host activity prevents physical collection; filter or partition events to the measured Job before assembly.

- [P2] Reconcile the pin manifest before reporting PASS — <repo>-build\verify-build-bundle.py:270-273
  When a frozen test or module is changed without altering the 150-test count, this check still returns PASS because `main()` never reconciles `MBCX-01-BUILD-PIN-MANIFEST.json` or invokes the pinned verifier. The generated BUILD report can therefore certify drifted bytes; validate the current blobs and hashes against the manifest before reporting the suite as passing.

- [P2] Keep reader routing unique per in-memory store — <repo>-build\mbcx01_build_state_store.py:270-270
```


## r2 — `MBCX-01-CODEXCLI-r2-FULL-LOG-2026-08-15.log` lines 15854-15872

```text
- [P1] Parse profile-source names on WCHAR boundaries — <repo>-build\mbcx01_build_etw_consumer.py:2088-2090
  When preflight enumerates the normal UTF-16LE name `InstructionRetired`, splitting on the unaligned byte sequence `b"\x00\x00"` matches across the final ASCII character and its terminator, producing `InstructionRetire`; additionally, a final chained entry after offset zero gets an empty slice. The source lookup therefore reports `ETW_PMC_SOURCE_UNAVAILABLE` even when the source exists, so parse nulls on two-byte boundaries and treat `NextEntryOffset == 0` as the end of the buffer.

- [P1] Decode PMC ownership rows instead of testing raw bytes — <repo>-build\mbcx01_build_etw_consumer.py:2149-2149
  On a Windows host with available PMCs, `ETW_PMC_COUNTER_OWNERSHIP_STATUS` contains a nonzero `NumberOfCounters` even when every counter has `OwnerType == EtwPmcOwnerFree`, so `any(buffer)` reports a conflict on a healthy machine. The query is also per-processor and expects an input buffer sized from the maximum-counter query; decode those owner rows for each processor rather than treating any nonzero metadata byte as ownership.

- [P1] Scope machine-wide CSwitch records before attribution — <repo>-build\mbcx01_build_etw_consumer.py:2468-2468
  When any unrelated host thread context-switches during the machine-wide trace, the root-scoping branch removes that thread's process/thread lifetimes but still returns all CSwitch records here. `consume_cswitch()` then requires every `old_thread_id` to resolve to a member lifetime and raises `ETW_CSWITCH_UNATTRIBUTED_THREAD`, so a normal busy host aborts the collection; foreign switches must remain only for per-processor counter baselines and not be emitted as member-attributed deltas.

- [P1] Populate retired instructions from the ETW deltas — <repo>-build\mbcx01_build_win32.py:822-822
  Every physical collection returns this scalar as zero, and no later code updates it before `produce_signed_measurement_receipt_v2()` copies it into the job receipt. The evidence tree independently contains the summed CSwitch deltas, while admission requires `retired_instructions > 0` and equality with that sum, so every real envelope is rejected; populate this value from the recomputed observations before returning the collection.

- [P1] Use one interval for elapsed-time cross-checking — <repo>-build\mbcx01_build_measurement_authority.py:548-548
  For a physical run, `collect()` starts its elapsed QPC after `CreateProcessW` and job/session setup, whereas the signed lifetime span starts at the earlier ETW ProcessStart timestamp and ends at ProcessStop before the final QPC query. These are different intervals, so requiring `elapsed_qpc_ticks == span` makes every live envelope fail `MONOTONIC_TIME_CROSS_CHECK_FAILED`; derive both values from the same endpoints or validate their intended containment instead.

- [P2] Keep optional completion messages off the critical path — <repo>-build\mbcx01_build_win32.py:708-708
  When the diagnostic `ACTIVE_PROCESS_ZERO` message is omitted, which the surrounding contract explicitly permits, this call waits before reaching the load-bearing root/job barrier. With `collect()`'s default `INFINITE` timeout it hangs forever, and the smoke path needlessly waits 60 seconds; drain diagnostics non-blockingly or under one overall deadline while using the job queries as the actual barrier.

- [P2] Parse quoted executable paths before hashing — <repo>-build\mbcx01_smoke_cell.py:350-350
```


## r3 — `MBCX-01-CODEXCLI-r3-FULL-LOG-2026-08-15.log` lines 20511-20538

```text
- [P1] Decode Kernel-Process events by their actual versioned schema — <repo>-build/mbcx01_build_etw_consumer.py:2809-2809
  On real Microsoft-Windows-Kernel-Process ProcessStart/Stop events, the payload begins with a 32-bit `ProcessID`; it is never a `<QI>` start-key/PID pair. This therefore derives both identities from unrelated PID/time or sequence bytes, so the captured root cannot match the known root identity and every physical collection aborts. Decode the provider's event-version template and obtain the start key from the appropriate sequence or extended-data field.

- [P1] Refuse unauthenticated non-work-tree verification — <repo>-build/verify-build-bundle.py:383-389
  When this script is invoked directly from an extracted non-Git directory without a pin manifest, this branch reports PASS and claims authentication by `verify-build-pinned.ps1` even though that launcher may never have run. Since a legitimate pinned reconstruction always exports the manifest, this permits unpinned copied bytes to produce a green pin section; fail this posture rather than claiming launcher authentication.

- [P1] Validate the envelope before accepting the expected red — <repo>-build/mbcx01_smoke_cell.py:442-447
  The fixture manifest is non-production and custody is always empty, so `evaluate_production_measurement` returns at its trust/custody gate before examining `envelope`; consequently even `verify_envelope({})` sets `pass_criterion_met` to true. The smoke runbook requires a structurally valid signed envelope, so validate its structure, signature, and evidence independently before treating the expected production refusal as a pass.

- [P1] Enforce the writer gate across processes — <repo>-build/mbcx01_build_state_store.py:298-300
  `_OPEN_WRITERS` is process-local, so two producer processes can simultaneously open the same WAL database as writers. Both can then calculate the same `MAX(seq) + 1` before either begins its write transaction, producing duplicate journal sequence numbers and violating the advertised single-writer invariant. Use an interprocess file lock or durable database lease for the writer door.

- [P2] Fail execution when the smoke criterion is false — <repo>-build/mbcx01_smoke_cell.py:321-324
  If verification returns no errors or omits the expected sentinel, `verify_envelope` records `pass_criterion_met: false`, but `execute` merely stores that result and returns; `main` then reports `status: OK` with exit code 0. Raise `SmokeAbort` or otherwise return nonzero when the declared smoke pass criterion is not met.

- [P2] Stop the ETW session when the loss query fails — <repo>-build/mbcx01_build_etw_consumer.py:2408-2414
  If `ControlTraceW(EVENT_TRACE_CONTROL_QUERY)` fails after a session has started, `_query_loss()` raises before the STOP block executes, leaving the system logger active and potentially blocking subsequent runs. Preserve the unknown-loss fault, but place session teardown in a `finally` so the logger is always stopped.

- [P2] Terminate suspended roots that never enter the job — <repo>-build/mbcx01_build_win32.py:813-817
  If job creation, configuration, completion-port setup, or `AssignProcessToJobObject` fails after `CreateProcessW` succeeds, the child remains suspended but unassigned. Closing its process and thread handles does not terminate it, and `KILL_ON_JOB_CLOSE` cannot affect an unassigned process, so these setup failures leak an indefinitely suspended child; explicitly terminate it unless assignment succeeded.

- [P2] Inspect database identity before creating store tables — <repo>-build/mbcx01_build_state_store.py:316-317
  When `path` points to an existing unrelated SQLite database, these statements add all state-store tables before any application ID or persisted identity is checked; because the newly created `meta` table is empty, the following branch then adopts that database as a valid store. A mistaken path therefore mutates and claims an unrelated database instead of refusing it; inspect pre-existing schema/application identity before initialization.

- [P2] Preserve spaces in Git Start-Process arguments — <repo>-build/verify-build-pinned.ps1:50-50
  When the repository path contains spaces, `Start-Process` joins this argument array without preserving quoting, so Git receives only the path prefix as the `-C` value and blob extraction fails. Quote the repository argument explicitly or invoke Git without `Start-Process`; the equivalent helper in `generate-build-pin-manifest.ps1` needs the same correction.

- [P2] Convert signature-verifier failures into closed verdicts — <repo>-build/mbcx01_build_state_authority.py:862-866
```


## r4 — `MBCX-01-CODEXCLI-r4-FULL-LOG-2026-08-16.log` lines 51092-51107

```text
- [P1] Bind authorization to the requested smoke run — <repo>-build\mbcx01_build_win32.py:722-724
  When a document merely contains this marker, the gate accepts it without checking the command line, host, cell, or destination that the authorization named, despite the bounded scope required by `MBCX-01-BUILD-SMOKE-RUNBOOK.md` §3. A stale authorization for the harmless default cell can therefore be replayed to launch a different elevated workload or write elsewhere; parse the authorized scope and reject mismatches before `CreateProcessW`.

- [P2] Inspect database identity before changing journal mode — <repo>-build\mbcx01_build_state_store.py:330-331
  When `path` names an unrelated SQLite database, this persistent `journal_mode=WAL` change occurs before the application-id/table checks, so the subsequent `STATE_STORE_FOREIGN_DATABASE` refusal still modifies another application's database. A tableless database carrying only a nonzero `user_version` is even silently adopted because that value is overwritten by the later schema initialization; inspect all identity signals through a non-writing connection before applying PRAGMAs or DDL.

- [P2] Reject malformed custody lists without raising — <repo>-build\mbcx01_build_state_authority.py:545-545
  With an otherwise valid receipt and exact-key custody object, a list such as `signer_key_ids=[valid_id, {}]` reaches this expression and raises `TypeError` because the dictionary is unhashable. Since custody evidence is caller-supplied and the public verifier promises a closed error list for every input, validate every list element before constructing sets or catch the failure at the public boundary.

- [P2] Snapshot artifact digests before launching the candidate — <repo>-build\mbcx01_smoke_cell.py:432-436
  Because `harness_identity()` and `_candidate_digest()` first read their files after `collect()` has completed and unsigned evidence has been written, an updater or other process can replace the candidate or harness source during the run and the signed envelope will bind the post-run bytes rather than those that produced the capture. Resolve and hash or hold the relevant files before launch, and ensure that exact resolved image is passed to process creation.

- [P2] Mirror CreateProcessW executable resolution — <repo>-build\mbcx01_smoke_cell.py:518-521
  For an extensionless command such as `cmd /c exit 0`, `CreateProcessW(None, ...)` successfully appends `.exe` and launches `cmd.exe`, but this search looks only for the literal file `cmd` in `PATH`. The physical collection therefore completes and is persisted before certification aborts with `CANDIDATE_BINARY_NOT_FOUND`; use Windows/PATHEXT resolution and carry the same resolved path into process launch.

- [P2] Prevent duplicate live store identities — <repo>-build\mbcx01_build_state_store.py:401-401
```


## r5 — `MBCX-01-CODEXCLI-r5-FULL-LOG-2026-08-16.log` lines 53129-53138

```text
- [P1] Reject non-calendar validity timestamps — <repo>-build\mbcx01_build_measurement_authority.py:233-236
  `TIMESTAMP_RE` checks only digit placement and then orders timestamps as strings, so a window such as `2020-00-00T00:00:00Z` through `2030-99-99T99:99:99Z` is considered valid. When the manifest and custody activation are regenerated over those values, `evaluate_production_measurement` returns `[]` at a 2026 verifier instant, allowing a malformed date to extend production trust instead of invalidating it; parse and calendar-validate both endpoints before comparison.

- [P2] Return a closed verdict for malformed state receipts — <repo>-build\mbcx01_build_state_authority.py:842-845
  When an exact-key receipt contains canonical JSON that is a dictionary but not a valid state, such as `prestate_read.state_utf8 == "{}"`, `_structural_errors` marks it nonfatal and this unguarded call eventually reaches `_semantic_errors`, where `common.current_cut` raises `KeyError('next_seq')`. This violates the documented closed-list behavior for caller-supplied material, so malformed or corrupted receipts can crash verification instead of returning the schema rejection and sentinel.

- [P2] Validate scenario IDs before deduplicating them — <repo>-build\mbcx01_build_cohort_authority.py:551-553
  A candidate can retain the exact expected key set while carrying an unhashable `scenario_id`, such as a dictionary. Provenance derivation records the mismatch, but `set(ids)` then raises `TypeError` before the closed error list is returned, so malformed population input crashes this validation boundary instead of yielding `BUILD_CANDIDATE_SCHEMA_INVALID`; validate the ID type and grammar before uniqueness checking.

- [P2] Compare state validity windows as parsed instants — <repo>-build\mbcx01_build_state_authority.py:527-530
```


## r6 — `MBCX-01-CODEXCLI-r6-FULL-LOG-2026-08-16.log` lines 29947-29959

```text
- [P1] Follow CreateProcessW when resolving extensionless candidates — <repo>-build/mbcx01_smoke_cell.py:701-701
  When an extensionless token has both `foo.COM` and `foo.EXE` in the same searched directory, the default PATHEXT ordering makes this resolver choose and rewrite the launch to `.COM`. `CreateProcessW(NULL, "foo ...")` does not apply PATHEXT; it appends `.exe`, so preflight changes which program the operator requested and then hashes and certifies the wrong candidate. Restrict extensionless resolution to CreateProcessW's `.exe` behavior.

- [P2] Match STOP events to the starting process incarnation — <repo>-build/mbcx01_build_etw_consumer.py:1528-1528
  When one TID's START names member process A but its STOP names member process B, this branch retains only the QPC. The later time-sorted zip closes A's lifetime with B's STOP and emits evidence under A despite the event carrying a different process pair. Preserve and compare the process identity on STOP while pairing lifetimes.

- [P2] Reject malformed nested states before reducer replay — <repo>-build/mbcx01_build_state_authority.py:312-312
  When `state_utf8` contains every top-level key but a nested scope value is `null`, this predicate accepts it because `scopes` itself is a dict; reducer replay then raises a raw `TypeError`. This violates the verifier's documented closed-list behavior and lets malformed receipt material abort callers instead of returning `STATE_AUTHORITY_V2_SCHEMA_INVALID` with the sentinel. Validate the nested state shape before replay.

- [P2] Validate cut-state mappings before iterating them — <repo>-build/mbcx01_build_cohort_authority.py:516-516
  With an otherwise hash-valid provenance and a JSON candidate whose `canonical_state_by_cut` is a scalar such as a string, this loop calls `.values()` before the later candidate-schema check. `validate_build_source_provenance` consequently raises `AttributeError` instead of returning the closed `BUILD_CANDIDATE_SCHEMA_INVALID` verdict. Guard this value as a mapping or defer traversal until schema validation.

- [P2] Preserve the primary error when ETW cleanup fails — <repo>-build/mbcx01_smoke_cell.py:550-550
```


## r7 — `MBCX-01-CODEXCLI-r7-FULL-LOG-2026-08-16.log` lines 18950-18959

```text
- [P1] Configure PMC before starting the trace pump — <repo>-build\mbcx01_build_etw_consumer.py:2687-2687
  On a physical run, `start()` enables CSwitch and starts `ProcessTrace` here, while `execute()` calls `configure_pmc()` only after `start()` returns. Any context switch delivered in that interval lacks the PMC extended-data item, so `_on_event_record` records `ETW_PMC_EXTENDED_DATA_ABSENT` and `capture()` rejects the entire one-shot run. Attach the counter before opening the consumer.

- [P1] Apply CreateProcessW's path-sensitive extension rule — <repo>-build\mbcx01_smoke_cell.py:752-754
  This candidate list is used for both bare names and names containing a path, but CreateProcessW appends `.exe` only to a bare extensionless name; an extensionless path is used verbatim. Thus, given `C:\dir\tool` and `C:\dir\tool.exe`, preflight selects, hashes, and rewrites the launch to `tool.exe` even though the requested command would run `tool`; conversely, the bare-name fallback can launch an extensionless file that the original command would not find. Generate candidates based on whether the token contains a path and remove the bare fallback.

- [P2] Decode the parent identity from the ProcessStart payload — <repo>-build\mbcx01_build_etw_consumer.py:3227-3228
  For brokered or explicit-parent process creation, the event-emitting context can differ from the parent declared by ProcessStart, but this records `EventHeader.ProcessId` and discards the payload's authoritative parent tuple. The supported v3/v4 payload already contains `ParentProcessID` and `ParentProcessSequenceNumber` at offsets 20 and 24; because `member_tree_incarnations()` uses this value to define Job membership, the current decode can omit legitimate descendants or include a foreign process and invalidate the grid.

- [P2] Model CreateProcessW's unquoted-path search — <repo>-build\mbcx01_smoke_cell.py:643-644
```


## r8 — `MBCX-01-CODEXCLI-r8-FULL-LOG-2026-08-17.log` lines 17412-17418

```text
- [P1] Escape file paths before constructing SQLite URIs — <repo>-build\mbcx01_build_state_store.py:379-379
  When a file-backed path contains a legal Windows URI metacharacter such as `#` or a percent escape, passing this hand-built string with `uri=True` makes SQLite parse the pathname as a URI rather than use it literally; for example, `a#b.sqlite` opens `a`. This bypasses `refuse_foreign_database()` checking the requested path and can read or mutate an unrelated database. URI-encode the path or avoid URI mode for writable connections, and apply the same correction to the read-only URI.

- [P1] Enable CSwitch only after attaching the PMC counter — <repo>-build\mbcx01_build_etw_consumer.py:2704-2705
  On a live Windows run, `StartTraceW` starts collecting context-switch events immediately because `EVENT_TRACE_FLAG_CSWITCH` is already set here, while `configure_pmc()` runs afterward. Any switch buffered during that interval lacks the requested PMC extended data, and opening the consumer later does not eliminate those records; processing one raises `ETW_PMC_EXTENDED_DATA_ABSENT` and rejects the physical run. Configure PMC attachment before enabling CSwitch, or otherwise exclude pre-configuration events.

- [P2] Detect spaced relative executable paths before returning — <repo>-build\mbcx01_smoke_cell.py:875-876
```


## r9 — `MBCX-01-CODEXCLI-r9-FULL-LOG-2026-08-17.log` lines 34402-34411

```text
- [P2] Verify persisted store identity before DDL — <repo>-build\mbcx01_build_state_store.py:370-371
  When the path points to another MBCX store with the same `STORE_APPLICATION_ID` but different `meta` identity or schema version, this condition accepts it. `open_verified()` then changes journal mode and executes `_SCHEMA` before discovering `STATE_STORE_IDENTITY_MISMATCH`, so a mistyped path can create tables/indexes or adopt a headerless database instead of leaving it untouched. Compare the persisted metadata and version through the read-only connection before opening it writable.

- [P2] Convert read-only SQLite failures to verifier refusals — <repo>-build\mbcx01_build_state_authority.py:842-842
  When `store_path` names a truncated database that still has the expected `meta`, application ID, and user version but lacks `journal`, the read-only open succeeds and this call raises a raw `sqlite3.OperationalError`. Neither this function nor the public verifier translates that exception, so production scorer verification crashes instead of returning the documented transaction-identity refusal and sentinel. Validate the required schema during read-only open or translate query failures to `StateStoreError`.

- [P2] Probe runtime hypervisor state instead of installed services — <repo>-build\mbcx01_smoke_cell.py:192-196
  On Windows images where Hyper-V or guest services are installed but the hypervisor is inactive, these registry keys remain present because they describe installed components rather than runtime CPUID/partition state. This reports `hypervisor_present=True`, and the subsequent service-key check can similarly misclassify a guest as a root partition, producing incorrect signed environment evidence or bypassing the guest capability requirement. Use Windows' runtime hypervisor and partition signals instead.

- [P2] Bind the launched command to the signed candidate identity — <repo>-build\mbcx01_smoke_cell.py:371-373
```
