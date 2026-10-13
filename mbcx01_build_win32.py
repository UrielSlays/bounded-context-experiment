"""BUILD B real Windows collector — REVIEWABLE CODE, NOT EXECUTED BY ANY TEST.

This module is the physical half of the BUILD B producer: the ctypes bindings
and the ordered orchestration that turn one candidate command line into one
`mbcx01_build_windows_producer.SimulatedCollection`-shaped observation record.
`mbcx01_build_windows_producer` never imports it; the producer only ever sees
the returned structure, so a fixture collection and a physical collection
differ in provenance and never in shape.

NOTHING HERE RUNS IN THIS TASK. The module is importable everywhere (all Win32
symbols are bound lazily inside `_win32()`), and `collect()` refuses to run
unless BOTH of these are present:

- the environment variable `MBCX01_BUILD_ALLOW_PHYSICAL=1`; and
- an explicit `authorization_path` argument naming a runbook authorization
  file that exists and carries the pinned authorization marker.

Neither is set anywhere in this repository. Executing a physical collection is
an owner-authorized runbook step, never a side effect of importing a module or
running a test.

Contract discipline implemented here (each step is ordered and checked; the
order IS the evidence, see MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md §2-§4):

1. `CreateProcessW(..., CREATE_SUSPENDED)` — the candidate root never executes
   an instruction before the Job exists and is configured;
2. `CreateJobObjectW` + `SetInformationJobObject(JobObjectExtendedLimitInformation)`
   with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and with BOTH breakaway bits
   (`JOB_OBJECT_LIMIT_BREAKAWAY_OK`, `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`)
   cleared, so no descendant can leave the accounting boundary;
3. `CreateIoCompletionPort` + `SetInformationJobObject(JobObjectAssociateCompletionPortInformation)`
   BEFORE the root resumes, so no NEW_PROCESS/EXIT_PROCESS message can be
   missed by construction (delivery itself is still only diagnostic);
4. `AssignProcessToJobObject` BEFORE `ResumeThread`;
5. identity: PID plus the 64-bit process start key for the root and every
   descendant, so PID reuse cannot substitute a member;
6. terminal barrier, then final queries: signed terminal lifetimes for every
   assigned PID/start key and `ActiveProcesses == 0` FIRST, then the two
   `QueryInformationJobObject` calls whose raw 96/144-byte buffers are
   retained verbatim. The barrier is the root wait plus the Job's own
   active-process count, under ONE deadline; completion messages are polled
   with a zero wait and never waited for, because §3 permits any of them —
   `ACTIVE_PROCESS_ZERO` included — to be undelivered;
7. strict ETW PMC: `TraceSetInformation(TracePmcCounterListInfo)` +
   `TraceSetInformation(TracePmcEventListInfo)` attaching `InstructionRetired`
   to `CSwitch`, ordered per-processor consumption, and any lost-event counter
   is fatal.

FAULT is not a verdict (Gravity slice0c): every native call is checked and a
failure raises `CollectorFault`. The collector never returns partial evidence,
never substitutes a default for an unreadable value and never downgrades an
unavailable capability into a diagnostic success.
"""

from __future__ import annotations

import ctypes
import os
import sys
import time
from ctypes import wintypes
from dataclasses import dataclass
from typing import Any, Callable

# --- Pinned ABI constants -------------------------------------------------
# These MUST equal the layout the frozen packer `mbcx01_r13_measurement._query_evidence`
# (:551-571) writes and the frozen validator `_validate_query_evidence`
# (:777-803) reads; `verify_struct_layout()` below re-derives them from the
# ctypes structures so a drift is a hard failure, not a silent mis-read.

JOBOBJECT_BASIC_AND_IO_ACCOUNTING_SIZE = 96
JOBOBJECT_EXTENDED_LIMIT_SIZE = 144
JOBOBJECT_BASIC_LIMIT_SIZE = 64
IO_COUNTERS_SIZE = 48
# Offsets inside JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION (64-bit ABI).
OFFSET_TOTAL_USER_TIME = 0
OFFSET_TOTAL_KERNEL_TIME = 8
OFFSET_THIS_PERIOD_TOTAL_USER_TIME = 16
OFFSET_THIS_PERIOD_TOTAL_KERNEL_TIME = 24
OFFSET_TOTAL_PAGE_FAULT_COUNT = 32
OFFSET_TOTAL_PROCESSES = 36
OFFSET_ACTIVE_PROCESSES = 40
OFFSET_TOTAL_TERMINATED_PROCESSES = 44
OFFSET_IO_COUNTERS = 48
# Offsets inside JOBOBJECT_EXTENDED_LIMIT_INFORMATION (64-bit ABI).
OFFSET_EXTENDED_IO_COUNTERS = 64
OFFSET_PROCESS_MEMORY_LIMIT = 112
OFFSET_JOB_MEMORY_LIMIT = 120
OFFSET_PEAK_PROCESS_MEMORY_USED = 128
OFFSET_PEAK_JOB_MEMORY_USED = 136  # == the frozen packer's peak_committed offset

# --- Win32 numeric constants ---------------------------------------------
CREATE_SUSPENDED = 0x00000004
CREATE_UNICODE_ENVIRONMENT = 0x00000400
CREATE_BREAKAWAY_FROM_JOB = 0x01000000  # named to be refused, never requested

JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION = 0x00000400
JOB_OBJECT_LIMIT_BREAKAWAY_OK = 0x00000800
JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK = 0x00001000
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000

JobObjectBasicProcessIdList = 3
JobObjectAssociateCompletionPortInformation = 7
JobObjectBasicAndIoAccountingInformation = 8
JobObjectExtendedLimitInformation = 9

JOB_OBJECT_MSG_END_OF_JOB_TIME = 1
JOB_OBJECT_MSG_END_OF_PROCESS_TIME = 2
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
JOB_OBJECT_MSG_NEW_PROCESS = 6
JOB_OBJECT_MSG_EXIT_PROCESS = 7
JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS = 8

#: Ceiling on the variable-length PROCESS_TELEMETRY_ID_INFORMATION record the
#: OS asks for. It measured 454 bytes on the box this was written against; the
#: ceiling exists so a nonsense ReturnLength becomes a named fault instead of an
#: allocation.
PROCESS_TELEMETRY_ID_MAX_BYTES = 65536

#: Exit code `collect()` gives a child it created SUSPENDED and could not hand
#: to the Job. Such a child never executed one instruction, so this code never
#: appears in any measurement — no collection that reaches the barrier can
#: produce it, because a child that got that far is Job-owned.
SUSPENDED_CHILD_TERMINATION_EXIT_CODE = 0xC0000001  # STATUS_UNSUCCESSFUL

INFINITE = 0xFFFFFFFF
WAIT_OBJECT_0 = 0x00000000
WAIT_TIMEOUT = 0x00000102
STILL_ACTIVE = 259

# Completion messages are DIAGNOSTICS (harness requirements §3): the drain polls
# with a zero millisecond wait and takes only what is already queued, so a
# message that is never delivered costs nothing. Nothing in the collector ever
# WAITS for one — the barrier is the Job's own active-process count.
COMPLETION_DRAIN_POLL_MS = 0
# Sleep between two Job active-process queries while the barrier is still open.
ACTIVE_PROCESS_ZERO_POLL_INTERVAL_S = 0.0005

# TRACE_QUERY_INFO_CLASS (evntrace.h). The two PMC classes are the only ones
# this collector sets. BUILD REVIEW ITEM — DISCHARGED 2026-08-14: both ordinals were verified at the
# Microsoft TRACE_QUERY_INFO_CLASS page (TracePmcEventListInfo=8,
# TracePmcCounterListInfo=9); see mbcx01_build_etw_consumer.py. Formerly: re-verify against the
# installed Windows SDK header before the first physical run — a wrong ordinal
# must fail the capability query, never silently configure nothing.
TracePmcEventListInfo = 8
TracePmcCounterListInfo = 9

