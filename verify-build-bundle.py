"""Deterministic, no-provider verifier for the MBCX-01 production BUILD lane.

Mirrors `verify-r13-normative-bundle.py` in discipline and adds what the BUILD lane
owes on top of it:

  1. the five FROZEN r13.2 suites run and must total exactly FROZEN_TEST_TOTAL OK (the
     constant below carries the count and the dated reason for every move since the
     145-test freeze) — the BUILD lane is additive or it is nothing;
  2. the three BUILD suites run (state, measurement, integration);
  3. two-way totality between `MBCX-01-BUILD-REPAIR-LEDGER.json` and the BUILD witness
     namespace, by INTROSPECTING the unittest test names actually executed: every
     declared witness must exist and have passed, every discovered witness must appear
     in exactly one ledger row, no row may be empty, and a row that declares no
     positive/adversarial witness must name an existing row that carries it;
  3b. REGISTRATION TOTALITY at four levels (W14, added 2026-08-16 with the cohort
     slice): the `mbcx01_build_*.py` / `test_mbcx01_build_*.py` globs and the
     registration tuples must agree in BOTH directions; every REQUIRED artifact must
     be registered for pinning and pinned (a not-yet-committed artifact is reported by
     name, decided by git, never by a list) and every subject pinned BEYOND `REQUIRED`
     must be named in `PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED`; the governed artifact
     namespace is derived from the UNION OF THE REGISTRATION LISTS and every member is
     on disk; and
     every `BUILD_MODULES` entry is named by a repair-ledger row that states a
     behaviour and carries a witness. Three cohort modules and an eighteen-witness
     suite once landed with none of these lists noticing — that is the failure this
     arm exists to make impossible;
  4. strict Draft 2020-12 compilation of the two BUILD schemas plus validation of their
     committed fixture instances and rejection of every mutant
     (`verify-build-schema-ajv.mjs`, vendored AJV);
  5. Python/Node canonicalization parity over committed documents
     (`verify-build-canonical-parity.mjs`);
  6. a FRESH `MBCX-01-BUILD-VERIFICATION-REPORT.json` emitted at runtime.

Before ANY of that is reported as passing, `MBCX-01-BUILD-PIN-MANIFEST.json` is
reconciled against the bytes this run is actually about. Counting 150 frozen tests proves
nothing about WHICH bytes ran: a frozen subject can be edited without adding or removing a
test, and before this arm existed the report certified the run anyway. The reconciliation
is two git-level checks, both loud, and neither hashes the working tree — this repository
is checked out with `core.autocrlf=true` while the manifest records LF blob identities, so
hashing working-tree files would fail on every CRLF checkout and would say nothing about
drift:

  a. STALENESS vs HEAD — every manifest subject is resolved as `HEAD:<path>` out of the
     object store and its blob id, byte count, LF count, line count and SHA-384 must equal
     what the manifest recorded. A manifest whose governing commit is behind a commit that
     changed a pinned subject fails BY NAME, subject by subject.
  b. UNCOMMITTED DRIFT — `git status --porcelain` restricted to the manifest subjects. Any
     dirty subject fails BY NAME; the pinned bytes are not what is on disk.

git is REQUIRED for both. If git cannot be executed, or this tree is not the repository
root, the arm FAILS as UNVERIFIABLE — it never skips quietly. The one mode that does not
reconcile is the pinned RECONSTRUCTION (`verify-build-pinned.ps1 -Commit/-ManifestBlob`),
which runs this verifier in a temporary directory that is not a work tree at all and whose
bytes the launcher has already authenticated blob by blob against the manifest. That mode
is NAMED in the report with `reconciliation_performed:false`, so a reader can always see
which of the two proofs is carrying the weight.

The report is a RUNTIME OUTPUT. No copy of it is committed: a stale report on disk is
an assertion nobody re-ran, and this lane has already ruled that a report which is not
the output of the run it describes is not evidence. `--output-report` writes it where
the caller asks; stdout always carries it.

Execution posture, enforced rather than claimed while this verifier runs:
  * in-process network calls are blocked (a call raises and fails the run);
  * every spawned process is recorded, and only an enumerated EXECUTABLE SET is
    permitted — this interpreter, the local `node` verifier/signer, `git` for the
    pin reconciliation, and `pwsh` for bw86's launcher-refusal witness. The fence
    claims the executable set and nothing more: it does not adjudicate the
    ARGUMENTS those executables were given (r8 ruling; the reasoning and the
    named residual live at `ExecutionPosture.check`);
  * the physical-collection gate must be unauthorized (env flag absent);
  * every committed trust-root manifest must be `production_ready:false`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FROZEN_TEST_MODULES = (
    "test_mbcx01_r13_state",
    "test_mbcx01_r13_packets",
    "test_mbcx01_r13_measurement",
    "test_mbcx01_r13_inference",
    "test_mbcx01_r13_integration",
)
# 145 at the r13.2 freeze; 147 since AMENDMENT-1 (2026-08-15, owner-ruled), which binds
# subject_id and owner_role into the canonical world and adds its two red witnesses;
# 150 since AMENDMENT-2 (2026-08-15, owner-ruled), which makes a thread's identity its
# TID *and* its interval in the frozen physical-evidence validator — a reused TID now
# carries one lifetime per use, every observation is resolved by QPC containment, and a
# thread lifetime must nest inside the process incarnation whose start key it claims.
# Its three witnesses are test_i11_adversarial_thread_lifetime_outside_its_process_is_refused,
# test_i11_positive_a_reused_thread_id_carries_one_lifetime_per_use and
# test_i11_adversarial_overlapping_lifetimes_for_one_thread_id_are_refused.
# See MBCX-01-R13-AMENDMENT-1-CANONICAL-WORLD-BINDING-2026-08-15.md and
# MBCX-01-R13-AMENDMENT-2-THREAD-IDENTITY-AND-PEM-TRANSPORT-2026-08-15.md. Raising this
# number is how a frozen-layer change is DECLARED; it is not routine maintenance.
# 150 -> 155, AMENDMENT-3 (2026-08-16, owner ratification pending at the merge
# gate): the first member CSwitch interval per processor is counted from a
# predecessor baseline (trace field cswitch_first_member_baselines) instead of
# a hard-coded zero delta — the r6 NO-GO signed 100 retired instructions where
# the stream proved 1,000,100. Five witnesses, test_i12_* "baseline" family in
# test_mbcx01_r13_measurement.py.
# See MBCX-01-R13-AMENDMENT-3-FIRST-MEMBER-INTERVAL-BASELINE-2026-08-16.md.
# 155 -> 156, r7 fold (2026-08-16): the totality rule — baselined processors
# must EQUAL observed processors; the empty-but-forgotten baseline set that
# three r7 seats executed (SEAT2 end-to-end, wrong by 1,000,000) is now
# unrepresentable, witnessed by the new test_i12 empty-set adversarial.
FROZEN_TEST_TOTAL = 156

BUILD_TEST_MODULES = (
    "test_mbcx01_build_state",
    "test_mbcx01_build_measurement",
    "test_mbcx01_build_integration",
    # 2026-08-16, cohort registration task: the BUILD cohort slice's witnesses
    # (design MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md r6 FINAL §3 "Registration").
    # There is no BUILD-suite TOTAL constant to move — `check_build_suites`
    # compares the number of tests RUN against the number DISCOVERED, so the suite
    # grows by registration alone and a silently-skipped witness still fails.
    "test_mbcx01_build_cohort",
)

BUILD_MODULES = (
    # 2026-08-16, cohort registration task: the three cohort siblings (design §2).
    "mbcx01_build_cohort_authority.py",
    "mbcx01_build_cohort_generator.py",
    "mbcx01_build_cohort_packet.py",
    "mbcx01_build_etw_consumer.py",
    "mbcx01_build_exactness_authority.py",
    "mbcx01_build_measurement_authority.py",
    "mbcx01_build_state_adapter.py",
    "mbcx01_build_state_authority.py",
    "mbcx01_build_state_operator_b.py",
    "mbcx01_build_state_store.py",
    "mbcx01_build_trust_anchor.py",
    "mbcx01_build_win32.py",
    "mbcx01_build_windows_producer.py",
)

#: FIXTURE-ONLY support for the witness suites (holds a committed test key and is
#: imported by no production authority module), plus the committed fixture anchor
#: document and the BUILD-side strict Ed25519 verifier.
#:
#: `mbcx01_build_integration.py` is listed HERE and not in `BUILD_MODULES` (r2 fold,
#: codex F3's packaging point): it imports the witness modules and the ceremony fixture,
#: assembles simulated evidence, and produces no admission decision of its own — it is a
#: fixture ASSEMBLER. Calling it a production module was the label that let it install
#: process-wide authority and look like part of the production graph.
BUILD_FIXTURE_SUPPORT = (
    "mbcx01_build_ceremony_fixture.py",
    "mbcx01_build_integration.py",
    "MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json",
    "verify-build-receipt-signature.mjs",
)

#: RED-WITNESS PROBE scripts. 2026-08-16, cohort registration task: this list is
#: NEW, and it exists because W14 level (a) is a TWO-WAY glob check — every
#: `mbcx01_build_*.py` on disk must be named by a registration list and every listed
#: module must be on disk. These three files matched the glob and were named by NO
#: list, which is precisely the "unregistered-and-unnoticed" hazard design §3
#: level (c) names. They are neither production authorities (`BUILD_MODULES`) nor
#: witness-suite support (`BUILD_FIXTURE_SUPPORT`): each is a standalone EVIDENCE
#: script written against a pre-fix public API so the identical file runs against a
#: reconstruction of the pre-fix bytes and against this tree. They are pinned
#: (`$buildSubjects`) and imported by nothing.
BUILD_RED_WITNESS_PROBES = (
    "mbcx01_build_fixtureiso_probe.py",
    "mbcx01_build_fixturekey_probe.py",
    "mbcx01_build_trustboot_probe.py",
)

OWNER_TRUST_ANCHOR_FIXTURE = "MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json"

BUILD_SCHEMA_PAIRS = (
    ("MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json",
     "MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json"),
    ("MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json",
     "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json"),
)

BUILD_WORK_PRODUCTS = (
    # 2026-08-16, cohort registration task: the cohort slice's design of record.
    "MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md",
    "MBCX-01-BUILD-DESIGN-NOTES.md",
    "MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md",
    "MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md",
    "MBCX-01-BUILD-SHELF-LOG.md",
    "MBCX-01-BUILD-SMOKE-RUNBOOK.md",
)

#: The committed BUILD cohort generator spec (design §3). 2026-08-16: it is listed
#: as its own constant rather than folded into `BUILD_WORK_PRODUCTS` because it is
#: not a document — it is READ AS AUTHORITY at runtime by
#: `mbcx01_build_cohort_authority.load_build_cohort_spec`, and its canonical
#: serialization is checked by the parity arm below (it joins `PARITY_DOCUMENTS`).
BUILD_COHORT_SPEC_ARTIFACT = "MBCX-01-BUILD-COHORT-GENERATOR-V1.json"

LEDGER = "MBCX-01-BUILD-REPAIR-LEDGER.json"
#: The pin manifest is deliberately NOT in `REQUIRED`: it is not one of its own subjects
#: (the launcher pins it by Git blob), so it is absent from a pinned reconstruction by
#: construction. `reconcile_pin_manifest` decides what its absence means, positively.
PIN_MANIFEST = "MBCX-01-BUILD-PIN-MANIFEST.json"
PIN_MANIFEST_ID = "MBCX-01-BUILD-PIN-MANIFEST"

#: Distinct named reconciliation failures. Each names ONE mode; none is a warning.
PIN_GIT_UNAVAILABLE = "PIN_MANIFEST_GIT_UNAVAILABLE"
PIN_NOT_REPOSITORY_ROOT = "PIN_MANIFEST_ROOT_IS_NOT_THE_REPOSITORY_ROOT"
PIN_MANIFEST_ABSENT = "PIN_MANIFEST_ABSENT_FROM_THE_WORK_TREE"
PIN_RECONSTRUCTION_MISMATCH = "PIN_MANIFEST_RECONSTRUCTION_BYTES_MISMATCH"
PIN_UNVERIFIABLE_POSTURE = "PIN_MANIFEST_ABSENT_OUTSIDE_A_GIT_WORK_TREE"
PIN_MANIFEST_SHAPE_INVALID = "PIN_MANIFEST_SHAPE_INVALID"
PIN_GOVERNING_COMMIT_UNRESOLVED = "PIN_MANIFEST_GOVERNING_COMMIT_UNRESOLVED"
PIN_GOVERNING_COMMIT_NOT_ANCESTOR = "PIN_MANIFEST_GOVERNING_COMMIT_NOT_AN_ANCESTOR_OF_HEAD"
PIN_SUBJECT_ABSENT_AT_HEAD = "PIN_MANIFEST_SUBJECT_ABSENT_AT_HEAD"
PIN_STALE_AT_HEAD = "PIN_MANIFEST_STALE_AT_HEAD"
PIN_UNCOMMITTED_DRIFT = "PIN_MANIFEST_SUBJECT_HAS_UNCOMMITTED_DRIFT"

REPORT_ID = "MBCX-01-BUILD-LIVE-NO-PAID-VERIFICATION"
GENERATED_REPORT = "MBCX-01-BUILD-VERIFICATION-REPORT.json"
SCHEMA_VERIFIER = "verify-build-schema-ajv.mjs"
PARITY_VERIFIER = "verify-build-canonical-parity.mjs"

REQUIRED = (
    *BUILD_MODULES,
    *BUILD_FIXTURE_SUPPORT,
    *BUILD_RED_WITNESS_PROBES,
    *(name + ".py" for name in BUILD_TEST_MODULES),
    *(name for pair in BUILD_SCHEMA_PAIRS for name in pair),
    *BUILD_WORK_PRODUCTS,
    BUILD_COHORT_SPEC_ARTIFACT,
    LEDGER,
    "verify-build-bundle.py", SCHEMA_VERIFIER, PARITY_VERIFIER,
    "verify-build-pinned.ps1", "generate-build-pin-manifest.ps1",
    "verify-r13-receipt-signature.mjs", "vendor/ajv-r12.bundle.cjs",
    "MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json",
    "MBCX-01-R13-REPAIR-LEDGER.json", "verify-r13-normative-bundle.py",
)

#: Documents the Python/Node canonicalization parity check hashes. Committed artifacts
#: only, so the check is deterministic and needs no fixture assembly. Receipt-level
#: parity over live signed artifacts is witness bi04.
PARITY_DOCUMENTS = (
    LEDGER,
    # 2026-08-16, cohort registration task: the spec artifact is canonical JSON that
    # a Python authority hashes at runtime, so Python/Node canonicalization parity
    # over it is exactly the claim this arm exists to make.
    BUILD_COHORT_SPEC_ARTIFACT,
    "MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json",
    "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json",
    "MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json",
    "MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json",
)

#: The parity claim is scoped to the value domain the BUILD receipts actually use:
#: objects, arrays, strings, booleans, null and exactly-representable integers. Python
#: `repr` and ECMAScript number-to-string are DIFFERENT specifications, so a float is
#: outside the claim — and the helper must REFUSE it rather than quietly hash it. This
#: committed document carries float planning diagnostics and is the control that proves
#: the refusal is real: a parity checker that silently accepted it would be asserting a
#: parity nobody verified.
PARITY_REFUSAL_CONTROL = "MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json"

#: The governed BUILD witness-id shape: `<test module>.<class>.test_b<ns><nn>_...`.
#:
#: 2026-08-16, cohort registration task — RECORDED PREFIX WIDENING, `b[aiw]` ->
#: `b[aiwc]`, per design §3 ("`WITNESS_ID` prefix widening (recorded)").  The three
#: existing namespaces are `ba` (state), `bw` (measurement) and `bi` (integration).
#: The number field is TWO DIGITS and that is a hard ceiling: `bw` had reached bw93
#: with only bw23/bw64 free below it, so the cohort suite's first eighteen witnesses
#: had to take the six remaining fresh numbers (bw94-bw99) plus MODULE-QUALIFIED
#: REUSES (bw70-bw79, legitimate because the id is `<module>.<class>.<method>` and
#: the bundle already reuses bw80-bw84 across two modules).  Continuing that way
#: would have spent the last of `bw` and made every future cohort witness a reuse,
#: which reads as a collision to anyone grepping a bare witness number.  `bc` =
#: BUILD-COHORT: a fresh namespace with its own 00-99 field.  This widens what the
#: regex ADMITS; it removes no check — every name outside the class still fails
#: `discover_witnesses` by name.
WITNESS_ID = re.compile(r"^test_mbcx01_build_[a-z]+\.[A-Za-z0-9_]+\.test_b[aiwc]\d{2}_")


class VerificationFailure(AssertionError):
    """A named BUILD verification failure. Never downgraded to a warning."""


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed: set[str] = set()

    def addSuccess(self, test):  # noqa: N802
        super().addSuccess(test)
        self.passed.add(test.id())


class ExecutionPosture:
    """Block in-process network calls and record every spawned process."""

    def __init__(self) -> None:
        self.spawned: list[list[str]] = []
        self._saved: dict = {}

    def __enter__(self) -> "ExecutionPosture":
        self._saved = {
            "run": subprocess.run,
            "connect": socket.socket.connect,
            "create_connection": socket.create_connection,
            "getaddrinfo": socket.getaddrinfo,
        }
        real_run = self._saved["run"]

        def watched_run(args, *rest, **kwargs):
            self.spawned.append([str(item) for item in args]
                               if isinstance(args, (list, tuple)) else [str(args)])
            return real_run(args, *rest, **kwargs)

        def refuse(*_args, **_kwargs):
            raise VerificationFailure("network call attempted during BUILD verification")

        subprocess.run = watched_run
        socket.socket.connect = refuse
        socket.create_connection = refuse
        socket.getaddrinfo = refuse
        return self

    def __exit__(self, *_exc) -> None:
        subprocess.run = self._saved["run"]
        socket.socket.connect = self._saved["connect"]
        socket.create_connection = self._saved["create_connection"]
        socket.getaddrinfo = self._saved["getaddrinfo"]

    def check(self) -> dict:
        # `git` is permitted because the pin-manifest reconciliation reads the object
        # store through it. It is a local, read-only query of this repository; the
        # network block above stays in force for it like everything else.
        # `node.exe` joins bare `node` the same way `git.exe` joins `git`: the r6
        # preflight probe resolves node via shutil.which, so on Windows the
        # spawned basename carries the extension. Same binary, same permission.
        # `pwsh` is permitted because bw86's launcher-refusal witness runs the
        # real `run-smoke-cell.ps1` in a System32-only PATH to prove it aborts
        # at the toolchain gate, pre-elevation, creating nothing.
        #
        # ⚖ WHAT THIS FENCE CLAIMS, r8 ruling (TAR-PIT triage run ON THE FENCE
        # ITSELF, matrix row THEATER → accept the residual, name it, zero
        # grind). This fence enumerates the EXECUTABLES a verification run may
        # spawn. It does NOT adjudicate what those executables were told to do.
        # r7 tried to: it pinned the pwsh ARGV SHAPE with a regex, r8 seats
        # immediately produced a script-identity bypass and a trailing-command
        # bypass, and the next round would have produced two more — the space
        # of PowerShell payload strings is UNBOUNDED, so a coverage claim over
        # it is falsifiable forever (TAR-PIT Lessons 9-11: a census is a
        # flashlight, not a fence; harvest it and delete it unless the space it
        # must cover is finite). The EXECUTABLE SET is finite and derivable, so
        # that is the claim this fence makes and the only one.
        #
        # NAMED RESIDUAL, in-model and accepted: a future test that spawns pwsh
        # to do something unrelated is enumerated, not distinguished. Reaching
        # it takes a maintainer editing our own suite — this lane's design of
        # record carries no threat model, and nothing here ships. What the
        # launcher actually did under bw86 is bw86's OWN assertion, where a
        # behavioural probe can fail; it was never this fence's to prove.
        # `powershell`/`powershell.exe` is permitted because bi24's runtime-environment
        # guard executes the real Win32_ComputerSystem.HypervisorPresent probe — a
        # local, read-only WMI query (codex r9 fold, 2026-08-17). The network block
        # above stays in force for it like everything else; no paid call, no spend.
        permitted = {"git", "git.exe", "node", "node.exe", "pwsh", "pwsh.exe",
                     "powershell", "powershell.exe",
                     os.path.basename(sys.executable).lower()}
        for command in self.spawned:
            name = os.path.basename(command[0]).lower()
            if name not in permitted:
                raise VerificationFailure("unexpected spawned process: %r" % (command,))
        return {"spawned_processes": len(self.spawned),
                "permitted_executables": sorted(permitted),
                "claim": "EXECUTABLE_SET_ONLY_ARGUMENTS_NOT_ADJUDICATED"}


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def require_artifacts() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise VerificationFailure("missing BUILD artifacts: " + ", ".join(missing))
    if (ROOT / GENERATED_REPORT).exists():
        raise VerificationFailure(
            "%s is a RUNTIME OUTPUT and must not be committed or left on disk before "
            "the run that produces it" % GENERATED_REPORT)


def _git(*arguments: str, cwd: Path, stdin: bytes | None = None) -> tuple[int, bytes, str]:
    """Run one local git query and return `(returncode, stdout_bytes, stderr_text)`.

    git is REQUIRED. A verifier that cannot run it cannot reconcile the pin manifest, and
    "could not check" must never look like "checked and clean", so an unrunnable git is a
    loud failure here rather than a skipped arm.
    """
    try:
        result = subprocess.run(["git", *arguments], cwd=str(cwd), input=stdin,
                                capture_output=True, check=False)
    except OSError as exc:
        raise VerificationFailure(
            "%s: git could not be executed (%s); %s cannot be reconciled against the "
            "current bytes, so this run is UNVERIFIABLE"
            % (PIN_GIT_UNAVAILABLE, exc, PIN_MANIFEST)) from exc
    return result.returncode, result.stdout, result.stderr.decode("utf-8", "replace")


def _head_blobs(paths, *, root: Path) -> dict[str, tuple[str, bytes] | None]:
    """`HEAD:<path>` -> (blob id, blob BYTES) for each path, or `None` when absent.

    One `git cat-file --batch` call. The bytes come out of the object store, so they are
    the committed LF bytes whatever this checkout's line endings are.
    """
    request = "".join("HEAD:%s\n" % path for path in paths).encode("utf-8")
    code, out, err = _git("cat-file", "--batch", cwd=root, stdin=request)
    if code != 0:
        raise VerificationFailure(
            "%s: git cat-file --batch failed (%s)" % (PIN_GIT_UNAVAILABLE, err.strip()))
    resolved: dict[str, tuple[str, bytes] | None] = {}
    offset = 0
    for path in paths:
        end = out.find(b"\n", offset)
        if end < 0:
            raise VerificationFailure(
                "%s: truncated git cat-file --batch response at %s"
                % (PIN_GIT_UNAVAILABLE, path))
        header = out[offset:end].decode("utf-8", "replace").split()
        offset = end + 1
        if len(header) >= 2 and header[-1] == "missing":
            resolved[path] = None
            continue
        if len(header) != 3 or header[1] != "blob" or not header[2].isdigit():
            raise VerificationFailure(
                "%s: unreadable git cat-file --batch header for %s: %r"
                % (PIN_GIT_UNAVAILABLE, path, " ".join(header)))
        size = int(header[2])
        content = out[offset:offset + size]
        if len(content) != size:
            raise VerificationFailure(
                "%s: truncated blob for %s" % (PIN_GIT_UNAVAILABLE, path))
        offset += size + 1  # the trailing LF git writes after each blob
        resolved[path] = (header[0], content)
    return resolved


def _pin_row_mismatches(row: dict, blob_id: str, content: bytes) -> list[str]:
    """Every recorded identity of one pinned subject that HEAD's bytes contradict."""
    lf_count = content.count(b"\n")
    lines = 0 if not content else (lf_count if content.endswith(b"\n") else lf_count + 1)
    actual = {
        "git_blob": blob_id,
        "bytes": len(content),
        "lf_count": lf_count,
        "lines": lines,
        "sha384": hashlib.sha384(content).hexdigest().upper(),
    }
    mismatched = []
    for field, value in sorted(actual.items()):
        recorded = row.get(field)
        if isinstance(recorded, str) and isinstance(value, str):
            if recorded.upper() != value.upper():
                mismatched.append("%s recorded=%s head=%s" % (field, recorded, value))
        elif recorded != value:
            mismatched.append("%s recorded=%r head=%r" % (field, recorded, value))
    return mismatched


