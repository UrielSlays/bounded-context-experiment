"""MBCX-01 BUILD B — ONE-CELL smoke driver (SMOKE-RUNBOOK section 3).

⛔ NOT AUTHORIZED BY THIS FILE. Executing the `execute` mode requires the owner
authorization document named on the command line to exist and to carry the
literal marker `MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED`, an ELEVATED
session (kernel PMC needs one), and `MBCX01_BUILD_ALLOW_PHYSICAL=1` in the
environment. This module NEVER sets that variable for you: `run-smoke-cell.ps1`
sets it, in its own process only, and only under an explicit `-Execute` switch.

Three modes, in increasing order of what they touch:

  selftest   Pure logic + static ABI only. No OS state whatsoever. Safe to run
             anywhere, unelevated, and it is the only mode this BUILD ran.
  preflight  Adds READ-ONLY host probes: elevation, virtualization posture,
             authorization marker, `node` + signature-verifier-script
             availability, PMU profile-source enumeration. Starts no session,
             creates no Job, writes nothing. It executes exactly two things and
             this list is the whole of them: `node --version`, and one
             read-only WMI query for the RUNTIME virtualization posture
             (`runtime_virtualization_facts`, added by the codex-CLI r9 F3 fold
             — the posture used to be inferred from installed-component
             registry keys, which is install-time evidence, not a runtime fact).
  execute    The runbook step. Starts the ETW session, runs ONE cell through
             `mbcx01_build_win32.collect()`, writes evidence to the destination
             named in the authorization, and then runs the BUILD verifier over
             the produced envelope with the REAL `evaluation_instant`.

THE PASS CRITERION IS AN HONEST RED. The smoke run is fixture-kind evidence by
definition (runbook section 3.1) and can never clear production admission. The
expected result of step 4 is a structurally valid envelope that admission
REFUSES with the honest sentinel(s). A green admission would be a DEFECT.

That refusal is reached at the trust/custody gate, BEFORE the envelope is read,
so it proves nothing about what was produced. The envelope's validity is
therefore established independently (`validate_produced_envelope`) and the pass
criterion is the CONJUNCTION of the two; a run whose criterion is not met aborts
with a nonzero exit code instead of reporting `status: OK`.

INDEPENDENT VALIDITY IS STRUCTURE + SIGNATURE + SEMANTICS. Presence and shape
were not enough: two council seats each re-signed a receipt whose sections were
all present and whose CONTENT was false, and the criterion passed both (r6
synthesis, ruling 6). The receipt is therefore also put through the harness's own
full per-receipt validator, `mbcx01_build_measurement_authority._receipt_errors`
— CALLED, never re-implemented — with the grid/production-admission codes that
cannot apply to one operator-chosen fixture cell held aside BY NAME and RECORDED
in the report (`SMOKE_NOT_APPLICABLE_RECEIPT_CODES`, `SMOKE_COORDINATE_PROBE`).
"""

from __future__ import annotations

import argparse
import ctypes
import datetime
import json
import os
import shutil
import subprocess
import sys
import traceback
from typing import Any

import mbcx01_build_etw_consumer as etw
import mbcx01_build_measurement_authority as authority
import mbcx01_build_win32 as win32
import mbcx01_build_windows_producer as producer
import mbcx01_r13_measurement as measurement

ROOT = os.path.dirname(os.path.abspath(__file__))
FIXTURE_MANIFEST_PATH = os.path.join(
    ROOT, "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json")

#: The smoke cell's identity. Every value is a LABEL of a fixture-kind run and
#: none of it can activate production — the manifest is `production_ready:false`
#: and every key in it is `fixture_only:true`.
SMOKE_RUN_ID = "RUN.BUILD.B.SMOKE.ONE-CELL"
SMOKE_CANDIDATE_ID = "CANDIDATE.BUILD.B.SMOKE.CMD-EXIT-0"
SMOKE_NONCE_BYTES = 32

#: WHAT `SMOKE_CANDIDATE_ID` NAMES. The id is FIXED — the driver has exactly one
#: candidate and spells its identity as a constant — so the invocation it stands
#: for has to be fixed too, and written down where the identity is (codex-CLI r9
#: F4). The image is compared by BASE NAME because `cmd.exe` is resolved from the
#: session's search path (`resolve_candidate_image`), and the arguments verbatim
#: after whitespace normalisation, because they are what makes the cell exit 0.
SMOKE_CANDIDATE_IMAGE_NAME = "cmd.exe"
SMOKE_CANDIDATE_ARGUMENTS = "/c exit 0"
SMOKE_CANDIDATE_COMMAND_LINE = "cmd.exe /c exit 0"

#: The refusal a resolved invocation that is not this candidate's gets, by name.
SMOKE_COMMAND_INCONSISTENT = "SMOKE_COMMAND_INCONSISTENT_WITH_CANDIDATE_IDENTITY"

EXPECTED_RED_SENTINEL = "PHYSICAL_HARNESS_UNAVAILABLE"


class SmokeAbort(RuntimeError):
    """A precondition the runbook says must ABORT the run.

    An abort is a legitimate outcome of the authorization, not a failure to
    hide (authorization document, Reporting section).
    """

    def __init__(self, *args: Any, report: dict[str, Any] | None = None) -> None:
        super().__init__(*args)
        #: The partial run report, when the abort happened after work was done
        #: and recorded. `main` prints it alongside the abort so the reason is
        #: diagnosable from the same output rather than only from disk.
        self.report = report


# --- preconditions --------------------------------------------------------


def read_authorization(path: str) -> dict[str, str]:
    """Re-check the marker HERE as well as inside `collect()`.

    `collect()` enforces the two-factor gate itself; this is a second, earlier
    read so the driver aborts before it touches anything at all rather than
    after it has started a session.
    """
    if not path or not os.path.isfile(path):
        raise SmokeAbort(f"AUTHORIZATION_FILE_ABSENT:{path!r}")
    with open(path, encoding="utf-8") as stream:
        text = stream.read()
    if win32.AUTHORIZATION_MARKER not in text:
        raise SmokeAbort(
            f"AUTHORIZATION_MARKER_ABSENT:{win32.AUTHORIZATION_MARKER}")
    return {"authorization_path": os.path.abspath(path),
            "marker": win32.AUTHORIZATION_MARKER,
            "authorization_sha384": measurement.sha384(text)}


def authorization_mirror(authorization_path: str | None, *,
                         launch_command_line: str,
                         cell: tuple[int, int, int]) -> dict[str, Any]:
    """A MIRROR, NOT A GATE: report what the document says next to what will run.

    ⚖ OWNER RULING 2026-08-16, and the reason this function no longer decides
    anything: an earlier version of this lane made the collector REFUSE a run
    whose authorization document did not name the exact command line and cell.
    That is a machine second-guessing the OWNER — the only person who runs this
    — and it immediately proved its own harm, because resolving `cmd.exe` to its
    absolute image made the runbook's own default invocation fail its own
    authorization. Owner, verbatim: *"There better not be any adversaries, any
    advanced blocking, treating the owner as a hostile... this is a research
    harness bro. It needs to output accurate data."* The enforcing gate was
    REVERTED; `mbcx01_build_win32._require_authorization` is back to the marker
    check it always was, and this function became the mirror.

    So: read the document, say plainly whether it mentions the command line and
    the cell about to be run, and STOP. It never raises, never refuses, never
    returns a verdict. The operator reads two lines and decides — which is the
    control that was always actually operating, since the operator is the owner
    holding the runbook.
    """
    facts: dict[str, Any] = {
        "posture": "MIRROR_ONLY_NEVER_REFUSES",
        "launch_command_line": launch_command_line,
        "cell": list(cell),
        "document_mentions_command_line": None,
        "document_mentions_cell": None,
        "read_error": None,
    }
    try:
        with open(authorization_path or "", encoding="utf-8") as stream:
            text = stream.read()
    except OSError as exc:
        facts["read_error"] = f"AUTHORIZATION_UNREADABLE:{exc}"
        return facts
    facts["document_mentions_command_line"] = launch_command_line in text
    facts["document_mentions_cell"] = any(
        spelling in text
        for spelling in (f"({cell[0]}, {cell[1]}, {cell[2]})",
                         f"({cell[0]},{cell[1]},{cell[2]})"))
    return facts


def is_elevated() -> bool:
    """True when the process holds an elevated (administrator) token."""
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:  # pragma: no cover - physical only
        return False


#: INSTALLED-COMPONENT registry evidence. Every key below says a component is
#: INSTALLED. None of them says anything runs: a service key persists across the
#: role being disabled, and `vmicheartbeat` is present on an ordinary Windows 11
#: desktop that has never been a guest (measured on the build host, 2026-08-17:
#: the key exists, the service is `Stopped`). These are recorded as what they
#: are and they decide the hypervisor-present axis of NOTHING (codex-CLI r9 F3).
HYPERVISOR_GUEST_COMPONENT_KEYS = (
    r"SYSTEM\CurrentControlSet\Services\vmicheartbeat",
    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization",
)
HYPERVISOR_HOST_COMPONENT_KEYS = (
    r"SYSTEM\CurrentControlSet\Services\hvservice",
    r"SYSTEM\CurrentControlSet\Services\vmms",
)

#: The RUNTIME hypervisor question, asked of the one Windows-documented runtime
#: field this codebase can express (see `runtime_virtualization_facts`). Written
#: here as one string so the probe a report names is the probe that ran.
RUNTIME_VIRTUALIZATION_QUERY = (
    "$ErrorActionPreference = 'Stop';"
    " $cs = Get-CimInstance -ClassName Win32_ComputerSystem;"
    " $running = @(Get-CimInstance -ClassName Win32_Service"
    " -Filter \"Name LIKE 'vmic%'\" |"
    " Where-Object { $_.State -eq 'Running' } | ForEach-Object { $_.Name });"
    " [pscustomobject]@{ hypervisor_present = [bool]$cs.HypervisorPresent;"
    " guest_integration_services_running = $running } | ConvertTo-Json -Compress"
)

RUNTIME_HYPERVISOR_PROBE = "WMI_WIN32_COMPUTERSYSTEM_HYPERVISORPRESENT"


def _hyperv_registry_key_exists(path: str) -> bool:
    """Does one HKLM key EXIST? (Installed-component evidence, nothing more.)"""
    import winreg  # local import: this module must stay importable off Windows

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path):
            return True
    except OSError:
        return False