# NtQueryInformationProcess classes used for process identity.
ProcessTelemetryIdInformation = 64

# ETW PMC source name and event list this collector pins (harness §4).
PMC_SOURCE_NAME = "InstructionRetired"
PMC_EVENT_LIST = "CSwitch"

AUTHORIZATION_MARKER = "MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED"
ALLOW_PHYSICAL_ENV = "MBCX01_BUILD_ALLOW_PHYSICAL"


class CollectorFault(RuntimeError):
    """A native call failed or an observation is unreadable.

    A fault is NOT a measurement verdict. It aborts the collection so that no
    partial, defaulted or repaired evidence can ever be signed.
    """


class PhysicalCollectionNotAuthorized(RuntimeError):
    """`collect()` was reached without the explicit two-factor authorization."""


# --- ctypes structures ----------------------------------------------------


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong)]


class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
    _fields_ = [("TotalUserTime", ctypes.c_longlong),
                ("TotalKernelTime", ctypes.c_longlong),
                ("ThisPeriodTotalUserTime", ctypes.c_longlong),
                ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
                ("TotalPageFaultCount", wintypes.DWORD),
                ("TotalProcesses", wintypes.DWORD),
                ("ActiveProcesses", wintypes.DWORD),
                ("TotalTerminatedProcesses", wintypes.DWORD)]


class JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION(ctypes.Structure):
    _fields_ = [("BasicInfo", JOBOBJECT_BASIC_ACCOUNTING_INFORMATION),
                ("IoInfo", IO_COUNTERS)]


class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.POINTER(ctypes.c_ulong)),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD)]


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t)]


class JOBOBJECT_ASSOCIATE_COMPLETION_PORT(ctypes.Structure):
    _fields_ = [("CompletionKey", ctypes.c_void_p),
                ("CompletionPort", wintypes.HANDLE)]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
                ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD)]


class STARTUPINFOW(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
                ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR),
                ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
                ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD),
                ("dwXCountChars", wintypes.DWORD), ("dwYCountChars", wintypes.DWORD),
                ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
                ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
                ("hStdInput", wintypes.HANDLE), ("hStdOutput", wintypes.HANDLE),
                ("hStdError", wintypes.HANDLE)]


def verify_struct_layout() -> dict[str, int]:
    """Re-derive the pinned sizes/offsets from the structures themselves.

    This is the ONLY function in this module a test may exercise: it touches no
    OS state. A mismatch means the collector would read a different field than
    the frozen packer wrote, which is a hard build failure.
    """
    if ctypes.sizeof(ctypes.c_void_p) != 8:
        raise CollectorFault("WINDOWS_64BIT_ABI_REQUIRED")
    derived = {
        "basic_and_io_size": ctypes.sizeof(JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION),
        "extended_limit_size": ctypes.sizeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION),
        "basic_limit_size": ctypes.sizeof(JOBOBJECT_BASIC_LIMIT_INFORMATION),
        "io_counters_size": ctypes.sizeof(IO_COUNTERS),
        "total_page_fault_offset":
            JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.TotalPageFaultCount.offset,
        "total_processes_offset":
            JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.TotalProcesses.offset,
        "active_processes_offset":
            JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.ActiveProcesses.offset,
        "total_terminated_offset":
            JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.TotalTerminatedProcesses.offset,
        "io_counters_offset": JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION.IoInfo.offset,
        "peak_job_memory_offset":
            JOBOBJECT_EXTENDED_LIMIT_INFORMATION.PeakJobMemoryUsed.offset,
    }
    expected = {
        "basic_and_io_size": JOBOBJECT_BASIC_AND_IO_ACCOUNTING_SIZE,
        "extended_limit_size": JOBOBJECT_EXTENDED_LIMIT_SIZE,
        "basic_limit_size": JOBOBJECT_BASIC_LIMIT_SIZE,
        "io_counters_size": IO_COUNTERS_SIZE,
        "total_page_fault_offset": OFFSET_TOTAL_PAGE_FAULT_COUNT,
        "total_processes_offset": OFFSET_TOTAL_PROCESSES,
        "active_processes_offset": OFFSET_ACTIVE_PROCESSES,
        "total_terminated_offset": OFFSET_TOTAL_TERMINATED_PROCESSES,
        "io_counters_offset": OFFSET_IO_COUNTERS,
        "peak_job_memory_offset": OFFSET_PEAK_JOB_MEMORY_USED,
    }
    if derived != expected:
        raise CollectorFault(f"JOB_QUERY_ABI_DRIFT:{derived}")
    return derived


# --- lazy Win32 binding ---------------------------------------------------


@dataclass(frozen=True)
class _Win32:
    kernel32: Any
    ntdll: Any
    advapi32: Any


def _win32() -> _Win32:
    """Bind the Win32 entry points. Import-safe: nothing binds at module import."""
    if os.name != "nt":
        raise CollectorFault("WINDOWS_HOST_REQUIRED")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    ntdll = ctypes.WinDLL("ntdll", use_last_error=True)
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD)]
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.CreateIoCompletionPort.argtypes = [
        wintypes.HANDLE, wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    kernel32.CreateIoCompletionPort.restype = wintypes.HANDLE
    kernel32.GetQueuedCompletionStatus.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p), wintypes.DWORD]
    kernel32.GetQueuedCompletionStatus.restype = wintypes.BOOL
    kernel32.CreateProcessW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.LPVOID, wintypes.LPVOID,
        wintypes.BOOL, wintypes.DWORD, wintypes.LPVOID, wintypes.LPCWSTR,
        ctypes.POINTER(STARTUPINFOW), ctypes.POINTER(PROCESS_INFORMATION)]
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    kernel32.ResumeThread.restype = wintypes.DWORD
    # Only ever called on a child this collector created SUSPENDED and could not
    # hand to the Job — see `collect()`'s cleanup. It is never used to end a
    # process the Job owns; that is what KILL_ON_JOB_CLOSE is for.
    kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.QueryPerformanceCounter.argtypes = [ctypes.POINTER(ctypes.c_longlong)]
    kernel32.QueryPerformanceCounter.restype = wintypes.BOOL
    kernel32.QueryPerformanceFrequency.argtypes = [ctypes.POINTER(ctypes.c_longlong)]
    kernel32.QueryPerformanceFrequency.restype = wintypes.BOOL
    kernel32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    ntdll.NtQueryInformationProcess.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.ULONG,
        ctypes.POINTER(wintypes.ULONG)]
    ntdll.NtQueryInformationProcess.restype = ctypes.c_long
    # TraceSetInformation is exported by advapi32 (and sechost on newer builds).
    advapi32.TraceSetInformation.argtypes = [
        ctypes.c_ulonglong, ctypes.c_int, wintypes.LPVOID, wintypes.ULONG]
    advapi32.TraceSetInformation.restype = wintypes.ULONG
    return _Win32(kernel32=kernel32, ntdll=ntdll, advapi32=advapi32)


def _check(ok: Any, api: str) -> None:
    """Every native return is checked; a failure is a fault, never a value."""
    if not ok:
        raise CollectorFault(f"{api}:WIN32_ERROR={ctypes.get_last_error()}")


def _check_handle(handle: Any, api: str) -> Any:
    if not handle:
        raise CollectorFault(f"{api}:WIN32_ERROR={ctypes.get_last_error()}")
    return handle