def reconcile_pin_manifest(root: Path = ROOT) -> dict:
    """Reconcile `MBCX-01-BUILD-PIN-MANIFEST.json` against the bytes this run is about.

    Two loud checks, neither of which hashes the working tree (see the module docstring
    on `core.autocrlf`): staleness of the recorded identities against `HEAD`, and
    uncommitted drift of any manifest subject. Both modes are reported by name, together,
    so one run tells the whole truth about the tree it just verified.
    """
    manifest_path = root / PIN_MANIFEST
    code, out, _err = _git("rev-parse", "--is-inside-work-tree", cwd=root)
    inside_work_tree = code == 0 and out.decode("utf-8", "replace").strip() == "true"

    if not inside_work_tree:
        # The pinned RECONSTRUCTION: `verify-build-pinned.ps1` exports every subject's
        # raw object-store bytes into a temporary directory AND writes the authenticated
        # manifest beside them (its line 52). There is no git history here to compare
        # against, but the files ARE raw LF blob bytes (no autocrlf smudge happens on an
        # export), so the manifest reconciles at the byte level: length, LF count, line
        # count and SHA-384 per subject. `git_blob` is the one identity this mode cannot
        # check, and the report says so instead of implying it.
        if not manifest_path.exists():
            # No git history AND no manifest: nothing in this layout can be reconciled
            # against anything, and nothing attests that any launcher authenticated it.
            # A legitimate pinned reconstruction ALWAYS carries the manifest
            # (verify-build-pinned.ps1 exports it beside the subjects), so this posture
            # has no legitimate caller — and the branch that used to PASS here claimed
            # launcher authentication that may never have happened. Could-not-check must
            # never read as checked-and-clean.
            raise VerificationFailure(
                "%s: %s is not inside a Git work tree and carries no %s; there is "
                "nothing to reconcile the pinned subject set against and nothing "
                "attests this layout was authenticated. Run from the repository, or "
                "through verify-build-pinned.ps1, which exports the manifest beside "
                "the subjects it authenticates."
                % (PIN_UNVERIFIABLE_POSTURE, root, PIN_MANIFEST))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rows = (list(manifest.get("subjects") or [])
                + list(manifest.get("frozen_dependencies") or []))
        if (manifest.get("manifest_id") != PIN_MANIFEST_ID or not rows
                or any(not isinstance(row.get("path"), str) for row in rows)):
            raise VerificationFailure(
                "%s: %s is not a readable pin manifest (manifest_id or subject rows)"
                % (PIN_MANIFEST_SHAPE_INVALID, PIN_MANIFEST))
        mismatched: list[str] = []
        for row in rows:
            subject = root / row["path"]
            if not subject.is_file():
                mismatched.append("%s (absent from the reconstruction)" % row["path"])
                continue
            content = subject.read_bytes()
            lf_count = content.count(b"\n")
            lines = 0 if not content else (
                lf_count if content.endswith(b"\n") else lf_count + 1)
            wrong = [
                name for name, recorded, found in (
                    ("bytes", row.get("bytes"), len(content)),
                    ("lf_count", row.get("lf_count"), lf_count),
                    ("lines", row.get("lines"), lines),
                    ("sha384", str(row.get("sha384", "")).upper(),
                     hashlib.sha384(content).hexdigest().upper()),
                ) if recorded != found]
            if wrong:
                mismatched.append("%s (%s)" % (row["path"], ", ".join(wrong)))
        if mismatched:
            raise VerificationFailure(
                "%s: reconstructed subject bytes differ from %s: %s"
                % (PIN_RECONSTRUCTION_MISMATCH, PIN_MANIFEST,
                   "; ".join(sorted(mismatched))))
        return {"status": "PASS", "mode": "PINNED_RECONSTRUCTION_BYTE_RECONCILED",
                "reconciliation_performed": True,
                "pin_manifest_present": True,
                "subjects_reconciled": len(rows),
                "identities_checked": ["bytes", "lf_count", "lines", "sha384"],
                "identities_not_checkable_here": ["git_blob"]}

    prefix = _git("rev-parse", "--show-prefix", cwd=root)[1].decode("utf-8", "replace").strip()
    if prefix:
        raise VerificationFailure(
            "%s: this verifier is at '%s' inside the repository, but every pinned subject "
            "path is repository-root relative" % (PIN_NOT_REPOSITORY_ROOT, prefix))
    if not manifest_path.is_file():
        raise VerificationFailure(
            "%s: %s is missing from the work tree; the pinned subject set of this lane "
            "cannot be reconciled" % (PIN_MANIFEST_ABSENT, PIN_MANIFEST))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = list(manifest.get("subjects") or []) + list(manifest.get("frozen_dependencies") or [])
    governing = manifest.get("governing_commit")
    if (manifest.get("manifest_id") != PIN_MANIFEST_ID or not rows
            or not isinstance(governing, str)
            or re.fullmatch(r"[0-9a-f]{40}", governing) is None
            or any(not isinstance(row.get("path"), str) or not row.get("git_blob")
                   for row in rows)):
        raise VerificationFailure(
            "%s: %s is not a readable pin manifest (manifest_id, governing_commit or "
            "subject rows)" % (PIN_MANIFEST_SHAPE_INVALID, PIN_MANIFEST))
    paths = [row["path"] for row in rows]

    failures: list[str] = []
    head = _git("rev-parse", "HEAD", cwd=root)[1].decode("utf-8", "replace").strip()
    if _git("rev-parse", "--verify", "--quiet", governing + "^{commit}", cwd=root)[0] != 0:
        failures.append(
            "%s: %s names governing_commit %s, which this repository cannot resolve"
            % (PIN_GOVERNING_COMMIT_UNRESOLVED, PIN_MANIFEST, governing))
    elif _git("merge-base", "--is-ancestor", governing, "HEAD", cwd=root)[0] != 0:
        failures.append(
            "%s: governing_commit %s is not an ancestor of HEAD %s; this manifest pins a "
            "history the checked-out commit does not contain"
            % (PIN_GOVERNING_COMMIT_NOT_ANCESTOR, governing, head))

    # (a) STALENESS vs HEAD, subject by subject, out of the object store.
    resolved = _head_blobs(paths, root=root)
    absent = sorted(path for path, value in resolved.items() if value is None)
    if absent:
        failures.append(
            "%s: pinned subjects that do not exist at HEAD: %s"
            % (PIN_SUBJECT_ABSENT_AT_HEAD, ", ".join(absent)))
    stale = []
    for row in rows:
        found = resolved.get(row["path"])
        if found is None:
            continue
        mismatched = _pin_row_mismatches(row, found[0], found[1])
        if mismatched:
            stale.append("%s (%s)" % (row["path"], "; ".join(mismatched)))
    if stale:
        failures.append(
            "%s: %s records bytes that HEAD %s no longer carries, subject by subject: %s"
            % (PIN_STALE_AT_HEAD, PIN_MANIFEST, head, "; ".join(sorted(stale))))

    # (b) UNCOMMITTED DRIFT, restricted to the manifest's own subjects.
    code, out, err = _git("status", "--porcelain", "--", *paths, cwd=root)
    if code != 0:
        raise VerificationFailure(
            "%s: git status failed (%s)" % (PIN_GIT_UNAVAILABLE, err.strip()))
    dirty = sorted(line for line in out.decode("utf-8", "replace").splitlines() if line.strip())
    if dirty:
        failures.append(
            "%s: pinned subjects differ from the committed bytes in this working tree: %s"
            % (PIN_UNCOMMITTED_DRIFT, "; ".join(dirty)))

    if failures:
        raise VerificationFailure(" | ".join(failures))
    return {"status": "PASS", "mode": "GIT_WORK_TREE", "reconciliation_performed": True,
            "pin_manifest": PIN_MANIFEST, "governing_commit": governing,
            "head_commit": head, "governing_commit_is_head": governing == head,
            "subjects_reconciled": len(rows),
            "identities_checked": ["git_blob", "bytes", "lf_count", "lines", "sha384"],
            "uncommitted_drift": False}


