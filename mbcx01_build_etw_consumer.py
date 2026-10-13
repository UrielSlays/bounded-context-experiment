"""BUILD B ETW PMC consumer — the seam `mbcx01_build_win32.collect()` requires.

`collect()` takes `etw_session_factory: Callable[[], EtwPmcSession]` and, until
this module existed, NOTHING in the lane supplied one: `grep -rn
'EtwPmcSession('` returned zero constructors and the only mention of
`ProcessTrace`/`EventRecordCallback` in the lane was the comment at
`mbcx01_build_win32.py:405-414` describing the seam. The reviewed collector was
therefore reviewable-but-unrunnable and the one-cell smoke proof could not
execute (MBCX-01-OPEN-ISSUES.json, `MBCX01-BUILD-B-ETW-CONSUMER-UNBUILT`).

This module is the missing half. It is split deliberately into two layers:

- a PURE layer (ordering, the CSwitch->PMC join, lifetime assembly from
  ProcessStart/ProcessStop, the availability rules and the environment gate)
  that touches no OS state and is exercised by the BUILD witness suite against
  SYNTHETIC record streams; and
- an OS layer (`EtwPmcConsumer`) that creates the session with `StartTraceW`,
  configures the two documented PMC classes, turns the CSwitch system provider on
  afterwards with `ControlTraceW(EVENT_TRACE_CONTROL_UPDATE)` so no switch is
  ever buffered without a counter attached to it, consumes with
  `OpenTraceW`/`ProcessTrace`/`EventRecordCallback` on its own thread, reads the
  loss counters back with `ControlTraceW(EVENT_TRACE_CONTROL_QUERY)` and stops
  the session with `ControlTraceW(EVENT_TRACE_CONTROL_STOP)` even on failure.

NOTHING HERE RUNS IN THIS TASK, exactly as for `mbcx01_build_win32`: every
Win32 symbol binds lazily inside `_etw_win32()`, `EtwPmcConsumer.start()` is
reached only from an owner-authorized runbook step, and no test, verifier or
import in this repository starts a trace session or touches a PMU.

POSTURE (inherited verbatim from `EtwPmcSession`'s docstring and NOT relaxed):
anything the platform will not grant — an unavailable source, a counter-owner
conflict, multiplexing, or any nonzero `EventsLost`/`LogBuffersLost`/
`RealTimeBuffersLost` — is UNAVAILABLE evidence, never a diagnostic success and
never an estimated instruction count. An unattached seam is a FAULT, never an
empty result, and a missing PMC extended-data item is never a counter of zero.

--------------------------------------------------------------------------
WHAT SOURCE REVIEW CANNOT ESTABLISH (read this before trusting a green suite)
--------------------------------------------------------------------------
The witness suite exercises the pure layer exhaustively and the ABI statically.
It CANNOT observe vendor behaviour. The following are `pending` until the
operator's elevated smoke run, and each one is flagged again at its use site:

1. Whether a single `EVENT_TRACE_SYSTEM_LOGGER_MODE` session will accept BOTH
   the SystemTraceProvider CSwitch stream AND the manifest provider
   `Microsoft-Windows-Kernel-Process` (see `SAME_SESSION_UNCERTAINTY` below).
   The class comment requires the SAME session; the primary sources this build
   opened do not confirm a system logger accepts manifest providers, and
   `NT Kernel Logger Constants` states the opposite for the DEPRECATED kernel
   logger. `_enable_process_provider()` therefore ATTEMPTS it and FAULTS on
   refusal — it never silently opens a second session.
2. Whether `ProcessTelemetryIdInformation = 64` is the right ordinal
   (`mbcx01_build_win32.py:123`). Undocumented; only execution can confirm it.
3. Whether the platform grants `InstructionRetired` at all, how many counters
   it grants, and whether another owner holds them.
4. Whether the manifest THIS BUILD READ is the manifest the KERNEL EMITS. The
   ProcessStart/ProcessStop payload layout itself is no longer a guess: it was
   read back from this OS build's own provider manifest through TDH and is
   pinned version by version in `KERNEL_PROCESS_PAYLOAD_LAYOUTS`, whose comment
   carries the field-by-field table and the queries that produced it. What
   source review cannot see is a LIVE record: a host on a different build may
   emit a version this one does not publish, which
   `_decode_kernel_process_event()` refuses as
   `ETW_KERNEL_PROCESS_EVENT_VERSION_UNSUPPORTED` rather than decoding at a
   guessed offset.
6. Whether a live ProcessStart's `ProcessSequenceNumber` equals the sequence
   number `mbcx01_build_win32.query_process_start_key()` reads for the same
   process. The two routes were compared at the byte on this box for 12 live
   processes through `NtQueryInformationProcess(ProcessTelemetryIdInformation)`
   alone; they have never yet been compared against a real ETW record. A
   disagreement is `ETW_PROCESS_LIFETIME_ROOT_ABSENT` — a fault — never a
   roster built around some other process.
5. How `ETW_PMC_COUNTER_OWNERSHIP_STATUS.ProcessorNumber` relates to PROCESSOR
   GROUPS on a host with more than 64 logical processors. The structure and the
   query contract themselves ARE settled — against the installed SDK header,
   because Microsoft Learn publishes neither (the TRACE_QUERY_INFO_CLASS page
   says the buffer formats live "in-line in the `TRACE_QUERY_INFO_CLASS`
   enumeration definition in `evntrace.h`") — but the group mapping is not
   stated anywhere this build could read. See
   `PMC_OWNER_PROCESSOR_INDEX_UNCERTAINTY`.

A green suite here means "the logic is right IF the platform behaves as
documented". It does not mean the consumer works.
"""

from __future__ import annotations

import ctypes
import os
import struct
import threading
from ctypes import wintypes
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

import mbcx01_build_win32 as win32

# ==========================================================================
# CONSTANTS — every value below names the Microsoft page this build OPENED.
# A value the page NAMES but does not NUMBER is marked `VALUE NOT PUBLISHED`
# and carries the same warning class as `ProcessTelemetryIdInformation = 64`.
# ==========================================================================

#: TRACE_QUERY_INFO_CLASS (evntrace.h). VERIFIED, numeric values published:
#: learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class
#: This build opened that page and read the enumeration body; the two PMC
#: ordinals already pinned in `mbcx01_build_win32.py:119-120` are CORRECT and
#: the BUILD REVIEW ITEM note above them is discharged for these two values.
TraceSystemTraceEnableFlagsInfo = 4
TraceProfileSourceConfigInfo = 6
TraceProfileSourceListInfo = 7
TracePmcEventListInfo = 8
TracePmcCounterListInfo = 9
TraceMaxPmcCounterQuery = 22
TracePmcCounterOwners = 25

#: ETW_PMC_COUNTER_OWNER_TYPE (evntrace.h). NO Microsoft Learn page publishes
#: this enumeration — the TRACE_QUERY_INFO_CLASS page this build opened says so
#: itself: "More comprehensive documentation about which APIs the values in the
#: enumeration should be used with, as well as the corresponding buffer input
#: and output formats are available in-line in the `TRACE_QUERY_INFO_CLASS`
#: enumeration definition in `evntrace.h`."
#: (learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class)
#:
#: ✅ VERIFIED 2026-08-15 against the INSTALLED SDK HEADER, read byte-for-byte:
#:   C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\shared\evntrace.h
#: lines 1416-1421, verbatim:
#:   typedef enum _ETW_PMC_COUNTER_OWNER_TYPE {
#:       EtwPmcOwnerFree, EtwPmcOwnerUntagged, EtwPmcOwnerTagged,
#:       EtwPmcOwnerTaggedWithSource } ETW_PMC_COUNTER_OWNER_TYPE;
#: The enumerators are unnumbered in the header, so they take the C default
#: 0,1,2,3. `EtwPmcOwnerFree` is the ONLY value that means "nobody holds this
#: counter"; every other value is an owner.
EtwPmcOwnerFree = 0
EtwPmcOwnerUntagged = 1
EtwPmcOwnerTagged = 2
EtwPmcOwnerTaggedWithSource = 3

#: GetActiveProcessorCount's ALL_PROCESSOR_GROUPS. The Learn page NAMES it
#: ("If this value is ALL_PROCESSOR_GROUPS, the function returns the number of
#: active processors in all processor groups") and publishes NO number.
#: ✅ VERIFIED 2026-08-15 against the installed SDK header
#:   C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\winnt.h
#: line 653: `#define ALL_PROCESSOR_GROUPS 0xffff`.
ALL_PROCESSOR_GROUPS = 0xFFFF

#: ⚠ UNVERIFIED UNTIL THE ELEVATED RUN, and named here so it cannot be missed:
#: the header describes the TracePmcCounterOwners input as
#: "ETW_PMC_COUNTER_OWNERSHIP_STATUS with ProcessorNumber set to an appropriate
#: processor index" and does not say how that index relates to PROCESSOR GROUPS
#: on a host with more than 64 logical processors. `_count_counter_owners()`
#: iterates 0..GetActiveProcessorCount(ALL_PROCESSOR_GROUPS)-1, which is the
#: only reading the header supports, and RECORDS the processor count it swept
#: so a reviewer of a real receipt can see what was actually asked.
PMC_OWNER_PROCESSOR_INDEX_UNCERTAINTY = (
    "UNVERIFIED_UNTIL_ELEVATED_RUN: TracePmcCounterOwners takes a flat "
    "ProcessorNumber; evntrace.h does not publish how that index maps onto "
    "processor groups above 64 logical processors. The sweep is 0..N-1 for "
    "N = GetActiveProcessorCount(ALL_PROCESSOR_GROUPS).")

#: WNODE_HEADER.Flags (wmistr.h). The page states Flags "Must contain
#: WNODE_FLAG_TRACED_GUID"; it does NOT publish the number.
#: learn.microsoft.com/en-us/windows/win32/etw/wnode-header
#: VALUE NOT PUBLISHED at the doc page — 0x00020000 is the long-standing
#: wmistr.h value and is asserted by `verify_etw_struct_layout()` only against
#: itself. FLAGGED: a wrong value makes StartTraceW fail loudly with
#: ERROR_INVALID_PARAMETER, so it cannot pass silently.
WNODE_FLAG_TRACED_GUID = 0x00020000

#: WNODE_HEADER.ClientContext clock type. Value 1 = "Query performance counter
#: (QPC)", published in the value table on the wnode-header page above. QPC is
#: required here because every lifetime and observation this lane signs is a
#: QPC tick and `mbcx01_build_windows_producer._timing_cross_check` recomputes
#: elapsed nanoseconds from the signed QPC span at the signed QPC frequency.
WNODE_CLIENT_CONTEXT_QPC = 1

#: Logging Mode Constants. VERIFIED, values published:
#: learn.microsoft.com/en-us/windows/win32/etw/logging-mode-constants
EVENT_TRACE_FILE_MODE_NONE = 0x00000000
EVENT_TRACE_REAL_TIME_MODE = 0x00000100
EVENT_TRACE_SYSTEM_LOGGER_MODE = 0x02000000
EVENT_TRACE_INDEPENDENT_SESSION_MODE = 0x08000000

#: EVENT_TRACE_PROPERTIES.EnableFlags. VERIFIED, values published in the
#: EnableFlags member table:
#: learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties
#: PROCESS and THREAD are enabled so the SAME system logger also carries the
#: kernel process/thread rundown that cross-checks the manifest lifetimes.
EVENT_TRACE_FLAG_PROCESS = 0x00000001
EVENT_TRACE_FLAG_THREAD = 0x00000002
EVENT_TRACE_FLAG_CSWITCH = 0x00000010
EVENT_TRACE_FLAG_NO_SYSCONFIG = 0x10000000

#: THE TWO ENABLE-FLAG SETS (codex-CLI r8 P1 — the r7 fold's own NEIGHBOUR).
#:
#: THE SET OF POINTS AT WHICH EVENT GENERATION CAN BEGIN, enumerated rather than
#: sampled, because the r7 fold moved the PMC attach ahead of the CONSUMER and
#: stopped there — while `EVENT_TRACE_FLAG_CSWITCH` rides `StartTraceW` ITSELF,
#: which is EARLIER. The session therefore began producing context switches
#: before any counter was attached to them, and one PMC-less switch refuses the
#: WHOLE one-shot elevated run. The full set, in the order `start()` reaches it:
#:
#:   1. StartTraceW EnableFlags        -> system providers, live at return
#:   2. ControlTraceW(UPDATE) EnableFlags -> the same providers, changed later
#:   3. EnableTraceEx2(Kernel-Process) -> the manifest provider
#:   4. OpenTraceW/ProcessTrace        -> DELIVERY, not generation
#:
#: and grep confirms there is no fifth: this module calls `StartTraceW` once
#: (`start()`), `EnableTraceEx2` once (`_enable_process_provider`), and
#: `ControlTraceW` only for STOP/QUERY plus the UPDATE added here.
#:
#: WHAT ACTUALLY HAS TO PRECEDE WHAT, said exactly rather than maximally: the
#: only record this module requires a PMC item on is the CLASSIC CSwitch —
#: `_on_event_record()` returns without a fault for any provider that is not
#: `THREAD_GUID_BYTES` and any opcode that is not `CSWITCH_EVENT_TYPE`, and the
#: Kernel-Process manifest events are decoded by
#: `_decode_kernel_process_event()`, which never reads extended data. So PROCESS
#: and THREAD may stay on the StartTraceW call (their events cost nothing and
#: cannot be faulted for a missing counter), and CSWITCH — and only CSWITCH — is
#: enabled AFTER `configure_pmc()`.
#:
#: This also keeps the start call's EnableFlags non-empty of system providers,
#: which the alternative (start with no providers at all) would not; whether an
#: independent system logger accepts a start with zero enabled providers is
#: UNVERIFIED_UNTIL_ELEVATED_RUN and is not something this fold needs to find out
#: on the owner's one session.
SESSION_ENABLE_FLAGS_AT_START = (EVENT_TRACE_FLAG_PROCESS | EVENT_TRACE_FLAG_THREAD
                                 | EVENT_TRACE_FLAG_NO_SYSCONFIG)
SESSION_ENABLE_FLAGS_AFTER_PMC = (SESSION_ENABLE_FLAGS_AT_START
                                  | EVENT_TRACE_FLAG_CSWITCH)

#: ControlTrace control codes. The ControlTraceW page NAMES all of these and
#: publishes NO numbers:
#: learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-controltracew
#: VALUE NOT PUBLISHED at the doc page — evntrace.h values. FLAGGED. A wrong
#: STOP code leaves the session running, which the runbook cleanup step and
#: `EtwPmcConsumer.stop()`'s own ERROR_WMI_INSTANCE_NOT_FOUND re-check catch.
EVENT_TRACE_CONTROL_QUERY = 0
EVENT_TRACE_CONTROL_STOP = 1
EVENT_TRACE_CONTROL_UPDATE = 2
EVENT_TRACE_CONTROL_FLUSH = 3

#: EVENT_TRACE_LOGFILE.ProcessTraceMode. The EVENT_TRACE_LOGFILEW page NAMES
#: all three and publishes NO numbers:
#: learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_logfilew
#: VALUE NOT PUBLISHED at the doc page — evntcons.h values. FLAGGED.
#: RAW_TIMESTAMP is REQUIRED here, not optional: the page states that without
#: it ProcessTrace converts TimeStamp to FILETIME, and this lane signs QPC
#: ticks. A wrong flag value shows up immediately as timestamps that are not
#: QPC ticks, which `_reject_non_qpc_timestamps()` refuses.
PROCESS_TRACE_MODE_REAL_TIME = 0x00000100
PROCESS_TRACE_MODE_RAW_TIMESTAMP = 0x00001000
PROCESS_TRACE_MODE_EVENT_RECORD = 0x10000000

#: EVENT_HEADER_EXTENDED_DATA_ITEM.ExtType. The page NAMES
#: EVENT_HEADER_EXT_TYPE_PMC_COUNTERS and states its DataPtr points at an
#: EVENT_EXTENDED_ITEM_PMC_COUNTERS; it publishes NO numbers:
#: learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header_extended_data_item
#: VALUE NOT PUBLISHED at the doc page — evntcons.h values. FLAGGED, and this
#: is the single most load-bearing unverified ordinal in this module: a wrong
#: PMC_COUNTERS value makes every CSwitch look like it carries no counter,
#: which this module reports as ETW_PMC_EXTENDED_DATA_ABSENT (a fault) rather
#: than as a counter of zero. It therefore cannot silently understate work.
#:
#: ✅ VERIFIED 2026-08-15 against the INSTALLED SDK HEADER — not a doc page,
#: because Learn publishes no numbers for these at all, which is exactly why
#: they were flagged. Source read byte-for-byte:
#:   C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\evntcons.h
#: lines 51-69. TWO PINS WERE WRONG and are corrected here:
#:   PROCESS_START_KEY was 0x000A, header says 0x000D (line 63);
#:   EVENT_KEY        was 0x000B, header says 0x000A (line 60) — 0x000B is
#:                    EVENT_HEADER_EXT_TYPE_EVENT_SCHEMA_TL (line 61).
#: Both were DEAD at the time of the correction (defined, never read), so no
#: capture was affected; they are corrected so that the next reader who binds
#: an ExtType from this table does not inherit the error at the moment it goes
#: live. PMC_COUNTERS = 0x0008 was already CORRECT (line 57). Witness bw48
#: re-derives every one of these from the header on every run.
EVENT_HEADER_EXT_TYPE_RELATED_ACTIVITYID = 0x0001
EVENT_HEADER_EXT_TYPE_SID = 0x0002
EVENT_HEADER_EXT_TYPE_TS_ID = 0x0003
EVENT_HEADER_EXT_TYPE_INSTANCE_INFO = 0x0004
EVENT_HEADER_EXT_TYPE_STACK_TRACE32 = 0x0005
EVENT_HEADER_EXT_TYPE_STACK_TRACE64 = 0x0006
EVENT_HEADER_EXT_TYPE_PEBS_INDEX = 0x0007
EVENT_HEADER_EXT_TYPE_PMC_COUNTERS = 0x0008
EVENT_HEADER_EXT_TYPE_EVENT_KEY = 0x000A
EVENT_HEADER_EXT_TYPE_PROCESS_START_KEY = 0x000D

#: EVENT_HEADER.Flags. VALUE NOT PUBLISHED at the EVENT_HEADER page (names
#: only). FLAGGED.
#:
#: ✅ VERIFIED 2026-08-15 against the INSTALLED SDK HEADER (same file as above,
#: lines 148-158). CLASSIC_HEADER WAS WRONG AND IT WAS LIVE: it was pinned at
#: 0x0040, which the header defines as EVENT_HEADER_FLAG_64_BIT_HEADER (line
#: 154); EVENT_HEADER_FLAG_CLASSIC_HEADER is 0x0100 (line 156). The earlier
#: comment here claimed the value was only used to decide whether to walk
#: ExtendedData and so degraded safely to the count check — that was FALSE:
#: `_on_event_record()` tests this flag to decide whether a record is a
#: classic (MOF) CSwitch and takes a BARE `return` when the bit is clear, so
#: the old pin decided that branch by POINTER WIDTH instead of by header type.
#: Stated exactly, because the severity matters: on an x64 host a classic
#: kernel record carries 0x0040 too, so the branch passed FOR THE WRONG REASON
#: and most records survived — but every record whose header is not a 64-bit
#: header was DROPPED BY A BARE `return`, with no fault, no count and no
#: evidence. A drop this module cannot see is the one failure mode it claims
#: not to have. EXTENDED_INFO = 0x0001 was already correct (line 148).
#: Witness bw48 pins both against the header.
EVENT_HEADER_FLAG_EXTENDED_INFO = 0x0001
EVENT_HEADER_FLAG_CLASSIC_HEADER = 0x0100

#: CLASSIC_EVENT_ID + the CSwitch identity. VERIFIED and published verbatim:
#: learn.microsoft.com/en-us/windows/win32/etw/classic-event-id
#:   "To enable the context switch event type for thread events, set GUID to
#:    3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c and Type to 36."
#: and the same ThreadGuid appears on
#: learn.microsoft.com/en-us/windows/win32/etw/nt-kernel-logger-constants
#: This pair IS the `TracePmcEventListInfo` payload. The pre-existing
#: `EtwPmcSession.configure()` sent a ZERO-FILLED blob here, which would have
#: attached InstructionRetired to GUID_NULL/type 0 — see the repair ledger row
#: BB-16 and witness bw41.
THREAD_GUID_BYTES = (b"\xd1\xa8\x6f\x3d"          # Data1 3d6fa8d1, little-endian
                     b"\x05\xfe"                   # Data2 fe05
                     b"\xd0\x11"                   # Data3 11d0
                     b"\x9d\xda\x00\xc0\x4f\xd7\xba\x7c")  # Data4, big-endian bytes
CSWITCH_EVENT_TYPE = 36

#: Microsoft-Windows-Kernel-Process provider. NOT VERIFIABLE at a Microsoft
#: API reference page: this is a manifest provider and Learn publishes no page
#: carrying its GUID, event ids or keyword numbers. FLAGGED at the same level
#: as `ProcessTelemetryIdInformation = 64`. The consequence of a wrong GUID is
#: that `EnableTraceEx2` succeeds against a provider nobody writes to, so ZERO
#: ProcessStart events arrive — which `assemble_member_lifetimes()` reports as
#: `ETW_PROCESS_LIFETIME_ROOT_ABSENT`, a fault, not an empty roster.
KERNEL_PROCESS_PROVIDER_GUID_BYTES = (
    b"\xd6\x2c\xfb\x22"                            # 22FB2CD6
    b"\x7b\x0e"                                     # 0E7B
    b"\x2b\x42"                                     # 422B
    b"\xa0\xc7\x2f\xad\x1f\xd0\xe7\x16")            # A0C7-2FAD1FD0E716
KERNEL_PROCESS_KEYWORD_PROCESS = 0x0000000000000010
KERNEL_PROCESS_KEYWORD_THREAD = 0x0000000000000020
KERNEL_PROCESS_EVENT_ID_PROCESS_START = 1
KERNEL_PROCESS_EVENT_ID_PROCESS_STOP = 2
KERNEL_PROCESS_EVENT_ID_THREAD_START = 3
KERNEL_PROCESS_EVENT_ID_THREAD_STOP = 4