def _check_nt(status: int, api: str) -> None:
    if status != 0:
        raise CollectorFault(f"{api}:NTSTATUS=0x{status & 0xFFFFFFFF:08X}")


# --- identity -------------------------------------------------------------


class PROCESS_TELEMETRY_ID_INFORMATION(ctypes.Structure):
    """Prefix of PROCESS_TELEMETRY_ID_INFORMATION up to ProcessSequenceNumber.

    SOURCE NOTE (start-key acquisition, BUILD REVIEW ITEM): the carrier of the
    64-bit per-incarnation identity for EVERY member — including descendants
    this collector never opened a handle to — is the
    `Microsoft-Windows-Kernel-Process` ETW provider's ProcessStart payload. That
    payload publishes the identity as `ProcessSequenceNumber`; it has no field
    named `ProcessStartKey` in any published version of the template (the
    version-by-version table is at
    `mbcx01_build_etw_consumer.KERNEL_PROCESS_PAYLOAD_LAYOUTS`).

    THESE TWO STRUCTURE MEMBERS ARE NOT THE SAME NUMBER, which is why the field
    this module reads is named explicitly. Measured at the byte on this box over
    12 live processes: `ProcessStartKey` carries a boot session id in its high
    16 bits and the sequence number in its low 48
    (e.g. pid 8548 -> ProcessStartKey 0x0048000000000096,
    ProcessSequenceNumber 0x0000000000000096). Reading `ProcessStartKey` for the
    root would therefore hand the ETW consumer a value no ProcessStart payload
    can ever equal, and every physical collection would abort at
    `ETW_PROCESS_LIFETIME_ROOT_ABSENT`. `query_process_start_key()` reads the
    sequence number so that the root's identity is the SAME quantity ETW
    publishes for the members. The high-16-bit composition above is an
    OBSERVATION, not a rule this module relies on: nothing here reconstructs one
    value from the other.
    """

    _fields_ = [("HeaderSize", wintypes.ULONG), ("ProcessId", wintypes.ULONG),
                ("ProcessStartKey", ctypes.c_ulonglong),
                ("CreateTime", ctypes.c_ulonglong),
                ("CreateInterruptTime", ctypes.c_ulonglong),
                ("CreateUnbiasedInterruptTime", ctypes.c_ulonglong),
                ("ProcessSequenceNumber", ctypes.c_ulonglong)]


def query_process_start_key(win32: _Win32, process_handle: Any) -> int:
    """The root's 64-bit identity, as the SAME quantity ETW publishes.

    Returns `ProcessSequenceNumber`, not the sibling `ProcessStartKey`: the two
    differ by a boot session id in the high 16 bits and only the sequence number
    appears in a Microsoft-Windows-Kernel-Process ProcessStart payload, so only
    the sequence number can be matched against the captured root. See
    `PROCESS_TELEMETRY_ID_INFORMATION` for the measurements. A zero is
    `PROCESS_START_KEY_UNAVAILABLE`, never a usable identity.

    THE BUFFER IS SIZED BY THE OS, NOT BY THE PREFIX. This information class
    fills a variable-length record — 454 bytes on the box this was measured on
    — and refuses anything shorter outright: asking with the 48-byte prefix
    above returns STATUS_INFO_LENGTH_MISMATCH (0xC0000004) and fills nothing,
    and asking with 96 returns STATUS_BUFFER_OVERFLOW (0x80000005). So the
    length is asked for first (a zero-length call reports the requirement in
    `ReturnLength` without touching the buffer), then requested in full, and the
    fixed prefix is read out of what came back. A length that could not hold the
    prefix, or that is absurd, is a named fault rather than a short read.
    """
    required = wintypes.ULONG(0)
    win32.ntdll.NtQueryInformationProcess(
        process_handle, ProcessTelemetryIdInformation, None, 0,
        ctypes.byref(required))
    length = int(required.value)
    if length < ctypes.sizeof(PROCESS_TELEMETRY_ID_INFORMATION):
        raise CollectorFault(f"PROCESS_TELEMETRY_ID_LENGTH_IMPLAUSIBLE:{length}")
    if length > PROCESS_TELEMETRY_ID_MAX_BYTES:
        raise CollectorFault(f"PROCESS_TELEMETRY_ID_LENGTH_IMPLAUSIBLE:{length}")
    raw = (ctypes.c_ubyte * length)()
    ctypes.cast(raw, ctypes.POINTER(wintypes.ULONG))[0] = length  # HeaderSize
    returned = wintypes.ULONG(0)
    status = win32.ntdll.NtQueryInformationProcess(
        process_handle, ProcessTelemetryIdInformation, ctypes.byref(raw),
        length, ctypes.byref(returned))
    _check_nt(status, "NtQueryInformationProcess(ProcessTelemetryIdInformation)")
    if int(returned.value) < ctypes.sizeof(PROCESS_TELEMETRY_ID_INFORMATION):
        raise CollectorFault(
            f"PROCESS_TELEMETRY_ID_SHORT_RETURN:{int(returned.value)}")
    buffer = PROCESS_TELEMETRY_ID_INFORMATION.from_buffer(raw)
    if buffer.ProcessSequenceNumber == 0:
        raise CollectorFault("PROCESS_START_KEY_UNAVAILABLE")
    return int(buffer.ProcessSequenceNumber)


# --- ETW PMC session ------------------------------------------------------


def resolve_thread_lifetime(lifetimes: Any, thread_id: int,
                            qpc: int) -> dict[str, Any] | None:
    """The ONE lifetime of `thread_id` whose interval contains `qpc`, or None.

    A thread id identifies a thread only WITHIN its own lifetime: Windows
    reuses a TID after the thread has terminated (Learn, *PsGetThreadId*
    Remarks; *Thread Handles and Identifiers*), so the roster may carry several
    disjoint rows for one TID and the QPC is what tells them apart.

    Returns None — never a neighbouring row — when the observation falls in no
    lifetime, and None as well if two rows both contain it, because an
    ambiguous attribution is not an attribution. The caller turns that into
    `ETW_CSWITCH_UNATTRIBUTED_THREAD`; the assembler that BUILDS the roster has
    already refused overlapping lifetimes by name, so a second match here means
    the roster was not built by that assembler.
    """
    found = []
    for row in lifetimes:
        # r7 fold (SEAT1 F7): a roster row missing its interval fields used to
        # surface as a raw KeyError here — a fault without a name. The posture
        # is unchanged (a malformed roster never attributes anything); only
        # the refusal now says what it refused.
        try:
            matches = (row["thread_id"] == thread_id
                       and row["started_qpc"] <= qpc <= row["ended_qpc"])
        except (KeyError, TypeError) as exc:
            raise CollectorFault(
                f"ETW_THREAD_ROSTER_ROW_INVALID:{exc!r}") from exc
        if matches:
            found.append(row)
    return found[0] if len(found) == 1 else None