def discover_witnesses(modules) -> set[str]:
    """Every test id in the BUILD witness namespace, by unittest introspection."""
    found: set[str] = set()
    loader = unittest.TestLoader()

    def walk(suite):
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                walk(test)
            else:
                found.add(test.id())

    for name in modules:
        walk(loader.loadTestsFromName(name))
    unnamed = sorted(t for t in found if not WITNESS_ID.match(t))
    if unnamed:
        raise VerificationFailure("witnesses outside the governed namespace: %s" % unnamed)
    return found


def run_tests(modules) -> tuple[set[str], int]:
    suite = unittest.TestSuite(
        unittest.TestLoader().loadTestsFromName(name) for name in modules)
    result: RecordingResult = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=2, resultclass=RecordingResult).run(suite)
    if not result.wasSuccessful():
        raise VerificationFailure("unit regression failure in: %s" % (modules,))
    return result.passed, result.testsRun


def check_frozen_suites() -> dict:
    _passed, count = run_tests(FROZEN_TEST_MODULES)
    if count != FROZEN_TEST_TOTAL:
        raise VerificationFailure(
            "frozen r13.2 suite total changed: %d != %d" % (count, FROZEN_TEST_TOTAL))
    return {"status": "PASS", "tests": count, "expected": FROZEN_TEST_TOTAL,
            "modules": list(FROZEN_TEST_MODULES)}