#: ProcessStart / ProcessStop PAYLOAD LAYOUT, PER EVENT VERSION.
#:
#: ✅ VERIFIED 2026-08-15 against THIS OS BUILD'S OWN PROVIDER MANIFEST — not a
#: doc page, because Microsoft publishes none for this provider, which is why
#: the layout was flagged in the first place. The manifest was read back through
#: TDH, the same decoding metadata a TDH-based consumer would see:
#:     TdhEnumerateManifestProviderEvents(22fb2cd6-0e7b-422b-a0c7-2fad1fd0e716)
#:     TdhGetManifestEventInformation(<each returned EVENT_DESCRIPTOR>)
#: on Windows 11 build 26200, provider resource
#: %SystemRoot%\system32\Microsoft-Windows-System-Events.dll.
#:
#: EVERY VERSION OF BOTH EVENTS BEGINS WITH `ProcessID`, A UINT32. There is no
#: version in which the payload begins with a 64-bit start key, and there is no
#: field named `ProcessStartKey` anywhere in these templates. The 64-bit
#: per-incarnation identity is `ProcessSequenceNumber`, and it exists only in
#: the LATER versions. Fields in manifest order, with the packed offset of each
#: fixed-size field (TDH walks a manifest payload field by field with no
#: alignment padding, so an offset is the running sum of the preceding sizes):
#:
#:   id 1 ProcessStart v0  ProcessID u32 @0, CreateTime FILETIME @4,
#:        ParentProcessID u32 @12, SessionID u32 @16, ImageName wstr @20
#:        -> NO sequence number
#:   id 1 ProcessStart v1  ...as v0 plus Flags u32 @20, ImageName wstr @24
#:        -> NO sequence number
#:   id 1 ProcessStart v2  ...as v1 plus ImageChecksum u32, TimeDateStamp u32,
#:        PackageFullName wstr, PackageRelativeAppId wstr after ImageName
#:        -> NO sequence number
#:   id 1 ProcessStart v3  ProcessID u32 @0, ProcessSequenceNumber u64 @4,
#:        CreateTime FILETIME @12, ParentProcessID u32 @20,
#:        ParentProcessSequenceNumber u64 @24, SessionID u32 @32, Flags u32 @36,
#:        ProcessTokenElevationType u32 @40, ProcessTokenIsElevated u32 @44,
#:        MandatoryLabel SID @48, then ImageName wstr, ImageChecksum u32,
#:        TimeDateStamp u32, PackageFullName wstr, PackageRelativeAppId wstr
#:   id 1 ProcessStart v4  as v3, plus SecurityMitigations u32 at the end
#:   id 2 ProcessStop  v0  ProcessID u32 @0, CreateTime @4, ExitTime @12,
#:        ExitCode u32 @20, TokenElevationType u32 @24, HandleCount u32 @28,
#:        CommitCharge u64 @32, CommitPeak u64 @40, ImageName ansi @48
#:        -> NO sequence number
#:   id 2 ProcessStop  v1  as v0 plus CPUCycleCount u64 @48,
#:        ReadOperationCount u32 @56, WriteOperationCount u32 @60,
#:        ReadTransferKiloBytes u32 @64, WriteTransferKiloBytes u32 @68,
#:        HardFaultCount u32 @72, ImageName ansi @76
#:        -> NO sequence number
#:   id 2 ProcessStop  v2  ProcessID u32 @0, ProcessSequenceNumber u64 @4,
#:        CreateTime @12, ExitTime @20, ExitCode u32 @28, then as v1
#:
#: The three versions that DO carry the identity share one prefix, so the table
#: below is `(event id, version) -> (ProcessID offset, ProcessSequenceNumber
#: offset)`. A version that is not in either table is refused by name rather
#: than decoded at a guessed offset.
KERNEL_PROCESS_PAYLOAD_LAYOUTS = {
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 3): (0, 4),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 4): (0, 4),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_STOP, 2): (0, 4),
}
#: ProcessStart's AUTHORITATIVE PARENT TUPLE, per event version:
#: `(event id, version) -> (ParentProcessID offset, ParentProcessSequenceNumber
#: offset)`. The offsets are READ OFF the same TDH-verified table above — v3 and
#: v4 both place `ParentProcessID u32 @20` and `ParentProcessSequenceNumber u64
#: @24` — and nothing here is taken from the finding that reported them.
#:
#: WHY A SECOND TABLE AND NOT A WIDER FIRST ONE: `KERNEL_PROCESS_PAYLOAD_LAYOUTS`
#: is keyed by both events, and ProcessStop has no parent fields at all. A row
#: absent here means "this template carries no parent tuple", which is the STOP
#: case and is not a fault.
#:
#: Until codex-CLI r7 P2 the decoder recorded `EventHeader.ProcessId` — the
#: context the start was LOGGED in — and discarded these fields. For a brokered
#: or explicit-parent creation the two differ, and `member_tree_incarnations()`
#: builds Job membership out of exactly this value: reading the header omits
#: legitimate descendants from the signed roster and admits foreign processes
#: whose start happens to be logged in a member's context. Witness bw97.
KERNEL_PROCESS_START_PARENT_LAYOUTS = {
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 3): (20, 24),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 4): (20, 24),
}
KERNEL_PROCESS_VERSIONS_WITHOUT_SEQUENCE_NUMBER = frozenset({
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 0),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 1),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_START, 2),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_STOP, 0),
    (KERNEL_PROCESS_EVENT_ID_PROCESS_STOP, 1),
})

#: ThreadStart / ThreadStop, from the SAME manifest dump. Both published
#: versions of both events begin `ProcessID u32 @0, ThreadID u32 @4` and differ
#: only in fields AFTER the two this module reads (v1 appends SubProcessTag,
#: and ThreadStop v1 also appends CycleTime), so the decode is version-
#: independent ACROSS THESE TWO TEMPLATES — and only across them.
#:
#: This set is therefore READ by `_decode_kernel_process_event`, not merely
#: declared: until 2026-08-16 it was consumed nowhere and the thread branch
#: decoded ANY version with eight payload bytes, so a future template whose
#: first eight bytes are not `ProcessID, ThreadID` would have been read at
#: guessed offsets and fed a fabricated TID into the signed roster. An
#: unverified version is `ETW_KERNEL_THREAD_VERSION_UNVERIFIED` — the same
#: posture the process events take, for the same reason. Witness bw77/bw78.
KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED = frozenset({0, 1})

#: EnableTraceEx2. VERIFIED page opened for the signature/semantics:
#: learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-enabletraceex2
#: Control code and level VALUES are NOT PUBLISHED there (evntrace.h /
#: evntprov.h). FLAGGED. A wrong control code fails the call, which faults.
EVENT_CONTROL_CODE_DISABLE_PROVIDER = 0
EVENT_CONTROL_CODE_ENABLE_PROVIDER = 1
TRACE_LEVEL_VERBOSE = 5
#: EVENT_ENABLE_PROPERTY_PROCESS_START_KEY makes ETW attach the 64-bit start
#: key as EVENT_HEADER_EXT_TYPE_PROCESS_START_KEY. Named on the
#: event_header_extended_data_item page; VALUE NOT PUBLISHED. FLAGGED.
EVENT_ENABLE_PROPERTY_PROCESS_START_KEY = 0x00000080

#: System error codes used for control-flow decisions (never for a verdict).
#: ERROR_CTX_CLOSE_PENDING is the ONE non-zero CloseTrace return that is a
#: success: the CloseTrace page states the call succeeded and ProcessTrace will
#: stop once it has processed the events already in its buffers. Its value is
#: VERIFIED 2026-08-15 against the installed SDK header
#: C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\shared\winerror.h
#: line 18367 (`#define ERROR_CTX_CLOSE_PENDING 7007L`).
ERROR_SUCCESS = 0
ERROR_ALREADY_EXISTS = 183
ERROR_MORE_DATA = 234
ERROR_WMI_INSTANCE_NOT_FOUND = 4201
ERROR_NO_SYSTEM_RESOURCES = 1450
ERROR_ACCESS_DENIED = 5
ERROR_CTX_CLOSE_PENDING = 7007

#: How long `stop()` waits for the ProcessTrace pump after CloseTrace. The wait
#: is bounded because a pump that never returns must become EVIDENCE (an
#: incomplete drain), not a hang; the value is a knob so a witness can drive the
#: timeout path without a thirty-second test.
CONSUMER_JOIN_TIMEOUT_SECONDS = 30

#: OpenTrace failure sentinel on a 64-bit host.
INVALID_PROCESSTRACE_HANDLE = 0xFFFFFFFFFFFFFFFF

#: Session naming. StartTraceW's page is explicit: use a DESCRIPTIVE name, do
#: not append random digits, and clean up an orphan rather than starting a
#: second session. `EtwPmcConsumer.start()` does exactly that.
SESSION_NAME = "MBCX01-BUILD-B-PMC"

#: Buffering. Real-time + a short flush timer, per the EVENT_TRACE_PROPERTIES
#: guidance ("Most real-time traces should start with a timer of 5 or 10
#: seconds"); a smoke cell is a sub-second run, so 1s is the documented floor.
SESSION_BUFFER_SIZE_KB = 128
SESSION_MINIMUM_BUFFERS = 64
SESSION_MAXIMUM_BUFFERS = 256
SESSION_FLUSH_TIMER_SECONDS = 1

#: Name buffers appended after EVENT_TRACE_PROPERTIES. Both names are limited
#: to 1,024 characters by the doc page; the log file name is unused (real-time
#: only) but the buffer is still reserved because ControlTraceW requires a
#: valid LogFileNameOffset.
LOGGER_NAME_CHARS = 1024
LOG_FILE_NAME_CHARS = 1024

#: See the module docstring, item 1. Restated here so a reader who jumps to
#: `_enable_process_provider()` cannot miss it.
SAME_SESSION_UNCERTAINTY = (
    "UNVERIFIED_UNTIL_ELEVATED_RUN: the EtwPmcSession contract requires the "
    "Microsoft-Windows-Kernel-Process ProcessStart/ProcessStop stream to come "
    "from the SAME session as the PMC-attached CSwitch stream. No Microsoft "
    "page this build opened confirms that an EVENT_TRACE_SYSTEM_LOGGER_MODE "
    "session accepts a manifest provider, and 'NT Kernel Logger Constants' "
    "states the deprecated kernel logger does NOT. This module attempts the "
    "documented single-session configuration and FAULTS if the platform "
    "refuses it; it never falls back to a second session, because a second "
    "session would silently break the same-session evidence claim.")

# --- pinned ETW ABI (64-bit) ----------------------------------------------
# Re-derived from the ctypes structures by `verify_etw_struct_layout()`, in the
# same style as `mbcx01_build_win32.verify_struct_layout()`. Every number below
# is COMPUTED from the member lists published on the Microsoft pages named
# above; Microsoft does not publish `sizeof`, so these are derivations, not
# quotations, and the verifier's job is to make a drift loud.

WNODE_HEADER_SIZE = 48
EVENT_TRACE_PROPERTIES_SIZE = 120
EVENT_HEADER_SIZE = 80
EVENT_DESCRIPTOR_SIZE = 16
ETW_BUFFER_CONTEXT_SIZE = 4
EVENT_HEADER_EXTENDED_DATA_ITEM_SIZE = 16
EVENT_RECORD_SIZE = 112
EVENT_TRACE_HEADER_SIZE = 48
EVENT_TRACE_SIZE = 88
SYSTEMTIME_SIZE = 16
TIME_ZONE_INFORMATION_SIZE = 172
TRACE_LOGFILE_HEADER_SIZE = 280
EVENT_TRACE_LOGFILE_SIZE = 448
CLASSIC_EVENT_ID_SIZE = 24
GUID_SIZE = 16
PMC_COUNTER_OWNER_SIZE = 12
PMC_COUNTER_OWNERSHIP_STATUS_HEADER_SIZE = 8

OFFSET_WNODE_GUID = 24
OFFSET_WNODE_CLIENT_CONTEXT = 40
OFFSET_WNODE_FLAGS = 44
OFFSET_PROPERTIES_LOG_FILE_MODE = 64
OFFSET_PROPERTIES_ENABLE_FLAGS = 72
OFFSET_PROPERTIES_EVENTS_LOST = 88
OFFSET_PROPERTIES_LOG_BUFFERS_LOST = 96
OFFSET_PROPERTIES_REALTIME_BUFFERS_LOST = 100
OFFSET_PROPERTIES_LOG_FILE_NAME_OFFSET = 112
OFFSET_PROPERTIES_LOGGER_NAME_OFFSET = 116
OFFSET_RECORD_BUFFER_CONTEXT = 80
OFFSET_RECORD_EXTENDED_DATA_COUNT = 84
OFFSET_RECORD_EXTENDED_DATA = 88
OFFSET_RECORD_USER_DATA = 96
OFFSET_HEADER_TIMESTAMP = 16
OFFSET_HEADER_PROVIDER_ID = 24
OFFSET_HEADER_EVENT_DESCRIPTOR = 40
OFFSET_LOGFILE_PROCESS_TRACE_MODE = 28
OFFSET_LOGFILE_EVENT_RECORD_CALLBACK = 424
OFFSET_LOGFILE_CONTEXT = 440

#: The counter list this session pins, in order. Index 0 IS InstructionRetired,
#: and `EVENT_EXTENDED_ITEM_PMC_COUNTERS.Counter[]` arrives in this same order,
#: which is what makes `select_pinned_counter(counters, 0)` correct.
PINNED_COUNTER_NAMES = (win32.PMC_SOURCE_NAME,)
PINNED_INSTRUCTION_RETIRED_INDEX = 0

#: The exact facts record the granted-capability evaluation consumes. Kept
#: CLOSED so an unnamed fact cannot creep in and quietly become optimism.
CAPABILITY_FACT_KEYS = frozenset({
    "pmc_source_available", "max_pmc_counters", "counter_owner_conflict_count",
    "multiplexing_detected", "attribution_complete", "counter_width_bits",
    "profile_source_name", "profile_source_id",
})


class EtwConsumerFault(RuntimeError):
    """A trace call failed or an observation is unreadable.

    Same discipline as `mbcx01_build_win32.CollectorFault`: a fault is NOT a
    measurement verdict. It aborts consumption so that no partial, defaulted or
    estimated PMC evidence can ever be signed.
    """


# ==========================================================================
# ctypes structures
# ==========================================================================


class GUID(ctypes.Structure):
    _fields_ = [("Data1", ctypes.c_ulong), ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort), ("Data4", ctypes.c_ubyte * 8)]

    @classmethod
    def from_le_bytes(cls, raw: bytes) -> "GUID":
        if len(raw) != GUID_SIZE:
            raise EtwConsumerFault(f"GUID_LENGTH_INVALID:{len(raw)}")
        return cls.from_buffer_copy(raw)


class _WNODE_CONTEXT(ctypes.Structure):
    _fields_ = [("Version", ctypes.c_ulong), ("Linkage", ctypes.c_ulong)]


class _WNODE_CONTEXT_UNION(ctypes.Union):
    _fields_ = [("HistoricalContext", ctypes.c_ulonglong),
                ("Detail", _WNODE_CONTEXT)]


class _WNODE_TIME_UNION(ctypes.Union):
    _fields_ = [("KernelHandle", wintypes.HANDLE),
                ("TimeStamp", ctypes.c_longlong)]


class WNODE_HEADER(ctypes.Structure):
    _anonymous_ = ("Context", "Time")
    _fields_ = [("BufferSize", ctypes.c_ulong), ("ProviderId", ctypes.c_ulong),
                ("Context", _WNODE_CONTEXT_UNION), ("Time", _WNODE_TIME_UNION),
                ("Guid", GUID), ("ClientContext", ctypes.c_ulong),
                ("Flags", ctypes.c_ulong)]


class _AGE_LIMIT_UNION(ctypes.Union):
    _fields_ = [("AgeLimit", ctypes.c_long), ("FlushThreshold", ctypes.c_long)]


class EVENT_TRACE_PROPERTIES(ctypes.Structure):
    _anonymous_ = ("Age",)
    _fields_ = [("Wnode", WNODE_HEADER),
                ("BufferSize", ctypes.c_ulong),
                ("MinimumBuffers", ctypes.c_ulong),
                ("MaximumBuffers", ctypes.c_ulong),
                ("MaximumFileSize", ctypes.c_ulong),
                ("LogFileMode", ctypes.c_ulong),
                ("FlushTimer", ctypes.c_ulong),
                ("EnableFlags", ctypes.c_ulong),
                ("Age", _AGE_LIMIT_UNION),
                ("NumberOfBuffers", ctypes.c_ulong),
                ("FreeBuffers", ctypes.c_ulong),
                ("EventsLost", ctypes.c_ulong),
                ("BuffersWritten", ctypes.c_ulong),
                ("LogBuffersLost", ctypes.c_ulong),
                ("RealTimeBuffersLost", ctypes.c_ulong),
                ("LoggerThreadId", wintypes.HANDLE),
                ("LogFileNameOffset", ctypes.c_ulong),
                ("LoggerNameOffset", ctypes.c_ulong)]


class EVENT_TRACE_PROPERTIES_BUFFER(ctypes.Structure):
    """Properties plus the two trailing name buffers, allocated as one block.

    The EVENT_TRACE_PROPERTIES Remarks section is explicit: allocate ONE block
    holding the structure, then the session name, then the log file name, and
    set `Wnode.BufferSize` to the size of the WHOLE block. The session name is
    copied for you by `StartTrace`; the log file name is not.
    """

    _fields_ = [("Props", EVENT_TRACE_PROPERTIES),
                ("LoggerName", ctypes.c_wchar * LOGGER_NAME_CHARS),
                ("LogFileName", ctypes.c_wchar * LOG_FILE_NAME_CHARS)]


class EVENT_DESCRIPTOR(ctypes.Structure):
    _fields_ = [("Id", ctypes.c_ushort), ("Version", ctypes.c_ubyte),
                ("Channel", ctypes.c_ubyte), ("Level", ctypes.c_ubyte),
                ("Opcode", ctypes.c_ubyte), ("Task", ctypes.c_ushort),
                ("Keyword", ctypes.c_ulonglong)]


class _EVENT_HEADER_TIME(ctypes.Structure):
    _fields_ = [("KernelTime", ctypes.c_ulong), ("UserTime", ctypes.c_ulong)]


class _EVENT_HEADER_TIME_UNION(ctypes.Union):
    _fields_ = [("Split", _EVENT_HEADER_TIME),
                ("ProcessorTime", ctypes.c_ulonglong)]


class EVENT_HEADER(ctypes.Structure):
    _anonymous_ = ("Time",)
    _fields_ = [("Size", ctypes.c_ushort), ("HeaderType", ctypes.c_ushort),
                ("Flags", ctypes.c_ushort), ("EventProperty", ctypes.c_ushort),
                ("ThreadId", ctypes.c_ulong), ("ProcessId", ctypes.c_ulong),
                ("TimeStamp", ctypes.c_longlong), ("ProviderId", GUID),
                ("EventDescriptor", EVENT_DESCRIPTOR),
                ("Time", _EVENT_HEADER_TIME_UNION), ("ActivityId", GUID)]


class _ETW_BUFFER_PROCESSOR(ctypes.Structure):
    _fields_ = [("ProcessorNumber", ctypes.c_ubyte),
                ("Alignment", ctypes.c_ubyte)]


class _ETW_BUFFER_PROCESSOR_UNION(ctypes.Union):
    _fields_ = [("Split", _ETW_BUFFER_PROCESSOR),
                ("ProcessorIndex", ctypes.c_ushort)]


class ETW_BUFFER_CONTEXT(ctypes.Structure):
    _anonymous_ = ("Processor",)
    _fields_ = [("Processor", _ETW_BUFFER_PROCESSOR_UNION),
                ("LoggerId", ctypes.c_ushort)]


class EVENT_HEADER_EXTENDED_DATA_ITEM(ctypes.Structure):
    _fields_ = [("Reserved1", ctypes.c_ushort), ("ExtType", ctypes.c_ushort),
                ("Linkage", ctypes.c_ushort), ("DataSize", ctypes.c_ushort),
                ("DataPtr", ctypes.c_ulonglong)]


class EVENT_RECORD(ctypes.Structure):
    _fields_ = [("EventHeader", EVENT_HEADER),
                ("BufferContext", ETW_BUFFER_CONTEXT),
                ("ExtendedDataCount", ctypes.c_ushort),
                ("UserDataLength", ctypes.c_ushort),
                ("ExtendedData", ctypes.POINTER(EVENT_HEADER_EXTENDED_DATA_ITEM)),
                ("UserData", ctypes.c_void_p),
                ("UserContext", ctypes.c_void_p)]


class _EVENT_TRACE_HEADER_CLASS(ctypes.Structure):
    _fields_ = [("Type", ctypes.c_ubyte), ("Level", ctypes.c_ubyte),
                ("Version", ctypes.c_ushort)]


class _EVENT_TRACE_HEADER_MARKER(ctypes.Structure):
    _fields_ = [("HeaderType", ctypes.c_ubyte), ("MarkerFlags", ctypes.c_ubyte)]


class _EVENT_TRACE_HEADER_FIELD_UNION(ctypes.Union):
    _fields_ = [("FieldTypeFlags", ctypes.c_ushort),
                ("Marker", _EVENT_TRACE_HEADER_MARKER)]


class _EVENT_TRACE_HEADER_VERSION_UNION(ctypes.Union):
    _fields_ = [("Version", ctypes.c_ulong), ("Class", _EVENT_TRACE_HEADER_CLASS)]


class _EVENT_TRACE_HEADER_GUID_UNION(ctypes.Union):
    _fields_ = [("Guid", GUID), ("GuidPtr", ctypes.c_ulonglong)]


class _EVENT_TRACE_HEADER_CONTEXT(ctypes.Structure):
    _fields_ = [("ClientContext", ctypes.c_ulong), ("Flags", ctypes.c_ulong)]


class _EVENT_TRACE_HEADER_TIME_UNION(ctypes.Union):
    _fields_ = [("Split", _EVENT_HEADER_TIME),
                ("ProcessorTime", ctypes.c_ulonglong),
                ("Context", _EVENT_TRACE_HEADER_CONTEXT)]


class EVENT_TRACE_HEADER(ctypes.Structure):
    _anonymous_ = ("Field", "Ver", "Id", "Time")
    _fields_ = [("Size", ctypes.c_ushort),
                ("Field", _EVENT_TRACE_HEADER_FIELD_UNION),
                ("Ver", _EVENT_TRACE_HEADER_VERSION_UNION),
                ("ThreadId", ctypes.c_ulong), ("ProcessId", ctypes.c_ulong),
                ("TimeStamp", ctypes.c_longlong),
                ("Id", _EVENT_TRACE_HEADER_GUID_UNION),
                ("Time", _EVENT_TRACE_HEADER_TIME_UNION)]


class _EVENT_TRACE_CONTEXT_UNION(ctypes.Union):
    _fields_ = [("ClientContext", ctypes.c_ulong),
                ("BufferContext", ETW_BUFFER_CONTEXT)]


class EVENT_TRACE(ctypes.Structure):
    _anonymous_ = ("Context",)
    _fields_ = [("Header", EVENT_TRACE_HEADER), ("InstanceId", ctypes.c_ulong),
                ("ParentInstanceId", ctypes.c_ulong), ("ParentGuid", GUID),
                ("MofData", ctypes.c_void_p), ("MofLength", ctypes.c_ulong),
                ("Context", _EVENT_TRACE_CONTEXT_UNION)]


class SYSTEMTIME(ctypes.Structure):
    _fields_ = [("wYear", ctypes.c_ushort), ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort), ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort), ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort), ("wMilliseconds", ctypes.c_ushort)]


class TIME_ZONE_INFORMATION(ctypes.Structure):
    _fields_ = [("Bias", ctypes.c_long), ("StandardName", ctypes.c_wchar * 32),
                ("StandardDate", SYSTEMTIME), ("StandardBias", ctypes.c_long),
                ("DaylightName", ctypes.c_wchar * 32),
                ("DaylightDate", SYSTEMTIME), ("DaylightBias", ctypes.c_long)]


class _TRACE_LOGFILE_VERSION(ctypes.Structure):
    _fields_ = [("MajorVersion", ctypes.c_ubyte), ("MinorVersion", ctypes.c_ubyte),
                ("SubVersion", ctypes.c_ubyte), ("SubMinorVersion", ctypes.c_ubyte)]


class _TRACE_LOGFILE_VERSION_UNION(ctypes.Union):
    _fields_ = [("Version", ctypes.c_ulong), ("VersionDetail", _TRACE_LOGFILE_VERSION)]