def runtime_virtualization_facts() -> dict[str, Any]:
    """READ-ONLY RUNTIME probe: is a hypervisor RUNNING on this host, right now?

    THE CITATION, VERBATIM. Learn, *Win32_ComputerSystem class* (Root\\CIMV2,
    CIMWin32.mof), property list:

        HypervisorPresent
          Data type: boolean
          Access type: Read-only
          Qualifiers: MappingStrings ("WMI")
        If True, a hypervisor is present.
        Windows Server 2008 R2, Windows 7, Windows Server 2008 and Windows
        Vista: This property is not supported before Windows 8 and Windows
        Server 2012.

    WHAT WAS CHECKED AND REJECTED, so the choice is reviewable rather than
    asserted (codex-CLI r9 F3 proposed the first of these):

      * `IsProcessorFeaturePresent` — Learn (*processthreadsapi.h*) enumerates
        every `PF_` constant it accepts and THERE IS NO HYPERVISOR MEMBER. The
        value 21 is `PF_VIRT_FIRMWARE_ENABLED`, documented as "Virtualization
        is enabled in the firmware and made available by the operating system"
        — a FIRMWARE capability, true on a machine running no hypervisor at
        all. Reading it as "hypervisor present" would be a second wrong number
        wearing a real API's name;
      * `CPUID.1:ECX[31]` — the hypervisor-present bit is real, but no
        documented Windows API exposes it and this module does not emit
        assembly. Unreachable, so not claimed;
      * `GetSystemInfo` / `SYSTEM_INFO` — no virtualization field on Learn.

    THE HONEST FAILURE MODE IS `None`, NEVER `False`. A host where the query
    cannot run (no PowerShell on PATH, WMI unavailable, a timeout, a reply that
    is not the shape this asked for) has an UNDETERMINED hypervisor posture, and
    "I could not tell" is a different fact from "there is none". `preflight`
    refuses to classify — and therefore to sign an environment record — on
    `None`; it never substitutes a default.

    The `vmic*` service STATE is collected in the same call because it is the
    one runtime signal that can FALSIFY a root-partition reading (integration
    services run in a Hyper-V GUEST). It is used only to refuse, never to claim
    — see `host_virtualization_facts`.
    """
    executable = shutil.which("powershell") or shutil.which("pwsh")
    facts: dict[str, Any] = {
        "probe": RUNTIME_HYPERVISOR_PROBE,
        "query": RUNTIME_VIRTUALIZATION_QUERY,
        "resolved_path": executable,
        "hypervisor_present": None,
        "guest_integration_services_running": None,
        "error": None,
    }
    if executable is None:
        facts["error"] = "RUNTIME_VIRTUALIZATION_SHELL_NOT_ON_PATH"
        return facts
    try:
        completed = subprocess.run(
            [executable, "-NoProfile", "-NonInteractive", "-Command",
             RUNTIME_VIRTUALIZATION_QUERY],
            capture_output=True, text=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        facts["error"] = f"RUNTIME_VIRTUALIZATION_PROBE_FAILED:{type(exc).__name__}:{exc}"
        return facts
    if completed.returncode != 0:
        facts["error"] = (f"RUNTIME_VIRTUALIZATION_PROBE_FAILED:exit="
                          f"{completed.returncode}:"
                          f"{(completed.stderr or '').strip()[:200]}")
        return facts
    try:
        reply = json.loads(completed.stdout)
    except ValueError as exc:
        facts["error"] = f"RUNTIME_VIRTUALIZATION_REPLY_UNPARSEABLE:{exc}"
        return facts
    if not isinstance(reply, dict) or not isinstance(
            reply.get("hypervisor_present"), bool):
        facts["error"] = "RUNTIME_VIRTUALIZATION_REPLY_OFF_CONTRACT"
        return facts
    running = reply.get("guest_integration_services_running")
    if isinstance(running, str):
        # `ConvertTo-Json` renders a one-element array as a scalar in Windows
        # PowerShell 5.1 (`-AsArray` is 6.0+), so one running service arrives as
        # a string. Normalised here rather than papered over at the reader.
        running = [running]
    facts["hypervisor_present"] = reply["hypervisor_present"]
    facts["guest_integration_services_running"] = sorted(running or [])
    return facts


def host_virtualization_facts() -> dict[str, Any]:
    """READ-ONLY host probe, with each fact labelled by the EVIDENCE THAT BACKS IT.

    codex-CLI r9 F3 (WRONG SIGNED ENVIRONMENT EVIDENCE). This function used to
    answer `hypervisor_present` from the EXISTENCE of installed-component
    registry keys and label the whole record `REGISTRY_SERVICE_PRESENCE`. Those
    keys survive the component being disabled or never having been used, so the
    record asserted a RUNTIME FACT it had only INSTALL-TIME evidence for — and
    that record is signed into the measurement envelope as the environment the
    cell ran in. Measured on the build host (2026-08-17, an ordinary bare-metal
    desktop): `Services\\vmicheartbeat` EXISTS and the service is `Stopped`.

    THE CLOSE TAKEN, per axis, because the two axes have different evidence:

      * HYPERVISOR PRESENT — a RUNTIME PROBE now decides it, and nothing else
        does: `Win32_ComputerSystem.HypervisorPresent`, quoted verbatim in
        `runtime_virtualization_facts` along with the candidates that were
        checked and rejected. `None` (UNDETERMINED) when the probe cannot run;
      * ROOT PARTITION — NO documented runtime API distinguishing a root
        partition from a guest is expressible here (the WMI class carries no
        partition field; the CPUID partition-privilege leaf is unreachable).
        So the registry evidence is recorded AS WHAT IT IS, under a name that
        says so (`hypervisor_host_components_installed`), and it is used in
        ONE direction only: it can be CONTRADICTED by the runtime fact that
        Hyper-V guest integration services are RUNNING (they run in the guest),
        which refuses the root reading. It is never promoted to a runtime
        claim, and `root_partition_determination` carries that sentence into
        the report and the environment record.

    ⚠ THE RESIDUAL, STATED RATHER THAN IMPLIED: a guest that has the Hyper-V
    host components installed AND its integration services stopped still reads
    as a root partition here. That is install-time evidence with nothing to
    contradict it, and the honest answer is that this probe cannot tell — which
    is why the determination string travels with the value instead of a bare
    boolean, and why the authorization document's operator ABORT clause remains
    the control for "am I actually inside a VM".

    The CLASSIFICATION decision is still made by
    `mbcx01_build_etw_consumer.classify_execution_environment`, which aborts on
    a guest or a nested host; this function only supplies it true inputs.
    """
    if os.name != "nt":
        raise SmokeAbort("WINDOWS_HOST_REQUIRED")
    guest_components = any(_hyperv_registry_key_exists(key)
                           for key in HYPERVISOR_GUEST_COMPONENT_KEYS)
    host_components = any(_hyperv_registry_key_exists(key)
                          for key in HYPERVISOR_HOST_COMPONENT_KEYS)
    runtime = runtime_virtualization_facts()
    running_guest_services = runtime["guest_integration_services_running"]
    contradicted = bool(running_guest_services)
    if contradicted:
        determination = "REFUSED_RUNTIME_GUEST_INTEGRATION_SERVICES_RUNNING"
    elif host_components:
        determination = "INSTALLED_COMPONENT_EVIDENCE_NOT_CONTRADICTED_AT_RUNTIME"
    else:
        determination = "NO_HOST_COMPONENTS_INSTALLED"
    # Nested virtualization is not directly readable from the guest side. It is
    # therefore reported as UNKNOWN and the operator must confirm it, which is
    # exactly what the authorization document's ABORT clause is for.
    return {"hypervisor_present": runtime["hypervisor_present"],
            "hypervisor_present_determination": (
                "UNDETERMINED" if runtime["hypervisor_present"] is None
                else "RUNTIME_FACT"),
            "hypervisor_present_probe": runtime["probe"],
            "hypervisor_present_probe_error": runtime["error"],
            "is_root_partition": bool(host_components and not contradicted),
            "root_partition_determination": determination,
            "hypervisor_host_components_installed": bool(host_components),
            "hypervisor_guest_components_installed": bool(guest_components),
            "hypervisor_guest_services_running": running_guest_services,
            "nested_virtualization_readable": False,
            "host_architecture": "WINDOWS_64BIT"
            if ctypes.sizeof(ctypes.c_void_p) == 8 else "WINDOWS_32BIT",
            "probe": "RUNTIME_WMI_HYPERVISOR_PLUS_REGISTRY_INSTALLED_COMPONENTS"}


def node_runtime_facts() -> dict[str, Any]:
    """READ-ONLY: is the `node` this run's signature verification needs THERE?

    Signature verification is not optional to this driver: both halves of the
    pass criterion route through `mbcx01_r13_measurement._invoke_signature_verifier`,
    which shells out to `node`. Elevation commonly changes PATH, so a `node` that
    resolves in the operator's ordinary shell can be missing in the elevated one —
    and the elevated session is the scarce, one-shot resource the whole runbook
    step is spent on (r6 synthesis: SEAT1 and SEAT3 each executed this failure).
    Probing it costs one `node --version` and starts nothing.
    """
    executable = shutil.which("node")
    facts: dict[str, Any] = {
        "probe": "SHUTIL_WHICH_THEN_VERSION", "requested": "node",
        "resolved_path": executable, "resolvable": executable is not None,
        "version": None, "exit_code": None, "runnable": False, "error": None}
    if executable is None:
        facts["error"] = "NODE_NOT_ON_PATH"
        return facts
    try:
        completed = subprocess.run([executable, "--version"], capture_output=True,
                                   text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        facts["error"] = f"NODE_NOT_RUNNABLE:{type(exc).__name__}:{exc}"
        return facts
    facts["exit_code"] = completed.returncode
    facts["version"] = (completed.stdout or "").strip() or None
    facts["runnable"] = completed.returncode == 0 and bool(facts["version"])
    if not facts["runnable"]:
        facts["error"] = (
            f"NODE_VERSION_PROBE_FAILED:exit={completed.returncode}:"
            f"{(completed.stderr or '').strip()[:200]}")
    return facts


def signature_verifier_facts() -> dict[str, Any]:
    """READ-ONLY: is the verifier SCRIPT node would be handed actually on disk?

    The path is read from the frozen layer (`mbcx01_r13_measurement.VERIFIER`) —
    this driver does not name it a second time, so the file probed is by
    construction the file the verifier seam will run.
    """
    path = str(measurement.VERIFIER)
    facts: dict[str, Any] = {"probe": "ISFILE_AND_DIGEST", "verifier_path": path,
                             "present": os.path.isfile(path),
                             "size_bytes": None, "sha384": None,
                             "error": None}
    if not facts["present"]:
        facts["error"] = "VERIFIER_SCRIPT_ABSENT"
        return facts
    try:
        with open(path, "rb") as stream:
            data = stream.read()
    except OSError as exc:
        facts["present"] = False
        facts["error"] = f"VERIFIER_SCRIPT_UNREADABLE:{exc}"
        return facts
    facts["size_bytes"] = len(data)
    facts["sha384"] = measurement.sha384(data)
    return facts


def preflight(authorization_path: str, *,
              operator_confirms_not_nested: bool,
              command_line: str | None = None,
              cell: tuple[int, int, int] | None = None) -> dict[str, Any]:
    """Everything that can be checked WITHOUT starting a session.

    Order is deliberate. The two static ABI checks run FIRST, because a layout
    drift must fail before anything touches the host at all. The authorization,
    elevation and environment gates run next, because they decide whether this
    process is allowed to probe the host. The `node`/verifier toolchain probe
    runs after those and BEFORE the PMU capability probe, so a toolchain gap is
    named before any capability enumeration and long before any ETW session or
    Job object could exist.

    WHEN THE CANDIDATE IS KNOWN, IT IS RESOLVED AND AUTHORIZED HERE. Given a
    `command_line` and a `cell`, this resolves the candidate image ONCE
    (`resolve_candidate_image`), checks the resolved invocation against the one
    the FIXED `SMOKE_CANDIDATE_ID` names
    (`refuse_invocation_inconsistent_with_candidate` — a wrong-record refusal,
    not a gate on the operator; see its docstring), and puts the resolved launch
    command line beside an advisory reading of the authorization document
    (`authorization_mirror`) before any host probe runs. `execute` reads both
    back out of this report, so
    the bytes that are hashed, the image that is launched and the text the
    authorization is judged against are one and the same. Called without them —
    the bare `preflight` mode of a caller that has no candidate — the two keys
    are present and `None`, and no authorization decision is claimed.
    """
    report: dict[str, Any] = {"mode": "preflight"}
    report["job_abi"] = win32.verify_struct_layout()
    report["etw_abi"] = etw.verify_etw_struct_layout()
    report["authorization"] = read_authorization(authorization_path)
    report["candidate_image"] = None
    report["authorization_mirror"] = None
    if command_line is not None:
        candidate = resolve_candidate_image(command_line)
        refuse_invocation_inconsistent_with_candidate(candidate)
        report["candidate_image"] = candidate
        if cell is not None:
            # A MIRROR, never a gate (owner ruling 2026-08-16): it reports what
            # the document says beside what will run, and decides nothing.
            report["authorization_mirror"] = authorization_mirror(
                authorization_path,
                launch_command_line=candidate["launch_command_line"], cell=cell)
    report["elevated"] = is_elevated()
    facts = host_virtualization_facts()
    report["host_virtualization_facts"] = facts
    if not operator_confirms_not_nested:
        raise SmokeAbort(
            "NESTED_VIRTUALIZATION_UNCONFIRMED: nested virtualization is "
            "unsupported and must abort (harness requirements section 1). The "
            "guest side cannot read it, so the OPERATOR must confirm it with "
            "--operator-confirms-not-nested.")
    if facts.get("hypervisor_present") is None:
        # UNDETERMINED IS NOT `False` (codex-CLI r9 F3). The environment record is
        # SIGNED into the measurement envelope, so classifying on an unanswered
        # runtime probe would put a claim in it that nothing backs — and the
        # cheapest of those claims, `BARE_METAL_WINDOWS`, is exactly the one a
        # falsy default would produce. The run stops here instead, naming the
        # probe and what it said, and nothing has been started.
        raise SmokeAbort(
            "HYPERVISOR_RUNTIME_POSTURE_UNDETERMINED: the runtime hypervisor probe "
            f"({facts.get('hypervisor_present_probe')}) could not answer "
            f"({facts.get('hypervisor_present_probe_error')}), and installed-component "
            "registry evidence is not a runtime fact. Nothing has been started; "
            "re-run once the probe can answer, or record the posture as UNDETERMINED "
            "and do not certify this cell.")
    report["environment"] = etw.classify_execution_environment(
        hypervisor_present=facts["hypervisor_present"],
        is_root_partition=facts["is_root_partition"],
        nested_virtualization=False,
        host_architecture=facts["host_architecture"])
    if not report["elevated"]:
        raise SmokeAbort(
            "ELEVATION_REQUIRED: kernel PMC needs an elevated session "
            "(smoke runbook section 3 step 2). Nothing has been started.")
    # The signature-verification toolchain, probed IN THIS (elevated) session and
    # BEFORE the capability probe — so before any ETW session or Job work could
    # start. A `node` that is unresolvable here would otherwise burn a perfect
    # one-shot elevated run at the LAST step, for a reason that has nothing to do
    # with the measurement (r6 synthesis ruling 6; SEAT1 + SEAT3, both EXECUTED).
    report["node_runtime"] = node_runtime_facts()
    report["signature_verifier"] = signature_verifier_facts()
    if not report["node_runtime"]["runnable"] or not report["signature_verifier"]["present"]:
        raise SmokeAbort(
            "SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE: both halves of the smoke "
            "pass criterion verify an Ed25519 signature through `node` and "
            f"{measurement.VERIFIER.name}, so a run that cannot reach them cannot "
            "be certified. Nothing has been started. node="
            f"{report['node_runtime']['error'] or report['node_runtime']['version']}"
            f"; verifier={report['signature_verifier']['error'] or 'PRESENT'}")
    # PMU capability probe (runbook section 3 step 1). This enumerates profile
    # sources and reads the counter grant; it starts NO session.
    consumer = etw.EtwPmcConsumer()
    consumer._win32 = etw._etw_win32()
    source_id = consumer._resolve_profile_source_id(win32.PMC_SOURCE_NAME)
    report["pmu_capability"] = etw.granted_capability_facts(
        **{**consumer._query_capability_facts(source_id),
           "profile_source_id": source_id})
    available, reasons = etw.evaluate_evidence_availability(
        capability_facts=report["pmu_capability"], loss=etw.LossCounters())
    report["pmu_available"] = available
    report["pmu_unavailable_reasons"] = list(reasons)
    return report


# --- the run --------------------------------------------------------------


def smoke_identity(*, harness_identity: dict[str, str], signing_key_id: str,
                   trust_policy_digest: str,
                   candidate_artifact_digest: str) -> producer.ProductionRunIdentity:
    return producer.ProductionRunIdentity(
        run_id=SMOKE_RUN_ID,
        candidate_id=SMOKE_CANDIDATE_ID,
        candidate_artifact_digest=candidate_artifact_digest,
        generator_digest=measurement.sha384("MBCX01.BUILD.B.SMOKE.GENERATOR"),
        harness_identity=harness_identity,
        signing_key_id=signing_key_id,
        trust_policy_digest=trust_policy_digest)


def harness_identity() -> dict[str, str]:
    """Digests of the exact harness bytes that produced this evidence.

    Not a label: each digest is taken over the file on disk, so an evidence
    consumer can bind the receipt to the collector and consumer source that
    made it (harness requirements section 5, "harness artifact/build/configuration").
    """
    def digest_of(name: str) -> str:
        with open(os.path.join(ROOT, name), "rb") as stream:
            return measurement.sha384(stream.read())

    return {
        "harness_artifact_digest": digest_of("mbcx01_build_win32.py"),
        "harness_build_digest": digest_of("mbcx01_build_etw_consumer.py"),
        "host_environment_digest": measurement.sha384(
            json.dumps({"os": sys.platform, "python": sys.version,
                        "machine": os.environ.get("PROCESSOR_ARCHITECTURE", "")},
                       sort_keys=True)),
        "harness_configuration_digest": digest_of("mbcx01_smoke_cell.py"),
    }


def external_enforcement_record() -> dict[str, Any]:
    """Supervisor-owned enforcement, recorded as OBSERVED.

    ⚠ HONEST LIMIT: the smoke cell runs `cmd.exe /c exit 0`, which performs no
    network work, but this driver does NOT install a supervisor-owned network
    denial. The record therefore states what is actually true of THIS run and
    the adapter will judge it. Harness requirements section 2 is explicit that
    "candidate-readable configuration or a constant label is not enforcement
    evidence", so this block must NOT be read as enforcement having happened.
    """
    return {
        "policy_id": "POLICY.BUILD.B.SMOKE.NO.EXTERNAL.COMPUTE",
        "policy_artifact_digest": measurement.sha384(
            "MBCX01.BUILD.B.SMOKE.EXTERNAL.POLICY"),
        "applied_before_resume": False,
        "enforcement_owner_role": "SUPERVISOR",
        "deny_outbound_network": False,
        "deny_external_compute_brokers": False,
        "deny_preexisting_helper_delegation": False,
        "external_compute_endpoint_count": 0,
        "validation_receipt_digest": measurement.sha384(
            "MBCX01.BUILD.B.SMOKE.EXTERNAL.VALIDATION.NOT.INSTALLED"),
    }


def execute(*, authorization_path: str, destination: str, command_line: str,
            cell: tuple[int, int, int], signer: Any, signing_key_id: str,
            operator_confirms_not_nested: bool) -> dict[str, Any]:
    """Runbook section 3 steps 1-6 for ONE cell.

    Ordering, which IS the evidence:

      1. preflight (static ABI, authorization marker, elevation, environment,
         PMU capability) — nothing has been started yet;
      1b. the candidate image is RESOLVED ONCE and hashed and the harness
         sources are hashed, all BEFORE anything is launched, and the values are
         held for the whole run. The receipt binds the bytes that PRODUCED the
         capture rather than whatever happens to be on disk when signing starts,
         and an unresolvable candidate aborts here rather than after an
         unrepeatable capture has been taken (codex-CLI r4 FOLD-3A/3B);
      2. the ETW session starts and the PMC counter is attached to CSwitch
         BEFORE the candidate exists, so the whole of the candidate's lifetime
         is inside the trace window;
      3. `collect()` runs the cell. It calls the live factory before
         `ResumeThread`, closes the trace window at the terminal barrier (which
         is where the consumer stops its pump, reads the loss counters and
         completes the signed rosters), then reads the deltas and the two Job
         queries;
      4. the evidence is written to the destination named in the authorization
         and NOWHERE else;
      5. the session is stopped in a `finally` so the runbook's cleanup
         obligation holds even when the collection faults.

    ⛔ NEVER RUN BY THIS BUILD. The BUILD that wrote this function ran only
    `selftest`. Everything below is reviewable code whose vendor behaviour is
    unverified until the operator's elevated run.
    """
    if os.environ.get(win32.ALLOW_PHYSICAL_ENV) != "1":
        raise SmokeAbort(
            f"{win32.ALLOW_PHYSICAL_ENV}=1 is required and this driver never "
            "sets it for you (see run-smoke-cell.ps1 -Execute).")
    report = preflight(authorization_path,
                       operator_confirms_not_nested=operator_confirms_not_nested,
                       command_line=command_line, cell=cell)
    report["mode"] = "execute"
    report["command_line"] = command_line
    report["cell"] = list(cell)
    if not report["pmu_available"]:
        raise SmokeAbort("PMU_UNAVAILABLE:" + ",".join(report["pmu_unavailable_reasons"]))
    # 1b. EVERYTHING THE ENVELOPE WILL BIND IS READ BEFORE THE LAUNCH (codex-CLI
    #     r4 FOLD-3A/3B). The candidate image was resolved ONCE and hashed by
    #     `preflight`, which also put that same resolved launch command line
    #     through the collector's authorization gate; the harness sources are
    #     hashed here. Both values are then HELD across the run and handed to the
    #     producer unchanged. Reading them after `collect()` returned — which is
    #     what this driver used to do — binds the POST-RUN bytes: an update or any
    #     other writer that touched the candidate or a harness source during the
    #     cell would be certified as the thing that produced the capture. It also
    #     means an unresolvable or unauthorized candidate aborts BEFORE an ETW
    #     session exists, instead of after an unrepeatable capture has been taken
    #     and persisted.
    candidate = report.get("candidate_image")
    if not candidate:
        raise SmokeAbort(
            "CANDIDATE_IMAGE_UNRESOLVED: preflight did not resolve the candidate "
            "image, so there is no pre-launch digest to bind and nothing here "
            "will resolve one a second time.")
    prelaunch_harness_identity = harness_identity()
    report["launch_command_line"] = candidate["launch_command_line"]
    report["prelaunch_binding"] = {
        "bound_before_launch": True,
        "harness_identity": prelaunch_harness_identity,
        "candidate_artifact_digest": candidate["candidate_artifact_digest"],
        "candidate_image_path": candidate["image_path"],
        "note": ("These digests were taken BEFORE the candidate was launched and "
                 "are the values the signed envelope carries. The launched image "
                 "is the same resolved path that was hashed."),
    }
    os.makedirs(destination, exist_ok=False)
    report["evidence_destination"] = os.path.abspath(destination)

    consumer = etw.EtwPmcConsumer()
    try:
        # `start()` ATTACHES THE COUNTER ITSELF, before the consumer opens
        # (codex-CLI r7 P1). This used to read `start(); configure_pmc()`, which
        # left a window between `ProcessTrace` starting and the counter being
        # attached: every context switch delivered in it carries no PMC item,
        # which the consumer records as ETW_PMC_EXTENDED_DATA_ABSENT and
        # `capture()` turns into a refusal of the WHOLE one-shot run.
        # `configure_pmc()` is still public and idempotent, so a runbook step
        # that calls it after this line is harmless — it just has nothing to do.
        consumer.start()
        # The factory needs nothing about the root: `collect()` sets the root
        # PID and start key on the session it receives, before it configures or
        # resumes anything, and the finalizer reads them back with
        # `session.root_identity()`.
        factory = etw.make_live_etw_session_factory(
            consumer, job_object_id=f"JOB.{cell[0]}.{cell[1]}.{cell[2]}")
        collection = win32.collect(
            # The resolved absolute image, quoted, with the candidate's own
            # arguments verbatim: what was hashed is what is launched.
            candidate["launch_command_line"], cell=cell,
            nonce=os.urandom(SMOKE_NONCE_BYTES).hex().upper(),
            external_enforcement=external_enforcement_record(),
            environment_record=report["environment"],
            pmc_source_id=consumer.source_id,
            etw_session_factory=factory,
            authorization_path=authorization_path,
            timeout_ms=60_000)
        report["collection_root_process_id"] = collection["root_process_id"]
        report["collection_trace_facts"] = collection["trace_facts"]
        # 3b. THE CAPTURE IS PERSISTED BEFORE IT IS CERTIFIED (r6 synthesis
        # ruling 6, SEAT3 F5 — EXECUTED: an unhandled post-collection
        # FileNotFoundError for `node` destroyed a successful collection). The
        # physical work is done and unrepeatable at this point; signing is a
        # separate act that can fail for reasons of its own. Writing the raw
        # capture first makes a certification failure cost the CERTIFICATE, not
        # the EVIDENCE. The files are named UNSIGNED-INCOMPLETE- on their face so
        # nothing here can be mistaken for a receipt.
        _persist_unsigned_evidence(destination, collection, report)
        envelope = producer.produce_signed_measurement_receipt_v2(
            producer.SimulatedCollection(**collection),
            signer=signer,
            identity=smoke_identity(
                # HELD from before the launch, never re-read here (FOLD-3A).
                harness_identity=prelaunch_harness_identity,
                signing_key_id=signing_key_id,
                trust_policy_digest=_fixture_trust_policy_digest(),
                candidate_artifact_digest=candidate["candidate_artifact_digest"]))
        _write_evidence(destination, collection, envelope, report)
        report["verification"] = verify_envelope(
            envelope,
            evaluation_instant=datetime.datetime.now(
                datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    finally:
        # THE CLEANUP NEVER REPLACES THE REASON THE RUN FAILED (codex-CLI r6
        # SEAT1 F5). `consumer.stop()` discharges step 5's cleanup obligation and
        # can fail on its own; raising that failure out of a `finally` that is
        # unwinding a setup or collection exception would REPLACE the primary
        # fault with the teardown fault, and the operator would read "the session
        # would not stop" for a run that actually died at the launch. The
        # collector answers this the same way at `mbcx01_build_win32.py`
        # (:940-946): the in-flight exception stays PRIMARY and the secondary is
        # ATTACHED to it. Nothing is swallowed — with nothing in flight the
        # cleanup failure IS the error and is raised unchanged.
        #
        # The in-flight exception is read BEFORE the try, because inside an
        # `except` clause `sys.exc_info()` names the exception being HANDLED
        # (the cleanup failure), not the one being unwound.
        in_flight = sys.exc_info()[1]
        try:
            loss = consumer.stop()
        except Exception as cleanup_failure:
            secondary = ("ETW_SESSION_STOP_FAILED:%s:%s"
                         % (type(cleanup_failure).__name__, cleanup_failure))
            report["cleanup"] = {"etw_session_stopped": False,
                                 "etw_session_stop_failure": secondary,
                                 "job_handles_closed_by_collector": True,
                                 "temp_artifacts_outside_destination": []}
            if in_flight is None:
                raise
            in_flight.add_note(secondary)
        else:
            report["loss_counters"] = {
                "events_lost": loss.events_lost,
                "log_buffers_lost": loss.log_buffers_lost,
                "realtime_buffers_lost": loss.realtime_buffers_lost}
            report["cleanup"] = {"etw_session_stopped": True,
                                 "job_handles_closed_by_collector": True,
                                 "temp_artifacts_outside_destination": []}
    # Step 6. The declared pass criterion is a VERDICT, not a field: a run whose
    # criterion was not met must not return a success to its caller, and `main`
    # must not print `status: OK` with exit code 0 over it. The evidence stays
    # written and the session stays stopped — this refuses to CERTIFY the run,
    # it does not discard it, and the partial report travels with the abort.
    verification = report["verification"]
    if not verification.get("pass_criterion_met"):
        raise SmokeAbort(
            "SMOKE_PASS_CRITERION_NOT_MET:" + _pass_criterion_failure(verification),
            report=report)
    return report


def _pass_criterion_failure(verification: dict[str, Any]) -> str:
    """Name which half of the pass criterion failed, rather than implying it."""
    reasons: list[str] = []
    if not verification.get("envelope_independently_valid"):
        validation = verification.get("envelope_validation") or {}
        named = (list(validation.get("structure_errors") or [])
                 + list(validation.get("evidence_errors") or [])
                 + list(validation.get("semantic_errors") or [])
                 + ["signature=%s" % validation.get("signature_note")])
        reasons.append("ENVELOPE_NOT_INDEPENDENTLY_VALID(%s)" % ",".join(named))
    if not verification.get("admission_errors"):
        reasons.append("ADMISSION_RETURNED_NO_ERRORS")
    elif not verification.get("expected_red_present"):
        reasons.append("EXPECTED_SENTINEL_ABSENT(%s)" % EXPECTED_RED_SENTINEL)
    return ";".join(reasons) if reasons else "UNSPECIFIED"


def _fixture_trust_policy_digest() -> str:
    with open(FIXTURE_MANIFEST_PATH, encoding="utf-8") as stream:
        manifest = json.load(stream)
    return manifest["roots"][0]["trust_policy_digest"]


def _split_command_line(command_line: str) -> tuple[str, str]:
    """The executable token and the REST, by the rule CreateProcessW applies.

    A command line whose first character is a double quote names its executable
    as everything up to the next double quote (spaces included); otherwise the
    executable is the first whitespace-delimited token. This mirrors the special
    first-argument handling Windows documents for CommandLineToArgvW — a
    `split()[0]` truncated a quoted path at its first space and aborted on a
    binary that CreateProcessW would have executed (codex-CLI r2 fold).

    The remainder is returned VERBATIM (leading whitespace stripped) because the
    caller rebuilds the command line around the resolved image and must not
    reinterpret the candidate's own arguments while doing so.

    ⚠ THIS SPLIT IS THE FIRST OF CreateProcessW's POSSIBILITIES, NOT ALL OF THEM
    (codex-CLI r7 P2). For an unquoted path containing a space the system tries
    SUCCESSIVE whitespace boundaries, and this returns only the first. The gap is
    not papered over here — `_unquoted_whitespace_ambiguity()` refuses by name
    exactly the command lines on which the first possibility and the system's
    full walk can name different images, so no caller of this function can
    silently certify a program the launch would not have run.
    """
    text = command_line.strip()
    if not text:
        raise SmokeAbort("CANDIDATE_COMMAND_LINE_EMPTY")
    if text.startswith('"'):
        closing = text.find('"', 1)
        if closing == -1 or closing == 1:
            raise SmokeAbort(f"CANDIDATE_COMMAND_LINE_UNPARSEABLE:{command_line!r}")
        return text[1:closing], text[closing + 1:].lstrip()
    parts = text.split(None, 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


def _executable_token(command_line: str) -> str:
    """Just the executable token (`_split_command_line`'s first half)."""
    return _split_command_line(command_line)[0]


#: The one extension `CreateProcessW` appends to an extensionless command line
#: (Learn, *CreateProcessW*, `lpCommandLine`). Lower case, because it is only
#: ever probed against a case-insensitive file system and this spelling is what
#: the resolution record shows the operator.
CREATEPROCESSW_APPENDED_EXTENSION = ".exe"

#: The extension list Windows documents as PATHEXT's value when the variable is
#: not set. Read as a DEFAULT, never as an override: the operator's elevated
#: session is the environment that decides, and it commonly differs from an
#: ordinary shell's.
#:
#: ⚠ OBSERVED, NOT APPLIED (codex-CLI r6 SEAT1 F1). PATHEXT belongs to the
#: command interpreter, not to `CreateProcessW`, so it is RECORDED in the
#: resolution report as a fact about the operator's session and is no longer
#: consulted when resolving an extensionless candidate.
DEFAULT_PATHEXT = ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC"


def _pathext() -> tuple[str, ...]:
    """PATHEXT from the environment, or the documented default when unset.

    REPORTING ONLY. Nothing in the resolution path reads this any more; it is
    kept because the operator's elevated session is the environment the run
    happened in and the report should say what it was.
    """
    raw = os.environ.get("PATHEXT") or ""
    if not raw.strip():
        raw = DEFAULT_PATHEXT
    extensions: list[str] = []
    seen: set[str] = set()
    for piece in raw.split(os.pathsep):
        text = piece.strip()
        if not text:
            continue
        if not text.startswith("."):
            text = "." + text
        if text.upper() in seen:
            continue
        seen.add(text.upper())
        extensions.append(text)
    return tuple(extensions)


def _executable_search_directories() -> tuple[str, ...]:
    """The directory sequence a bare file name is searched in, in ORDER.

    `CreateProcessW` with a NULL `lpApplicationName` documents this sequence for
    a file name that carries no directory component, and it is mirrored here
    rather than approximated by PATH alone, because this driver hands the
    RESOLVED path back to process creation — so a search that differs from
    Windows' own would silently launch a different image than Windows would have
    chosen. Quoted from Learn, *CreateProcessW*, `lpCommandLine`:

      1. The directory from which the application loaded.
      2. The current directory for the parent process.
      3. The 32-bit Windows system directory.
      4. The 16-bit Windows system directory. "There is no function that obtains
         the path of this directory, but it is searched. The name of this
         directory is System."
      5. The Windows directory.
      6. The directories that are listed in the PATH environment variable.

    STEP 4 WAS MISSING until the codex-CLI r7 documented-set close (witnesses
    bi22/bi21): the sweep that closed the extension rule enumerated five, not
    six, so a bare name living in `%SystemRoot%\\System` resolved to whatever a
    LATER directory held, or to nothing at all. Every step Learn names is here,
    and its ONE documented exclusion is honoured by not existing anywhere in
    this module: "this function does not search the per-application path
    specified by the App Paths registry key". Nothing on the RESOLUTION path
    reads a registry — this function, `_candidate_file_names` and
    `resolve_candidate_image` consult the environment and the file system and
    nothing else. (The module does open registry keys elsewhere, in the
    virtualization probe at `host_virtualization_facts`; that is a different
    question and it never reaches here.)
    """
    directories = [os.path.dirname(os.path.abspath(sys.executable)), os.getcwd()]
    system_root = os.environ.get("SystemRoot") or os.environ.get("windir")
    if system_root:
        directories.append(os.path.join(system_root, "System32"))
        directories.append(os.path.join(system_root, "System"))
        directories.append(system_root)
    directories.extend(os.environ.get("PATH", "").split(os.pathsep))
    ordered: list[str] = []
    seen: set[str] = set()
    for directory in directories:
        text = directory.strip().strip('"')
        if not text:
            continue
        key = os.path.normcase(os.path.abspath(text))
        if key in seen:
            continue
        seen.add(key)
        ordered.append(text)
    return tuple(ordered)


def _token_carries_a_path(token: str) -> bool:
    """Does this token name a DIRECTORY — the fact the `.exe` rule turns on?

    "…or if the file name contains a path, .exe is not appended" (Learn,
    *CreateProcessW*, `lpCommandLine`). A drive-relative token such as `C:tool`
    carries a path too, which is why the drive letter counts and not only a
    separator.
    """
    return bool(os.path.dirname(token) or os.path.splitdrive(token)[0])


def _candidate_file_names(token: str) -> tuple[str, ...]:
    """The file names to try for one token, in the order CreateProcessW tries them.

    THE RULE IS PATH-SENSITIVE, and that is the whole of it. Learn,
    *CreateProcessW*, `lpCommandLine`, for a NULL `lpApplicationName`:

        "If the file name does not contain an extension, .exe is appended.
         Therefore, if the file name extension is .com, this parameter must
         include the .com extension. If the file name ends in a period (.) with
         no extension, or if the file name contains a path, .exe is not
         appended."

    Three disjoint cases, one candidate each:

      * a token that already carries an extension (a trailing period counts as
        one for this purpose, and `os.path.splitext` reports it) is used AS
        GIVEN;
      * a token that carries a PATH is used AS GIVEN, extension or not; and
      * a BARE extensionless token gets `.exe` and nothing else.

    NEVER A PATHEXT WALK (codex-CLI r6 SEAT1 F1). PATHEXT is the COMMAND
    INTERPRETER's list: walking it made this function resolve, hash and CERTIFY
    a different program than the launch semantics select — with `foo.COM` and
    `foo.EXE` both in a searched directory the default PATHEXT order picked
    `foo.COM` while `CreateProcessW(NULL, "foo ...")` runs `foo.EXE`.

    AND NEVER A BARE FALLBACK (codex-CLI r7 P1 — the r6 fold's own NEIGHBOUR).
    That fold applied the append UNIFORMLY, `(token + ".exe", token)`, which
    broke the path clause in both directions on the same day it closed the
    PATHEXT one:

      * `C:\\dir\\tool` requested with `C:\\dir\\tool.exe` on disk resolved,
        hashed and certified `tool.exe` while the launch runs `tool` — a WRONG
        NUMBER in a signed receipt; and
      * a bare `witness` with only an extensionless `witness` in a searched
        directory resolved THAT, certifying an image
        `CreateProcessW(NULL, "witness ...")` never looks for and therefore
        never launches.

    An extensionless image reached BY PATH is still supported — it is a real
    file and Windows really does run it — but it is reached the way Windows
    reaches it: named with its directory, verbatim. Witnesses bi19/bi21.
    """
    if os.path.splitext(token)[1] or _token_carries_a_path(token):
        return (token,)
    return (token + CREATEPROCESSW_APPENDED_EXTENSION,)


#: The named refusal for the ONE documented resolution rule this driver does not
#: implement: the successive-whitespace interpretation of an UNQUOTED path
#: containing a space (Learn, *CreateProcessW*, `lpApplicationName`).
UNQUOTED_SPACE_PATH_UNSUPPORTED = "SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED"


def _whitespace_extended_prefixes(command_line: str) -> tuple[str, ...]:
    """The LONGER executable names `CreateProcessW` tries after the first token.

    Learn, *CreateProcessW*, `lpApplicationName`, for
    `c:\\program files\\sub dir\\program name`: the system "tries to interpret the
    possibilities in the following order: c:\\program.exe,
    c:\\program files\\sub.exe, c:\\program files\\sub dir\\program.exe,
    c:\\program files\\sub dir\\program name.exe".

    Those possibilities are the whitespace-delimited PREFIXES of the command
    line. This returns them in that order with the FIRST one dropped, because the
    first is the token `_split_command_line` already answered.
    """
    text = command_line.strip()
    prefixes: list[str] = []
    index = 0
    while index < len(text):
        if text[index].isspace():
            if text[:index] and text[:index] not in prefixes:
                prefixes.append(text[:index])
            while index < len(text) and text[index].isspace():
                index += 1
            continue
        index += 1
    if text and text not in prefixes:
        prefixes.append(text)
    return tuple(prefixes[1:])


def _extended_prefix_naming_a_file(command_line: str) -> str | None:
    """The first whitespace-extended prefix that NAMES AN EXISTING FILE, or None.

    THE EXISTENCE CHECK IS THE WHOLE GUARD, and it has to be, because
    `_token_carries_a_path` alone answers YES for prefixes that are not paths at
    all: `ntpath.dirname("cmd /c")` is `"cmd "`, so the runbook's own
    `cmd /c exit 0` looks path-carrying at its second boundary. It is not a file,
    so it is not a possibility, so nothing is refused. Only a prefix that really
    is on disk means Windows has somewhere else to go.

    `.exe` is appended as a second candidate for the same reason the
    `lpApplicationName` enumeration does: every possibility it lists ends `.exe`.
    """
    for prefix in _whitespace_extended_prefixes(command_line):
        if not _token_carries_a_path(prefix):
            continue
        for name in (prefix, prefix + CREATEPROCESSW_APPENDED_EXTENSION):
            if os.path.isfile(name):
                return name
    return None


def _unquoted_whitespace_ambiguity(command_line: str, token: str,
                                   remainder: str, *,
                                   resolved: str | None) -> str | None:
    """The refusal sentence when our reading and Windows' can name DIFFERENT files.

    Returns None — no refusal — for every command line on which the two readings
    must agree, which is the point: a guard that swallowed the runbook's own
    `cmd.exe /c exit 0` would be a worse defect than the one it closes.

    THE THREE CONDITIONS, all required, each doing work:

    1. THE COMMAND LINE IS UNQUOTED. A quoted executable is unambiguous by
       Microsoft's own instruction — "use quoted strings to indicate where the
       file name ends and the arguments begin" — so there is nothing to refuse.
    2. THERE IS A LATER WHITESPACE BOUNDARY. With no arguments there is no
       second possibility for Windows to try; the first interpretation is the
       only one.
    3. THE TOKEN CARRIES A PATH, **OR A LATER BOUNDARY FORMS ONE THAT EXISTS**.
       The documented ambiguity is about "a long file name that contains a
       space", and every possibility Learn enumerates is a longer PATH.

       ⚠ THE r7 FOLD READ THAT AS A PROPERTY OF THE FIRST TOKEN, AND IT IS NOT
       (codex-CLI r8 P2). `tools dir\\app.exe --arg` splits to `tools`, which
       carries no path — so the check above returned "nothing to refuse" and the
       operator got `CANDIDATE_BINARY_NOT_FOUND:'tools'` for a command line
       `CreateProcessW` launches perfectly well at its SECOND boundary. The
       ambiguity is a property of the COMMAND LINE, not of its first word: an
       unquoted RELATIVE spaced path has a pathless first token by construction,
       which is exactly the shape the first reading of this rule could not see.
       `_extended_prefix_naming_a_file()` now asks the question the rule actually
       poses — is there a later whitespace boundary that names a file Windows
       would go on to try? — and only a prefix that EXISTS counts.

       A bare name with no such prefix still has no directory to grow into:
       extending it would produce a file name containing a space in a searched
       directory, which is not the operator's meaning, and
       `CANDIDATE_BINARY_NOT_FOUND` stays the honest answer there (witness bi16).

    And then one of two things has to be true for the readings to diverge:

      (a) OUR FIRST POSSIBILITY DID NOT RESOLVE, so Windows would go on to the
          next boundary and could launch an image this function never hashed.
          `C:\\dir\\A B\\tool.exe --arg` is that shape: pre-r7 it aborted
          `CANDIDATE_BINARY_NOT_FOUND:'C:\\dir\\A'` — a generic not-found for a
          command line Windows launches perfectly well.
      (b) OUR FIRST POSSIBILITY RESOLVED, but the two Learn paragraphs disagree
          about WHICH file it is. `lpCommandLine` says `.exe` is not appended to
          a name containing a path; the `lpApplicationName` enumeration appends
          `.exe` to each whitespace prefix (`c:\\program.exe`). That only matters
          when the token is extensionless AND a sibling `.exe` exists — then the
          two readings name two different programs, and picking one to hash and
          certify is exactly the wrong number `resolve_candidate_image` exists to
          make impossible.

    A resolved token with no `.exe` sibling is the case both readings answer the
    same way, and it is answered, not refused.
    """
    if command_line.strip().startswith('"'):
        return None
    if not remainder:
        return None
    if not _token_carries_a_path(token):
        # A pathless first token that RESOLVED is the first possibility Windows
        # tries and accepts, so the readings agree and there is nothing to refuse.
        if resolved is not None:
            return None
        extended = _extended_prefix_naming_a_file(command_line)
        if extended is None:
            return None
        return (
            f"{UNQUOTED_SPACE_PATH_UNSUPPORTED}:{token!r} did not resolve and the "
            f"command line is unquoted, but the later whitespace boundary "
            f"{extended!r} names a file that exists - CreateProcessW would go on "
            "to try it and could launch an image this preflight never hashed. "
            "QUOTE the executable path in the authorization document and re-run: "
            '"<full path>" <arguments>.')
    if resolved is None:
        return (
            f"{UNQUOTED_SPACE_PATH_UNSUPPORTED}:{token!r} did not resolve and the "
            "command line is unquoted, so CreateProcessW would go on to try the "
            "next whitespace boundary and could launch an image this preflight "
            "never hashed. QUOTE the executable path in the authorization "
            "document and re-run: \"<full path>\" <arguments>.")
    if (not os.path.splitext(token)[1]
            and os.path.isfile(token + CREATEPROCESSW_APPENDED_EXTENSION)):
        return (
            f"{UNQUOTED_SPACE_PATH_UNSUPPORTED}:{token!r} is extensionless, an "
            f"{token + CREATEPROCESSW_APPENDED_EXTENSION!r} also exists, and the "
            "command line is unquoted - the two documented readings of "
            "CreateProcessW name DIFFERENT programs here, so neither may be "
            "hashed and certified as the one that ran. QUOTE the executable "
            "path in the authorization document and re-run.")
    return None


def resolve_candidate_image(command_line: str) -> dict[str, Any]:
    """Resolve the candidate image ONCE, hash it, and say how to launch it.

    THE HASHED IMAGE AND THE LAUNCHED IMAGE ARE THE SAME FILE. The returned
    `launch_command_line` names the resolved absolute path (quoted) followed by
    the candidate's own arguments verbatim, so `CreateProcessW(NULL, ...)` has
    nothing left to search for and cannot pick a different image than the one
    this function read. Two defects close on that single fact:

      * the digest bound into the receipt is taken BEFORE the candidate is
        launched, by a caller that holds it across the run (codex-CLI r4
        FOLD-3A); and
      * an extensionless command such as `cmd /c exit 0` — which Windows
        launches perfectly well by appending an extension — is RESOLVED rather
        than refused, so a completed, unrepeatable capture is not lost at the
        certification step to a resolution mismatch (FOLD-3B). On the one-shot
        elevated session that refusal costs the whole run.

    THE RESOLUTION RULE IS `CreateProcessW`'s, NOT THE SHELL'S (codex-CLI r6
    SEAT1 F1): a BARE extensionless token gets `.exe` appended, a token carrying
    a path is used verbatim, and PATHEXT is never walked
    (`_candidate_file_names`). The `pathext` field below is therefore an
    OBSERVATION of the operator's session, not an input to the answer above it.

    THE ONE DOCUMENTED RULE THIS FUNCTION REFUSES INSTEAD OF IMPLEMENTING
    (codex-CLI r7 P2). An UNQUOTED long file name containing a space is
    ambiguous, and Learn (*CreateProcessW*, `lpApplicationName`) enumerates the
    interpretations for `c:\\program files\\sub dir\\program name`:

        1. c:\\program.exe   2. c:\\program files\\sub.exe
        3. c:\\program files\\sub dir\\program.exe
        4. c:\\program files\\sub dir\\program name.exe

    This driver models the FIRST possibility and stops. Implementing the walk
    would be machinery: the harness writes its own command lines, the
    authorization document quotes them, and the documented FIX is one character
    — "use quoted strings to indicate where the file name ends and the arguments
    begin". So the shapes where our answer and Windows' can DIFFER are refused
    BY NAME, as `SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED`, and the refusal says to
    quote. It is scoped so it can never eat a command line that works — see
    `_unquoted_whitespace_ambiguity()`. Witnesses bi20/bi21.

    ⚠ HONEST LIMIT. This narrows the window between hashing and launching; it
    does not close it. The file is read, not held under a deny-write share, so a
    replacement in the microseconds between this read and `CreateProcessW` would
    still be unbound. That is a measurement instrument's residual, recorded here
    rather than implied: the pre-fold window was the ENTIRE run, this one is the
    interval between two adjacent statements in `execute`.
    """
    token, remainder = _split_command_line(command_line)
    names = _candidate_file_names(token)
    image: str | None = None
    if _token_carries_a_path(token):
        # A name carrying a directory component is NOT searched for: Windows
        # resolves it against the current directory and nothing else.
        directories: tuple[str, ...] = ()
        for name in names:
            if os.path.isfile(name):
                image = os.path.abspath(name)
                break
    else:
        directories = _executable_search_directories()
        for directory in directories:
            for name in names:
                probe = os.path.join(directory, name)
                if os.path.isfile(probe):
                    image = os.path.abspath(probe)
                    break
            if image is not None:
                break
    ambiguity = _unquoted_whitespace_ambiguity(command_line, token, remainder,
                                               resolved=image)
    if ambiguity is not None:
        raise SmokeAbort(ambiguity)
    if image is None:
        raise SmokeAbort(f"CANDIDATE_BINARY_NOT_FOUND:{token!r}")
    with open(image, "rb") as stream:
        data = stream.read()
    # THE COMMAND LINE IS ONLY REWRITTEN WHEN REWRITING CHANGES SOMETHING. A
    # command line that already names the resolved image as an unambiguous
    # absolute path is passed through VERBATIM, because the collector's
    # authorization gate searches the authorization document for the exact text
    # it is about to run: re-quoting a fully specified command line would turn an
    # authorized run into a refusal on the one-shot elevated session.
    quoted = command_line.strip().startswith('"')
    already_exact = (os.path.isabs(token)
                     and os.path.normcase(token) == os.path.normcase(image)
                     and (quoted or not any(character.isspace()
                                            for character in token)))
    if already_exact:
        launch = command_line.strip()
    else:
        launch = '"%s"' % image + ((" " + remainder) if remainder else "")
    return {
        "requested_command_line": command_line,
        "executable_token": token,
        "image_path": image,
        "launch_command_line": launch,
        "launch_command_line_rewritten": not already_exact,
        "candidate_artifact_digest": measurement.sha384(data),
        "image_size_bytes": len(data),
        "resolution": "DIRECTORY_COMPONENT" if not directories else "SEARCHED",
        "attempted_file_names": list(names),
        "search_directories": list(directories),
        "pathext": list(_pathext()),
    }


def refuse_invocation_inconsistent_with_candidate(candidate: dict[str, Any]) -> None:
    """The resolved invocation must be the one `SMOKE_CANDIDATE_ID` NAMES.

    codex-CLI r9 F4. `smoke_identity()` signs a FIXED candidate id,
    `CANDIDATE.BUILD.B.SMOKE.CMD-EXIT-0`, with an artifact digest taken over the
    IMAGE only. A supported non-default `--command-line` — `cmd.exe /c whoami`
    is the smallest example — therefore produced an envelope certifying a
    DIFFERENT invocation under that same fixed identity, with a digest that
    could not tell the two apart because both run the same `cmd.exe` bytes. Two
    receipts, one identity, different work: the wrong number an evidence
    consumer cannot see.

    ⚖ WHAT THIS IS AND IS NOT (owner ruling 2026-08-16, and the reason
    `authorization_mirror` stopped deciding anything). This refuses a WRONG
    RECORD, never a person. It does not ask who is running, does not read the
    authorization document, and does not second-guess the operator's right to
    run anything: it says only that THIS driver has ONE candidate id and that
    an invocation which is not that candidate cannot be certified as it. The
    other close — minting a fresh candidate id and artifact digest per command
    line — is new machinery (identity derivation, a digest that covers
    arguments, a manifest that knows about both) and is not built here.

    The comparison is deliberately narrow, so it cannot eat an invocation that
    IS this candidate: the image by BASE NAME (`cmd.exe` is resolved out of the
    session's search path, so the absolute path differs by host), the arguments
    with runs of whitespace collapsed, both case-insensitively — `cmd /c exit
    0`, `cmd.exe /c exit 0`, `"C:\\WINDOWS\\System32\\cmd.exe" /c exit 0` and
    `C:\\WINDOWS\\System32\\cmd.exe /C EXIT 0` are all the same invocation and
    all pass.
    """
    image_name = os.path.basename(candidate["image_path"])
    _token, arguments = _split_command_line(candidate["requested_command_line"])
    arguments = " ".join(arguments.split())
    mismatches: list[str] = []
    if image_name.casefold() != SMOKE_CANDIDATE_IMAGE_NAME.casefold():
        mismatches.append("image=%r (declared %r)"
                          % (image_name, SMOKE_CANDIDATE_IMAGE_NAME))
    if arguments.casefold() != SMOKE_CANDIDATE_ARGUMENTS.casefold():
        mismatches.append("arguments=%r (declared %r)"
                          % (arguments, SMOKE_CANDIDATE_ARGUMENTS))
    if mismatches:
        raise SmokeAbort(
            f"{SMOKE_COMMAND_INCONSISTENT}:{SMOKE_CANDIDATE_ID} is a FIXED "
            f"candidate identity and names the invocation "
            f"{SMOKE_CANDIDATE_COMMAND_LINE!r}; the resolved invocation "
            f"{candidate['launch_command_line']!r} differs in "
            + "; ".join(mismatches)
            + ". Signing it under this id would certify work the id does not "
              "name. Run the declared candidate, or add a candidate identity "
              "for the invocation you want measured.")


def _candidate_digest(command_line: str) -> str:
    """SHA-384 of the candidate BINARY, not of its command line.

    The command line is a label; the artifact digest has to bind the bytes that
    executed, so the executable is read from disk. If it cannot be located the
    run ABORTS rather than substituting a digest of the string. The location is
    `resolve_candidate_image`'s and no other: one resolution, used for both the
    hash and the launch.
    """
    return resolve_candidate_image(command_line)["candidate_artifact_digest"]


#: Every pre-certification artifact carries this prefix. It is not decoration:
#: these files exist BECAUSE signing may not have happened, so the name has to
#: say so on disk, without a reader having to open anything or consult a report.
UNSIGNED_EVIDENCE_PREFIX = "UNSIGNED-INCOMPLETE-"


def _write_artifact(destination: str, name: str, data: Any) -> str:
    """Write one evidence artifact into the destination and NOWHERE else."""
    path = os.path.join(destination, name)
    if isinstance(data, (bytes, bytearray)):
        with open(path, "wb") as stream:
            stream.write(data)
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(data, indent=2, sort_keys=True, default=str))
            stream.write("\n")
    return path


def _collection_transcript(collection: dict[str, Any]) -> dict[str, Any]:
    """The collection minus the raw buffers, which are written as their own files."""
    return {key: value for key, value in collection.items()
            if not isinstance(value, (bytes, bytearray))}


def _persist_unsigned_evidence(destination: str, collection: dict[str, Any],
                               report: dict[str, Any]) -> None:
    """Write the RAW capture before the signer is invoked (r6 fold, SEAT3 F5).

    ⚠ WHAT THESE FILES ARE NOT. They are not a receipt, not a measurement, and
    not admissible as either: nothing here is signed, no digest here is bound to
    a trust root, and the envelope that would carry that binding does not exist
    yet. They are the unrepeatable physical capture, kept so that a failure of
    the CERTIFICATION step (which shells out to `node`, which can be missing,
    which is exactly what SEAT3 executed) costs the certificate rather than the
    evidence. The signed artifacts are written afterwards, alongside these, by
    `_write_evidence`; these are never deleted, because a reader comparing the
    two is a reader who can see what signing added.
    """
    readme = {
        "signed": False,
        "certified": False,
        "what_this_is": (
            "The RAW physical capture, written to disk BEFORE the signer ran. "
            "The collection is unrepeatable; the signature is not. These files "
            "exist so a post-collection certification failure cannot destroy the "
            "capture."),
        "what_this_is_not": (
            "NOT a measurement receipt and NOT admissible evidence. Nothing here "
            "is signed and nothing here is bound to a trust root. If "
            "signed-envelope.json is absent from this directory, this run was "
            "never certified and its numbers must not be reported as a "
            "measurement."),
        "run_id": SMOKE_RUN_ID,
        "candidate_id": SMOKE_CANDIDATE_ID,
        "evidence_kind": "FIXTURE_SMOKE_ONE_CELL",
    }
    written = [
        _write_artifact(destination, UNSIGNED_EVIDENCE_PREFIX + "basic-and-io-raw.bin",
                        collection["basic_and_io_raw_bytes"]),
        _write_artifact(destination, UNSIGNED_EVIDENCE_PREFIX + "extended-limit-raw.bin",
                        collection["extended_limit_raw_bytes"]),
        _write_artifact(destination,
                        UNSIGNED_EVIDENCE_PREFIX + "collection-transcript.json",
                        _collection_transcript(collection)),
        _write_artifact(destination, UNSIGNED_EVIDENCE_PREFIX + "README.json", readme),
    ]
    report["unsigned_evidence_written"] = written
    report["unsigned_evidence_note"] = readme["what_this_is_not"]


def _write_evidence(destination: str, collection: dict[str, Any],
                    envelope: dict[str, Any], report: dict[str, Any]) -> None:
    """Runbook section 3 step 3: the destination and NOWHERE else.

    The raw 96/144-byte Job query buffers are written as their own files as
    well as travelling base64 inside the envelope, because the harness
    requirements call for "raw returned bytes and raw-result digest" and a
    reviewer should be able to hash the buffer without parsing an envelope.

    These are the CERTIFIED artifacts. The `UNSIGNED-INCOMPLETE-` copies of the
    same raw buffers were written before the signer ran and stay where they are.
    """
    def write(name: str, data: Any) -> str:
        return _write_artifact(destination, name, data)

    written = [
        write("basic-and-io-raw.bin", collection["basic_and_io_raw_bytes"]),
        write("extended-limit-raw.bin", collection["extended_limit_raw_bytes"]),
        write("signed-envelope.json", envelope),
        write("collection-transcript.json", _collection_transcript(collection)),
    ]
    report["evidence_written"] = written
    report["envelope_digests"] = {
        "receipt_digest": envelope["receipt_digest"],
        "subject_digest": envelope["subject_digest"],
        "environment_digest": envelope["environment_digest"]}


def _evidence_section_errors(receipt: Any) -> set[str]:
    """Are the evidence sections the producer must write actually THERE?

    PRESENCE AND SHAPE ONLY, judged against the frozen key sets
    (`mbcx01_r13_measurement.RECEIPT_KEYS` / `JOB_KEYS` / `EVIDENCE_KEYS` /
    `QUERY_BUNDLE_KEYS` / `HARNESS_IDENTITY_KEYS`), which is a different
    question from grid admission. A smoke run is ONE cell at an operator-chosen
    coordinate, so the coverage, coordinate, affordability and gate checks in
    `mbcx01_build_measurement_authority._receipt_errors` are deliberately NOT
    applied here: those are what the honest production refusal is FOR, and
    borrowing them would turn "this is not a 100-cell production grid" into
    "the collector produced nothing", which is a different and false statement.
    """
    if not isinstance(receipt, dict) or set(receipt) != measurement.RECEIPT_KEYS:
        return {"RECEIPT_SECTION_ABSENT"}
    job = receipt.get("job_receipt")
    if not isinstance(job, dict) or set(job) != measurement.JOB_KEYS:
        return {"JOB_RECEIPT_SECTION_ABSENT"}
    evidence = job.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != measurement.EVIDENCE_KEYS:
        return {"EVIDENCE_SECTION_ABSENT"}
    errors: set[str] = set()
    identity = evidence.get("harness_identity")
    if (not isinstance(identity, dict)
            or set(identity) != measurement.HARNESS_IDENTITY_KEYS
            or not all(identity[name] for name in sorted(identity))):
        errors.add("HARNESS_IDENTITY_EVIDENCE_ABSENT")
    membership = evidence.get("process_membership")
    processes = membership.get("processes") if isinstance(membership, dict) else None
    if (not isinstance(membership, dict)
            or set(membership) != measurement.MEMBERSHIP_KEYS
            or not isinstance(processes, list) or not processes):
        errors.add("PROCESS_MEMBERSHIP_EVIDENCE_ABSENT")
    queries = evidence.get("job_queries")
    if not isinstance(queries, dict) or set(queries) != measurement.QUERY_BUNDLE_KEYS:
        errors.add("JOB_QUERY_EVIDENCE_ABSENT")
    else:
        for name in sorted(queries):
            row = queries[name]
            if (not isinstance(row, dict) or set(row) != measurement.QUERY_KEYS
                    or not row.get("raw_bytes_b64") or not row.get("raw_bytes_sha384")):
                errors.add("JOB_QUERY_EVIDENCE_ABSENT")
    trace = evidence.get("trace")
    if not isinstance(trace, dict) or set(trace) != measurement.TRACE_KEYS:
        errors.add("TRACE_EVIDENCE_ABSENT")
    for section, keys in (("environment", measurement.ENVIRONMENT_KEYS),
                          ("completion", measurement.COMPLETION_KEYS),
                          ("external_enforcement", measurement.EXTERNAL_KEYS)):
        block = evidence.get(section)
        if not isinstance(block, dict) or set(block) != keys:
            errors.add(f"{section.upper()}_EVIDENCE_ABSENT")
    return errors


#: Codes the FULL production per-receipt validator raises for reasons that are
#: GRID or PRODUCTION-ADMISSION questions rather than statements about what this
#: collector produced. They are held NOT-APPLICABLE for a one-cell fixture smoke
#: run — BY NAME, and RECORDED in the report under `semantic_not_applicable`, so
#: a reviewer reads exactly what was set aside instead of finding a silent gap.
#:
#: EXTERNAL_WORK_UNMEASURED is the only member. `_validate_physical_evidence`
#: requires a SUPERVISOR-INSTALLED denial (`applied_before_resume: True`,
#: `deny_outbound_network: True`, ...); `external_enforcement_record()` above
#: states on its own face that this driver installs no such denial and that the
#: block "must NOT be read as enforcement having happened". The refusal is
#: therefore TRUE of the production obligation and says nothing whatsoever about
#: the capture — and making it fatal here would make the smoke pass criterion
#: unreachable by construction, which is the same defect wearing the other sign.
SMOKE_NOT_APPLICABLE_RECEIPT_CODES = frozenset({"EXTERNAL_WORK_UNMEASURED"})

#: A REGISTERED grid coordinate, substituted ONLY so the production validator's
#: grid-registration test (`H/D/F in H_VALUES/D_VALUES/F_VALUES`) has something
#: to accept for a cell the OPERATOR chose. The runbook's own default is
#: `--cell 0,0,0`, which is not a registered coordinate; that test short-circuits
#: the whole validator with MEASUREMENT_SCHEMA_INVALID, so subtracting the code
#: afterwards would silently disable every semantic check for exactly the
#: invocation the runbook publishes. The substitution is made on a SHALLOW copy —
#: the evidence tree judged is the receipt's own object, nothing is rebuilt,
#: nothing is written back — and the real coordinate is reported unchanged.
SMOKE_COORDINATE_PROBE = (measurement.H_VALUES[0], measurement.D_VALUES[0],
                          measurement.F_VALUES[0])


def _semantic_receipt_errors(receipt: Any) -> dict[str, Any]:
    """Judge the receipt's SEMANTICS with the harness's own full validator.

    NOTHING IS REIMPLEMENTED HERE. `_evidence_section_errors` above asks only
    whether the evidence sections are PRESENT and correctly SHAPED, which two
    council seats independently executed past: each re-signed a receipt whose
    structure, digests, preimage and signature were impeccable and whose CONTENT
    was false (`process_membership.membership_complete` flipped to False; a
    perturbed `retired_instructions`), and the smoke criterion passed both while
    `mbcx01_build_measurement_authority._receipt_errors` — the validator this
    repository already owns — refused them by name (r6 synthesis, ruling 6).

    So that validator is CALLED. What is excluded is named above and recorded in
    the returned dict; everything else it says is fatal to the smoke criterion.
    """
    registered = (isinstance(receipt, dict)
                  and receipt.get("H") in measurement.H_VALUES
                  and receipt.get("D") in measurement.D_VALUES
                  and receipt.get("F") in measurement.F_VALUES)
    subject = receipt
    if isinstance(receipt, dict) and not registered:
        subject = dict(receipt)
        subject["H"], subject["D"], subject["F"] = SMOKE_COORDINATE_PROBE
    fault: str | None = None
    try:
        raised = set(authority._receipt_errors(subject)[0])
    except (KeyError, TypeError, ValueError, AttributeError, IndexError,
            OverflowError) as exc:
        # Could not judge is not judged. It never becomes a pass — the same
        # posture `evaluate_production_measurement` takes over malformed input.
        raised = {"MEASUREMENT_SEMANTIC_VALIDATION_FAULT"}
        fault = f"{type(exc).__name__}:{exc}"
    return {
        "validator": "mbcx01_build_measurement_authority._receipt_errors",
        "errors": sorted(raised - SMOKE_NOT_APPLICABLE_RECEIPT_CODES),
        "not_applicable": sorted(raised & SMOKE_NOT_APPLICABLE_RECEIPT_CODES),
        "coordinate_registered": bool(registered),
        "coordinate_probe": None if registered else list(SMOKE_COORDINATE_PROBE),
        "fault": fault,
    }


def validate_produced_envelope(envelope: Any, *,
                               roots: dict[str, dict[str, Any]] | None) -> dict[str, Any]:
    """Judge the produced envelope on its OWN merits, independently of admission.

    WHY THIS EXISTS. `evaluate_production_measurement` reaches its trust and
    custody gate FIRST and returns there: the smoke manifest is
    `production_ready:false` with no custody evidence, so the refusal below is
    reached without the envelope ever being read. `verify_envelope({})` therefore
    produced exactly the same honest sentinel as a real receipt would. An honest
    red about NOTHING is not the runbook's pass criterion — section 3 step 4
    requires a STRUCTURALLY VALID SIGNED envelope that admission then refuses —
    so structure, signature and evidence are judged HERE, before that refusal is
    allowed to count as a pass.

    Nothing is rebuilt: the closed key set, schema/domain/version/algorithm
    identity, run and cell identity, producer role and fixture kind against the
    root, nonce shape, subject/environment digests, the V2 timing cross-check
    and the signature carrier/preimage are all judged by the production
    authority's own per-envelope validator; the receipt's SEMANTICS are judged by
    that authority's own per-receipt validator (`_semantic_receipt_errors`, r6
    fold — presence and shape were not enough, two seats executed past them); and
    the signature itself is checked with the SAME Node verifier seam admission
    uses, against the public half of the fixture root named in the manifest.
    """
    validation: dict[str, Any] = {
        "structure_errors": [], "evidence_errors": [], "semantic_errors": [],
        "semantic_not_applicable": [], "semantic_coordinate_registered": False,
        "semantic_coordinate_probe": None, "semantic_validation_fault": None,
        "semantic_validator": None,
        "signature_verified": False, "signature_note": "NOT_ATTEMPTED",
        "valid": False}
    if roots is None:
        # The manifest itself did not validate, so there is no root to judge the
        # envelope against. That is a refusal to certify, never a pass.
        validation["structure_errors"] = ["TRUST_ROOT_MANIFEST_UNVALIDATED"]
        validation["evidence_errors"] = ["TRUST_ROOT_MANIFEST_UNVALIDATED"]
        validation["semantic_errors"] = ["TRUST_ROOT_MANIFEST_UNVALIDATED"]
        return validation
    structure_errors, receipt, signature_candidate = authority._envelope_errors(
        envelope, SMOKE_RUN_ID, roots, None)
    validation["structure_errors"] = sorted(structure_errors)
    validation["evidence_errors"] = sorted(_evidence_section_errors(receipt))
    semantic = _semantic_receipt_errors(receipt)
    validation["semantic_errors"] = semantic["errors"]
    validation["semantic_not_applicable"] = semantic["not_applicable"]
    validation["semantic_coordinate_registered"] = semantic["coordinate_registered"]
    validation["semantic_coordinate_probe"] = semantic["coordinate_probe"]
    validation["semantic_validation_fault"] = semantic["fault"]
    validation["semantic_validator"] = semantic["validator"]
    root = roots.get(envelope.get("signing_key_id")) if isinstance(envelope, dict) else None
    if not signature_candidate or root is None:
        validation["signature_note"] = "NOT_A_SIGNATURE_CANDIDATE"
    else:
        try:
            validation["signature_verified"] = measurement._invoke_signature_verifier(
                [{"payload_b64": envelope["receipt_preimage_b64"],
                  "public_key_pem": root["public_key_pem"],
                  "signature_b64": envelope["signature_b64"]}])[0]
            validation["signature_note"] = (
                "VERIFIED" if validation["signature_verified"] else "REFUSED")
        except (ValueError, KeyError, TypeError) as exc:
            # Could not verify is not verified. It never becomes a pass.
            validation["signature_note"] = f"VERIFIER_UNAVAILABLE:{exc}"
    validation["valid"] = bool(not validation["structure_errors"]
                               and not validation["evidence_errors"]
                               and not validation["semantic_errors"]
                               and validation["signature_verified"])
    return validation


def verify_envelope(envelope: dict[str, Any], *,
                    evaluation_instant: str) -> dict[str, Any]:
    """Runbook section 3 step 4, with the REAL instant, expecting the honest RED.

    The deterministic default `evaluation_instant` exists for suite
    reproducibility and is NOT a production freshness check, so it is passed
    explicitly here. The fixture manifest is `production_ready:false` and no
    production anchor is wired, so the expected outcome is a REFUSAL naming
    `PHYSICAL_HARNESS_UNAVAILABLE`.

    THAT RED IS THE PASS CRITERION ONLY FOR A VALID ENVELOPE. The refusal is
    reached at the trust/custody gate, before the envelope is examined, so it
    says nothing whatsoever about what was produced. The criterion is therefore
    the CONJUNCTION: the envelope is independently valid (structure, signature,
    evidence presence AND receipt semantics — `validate_produced_envelope`) AND
    admission refuses it with the expected sentinel. An empty or malformed
    envelope fails the first half, and so does a re-signed one whose content is
    false.
    """
    with open(FIXTURE_MANIFEST_PATH, encoding="utf-8") as stream:
        manifest = json.load(stream)
    result: dict[str, Any] = {"evaluation_instant": evaluation_instant,
                              "manifest_path": FIXTURE_MANIFEST_PATH}
    roots: dict[str, dict[str, Any]] | None
    try:
        roots = authority.validate_production_trust_root_manifest(
            manifest, evaluation_instant=evaluation_instant)
        result["manifest_roots_fixture_only"] = sorted(
            {bool(row["fixture_only"]) for row in roots.values()})
        result["manifest_validation"] = "PARSED"
    except authority.MeasurementAuthorityError as exc:
        roots = None
        result["manifest_validation"] = f"REFUSED:{exc}"
    validation = validate_produced_envelope(envelope, roots=roots)
    result["envelope_validation"] = validation
    result["envelope_independently_valid"] = bool(validation["valid"])
    errors = authority.evaluate_production_measurement(
        [envelope], trust_root_manifest=manifest, custody_evidence={},
        expected_run_id=SMOKE_RUN_ID)
    result["admission_errors"] = errors
    result["expected_red_present"] = EXPECTED_RED_SENTINEL in errors
    result["pass_criterion_met"] = bool(
        result["envelope_independently_valid"] and errors
        and result["expected_red_present"])
    result["note"] = (
        "An EMPTY error list here would be a DEFECT, not a success: a smoke "
        "run is fixture-kind evidence and can never clear production admission. "
        "An empty or malformed envelope is equally a DEFECT: the refusal is "
        "reached before the envelope is read, so the honest red only counts as "
        "a pass for an envelope this driver independently validated.")
    return result


# --- selftest -------------------------------------------------------------


def selftest() -> dict[str, Any]:
    """Exercise the pure layer and both static ABI checks. Touches no OS state.

    This is the ONLY mode the BUILD that wrote this file ever ran. It proves
    the wiring is present and self-consistent; it proves NOTHING about vendor
    behaviour (see `mbcx01_build_etw_consumer`'s module docstring).
    """
    report: dict[str, Any] = {"mode": "selftest"}
    report["job_abi"] = win32.verify_struct_layout()
    report["etw_abi"] = etw.verify_etw_struct_layout()
    blob = etw.classic_event_id_blob()
    report["cswitch_attachment_blob_hex"] = blob.hex()
    report["cswitch_attachment_is_zero_filled"] = blob == b"\x00" * len(blob)
    capture = etw.CapturedTrace(
        cswitch_records=[
            {"processor": 1, "qpc": 25, "old_thread_id": 900,
             "instruction_retired": 2500},
            {"processor": 0, "qpc": 12, "old_thread_id": 900,
             "instruction_retired": 1000},
            {"processor": 0, "qpc": 20, "old_thread_id": 900,
             "instruction_retired": 1700}],
        process_events=[
            {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
             "parent_process_id": None, "parent_process_start_key": None, "qpc": 10},
            {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
             "parent_process_id": 4100, "parent_process_start_key": 0x11, "qpc": 13},
            {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22, "qpc": 27},
            {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11, "qpc": 30}],
        thread_events=[
            {"kind": "START", "thread_id": 900, "process_id": 4100,
             "process_start_key": 0x11, "qpc": 11},
            {"kind": "STOP", "thread_id": 900, "process_id": 4100,
             "process_start_key": 0x11, "qpc": 29}],
        capability_facts=etw.granted_capability_facts_for_test(),
        loss=etw.LossCounters(0, 0, 0), session_handle=0, source_id=0)
    session = etw.make_etw_session_factory(
        capture, job_object_id="JOB.0.0.0", root_process_id=4100,
        root_process_start_key="0000000000000011")()
    observations = session.consume_cswitch()
    report["members"] = session.members()
    report["records_reordered"] = capture.reordered_record_count
    report["observations"] = observations
    report["attributed_retired_instructions"] = sum(
        row["delta_from_previous"] for row in observations)
    report["trace_facts"] = win32._trace_facts(session)
    report["frozen_shape_checks"] = {
        "capability_query": set(session.capability) == measurement.CAPABILITY_QUERY_KEYS,
        "event_attachment": set(session.attachment) == measurement.EVENT_ATTACHMENT_KEYS,
        "process_keys": all(set(row) == measurement.PROCESS_KEYS
                            for row in session.members()),
        "thread_keys": all(set(row) == measurement.THREAD_LIFETIME_KEYS
                           for row in session.thread_lifetimes),
        "cswitch_keys": all(set(row) == measurement.CSWITCH_OBSERVATION_KEYS
                            for row in observations),
        "trace_fact_fields": set(report["trace_facts"]) == set(
            producer.TRACE_FACT_FIELDS),
    }
    # The UNAVAILABLE posture, demonstrated rather than asserted.
    capture.loss = etw.LossCounters(events_lost=1)
    try:
        etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        report["loss_posture"] = "DEFECT: a lossy capture built a session"
    except etw.EtwConsumerFault as fault:
        report["loss_posture"] = str(fault)
    return report


def load_fixture_signer(pem_path: str | None,
                        key_id: str | None) -> tuple[Any, str]:
    """Build the FIXTURE signer from a key the OPERATOR supplies.

    No key material lives in this module or in the consumer, mirroring
    `FixtureSigner`'s own rule ("The private key is always injected by the
    caller; no key material is embedded in this module"). `FixtureSigner`
    additionally refuses any key id that is not a test id, so a production key
    cannot be routed through here even by mistake — which is the point: a smoke
    run is fixture-kind evidence and can never clear production admission.
    """
    if not pem_path or not key_id:
        raise SmokeAbort(
            "FIXTURE_SIGNING_KEY_REQUIRED: pass --fixture-signing-key-pem and "
            "--fixture-signing-key-id. This driver embeds no key material and "
            "will not invent one. Runbook section 3 step 1: fixture signing key ONLY.")
    if not os.path.isfile(pem_path):
        raise SmokeAbort(f"FIXTURE_SIGNING_KEY_NOT_FOUND:{pem_path!r}")
    with open(pem_path, encoding="utf-8") as stream:
        pem = stream.read()
    try:
        return producer.FixtureSigner(key_id, pem, fixture_only=True), key_id
    except ValueError as exc:
        raise SmokeAbort(f"FIXTURE_SIGNING_KEY_REFUSED:{exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("selftest", "preflight", "execute"))
    parser.add_argument("--authorization", default=None)
    parser.add_argument("--destination", default=None)
    parser.add_argument("--command-line", default="cmd.exe /c exit 0")
    parser.add_argument("--cell", default="0,0,0")
    parser.add_argument("--operator-confirms-not-nested", action="store_true")
    parser.add_argument(
        "--fixture-signing-key-pem", default=None,
        help="path to the FIXTURE PKCS#8 Ed25519 private key that signs the "
             "smoke envelope. Required for `execute`. A smoke run is "
             "fixture-kind evidence by definition (runbook 3.1) and can NEVER "
             "clear production admission, so a production key must never be "
             "supplied here — FixtureSigner refuses a non-test key id anyway.")
    parser.add_argument(
        "--fixture-signing-key-id", default=None,
        help="the key id matching --fixture-signing-key-pem. Must contain "
             "'.TEST.' or end with '.TEST'.")
    parser.add_argument("--report", default=None,
                        help="write the JSON report here (default: stdout only)")
    args = parser.parse_args(argv)
    instant = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    try:
        if args.mode == "selftest":
            report = selftest()
        elif args.mode == "preflight":
            # The candidate and cell are passed even here: the whole value of a
            # preflight is that it says what the elevated session will say, and
            # the mirror reports both, and decides nothing (see authorization_mirror
            # for why the verdict there is ADVISORY without the physical flag).
            report = preflight(
                args.authorization,
                operator_confirms_not_nested=args.operator_confirms_not_nested,
                command_line=args.command_line,
                cell=tuple(int(part) for part in args.cell.split(",")))
        else:
            cell = tuple(int(part) for part in args.cell.split(","))
            signer, key_id = load_fixture_signer(
                args.fixture_signing_key_pem, args.fixture_signing_key_id)
            report = execute(
                authorization_path=args.authorization,
                destination=args.destination, command_line=args.command_line,
                cell=cell, signer=signer, signing_key_id=key_id,
                operator_confirms_not_nested=args.operator_confirms_not_nested)
        report["status"] = "OK"
        code = 0
    except (SmokeAbort, etw.EtwConsumerFault, win32.CollectorFault,
            win32.PhysicalCollectionNotAuthorized) as fault:
        report = {"mode": args.mode, "status": "ABORT", "reason": str(fault),
                  "note": "An abort for an unsupported environment or an "
                          "unbuilt step is a legitimate, recordable outcome."}
        partial = getattr(fault, "report", None)
        if isinstance(partial, dict):
            report["partial_report"] = partial
        code = 2
    except Exception:  # pragma: no cover - operator diagnostics
        report = {"mode": args.mode, "status": "FAULT",
                  "traceback": traceback.format_exc()}
        code = 3
    report["generated_at"] = instant
    text = json.dumps(report, indent=2, sort_keys=True, default=str)
    print(text)
    if args.report:
        with open(args.report, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