def check_build_suites() -> tuple[dict, set[str]]:
    passed, count = run_tests(BUILD_TEST_MODULES)
    discovered = discover_witnesses(BUILD_TEST_MODULES)
    if count != len(discovered):
        raise VerificationFailure(
            "BUILD suite ran %d tests but discovered %d witnesses" % (count, len(discovered)))
    return ({"status": "PASS", "tests": count, "modules": list(BUILD_TEST_MODULES)},
            passed)


def check_ledger(passed: set[str]) -> dict:
    """Exact two-way totality between the ledger and the BUILD witness namespace."""
    ledger = load_json(LEDGER)
    if ledger.get("schema_id") != "MBCX01BuildRepairLedgerV1":
        raise VerificationFailure("BUILD repair ledger schema_id mismatch")
    rows = ledger["invariants"]
    discovered = discover_witnesses(BUILD_TEST_MODULES)

    declared: list[str] = []
    for name, row in sorted(rows.items()):
        witnesses = list(row.get("positive") or []) + list(row.get("adversarial") or [])
        if not witnesses:
            raise VerificationFailure("empty ledger row: %s" % name)
        declared.extend(witnesses)
        for axis in ("positive", "adversarial"):
            if row.get(axis):
                continue
            carrier = row.get(axis + "_covered_by")
            if not carrier or carrier not in rows:
                raise VerificationFailure(
                    "row %s declares no %s witness and names no existing carrier row"
                    % (name, axis))
            if not rows[carrier].get(axis):
                raise VerificationFailure(
                    "row %s points at %s for its %s witness, which has none"
                    % (name, carrier, axis))

    duplicates = sorted({w for w in declared if declared.count(w) > 1})
    if duplicates:
        raise VerificationFailure("witness declared in more than one row: %s" % duplicates)
    missing = sorted(set(declared) - discovered)
    extra = sorted(discovered - set(declared))
    if missing or extra:
        raise VerificationFailure(
            "ledger/witness mismatch: declared-but-absent=%s executed-but-unmapped=%s"
            % (missing, extra))
    not_passed = sorted(set(declared) - passed)
    if not_passed:
        raise VerificationFailure("declared witnesses that did not pass: %s" % not_passed)
    totals = ledger.get("totals") or {}
    if (totals.get("invariants") != len(rows)
            or totals.get("witnesses") != len(declared)):
        raise VerificationFailure("ledger totals do not match its own rows")
    return {"status": "PASS", "invariants": len(rows), "witnesses": len(declared),
            "two_way_total": True}