@dataclass
class EtwPmcSession:
    """Strict event-attached PMC session configuration and consumption.

    Configuration is exactly the two documented calls: pin the counter list to
    `InstructionRetired` (`TracePmcCounterListInfo`) and attach it to the
    `CSwitch` event (`TracePmcEventListInfo`). Anything the platform will not
    grant — an unavailable source, a counter-owner conflict, multiplexing, or
    any nonzero `EventsLost`/`LogBuffersLost`/`RealTimeBuffersLost` — is
    reported as UNAVAILABLE evidence, never as a diagnostic success and never
    as an estimated instruction count.
    """

    session_handle: int
    capability: dict[str, Any]
    attachment: dict[str, Any]
    observations: list[dict[str, Any]]
    thread_lifetimes: list[dict[str, Any]]
    events_lost: int = 0
    log_buffers_lost: int = 0
    realtime_buffers_lost: int = 0
    # AMENDMENT-3 (2026-08-16): per-processor predecessor baselines from the
    # CSwitch scoping — rows of {"processor", "counter_value"}. The interval
    # that ends at a processor's FIRST member switch-out is member work; the
    # scoping records the raw counter of the record immediately preceding it
    # so `consume_cswitch()` can count that interval instead of hard-coding
    # the first delta to zero (which signed a bounded-looking undercount of
    # unbounded magnitude — the r6 NO-GO). A processor with no predecessor
    # (capture-start) carries a row holding its own first counter, so its delta
    # is the declared zero — an explicit observation, never an absence (r7
    # totality rule; the r8 seats caught this comment still saying "no row").
    first_member_baselines: tuple = ()
    # BUILD ITEM (the ETW consumer seam): `record_stream` is the callable the
    # `ProcessTrace`/`EventRecordCallback` consumer supplies, yielding raw
    # CSwitch/PMC records in per-processor timestamp order; `member_lifetimes`
    # is the signed PID/start-key lifetime list for every member, terminated
    # included, built from the `Microsoft-Windows-Kernel-Process`
    # ProcessStart/ProcessStop stream of the SAME session — the only source
    # that observes a descendant this collector never opened a handle to. Both
    # are seams so the ordering/delta/join discipline below is reviewable
    # without opening an ETW session; an unattached seam is a fault, never an
    # empty result.
    #
    # BUILT 2026-08-14 by `mbcx01_build_etw_consumer`, which also supplies the
    # two seams below. They are separate fields, not extra keys on `capability`
    # / `attachment`, because those two dicts are copied VERBATIM into the
    # signed evidence tree and the frozen validator requires them to equal
    # EXACTLY `CAPABILITY_QUERY_KEYS` / `EVENT_ATTACHMENT_KEYS`:
    #
    # - `event_id_blob` is the real CLASSIC_EVENT_ID payload (Thread class GUID
    #   3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c + type 36) that
    #   `TracePmcEventListInfo` attaches the counter to. `configure()` used to
    #   send a ZERO-FILLED buffer sized from `attachment["event_id_blob_size"]`
    #   — a key `EVENT_ATTACHMENT_KEYS` cannot carry — which would have
    #   attached InstructionRetired to GUID_NULL/type 0 and collected nothing.
    # - `capability_facts` is what the platform GRANTED. `_trace_facts()` used
    #   to read those facts out of `capability`, which can only ever hold the
    #   five evidence keys, so a healthy PMU was reported as
    #   `etw_pmc_source_available: False` next to summed PMC deltas.
    #
    # Both are seams with the same posture as the two above: unattached is a
    # FAULT, never a default.
    # - `trace_finalizer` closes the cell's TRACE WINDOW at the terminal
    #   barrier. It exists because a LIVE session cannot otherwise be built at
    #   all: `collect()` calls the factory BEFORE `ResumeThread`, so at that
    #   instant the candidate has not executed and the signed PID/start-key
    #   roster the session must carry does not exist yet — it is only complete
    #   when the last ProcessStop arrives. `consume_cswitch()` reads
    #   `self.thread_lifetimes` on its first line, before it calls `records()`,
    #   so the roster has to be complete by then, and until this hook existed
    #   `collect()` offered no call site between the barrier and consumption
    #   where the consumer could complete it.
    record_stream: Callable[[], Any] | None = None
    member_lifetimes: list[dict[str, Any]] | None = None
    event_id_blob: bytes | None = None
    capability_facts: dict[str, Any] | None = None
    trace_finalizer: Callable[["EtwPmcSession"], None] | None = None
    # - the root this session is measuring. `collect()` sets both AFTER it has
    #   queried the start key and BEFORE it configures the session or resumes
    #   the candidate, so the finalizer can bind the observed ETW roster to the
    #   process the collector actually created. Without this seam a consumer
    #   has to eavesdrop on `query_process_start_key`, which is a patch, not a
    #   contract.
    root_process_id: int | None = None
    root_process_start_key: str | None = None

    def records(self) -> Any:
        if self.record_stream is None:
            raise CollectorFault("ETW_CONSUMER_NOT_ATTACHED")
        return self.record_stream()

    def members(self) -> list[dict[str, Any]]:
        if not self.member_lifetimes:
            raise CollectorFault("ETW_PROCESS_LIFETIME_STREAM_NOT_ATTACHED")
        return list(self.member_lifetimes)

    def classic_event_id_blob(self) -> bytes:
        """The CLASSIC_EVENT_ID payload `TracePmcEventListInfo` attaches to."""
        if not self.event_id_blob:
            raise CollectorFault("ETW_EVENT_ATTACHMENT_BLOB_NOT_ATTACHED")
        return bytes(self.event_id_blob)

    def granted_capability(self) -> dict[str, Any]:
        """What the platform granted — never inferred from the evidence record."""
        if not self.capability_facts:
            raise CollectorFault("ETW_CAPABILITY_FACTS_NOT_ATTACHED")
        return dict(self.capability_facts)

    def root_identity(self) -> tuple[int, str]:
        """The (PID, 16-hex start key) pair this session is measuring."""
        pid = self.root_process_id
        key = self.root_process_start_key
        if pid is None or key is None:
            raise CollectorFault("ETW_ROOT_IDENTITY_NOT_ATTACHED")
        if (not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0
                or not isinstance(key, str) or len(key) != 16
                or any(char not in "0123456789ABCDEF" for char in key)):
            raise CollectorFault(f"ETW_ROOT_IDENTITY_INVALID:{pid!r}/{key!r}")
        return int(pid), key

    def close_trace_window(self) -> None:
        """Close this cell's trace window at the terminal barrier.

        Called by `collect()` AFTER every member is terminal and BEFORE any
        counter delta is read, so the record stream and the signed lifetime
        rosters are complete and frozen before consumption starts. A missing
        finalizer is a FAULT and never a no-op: silently consuming a trace
        window nobody closed would read a partial stream as a whole one.
        """
        if self.trace_finalizer is None:
            raise CollectorFault("ETW_TRACE_FINALIZER_NOT_ATTACHED")
        self.trace_finalizer(self)

    def configure(self, win32: _Win32, source_id: int) -> None:
        source = ctypes.c_ulong(source_id)
        status = win32.advapi32.TraceSetInformation(
            self.session_handle, TracePmcCounterListInfo,
            ctypes.byref(source), ctypes.sizeof(source))
        if status != 0:
            raise CollectorFault(f"TraceSetInformation(TracePmcCounterListInfo):{status}")
        # CLASSIC_EVENT_ID list pinning InstructionRetired to CSwitch. The blob
        # is the ATTACHED one, built by the consumer from the documented kernel
        # CSwitch GUID/type pair, so the attachment is never guessed and never
        # a zero-filled placeholder.
        blob = self.classic_event_id_blob()
        event_list = (ctypes.c_ubyte * len(blob))(*blob)
        status = win32.advapi32.TraceSetInformation(
            self.session_handle, TracePmcEventListInfo,
            ctypes.byref(event_list), ctypes.sizeof(event_list))
        if status != 0:
            raise CollectorFault(f"TraceSetInformation(TracePmcEventListInfo):{status}")

    def consume_cswitch(self) -> list[dict[str, Any]]:
        """Ordered per-processor CSwitch consumption with recomputed deltas.

        Every counter delta is recomputed from consecutive counter values on
        the SAME processor and attributed to the outgoing `OldThreadId`, then
        joined to a signed Job-member PID/start-key/TID lifetime. An event that
        cannot be joined is a fault: an unattributable delta may never be
        summed into a retired-instruction total.

        The join is by TID *and* QPC (AMENDMENT-2, 2026-08-15). Windows reuses
        a thread id once the thread has terminated, so one TID can own several
        DISJOINT lifetimes in one capture; this used to build one dict entry per
        TID, which silently kept whichever row the roster happened to list last
        and attributed both lives' deltas to it. `resolve_thread_lifetime()`
        picks the lifetime whose interval CONTAINS the record's QPC, and a QPC
        inside none of them is `ETW_CSWITCH_UNATTRIBUTED_THREAD` — the same
        refusal an unknown TID already got, for the same reason.
        """
        previous_by_processor: dict[int, int] = {}
        # AMENDMENT-3: seed each baselined processor with its predecessor's
        # raw counter, so the first member delta is counter - baseline (the
        # member's actual first interval) rather than a hard-coded zero. A
        # malformed baseline row is a fault, never a silent zero.
        for row in self.first_member_baselines:
            if (not isinstance(row, dict)
                    or set(row) != {"processor", "counter_value"}
                    or not all(isinstance(row[name], int)
                               and not isinstance(row[name], bool)
                               and row[name] >= 0
                               for name in ("processor", "counter_value"))
                    or row["processor"] in previous_by_processor):
                raise CollectorFault("ETW_CSWITCH_BASELINE_INVALID")
            previous_by_processor[int(row["processor"])] = int(row["counter_value"])
        observations: list[dict[str, Any]] = []
        lifetimes = list(self.thread_lifetimes)
        for sequence, record in enumerate(self.records()):
            processor = int(record["processor"])
            counter_value = int(record["instruction_retired"])
            thread_id = int(record["old_thread_id"])
            lifetime = resolve_thread_lifetime(lifetimes, thread_id,
                                               int(record["qpc"]))
            if lifetime is None:
                raise CollectorFault("ETW_CSWITCH_UNATTRIBUTED_THREAD")
            prior = previous_by_processor.get(processor)
            delta = 0 if prior is None else counter_value - prior
            if delta < 0:
                raise CollectorFault("ETW_PMC_COUNTER_WENT_BACKWARDS")
            previous_by_processor[processor] = counter_value
            observations.append({
                "sequence": sequence, "processor": processor,
                "qpc": int(record["qpc"]), "old_thread_id": thread_id,
                "counter_value": counter_value, "delta_from_previous": delta,
                "process_id": lifetime["process_id"],
                "process_start_key": lifetime["process_start_key"]})
        if self.events_lost or self.log_buffers_lost or self.realtime_buffers_lost:
            raise CollectorFault("ETW_EVENT_LOSS_DETECTED")
        self.observations = observations
        return observations