class _TRACE_LOGFILE_INSTANCE(ctypes.Structure):
    _fields_ = [("StartBuffers", ctypes.c_ulong), ("PointerSize", ctypes.c_ulong),
                ("EventsLost", ctypes.c_ulong), ("CpuSpeedInMHz", ctypes.c_ulong)]


class _TRACE_LOGFILE_INSTANCE_UNION(ctypes.Union):
    _fields_ = [("LogInstanceGuid", GUID), ("Detail", _TRACE_LOGFILE_INSTANCE)]


class TRACE_LOGFILE_HEADER(ctypes.Structure):
    _anonymous_ = ("Ver", "Instance")
    _fields_ = [("BufferSize", ctypes.c_ulong),
                ("Ver", _TRACE_LOGFILE_VERSION_UNION),
                ("ProviderVersion", ctypes.c_ulong),
                ("NumberOfProcessors", ctypes.c_ulong),
                ("EndTime", ctypes.c_longlong),
                ("TimerResolution", ctypes.c_ulong),
                ("MaximumFileSize", ctypes.c_ulong),
                ("LogFileMode", ctypes.c_ulong),
                ("BuffersWritten", ctypes.c_ulong),
                ("Instance", _TRACE_LOGFILE_INSTANCE_UNION),
                ("LoggerName", ctypes.c_wchar_p),
                ("LogFileName", ctypes.c_wchar_p),
                ("TimeZone", TIME_ZONE_INFORMATION),
                ("BootTime", ctypes.c_longlong),
                ("PerfFreq", ctypes.c_longlong),
                ("StartTime", ctypes.c_longlong),
                ("ReservedFlags", ctypes.c_ulong),
                ("BuffersLost", ctypes.c_ulong)]


EVENT_RECORD_CALLBACK = ctypes.WINFUNCTYPE(None, ctypes.POINTER(EVENT_RECORD))
EVENT_TRACE_BUFFER_CALLBACK = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)


class _LOGFILE_MODE_UNION(ctypes.Union):
    _fields_ = [("LogFileMode", ctypes.c_ulong), ("ProcessTraceMode", ctypes.c_ulong)]


class _LOGFILE_CALLBACK_UNION(ctypes.Union):
    _fields_ = [("EventCallback", ctypes.c_void_p),
                ("EventRecordCallback", ctypes.c_void_p)]


class EVENT_TRACE_LOGFILEW(ctypes.Structure):
    _anonymous_ = ("Mode", "Callback")
    _fields_ = [("LogFileName", ctypes.c_wchar_p),
                ("LoggerName", ctypes.c_wchar_p),
                ("CurrentTime", ctypes.c_longlong),
                ("BuffersRead", ctypes.c_ulong),
                ("Mode", _LOGFILE_MODE_UNION),
                ("CurrentEvent", EVENT_TRACE),
                ("LogfileHeader", TRACE_LOGFILE_HEADER),
                ("BufferCallback", ctypes.c_void_p),
                ("BufferSize", ctypes.c_ulong),
                ("Filled", ctypes.c_ulong),
                ("EventsLost", ctypes.c_ulong),
                ("Callback", _LOGFILE_CALLBACK_UNION),
                ("IsKernelTrace", ctypes.c_ulong),
                ("Context", ctypes.c_void_p)]


class CLASSIC_EVENT_ID(ctypes.Structure):
    _fields_ = [("EventGuid", GUID), ("Type", ctypes.c_ubyte),
                ("Reserved", ctypes.c_ubyte * 7)]


class ENABLE_TRACE_PARAMETERS(ctypes.Structure):
    _fields_ = [("Version", ctypes.c_ulong), ("EnableProperty", ctypes.c_ulong),
                ("ControlFlags", ctypes.c_ulong), ("SourceId", GUID),
                ("EnableFilterDesc", ctypes.c_void_p),
                ("FilterDescCount", ctypes.c_ulong)]


class PROFILE_SOURCE_INFO(ctypes.Structure):
    """Returned by TraceQueryInformation(TraceProfileSourceListInfo).

    The list is a chain: `NextEntryOffset` is a byte delta to the next record,
    and zero terminates it. `Description` is a variable-length WCHAR array that
    follows the fixed prefix, so this structure declares the PREFIX only and
    the description is read from the raw buffer.

    ✅ LAYOUT VERIFIED 2026-08-15 against the installed SDK header
    C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.26100.0\\shared\\evntrace.h
    lines 1407-1414, verbatim:

        typedef struct _PROFILE_SOURCE_INFO {
            ULONG NextEntryOffset; ULONG Source; ULONG MinInterval;
            ULONG MaxInterval; ULONG64 Reserved;
            WCHAR Description[ANYSIZE_ARRAY];
        } PROFILE_SOURCE_INFO, *PPROFILE_SOURCE_INFO;

    No Microsoft Learn page publishes this structure (searched 2026-08-15); the
    TRACE_QUERY_INFO_CLASS page states the buffer formats live "in-line in the
    `TRACE_QUERY_INFO_CLASS` enumeration definition in `evntrace.h`", which is
    the header quoted above. `Description` is WCHAR, so it is parsed as UTF-16
    CODE UNITS and terminated by a NUL code unit on a TWO-byte boundary — see
    `_profile_source_description()`.
    """

    _fields_ = [("NextEntryOffset", ctypes.c_ulong), ("Source", ctypes.c_ulong),
                ("MinInterval", ctypes.c_ulong), ("MaxInterval", ctypes.c_ulong),
                ("Reserved", ctypes.c_ulonglong)]


class ETW_PMC_COUNTER_OWNER(ctypes.Structure):
    """One counter-ownership row of a TracePmcCounterOwners answer.

    ✅ LAYOUT VERIFIED 2026-08-15 against evntrace.h lines 1423-1427, verbatim:

        typedef struct _ETW_PMC_COUNTER_OWNER {
            ETW_PMC_COUNTER_OWNER_TYPE OwnerType; ULONG ProfileSource;
            ULONG OwnerTag; } ETW_PMC_COUNTER_OWNER, *PETW_PMC_COUNTER_OWNER;

    A C enumeration of four small values is an `int` here, which is the same
    4-byte width the two ULONGs use, so the row is 12 bytes on the 64-bit ABI
    this module pins and `verify_etw_struct_layout()` re-derives that.
    """

    _fields_ = [("OwnerType", ctypes.c_ulong), ("ProfileSource", ctypes.c_ulong),
                ("OwnerTag", ctypes.c_ulong)]


class ETW_PMC_COUNTER_OWNERSHIP_STATUS(ctypes.Structure):
    """The PREFIX of one processor's TracePmcCounterOwners buffer.

    ✅ LAYOUT VERIFIED 2026-08-15 against evntrace.h lines 1429-1433, verbatim:

        typedef struct _ETW_PMC_COUNTER_OWNERSHIP_STATUS {
            ULONG ProcessorNumber; ULONG NumberOfCounters;
            ETW_PMC_COUNTER_OWNER CounterOwners[ANYSIZE_ARRAY];
        } ETW_PMC_COUNTER_OWNERSHIP_STATUS, *PETW_PMC_COUNTER_OWNERSHIP_STATUS;

    Declared as the prefix only — exactly like `PROFILE_SOURCE_INFO` — because
    `CounterOwners` is variable-length and is read out of the raw buffer by
    `pmc_counter_owner_rows()`. `ctypes.sizeof()` of this prefix is the
    header's `RTL_SIZEOF_THROUGH_FIELD(ETW_PMC_COUNTER_OWNERSHIP_STATUS,
    NumberOfCounters)`, which is the term the header's own buffer-sizing rule
    uses (evntrace.h lines 2350-2354).
    """

    _fields_ = [("ProcessorNumber", ctypes.c_ulong),
                ("NumberOfCounters", ctypes.c_ulong)]


def verify_etw_struct_layout() -> dict[str, int]:
    """Re-derive every pinned ETW size/offset from the structures themselves.

    Import-safe and OS-free, exactly like `mbcx01_build_win32.verify_struct_layout`:
    it touches no session, no PMU and no handle. A mismatch means this consumer
    would hand ETW a differently-shaped block than the one the documented ABI
    describes, which is a hard build failure and NOT something to discover at
    3am on the operator's box.
    """
    if ctypes.sizeof(ctypes.c_void_p) != 8:
        raise EtwConsumerFault("WINDOWS_64BIT_ABI_REQUIRED")
    derived = {
        "guid_size": ctypes.sizeof(GUID),
        "wnode_header_size": ctypes.sizeof(WNODE_HEADER),
        "event_trace_properties_size": ctypes.sizeof(EVENT_TRACE_PROPERTIES),
        "event_header_size": ctypes.sizeof(EVENT_HEADER),
        "event_descriptor_size": ctypes.sizeof(EVENT_DESCRIPTOR),
        "etw_buffer_context_size": ctypes.sizeof(ETW_BUFFER_CONTEXT),
        "extended_data_item_size": ctypes.sizeof(EVENT_HEADER_EXTENDED_DATA_ITEM),
        "event_record_size": ctypes.sizeof(EVENT_RECORD),
        "event_trace_header_size": ctypes.sizeof(EVENT_TRACE_HEADER),
        "event_trace_size": ctypes.sizeof(EVENT_TRACE),
        "systemtime_size": ctypes.sizeof(SYSTEMTIME),
        "time_zone_information_size": ctypes.sizeof(TIME_ZONE_INFORMATION),
        "trace_logfile_header_size": ctypes.sizeof(TRACE_LOGFILE_HEADER),
        "event_trace_logfile_size": ctypes.sizeof(EVENT_TRACE_LOGFILEW),
        "classic_event_id_size": ctypes.sizeof(CLASSIC_EVENT_ID),
        "pmc_counter_owner_size": ctypes.sizeof(ETW_PMC_COUNTER_OWNER),
        "pmc_counter_ownership_status_header_size": ctypes.sizeof(
            ETW_PMC_COUNTER_OWNERSHIP_STATUS),
        "wnode_guid_offset": WNODE_HEADER.Guid.offset,
        "wnode_client_context_offset": WNODE_HEADER.ClientContext.offset,
        "wnode_flags_offset": WNODE_HEADER.Flags.offset,
        "log_file_mode_offset": EVENT_TRACE_PROPERTIES.LogFileMode.offset,
        "enable_flags_offset": EVENT_TRACE_PROPERTIES.EnableFlags.offset,
        "events_lost_offset": EVENT_TRACE_PROPERTIES.EventsLost.offset,
        "log_buffers_lost_offset": EVENT_TRACE_PROPERTIES.LogBuffersLost.offset,
        "realtime_buffers_lost_offset": EVENT_TRACE_PROPERTIES.RealTimeBuffersLost.offset,
        "log_file_name_offset_field": EVENT_TRACE_PROPERTIES.LogFileNameOffset.offset,
        "logger_name_offset_field": EVENT_TRACE_PROPERTIES.LoggerNameOffset.offset,
        "record_buffer_context_offset": EVENT_RECORD.BufferContext.offset,
        "record_extended_data_count_offset": EVENT_RECORD.ExtendedDataCount.offset,
        "record_extended_data_offset": EVENT_RECORD.ExtendedData.offset,
        "record_user_data_offset": EVENT_RECORD.UserData.offset,
        "header_timestamp_offset": EVENT_HEADER.TimeStamp.offset,
        "header_provider_id_offset": EVENT_HEADER.ProviderId.offset,
        "header_event_descriptor_offset": EVENT_HEADER.EventDescriptor.offset,
        "logfile_process_trace_mode_offset": EVENT_TRACE_LOGFILEW.Mode.offset,
        "logfile_event_record_callback_offset": EVENT_TRACE_LOGFILEW.Callback.offset,
        "logfile_context_offset": EVENT_TRACE_LOGFILEW.Context.offset,
    }
    expected = {
        "guid_size": GUID_SIZE,
        "wnode_header_size": WNODE_HEADER_SIZE,
        "event_trace_properties_size": EVENT_TRACE_PROPERTIES_SIZE,
        "event_header_size": EVENT_HEADER_SIZE,
        "event_descriptor_size": EVENT_DESCRIPTOR_SIZE,
        "etw_buffer_context_size": ETW_BUFFER_CONTEXT_SIZE,
        "extended_data_item_size": EVENT_HEADER_EXTENDED_DATA_ITEM_SIZE,
        "event_record_size": EVENT_RECORD_SIZE,
        "event_trace_header_size": EVENT_TRACE_HEADER_SIZE,
        "event_trace_size": EVENT_TRACE_SIZE,
        "systemtime_size": SYSTEMTIME_SIZE,
        "time_zone_information_size": TIME_ZONE_INFORMATION_SIZE,
        "trace_logfile_header_size": TRACE_LOGFILE_HEADER_SIZE,
        "event_trace_logfile_size": EVENT_TRACE_LOGFILE_SIZE,
        "classic_event_id_size": CLASSIC_EVENT_ID_SIZE,
        "pmc_counter_owner_size": PMC_COUNTER_OWNER_SIZE,
        "pmc_counter_ownership_status_header_size":
            PMC_COUNTER_OWNERSHIP_STATUS_HEADER_SIZE,
        "wnode_guid_offset": OFFSET_WNODE_GUID,
        "wnode_client_context_offset": OFFSET_WNODE_CLIENT_CONTEXT,
        "wnode_flags_offset": OFFSET_WNODE_FLAGS,
        "log_file_mode_offset": OFFSET_PROPERTIES_LOG_FILE_MODE,
        "enable_flags_offset": OFFSET_PROPERTIES_ENABLE_FLAGS,
        "events_lost_offset": OFFSET_PROPERTIES_EVENTS_LOST,
        "log_buffers_lost_offset": OFFSET_PROPERTIES_LOG_BUFFERS_LOST,
        "realtime_buffers_lost_offset": OFFSET_PROPERTIES_REALTIME_BUFFERS_LOST,
        "log_file_name_offset_field": OFFSET_PROPERTIES_LOG_FILE_NAME_OFFSET,
        "logger_name_offset_field": OFFSET_PROPERTIES_LOGGER_NAME_OFFSET,
        "record_buffer_context_offset": OFFSET_RECORD_BUFFER_CONTEXT,
        "record_extended_data_count_offset": OFFSET_RECORD_EXTENDED_DATA_COUNT,
        "record_extended_data_offset": OFFSET_RECORD_EXTENDED_DATA,
        "record_user_data_offset": OFFSET_RECORD_USER_DATA,
        "header_timestamp_offset": OFFSET_HEADER_TIMESTAMP,
        "header_provider_id_offset": OFFSET_HEADER_PROVIDER_ID,
        "header_event_descriptor_offset": OFFSET_HEADER_EVENT_DESCRIPTOR,
        "logfile_process_trace_mode_offset": OFFSET_LOGFILE_PROCESS_TRACE_MODE,
        "logfile_event_record_callback_offset": OFFSET_LOGFILE_EVENT_RECORD_CALLBACK,
        "logfile_context_offset": OFFSET_LOGFILE_CONTEXT,
    }
    if derived != expected:
        drift = {name: (value, expected[name])
                 for name, value in derived.items() if value != expected[name]}
        raise EtwConsumerFault(f"ETW_ABI_DRIFT:{drift}")
    # The name buffers must sit AFTER the structure, and the whole block is
    # what `Wnode.BufferSize` describes (EVENT_TRACE_PROPERTIES Remarks).
    if EVENT_TRACE_PROPERTIES_BUFFER.LoggerName.offset != EVENT_TRACE_PROPERTIES_SIZE:
        raise EtwConsumerFault("ETW_ABI_DRIFT:logger_name_not_after_properties")
    if (EVENT_TRACE_PROPERTIES_BUFFER.LogFileName.offset
            <= EVENT_TRACE_PROPERTIES_BUFFER.LoggerName.offset):
        raise EtwConsumerFault("ETW_ABI_DRIFT:log_file_name_must_follow_logger_name")
    return derived


def classic_event_id_blob(guid_bytes: bytes = THREAD_GUID_BYTES,
                          event_type: int = CSWITCH_EVENT_TYPE) -> bytes:
    """The exact `TracePmcEventListInfo` payload: one CLASSIC_EVENT_ID.

    Documented verbatim on the CLASSIC_EVENT_ID page: for the context-switch
    event type of thread events, GUID = 3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c
    and Type = 36. This is what the pre-existing `EtwPmcSession.configure()`
    filled with ZEROES, which would have attached InstructionRetired to
    GUID_NULL/type 0 and collected nothing.
    """
    entry = CLASSIC_EVENT_ID()
    entry.EventGuid = GUID.from_le_bytes(guid_bytes)
    entry.Type = int(event_type)
    blob = bytes(bytearray(entry))
    if len(blob) != CLASSIC_EVENT_ID_SIZE:
        raise EtwConsumerFault(f"CLASSIC_EVENT_ID_SIZE_INVALID:{len(blob)}")
    return blob


# ==========================================================================
# PURE layer — no OS state, fully exercised by the BUILD witness suite
# ==========================================================================

RECORD_FIELDS = ("processor", "qpc", "old_thread_id", "instruction_retired")