# ---------------------------------------------------------------------------
# W14 — REGISTRATION TOTALITY, four levels (design §3, 2026-08-16)
# ---------------------------------------------------------------------------
#
# Design of record: MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md r6 FINAL §3, "Totality,
# four levels".  The hazard this arm exists for is the one the cohort slice hit in
# the flesh: three production modules and an eighteen-witness suite landed on disk
# and in git, and NOTHING in this verifier noticed, because every list here is
# hand-maintained and nothing cross-checked the lists against the world.  Each
# level below fails LOUD with its own name; none is a warning.
#
#   (a) glob-vs-registration, BOTH directions, for modules and for test modules;
#   (b) every REQUIRED artifact is registered for pinning AND pinned, and every
#       subject pinned BEYOND `REQUIRED` is named in a declared set (cohort-BUILD
#       council r1, adjudication 2: keep the subset relation, constrain the difference);
#   (c) the governed artifact namespace is DERIVED FROM THE UNION OF THE
#       REGISTRATION LISTS (never a filename glob — a glob leaves a
#       differently-named artifact unregistered-and-unnoticed) and every member of
#       it is on disk;
#   (d) every `BUILD_MODULES` entry is named by >= 1 repair-ledger row that also
#       names a behaviour and carries a witness.
W14_MODULE_GLOB_MISMATCH = "W14_MODULE_GLOB_VS_REGISTRATION_MISMATCH"
W14_TEST_GLOB_MISMATCH = "W14_TEST_MODULE_GLOB_VS_REGISTRATION_MISMATCH"
W14_NOT_REGISTERED_FOR_PINNING = "W14_REQUIRED_ARTIFACT_NOT_REGISTERED_FOR_PINNING"
W14_UNPINNED_AT_GOVERNING_COMMIT = "W14_REQUIRED_ARTIFACT_UNPINNED_AT_THE_GOVERNING_COMMIT"
W14_ARTIFACT_ABSENT_FROM_DISK = "W14_GOVERNED_ARTIFACT_ABSENT_FROM_DISK"
W14_MODULE_WITHOUT_WITNESS = "W14_BUILD_MODULE_WITHOUT_A_DECLARED_LEDGER_WITNESS"
W14_ROW_WITHOUT_BEHAVIOUR = "W14_LEDGER_ROW_NAMES_A_MODULE_WITHOUT_NAMING_A_BEHAVIOUR"
W14_UNKNOWN_MODULE_IN_LEDGER = "W14_LEDGER_ROW_NAMES_AN_UNREGISTERED_MODULE"
W14_PIN_SUBJECT_OUTSIDE_DECLARED_SET = "W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET"