# --- authorization gate ---------------------------------------------------


def _require_authorization(authorization_path: str | None) -> dict[str, str]:
    """Two-factor refusal: an env flag AND a runbook authorization file.

    This exists so that no import, no test run and no accidental call can start
    a physical collection. Neither factor is set anywhere in this repository.
    """
    if os.environ.get(ALLOW_PHYSICAL_ENV) != "1":
        raise PhysicalCollectionNotAuthorized(
            f"{ALLOW_PHYSICAL_ENV}=1 is required for a physical collection")
    if not authorization_path or not os.path.isfile(authorization_path):
        raise PhysicalCollectionNotAuthorized(
            "a runbook authorization file path is required")
    with open(authorization_path, encoding="utf-8") as stream:
        text = stream.read()
    if AUTHORIZATION_MARKER not in text:
        raise PhysicalCollectionNotAuthorized(
            f"authorization file does not carry {AUTHORIZATION_MARKER}")
    return {"authorization_path": os.path.abspath(authorization_path),
            "marker": AUTHORIZATION_MARKER}


# --- the orchestration ----------------------------------------------------


def collect(command_line: str, *, cell: tuple[int, int, int],
            nonce: str, external_enforcement: dict[str, Any],
            environment_record: dict[str, Any], pmc_source_id: int,
            etw_session_factory: Callable[[], EtwPmcSession],
            authorization_path: str | None = None,
            timeout_ms: int = INFINITE) -> dict[str, Any]:
    """Run ONE cell under a Job Object and return one observation record.

    Refuses to run without the explicit two-factor authorization. The returned
    mapping has exactly the field names of
    `mbcx01_build_windows_producer.SimulatedCollection`, so the producer treats
    a physical collection and a fixture collection identically.

    Ordering is the evidence and is not reorderable: suspended create → job
    create/configure (kill-on-close, both breakaway modes denied) → completion
    port associate → assign → resume → terminal barrier → final queries.

    THE CLEANUP OWNS THE WINDOW THE JOB DOES NOT. Between `CreateProcessW` and
    `AssignProcessToJobObject` the child exists, is suspended and belongs to no
    Job, so `KILL_ON_JOB_CLOSE` cannot reach it and closing its handles does not
    end it. Any failure in that window therefore TERMINATES the child
    explicitly before the handles are closed; a termination that itself fails is
    attached to the setup fault as a note rather than swallowed. After the
    assignment succeeds nothing here terminates anything — the Job does.

    `timeout_ms` is ONE overall deadline for the whole terminal barrier (root
    wait plus active-process-zero), not a per-call wait. Completion messages are
    drained non-blockingly and are never waited for, because their delivery is
    not guaranteed (harness requirements §3): waiting for a message the contract
    permits to be absent would hang at the default `INFINITE`.

    The two elapsed values this function returns are the SIGNED MEMBER-LIFETIME
    interval — earliest member ProcessStart to latest member ProcessStop, from
    the same signed lifetimes the receipt carries — converted at the measured
    QPC frequency. The collector's OWN observation interval (a QPC read before
    `CreateProcessW` and one after the barrier) is not reported: it is the fence
    that proves the signed lifetimes belong to the window this call observed.
    """
    authorization = _require_authorization(authorization_path)
    verify_struct_layout()
    win32 = _win32()
    frequency = ctypes.c_longlong(0)
    _check(win32.kernel32.QueryPerformanceFrequency(ctypes.byref(frequency)),
           "QueryPerformanceFrequency")
    # The collector's observation window OPENS here, BEFORE the candidate
    # process exists, so the root's ETW ProcessStart cannot precede it.
    observation_started_qpc = ctypes.c_longlong(0)
    _check(win32.kernel32.QueryPerformanceCounter(ctypes.byref(observation_started_qpc)),
           "QueryPerformanceCounter(observation_start)")

    startup = STARTUPINFOW()
    startup.cb = ctypes.sizeof(STARTUPINFOW)
    process_information = PROCESS_INFORMATION()
    # 1. The candidate root is created SUSPENDED: not one instruction executes
    #    before the Job exists, is configured and owns it.
    _check(win32.kernel32.CreateProcessW(
        None, ctypes.create_unicode_buffer(command_line), None, None, False,
        CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT, None, None,
        ctypes.byref(startup), ctypes.byref(process_information)), "CreateProcessW")
    job = None
    port = None
    assigned = False
    try:
        # 2. Job creation and limits. KILL_ON_JOB_CLOSE bounds the run; BOTH
        #    breakaway bits stay CLEAR so no descendant can leave accounting.
        job = _check_handle(win32.kernel32.CreateJobObjectW(None, None),
                            "CreateJobObjectW")
        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = (
            JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            | JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION)
        if limits.BasicLimitInformation.LimitFlags & (
                JOB_OBJECT_LIMIT_BREAKAWAY_OK | JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK):
            raise CollectorFault("BREAKAWAY_LIMIT_REQUESTED")
        _check(win32.kernel32.SetInformationJobObject(
            job, JobObjectExtendedLimitInformation, ctypes.byref(limits),
            ctypes.sizeof(limits)), "SetInformationJobObject(ExtendedLimit)")
        # 3. Completion port associated BEFORE resume: no NEW_PROCESS or
        #    EXIT_PROCESS message can be missed by construction. Delivery is
        #    still only diagnostic (harness requirements §3).
        port = _check_handle(win32.kernel32.CreateIoCompletionPort(
            wintypes.HANDLE(-1), None, None, 1), "CreateIoCompletionPort")
        association = JOBOBJECT_ASSOCIATE_COMPLETION_PORT()
        association.CompletionKey = ctypes.c_void_p(id(job))
        association.CompletionPort = port
        _check(win32.kernel32.SetInformationJobObject(
            job, JobObjectAssociateCompletionPortInformation,
            ctypes.byref(association), ctypes.sizeof(association)),
            "SetInformationJobObject(AssociateCompletionPort)")
        # 4. Assign BEFORE resume.
        _check(win32.kernel32.AssignProcessToJobObject(job, process_information.hProcess),
               "AssignProcessToJobObject")
        # From here on the Job owns the child, so KILL_ON_JOB_CLOSE ends it if
        # anything below fails. Before here nothing does — see the cleanup.
        assigned = True
        # 5. Identity of the root: PID + 64-bit start key, captured while the
        #    process is still suspended so no reuse window exists.
        root_start_key = query_process_start_key(win32, process_information.hProcess)
        session = etw_session_factory()
        # Tell the session which root it is measuring, as VALUES, before it is
        # configured and long before the candidate runs: the trace window's
        # finalizer binds the observed ETW roster to exactly this PID/start-key
        # pair, and a consumer must never have to infer it.
        session.root_process_id = int(process_information.dwProcessId)
        session.root_process_start_key = f"{root_start_key:016X}"
        session.root_identity()
        session.configure(win32, pmc_source_id)
        if win32.kernel32.ResumeThread(process_information.hThread) == 0xFFFFFFFF:
            raise CollectorFault("ResumeThread:WIN32_ERROR="
                                 f"{ctypes.get_last_error()}")
        # 6. Terminal barrier, under ONE deadline for the whole barrier.
        #    The load-bearing parts are the root wait and the Job's own
        #    ActiveProcesses == 0 read; completion messages are drained
        #    non-blockingly around them and are never waited for.
        deadline = _barrier_deadline(timeout_ms)
        if win32.kernel32.WaitForSingleObject(
                process_information.hProcess,
                _remaining_ms(deadline)) != WAIT_OBJECT_0:
            raise CollectorFault("ROOT_PROCESS_DID_NOT_REACH_TERMINAL_STATE")
        diagnostics = _new_completion_diagnostics()
        active = _await_active_process_zero(win32, job, port, diagnostics, deadline)
        if active != 0:
            raise CollectorFault("ACTIVE_PROCESS_RACE_AT_BARRIER")
        _drain_completion_port(win32, port, diagnostics)
        # The collector's observation window CLOSES here: the root is terminal
        # and the Job reports no active process, so every member ProcessStop
        # has already happened.
        observation_ended_qpc = ctypes.c_longlong(0)
        _check(win32.kernel32.QueryPerformanceCounter(ctypes.byref(observation_ended_qpc)),
               "QueryPerformanceCounter(observation_end)")
        # The trace window closes HERE: after the root reached its terminal
        # state and before a single counter delta is read. The consumer stops
        # its ProcessTrace pump, reads the loss counters back and completes the
        # signed PID/start-key and thread rosters inside this call, so
        # `consume_cswitch()` below sees a frozen, complete stream.
        session.close_trace_window()
        observations = session.consume_cswitch()
        members = session.members()
        # 7. Final queries, AFTER the barrier, retained as raw bytes.
        basic_raw = _query_raw(win32, job, JobObjectBasicAndIoAccountingInformation,
                               JOBOBJECT_BASIC_AND_IO_ACCOUNTING_SIZE)
        extended_raw = _query_raw(win32, job, JobObjectExtendedLimitInformation,
                                  JOBOBJECT_EXTENDED_LIMIT_SIZE)
        retired_instructions = _sum_attributed_retired_instructions(observations)
        scalars = _decode_scalars(basic_raw, extended_raw,
                                  retired_instructions=retired_instructions)
        # The signed elapsed values and the receipt's lifetimes span are the
        # SAME two endpoints; the collector's own window only fences them.
        span_started_qpc, span_ended_qpc = _member_lifetime_endpoints(members)
        _check_span_within_observation_window(
            span_started_qpc, span_ended_qpc,
            int(observation_started_qpc.value), int(observation_ended_qpc.value))
        elapsed_ticks = span_ended_qpc - span_started_qpc
        completion = _completion_record(
            diagnostics, final_active_processes=active,
            all_members_terminal=all(
                row.get("terminal_status") == "EXITED" for row in members))
        return {
            "H": cell[0], "D": cell[1], "F": cell[2],
            "job_object_id": f"JOB.{cell[0]}.{cell[1]}.{cell[2]}",
            "root_process_id": int(process_information.dwProcessId),
            "root_process_start_key": f"{root_start_key:016X}",
            "created_suspended": True,
            "completion_port_associated_before_resume": True,
            "assigned_before_resume": True,
            "breakaway_enabled": False,
            "silent_breakaway_enabled": False,
            "basic_and_io_raw_bytes": basic_raw,
            "basic_and_io_query": _query_metadata(
                "JobObjectBasicAndIoAccountingInformation",
                JOBOBJECT_BASIC_AND_IO_ACCOUNTING_SIZE, len(basic_raw)),
            "extended_limit_raw_bytes": extended_raw,
            "extended_limit_query": _query_metadata(
                "JobObjectExtendedLimitInformation",
                JOBOBJECT_EXTENDED_LIMIT_SIZE, len(extended_raw)),
            "process_lifetimes": tuple(members),
            "thread_lifetimes": tuple(session.thread_lifetimes),
            "cswitch_observations": tuple(observations),
            "cswitch_first_member_baselines": tuple(session.first_member_baselines),
            "trace_capability_query": dict(session.capability),
            "trace_event_attachment": dict(session.attachment),
            "trace_facts": _trace_facts(session),
            "scalars": scalars,
            "qpc_frequency_hz": int(frequency.value),
            "elapsed_qpc_ticks": elapsed_ticks,
            "elapsed_monotonic_ns": elapsed_ticks * 1_000_000_000 // int(frequency.value),
            "environment": dict(environment_record),
            "external_enforcement": dict(external_enforcement),
            "completion": completion,
            "nonce": nonce,
            "collector_labels": {"collector": __name__, **authorization},
        }
    finally:
        # A child created SUSPENDED that was never ASSIGNED belongs to nobody.
        # Closing its handles does not end it, and KILL_ON_JOB_CLOSE cannot
        # reach a process no Job holds, so a failure between `CreateProcessW`
        # and `AssignProcessToJobObject` — job creation, either
        # `SetInformationJobObject`, the completion port, or the assignment
        # itself — would leave it suspended for the life of the box. It is
        # terminated EXPLICITLY here, before the handle that addresses it is
        # closed, and only when the assignment did not succeed: once the Job
        # owns the child, ending it is the Job's job.
        if not assigned and process_information.hProcess:
            if not win32.kernel32.TerminateProcess(
                    process_information.hProcess,
                    SUSPENDED_CHILD_TERMINATION_EXIT_CODE):
                secondary = ("SUSPENDED_CHILD_NOT_TERMINATED:TerminateProcess:"
                             f"WIN32_ERROR={ctypes.get_last_error()}")
                in_flight = sys.exc_info()[1]
                if in_flight is None:
                    raise CollectorFault(secondary)
                # The setup fault that got here stays the PRIMARY error; this
                # one is attached to it, so a child left running is never a
                # silent pass and never masks why the collection failed.
                in_flight.add_note(secondary)
        for handle in (process_information.hThread, process_information.hProcess,
                       port, job):
            if handle:
                win32.kernel32.CloseHandle(handle)