def order_records_per_processor(
        records: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Return the records in per-processor timestamp order plus a reorder count.

    `EtwPmcSession.consume_cswitch()` recomputes every delta from CONSECUTIVE
    counter values on the SAME processor, so the stream it is handed has to be
    per-processor monotonic in time. A real-time session does not guarantee
    that on arrival: ETW buffers are per-processor and are delivered when they
    flush, so records from different CPUs interleave arbitrarily.

    The reordering is therefore performed here, ONCE, and the number of records
    that had to move is RETURNED so it can be recorded as evidence. Silently
    sorting a stream and reporting nothing would hide exactly the kind of
    delivery anomaly this lane exists to notice.

    The sort is stable, so two events at the same (processor, qpc) keep their
    capture order rather than being reordered on a tie.
    """
    rows: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            raise EtwConsumerFault("ETW_CSWITCH_RECORD_INCOMPLETE:not_a_record")
        missing = [name for name in RECORD_FIELDS if name not in record]
        if missing:
            raise EtwConsumerFault(
                f"ETW_CSWITCH_RECORD_INCOMPLETE:{','.join(sorted(missing))}")
        for name in RECORD_FIELDS:
            value = record[name]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise EtwConsumerFault(f"ETW_CSWITCH_RECORD_INCOMPLETE:{name}")
        rows.append(dict(record))
    ordered = sorted(rows, key=lambda row: (row["processor"], row["qpc"]))
    reordered = sum(1 for left, right in zip(rows, ordered) if left is not right
                    and (left["processor"], left["qpc"], left["old_thread_id"],
                         left["instruction_retired"])
                    != (right["processor"], right["qpc"], right["old_thread_id"],
                        right["instruction_retired"]))
    return ordered, reordered


def pmc_counters_from_extended_data(
        items: Sequence[tuple[int, bytes]]) -> tuple[int, ...]:
    """Read the PMC counter array out of an event's extended data items.

    Each item is `(ExtType, payload_bytes)`. The PMC payload is
    `EVENT_EXTENDED_ITEM_PMC_COUNTERS`, i.e. `ULONG64 Counter[ANYSIZE_ARRAY]`,
    delivered in the order of the counter list the session pinned.

    An ABSENT item is a FAULT, never a counter of zero: "no counter observed"
    and "the workload retired no instructions" are different claims and only
    one of them is ever true here.
    """
    for ext_type, payload in items:
        if int(ext_type) != EVENT_HEADER_EXT_TYPE_PMC_COUNTERS:
            continue
        raw = bytes(payload)
        if not raw or len(raw) % 8 != 0:
            raise EtwConsumerFault(f"ETW_PMC_EXTENDED_DATA_MALFORMED:{len(raw)}")
        return tuple(struct.unpack("<%dQ" % (len(raw) // 8), raw))
    raise EtwConsumerFault("ETW_PMC_EXTENDED_DATA_ABSENT")


def select_pinned_counter(counters: Sequence[int],
                          index: int = PINNED_INSTRUCTION_RETIRED_INDEX) -> int:
    """Pick the pinned counter by its position in the configured counter list."""
    if index < 0 or index >= len(counters):
        raise EtwConsumerFault(
            f"ETW_PMC_COUNTER_INDEX_UNAVAILABLE:{index}/{len(counters)}")
    value = counters[index]
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise EtwConsumerFault(f"ETW_PMC_COUNTER_VALUE_INVALID:{value!r}")
    return int(value)


def _profile_source_description(tail: bytes) -> str:
    """Decode one `PROFILE_SOURCE_INFO.Description` WCHAR array.

    `Description` is `WCHAR[]` (evntrace.h line 1413), so it is a sequence of
    UTF-16 CODE UNITS and the string ends at the first NUL code unit — a
    two-byte NUL sitting on a TWO-BYTE BOUNDARY relative to the start of the
    array. Splitting the raw bytes on `b"\\x00\\x00"` instead matches the
    UNALIGNED pair formed by the high byte of the last ASCII character and the
    low byte of the terminator, which silently drops that character:
    `InstructionRetired` parsed that way is `InstructionRetire`, which then
    matches nothing and reports a present source as absent.

    A trailing odd byte cannot be a code unit and is not decoded. Nothing here
    guesses: an array with no terminator at all decodes to everything it
    contains, and the caller compares the WHOLE decoded name.
    """
    units = bytearray()
    for index in range(0, len(tail) - 1, 2):
        unit = tail[index:index + 2]
        if unit == b"\x00\x00":
            break
        units += unit
    return bytes(units).decode("utf-16-le", "ignore")


def pmc_counter_owner_rows(raw: bytes, *, max_counters: int) -> list[dict[str, Any]]:
    """Decode ONE processor's `ETW_PMC_COUNTER_OWNERSHIP_STATUS` answer.

    Layout and semantics come from the installed SDK header (evntrace.h lines
    1416-1433 for the structures, 2345-2361 for the query contract), quoted at
    `ETW_PMC_COUNTER_OWNERSHIP_STATUS`. The answer is `ProcessorNumber`,
    `NumberOfCounters`, then that many `ETW_PMC_COUNTER_OWNER` rows —
    "NumberOfCounters is set to the number of items in the CounterOwners
    array".

    So `NumberOfCounters` is METADATA, not ownership: a healthy host with four
    unused counters answers `NumberOfCounters = 4` and four rows of
    `EtwPmcOwnerFree`. Treating any nonzero byte in the buffer as an owner
    reports that host as a counter-owner conflict and refuses its evidence.

    Refusals rather than guesses: a buffer too short for the prefix, a
    `NumberOfCounters` larger than the buffer can hold, and a
    `NumberOfCounters` larger than the platform's own maximum-counter answer
    are each `ETW_PMC_COUNTER_OWNERS_MALFORMED`, because a mis-sized ownership
    answer must never become "nobody owns anything".
    """
    header_size = ctypes.sizeof(ETW_PMC_COUNTER_OWNERSHIP_STATUS)
    row_size = ctypes.sizeof(ETW_PMC_COUNTER_OWNER)
    if len(raw) < header_size:
        raise EtwConsumerFault(
            f"ETW_PMC_COUNTER_OWNERS_MALFORMED:short_buffer:{len(raw)}")
    status = ETW_PMC_COUNTER_OWNERSHIP_STATUS.from_buffer_copy(raw[:header_size])
    count = int(status.NumberOfCounters)
    if count > int(max_counters):
        raise EtwConsumerFault(
            "ETW_PMC_COUNTER_OWNERS_MALFORMED:NumberOfCounters="
            f"{count}>max_pmc_counters={int(max_counters)}")
    if header_size + count * row_size > len(raw):
        raise EtwConsumerFault(
            "ETW_PMC_COUNTER_OWNERS_MALFORMED:NumberOfCounters="
            f"{count}>buffer={len(raw)}")
    rows: list[dict[str, Any]] = []
    for index in range(count):
        start = header_size + index * row_size
        owner = ETW_PMC_COUNTER_OWNER.from_buffer_copy(raw[start:start + row_size])
        rows.append({"processor_number": int(status.ProcessorNumber),
                     "counter_index": index,
                     "owner_type": int(owner.OwnerType),
                     "profile_source": int(owner.ProfileSource),
                     "owner_tag": int(owner.OwnerTag)})
    return rows


def count_owned_pmc_counters(rows: Iterable[dict[str, Any]]) -> int:
    """How many decoded owner rows are held by somebody.

    `EtwPmcOwnerFree` is the one value that means the counter is free; every
    other `ETW_PMC_COUNTER_OWNER_TYPE` names an owner, tagged or not. An
    owner-type value the header does not define is NOT quietly treated as free
    — it is refused, because an ownership word this build cannot read must not
    decide that a counter is available.
    """
    owned = 0
    for row in rows:
        owner_type = int(row["owner_type"])
        if owner_type not in (EtwPmcOwnerFree, EtwPmcOwnerUntagged,
                              EtwPmcOwnerTagged, EtwPmcOwnerTaggedWithSource):
            raise EtwConsumerFault(
                f"ETW_PMC_COUNTER_OWNER_TYPE_UNKNOWN:{owner_type}")
        if owner_type != EtwPmcOwnerFree:
            owned += 1
    return owned


def _start_key_text(value: Any) -> str:
    """Normalise a start key to the frozen 16-hex-digit uppercase form."""
    if isinstance(value, str):
        text = value.strip().upper()
    elif isinstance(value, int) and not isinstance(value, bool):
        text = f"{value:016X}"
    else:
        raise EtwConsumerFault(f"ETW_PROCESS_START_KEY_INVALID:{value!r}")
    if len(text) != 16 or any(char not in "0123456789ABCDEF" for char in text):
        raise EtwConsumerFault(f"ETW_PROCESS_START_KEY_INVALID:{text!r}")
    if int(text, 16) == 0:
        raise EtwConsumerFault("ETW_PROCESS_START_KEY_UNAVAILABLE")
    return text


def assemble_member_lifetimes(process_events: Iterable[dict[str, Any]], *,
                              job_object_id: str, root_process_id: int,
                              root_process_start_key: str,
                              membership_source: str =
                              "JOB_ASSIGNMENT_PROCESS_ETW_AND_FINAL_QUERY",
                              ) -> list[dict[str, Any]]:
    """Build the signed PID/start-key lifetime list from ProcessStart/ProcessStop.

    This is the ONLY route that observes a descendant the collector never
    opened a handle to, which is why `EtwPmcSession.member_lifetimes` names it
    specifically. Every member — terminated included — gets one row in the
    frozen `mbcx01_r13_measurement.PROCESS_KEYS` shape.

    A member without a terminal, a stop without a start, a zero start key or a
    non-monotonic lifetime is a FAULT. A roster that is missing the root is a
    fault too: an empty or partial roster must never be signed as a complete
    membership snapshot.

    THE PARENT TUPLE IS AN IDENTITY, AND THE ROOT HAS NONE (2026-08-15). The
    frozen validator (`mbcx01_r13_measurement._validate_physical_evidence`,
    :889-899) reads the two parent fields as evidence, not as decoration:

      * the ROOT row must carry `parent_process_id is None` AND
        `parent_process_start_key is None` — the process that created the root
        is the COLLECTOR, which is not a Job member, so naming it would put a
        non-member into the membership evidence; and
      * every other row must carry a 16-hex parent key whose
        `(parent_process_id, parent_process_start_key)` pair is itself a member.

    The decoded ProcessStart stream cannot satisfy the first on its own:
    `_decode_kernel_process_event` records a parent for EVERY start including
    the root's, whose parent is the collector. So the root is SPECIAL-CASED here
    — the one row whose parent fields are `None` by definition. Until that was
    done every LIVE capture produced `PROCESS_MEMBERSHIP_INVALID` after the
    candidate had already run: right evidence, refused, with the whole receipt
    lost. Witness bw65.

    A DESCENDANT'S PARENT KEY NOW USUALLY ARRIVES DECODED (codex-CLI r7 P2): the
    v3/v4 ProcessStart template carries `ParentProcessSequenceNumber` and the
    decoder reads it. A key that arrives set is honoured and never re-resolved.
    The containment resolution below therefore still runs — for a parent that
    started before the trace window, whose sequence number the payload reports
    as 0 — and it is unchanged, so the old and the new streams are both
    assembled correctly. It resolves from the process-incarnation stream by QPC
    containment, exactly as `bind_thread_start_keys` resolves a thread's own key.

    Nothing is guessed: a descendant whose parent PID has no incarnation
    containing its start is `ETW_PROCESS_PARENT_START_KEY_UNBINDABLE`, two
    containing incarnations are `ETW_PROCESS_INCARNATION_AMBIGUOUS`, and a
    non-root row with no parent PID at all is
    `ETW_PROCESS_LIFETIME_PARENT_UNKNOWN`.
    """
    events = list(process_events)
    root_key = _start_key_text(root_process_start_key)
    starts: dict[tuple[int, str], dict[str, Any]] = {}
    stops: dict[tuple[int, str], int] = {}
    order: list[tuple[int, str]] = []
    for event in events:
        if not isinstance(event, dict) or "kind" not in event:
            raise EtwConsumerFault("ETW_PROCESS_LIFETIME_EVENT_INVALID")
        kind = str(event["kind"]).upper()
        process_id = event.get("process_id")
        if (not isinstance(process_id, int) or isinstance(process_id, bool)
                or process_id <= 0):
            raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_PID_INVALID:{process_id!r}")
        key = _start_key_text(event.get("process_start_key"))
        qpc = event.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_QPC_INVALID:{qpc!r}")
        pair = (int(process_id), key)
        if kind == "START":
            if pair in starts:
                raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_DUPLICATE_START:{pair}")
            parent_id = event.get("parent_process_id")
            parent_key = event.get("parent_process_start_key")
            if parent_id is not None and (not isinstance(parent_id, int)
                                          or isinstance(parent_id, bool)):
                raise EtwConsumerFault("ETW_PROCESS_LIFETIME_PARENT_INVALID")
            starts[pair] = {
                "parent_process_id": None if parent_id is None else int(parent_id),
                "parent_process_start_key":
                    None if parent_key in (None, 0) else _start_key_text(parent_key),
                "started_qpc": int(qpc)}
            order.append(pair)
        elif kind == "STOP":
            if pair in stops:
                raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_DUPLICATE_STOP:{pair}")
            stops[pair] = int(qpc)
        else:
            raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_EVENT_INVALID:{kind}")
    unmatched = sorted(set(stops) - set(starts))
    if unmatched:
        raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_UNMATCHED_STOP:{unmatched}")
    unterminated = sorted(set(starts) - set(stops))
    if unterminated:
        raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_INCOMPLETE:{unterminated}")
    root_pair = (int(root_process_id), root_key)
    if root_pair not in starts:
        raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_ROOT_ABSENT:{root_pair}")
    intervals = process_incarnation_intervals(events)
    rows: list[dict[str, Any]] = []
    for pair in order:
        start = starts[pair]
        ended = stops[pair]
        if ended <= start["started_qpc"]:
            raise EtwConsumerFault(
                f"ETW_PROCESS_LIFETIME_NONMONOTONIC:{pair}:"
                f"{start['started_qpc']}>={ended}")
        if pair == root_pair:
            # The root's creator is the collector, not a member of the Job it
            # is measuring. The membership evidence says so with two Nones.
            parent_id: int | None = None
            parent_key: str | None = None
        else:
            parent_id = start["parent_process_id"]
            if parent_id is None or parent_id <= 0:
                raise EtwConsumerFault(
                    f"ETW_PROCESS_LIFETIME_PARENT_UNKNOWN:{pair}")
            parent_key = start["parent_process_start_key"]
            if parent_key is None:
                parent_key = _resolve_parent_start_key(
                    intervals, parent_id, start["started_qpc"])
        rows.append({
            "process_id": pair[0], "process_start_key": pair[1],
            "parent_process_id": parent_id,
            "parent_process_start_key": parent_key,
            "job_object_id": job_object_id,
            "assigned_before_resume": True,
            "membership_source": membership_source,
            "started_qpc": start["started_qpc"], "ended_qpc": ended,
            "terminal_status": "EXITED"})
    return rows


def process_incarnation_intervals(process_events: Iterable[dict[str, Any]],
                                  ) -> dict[int, list[tuple[int, int | None, str]]]:
    """Every decoded PID's incarnations as `(started_qpc, ended_qpc, start key)`.

    ONE incarnation is one ProcessStart and the ProcessStop that closes it, so
    a PID that was reused inside the capture window has SEVERAL rows here and
    they are the only thing that can tell them apart in TIME. `ended_qpc` is
    `None` when the stream carries no ProcessStop for that incarnation, which
    is an OPEN interval and never a closed one guessed at the window edge; the
    roster completeness fault for a member without a terminal belongs to
    `assemble_member_lifetimes`, not here.
    """
    intervals: dict[int, list[tuple[int, int | None, str]]] = {}
    stops: dict[tuple[int, str], int] = {}
    for event in process_events:
        if not isinstance(event, dict):
            raise EtwConsumerFault("ETW_PROCESS_LIFETIME_EVENT_INVALID")
        kind = str(event.get("kind", "")).upper()
        if kind not in {"START", "STOP"}:
            continue
        process_id = event.get("process_id")
        if (not isinstance(process_id, int) or isinstance(process_id, bool)
                or process_id <= 0):
            raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_PID_INVALID:{process_id!r}")
        qpc = event.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            raise EtwConsumerFault(f"ETW_PROCESS_LIFETIME_QPC_INVALID:{qpc!r}")
        key = _start_key_text(event.get("process_start_key"))
        if kind == "START":
            intervals.setdefault(int(process_id), []).append(
                (int(qpc), None, key))
        else:
            stops[(int(process_id), key)] = int(qpc)
    closed: dict[int, list[tuple[int, int | None, str]]] = {}
    for process_id, rows in intervals.items():
        closed[process_id] = sorted(
            (started, stops.get((process_id, key)), key)
            for started, _open, key in rows)
    return closed


def _containing_incarnations(intervals: dict[int, list[tuple[int, int | None, str]]],
                             process_id: Any, qpc: Any) -> list[str]:
    """The start keys of every incarnation of `process_id` alive at `qpc`.

    Containment includes BOTH ends of a closed interval, and an OPEN interval
    (a start whose ProcessStop the stream never carried) contains every qpc at
    or after its start. This is the one containment rule in this module: the
    thread binder, the parent-key resolver and the member-tree partition all
    read it here rather than each spelling it again.
    """
    return [key for started, ended, key in intervals.get(int(process_id), ())
            if started <= int(qpc) and (ended is None or int(qpc) <= ended)]


def _resolve_parent_start_key(intervals: dict[int, list[tuple[int, int | None, str]]],
                              parent_process_id: int, started_qpc: int) -> str:
    """Which incarnation of the parent PID was alive when the child started.

    A PID is not an identity, so "the parent is PID 4100" only becomes evidence
    once it names WHICH life of 4100. The creating process is by construction
    alive at the instant it creates a child, so the child's own start QPC
    selects the incarnation. Zero containing incarnations and two containing
    incarnations are both refused BY NAME rather than resolved to the nearest
    neighbour — the same posture `bind_thread_start_keys` takes.
    """
    candidates = _containing_incarnations(intervals, parent_process_id, started_qpc)
    if not candidates:
        raise EtwConsumerFault(
            "ETW_PROCESS_PARENT_START_KEY_UNBINDABLE:"
            f"{int(parent_process_id)}@{int(started_qpc)}")
    if len(candidates) > 1:
        raise EtwConsumerFault(
            f"ETW_PROCESS_INCARNATION_AMBIGUOUS:"
            f"{int(parent_process_id)}@{int(started_qpc)}")
    return candidates[0]


def bind_thread_start_keys(thread_events: Iterable[dict[str, Any]],
                           process_events: Iterable[dict[str, Any]],
                           ) -> list[dict[str, Any]]:
    """Give every thread event the process START KEY its own PID's start carried.

    A thread lifetime is keyed by (process_id, process_start_key) because a PID
    alone is not an identity — it is reused. The Microsoft-Windows-Kernel-Process
    THREAD payload does not carry the start key, so the key has to come from
    somewhere; the only source that is already in hand, already signed into the
    member roster and guaranteed to agree with it is the PROCESS stream this
    same consumer decoded. Binding from it is what makes the two rosters carry
    the same key BY CONSTRUCTION rather than by coincidence.

    The bind is by PID *and* QPC INTERVAL — the whole interval, both ends. Until
    2026-08-15 (AMENDMENT-2) this function said exactly that and did something
    weaker: it read only `kind == "START"` events, `continue`d past every
    ProcessStop, and bound a thread to the LAST start not in its future. A
    thread observed in the GAP between two incarnations of a reused PID —
    when no incarnation is alive at all — was therefore bound to the DEAD one,
    which is a foreign thread's work attributed to a member by name. Now a
    thread event binds to the incarnation whose interval CONTAINS its QPC:

      * exactly one containing incarnation -> bind it;
      * none -> `ETW_THREAD_START_KEY_UNBINDABLE:<pid>@<qpc>`;
      * more than one -> `ETW_PROCESS_INCARNATION_AMBIGUOUS:<pid>@<qpc>`, a
        world where one PID is alive twice at one instant, which cannot be
        resolved and must not be guessed at.

    Never a guess at the neighbouring incarnation and never a silent drop,
    which is the same posture as an absent PMC item.
    """
    intervals = process_incarnation_intervals(process_events)
    bound: list[dict[str, Any]] = []
    for event in thread_events:
        if not isinstance(event, dict):
            raise EtwConsumerFault("ETW_THREAD_LIFETIME_EVENT_INVALID")
        row = dict(event)
        if row.get("process_start_key") is not None:
            bound.append(row)
            continue
        process_id = row.get("process_id")
        if (not isinstance(process_id, int) or isinstance(process_id, bool)
                or process_id <= 0):
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_PID_INVALID:{process_id!r}")
        qpc = row.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_QPC_INVALID:{qpc!r}")
        candidates = _containing_incarnations(intervals, process_id, qpc)
        if not candidates:
            raise EtwConsumerFault(
                f"ETW_THREAD_START_KEY_UNBINDABLE:{int(process_id)}@{int(qpc)}")
        if len(candidates) > 1:
            raise EtwConsumerFault(
                f"ETW_PROCESS_INCARNATION_AMBIGUOUS:{int(process_id)}@{int(qpc)}")
        row["process_start_key"] = candidates[0]
        bound.append(row)
    return bound


def assemble_thread_lifetimes(thread_events: Iterable[dict[str, Any]],
                              member_lifetimes: Sequence[dict[str, Any]],
                              ) -> list[dict[str, Any]]:
    """Build the per-thread lifetimes every CSwitch delta is attributed to.

    `consume_cswitch()` refuses an event whose `OldThreadId` has no lifetime
    (`ETW_CSWITCH_UNATTRIBUTED_THREAD`), so an incomplete thread roster becomes
    a fault THERE rather than an unattributed delta silently dropping out of a
    retired-instruction total. A thread belonging to a process that is not a
    signed Job member is refused here.

    A THREAD ID IS NOT UNIQUE IN A CAPTURE (AMENDMENT-2, 2026-08-15). "The
    operating system may reuse a thread ID after the thread has terminated"
    (Learn, *PsGetThreadId* Remarks; *Thread Handles and Identifiers*), so one
    TID can carry SEVERAL lifetimes as long as they are DISJOINT. This used to
    key `starts`/`stops` by TID alone and raise
    `ETW_THREAD_LIFETIME_DUPLICATE_START` on the second start, which refused a
    perfectly ordinary long capture — right evidence, refused, with the whole
    receipt lost. Starts and stops are now paired IN QPC ORDER per TID, and:

      * two lifetimes for one TID that overlap or merely touch are the
        impossible world (the join would stop being a function) and fault
        `ETW_THREAD_LIFETIME_OVERLAPPING_REUSE:<tid>`;
      * two STARTs at the SAME qpc keep the older name,
        `ETW_THREAD_LIFETIME_DUPLICATE_START:<tid>`: identical timestamps are a
        duplicated event, not a second life;
      * a lifetime that does not NEST inside the member incarnation whose start
        key it carries faults `ETW_THREAD_LIFETIME_OUTSIDE_PROCESS:<tid>:<pair>`
        — the second half of the same defect, and the one that admits WRONG
        evidence, because the (PID, start key) pair alone says nothing about
        WHEN. This catches the thread events that arrive with a key already set
        and therefore never pass through `bind_thread_start_keys`.

    A STOP CARRIES ITS OWN PROCESS IDENTITY, AND THE PAIRING READS IT (codex-CLI
    r6 SEAT1 F2). A STOP's `(pid, start key)` was validated against the member
    roster and then discarded — only its QPC was kept — so a stop logged by
    member B could close a lifetime opened by member A, and a TID is unique to
    NEITHER: the assembled row then named A and carried B's end instant. Every
    CSwitch delta in that borrowed tail would be attributed to A's thread and
    signed as A's evidence. Start and stop must agree on the incarnation, and a
    pair that disagrees is `ETW_THREAD_LIFETIME_PROCESS_MISMATCH:<tid>:<start
    pair>!=<stop pair>`. The same TID living in two members, each with its own
    matched stop, is an ordinary capture and still assembles.
    """
    members = {(row["process_id"], row["process_start_key"]): row
               for row in member_lifetimes}
    starts: dict[int, list[dict[str, Any]]] = {}
    stops: dict[int, list[dict[str, Any]]] = {}
    order: list[int] = []
    for event in thread_events:
        if not isinstance(event, dict) or "kind" not in event:
            raise EtwConsumerFault("ETW_THREAD_LIFETIME_EVENT_INVALID")
        kind = str(event["kind"]).upper()
        thread_id = event.get("thread_id")
        if (not isinstance(thread_id, int) or isinstance(thread_id, bool)
                or thread_id <= 0):
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_TID_INVALID:{thread_id!r}")
        qpc = event.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_QPC_INVALID:{qpc!r}")
        pair = (event.get("process_id"), _start_key_text(event.get("process_start_key")))
        if pair not in members:
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_UNKNOWN_MEMBER:{pair}")
        if kind == "START":
            if any(row["started_qpc"] == int(qpc) for row in starts.get(thread_id, ())):
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_DUPLICATE_START:{thread_id}")
            if thread_id not in starts:
                order.append(thread_id)
            starts.setdefault(thread_id, []).append(
                {"process_id": pair[0], "process_start_key": pair[1],
                 "started_qpc": int(qpc)})
        elif kind == "STOP":
            if any(row["qpc"] == int(qpc) for row in stops.get(thread_id, ())):
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_DUPLICATE_STOP:{thread_id}")
            # The stop's own incarnation is KEPT, not just its instant: it is
            # half of the identity the pairing below has to agree on.
            stops.setdefault(thread_id, []).append(
                {"process_id": pair[0], "process_start_key": pair[1],
                 "qpc": int(qpc)})
        else:
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_EVENT_INVALID:{kind}")
    unmatched = sorted(thread_id for thread_id, ends in stops.items()
                       if len(ends) > len(starts.get(thread_id, ())))
    if unmatched:
        raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_UNMATCHED_STOP:{unmatched}")
    unterminated = sorted(thread_id for thread_id, begins in starts.items()
                          if len(begins) > len(stops.get(thread_id, ())))
    if unterminated:
        raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_INCOMPLETE:{unterminated}")
    rows: list[dict[str, Any]] = []
    for thread_id in order:
        lives = sorted(starts[thread_id], key=lambda row: row["started_qpc"])
        ends = sorted(stops[thread_id], key=lambda row: row["qpc"])
        previous_end: int | None = None
        for start, end in zip(lives, ends):
            ended = end["qpc"]
            start_pair = (start["process_id"], start["process_start_key"])
            stop_pair = (end["process_id"], end["process_start_key"])
            if start_pair != stop_pair:
                # A stop that belongs to another incarnation cannot end this
                # life: keeping the pair silent used to hand member A a lifetime
                # closed by member B's event (codex-CLI r6 SEAT1 F2).
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_PROCESS_MISMATCH:{thread_id}:"
                    f"{start_pair}!={stop_pair}")
            if ended <= start["started_qpc"]:
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_NONMONOTONIC:{thread_id}")
            if previous_end is not None and start["started_qpc"] <= previous_end:
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_OVERLAPPING_REUSE:{thread_id}")
            previous_end = ended
            pair = (start["process_id"], start["process_start_key"])
            member = members[pair]
            if not (member["started_qpc"] <= start["started_qpc"]
                    and ended <= member["ended_qpc"]):
                raise EtwConsumerFault(
                    f"ETW_THREAD_LIFETIME_OUTSIDE_PROCESS:{thread_id}:{pair}")
            rows.append({"process_id": start["process_id"],
                         "process_start_key": start["process_start_key"],
                         "thread_id": thread_id,
                         "started_qpc": start["started_qpc"], "ended_qpc": ended})
    return rows


@dataclass(frozen=True)
class MemberEventPartition:
    """One capture's events split into the measured Job's tree and the rest.

    Both halves are KEPT. The excluded half is not evidence about the Job and
    never reaches assembly, but it is counted into the capture's provenance, so
    "the host was busy" is an observed number rather than an invisible drop.
    """

    process_events: list[dict[str, Any]]
    thread_events: list[dict[str, Any]]
    excluded_process_events: list[dict[str, Any]]
    excluded_thread_events: list[dict[str, Any]]


def member_tree_incarnations(process_events: Iterable[dict[str, Any]], *,
                             root_process_id: int, root_process_start_key: str,
                             ) -> set[tuple[int, str]]:
    """The `(pid, start key)` incarnations reachable from the root by parenthood.

    Microsoft-Windows-Kernel-Process is a MACHINE-WIDE provider: when it is
    enabled on this session it delivers every process and thread event on the
    box, not the measured Job's. The Job's members are the root plus every
    descendant (the collector assigns the root before it resumes and leaves
    breakaway disabled, so a descendant joins the Job by inheritance), and the
    stream can say which starts those are: a ProcessStart names its creator,
    and the creator is alive at that instant, so the incarnation intervals
    identify WHICH life of that PID created it.

    The walk starts at the root pair and accepts a start whose parent
    incarnation is already accepted, to a fixpoint. A start whose parent is not
    in the tree is OUT OF POPULATION — foreign, excluded, never a fault, because
    an unrelated process running on the host is not evidence about this Job and
    refusing the capture because the box was not idle would be a ceiling on what
    the experiment can observe.

    A parent PID with TWO accepted incarnations containing the child's start is
    the impossible world (one PID alive twice at one instant) and keeps the
    existing name `ETW_PROCESS_INCARNATION_AMBIGUOUS`, because that IS a
    statement about member evidence.

    ⚠ THE PARENT LINK IS THE PAYLOAD'S, NOT THE HEADER'S (codex-CLI r7 P2). It
    used to be `EventHeader.ProcessId` — the process in whose context the start
    was LOGGED — which is the same thing only for an ordinary direct creation.
    For a brokered or explicit-parent creation the emitting context is a third
    process, so the header link dropped legitimate descendants out of the tree
    AND admitted foreign processes whose starts happened to be logged inside a
    member. The tuple now comes from `ParentProcessID` /
    `ParentProcessSequenceNumber` in the v3/v4 template
    (`KERNEL_PROCESS_START_PARENT_LAYOUTS`), which is what the provider declares
    the parent to be; the header pid survives as `event_header_process_id`,
    diagnostic evidence that decides nothing. This link is still pinned by the
    same manifest uncertainty as the rest of the payload offsets — module
    docstring item 4 — and a tree that came out too SMALL is not silent: the
    roster count is cross-checked against the Job's own `TotalProcesses` by
    `mbcx01_r13_measurement._validate_query_evidence` (:789-791), which refuses a
    disagreement in either direction.
    """
    events = list(process_events)
    intervals = process_incarnation_intervals(events)
    accepted = {(int(root_process_id), _start_key_text(root_process_start_key))}
    starts: list[tuple[int, int, str, Any, Any]] = []
    for event in events:
        if not isinstance(event, dict):
            raise EtwConsumerFault("ETW_PROCESS_LIFETIME_EVENT_INVALID")
        if str(event.get("kind", "")).upper() != "START":
            continue
        starts.append((int(event["qpc"]), int(event["process_id"]),
                       _start_key_text(event.get("process_start_key")),
                       event.get("parent_process_id"),
                       event.get("parent_process_start_key")))
    starts.sort(key=lambda row: row[0])
    growing = True
    while growing:
        growing = False
        for qpc, process_id, key, parent_id, parent_key in starts:
            if (process_id, key) in accepted:
                continue
            if (not isinstance(parent_id, int) or isinstance(parent_id, bool)
                    or parent_id <= 0):
                continue  # nothing links this start to the tree
            if parent_key not in (None, 0):
                if (int(parent_id), _start_key_text(parent_key)) in accepted:
                    accepted.add((process_id, key))
                    growing = True
                continue
            candidates = [candidate for candidate
                          in _containing_incarnations(intervals, parent_id, qpc)
                          if (int(parent_id), candidate) in accepted]
            if len(candidates) > 1:
                raise EtwConsumerFault(
                    f"ETW_PROCESS_INCARNATION_AMBIGUOUS:{int(parent_id)}@{int(qpc)}")
            if candidates:
                accepted.add((process_id, key))
                growing = True
    return accepted


def partition_job_member_events(process_events: Iterable[dict[str, Any]],
                                thread_events: Iterable[dict[str, Any]], *,
                                root_process_id: int,
                                root_process_start_key: str,
                                ) -> MemberEventPartition:
    """Split a machine-wide capture into the measured Job's events and the rest.

    This is the SCOPE the provider itself cannot apply. `EnableTraceEx2` is
    called before the candidate is resumed, when the only member that exists is
    the suspended root, so no filter written at enable time can name the
    descendants that appear later; the population is therefore decided HERE,
    once, against the tree `member_tree_incarnations()` derives, and before any
    assembly runs.

    Exclusion is SCOPING, never silencing. What is excluded is exactly what is
    not evidence about this Job:

      * a process event whose `(pid, start key)` is not in the tree — including
        the ProcessStop of a host process that started before this session and
        would otherwise have been an `ETW_PROCESS_LIFETIME_UNMATCHED_STOP`, and
        the ProcessStart of a host process that would otherwise have been
        assembled INTO the signed roster and contradicted the Job's own
        `TotalProcesses`;
      * a thread event whose PID, at that thread's QPC, was owned by an
        incarnation that is not in the tree, or whose PID never appears in the
        tree at all — the host threads that would otherwise have faulted as
        `ETW_THREAD_START_KEY_UNBINDABLE`.

    What is NOT excluded, because it is a statement about MEMBER evidence and
    must keep faulting by name:

      * any event whose shape is invalid — it is passed through so that the
        assembler names the fault it always named;
      * a thread event on a MEMBER PID at an instant when no incarnation of
        that PID was alive at all (member or foreign). That is the stream
        disagreeing with itself about a member, and it still reaches
        `bind_thread_start_keys` and still raises
        `ETW_THREAD_START_KEY_UNBINDABLE`.
    """
    events = list(process_events)
    threads = list(thread_events)
    intervals = process_incarnation_intervals(events)
    accepted = member_tree_incarnations(
        events, root_process_id=root_process_id,
        root_process_start_key=root_process_start_key)
    member_process_ids = {process_id for process_id, _key in accepted}
    kept_processes: list[dict[str, Any]] = []
    foreign_processes: list[dict[str, Any]] = []
    for event in events:
        if not isinstance(event, dict) or str(event.get("kind", "")).upper() \
                not in {"START", "STOP"}:
            kept_processes.append(event)  # malformed: the assembler names it
            continue
        pair = (int(event["process_id"]), _start_key_text(event.get("process_start_key")))
        (kept_processes if pair in accepted else foreign_processes).append(event)
    kept_threads: list[dict[str, Any]] = []
    foreign_threads: list[dict[str, Any]] = []
    for event in threads:
        if not isinstance(event, dict):
            kept_threads.append(event)
            continue
        process_id = event.get("process_id")
        if (not isinstance(process_id, int) or isinstance(process_id, bool)
                or process_id <= 0):
            kept_threads.append(event)
            continue
        key = event.get("process_start_key")
        if key is not None:
            try:
                pair = (int(process_id), _start_key_text(key))
            except EtwConsumerFault:
                kept_threads.append(event)
                continue
            (kept_threads if pair in accepted else foreign_threads).append(event)
            continue
        qpc = event.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            kept_threads.append(event)
            continue
        containing = _containing_incarnations(intervals, process_id, qpc)
        if any((int(process_id), candidate) in accepted for candidate in containing):
            kept_threads.append(event)
        elif containing or int(process_id) not in member_process_ids:
            foreign_threads.append(event)
        else:
            kept_threads.append(event)
    return MemberEventPartition(kept_processes, kept_threads,
                                foreign_processes, foreign_threads)


@dataclass(frozen=True)
class CswitchMemberScope:
    """One capture's CSwitch records split into member-attributed and foreign.

    `records` is what `EtwPmcSession.consume_cswitch()` is handed; every one of
    them names an outgoing thread the signed member roster knows. `excluded`
    holds the foreign records VERBATIM, raw counter values included, so the
    per-processor arithmetic they were used for stays auditable and "the host
    was busy" is a counted observation rather than an invisible drop.
    """

    records: list[dict[str, Any]]
    excluded: list[dict[str, Any]]
    foreign_instructions: int
    baseline_records: int
    #: Roster-TID records kept because NO lifetime this capture knows — member
    #: or foreign — contains their QPC. They still fault downstream; the count
    #: is what tells an aborted capture's operator "the host recycled a TID we
    #: cannot place" from "the roster is incomplete".
    roster_tid_outside_any_lifetime: int = 0
    #: AMENDMENT-3 (2026-08-16): per-processor predecessor baselines — rows of
    #: {"processor", "counter_value"}, one for each processor whose first KEPT
    #: record has a predecessor of any kind in the raw stream. The raw counter
    #: of that predecessor is the only evidence the first member interval can
    #: be measured against; without it the delta rule's first-record zero
    #: silently discarded real member work of unbounded magnitude (the r6
    #: NO-GO: 100 signed where the stream proved 1,000,100). A processor whose
    #: first record ever is the member switch-out carries its OWN counter —
    #: capture-start
    #: truncation, declared, small by construction.
    first_member_baselines: tuple[dict[str, int], ...] = ()


def foreign_thread_intervals(thread_events: Iterable[dict[str, Any]],
                             ) -> dict[int, list[tuple[int, int | None]]]:
    """Every FOREIGN thread id's observed lives as `(started_qpc, ended_qpc)`.

    The events are the half `partition_job_member_events()` already separated —
    nothing is re-derived here and no new stream is opened; the starts and
    stops are simply paired per TID, in QPC order, the way
    `process_incarnation_intervals()` pairs process incarnations.

    `ended_qpc` is `None` when the stream carries no ThreadStop for that start
    (an OPEN interval, never a closed one guessed at the window edge).

    A LEADING ThreadStop with NO preceding ThreadStart — a host thread that
    already existed when the session opened — yields a CAPTURE-PREFIX interval
    `(0, stop_qpc)` (r7 fold, SEAT2 CHANGE ruling 2a, SEAT1's named alternative
    concurring). Nothing is guessed: the stop time is observed, a TID is unique
    while its thread is live and reusable only after termination (PsGetThreadId
    Remarks), so every earlier in-capture switch naming that TID belongs to the
    pre-existing incarnation. The member branch still wins containment first,
    so the prefix interval can never move a member's work out of the
    measurement — it can only stop an ordinary pre-existing host thread from
    aborting the one-shot capture when the member later receives the recycled
    TID. Only the FIRST leading stop forms the prefix; any further unmatched
    stop still yields no interval (a second life cannot precede the capture).
    """
    starts: dict[int, list[int]] = {}
    stops: dict[int, list[int]] = {}
    for event in thread_events:
        if not isinstance(event, dict):
            raise EtwConsumerFault("ETW_THREAD_LIFETIME_EVENT_INVALID")
        kind = str(event.get("kind", "")).upper()
        if kind not in {"START", "STOP"}:
            continue
        thread_id = event.get("thread_id")
        if (not isinstance(thread_id, int) or isinstance(thread_id, bool)
                or thread_id <= 0):
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_TID_INVALID:{thread_id!r}")
        qpc = event.get("qpc")
        if not isinstance(qpc, int) or isinstance(qpc, bool) or qpc < 0:
            raise EtwConsumerFault(f"ETW_THREAD_LIFETIME_QPC_INVALID:{qpc!r}")
        (starts if kind == "START" else stops).setdefault(
            int(thread_id), []).append(int(qpc))
    intervals: dict[int, list[tuple[int, int | None]]] = {}
    for thread_id in set(starts) | set(stops):
        begins = sorted(starts.get(thread_id, ()))
        ends = sorted(stops.get(thread_id, ()))
        cursor = 0
        rows: list[tuple[int, int | None]] = []
        # r7 fold: a leading stop is a pre-existing thread's terminal — the
        # capture prefix through that stop is its known life.
        if ends and (not begins or ends[0] < begins[0]):
            rows.append((0, ends[0]))
            cursor = 1
        for started in begins:
            while cursor < len(ends) and ends[cursor] < started:
                cursor += 1
            if cursor < len(ends):
                rows.append((started, ends[cursor]))
                cursor += 1
            else:
                rows.append((started, None))
        if rows:
            intervals[thread_id] = rows
    return intervals


def _lifetime_contains(intervals: dict[int, list[tuple[int, int | None]]],
                       thread_id: int, qpc: int) -> bool:
    """Is `thread_id` alive at `qpc` in any of the intervals given?

    Containment includes BOTH ends of a closed interval and everything at or
    after the start of an open one — the same rule
    `_containing_incarnations()` applies to processes, spelled once here for
    threads so the two scopes cannot drift apart.
    """
    return any(started <= qpc and (ended is None or qpc <= ended)
               for started, ended in intervals.get(int(thread_id), ()))


def scope_cswitch_records_to_members(records: Iterable[dict[str, Any]],
                                     thread_lifetimes: Iterable[dict[str, Any]],
                                     foreign_thread_events: Iterable[dict[str, Any]] = (),
                                     ) -> CswitchMemberScope:
    """Keep foreign context switches as BASELINES only, never as member deltas.

    The CSwitch stream is machine-wide for the same reason the process stream
    is (`_enable_process_provider`), so on any non-idle host most switches
    belong to threads the measured Job never held. Handing those to
    `consume_cswitch()` aborts the collection by name
    (`ETW_CSWITCH_UNATTRIBUTED_THREAD`) after the candidate has already run,
    which is a wrong diagnosis of right evidence.

    THE ARITHMETIC IS WHY THIS IS NOT A FILTER. `consume_cswitch()` — and,
    independently, the frozen validator
    (`mbcx01_r13_measurement._validate_physical_evidence`, :1031-1039) —
    recompute each delta as `counter_value` minus the previous
    `counter_value` ON THE SAME PROCESSOR *IN THE EMITTED STREAM*, and every
    emitted row must resolve to a member thread. Dropping foreign rows and
    passing raw counters through would therefore telescope each member delta
    across the foreign intervals in between: the aggregate would become the
    instructions retired by the WHOLE MACHINE between the first and last member
    switch on each processor. So the foreign records are used HERE, once, for
    exactly the arithmetic they are evidence for:

      * a kept record's emitted `instruction_retired` is its RAW counter minus
        the foreign work already accumulated on that processor, so the delta
        the two downstream recomputations produce is exactly
        `raw(this switch) - raw(the switch immediately before it)` — the
        interval the member thread actually ran, whatever ran before it;
      * with no foreign records at all the subtraction is zero and every
        emitted value is the RAW counter, byte-identical to before;
      * `excluded` keeps the foreign records with their raw values, and
        `foreign_instructions` is what was subtracted.

    ⚠ SO `counter_value` IN A SCOPED CAPTURE IS A PER-PROCESSOR MEMBER-
    ATTRIBUTED ACCUMULATOR, NOT THE RAW MSR VALUE. It is stated here because
    the receipt carries the number: the frozen observation schema
    (`CSWITCH_OBSERVATION_KEYS`) has one counter field and no room for both, and
    of the two readings only this one makes `delta_from_previous` mean what the
    signed attribution string says it means
    ("SUM_INSTRUCTIONRETIRED_CSWITCH_DELTAS_BY_OLD_THREAD_...").

    ⚠ BOUNDED, DECLARED UNDERCOUNT: the first emitted record on a processor has
    no predecessor in the emitted stream, so both recomputations give it delta
    0 and the interval ending at it is not counted. That rule is not new — it
    is how the contract has always treated the first record on a processor —
    but scoping changes WHICH interval it discards, from the first switch of
    any kind to the first MEMBER switch. `baseline_records` counts them (one
    per processor that carries any member switch) so the discarded intervals
    are visible in the capture's provenance rather than implied.

    MEMBERSHIP IS DECIDED BY TID *AND* QPC (2026-08-16, council r6). "The
    operating system may reuse a thread ID after the thread has terminated"
    (Learn, *PsGetThreadId* Remarks), so a roster TID alone does not say the
    switch belongs to the member. Until this fold the scope kept any roster-TID
    record whatever its QPC, so an ordinary mid-capture reuse by a host process
    reached `consume_cswitch()`, was refused as
    `ETW_CSWITCH_UNATTRIBUTED_THREAD`, and destroyed a valid capture after the
    candidate had already run — right evidence refused. The three cases are now
    told apart by evidence that is ALREADY IN HAND:

      * QPC inside a MEMBER lifetime of that TID -> member, kept, unchanged;
      * QPC inside a KNOWN FOREIGN lifetime of that TID (the incarnation
        `partition_job_member_events()` separated, paired by
        `foreign_thread_intervals()`) -> treated as ANY other foreign record:
        its raw value feeds the per-processor baseline/offset arithmetic and it
        lands in `excluded`. This is a CLASSIFICATION change only; not one term
        of the arithmetic below moves;
      * QPC inside NO lifetime this capture knows -> KEPT, exactly as before,
        so `consume_cswitch()` still refuses it by name — and counted in
        `roster_tid_outside_any_lifetime`, because "the host recycled a TID we
        cannot place" and "the roster is incomplete" are different findings and
        the operator of an aborted capture has to be able to tell them apart.

    WHAT IS KEPT DESPITE LOOKING FOREIGN, so that member faults stay faults:

      * a record whose outgoing TID is in the signed roster and whose QPC is in
        none of the known lifetimes, as above: the stream disagreeing with
        itself about a member, refused downstream rather than absorbed here.
      * a raw counter that goes BACKWARDS across a foreign interval is
        `ETW_PMC_COUNTER_WENT_BACKWARDS` here, because after exclusion nothing
        downstream would ever see that step. A backwards step ending at a KEPT
        record still surfaces downstream, unchanged.

    The records must arrive in per-processor timestamp order — the order
    `order_records_per_processor()` produces and that the delta rule requires;
    an out-of-order stream is refused rather than rebased against the wrong
    predecessor.

    `foreign_thread_events` is the partition's excluded half. Given none — the
    case where no foreign-lifetime evidence exists at all — every roster-TID
    record outside a member lifetime is unplaceable and the pre-fold fail-loud
    posture is exactly what is left, now counted.
    """
    member_thread_ids = set()
    member_intervals: dict[int, list[tuple[int, int | None]]] = {}
    for row in thread_lifetimes:
        if not isinstance(row, dict) or "thread_id" not in row:
            raise EtwConsumerFault("ETW_THREAD_LIFETIME_ROW_INVALID")
        thread_id = int(row["thread_id"])
        member_thread_ids.add(thread_id)
        started = row.get("started_qpc")
        ended = row.get("ended_qpc")
        if (isinstance(started, int) and not isinstance(started, bool)
                and isinstance(ended, int) and not isinstance(ended, bool)):
            member_intervals.setdefault(thread_id, []).append(
                (int(started), int(ended)))
        else:
            # A roster row with no interval cannot place anything in time, so
            # it covers the whole capture — which is exactly the behaviour
            # every caller had before lifetimes were consulted. The production
            # roster (`assemble_thread_lifetimes()`) always carries both ends.
            member_intervals.setdefault(thread_id, []).append((0, None))
    foreign_intervals = foreign_thread_intervals(foreign_thread_events)
    # r8 fold (SEAT2 F1, EXECUTED): one TID cannot be alive as a member and as a
    # foreign thread at the same instant — a TID is unique system-wide while its
    # thread exists and is reusable only after termination (PsGetThreadId). An
    # overlap between the two derived interval sets is therefore an internally
    # CONTRADICTORY trace, not an ambiguity to resolve: the member-first rule
    # below would silently pick a side and attribute a delta under ownership the
    # stream itself contradicts. It fails loud instead. (The impossible input is
    # platform-unreachable today; this is a consistency check between two of our
    # OWN derived structures, at correctness volume — no adversary is implied.)
    for thread_id, member_rows in member_intervals.items():
        for m_start, m_end in member_rows:
            for f_start, f_end in foreign_intervals.get(thread_id, ()):
                m_stop = m_end if m_end is not None else None
                f_stop = f_end if f_end is not None else None
                starts_before_other_ends = (f_stop is None or m_start <= f_stop)
                other_starts_before_ends = (m_stop is None or f_start <= m_stop)
                if starts_before_other_ends and other_starts_before_ends:
                    raise EtwConsumerFault(
                        "ETW_THREAD_MEMBER_FOREIGN_INTERVAL_OVERLAP:"
                        f"{thread_id}@member[{m_start},{m_end}]"
                        f"/foreign[{f_start},{f_end}]")
    kept: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    previous_raw: dict[int, int] = {}
    previous_qpc: dict[int, int] = {}
    foreign_offset: dict[int, int] = {}
    foreign_instructions = 0
    baseline_records = 0
    roster_tid_outside_any_lifetime = 0
    first_member_baselines: list[dict[str, int]] = []
    for record in records:
        if not isinstance(record, dict):
            raise EtwConsumerFault("ETW_CSWITCH_RECORD_INCOMPLETE:not_a_record")
        missing = [name for name in RECORD_FIELDS if name not in record]
        if missing:
            raise EtwConsumerFault(
                f"ETW_CSWITCH_RECORD_INCOMPLETE:{','.join(sorted(missing))}")
        processor = int(record["processor"])
        qpc = int(record["qpc"])
        raw = int(record["instruction_retired"])
        if processor in previous_qpc and qpc < previous_qpc[processor]:
            raise EtwConsumerFault(
                f"ETW_CSWITCH_RECORDS_UNORDERED:{processor}@{qpc}")
        previous_qpc[processor] = qpc
        prior = previous_raw.get(processor)
        step = 0 if prior is None else raw - prior
        previous_raw[processor] = raw
        old_thread_id = int(record["old_thread_id"])
        member_switch = _lifetime_contains(member_intervals, old_thread_id, qpc)
        unplaceable = (not member_switch
                       and old_thread_id in member_thread_ids
                       and not _lifetime_contains(foreign_intervals,
                                                  old_thread_id, qpc))
        if member_switch or unplaceable:
            if unplaceable:
                roster_tid_outside_any_lifetime += 1
            if processor not in foreign_offset:
                baseline_records += 1
                foreign_offset[processor] = 0
                # AMENDMENT-3, r7 totality rule: EVERY processor with a kept
                # record emits a baseline row — the predecessor's raw counter
                # when one exists (offset-consistent by construction: the
                # foreign offset only starts accumulating from this record on),
                # or this record's OWN raw at capture-start, whose delta is
                # then the declared zero. Totality is what lets the frozen
                # validator refuse an empty-but-forgotten baseline set: an
                # absent row is no longer expressible for an observed
                # processor (r7, three seats convergent, SEAT2 end-to-end).
                first_member_baselines.append(
                    {"processor": processor,
                     "counter_value": int(prior) if prior is not None else raw})
            emitted = raw - foreign_offset[processor]
            if emitted < 0:
                raise EtwConsumerFault(
                    f"ETW_PMC_COUNTER_WENT_BACKWARDS:{processor}@{qpc}")
            row = dict(record)
            row["instruction_retired"] = emitted
            kept.append(row)
            continue
        if step < 0:
            raise EtwConsumerFault(
                f"ETW_PMC_COUNTER_WENT_BACKWARDS:{processor}@{qpc}")
        if processor in foreign_offset:
            # Only work that lands BETWEEN two emitted member records has to be
            # subtracted; foreign switches before this processor's first member
            # switch are already outside the emitted chain.
            foreign_offset[processor] += step
            foreign_instructions += step
        excluded.append(dict(record))
    return CswitchMemberScope(kept, excluded, foreign_instructions,
                              baseline_records,
                              roster_tid_outside_any_lifetime,
                              tuple(first_member_baselines))


def record_cswitch_scope_provenance(scope: CswitchMemberScope) -> dict[str, Any]:
    """The counted facts a scoped CSwitch stream leaves behind.

    Exclusion is scoping, never silencing: how many switches were foreign, how
    many instructions their intervals accounted for, how many per-processor
    baseline records the contract discarded, how many roster TIDs could not be
    placed in any known life, and how many member-attributed records survived —
    all of them are numbers a reviewer can read off the capture, not inferences
    from a smaller list.

    ⚠ THE TWO EXCLUSION NUMBERS HAVE DIFFERENT DENOMINATORS, and the field name
    now says which is which. `excluded_foreign_cswitch_records` counts EVERY
    excluded record; `foreign_instructions_excluded_after_first_member`
    accumulates only the steps taken after that processor's first member record,
    because foreign work before it is outside the emitted chain and is
    deliberately never subtracted from anything. Dividing one by the other was
    always meaningless; the name is what stops an auditor doing it.
    """
    return {"cswitch_scope": "JOB_MEMBER_THREAD_ROSTER",
            "member_attributed_cswitch_records": len(scope.records),
            "excluded_foreign_cswitch_records": len(scope.excluded),
            "foreign_instructions_excluded_after_first_member":
                int(scope.foreign_instructions),
            "per_processor_baseline_records": int(scope.baseline_records),
            "kept_roster_tid_outside_any_lifetime":
                int(scope.roster_tid_outside_any_lifetime)}


@dataclass(frozen=True)
class LossCounters:
    """The three loss counters `ControlTraceW(EVENT_TRACE_CONTROL_QUERY)` returns.

    Each is documented as an OUTPUT member of EVENT_TRACE_PROPERTIES:
    "EventsLost - the number of events that were not recorded",
    "LogBuffersLost - buffers that could not be written to the log file",
    "RealTimeBuffersLost - buffers that could not be delivered in real-time".
    Any one of them being nonzero means the observed CSwitch stream is not the
    whole stream, so no attributed total derived from it can be exact.
    """

    events_lost: int = 0
    log_buffers_lost: int = 0
    realtime_buffers_lost: int = 0

    def any_loss(self) -> bool:
        return bool(self.events_lost or self.log_buffers_lost
                    or self.realtime_buffers_lost)


def granted_capability_facts(*, pmc_source_available: bool, max_pmc_counters: int,
                             counter_owner_conflict_count: int,
                             multiplexing_detected: bool,
                             attribution_complete: bool,
                             counter_width_bits: int,
                             profile_source_name: str,
                             profile_source_id: int) -> dict[str, Any]:
    """The closed record of what the platform actually GRANTED.

    Deliberately separate from the session's `capability` record: `capability`
    is the frozen five-key EVIDENCE shape (`CAPABILITY_QUERY_KEYS`) that
    `collect()` copies verbatim into `trace_capability_query`, and it cannot
    carry an extra key without failing the frozen validator. Before this build,
    `mbcx01_build_win32._trace_facts` read the granted facts out of that same
    five-key dict, so a healthy PMU could only ever be reported as
    `etw_pmc_source_available: False` — see repair ledger row BB-16.
    """
    facts = {"pmc_source_available": bool(pmc_source_available),
             "max_pmc_counters": int(max_pmc_counters),
             "counter_owner_conflict_count": int(counter_owner_conflict_count),
             "multiplexing_detected": bool(multiplexing_detected),
             "attribution_complete": bool(attribution_complete),
             "counter_width_bits": int(counter_width_bits),
             "profile_source_name": str(profile_source_name),
             "profile_source_id": int(profile_source_id)}
    if set(facts) != CAPABILITY_FACT_KEYS:
        raise EtwConsumerFault("ETW_CAPABILITY_FACT_KEYS_INVALID")
    return facts


def granted_capability_facts_for_test(**changes: Any) -> dict[str, Any]:
    """A fully-granted facts record, for witnesses and for review reading.

    FIXTURE AFFORDANCE ONLY. It fabricates nothing at run time: the OS layer
    builds its facts from `TraceQueryInformation` output via
    `granted_capability_facts()`, and this helper exists so a witness can state
    the granted baseline it is perturbing.
    """
    baseline = {"pmc_source_available": True, "max_pmc_counters": 2,
                "counter_owner_conflict_count": 0, "multiplexing_detected": False,
                "attribution_complete": True, "counter_width_bits": 64,
                "profile_source_name": win32.PMC_SOURCE_NAME, "profile_source_id": 0}
    baseline.update(changes)
    return granted_capability_facts(**baseline)


def evaluate_evidence_availability(*, capability_facts: dict[str, Any],
                                   loss: LossCounters) -> tuple[bool, tuple[str, ...]]:
    """Decide whether the PMC evidence is AVAILABLE, and name every reason if not.

    Harness requirements §4: "zero owner conflict, multiplexing, scaling
    ambiguity, EventsLost, LogBuffersLost and RealTimeBuffersLost" and
    "Unsupported, lossy, incomplete or ambiguous evidence is unavailable, never
    diagnostic-only success."

    Returns EVERY reason rather than the first, because a run that is
    unavailable for three reasons is a different finding from one that is
    unavailable for one, and the runbook asks for capability gaps verbatim.
    """
    if (not isinstance(capability_facts, dict)
            or set(capability_facts) != CAPABILITY_FACT_KEYS):
        raise EtwConsumerFault("ETW_CAPABILITY_FACTS_STRUCTURE_INVALID")
    reasons: list[str] = []
    if not capability_facts["pmc_source_available"]:
        reasons.append("ETW_PMC_SOURCE_UNAVAILABLE")
    if int(capability_facts["max_pmc_counters"]) < 1:
        reasons.append("ETW_PMC_NO_COUNTERS_GRANTED")
    if int(capability_facts["counter_owner_conflict_count"]) > 0:
        reasons.append("ETW_PMC_COUNTER_OWNER_CONFLICT")
    if capability_facts["multiplexing_detected"]:
        reasons.append("ETW_PMC_MULTIPLEXING_DETECTED")
    if not capability_facts["attribution_complete"]:
        reasons.append("ETW_ATTRIBUTION_INCOMPLETE")
    if int(capability_facts["counter_width_bits"]) != 64:
        reasons.append("ETW_PMC_COUNTER_WIDTH_AMBIGUOUS")
    if int(loss.events_lost) != 0:
        reasons.append("ETW_EVENTS_LOST")
    if int(loss.log_buffers_lost) != 0:
        reasons.append("ETW_LOG_BUFFERS_LOST")
    if int(loss.realtime_buffers_lost) != 0:
        reasons.append("ETW_REALTIME_BUFFERS_LOST")
    return (not reasons), tuple(reasons)


def require_available_evidence(*, capability_facts: dict[str, Any],
                               loss: LossCounters) -> None:
    """Refuse to proceed on unavailable evidence.

    Called before any attributed total is computed, so the failure mode is a
    named refusal and never an estimated instruction count.
    """
    available, reasons = evaluate_evidence_availability(
        capability_facts=capability_facts, loss=loss)
    if not available:
        raise EtwConsumerFault("ETW_EVIDENCE_UNAVAILABLE:" + ",".join(reasons))


def classify_execution_environment(*, hypervisor_present: bool,
                                   is_root_partition: bool,
                                   nested_virtualization: bool,
                                   host_architecture: str,
                                   guest_pmu_capability_receipt_digest: str | None = None,
                                   ) -> dict[str, Any]:
    """The smoke-cell precondition gate, in the frozen `ENVIRONMENT_KEYS` shape.

    Harness requirements §1: an eligible Windows host or a Hyper-V ROOT
    partition. A guest is eligible only when explicitly granted PMU access with
    a SIGNED capability receipt. Nested virtualization is UNSUPPORTED.

    The smoke authorization is narrower still and says so in terms: "If the
    operator finds this is executing inside a GUEST, ABORT." This function
    therefore refuses a guest outright unless a signed PMU capability receipt
    digest is supplied, and refuses nesting unconditionally.
    """
    if str(host_architecture) != "WINDOWS_64BIT":
        raise EtwConsumerFault(
            f"SMOKE_ENVIRONMENT_ARCHITECTURE_UNSUPPORTED:{host_architecture}")
    if nested_virtualization:
        raise EtwConsumerFault("SMOKE_ENVIRONMENT_IS_NESTED")
    if not hypervisor_present:
        kind = "BARE_METAL_WINDOWS"
    elif is_root_partition:
        kind = "HYPER_V_ROOT_PARTITION"
    elif guest_pmu_capability_receipt_digest:
        return {"execution_environment": "HYPER_V_GUEST",
                "host_architecture": "WINDOWS_64BIT",
                "nested_virtualization": False,
                "guest_pmu_exposure": "EXPLICITLY_ENABLED",
                "guest_pmu_capability_receipt_digest":
                    str(guest_pmu_capability_receipt_digest).upper()}
    else:
        raise EtwConsumerFault(
            "SMOKE_ENVIRONMENT_IS_A_VIRTUALIZATION_GUEST:"
            "a guest needs an explicit signed PMU capability receipt "
            "(harness requirements section 1); the smoke authorization says ABORT")
    return {"execution_environment": kind,
            "host_architecture": "WINDOWS_64BIT",
            "nested_virtualization": False,
            "guest_pmu_exposure": "NOT_APPLICABLE",
            "guest_pmu_capability_receipt_digest": None}


# ==========================================================================
# The seam `collect()` consumes
# ==========================================================================


@dataclass
class CapturedTrace:
    """Everything ONE consumed trace yielded — and nothing else.

    The OS layer fills this from `ProcessTrace`; a witness fills it with
    synthetic records. Both go through the SAME assembly path below, so the
    reviewable logic and the physical logic are one code path and never two.
    """

    cswitch_records: list[dict[str, Any]]
    process_events: list[dict[str, Any]]
    thread_events: list[dict[str, Any]]
    capability_facts: dict[str, Any]
    loss: LossCounters
    session_handle: int
    source_id: int
    counter_index: int = PINNED_INSTRUCTION_RETIRED_INDEX
    reordered_record_count: int = 0
    provenance: dict[str, Any] = field(default_factory=dict)
    #: The thread events `partition_job_member_events()` put OUTSIDE the member
    #: tree. Carried rather than dropped because they are the only evidence
    #: that tells a recycled member TID from an unplaceable one; the CSwitch
    #: scope consumes them and nothing else does.
    foreign_thread_events: list[dict[str, Any]] = field(default_factory=list)


def capability_evidence_record(*, source_id: int,
                               counter_width_bits: int = 64) -> dict[str, Any]:
    """The frozen five-key `CAPABILITY_QUERY_KEYS` evidence record.

    `query_status_code` is 0 because a nonzero status is a FAULT that aborts
    the collection long before a receipt exists — the collector never records
    a failed capability query as a value.
    """
    return {"query_status_code": 0,
            "counter_information_class": "TracePmcCounterListInfo",
            "event_information_class": "TracePmcEventListInfo",
            "source_id": int(source_id),
            "counter_width_bits": int(counter_width_bits)}


def event_attachment_record() -> dict[str, Any]:
    """The frozen five-key `EVENT_ATTACHMENT_KEYS` evidence record."""
    return {"counter_query_class": "TracePmcCounterListInfo",
            "event_query_class": "TracePmcEventListInfo",
            "profile_source": win32.PMC_SOURCE_NAME.upper(),
            "event_list": win32.PMC_EVENT_LIST.upper(),
            "attached": True}


def build_etw_pmc_session(capture: CapturedTrace, *, job_object_id: str,
                          root_process_id: int,
                          root_process_start_key: str) -> win32.EtwPmcSession:
    """Assemble the exact `EtwPmcSession` `collect()` expects from a capture.

    Order matters and is the evidence: refuse unavailable evidence FIRST, then
    order the records, then PARTITION the capture to the measured Job's member
    tree, then assemble the member roster, then the thread roster (which is
    validated against that roster), then SCOPE the CSwitch stream to that
    thread roster, and only then hand the collector a session. Nothing is
    defaulted and nothing is estimated at any step.

    The CSwitch scope comes last because it is the first point at which the
    signed thread roster exists: `scope_cswitch_records_to_members()` decides
    membership against that roster, keeps foreign switches as per-processor
    baselines only, and records what it excluded in the capture's provenance.

    Both scopes run on this path as well as on the live one so that the
    reviewable logic and the physical logic stay ONE code path: a witness
    capture and a real capture are scoped by the same functions, in the same
    positions, against the same root identity.
    """
    require_available_evidence(capability_facts=capture.capability_facts,
                               loss=capture.loss)
    ordered, reordered = order_records_per_processor(capture.cswitch_records)
    capture.reordered_record_count = reordered
    partition = partition_job_member_events(
        capture.process_events, capture.thread_events,
        root_process_id=root_process_id,
        root_process_start_key=root_process_start_key)
    members = assemble_member_lifetimes(
        partition.process_events, job_object_id=job_object_id,
        root_process_id=root_process_id,
        root_process_start_key=root_process_start_key)
    threads = assemble_thread_lifetimes(partition.thread_events, members)
    # BOTH sources of foreign-lifetime evidence: the partition taken here (a
    # capture handed over raw) and the one `capture()` already took (a capture
    # that arrived scoped). Neither is recomputed; a lifetime observed twice is
    # the same interval twice and decides containment identically.
    scope = scope_cswitch_records_to_members(
        ordered, threads,
        list(partition.excluded_thread_events) + list(capture.foreign_thread_events))
    capture.provenance.update(record_cswitch_scope_provenance(scope))
    def already_closed(session: win32.EtwPmcSession) -> None:
        """The pre-captured finalizer. NOT a no-op: it RE-CHECKS completeness.

        A replay/witness session is built from a capture that is already whole,
        so closing its window has nothing left to do — but "nothing left to do"
        still has to be VERIFIED, otherwise `close_trace_window()` would be a
        hook that silently accepts an incomplete roster on this path while
        enforcing one on the live path.
        """
        if not session.member_lifetimes or not session.thread_lifetimes:
            raise win32.CollectorFault("ETW_TRACE_WINDOW_ROSTER_INCOMPLETE")
        require_available_evidence(capability_facts=capture.capability_facts,
                                   loss=capture.loss)

    return win32.EtwPmcSession(
        session_handle=int(capture.session_handle),
        capability=capability_evidence_record(
            source_id=capture.source_id,
            counter_width_bits=int(capture.capability_facts["counter_width_bits"])),
        attachment=event_attachment_record(),
        observations=[],
        thread_lifetimes=threads,
        events_lost=int(capture.loss.events_lost),
        log_buffers_lost=int(capture.loss.log_buffers_lost),
        realtime_buffers_lost=int(capture.loss.realtime_buffers_lost),
        record_stream=lambda: list(scope.records),
        member_lifetimes=members,
        event_id_blob=classic_event_id_blob(),
        capability_facts=dict(capture.capability_facts),
        first_member_baselines=scope.first_member_baselines,
        trace_finalizer=already_closed)


def make_etw_session_factory(capture: CapturedTrace, *, job_object_id: str,
                             root_process_id: int, root_process_start_key: str,
                             ) -> Callable[[], win32.EtwPmcSession]:
    """Return the callable `collect(etw_session_factory=...)` takes.

    `collect()` calls the factory ONCE, after the root exists suspended and is
    assigned to the Job, and immediately calls `session.configure(...)`. The
    factory therefore has to be able to hand back a fully-formed session at
    that instant, which is why the capture is completed BEFORE the factory is
    built rather than inside it.
    """
    def factory() -> win32.EtwPmcSession:
        return build_etw_pmc_session(
            capture, job_object_id=job_object_id,
            root_process_id=root_process_id,
            root_process_start_key=root_process_start_key)

    return factory


def make_live_etw_session_factory(consumer: "EtwPmcConsumer", *, job_object_id: str,
                                  ) -> Callable[[], win32.EtwPmcSession]:
    """The factory a REAL collection uses. ⛔ Never executed by any test.

    `collect()` calls this before `ResumeThread`, when the candidate has not
    run and no roster exists. It therefore hands back a session whose stream
    and rosters are EMPTY CONTAINERS, plus a `trace_finalizer` that fills them
    in place when `collect()` closes the trace window at the terminal barrier.
    The containers are mutated rather than replaced because `collect()` and
    `consume_cswitch()` both hold references to the objects handed over here.

    Nothing is defaulted at any point: if the finalizer cannot complete the
    roster, `assemble_member_lifetimes()` faults and the collection aborts. An
    empty roster never reaches a receipt.

    The root PID and start key are read from `session.root_identity()`, which
    `collect()` sets on the session it received from this factory, before it
    configures or resumes anything.
    """
    records: list[dict[str, Any]] = []
    threads: list[dict[str, Any]] = []
    members: list[dict[str, Any]] = []

    def finalize(session: win32.EtwPmcSession) -> None:
        loss = consumer.stop()
        # The root identity is read BEFORE the capture is taken, because the
        # capture is what gets scoped to that root's member tree: the provider
        # is machine-wide and everything else on the box lands in the same
        # stream. `collect()` set both fields before it resumed anything.
        root_process_id, root_start_key = session.root_identity()
        capture = consumer.capture(root_process_id=root_process_id,
                                   root_process_start_key=root_start_key)
        capture.loss = loss
        require_available_evidence(capability_facts=capture.capability_facts,
                                   loss=loss)
        session.events_lost = int(loss.events_lost)
        session.log_buffers_lost = int(loss.log_buffers_lost)
        session.realtime_buffers_lost = int(loss.realtime_buffers_lost)
        ordered, reordered = order_records_per_processor(capture.cswitch_records)
        capture.reordered_record_count = reordered
        members[:] = assemble_member_lifetimes(
            capture.process_events, job_object_id=job_object_id,
            root_process_id=root_process_id,
            root_process_start_key=root_start_key)
        threads[:] = assemble_thread_lifetimes(capture.thread_events, members)
        # The CSwitch stream is machine-wide like the lifetime stream, so it is
        # scoped to the member thread roster HERE — after that roster exists and
        # after the per-processor ordering the delta rule needs. Foreign
        # switches stay as per-processor baselines only; see
        # `scope_cswitch_records_to_members()`. The foreign THREAD events the
        # capture carries are what lets a host thread that recycled a member
        # TID be excluded instead of aborting the whole collection.
        scope = scope_cswitch_records_to_members(
            ordered, threads, capture.foreign_thread_events)
        capture.provenance.update(record_cswitch_scope_provenance(scope))
        records[:] = scope.records
        session.first_member_baselines = scope.first_member_baselines
        session.capability_facts = dict(capture.capability_facts)

    def factory() -> win32.EtwPmcSession:
        return win32.EtwPmcSession(
            session_handle=int(consumer.session_handle),
            capability=capability_evidence_record(source_id=consumer.source_id),
            attachment=event_attachment_record(),
            observations=[],
            thread_lifetimes=threads,
            record_stream=lambda: list(records),
            member_lifetimes=members,
            event_id_blob=classic_event_id_blob(),
            capability_facts=consumer.granted_capability_facts(),
            trace_finalizer=finalize)

    return factory


# ==========================================================================
# OS layer — NEVER executed by any test, verifier or import in this repository
# ==========================================================================


@dataclass(frozen=True)
class _EtwWin32:
    advapi32: Any
    kernel32: Any


def _etw_win32() -> _EtwWin32:
    """Bind the ETW entry points. Import-safe: nothing binds at module import.

    `TraceSetInformation`, `StartTraceW`, `ControlTraceW`, `OpenTraceW`,
    `ProcessTrace`, `CloseTrace` and `EnableTraceEx2` are documented as
    Advapi32 exports (forwarded to Sechost on Windows 8.1+), which is the same
    binding `mbcx01_build_win32._win32()` already uses for TraceSetInformation.
    """
    if os.name != "nt":
        raise EtwConsumerFault("WINDOWS_HOST_REQUIRED")
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    advapi32.StartTraceW.argtypes = [
        ctypes.POINTER(ctypes.c_ulonglong), wintypes.LPCWSTR, wintypes.LPVOID]
    advapi32.StartTraceW.restype = ctypes.c_ulong
    advapi32.ControlTraceW.argtypes = [
        ctypes.c_ulonglong, wintypes.LPCWSTR, wintypes.LPVOID, ctypes.c_ulong]
    advapi32.ControlTraceW.restype = ctypes.c_ulong
    advapi32.OpenTraceW.argtypes = [ctypes.POINTER(EVENT_TRACE_LOGFILEW)]
    advapi32.OpenTraceW.restype = ctypes.c_ulonglong
    advapi32.ProcessTrace.argtypes = [
        ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_ulong,
        wintypes.LPVOID, wintypes.LPVOID]
    advapi32.ProcessTrace.restype = ctypes.c_ulong
    advapi32.CloseTrace.argtypes = [ctypes.c_ulonglong]
    advapi32.CloseTrace.restype = ctypes.c_ulong
    advapi32.TraceSetInformation.argtypes = [
        ctypes.c_ulonglong, ctypes.c_int, wintypes.LPVOID, ctypes.c_ulong]
    advapi32.TraceSetInformation.restype = ctypes.c_ulong
    advapi32.TraceQueryInformation.argtypes = [
        ctypes.c_ulonglong, ctypes.c_int, wintypes.LPVOID, ctypes.c_ulong,
        ctypes.POINTER(ctypes.c_ulong)]
    advapi32.TraceQueryInformation.restype = ctypes.c_ulong
    advapi32.EnableTraceEx2.argtypes = [
        ctypes.c_ulonglong, ctypes.POINTER(GUID), ctypes.c_ulong, ctypes.c_ubyte,
        ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulong,
        ctypes.POINTER(ENABLE_TRACE_PARAMETERS)]
    advapi32.EnableTraceEx2.restype = ctypes.c_ulong
    # The per-processor PMC ownership sweep needs the processor population.
    kernel32.GetActiveProcessorCount.argtypes = [ctypes.c_ushort]
    kernel32.GetActiveProcessorCount.restype = ctypes.c_ulong
    return _EtwWin32(advapi32=advapi32, kernel32=kernel32)


def _check_trace(status: int, api: str) -> None:
    """Every trace return is checked; a failure is a fault, never a value."""
    if int(status) != ERROR_SUCCESS:
        raise EtwConsumerFault(f"{api}:WIN32_ERROR={int(status)}")


def _new_properties(*, log_file_mode: int, enable_flags: int) -> EVENT_TRACE_PROPERTIES_BUFFER:
    """One zeroed properties block with the documented offsets already set.

    "Be sure to initialize the memory for this structure to zero before setting
    any members" — EVENT_TRACE_PROPERTIES Remarks. ctypes zero-initialises, and
    the offsets are taken with `offsetof`-equivalents so a layout drift cannot
    silently point ETW at the wrong bytes.
    """
    block = EVENT_TRACE_PROPERTIES_BUFFER()
    block.Props.Wnode.BufferSize = ctypes.sizeof(EVENT_TRACE_PROPERTIES_BUFFER)
    block.Props.Wnode.Flags = WNODE_FLAG_TRACED_GUID
    block.Props.Wnode.ClientContext = WNODE_CLIENT_CONTEXT_QPC
    block.Props.BufferSize = SESSION_BUFFER_SIZE_KB
    block.Props.MinimumBuffers = SESSION_MINIMUM_BUFFERS
    block.Props.MaximumBuffers = SESSION_MAXIMUM_BUFFERS
    block.Props.FlushTimer = SESSION_FLUSH_TIMER_SECONDS
    block.Props.LogFileMode = log_file_mode
    block.Props.EnableFlags = enable_flags
    block.Props.LoggerNameOffset = EVENT_TRACE_PROPERTIES_BUFFER.LoggerName.offset
    block.Props.LogFileNameOffset = EVENT_TRACE_PROPERTIES_BUFFER.LogFileName.offset
    return block


def _enable_flags_update_properties(enable_flags: int) -> EVENT_TRACE_PROPERTIES_BUFFER:
    """The properties block for `ControlTraceW(EVENT_TRACE_CONTROL_UPDATE)`.

    UPDATE reads members the other control codes ignore, so two of them are set
    DIFFERENTLY here and each difference is a quoted requirement, not a taste.
    ControlTraceW, *Properties*, on what UPDATE may change:

      "EnableFlags: Set this member to 0 to disable all system providers. Set
       this to a non-zero value to specify the system providers that you want to
       enable or keep enabled. This may be non-zero only for system loggers."

    — which is why the caller passes the WHOLE set it wants live, not just the
    flag being added: anything omitted is not "left alone", it is disabled.

      "LogFileMode: Set this member if you want to turn EVENT_TRACE_REAL_TIME_MODE
       on and off. To turn real time consuming off, set this member to 0. To turn
       real time consuming on ..., set this member to EVENT_TRACE_REAL_TIME_MODE
       and it will be OR'd with the current modes."

    — so `log_file_mode=0`, which every other control call in this module uses,
    would TURN REAL-TIME DELIVERY OFF. It is set to `EVENT_TRACE_REAL_TIME_MODE`,
    which the page says is OR'd with the current modes and therefore changes
    nothing.

      "LogFileNameOffset: Set this member if you want to switch to another log
       file... If this member is 0, the file name is not updated. If the offset is
       not zero and you do not change the log file name, the function returns an
       error."

    — this session has no log file and is not changing one, so the offset
    `_new_properties()` sets for StartTraceW/STOP/QUERY is zeroed here. Leaving it
    would make the call FAIL, which on the one elevated session means no CSwitch
    stream at all.
    """
    block = _new_properties(log_file_mode=EVENT_TRACE_REAL_TIME_MODE,
                            enable_flags=enable_flags)
    block.Props.LogFileNameOffset = 0
    return block


class EtwPmcConsumer:
    """Create, configure, consume and tear down ONE strict PMC session.

    ⛔ NEVER EXECUTED BY ANY TEST, VERIFIER OR IMPORT IN THIS REPOSITORY.
    `start()` is reached only from the owner-authorized smoke runbook step; the
    BUILD suite exercises the pure layer above and the static ABI check, and
    nothing else. Kernel PMC requires an ELEVATED session.

    Lifecycle, in the order the evidence requires:

      start()   StartTraceW(real-time, system logger; PROCESS|THREAD, NO CSWITCH)
                -> TraceSetInformation(TracePmcCounterListInfo)  [pin the source]
                -> TraceSetInformation(TracePmcEventListInfo)    [attach to CSwitch]
                -> ControlTraceW(UPDATE, +EVENT_TRACE_FLAG_CSWITCH) [switches ON]
                -> EnableTraceEx2(Microsoft-Windows-Kernel-Process)
                -> OpenTraceW + ProcessTrace on a consumer thread

    Every step that can GENERATE a record needing a counter comes after the two
    TraceSetInformation calls; `SESSION_ENABLE_FLAGS_AT_START` enumerates that
    set and says why PROCESS and THREAD do not have to move.
      stop()    CloseTrace -> join -> ControlTraceW(QUERY) -> ControlTraceW(STOP)

    `stop()` runs from a `finally` in `run()` so the session is torn down even
    when configuration faults, which is the runbook's cleanup obligation.
    """

    def __init__(self, *, session_name: str = SESSION_NAME) -> None:
        self.session_name = session_name
        self._win32: _EtwWin32 | None = None
        self._session_handle = ctypes.c_ulonglong(0)
        self._trace_handle = ctypes.c_ulonglong(INVALID_PROCESSTRACE_HANDLE)
        self._thread: threading.Thread | None = None
        self._callback = None
        self._cswitch_records: list[dict[str, Any]] = []
        self._process_events: list[dict[str, Any]] = []
        self._thread_events: list[dict[str, Any]] = []
        self._callback_faults: list[str] = []
        self._source_id = -1
        self._capability_facts: dict[str, Any] | None = None
        self._started = False
        #: Set by `configure_pmc()`, which `start()` calls BEFORE the consumer
        #: opens (codex-CLI r7 P1). It makes the public method idempotent, so a
        #: caller that still configures after `start()` cannot re-issue the two
        #: TraceSetInformation calls against a running pump.
        self._pmc_configured = False
        #: Teardown evidence. `_loss` stays None until the counters have been
        #: read WHILE THE SESSION WAS ALIVE, `_drain_faults` records every
        #: reason the drain was not proven complete, and `_session_stopped`
        #: makes any later loss query refuse instead of reading a dead session.
        self._loss: LossCounters | None = None
        self._drain_faults: list[str] = []
        self._session_stopped = False
        self._recorded_session_handle = 0

    # -- what the live factory reads at factory time ------------------------

    @property
    def session_handle(self) -> int:
        return int(self._session_handle.value)

    @property
    def source_id(self) -> int:
        if self._source_id < 0:
            raise EtwConsumerFault("ETW_PMC_SOURCE_NOT_RESOLVED")
        return int(self._source_id)

    def granted_capability_facts(self) -> dict[str, Any]:
        if self._capability_facts is None:
            raise EtwConsumerFault("ETW_CAPABILITY_NOT_QUERIED")
        return dict(self._capability_facts)

    # -- session lifetime ---------------------------------------------------

    def start(self) -> None:
        """Start the session, pin the counter, attach it to CSwitch, consume."""
        verify_etw_struct_layout()
        self._win32 = _etw_win32()
        self._stop_orphan_session()
        block = _new_properties(
            log_file_mode=(EVENT_TRACE_REAL_TIME_MODE
                           | EVENT_TRACE_SYSTEM_LOGGER_MODE
                           | EVENT_TRACE_INDEPENDENT_SESSION_MODE),
            # NO `EVENT_TRACE_FLAG_CSWITCH` HERE (codex-CLI r8 P1). The flag rides
            # this very call, so a session started with it is producing context
            # switches from the moment StartTraceW returns — before any counter
            # exists to attach to them. See `SESSION_ENABLE_FLAGS_AT_START`.
            enable_flags=SESSION_ENABLE_FLAGS_AT_START)
        # Wnode.Guid stays GUID_NULL: StartTraceW's Remarks say "In most cases,
        # you will set Properties.Wnode.Guid to all-zero (i.e. GUID_NULL) to
        # allow the ETW system to generate a new GUID for the session", and the
        # SystemTraceProvider page requires that a private-named system logger
        # NOT use SystemTraceControlGuid.
        status = self._win32.advapi32.StartTraceW(
            ctypes.byref(self._session_handle), self.session_name, ctypes.byref(block))
        if int(status) == ERROR_ACCESS_DENIED:
            raise EtwConsumerFault(
                "StartTraceW:ELEVATION_REQUIRED - kernel PMC needs an elevated "
                "session (smoke runbook section 3 step 2)")
        if int(status) == ERROR_NO_SYSTEM_RESOURCES:
            raise EtwConsumerFault(
                "StartTraceW:SYSTEM_LOGGER_SLOTS_EXHAUSTED - at most 8 system "
                "loggers may be active")
        _check_trace(status, "StartTraceW")
        self._started = True
        self._recorded_session_handle = int(self._session_handle.value)
        self._source_id = self._resolve_profile_source_id(win32.PMC_SOURCE_NAME)
        self._capability_facts = self._query_capability_facts(self._source_id)
        # THE COUNTER IS ATTACHED BEFORE ANYTHING CAN GENERATE A CSWITCH
        # (codex-CLI r7 P1, COMPLETED by r8 P1). r7 moved `configure_pmc()` ahead
        # of the CONSUMER, because `mbcx01_smoke_cell.execute()` used to call it
        # only after `start()` had RETURNED and every switch delivered in that
        # window carried no PMC extended-data item — `_on_event_record` records
        # those as `ETW_PMC_EXTENDED_DATA_ABSENT` (correctly: an unattributable
        # switch is not evidence) and `capture()` then refuses the WHOLE run.
        #
        # But the pump was never the earliest door. `EVENT_TRACE_FLAG_CSWITCH`
        # rides `StartTraceW`, so switches were already being BUFFERED into the
        # session before this line — same fault, same refused run, one call
        # earlier. The flag is now off at the start and turned on HERE, after the
        # attach; `SESSION_ENABLE_FLAGS_AT_START` enumerates the whole set of
        # points at which generation can begin and states why PROCESS and THREAD
        # need not move.
        self.configure_pmc()
        self._enable_cswitch_flag()
        self._enable_process_provider()
        self._open_and_consume()

    def stop(self) -> LossCounters:
        """Tear down, PROVE the drain, and return the pre-stop loss counters.

        Every step here is evidence, so every step is checked:

        - `CloseTrace`'s return is READ. Only ERROR_SUCCESS and the documented
          ERROR_CTX_CLOSE_PENDING ("the call was successful; ProcessTrace will
          stop after processing the events already in its buffers") mean the
          pump was told to stop. Anything else means it was not.
        - the join RESULT is read. A pump that is still alive after the wait is
          still appending records, so the capture is a snapshot of a MOVING
          stream and the loss counters do not describe it.
        - the loss counters are read HERE, while the session is still alive,
          and carried. `capture()` never re-reads them; after the STOP below
          the session no longer exists and a query against it is refused.

        NO FAULT ANYWHERE ABOVE SKIPS THE TEARDOWN. The loss query runs in a
        `try` whose `finally` calls `_stop_session_logger()`, so a session that
        started is stopped even when the counters are unreadable — leaving one
        of the box's eight system logger slots occupied would block the next run
        and would not make the loss any more known. The unknown-loss fault is
        preserved exactly: it is raised after the teardown as the PRIMARY error,
        with a teardown failure appended after `SECONDARY` rather than replacing
        it. The same holds for an unproven drain, which is raised last, and
        `capture()` refuses on the same records even if a raise here is
        swallowed.

        Safe to call twice, and deliberately does NOT re-raise on the second
        call: `mbcx01_smoke_cell` calls `stop()` from a `finally` after
        `collect()` has already called it through the trace finalizer, and a
        second raise there would MASK the first fault. The verdict is not lost
        — `capture()` still refuses on `_drain_faults`.
        """
        if self._win32 is None:
            return LossCounters()
        if self._session_stopped:
            return self._loss if self._loss is not None else LossCounters()
        if int(self._trace_handle.value) != INVALID_PROCESSTRACE_HANDLE:
            status = int(self._win32.advapi32.CloseTrace(self._trace_handle))
            self._trace_handle = ctypes.c_ulonglong(INVALID_PROCESSTRACE_HANDLE)
            if status not in (ERROR_SUCCESS, ERROR_CTX_CLOSE_PENDING):
                self._drain_faults.append(f"CloseTrace:WIN32_ERROR={status}")
        if self._thread is not None:
            self._thread.join(timeout=CONSUMER_JOIN_TIMEOUT_SECONDS)
            if self._thread.is_alive():
                self._drain_faults.append(
                    "ProcessTrace pump still alive after a "
                    f"{CONSUMER_JOIN_TIMEOUT_SECONDS}s join")
        loss: LossCounters | None = None
        loss_fault: str | None = None
        try:
            loss = self._query_loss()
        except EtwConsumerFault as fault:
            loss_fault = str(fault)
        finally:
            teardown_fault = self._stop_session_logger()
        if loss is not None:
            self._loss = loss
        # The handle is kept as EVIDENCE (which session produced this capture)
        # and invalidated as a HANDLE, so no later call can use a dead session.
        self._recorded_session_handle = (int(self._session_handle.value)
                                         or self._recorded_session_handle)
        self._session_handle = ctypes.c_ulonglong(0)
        self._session_stopped = True
        if loss_fault is not None:
            raise EtwConsumerFault(
                loss_fault if teardown_fault is None
                else f"{loss_fault}; SECONDARY {teardown_fault}")
        if teardown_fault is not None:
            raise EtwConsumerFault(teardown_fault)
        if self._drain_faults:
            raise EtwConsumerFault(
                "ETW_TRACE_DRAIN_INCOMPLETE:" + ";".join(self._drain_faults))
        return loss

    def _stop_session_logger(self) -> str | None:
        """`ControlTraceW(STOP)`, returning its fault TEXT instead of raising.

        Called from `stop()`'s `finally`, so it runs whether or not the loss
        query succeeded: an unreadable loss counter is a reason to refuse the
        evidence, never a reason to leave a system logger running — the box has
        only eight of those slots and an orphan blocks the next run.

        It returns text rather than raising because it runs while another fault
        may already be in flight. `stop()` raises the loss-query fault as the
        PRIMARY error and appends this one after `SECONDARY`, so a teardown
        failure is never silent and never masks the reason the evidence is
        unavailable.

        `_started` is cleared once the stop has been ATTEMPTED, successfully or
        not: the second `stop()` that `mbcx01_smoke_cell` makes from its
        `finally` must not re-issue a control call against a handle this one has
        already invalidated. ERROR_MORE_DATA on STOP is documented as "ETW will
        have already stopped the session" and ERROR_WMI_INSTANCE_NOT_FOUND means
        it is already gone; neither is a teardown failure.
        """
        if not self._started:
            return None
        block = _new_properties(log_file_mode=0, enable_flags=0)
        status = self._win32.advapi32.ControlTraceW(
            self._session_handle, self.session_name, ctypes.byref(block),
            EVENT_TRACE_CONTROL_STOP)
        self._started = False
        if int(status) not in (ERROR_SUCCESS, ERROR_MORE_DATA,
                               ERROR_WMI_INSTANCE_NOT_FOUND):
            return ("ETW_SESSION_TEARDOWN_FAULT:ControlTraceW(STOP):"
                    f"WIN32_ERROR={int(status)}")
        return None

    def _stop_orphan_session(self) -> None:
        """Clean up an orphan of OUR OWN session name before starting.

        StartTraceW's own guidance: "If your component's session is already
        running when your component starts, your component should clean up the
        orphaned session rather than creating a second session." Scoped to this
        exact name so it can never stop somebody else's logger.
        """
        block = _new_properties(log_file_mode=0, enable_flags=0)
        status = self._win32.advapi32.ControlTraceW(
            ctypes.c_ulonglong(0), self.session_name, ctypes.byref(block),
            EVENT_TRACE_CONTROL_STOP)
        if int(status) not in (ERROR_SUCCESS, ERROR_MORE_DATA,
                               ERROR_WMI_INSTANCE_NOT_FOUND):
            raise EtwConsumerFault(
                f"ControlTraceW(STOP orphan):WIN32_ERROR={int(status)}")

    # -- capability ---------------------------------------------------------

    def _resolve_profile_source_id(self, name: str) -> int:
        """Look the pinned source up in TraceProfileSourceListInfo.

        The extended-data page states the valid Source values are "found by
        calling TraceQueryInformation with TraceProfileSourceListInfo", so the
        id is LOOKED UP and never guessed. An absent source is UNAVAILABLE.

        The answer is "An array of PROFILE_SOURCE_INFO structs" (evntrace.h
        lines 2137-2144) chained by `NextEntryOffset`, and this walk reads that
        chain the way the header defines it:

        - the name is decoded as WCHAR CODE UNITS by
          `_profile_source_description()`. Splitting the raw bytes on
          `b"\\x00\\x00"` matched the UNALIGNED pair spanning the last ASCII
          character and its terminator, so the normal name `InstructionRetired`
          parsed as `InstructionRetire` and a source that WAS present was
          reported `ETW_PMC_SOURCE_UNAVAILABLE`;
        - `NextEntryOffset == 0` ENDS the list, so the last entry's description
          runs to the end of the returned buffer. `offset + next or len(raw)`
          evaluated to `offset` for a final entry at a nonzero offset, i.e. an
          EMPTY name, which is why a chained final entry could never match
          either;
        - a `NextEntryOffset` that does not advance past the fixed prefix, or a
          buffer that ends mid-prefix, is `ETW_PMC_SOURCE_LIST_MALFORMED` — a
          named refusal instead of a re-read of the same bytes forever.
        """
        size = ctypes.c_ulong(0)
        self._win32.advapi32.TraceQueryInformation(
            ctypes.c_ulonglong(0), TraceProfileSourceListInfo, None, 0,
            ctypes.byref(size))
        if int(size.value) == 0:
            raise EtwConsumerFault("TraceProfileSourceListInfo:EMPTY_SOURCE_LIST")
        buffer = (ctypes.c_ubyte * int(size.value))()
        _check_trace(self._win32.advapi32.TraceQueryInformation(
            ctypes.c_ulonglong(0), TraceProfileSourceListInfo, ctypes.byref(buffer),
            size, ctypes.byref(size)), "TraceQueryInformation(ProfileSourceList)")
        raw = bytes(bytearray(buffer))
        prefix_size = ctypes.sizeof(PROFILE_SOURCE_INFO)
        offset = 0
        wanted = name.strip().upper()
        while offset < len(raw):
            if offset + prefix_size > len(raw):
                raise EtwConsumerFault(
                    f"ETW_PMC_SOURCE_LIST_MALFORMED:truncated_entry@{offset}")
            entry = PROFILE_SOURCE_INFO.from_buffer_copy(
                raw[offset:offset + prefix_size])
            next_offset = int(entry.NextEntryOffset)
            if next_offset == 0:
                end = len(raw)
            elif next_offset < prefix_size:
                raise EtwConsumerFault(
                    f"ETW_PMC_SOURCE_LIST_MALFORMED:NextEntryOffset={next_offset}")
            else:
                end = min(offset + next_offset, len(raw))
            description = _profile_source_description(
                raw[offset + prefix_size:end])
            if description.strip().upper() == wanted:
                return int(entry.Source)
            if next_offset == 0:
                break
            offset += next_offset
        raise EtwConsumerFault(f"ETW_PMC_SOURCE_UNAVAILABLE:{name}")

    def _query_capability_facts(self, source_id: int) -> dict[str, Any]:
        """Record what the platform GRANTED, as values, never as prose."""
        maximum = ctypes.c_ulong(0)
        size = ctypes.c_ulong(ctypes.sizeof(maximum))
        status = self._win32.advapi32.TraceQueryInformation(
            ctypes.c_ulonglong(0), TraceMaxPmcCounterQuery, ctypes.byref(maximum),
            size, ctypes.byref(size))
        _check_trace(status, "TraceQueryInformation(MaxPmcCounter)")
        # The ownership query's input buffer is sized FROM this answer, which
        # is why the maximum is read first (evntrace.h lines 2350-2354).
        owners = self._count_counter_owners(int(maximum.value))
        return granted_capability_facts(
            pmc_source_available=True,
            max_pmc_counters=int(maximum.value),
            counter_owner_conflict_count=owners,
            # Multiplexing is inferred from the grant: this session pins ONE
            # counter, so if the platform can hold at least one counter and no
            # other owner holds it, no multiplexing is in play. A platform that
            # grants fewer counters than the pinned list is caught as
            # ETW_PMC_NO_COUNTERS_GRANTED, not silently multiplexed.
            multiplexing_detected=int(maximum.value) < len(PINNED_COUNTER_NAMES),
            attribution_complete=True,
            counter_width_bits=64,
            profile_source_name=win32.PMC_SOURCE_NAME,
            profile_source_id=int(source_id))

    def _count_counter_owners(self, max_counters: int) -> int:
        """How many processor PMC counters are held by somebody, box-wide.

        TracePmcCounterOwners "Queries ETW for a list of processor performance
        monitoring counters currently in use. This list may contain counters in
        use by facilities other than ETW." (TRACE_QUERY_INFO_CLASS page.) Any
        owner at all is a conflict for a strict single-counter attachment, so
        the COUNT is recorded and the availability rule refuses on > 0.

        THE QUERY IS PER-PROCESSOR AND TAKES AN INPUT BUFFER. evntrace.h lines
        2345-2361 state it verbatim: "Input Format:
        ETW_PMC_COUNTER_OWNERSHIP_STATUS with ProcessorNumber set to an
        appropriate processor index. The input buffer must be of size at least
        RTL_SIZEOF_THROUGH_FIELD(ETW_PMC_COUNTER_OWNERSHIP_STATUS,
        NumberOfCounters) + (sizeof(ETW_PMC_COUNTER_OWNER) *
        EtwMaxPmcCounters), where EtwMaxPmcCounters is the result of a
        TraceQueryInformation(TraceMaxPmcCounterQuery, ...) operation.  Output
        Format: ETW_PMC_COUNTER_OWNERSHIP_STATUS with CounterOwners filled
        out." So every processor is asked, each answer is DECODED, and the
        owner rows decide — not the presence of nonzero bytes.

        What that replaced, and why it mattered: this method used to size the
        buffer from a zero-length probe and return `1 if any(bytes(buffer))`.
        On a healthy host the answer contains `NumberOfCounters` (a count of
        rows, nonzero whenever the platform has any counters at all) next to
        rows that are all `EtwPmcOwnerFree`, so a machine whose every PMC was
        free was reported as a counter-owner conflict and its evidence refused
        as `ETW_PMC_COUNTER_OWNER_CONFLICT`.

        `max_counters` of zero means the platform grants no counters at all;
        there are no owner rows to ask about and the grant itself is what is
        wrong, so this returns 0 and `evaluate_evidence_availability()` names it
        `ETW_PMC_NO_COUNTERS_GRANTED`. A failed query is a FAULT, never a
        comfortable zero. See `PMC_OWNER_PROCESSOR_INDEX_UNCERTAINTY` for the
        one thing the header does not settle.
        """
        if int(max_counters) < 1:
            return 0
        header_size = ctypes.sizeof(ETW_PMC_COUNTER_OWNERSHIP_STATUS)
        buffer_size = (header_size
                       + ctypes.sizeof(ETW_PMC_COUNTER_OWNER) * int(max_counters))
        owned = 0
        for processor in range(self._active_processor_count()):
            buffer = (ctypes.c_ubyte * buffer_size)()
            request = ETW_PMC_COUNTER_OWNERSHIP_STATUS.from_buffer(buffer)
            request.ProcessorNumber = processor
            # The header names ProcessorNumber as the only input field. The
            # capacity is stated as well, because the header does not say
            # whether the kernel reads NumberOfCounters as capacity, and a zero
            # read as capacity would answer "no owners" for a busy counter —
            # the one wrong answer that could pass silently. The buffer really
            # does hold this many rows.
            request.NumberOfCounters = int(max_counters)
            size = ctypes.c_ulong(buffer_size)
            status = self._win32.advapi32.TraceQueryInformation(
                ctypes.c_ulonglong(0), TracePmcCounterOwners,
                ctypes.byref(buffer), size, ctypes.byref(size))
            _check_trace(int(status),
                         f"TraceQueryInformation(PmcCounterOwners,cpu={processor})")
            returned = min(int(size.value) or buffer_size, buffer_size)
            rows = pmc_counter_owner_rows(bytes(bytearray(buffer))[:returned],
                                          max_counters=int(max_counters))
            owned += count_owned_pmc_counters(rows)
        return owned

    def _active_processor_count(self) -> int:
        """How many logical processors the ownership sweep has to ask about.

        `GetActiveProcessorCount(ALL_PROCESSOR_GROUPS)` returns "the number of
        active processors in all processor groups" (kernel32 / Learn), which is
        the population the per-processor ownership query has to cover. A zero
        or failing answer is a FAULT: sweeping zero processors would report
        "nobody owns a counter" without having asked anyone.
        """
        count = int(self._win32.kernel32.GetActiveProcessorCount(
            ALL_PROCESSOR_GROUPS))
        if count < 1:
            raise EtwConsumerFault(
                "GetActiveProcessorCount(ALL_PROCESSOR_GROUPS):WIN32_ERROR="
                f"{ctypes.get_last_error()}")
        return count

    # -- configuration ------------------------------------------------------

    def _enable_cswitch_flag(self) -> None:
        """Turn the CSwitch system provider ON, AFTER the counter is attached.

        THE DOCUMENTED MECHANISM, and it is documented for exactly this session
        shape. ControlTraceW, *Properties*, on EVENT_TRACE_CONTROL_UPDATE:

          "EnableFlags: Set this member to 0 to disable all system providers.
           Set this to a non-zero value to specify the system providers that you
           want to enable or keep enabled. This may be non-zero only for system
           loggers."

        This session IS a system logger — `start()` passes
        `EVENT_TRACE_SYSTEM_LOGGER_MODE | EVENT_TRACE_INDEPENDENT_SESSION_MODE` —
        so the sentence applies to it and to nothing else in this module.

        `SESSION_ENABLE_FLAGS_AFTER_PMC` is the WHOLE set, not the delta, because
        the page says what a non-zero value means: the providers to "enable or
        keep enabled". Passing only CSWITCH here would DISABLE the process and
        thread flags the start call turned on, which the lifetime cross-check
        depends on. `_enable_flags_update_properties()` carries the two other
        UPDATE-specific requirements (real-time not switched off, log file name
        offset zeroed) with the quotations that require them.

        The return is CHECKED like every other trace return in this module: a
        failure here means the session collects no context switches at all, which
        is a fault to be seen immediately rather than an empty capture to be
        puzzled over after the elevated session is gone.

        ⚠ UNVERIFIED_UNTIL_ELEVATED_RUN, and stated rather than implied: no test,
        verifier or import in this repository executes this call, so what is
        proven here is the ORDER and the arguments, not the OS's answer. If the
        platform declines a flag update on an independent system logger, the
        operator gets `ControlTraceW(UPDATE:CSWITCH):WIN32_ERROR=<n>` at start,
        before any measurement is taken and before the candidate is resumed.
        """
        block = _enable_flags_update_properties(SESSION_ENABLE_FLAGS_AFTER_PMC)
        status = self._win32.advapi32.ControlTraceW(
            self._session_handle, self.session_name, ctypes.byref(block),
            EVENT_TRACE_CONTROL_UPDATE)
        _check_trace(status, "ControlTraceW(UPDATE:CSWITCH)")

    def _enable_process_provider(self) -> None:
        """Enable Microsoft-Windows-Kernel-Process on THIS session.

        See `SAME_SESSION_UNCERTAINTY`. The lifetime stream must come from the
        same session as the PMC stream; if the platform refuses that, the
        refusal is a FAULT and the operator gets it verbatim, because falling
        back to a second session would silently void the same-session claim
        that the membership evidence rests on.

        THIS ENABLE IS MACHINE-WIDE, AND DELIBERATELY SO. Every process and
        thread event on the box arrives on this session, not just the measured
        Job's. It is not narrowed at the provider because at this instant the
        Job's population does not exist yet: `collect()` enables the session
        before it resumes the root, so the only member that exists is the
        suspended root and no filter written now could name the descendants
        that appear later. The scope is applied ONCE, downstream and by name,
        in `partition_job_member_events()`, which keeps the root's member tree
        and puts everything else out of population BEFORE any assembly. Without
        that step a non-idle host either aborts the capture
        (`ETW_PROCESS_LIFETIME_UNMATCHED_STOP`, `ETW_THREAD_START_KEY_UNBINDABLE`
        on a stranger's events) or signs a roster containing processes the Job
        never held. Witness bw66.
        """
        provider = GUID.from_le_bytes(KERNEL_PROCESS_PROVIDER_GUID_BYTES)
        parameters = ENABLE_TRACE_PARAMETERS()
        parameters.Version = 2
        parameters.EnableProperty = EVENT_ENABLE_PROPERTY_PROCESS_START_KEY
        status = self._win32.advapi32.EnableTraceEx2(
            self._session_handle, ctypes.byref(provider),
            EVENT_CONTROL_CODE_ENABLE_PROVIDER, TRACE_LEVEL_VERBOSE,
            KERNEL_PROCESS_KEYWORD_PROCESS | KERNEL_PROCESS_KEYWORD_THREAD,
            0, 0, ctypes.byref(parameters))
        if int(status) != ERROR_SUCCESS:
            raise EtwConsumerFault(
                "EnableTraceEx2(Microsoft-Windows-Kernel-Process):"
                f"WIN32_ERROR={int(status)} - {SAME_SESSION_UNCERTAINTY}")

    def configure_pmc(self) -> None:
        """The two documented calls, in the documented order.

        Order is not cosmetic: `TracePmcCounterListInfo` "Configures the
        session with a list of profiling sources that will be collected when
        events configured by TracePmcEventListInfo are logged", and
        `TracePmcEventListInfo` "Configures the session with a list of system
        events for which performance monitoring counters configured by
        TracePmcCounterListInfo will be collected". The counter list is pinned
        FIRST, then the event that samples it.

        This mirrors `EtwPmcSession.configure()`, which `collect()` calls; the
        method here exists so the consumer can also configure a session it owns
        outright without going through a collection.

        CALLED BY `start()`, AND IDEMPOTENT (codex-CLI r7 P1). The attachment
        moved INTO `start()`, before the consumer opens, because a counter
        attached after the pump leaves a window in which CSwitch records arrive
        without PMC data and refuse the whole run. This stays PUBLIC and a
        second call is a NO-OP rather than a re-issue against a live pump, so
        the runbook's old `start(); configure_pmc()` sequence still does exactly
        the right thing.

        AND IT NOW RUNS BEFORE THE SWITCHES EXIST AT ALL (codex-CLI r8 P1).
        Being ahead of the pump was not enough: `EVENT_TRACE_FLAG_CSWITCH` rides
        `StartTraceW`, so the session was already buffering PMC-less switches
        before this method was reached. `start()` no longer passes that flag and
        calls `_enable_cswitch_flag()` immediately after this returns.
        """
        if self._pmc_configured:
            return
        sources = (ctypes.c_ulong * len(PINNED_COUNTER_NAMES))(self._source_id)
        _check_trace(self._win32.advapi32.TraceSetInformation(
            self._session_handle, TracePmcCounterListInfo, ctypes.byref(sources),
            ctypes.sizeof(sources)), "TraceSetInformation(TracePmcCounterListInfo)")
        blob = classic_event_id_blob()
        events = (ctypes.c_ubyte * len(blob))(*blob)
        _check_trace(self._win32.advapi32.TraceSetInformation(
            self._session_handle, TracePmcEventListInfo, ctypes.byref(events),
            ctypes.sizeof(events)), "TraceSetInformation(TracePmcEventListInfo)")
        self._pmc_configured = True

    # -- consumption --------------------------------------------------------

    def _open_and_consume(self) -> None:
        """OpenTraceW + ProcessTrace with an EventRecordCallback, on its own thread.

        `ProcessTrace` blocks until the trace handle is closed, so it cannot
        run on the thread that also has to resume the candidate and wait at the
        terminal barrier. The callback appends to plain lists and the lists are
        only READ after `stop()` has joined the thread, so no lock is needed
        and no partially-consumed stream is ever assembled.
        """
        logfile = EVENT_TRACE_LOGFILEW()
        logfile.LoggerName = self.session_name
        logfile.LogFileName = None
        logfile.ProcessTraceMode = (PROCESS_TRACE_MODE_REAL_TIME
                                    | PROCESS_TRACE_MODE_EVENT_RECORD
                                    | PROCESS_TRACE_MODE_RAW_TIMESTAMP)
        # Keep a reference on self: a ctypes callback that is garbage collected
        # while ETW still holds it is a use-after-free, not a Python error.
        self._callback = EVENT_RECORD_CALLBACK(self._on_event_record)
        logfile.EventRecordCallback = ctypes.cast(self._callback, ctypes.c_void_p)
        handle = self._win32.advapi32.OpenTraceW(ctypes.byref(logfile))
        if int(handle) == INVALID_PROCESSTRACE_HANDLE:
            raise EtwConsumerFault(
                f"OpenTraceW:WIN32_ERROR={ctypes.get_last_error()}")
        self._trace_handle = ctypes.c_ulonglong(int(handle))

        def pump() -> None:
            handles = (ctypes.c_ulonglong * 1)(int(handle))
            status = self._win32.advapi32.ProcessTrace(handles, 1, None, None)
            if int(status) != ERROR_SUCCESS:
                self._callback_faults.append(
                    f"ProcessTrace:WIN32_ERROR={int(status)}")

        self._thread = threading.Thread(target=pump, name="mbcx01-etw-consumer",
                                        daemon=True)
        self._thread.start()

    def _on_event_record(self, record_pointer: Any) -> None:
        """The EventRecordCallback. Records raw facts; decides nothing.

        A callback that raises into ETW is undefined behaviour, so a decoding
        problem is APPENDED to `_callback_faults` and re-raised on the calling
        thread by `capture()`. It is never swallowed.
        """
        try:
            record = record_pointer.contents
            header = record.EventHeader
            provider = bytes(bytearray(header.ProviderId))
            timestamp = int(header.TimeStamp)
            if provider == KERNEL_PROCESS_PROVIDER_GUID_BYTES:
                self._decode_kernel_process_event(record, timestamp)
                return
            if not (int(header.Flags) & EVENT_HEADER_FLAG_CLASSIC_HEADER):
                return
            if provider != THREAD_GUID_BYTES:
                return
            if int(header.EventDescriptor.Opcode) != CSWITCH_EVENT_TYPE:
                return
            items = self._extended_data_items(record)
            counters = pmc_counters_from_extended_data(items)
            self._cswitch_records.append({
                "processor": int(record.BufferContext.ProcessorIndex),
                "qpc": timestamp,
                "old_thread_id": self._cswitch_old_thread_id(record),
                "instruction_retired": select_pinned_counter(
                    counters, PINNED_INSTRUCTION_RETIRED_INDEX)})
        except EtwConsumerFault as fault:  # pragma: no cover - physical only
            self._callback_faults.append(str(fault))
        except Exception as exc:  # pragma: no cover - physical only
            self._callback_faults.append(f"CALLBACK_FAULT:{exc!r}")

    def _extended_data_items(self, record: Any) -> list[tuple[int, bytes]]:
        """Copy every extended data item out of ETW's buffer while it is valid."""
        items: list[tuple[int, bytes]] = []
        if not (int(record.EventHeader.Flags) & EVENT_HEADER_FLAG_EXTENDED_INFO):
            return items
        for index in range(int(record.ExtendedDataCount)):
            item = record.ExtendedData[index]
            payload = ctypes.string_at(int(item.DataPtr), int(item.DataSize))
            items.append((int(item.ExtType), bytes(payload)))
        return items

    def _cswitch_old_thread_id(self, record: Any) -> int:
        """The OUTGOING thread — the one the delta is attributed to.

        VERIFIED at the primary source. learn.microsoft.com/en-us/windows/win32/etw/cswitch
        publishes the MOF verbatim:

            [EventType{36}, EventTypeName{"CSwitch"}]
            class CSwitch : Thread_V2
            {
              uint32 NewThreadId;     // WmiDataId(1)  -> payload offset 0
              uint32 OldThreadId;     // WmiDataId(2)  -> payload offset 4
              ...

        So `OldThreadId` is the SECOND uint32, at byte offset 4. It is read from
        the raw payload rather than through a decoded structure so that a
        manifest revision cannot silently reinterpret the field, and a payload
        too short to contain it is a fault rather than a zero thread id.
        """
        raw = ctypes.string_at(record.UserData, int(record.UserDataLength))
        if len(raw) < 8:
            raise EtwConsumerFault(f"ETW_CSWITCH_PAYLOAD_SHORT:{len(raw)}")
        return int(struct.unpack_from("<I", raw, 4)[0])

    def _decode_kernel_process_event(self, record: Any, timestamp: int) -> None:
        """Decode ProcessStart/ProcessStop/ThreadStart/ThreadStop payloads.

        THE PAYLOAD BEGINS WITH A UINT32 `ProcessID`, NEVER WITH A START KEY,
        and the 64-bit `ProcessSequenceNumber` that names the incarnation exists
        only in the later versions of each event. Both facts are read out of
        this OS build's own provider manifest through TDH; the field-by-field
        table, the versions and the exact queries are at
        `KERNEL_PROCESS_PAYLOAD_LAYOUTS`.

        The EVENT VERSION therefore selects the layout. It is taken from
        `EventHeader.EventDescriptor.Version` and looked up, never assumed:

        - a version whose template this build read and which carries the
          sequence number is decoded at that template's offsets;
        - a version whose template this build read and which carries NO
          sequence number is `ETW_KERNEL_PROCESS_EVENT_VERSION_WITHOUT_START_KEY`;
        - any other version is `ETW_KERNEL_PROCESS_EVENT_VERSION_UNSUPPORTED`.

        The last two are faults, so a layout this build did not verify can never
        be decoded by guess — and a payload too short for the template it claims
        is `ETW_KERNEL_PROCESS_PAYLOAD_SHORT` rather than a truncated integer.

        THE THREAD EVENTS ARE GATED THE SAME WAY (2026-08-16, council r6). Both
        published ThreadStart/ThreadStop templates begin `ProcessID u32 @0,
        ThreadID u32 @4`, and `KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED` names
        exactly those two; a version outside that set is
        `ETW_KERNEL_THREAD_VERSION_UNVERIFIED` rather than eight bytes read at
        offsets nobody verified for it.
        """
        descriptor = record.EventHeader.EventDescriptor
        event_id = int(descriptor.Id)
        version = int(descriptor.Version)
        raw = ctypes.string_at(record.UserData, int(record.UserDataLength))
        if event_id in (KERNEL_PROCESS_EVENT_ID_PROCESS_START,
                        KERNEL_PROCESS_EVENT_ID_PROCESS_STOP):
            layout = KERNEL_PROCESS_PAYLOAD_LAYOUTS.get((event_id, version))
            if layout is None:
                if (event_id, version) in KERNEL_PROCESS_VERSIONS_WITHOUT_SEQUENCE_NUMBER:
                    raise EtwConsumerFault(
                        "ETW_KERNEL_PROCESS_EVENT_VERSION_WITHOUT_START_KEY:"
                        f"id={event_id},version={version}")
                raise EtwConsumerFault(
                    "ETW_KERNEL_PROCESS_EVENT_VERSION_UNSUPPORTED:"
                    f"id={event_id},version={version}")
            process_id_offset, sequence_offset = layout
            parent_layout = KERNEL_PROCESS_START_PARENT_LAYOUTS.get(
                (event_id, version))
            required = sequence_offset + 8
            if parent_layout is not None:
                required = max(required, parent_layout[1] + 8)
            if len(raw) < required:
                raise EtwConsumerFault(
                    f"ETW_KERNEL_PROCESS_PAYLOAD_SHORT:{len(raw)}<{required}"
                    f":id={event_id},version={version}")
            process_id = struct.unpack_from("<I", raw, process_id_offset)[0]
            start_key = struct.unpack_from("<Q", raw, sequence_offset)[0]
            kind = ("START" if event_id == KERNEL_PROCESS_EVENT_ID_PROCESS_START
                    else "STOP")
            event: dict[str, Any] = {"kind": kind, "process_id": int(process_id),
                                     "process_start_key": int(start_key),
                                     "qpc": timestamp}
            if kind == "START":
                # THE PARENT IS THE ONE THE PAYLOAD DECLARES (codex-CLI r7 P2).
                # `EventHeader.ProcessId` is the context the start was LOGGED
                # in, which for a brokered or explicit-parent creation is NOT
                # the parent; the template carries the authoritative tuple at
                # `KERNEL_PROCESS_START_PARENT_LAYOUTS`' offsets and that is
                # what membership is built from. The header pid is kept beside
                # it as DIAGNOSTIC evidence — it is the only record of which
                # process emitted the event, and a reader comparing the two can
                # see a brokered creation for what it is — but nothing decides
                # membership from it.
                #
                # Neither field is the finished evidence:
                # `assemble_member_lifetimes()` turns them into the frozen
                # parent tuple, forcing the measured ROOT's pair to
                # (None, None) — its creator is the collector, which is not a
                # member. A parent sequence number of 0 (a parent that started
                # before this trace window, so the provider has no incarnation
                # number for it) still RESOLVES by QPC containment there, the
                # way every parent key did before this decode existed.
                parent_id = None
                parent_key = None
                if parent_layout is not None:
                    parent_id = int(struct.unpack_from(
                        "<I", raw, parent_layout[0])[0])
                    parent_key = int(struct.unpack_from(
                        "<Q", raw, parent_layout[1])[0])
                event["parent_process_id"] = parent_id
                event["parent_process_start_key"] = parent_key
                event["event_header_process_id"] = int(
                    record.EventHeader.ProcessId)
            self._process_events.append(event)
        elif event_id in (KERNEL_PROCESS_EVENT_ID_THREAD_START,
                          KERNEL_PROCESS_EVENT_ID_THREAD_STOP):
            # The thread branch is version-gated for the same reason the
            # process branch is: "eight bytes long" is not evidence that the
            # first eight bytes are `ProcessID, ThreadID`. Only the two
            # templates this build actually read are decoded.
            if version not in KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED:
                raise EtwConsumerFault(
                    "ETW_KERNEL_THREAD_VERSION_UNVERIFIED:"
                    f"id={event_id},version={version}")
            if len(raw) < 8:
                raise EtwConsumerFault(f"ETW_KERNEL_THREAD_PAYLOAD_SHORT:{len(raw)}")
            process_id, thread_id = struct.unpack_from("<II", raw, 0)
            # NO start key here, and none is invented: the THREAD payload does
            # not carry one. It is bound in `capture()` by
            # `bind_thread_start_keys()` from the PROCESS events this same
            # consumer decoded, which is also where an unbindable thread
            # becomes a named fault. (This slot previously held a hard-coded
            # `"process_start_key": None`, which `assemble_thread_lifetimes()`
            # can never join — every live thread stream died at
            # `ETW_PROCESS_START_KEY_INVALID:None`, after the candidate had
            # already run. Witness bw49.)
            self._thread_events.append({
                "kind": ("START" if event_id == KERNEL_PROCESS_EVENT_ID_THREAD_START
                         else "STOP"),
                "thread_id": int(thread_id), "process_id": int(process_id),
                "qpc": timestamp})

    # -- results ------------------------------------------------------------

    def _query_loss(self) -> LossCounters:
        """Read EventsLost / LogBuffersLost / RealTimeBuffersLost back.

        ControlTraceW(EVENT_TRACE_CONTROL_QUERY) "Retrieves session properties
        and statistics", and the three counters are documented OUTPUT members
        of EVENT_TRACE_PROPERTIES. If the query itself fails the counters are
        UNKNOWN, and unknown loss is treated as loss: the fault propagates.

        This runs exactly ONCE per session, inside `stop()`, BEFORE
        ControlTraceW(STOP). After the stop there is no session to describe:
        the query would either fail or answer about something else, and either
        way the number would not be evidence about the trace that ran. So a
        post-stop query is refused by name rather than answered.
        """
        if self._session_stopped:
            raise EtwConsumerFault(
                "ETW_LOSS_QUERY_AFTER_SESSION_STOP: the loss counters are read "
                "once, in stop(), while the session is still alive; the "
                "counters that stop() carried are the only ones that describe "
                "the trace that ran")
        block = _new_properties(log_file_mode=0, enable_flags=0)
        status = self._win32.advapi32.ControlTraceW(
            self._session_handle, self.session_name, ctypes.byref(block),
            EVENT_TRACE_CONTROL_QUERY)
        if int(status) not in (ERROR_SUCCESS, ERROR_MORE_DATA):
            raise EtwConsumerFault(
                f"ControlTraceW(QUERY):WIN32_ERROR={int(status)} - loss counters "
                "unreadable, so loss is UNKNOWN and evidence is unavailable")
        return LossCounters(events_lost=int(block.Props.EventsLost),
                            log_buffers_lost=int(block.Props.LogBuffersLost),
                            realtime_buffers_lost=int(block.Props.RealTimeBuffersLost))

    def capture(self, *, root_process_id: int | None = None,
                root_process_start_key: str | None = None) -> CapturedTrace:
        """Everything the consumed trace yielded. Call AFTER `stop()`.

        "After `stop()`" is ENFORCED, not documented: a capture taken while the
        pump may still be running is a snapshot of a moving stream, and the
        loss counters that would describe it have not been read yet. The
        counters `stop()` read while the session was alive are carried here;
        they are never re-queried, because the session no longer exists.

        GIVE IT THE ROOT AND IT SCOPES. Microsoft-Windows-Kernel-Process is
        machine-wide, so `self._process_events` / `self._thread_events` hold the
        whole box. When a root identity is supplied — which the live factory
        always does, from `session.root_identity()` — the two raw streams are
        partitioned to that root's member tree by
        `partition_job_member_events()` BEFORE the thread keys are bound, and
        the counts of what was excluded travel in `provenance`. Without a root
        identity the raw streams are used exactly as before, which is what the
        witness suite exercises; a half-supplied identity is a fault rather
        than a partial scope.

        THE CSWITCH STREAM LEAVES HERE RAW, AND THAT IS THE CONTRACT. It is
        machine-wide too, but it cannot be scoped at this point: membership for
        a context switch is decided against the SIGNED THREAD ROSTER, and that
        roster does not exist until `assemble_thread_lifetimes()` has run over
        the scoped lifetime streams this method returns. Nor may it be sorted
        here — `order_records_per_processor()` has to see the arrival order to
        count how many records had to move. The scope is applied once, by
        `scope_cswitch_records_to_members()`, at the two places that hold the
        finished roster: `build_etw_pmc_session()` for a replayed capture and
        the live factory's `finalize()` for a physical one. Until that step
        existed, every foreign context switch on a busy host reached
        `consume_cswitch()` and aborted the collection as
        `ETW_CSWITCH_UNATTRIBUTED_THREAD`. Witness bw73.
        """
        if (root_process_id is None) != (root_process_start_key is None):
            raise EtwConsumerFault(
                "ETW_MEMBER_SCOPE_IDENTITY_INCOMPLETE: scoping a capture to the "
                "measured Job needs BOTH the root PID and the root start key")
        if self._callback_faults:
            raise EtwConsumerFault(
                "ETW_CONSUMER_CALLBACK_FAULT:" + ";".join(self._callback_faults))
        if self._capability_facts is None:
            raise EtwConsumerFault("ETW_CAPABILITY_NOT_QUERIED")
        if self._loss is None:
            raise EtwConsumerFault(
                "ETW_TRACE_NOT_STOPPED: stop() has not run, so the drain is "
                "unproven and no loss counters were read while the session was "
                "alive")
        if self._drain_faults:
            raise EtwConsumerFault(
                "ETW_TRACE_DRAIN_INCOMPLETE:" + ";".join(self._drain_faults))
        provenance: dict[str, Any] = {
            "consumer": __name__, "session_name": self.session_name,
            "same_session_claim": SAME_SESSION_UNCERTAINTY}
        foreign_thread_events: list[dict[str, Any]] = []
        if root_process_id is None:
            process_events = list(self._process_events)
            thread_events = list(self._thread_events)
            provenance["member_scope"] = "UNSCOPED_RAW_STREAM"
        else:
            partition = partition_job_member_events(
                self._process_events, self._thread_events,
                root_process_id=root_process_id,
                root_process_start_key=str(root_process_start_key))
            process_events = partition.process_events
            thread_events = partition.thread_events
            # The excluded half is EVIDENCE, not a leftover: it is the only
            # thing that can tell a host thread that recycled a member TID from
            # a member TID nobody can place. It used to be counted and dropped.
            foreign_thread_events = list(partition.excluded_thread_events)
            provenance["member_scope"] = "JOB_MEMBER_TREE"
            provenance["excluded_foreign_process_events"] = len(
                partition.excluded_process_events)
            provenance["excluded_foreign_thread_events"] = len(
                partition.excluded_thread_events)
        return CapturedTrace(
            cswitch_records=list(self._cswitch_records),
            process_events=process_events,
            thread_events=bind_thread_start_keys(thread_events, process_events),
            capability_facts=dict(self._capability_facts),
            loss=self._loss,
            session_handle=int(self._recorded_session_handle),
            source_id=int(self._source_id),
            provenance=provenance,
            foreign_thread_events=foreign_thread_events)