PIN_MANIFEST_GENERATOR = "generate-build-pin-manifest.ps1"

#: THE DELIBERATE EXTRA PINS: the ONLY subjects the pin sources may carry BEYOND
#: `REQUIRED`. Level (b) is a SUBSET relation (`REQUIRED` is a subset of the pinned
#: subject set) and not equality, because a pinned reconstruction needs the frozen r13.2
#: layer this bundle re-runs but never imports; literal equality would refuse a RIGHT
#: reconstruction (council r1, seat 2). But an UNCONSTRAINED difference
#: is a hole: a synthetic pin-only subject — in the pin manifest, in no registration
#: list — left the bundle at PASS (cohort-BUILD council r1, seat 3, EXECUTED). This
#: constant closes it: anything pinned that is neither REQUIRED nor named here is
#: refused by name as W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET. ADDING A LINE HERE
#: IS A DECLARATION — it says a human decided this artifact is pinned on purpose and
#: what for; it is not a place to silence a surprise.
PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED = (
    # BUILD-side pins this bundle does not import and therefore cannot list in
    # REQUIRED: the handoff document a reconstruction is read against, and the smoke
    # cell plus its launcher, which run on hardware rather than in this suite.
    "MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md",
    "mbcx01_smoke_cell.py",
    "run-smoke-cell.ps1",
    # The FROZEN r13.2 layer ($frozenDependencies): the five frozen suites this bundle
    # runs by subprocess, their production modules, and the frozen contracts/documents
    # they read. Frozen means the BUILD lane may re-run them and may not edit them.
    "MBCX-01-COUNCIL-R12-SYNTHESIS-AND-CLOSURE-COMMISSION.md",
    "MBCX-01-EXPERIMENT-DESIGN-r9.md",
    "MBCX-01-INFERENCE-CONTRACT-v8.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v7.json",
    "MBCX-01-PACKET-SCHEMAS-v7.json",
    "MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md",
    "MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json",
    "MBCX-01-R13-CLOSURE-ARCHITECTURE.md",
    "MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json",
    "MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md",
    "MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md",
    "MBCX-01-R13-SYNTHETIC-COHORT-GENERATOR.json",
    "MBCX-01-R13.1-SHELF-QUERY-LOG.md",
    "MBCX-01-STATE-TRANSITION-CONTRACT-v8.json",
    "mbcx01_r13_common.py",
    "mbcx01_r13_inference.py",
    "mbcx01_r13_integration.py",
    "mbcx01_r13_measurement.py",
    "mbcx01_r13_packets.py",
    "mbcx01_r13_state_oracle.py",
    "mbcx01_r13_state_reference.py",
    "test_mbcx01_r13_inference.py",
    "test_mbcx01_r13_integration.py",
    "test_mbcx01_r13_measurement.py",
    "test_mbcx01_r13_packets.py",
    "test_mbcx01_r13_state.py",
    "verify-r13-schema-ajv.mjs",
)


def _ps1_string_list(source: str, name: str) -> list[str]:
    """The single-quoted entries of one `$name = @( ... )` array in a PowerShell file.

    The pin manifest's subject set is DEFINED by this script; the committed manifest
    is its OUTPUT at one commit.  Level (b) needs both, because they answer different
    questions: the script says what WILL be pinned, the manifest says what IS.

    COMMENT LINES ARE DROPPED FIRST, and that is not cosmetic: PowerShell comments in
    these arrays are English prose, and one apostrophe in a comment makes the naive
    quote scan emit a two-line fragment of that comment AS A SUBJECT PATH. Red on the
    pre-fix parser, 2026-08-16:

        non-existent entries: ['s committed generator spec, its three\\n    #
        production siblings and its witness suite. verify-build-bundle.py']

    A phantom entry can only ever ENLARGE the "will be pinned" set, which is the side
    that would hide a missing registration.
    """
    match = re.search(r"\$" + re.escape(name) + r"\s*=\s*@\((.*?)\n\)", source, re.S)
    if match is None:
        raise VerificationFailure(
            "%s: cannot find $%s in %s" % (W14_NOT_REGISTERED_FOR_PINNING, name,
                                           PIN_MANIFEST_GENERATOR))
    body = "\n".join(line for line in match.group(1).splitlines()
                     if not line.lstrip().startswith("#"))
    return re.findall(r"'([^']+)'", body)


def governed_artifact_namespace(*, build_modules, fixture_support, probes,
                                test_modules, required) -> list[str]:
    """Level (c): the namespace, DERIVED FROM THE REGISTRATION LISTS THEMSELVES.

    Deliberately not a glob and deliberately not `os.listdir`: the r3 seat-1 finding
    is that a glob silently blesses whatever happens to be lying there and misses an
    artifact that was named differently.  Every path here was written into a list by
    a human, which is exactly the property that makes level (c) mean something.
    """
    names = set(build_modules) | set(fixture_support) | set(probes) | set(required)
    names |= {name + ".py" for name in test_modules}
    names |= {name for pair in BUILD_SCHEMA_PAIRS for name in pair}
    names |= set(BUILD_WORK_PRODUCTS) | set(PARITY_DOCUMENTS)
    names |= {LEDGER, BUILD_COHORT_SPEC_ARTIFACT, PIN_MANIFEST_GENERATOR}
    return sorted(names)