def _query_raw(win32: _Win32, job: Any, information_class: int, size: int) -> bytes:
    """One final query; the RAW returned bytes are the evidence, not a decode."""
    buffer = (ctypes.c_byte * size)()
    returned = wintypes.DWORD(0)
    _check(win32.kernel32.QueryInformationJobObject(
        job, information_class, ctypes.byref(buffer), size, ctypes.byref(returned)),
        f"QueryInformationJobObject({information_class})")
    if int(returned.value) != size:
        raise CollectorFault(
            f"JOB_QUERY_SHORT_RETURN:{information_class}:{int(returned.value)}")
    return bytes(bytearray(buffer))


def _query_metadata(information_class: str, size: int, returned: int) -> dict[str, Any]:
    return {"query_status_code": 0, "information_class": information_class,
            "structure_version": 1, "abi": "WINDOWS_64BIT",
            "structure_size_bytes": size, "returned_size_bytes": returned,
            "collected_after_terminal_barrier": True}


def _sum_attributed_retired_instructions(observations: Any) -> int:
    """Sum the recomputed, ALREADY-ATTRIBUTED PMC deltas of one collection.

    This is the only source of `retired_instructions`: `consume_cswitch()` has
    already recomputed each delta from consecutive counter values on the same
    processor and joined it to a signed member PID/start-key/TID lifetime, and
    an unattributable record faulted there rather than reaching this sum. The
    frozen validator recomputes the identical total from the signed evidence
    tree and requires the job scalar to equal it
    (`mbcx01_r13_measurement.py:1040-1042`), so this function exists to make
    those two numbers the same number by construction.

    A delta that is not a non-negative `int` is a FAULT: an unreadable
    observation may never be summed, skipped or coerced into a total that is
    about to be signed. A zero total is returned as observed — a cell that
    retired nothing is refused by name at admission
    (`INSTRUCTION_ACCOUNTING_MISSING`), never repaired here.
    """
    total = 0
    for observation in observations:
        delta = observation.get("delta_from_previous") if isinstance(observation, dict) else None
        if not isinstance(delta, int) or isinstance(delta, bool) or delta < 0:
            raise CollectorFault(f"ETW_PMC_DELTA_UNREADABLE:{delta!r}")
        total += delta
    return total