def check_registration_totality(*, root: Path = ROOT, build_modules=None,
                                fixture_support=None, probes=None, test_modules=None,
                                required=None, ledger_document=None,
                                registered_for_pinning=None,
                                pin_manifest_document=None) -> dict:
    """W14, all four levels.  Every list is injectable so the witnesses can red it."""
    build_modules = tuple(BUILD_MODULES if build_modules is None else build_modules)
    fixture_support = tuple(BUILD_FIXTURE_SUPPORT if fixture_support is None
                            else fixture_support)
    probes = tuple(BUILD_RED_WITNESS_PROBES if probes is None else probes)
    test_modules = tuple(BUILD_TEST_MODULES if test_modules is None else test_modules)
    required = tuple(REQUIRED if required is None else required)

    # --- (a) glob vs registration, both directions ---------------------------
    module_glob = {path.name for path in root.glob("mbcx01_build_*.py")}
    registered_modules = ({name for name in build_modules if name.endswith(".py")}
                          | {name for name in fixture_support if name.endswith(".py")}
                          | set(probes))
    if module_glob != registered_modules:
        raise VerificationFailure(
            "%s: on disk but registered nowhere=%s; registered but not on disk=%s"
            % (W14_MODULE_GLOB_MISMATCH, sorted(module_glob - registered_modules),
               sorted(registered_modules - module_glob)))
    test_glob = {path.name for path in root.glob("test_mbcx01_build_*.py")}
    registered_tests = {name + ".py" for name in test_modules}
    if test_glob != registered_tests:
        raise VerificationFailure(
            "%s: on disk but registered nowhere=%s; registered but not on disk=%s"
            % (W14_TEST_GLOB_MISMATCH, sorted(test_glob - registered_tests),
               sorted(registered_tests - test_glob)))

    # --- (b) registered for pinning, and pinned ------------------------------
    if registered_for_pinning is None:
        generator_source = (root / PIN_MANIFEST_GENERATOR).read_text(encoding="utf-8")
        will_be_pinned = set(_ps1_string_list(generator_source, "buildSubjects"))
        will_be_pinned |= set(_ps1_string_list(generator_source, "frozenDependencies"))
    else:
        will_be_pinned = set(registered_for_pinning)
    unregistered = sorted(set(required) - will_be_pinned)
    if unregistered:
        raise VerificationFailure(
            "%s: %s is REQUIRED to run this bundle but %s would not pin it, so a "
            "reconstruction at the governing commit could not run: %s"
            % (W14_NOT_REGISTERED_FOR_PINNING, "/".join(unregistered[:3]),
               PIN_MANIFEST_GENERATOR, unregistered))

    manifest_path = root / PIN_MANIFEST
    pinned: set[str] = set()
    governing = None
    manifest = pin_manifest_document
    if manifest is None and manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest is not None:
        governing = manifest.get("governing_commit")
        pinned = {row["path"] for row in (list(manifest.get("subjects") or [])
                                          + list(manifest.get("frozen_dependencies") or []))
                  if isinstance(row.get("path"), str)}

    # The difference `pinned - REQUIRED` is DECLARED, not free. Level (b) stays a
    # SUBSET relation on purpose (equality would refuse a right reconstruction, which
    # legitimately pins the frozen layer), but every subject in the difference must be
    # named in PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED. Both pin sources are covered:
    # the generator says what WILL be pinned, the manifest says what IS, and a stray
    # can enter through either. Red, recorded 2026-08-16 on the pre-fix bytes
    # (sha256 1f9ebbb9...): a synthetic pin-only subject injected into the manifest rode
    # inside `level_b_pin_manifest_is_subset_not_equal` and the section still said PASS.
    declared_beyond = set(PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED)
    undeclared = sorted((will_be_pinned | pinned) - set(required) - declared_beyond)
    if undeclared:
        raise VerificationFailure(
            "%s: these subjects are pinned but are neither REQUIRED to run this bundle "
            "nor named in PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED, so nothing declares "
            "why a reconstruction carries them: %s"
            % (W14_PIN_SUBJECT_OUTSIDE_DECLARED_SET, undeclared))

    unpinned = sorted(set(required) - pinned)
    # An artifact that DID NOT EXIST at the governing commit cannot be in a manifest
    # generated there. That is the only exemption, it is decided by git rather than
    # by a list, and it is REPORTED BY NAME — regenerating the manifest at the commit
    # that lands the artifact is what closes it. An artifact that DOES exist at the
    # governing commit and is still unpinned is a loud failure: that is the real
    # "unregistered-and-unnoticed" shape.
    pending_first_pin: list[str] = []
    if unpinned:
        inside = (_git("rev-parse", "--is-inside-work-tree", cwd=root)[1]
                  .decode("utf-8", "replace").strip() == "true")
        if not inside or not governing:
            raise VerificationFailure(
                "%s: %s does not pin %s and this layout cannot ask git whether they "
                "existed at the governing commit" % (W14_UNPINNED_AT_GOVERNING_COMMIT,
                                                     PIN_MANIFEST, unpinned))
        existing = [path for path in unpinned
                    if _git("cat-file", "-e", "%s:%s" % (governing, path), cwd=root)[0] == 0]
        if existing:
            raise VerificationFailure(
                "%s: these artifacts exist at governing_commit %s and are REQUIRED, "
                "but %s does not pin them: %s"
                % (W14_UNPINNED_AT_GOVERNING_COMMIT, governing, PIN_MANIFEST, existing))
        pending_first_pin = sorted(set(unpinned) - set(existing))

    # --- (c) the governed artifact namespace is on disk ----------------------
    namespace = governed_artifact_namespace(
        build_modules=build_modules, fixture_support=fixture_support, probes=probes,
        test_modules=test_modules, required=required)
    absent = sorted(name for name in namespace if not (root / name).is_file())
    if absent:
        raise VerificationFailure(
            "%s: the governed artifact namespace is derived from the registration "
            "lists, and these members are not on disk: %s"
            % (W14_ARTIFACT_ABSENT_FROM_DISK, absent))

    # --- (d) module -> named behaviour -> declared witness -------------------
    ledger = load_json(LEDGER) if ledger_document is None else ledger_document
    rows = ledger["invariants"]
    known = set(build_modules) | set(fixture_support) | set(probes)
    covered: dict[str, list[str]] = {}
    for name, row in sorted(rows.items()):
        declared = list(row.get("modules") or [])
        unknown = sorted(set(declared) - known)
        if unknown:
            raise VerificationFailure(
                "%s: ledger row %s names %s, which no registration list carries"
                % (W14_UNKNOWN_MODULE_IN_LEDGER, name, unknown))
        if declared and not str(row.get("requirement") or "").strip():
            raise VerificationFailure(
                "%s: ledger row %s claims coverage of %s without stating the "
                "behaviour it owns" % (W14_ROW_WITHOUT_BEHAVIOUR, name, declared))
        if declared and not (list(row.get("positive") or [])
                             + list(row.get("adversarial") or [])):
            raise VerificationFailure(
                "%s: ledger row %s claims coverage of %s and declares no witness"
                % (W14_ROW_WITHOUT_BEHAVIOUR, name, declared))
        for module in declared:
            covered.setdefault(module, []).append(name)
    uncovered = sorted(set(build_modules) - set(covered))
    if uncovered:
        raise VerificationFailure(
            "%s: these production modules are named by no ledger row, so nothing "
            "declares what they own or which witness would change if they were "
            "replaced: %s" % (W14_MODULE_WITHOUT_WITNESS, uncovered))

    return {
        "status": "PASS",
        "design": "MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md r6 FINAL section 3",
        "level_a_module_glob_two_way": len(module_glob),
        "level_a_test_glob_two_way": len(test_glob),
        "level_b_required": len(set(required)),
        "level_b_registered_for_pinning": True,
        "level_b_pinned_at_governing_commit": sorted(set(required) & pinned) != [],
        "level_b_pending_first_pin": pending_first_pin,
        "level_b_pin_manifest_is_subset_not_equal": sorted(pinned - set(required)),
        "level_b_declared_pins_beyond_required": sorted(declared_beyond),
        "level_b_pins_beyond_required_are_declared":
            "EVERY_PINNED_SUBJECT_IS_REQUIRED_OR_NAMED_IN_"
            "PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED",
        "level_c_governed_artifacts": len(namespace),
        "level_c_derivation": "UNION_OF_THE_REGISTRATION_LISTS_NEVER_A_GLOB",
        "level_d_modules_covered": len(covered),
        "level_d_rows_naming_modules": sum(1 for row in rows.values() if row.get("modules")),
        "level_d_nontriviality_enforced":
            "EVERY_NAMED_MODULE_HAS_A_ROW_THAT_STATES_A_BEHAVIOUR_AND_CARRIES_A_"
            "PASSING_WITNESS",
        "level_d_nontriviality_not_enforced":
            "REPLACEMENT_SENSITIVITY_IS_NOT_MECHANICALLY_CHECKED: the ledger schema "
            "has no field that ties a witness to the module code path it would fail "
            "on, so this arm cannot prove a declared witness FLIPS when the named "
            "module is replaced. That half is carried by the red-first discipline of "
            "each witness, not by this check.",
    }