def _member_lifetime_endpoints(members: Any) -> tuple[int, int]:
    """The two endpoints of the signed member-lifetime interval.

    `(earliest member ProcessStart QPC, latest member ProcessStop QPC)` over the
    SIGNED lifetimes this collection is about to carry — the identical pair the
    admission cross-check recomputes from the receipt
    (`mbcx01_build_measurement_authority._timing_errors`). An empty or
    unreadable roster is a fault, never an assumed interval.
    """
    rows = list(members)
    if not rows:
        raise CollectorFault("ETW_PROCESS_LIFETIME_ROSTER_EMPTY")
    try:
        started = min(int(row["started_qpc"]) for row in rows)
        ended = max(int(row["ended_qpc"]) for row in rows)
    except (KeyError, TypeError, ValueError) as exc:
        raise CollectorFault("ETW_PROCESS_LIFETIME_QPC_UNREADABLE") from exc
    if ended <= started:
        raise CollectorFault(f"ETW_LIFETIME_SPAN_NOT_POSITIVE:{started}>={ended}")
    return started, ended


def _check_span_within_observation_window(span_started_qpc: int, span_ended_qpc: int,
                                          observation_started_qpc: int,
                                          observation_ended_qpc: int) -> None:
    """Fence: the signed lifetime interval must nest in the observed window.

    The collector opens its window with a QPC read BEFORE `CreateProcessW` and
    closes it with one AFTER the terminal barrier, and the ETW session is pinned
    to the QPC clock (`WNODE_CLIENT_CONTEXT_QPC`), so on any run of this cell
    every member ProcessStart/ProcessStop lies inside that window. A roster that
    does not is a roster from some other window — a different cell, a stale
    capture, or a clock that is not the one the receipt names — and is a FAULT
    rather than a signed number.
    """
    if not (observation_started_qpc <= span_started_qpc
            and span_ended_qpc <= observation_ended_qpc):
        raise CollectorFault(
            "ETW_LIFETIME_SPAN_OUTSIDE_OBSERVATION_WINDOW:"
            f"[{span_started_qpc},{span_ended_qpc}]"
            f"!<=[{observation_started_qpc},{observation_ended_qpc}]")


def _decode_scalars(basic_raw: bytes, extended_raw: bytes, *,
                    retired_instructions: int) -> dict[str, int]:
    """Canonical scalars: the Job's own bytes plus the summed PMC deltas.

    Every scalar except `retired_instructions` is decoded from the SAME bytes
    the receipt retains. `retired_instructions` is NOT a Job value at all and is
    a REQUIRED keyword argument: the caller passes the attributed PMC total from
    `_sum_attributed_retired_instructions()`, so a caller that forgets it gets a
    `TypeError` instead of a silently zero instruction count in a signed
    receipt.

    100-ns kernel units are converted to nanoseconds by multiplying by 100, so
    the frozen cross-check `user_time_ns % 100 == 0` holds by construction and
    a value that does not is a real disagreement rather than a rounding
    artefact (`mbcx01_r13_measurement.py:783-793`).
    """
    if (not isinstance(retired_instructions, int)
            or isinstance(retired_instructions, bool) or retired_instructions < 0):
        raise CollectorFault(f"RETIRED_INSTRUCTIONS_UNREADABLE:{retired_instructions!r}")
    accounting = JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION.from_buffer_copy(basic_raw)
    extended = JOBOBJECT_EXTENDED_LIMIT_INFORMATION.from_buffer_copy(extended_raw)
    basic = accounting.BasicInfo
    io = accounting.IoInfo
    return {
        "user_time_ns": int(basic.TotalUserTime) * 100,
        "kernel_time_ns": int(basic.TotalKernelTime) * 100,
        "total_page_faults": int(basic.TotalPageFaultCount),
        "total_processes": int(basic.TotalProcesses),
        "active_processes_at_final_query": int(basic.ActiveProcesses),
        "total_terminated_processes": int(basic.TotalTerminatedProcesses),
        "read_operations": int(io.ReadOperationCount),
        "write_operations": int(io.WriteOperationCount),
        "other_operations": int(io.OtherOperationCount),
        "read_transfer_bytes": int(io.ReadTransferCount),
        "write_transfer_bytes": int(io.WriteTransferCount),
        "other_transfer_bytes": int(io.OtherTransferCount),
        "peak_committed_bytes": int(extended.PeakJobMemoryUsed),
        # Retired instructions never come from the Job: they are the summed,
        # attributed ETW PMC deltas the caller passes in, so a Job query can
        # never stand in for PMC evidence.
        "retired_instructions": int(retired_instructions),
    }


def _active_process_count(win32: _Win32, job: Any) -> int:
    raw = _query_raw(win32, job, JobObjectBasicAndIoAccountingInformation,
                     JOBOBJECT_BASIC_AND_IO_ACCOUNTING_SIZE)
    accounting = JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION.from_buffer_copy(raw)
    return int(accounting.BasicInfo.ActiveProcesses)


def _new_completion_diagnostics() -> dict[str, Any]:
    """The message counters one collection accumulates across its drain polls."""
    return {"new_process_messages": 0, "exit_process_messages": 0,
            "active_zero_message_seen": False}


def _barrier_deadline(timeout_ms: int) -> float | None:
    """ONE deadline for the whole terminal barrier, or None for `INFINITE`."""
    if timeout_ms == INFINITE:
        return None
    return time.monotonic() + (int(timeout_ms) / 1000.0)


def _remaining_ms(deadline: float | None) -> int:
    """Milliseconds left on the barrier deadline; `INFINITE` when there is none."""
    if deadline is None:
        return INFINITE
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return 0
    return min(int(remaining * 1000), INFINITE - 1)


def _drain_completion_port(win32: _Win32, port: Any,
                           diagnostics: dict[str, Any] | None = None) -> dict[str, Any]:
    """Take the Job completion messages ALREADY QUEUED — never wait for one.

    Every `GetQueuedCompletionStatus` call here passes
    `COMPLETION_DRAIN_POLL_MS` (0), so the drain returns as soon as the queue is
    empty and costs nothing when a message the contract permits to be absent
    never arrives. Delivery is not guaranteed (harness requirements §3): the
    collector previously WAITED here for `JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO`,
    which hangs forever at the default `INFINITE` and burns the caller's whole
    timeout otherwise.

    Counters accumulate into `diagnostics` so a collection can poll repeatedly
    while its barrier is open. This function reports MESSAGES ONLY; it makes no
    claim about the Job's state, which only a Job query can observe
    (`_completion_record`).
    """
    if diagnostics is None:
        diagnostics = _new_completion_diagnostics()
    completion_code = wintypes.DWORD(0)
    completion_key = ctypes.c_void_p()
    overlapped = ctypes.c_void_p()
    while True:
        ok = win32.kernel32.GetQueuedCompletionStatus(
            port, ctypes.byref(completion_code), ctypes.byref(completion_key),
            ctypes.byref(overlapped), COMPLETION_DRAIN_POLL_MS)
        if not ok:
            if ctypes.get_last_error() == WAIT_TIMEOUT:
                break
            raise CollectorFault(
                f"GetQueuedCompletionStatus:WIN32_ERROR={ctypes.get_last_error()}")
        code = int(completion_code.value)
        if code == JOB_OBJECT_MSG_NEW_PROCESS:
            diagnostics["new_process_messages"] += 1
        elif code in (JOB_OBJECT_MSG_EXIT_PROCESS, JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS):
            diagnostics["exit_process_messages"] += 1
        elif code == JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
            diagnostics["active_zero_message_seen"] = True
    return diagnostics


def _await_active_process_zero(win32: _Win32, job: Any, port: Any,
                               diagnostics: dict[str, Any],
                               deadline: float | None) -> int:
    """THE barrier: query the Job until it reports zero active processes.

    The Job's own `ActiveProcesses` count is what closes the roster, so it is
    what is waited on — not a completion message, whose delivery the contract
    does not guarantee. Diagnostics are drained non-blockingly on every pass, so
    the message record stays as complete as the platform made it without any
    message ever being on the critical path.

    Returns the count that was observed to be zero; exceeding the caller's one
    barrier deadline is a named fault, never a partial collection.
    """
    while True:
        _drain_completion_port(win32, port, diagnostics)
        active = _active_process_count(win32, job)
        if active == 0:
            return active
        if deadline is not None and time.monotonic() >= deadline:
            raise CollectorFault(f"ACTIVE_PROCESS_ZERO_DEADLINE_EXCEEDED:{active}")
        time.sleep(ACTIVE_PROCESS_ZERO_POLL_INTERVAL_S)


def _completion_record(diagnostics: dict[str, Any], *, final_active_processes: int,
                       all_members_terminal: bool) -> dict[str, Any]:
    """The signed completion evidence: diagnostics as delivered, barrier as OBSERVED.

    The four message fields are what the completion port actually delivered — a
    cell whose messages were lost carries `False`/short counts and is not failed
    for it on its own. `completion_port_drained` means the narrow thing the
    frozen validator reads it as: the port was drained THROUGH its end-of-job
    `JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO` message. Emptying a queue that message
    never reached is not that, so it does not set the flag. The two barrier
    fields are the values the caller
    OBSERVED: `final_active_processes` is the Job query that ended the barrier
    and `all_members_terminal` is derived from the terminal status of the signed
    member roster. Neither is asserted here, because a drain cannot see either.
    """
    active_zero_seen = bool(diagnostics["active_zero_message_seen"])
    return {"completion_port_drained": active_zero_seen,
            "active_zero_message_seen": active_zero_seen,
            "new_process_messages": int(diagnostics["new_process_messages"]),
            "exit_process_messages": int(diagnostics["exit_process_messages"]),
            "diagnostic_messages_complete": active_zero_seen,
            "diagnostics_query_succeeded": True,
            "final_active_processes": int(final_active_processes),
            "all_members_terminal": bool(all_members_terminal)}


def _trace_facts(session: EtwPmcSession) -> dict[str, Any]:
    """The ETW facts exactly as the session observed them — no optimism.

    The GRANTED facts come from `session.granted_capability()`, NOT from
    `session.capability`. `capability` is the frozen five-key evidence record
    (`mbcx01_r13_measurement.CAPABILITY_QUERY_KEYS`) that `collect()` copies
    verbatim into `trace_capability_query`; it structurally cannot carry
    `pmc_source_available` / `max_pmc_counters` / `counter_owner_conflict_count`
    / `multiplexing_detected` / `attribution_complete`. Reading them out of it
    with `.get()` defaults produced a self-contradicting receipt on every real
    run: summed PMC deltas signed alongside `etw_pmc_source_available: False`
    and `etw_attribution_complete: False`. An unattached facts record is a
    FAULT here for the same reason an unattached record stream is.
    """
    granted = session.granted_capability()
    # Every lookup below is a HARD subscript, never a `.get()` with a default:
    # the facts record is a closed key set, so an absent fact is a missing
    # observation and must raise rather than become a comfortable zero.
    try:
        return {
            "instruction_backend": "ETW_PMC_EVENT_ATTACHED_V1",
            "instruction_profile_source": PMC_SOURCE_NAME.upper(),
            "instruction_event_list": PMC_EVENT_LIST.upper(),
            "instruction_attribution": (
                "SUM_INSTRUCTIONRETIRED_CSWITCH_DELTAS_BY_OLD_THREAD_JOINED_TO_"
                "SIGNED_JOB_PID_TID_LIFETIMES_INCLUDING_TERMINATED"),
            # The capability QUERY status stays on the evidence record, which
            # is the thing that carries the query's own outcome.
            "etw_capability_query_succeeded": session.capability["query_status_code"] == 0,
            "etw_pmc_source_available": bool(granted["pmc_source_available"]),
            "etw_max_pmc_counters": int(granted["max_pmc_counters"]),
            "etw_counter_owner_conflict_count":
                int(granted["counter_owner_conflict_count"]),
            "etw_pmc_strict_mode": True,
            "etw_pmc_multiplexing_detected": bool(granted["multiplexing_detected"]),
            "etw_events_lost": int(session.events_lost),
            "etw_log_buffers_lost": int(session.log_buffers_lost),
            "etw_realtime_buffers_lost": int(session.realtime_buffers_lost),
            "etw_attribution_complete": bool(granted["attribution_complete"]),
        }
    except KeyError as exc:
        raise CollectorFault(f"ETW_CAPABILITY_FACT_MISSING:{exc}") from exc