def check_schemas() -> dict:
    for arguments in (["--compile-only"], []):
        result = subprocess.run(
            ["node", str(ROOT / SCHEMA_VERIFIER), *arguments],
            cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise VerificationFailure(result.stderr or result.stdout)
    reply = json.loads(result.stdout.splitlines()[0])
    subjects = reply["subjects"]
    for _pair_schema, fixture in BUILD_SCHEMA_PAIRS:
        if not any(row["fixture"] == fixture for row in subjects.values()):
            raise VerificationFailure("schema verifier did not cover %s" % fixture)
    return {"status": "PASS", "subjects": len(subjects),
            "mutants_rejected": sum(row["mutants_rejected"] for row in subjects.values()),
            "strict_compile": True}


def _parity_digests(documents: dict) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="mbcx01-build-parity-") as directory:
        path = Path(directory) / "documents.json"
        path.write_text(json.dumps({"documents": documents}, ensure_ascii=False),
                        encoding="utf-8")
        return subprocess.run(["node", str(ROOT / PARITY_VERIFIER), str(path)],
                              cwd=ROOT, capture_output=True, text=True, check=False)


def check_canonical_parity() -> dict:
    """Python `canonical_json`/`sha384` must equal the Node digest, document for document."""
    import mbcx01_r13_common as common

    documents = {name: load_json(name) for name in PARITY_DOCUMENTS}
    result = _parity_digests(documents)
    if result.returncode != 0:
        raise VerificationFailure(result.stderr or result.stdout)
    digests = json.loads(result.stdout)["digests"]
    for name, document in sorted(documents.items()):
        encoded = common.canonical_json(document)
        if (digests[name]["sha384"] != common.sha384(encoded)
                or digests[name]["bytes"] != len(encoded)):
            raise VerificationFailure("canonicalization parity mismatch: %s" % name)

    # Control: a document outside the claimed value domain must be REFUSED, loudly.
    control = _parity_digests({PARITY_REFUSAL_CONTROL: load_json(PARITY_REFUSAL_CONTROL)})
    if control.returncode == 0 or "non-integer number" not in control.stderr:
        raise VerificationFailure(
            "the parity helper accepted a float-bearing document; the parity claim would "
            "then cover a domain it does not verify")
    return {"status": "PASS", "documents": len(documents), "hash_algorithm": "SHA-384",
            "boundary": "python:mbcx01_r13_common vs node:" + PARITY_VERIFIER,
            "value_domain": "object/array/string/boolean/null/safe-integer",
            "out_of_domain_control_refused": PARITY_REFUSAL_CONTROL}


def check_no_production_activation() -> dict:
    """`production_activation:false` is a CHECK here, not a claim."""
    import mbcx01_build_win32 as win32

    for _schema, fixture in BUILD_SCHEMA_PAIRS:
        document = load_json(fixture)
        if document.get("production_ready") is not False:
            raise VerificationFailure("committed manifest is not fixture-only: " + fixture)
    # The committed owner trust anchor is the FIXTURE anchor. A production anchor is
    # generated in the owner ceremony and delivered by operator configuration; one
    # sitting in this repository would be an activation nobody authorized.
    anchor = load_json(OWNER_TRUST_ANCHOR_FIXTURE)
    if anchor.get("fixture_only") is not True or "PRIVATE" in json.dumps(anchor):
        raise VerificationFailure(
            "committed owner trust anchor is not fixture-only, or carries key material: "
            + OWNER_TRUST_ANCHOR_FIXTURE)
    if os.environ.get(win32.ALLOW_PHYSICAL_ENV) is not None:
        raise VerificationFailure(
            "%s is set; this verifier refuses to run in an environment authorized for "
            "physical collection" % win32.ALLOW_PHYSICAL_ENV)
    return {"status": "PASS",
            "committed_manifests_production_ready": False,
            "committed_owner_trust_anchor_fixture_only": True,
            "physical_collection_env_flag_present": False,
            "signing_ceremony_performed": False,
            "trust_root_activated": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-report",
                        help="write the freshly generated report to this path")
    args = parser.parse_args()
    require_artifacts()

    report = {
        "report_id": REPORT_ID,
        "experiment_executed": False,
        "provider_calls": 0,
        "paid_calls": 0,
        "physical_harness_executed": False,
        "production_activation": False,
        "route_qualification_executed": False,
        "scientific_calls": 0,
        "top_level_readiness": "BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED",
        "blocking_prerequisites": [
            "PRODUCTION_STATE_TRUST_ROOT_NOT_ACTIVATED",
            "PRODUCTION_MEASUREMENT_TRUST_ROOT_NOT_ACTIVATED",
            "PHYSICAL_HARNESS_NOT_EXECUTED",
        ],
        "sections": {},
    }
    with ExecutionPosture() as posture:
        # FIRST: which bytes is this run about? A suite total cannot answer that.
        report["sections"]["pin_manifest"] = reconcile_pin_manifest()
        print("pin_manifest: PASS")
        report["sections"]["frozen_suites"] = check_frozen_suites()
        print("frozen_suites: PASS")
        build_section, passed = check_build_suites()
        report["sections"]["build_suites"] = build_section
        print("build_suites: PASS")
        report["sections"]["ledger"] = check_ledger(passed)
        print("ledger: PASS")
        report["sections"]["registration_totality"] = check_registration_totality()
        print("registration_totality: PASS")
        report["sections"]["schemas"] = check_schemas()
        print("schemas: PASS")
        report["sections"]["canonical_parity"] = check_canonical_parity()
        print("canonical_parity: PASS")
        report["sections"]["no_production_activation"] = check_no_production_activation()
        print("no_production_activation: PASS")
    report["sections"]["execution_posture"] = dict(posture.check(), status="PASS")
    print("execution_posture: PASS")

    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output_report:
        Path(args.output_report).write_text(serialized, encoding="utf-8")
        print("report written: %s" % args.output_report)
    print(serialized, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as failure:
        print("BUILD VERIFICATION FAILED: %s" % failure, file=sys.stderr)
        raise SystemExit(1) from failure
