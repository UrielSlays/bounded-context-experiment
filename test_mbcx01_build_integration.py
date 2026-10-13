"""BUILD integration witnesses — the connected authority graph (bi01-bi05) and the
verifier's own pin-manifest reconciliation (bi06-bi08).

Red-stage honesty, stated up front rather than discovered later: bi01 and bi02 were
GREEN the moment they were written, and that is expected, not papered over. Both halves
of the graph (BUILD A state authority, BUILD B measurement/exactness authority) already
had their own executed red-then-green witness sets, so a connected fixture that only
joins them cannot fail for a NEW reason unless the join itself is wrong. What bi01 and
bi02 add is the join: that a state receipt minted from a REAL file-backed store over
the frozen packet graph discharges the state sentinel for the same scorer input the
frozen validator checked, that a simulated grid admits and binds exactness over the
SAME envelope set, and that no fixture-labelled artifact anywhere in that graph can
cross into production admission.

bi03 (no-execution proof) and bi04 (Python/Node canonicalization parity) are genuinely
discriminating: bi03 fails if any network, provider or physical-collection call is made
during the connected run, and bi04 fails if the two canonicalizers disagree on a byte.

bi05 was added by the BUILD acceptance r2 fold (fix class FIXTURE_ISOLATION) and was RED
against the pre-fold bytes: `build_connected_authority_fixture` installed the committed
fixture owner anchor process-wide and `release_connected_authority_fixture` left it there,
so a caller that built and released this fixture was afterwards verifying production
evidence under a publicly-signable root (codex r2 F3, EXECUTED). See
MBCX-01-BUILD-FIXTUREISO-RED-WITNESS-RUN-2026-08-14.txt.

bi06-bi08 were added by the codex BUILD acceptance finding on `verify-build-bundle.py`'s
suite-total check and were RED against the pre-fold bytes: the verifier never opened
MBCX-01-BUILD-PIN-MANIFEST.json, so a frozen subject edited without changing the 150-test
total still produced a BUILD report that said PASS. They run entirely inside a THROWAWAY
git repository built in a temporary directory; they never reconcile, mutate or read the
repository this file lives in.

bi09/bi10 (smoke candidate digest) and bi11-bi13 (the smoke pass criterion) were added by
the codex-CLI r2 and r3 folds; each class carries its own measured red above its tests.

bi14-bi16 (the ONE pre-launch candidate resolution) were added by the codex-CLI r4 folds
3A and 3B; bi14 and bi15 are measured reds and bi16 is labelled a GUARD, not a red.

bi17 (ONE authorization decision, made by the collector's own gate over the resolved
launch command line) was added when the r4 P1 fold made that gate bind the command line
and cell: one measured red and two guards.

No test in this file runs the experiment, makes a provider or paid call, creates a
Windows Job, opens an ETW session, executes the 100-cell physical grid, or activates a
production trust root or signing ceremony.
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import importlib.util
import inspect
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_exactness_authority as exactness
import mbcx01_build_integration as integration
import mbcx01_build_measurement_authority as measurement_authority
import mbcx01_build_state_authority as state_authority
import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_build_win32 as win32
import mbcx01_build_windows_producer as producer
import mbcx01_r13_common as common
import mbcx01_r13_measurement as measurement
from test_mbcx01_build_measurement import (
    COMMITTED_TEST_SIGNING_PRIVATE_KEY_PEM, R13_RUN_ID, RUN_ID, SIMULATED_KEY_ID,
    simulated_collections, simulated_custody_evidence, simulated_production_grid,
    simulated_production_manifest)
from test_mbcx01_r13_measurement import sign_no_paid_test_envelopes

CANONICAL_PARITY_SCRIPT = "verify-build-canonical-parity.mjs"
BUNDLE_VERIFIER_SCRIPT = "verify-build-bundle.py"

OPERATOR_ANCHOR_ID = "MBCX01.BUILD.OWNER.ANCHOR.OPERATOR.TEST.1"

#: A miniature pinned "frozen test module" for bi06. It is written into a THROWAWAY git
#: repository, never into this one, and its two tests exist so the witness can measure the
#: suite TOTAL across a byte mutation the way `check_frozen_suites` measures 150.
PIN_PROBE_SUITE_SOURCE = (
    "import unittest\r\n"
    "\r\n"
    "\r\n"
    "class PinnedSubjectTests(unittest.TestCase):\r\n"
    "    def test_first(self):\r\n"
    "        self.assertTrue(True)\r\n"
    "\r\n"
    "    def test_second(self):\r\n"
    "        self.assertTrue(True)\r\n")


def load_bundle_verifier():
    """Import `verify-build-bundle.py` as a module (its file name is not an identifier)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), BUNDLE_VERIFIER_SCRIPT)
    spec = importlib.util.spec_from_file_location("mbcx01_build_bundle_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setUpModule():  # noqa: N802 - unittest name
    """OPERATOR WIRING for the suite (see the two BUILD witness suites for the why)."""
    ceremony.configure_test_production_anchor()


def tearDownModule():  # noqa: N802 - unittest name
    trust_anchor.clear_owner_trust_anchor()


class BuildConnectedAuthorityGraphWitnesses(unittest.TestCase):
    """bi01-bi04: the two BUILD artifacts joined into ONE authority graph."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.graph = integration.build_connected_authority_fixture()

    @classmethod
    def tearDownClass(cls):
        integration.release_connected_authority_fixture(cls.graph)

    # ---- bi01: one connected flow -------------------------------------------------

    def test_bi01_positive_one_connected_flow_admits_state_measurement_and_exactness(self):
        """Invariant: the complete authority graph connects. The frozen
        `packet_fixture_manifest` graph is committed through the REAL file-backed
        `SingleWriterStateStore`, the adapter mints a `StateAuthorityReceiptV2` from the
        durable rows, and `verify_production_scorer_input` returns `[]` — the one named
        state sentinel discharged, every other frozen check still executed. In the same
        graph a simulated 100-cell grid produced by `produce_signed_measurement_receipt_v2`
        is admitted by `evaluate_production_measurement` with `[]`, and
        `verify_production_carrier_exactness` binds a `CarrierExactnessReceiptV3` to THAT
        envelope set.

        GREEN AT BIRTH (declared, not hidden): both halves were already green, so this
        witness could not be red for a new reason. Its job is the join."""
        graph = self.graph
        self.assertEqual(graph["state_terminal"]["status"], "COMMITTED")
        self.assertTrue(os.path.isfile(graph["store_path"]))
        self.assertEqual(graph["state_admission_errors"], [])
        self.assertNotIn(state_authority.STATE_AUTHORITY_SENTINEL,
                         graph["state_admission_errors"])

        # The state receipt is bound to the SAME scorer input the frozen path validated,
        # and it was verified with the store CLOSED — from the durable path alone.
        self.assertEqual(
            graph["state_receipt"]["postcommit_readback"]["state_utf8"],
            common.canonical_json(
                graph["scorer_input"]["transition_authority"]["postcommit_state"]
            ).decode("utf-8"))
        self.assertEqual(graph["state_receipt"]["anti_replay"]["transaction_commit_id"],
                         graph["durable_anti_replay_anchors"].get(
                             "transaction_commit_id",
                             graph["state_receipt"]["transaction_commit_id"]))

        self.assertEqual(len(graph["measurement_envelopes"]), 100)
        self.assertEqual(graph["measurement_admission_errors"], [])
        self.assertEqual(set(graph["exactness_receipt"]),
                         set(exactness.EXACTNESS_RECEIPT_V3_KEYS))
        self.assertEqual(graph["exactness_receipt"]["authority_mode"],
                         exactness.PRODUCTION_AUTHORITY_MODE)
        self.assertEqual(
            graph["exactness_receipt"]["measurement_grid_identity_hash"],
            measurement.measurement_grid_identity_hash(graph["measurement_envelopes"]))

    # ---- bi02: fixture evidence cannot cross production admission -------------------

    def test_bi02_adversarial_fixture_evidence_cannot_cross_production_admission(self):
        """Invariant: nowhere in the connected graph can fixture-labelled evidence buy
        production authority — not the fixture V1 state receipt standing alone, not the
        frozen r13 fixture measurement envelopes, not a `CarrierExactnessReceiptV2`
        relabelled `PRODUCTION_MEASUREMENT_AUTHORITY` with its hash repaired."""
        graph = self.graph
        # (a) the fixture V1 state receipt alone: unchanged frozen behaviour, sentinel intact.
        fixture_only = state_authority.verify_production_scorer_input(
            graph["scorer_input"], None, expected_manifest=graph["expected_manifest"],
            trust_root_manifest=graph["state_trust_root_manifest"],
            custody_evidence=graph["state_custody_evidence"],
            store_path=graph["store_path"])
        self.assertIn(state_authority.STATE_AUTHORITY_SENTINEL, fixture_only)
        # ... and handing that V1 in as if it were the production receipt is a named refusal.
        v1_as_v2 = state_authority.verify_state_authority_receipt_v2(
            graph["scorer_input"]["state_authority_receipt"],
            trust_root_manifest=graph["state_trust_root_manifest"],
            custody_evidence=graph["state_custody_evidence"],
            store_path=graph["store_path"])
        self.assertIn(state_authority.STATE_AUTHORITY_V2_SCHEMA_INVALID, v1_as_v2)
        self.assertIn(state_authority.STATE_AUTHORITY_SENTINEL, v1_as_v2)

        # (b) frozen r13 fixture measurement envelopes stay unavailable.
        r13_rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=R13_RUN_ID))
        r13_errors = measurement_authority.evaluate_production_measurement(
            r13_rows, trust_root_manifest=graph["measurement_trust_root_manifest"],
            custody_evidence=graph["measurement_custody_evidence"],
            expected_run_id=R13_RUN_ID)
        self.assertIn(measurement_authority.FAIL_LOUD_SENTINEL, r13_errors)
        self.assertTrue(set(r13_errors) <= measurement_authority.PRODUCTION_ERROR_CODES,
                        r13_errors)

        # (c) a fixture V2 exactness receipt relabelled production is refused.
        fixture_receipt = measurement.fixture_carrier_exactness_receipt(
            "CANDIDATE.BASELINE", r13_rows)
        fixture_receipt["authority_mode"] = exactness.PRODUCTION_AUTHORITY_MODE
        fixture_receipt["receipt_hash"] = measurement.sha384(
            {key: value for key, value in fixture_receipt.items()
             if key != "receipt_hash"})
        with self.assertRaisesRegex(measurement_authority.MeasurementAuthorityError,
                                    "FIXTURE_EVIDENCE_RELABELED"):
            exactness.verify_production_carrier_exactness(
                fixture_receipt, envelopes=graph["measurement_envelopes"],
                suite_document=graph["exactness_suite"],
                trust_root_manifest=graph["measurement_trust_root_manifest"],
                custody_evidence=graph["measurement_custody_evidence"])

    # ---- bi03: no-execution proof ---------------------------------------------------

    def test_bi03_positive_the_connected_run_executes_no_network_provider_or_harness_call(self):
        """Invariant: the connected authority run is inert. Executed under live guards,
        it makes zero in-process network calls, spawns nothing but the committed local
        `node` verifier/signer, never calls `mbcx01_build_win32.collect`, and cannot:
        the physical-collection gate refuses without BOTH the environment flag and the
        runbook authorization marker, neither of which exists anywhere in this tree. The
        frozen r13.2 no-paid report facts are re-read from the committed file and must
        still hold."""
        spawned: list[list[str]] = []
        collect_calls: list[tuple] = []
        real_run = subprocess.run
        real_collect = win32.collect
        real_connect = socket.socket.connect
        real_create_connection = socket.create_connection
        real_getaddrinfo = socket.getaddrinfo

        def watched_run(args, *rest, **kwargs):
            spawned.append([str(item) for item in args]
                           if isinstance(args, (list, tuple)) else [str(args)])
            return real_run(args, *rest, **kwargs)

        def refuse_network(*_args, **_kwargs):
            raise AssertionError("the connected BUILD run attempted a network call")

        def refuse_collect(*args, **kwargs):
            collect_calls.append((args, kwargs))
            raise AssertionError("the connected BUILD run attempted a physical collection")

        graph = None
        try:
            subprocess.run = watched_run
            win32.collect = refuse_collect
            socket.socket.connect = refuse_network
            socket.create_connection = refuse_network
            socket.getaddrinfo = refuse_network
            graph = integration.build_connected_authority_fixture()
        finally:
            subprocess.run = real_run
            win32.collect = real_collect
            socket.socket.connect = real_connect
            socket.create_connection = real_create_connection
            socket.getaddrinfo = real_getaddrinfo
            if graph is not None:
                integration.release_connected_authority_fixture(graph)

        self.assertEqual(graph["state_admission_errors"], [])
        self.assertEqual(graph["measurement_admission_errors"], [])
        self.assertEqual(collect_calls, [])
        self.assertTrue(spawned, "the run must actually have used the node verifier")
        for command in spawned:
            self.assertEqual(command[0], "node", command)
            if command[1] != "-e":
                self.assertTrue(command[1].endswith(".mjs"), command)
                self.assertTrue(os.path.isfile(command[1]), command)

        # The physical-collection gate is two-factor and BOTH factors are absent here.
        self.assertIsNone(os.environ.get(win32.ALLOW_PHYSICAL_ENV))
        # The gate now also binds the command line and the cell (codex-CLI r4 P1
        # fold), so both call sites name them; the env and path factors this test is
        # about are checked first and still fire first.
        with self.assertRaises(win32.PhysicalCollectionNotAuthorized):
            win32._require_authorization(None)
        with tempfile.TemporaryDirectory(prefix="mbcx01-build-auth-") as directory:
            unmarked = os.path.join(directory, "not-an-authorization.txt")
            with open(unmarked, "w", encoding="utf-8") as stream:
                stream.write("this file carries no authorization marker\n")
            with self.assertRaises(win32.PhysicalCollectionNotAuthorized):
                win32._require_authorization(unmarked)

        report = integration.frozen_no_paid_report()
        for name, expected in sorted(integration.NO_PAID_REPORT_FACTS.items()):
            with self.subTest(fact=name):
                self.assertEqual(report[name], expected)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE", report["blocking_prerequisites"])
        self.assertIn("STATE_AUTHORITY_UNAVAILABLE", report["blocking_prerequisites"])

    # ---- bi04: canonicalization parity ----------------------------------------------

    def test_bi04_positive_python_and_node_canonicalization_agree_byte_for_byte(self):
        """Invariant: `canonical_json`/`sha384` computed in Python equal the digest a
        Node implementation of the same contract computes over the same documents. The
        parity is checked on NONTRIVIAL live artifacts of the connected graph — the
        signed state receipt, a signed measurement envelope and the production exactness
        receipt — not on a toy object."""
        graph = self.graph
        documents = {
            "state_authority_receipt_v2": graph["state_receipt"],
            "state_receipt_signed_preimage": {
                key: value for key, value in graph["state_receipt"].items()
                if key not in state_authority.V2_UNSIGNED_KEYS},
            "signed_measurement_receipt_v2": graph["measurement_envelopes"][0],
            "carrier_exactness_receipt_v3": graph["exactness_receipt"],
            "durable_anti_replay_anchors": graph["durable_anti_replay_anchors"],
        }
        digests = self.node_digests(documents)
        self.assertEqual(sorted(digests), sorted(documents))
        for name, document in sorted(documents.items()):
            with self.subTest(document=name):
                encoded = common.canonical_json(document)
                self.assertEqual(digests[name]["sha384"], common.sha384(encoded))
                self.assertEqual(digests[name]["bytes"], len(encoded))
        # A digest that agrees on identical inputs proves nothing unless it also
        # DISAGREES on different ones: one changed byte must move the Node digest.
        mutated = json.loads(json.dumps(documents["carrier_exactness_receipt_v3"]))
        mutated["result"] = "PASS_"
        moved = self.node_digests({"mutated": mutated})["mutated"]["sha384"]
        self.assertNotEqual(moved, digests["carrier_exactness_receipt_v3"]["sha384"])
        self.assertEqual(moved, common.sha384(common.canonical_json(mutated)))

    # ---- bi05: the fixture assembler does not leak its anchor ----------------------

    def test_bi05_adversarial_the_integration_fixture_does_not_leak_its_verifier_context(self):
        """Invariant (codex r2 F3): the connected fixture is an ASSEMBLER, not an
        operator. It installs the verifier context it needs for the scope of the
        assembly and restores whatever the operator had wired, so a long-lived process
        that builds and releases this fixture is never left verifying production
        evidence under the committed fixture root."""
        operator = ceremony.owner_anchor_document(
            anchor_id=OPERATOR_ANCHOR_ID,
            public_key_pem=ceremony.test_production_anchor_document()["public_key_pem"],
            fixture_only=False)
        trust_anchor.configure_owner_trust_anchor(
            operator, current_time=ceremony.TEST_VERIFIER_INSTANT)
        self.addCleanup(ceremony.configure_test_production_anchor)
        before, refusal = trust_anchor.resolve_production_verifier_context(
            trust_anchor.AUTHORITY_MEASUREMENT)
        self.assertIsNone(refusal)
        self.assertEqual(before.anchor.anchor_id, OPERATOR_ANCHOR_ID)

        graph = integration.build_connected_authority_fixture()
        try:
            # The assembly itself still admits at all three doors under its OWN context.
            self.assertEqual(graph["measurement_admission_errors"], [])
            self.assertEqual(graph["state_admission_errors"], [])
        finally:
            integration.release_connected_authority_fixture(graph)

        after, refusal = trust_anchor.resolve_production_verifier_context(
            trust_anchor.AUTHORITY_MEASUREMENT)
        self.assertIsNone(refusal)
        self.assertIs(after, before)
        self.assertEqual(after.anchor.anchor_id, OPERATOR_ANCHOR_ID)
        self.assertIs(after.anchor.fixture_only, False)
        # The executed consequence: the NEXT production evaluation in this process is
        # judged under the OPERATOR's root, so a universe signed by the committed
        # fixture owner key does not admit.
        manifest = simulated_production_manifest()
        custody = simulated_custody_evidence(
            manifest,
            anchor_id=ceremony.fixture_owner_anchor_document()["anchor_id"],
            private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
        errors = measurement_authority.evaluate_production_measurement(
            simulated_production_grid(), trust_root_manifest=manifest,
            custody_evidence=custody, expected_run_id=RUN_ID)
        self.assertIn("PRODUCTION_ACTIVATION_UNAUTHENTICATED", errors)
        self.assertIn(measurement_authority.FAIL_LOUD_SENTINEL, errors)

    def node_digests(self, documents: dict) -> dict:
        """Canonicalize + SHA-384 each document with the Node parity helper."""
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8",
                                         delete=False) as stream:
            json.dump({"documents": documents}, stream, ensure_ascii=False)
            path = stream.name
        try:
            result = subprocess.run(
                ["node", CANONICAL_PARITY_SCRIPT, path],
                capture_output=True, text=True, timeout=120, check=False)
        finally:
            os.unlink(path)
        self.assertEqual(result.returncode, 0, (result.stdout + result.stderr)[-4000:])
        reply = json.loads(result.stdout)
        self.assertIs(reply.get("ok"), True, reply)
        return reply["digests"]


class BuildPinManifestReconciliationWitnesses(unittest.TestCase):
    """bi06: the BUILD verifier reconciles its pin manifest before it certifies anything.

    RED against the pre-fold bytes: `verify-build-bundle.py` never opened
    MBCX-01-BUILD-PIN-MANIFEST.json, so a frozen subject could be edited without changing
    the 150-test total and the generated BUILD report still said PASS — certified bytes
    nobody had reconciled (codex BUILD acceptance finding on the suite-total check).

    Every check here runs against a THROWAWAY git repository built in a temporary
    directory. This witness never reads, mutates or reconciles the repository it lives in.
    """

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.bundle = load_bundle_verifier()

    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix="mbcx01-build-pin-witness-")
        self.addCleanup(shutil.rmtree, self.directory, True)
        self.root = Path(self.directory)
        self.git("init", "-q")
        self.git("config", "user.email", "witness@example.invalid")
        self.git("config", "user.name", "MBCX-01 pin witness")
        self.git("config", "commit.gpgsign", "false")
        # The DESIGN CONSTRAINT this arm exists under, reproduced deliberately: a CRLF
        # checkout over LF blobs. A freshness check that hashed working-tree files would
        # false-fire here on every subject.
        self.git("config", "core.autocrlf", "true")
        self.write("pinned_subject.py", PIN_PROBE_SUITE_SOURCE)
        self.write("pinned_document.json", '{"pinned": true}\r\n')
        self.git("add", "--all")
        self.git("commit", "-q", "-m", "pin witness base")

    # ---- throwaway-repository helpers ------------------------------------------------

    def git(self, *arguments: str) -> str:
        result = subprocess.run(["git", "-C", self.directory, *arguments],
                                capture_output=True, text=True, check=False, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return result.stdout

    def write(self, name: str, text: str) -> None:
        with open(os.path.join(self.directory, name), "wb") as stream:
            stream.write(text.encode("utf-8"))

    def pin_manifest(self, commit: str = "HEAD") -> dict:
        """The same rows `generate-build-pin-manifest.ps1` writes, from the object store."""
        rows = []
        for path in ("pinned_subject.py", "pinned_document.json"):
            blob = self.git("rev-parse", "%s:%s" % (commit, path)).strip()
            content = subprocess.run(["git", "-C", self.directory, "cat-file", "blob", blob],
                                     capture_output=True, check=True, timeout=120).stdout
            lf_count = content.count(b"\n")
            rows.append({
                "path": path, "bytes": len(content),
                "lines": 0 if not content else (
                    lf_count if content.endswith(b"\n") else lf_count + 1),
                "lf_count": lf_count,
                "sha384": hashlib.sha384(content).hexdigest().upper(),
                "git_blob": blob,
            })
        return {"manifest_id": self.bundle.PIN_MANIFEST_ID,
                "governing_commit": self.git("rev-parse", commit).strip(),
                "hash_algorithm": "SHA-384",
                "subjects": rows[:1], "frozen_dependencies": rows[1:]}

    def install_manifest(self, manifest: dict) -> None:
        (self.root / self.bundle.PIN_MANIFEST).write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def subject_status(self) -> str:
        """`git status --porcelain` restricted to the pinned subjects, as the arm reads it."""
        return self.git("status", "--porcelain", "--",
                        "pinned_subject.py", "pinned_document.json")

    def suite_total(self, name: str = "pinned_subject.py") -> int:
        """The pinned module's TEST COUNT, by the same introspection the verifier uses."""
        spec = importlib.util.spec_from_file_location(
            "mbcx01_pin_probe_suite", os.path.join(self.directory, name))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return unittest.TestLoader().loadTestsFromModule(module).countTestCases()

    def reconcile(self):
        return self.bundle.reconcile_pin_manifest(root=self.root)

    def assert_named_failure(self, named: str, *fragments: str):
        with self.assertRaises(self.bundle.VerificationFailure) as refusal:
            self.reconcile()
        message = str(refusal.exception)
        self.assertIn(named, message)
        for fragment in fragments:
            self.assertIn(fragment, message)
        return message

    # ---- bi06 -------------------------------------------------------------------------

    def test_bi06_adversarial_drifted_pinned_bytes_fail_by_name_while_the_suite_total_holds(self):
        """Invariant: the BUILD verifier reconciles MBCX-01-BUILD-PIN-MANIFEST.json against
        the current bytes, so a subject that drifts without changing the suite TOTAL is a
        named failure instead of a certified PASS. Both drift modes are named separately:
        uncommitted drift in the work tree, and staleness of the manifest against HEAD.

        The control that keeps this honest is measured, not asserted: across every
        mutation the pinned module's test count is UNCHANGED, which is exactly the signal
        `check_frozen_suites` reads. The count stays green; the reconciliation does not."""
        self.install_manifest(self.pin_manifest())
        total_before = self.suite_total()
        self.assertEqual(total_before, 2)

        # Control 1 — a clean CRLF checkout over LF blobs reconciles.
        clean = self.reconcile()
        self.assertEqual(clean["status"], "PASS")
        self.assertIs(clean["reconciliation_performed"], True)
        self.assertEqual(clean["subjects_reconciled"], 2)
        self.assertEqual(self.subject_status(), "")
        # ...and it reconciles DESPITE the working-tree bytes differing from the pinned
        # SHA-384, which is why this arm reads the object store and not the files on disk.
        with open(os.path.join(self.directory, "pinned_subject.py"), "rb") as stream:
            on_disk = stream.read()
        pinned_sha = self.pin_manifest()["subjects"][0]["sha384"]
        self.assertIn(b"\r\n", on_disk)
        self.assertNotEqual(hashlib.sha384(on_disk).hexdigest().upper(), pinned_sha)

        # (b) UNCOMMITTED DRIFT — one comment line, no test added, no test removed.
        self.write("pinned_subject.py",
                   PIN_PROBE_SUITE_SOURCE + "# drifted, same test count\r\n")
        self.assertEqual(self.suite_total(), total_before)
        self.assert_named_failure(self.bundle.PIN_UNCOMMITTED_DRIFT, "pinned_subject.py")

        # (a) STALENESS vs HEAD — committing the same drift clears the work tree and moves
        # the blob out from under the manifest, which still pins the previous bytes.
        self.git("add", "--all")
        self.git("commit", "-q", "-m", "drifted pinned subject")
        self.assertEqual(self.subject_status(), "")
        self.assertEqual(self.suite_total(), total_before)
        message = self.assert_named_failure(self.bundle.PIN_STALE_AT_HEAD,
                                            "pinned_subject.py", "git_blob")
        self.assertNotIn("pinned_document.json", message)

        # Regenerating the manifest at the new HEAD is what closes it: the arm reports
        # staleness, it does not become permanently red.
        self.install_manifest(self.pin_manifest())
        self.assertEqual(self.reconcile()["status"], "PASS")

        # A subject the manifest pins but HEAD does not carry is its own named failure.
        self.git("rm", "-q", "pinned_document.json")
        self.git("commit", "-q", "-m", "remove a pinned subject")
        self.assert_named_failure(self.bundle.PIN_SUBJECT_ABSENT_AT_HEAD,
                                  "pinned_document.json")

    def test_bi07_adversarial_an_unreconcilable_pin_manifest_is_never_a_silent_skip(self):
        """Invariant: "could not check" must never read as "checked and clean".

        Unverifiable postures are loud named failures: git that cannot be executed at
        all, and a manifest that is not a readable pin manifest — in or out of a work
        tree. Outside a work tree (the pinned reconstruction, where
        `verify-build-pinned.ps1` exports raw blob bytes AND the manifest beside them),
        a present manifest reconciles at the BYTE level — length/LF/lines/SHA-384 per
        subject, `git_blob` declared uncheckable — and a mutated reconstructed subject
        is a named failure. A bare directory with no manifest at all is the one
        non-reconciling posture, reported with `reconciliation_performed:false`."""
        self.install_manifest(self.pin_manifest())

        real_run = subprocess.run

        def no_git(arguments, *rest, **kwargs):
            if arguments and str(arguments[0]) == "git":
                raise FileNotFoundError(2, "The system cannot find the file specified")
            return real_run(arguments, *rest, **kwargs)

        try:
            subprocess.run = no_git
            self.assert_named_failure(self.bundle.PIN_GIT_UNAVAILABLE)
        finally:
            subprocess.run = real_run
        # The harness itself is proved: with git restored, the same call reconciles.
        self.assertEqual(self.reconcile()["status"], "PASS")

        manifest = self.pin_manifest()
        manifest["manifest_id"] = "NOT-THE-BUILD-PIN-MANIFEST"
        self.install_manifest(manifest)
        self.assert_named_failure(self.bundle.PIN_MANIFEST_SHAPE_INVALID)
        self.install_manifest(self.pin_manifest())
        self.assertEqual(self.reconcile()["status"], "PASS")

        # A work tree with no manifest in it at all.
        os.unlink(os.path.join(self.directory, self.bundle.PIN_MANIFEST))
        self.assert_named_failure(self.bundle.PIN_MANIFEST_ABSENT)

        # Outside a work tree with NO manifest: an UNVERIFIABLE posture, refused by
        # name (codex r3: the old PASS here claimed launcher authentication that may
        # never have happened — could-not-check must never read as checked-and-clean).
        outside = tempfile.mkdtemp(prefix="mbcx01-build-pin-outside-")
        self.addCleanup(shutil.rmtree, outside, True)
        with self.assertRaises(self.bundle.VerificationFailure) as refusal:
            self.bundle.reconcile_pin_manifest(root=Path(outside))
        self.assertIn(self.bundle.PIN_UNVERIFIABLE_POSTURE, str(refusal.exception))

        # A non-manifest file at the manifest path is a shape failure there too.
        shutil.copyfile(os.path.join(self.directory, "pinned_document.json"),
                        os.path.join(outside, self.bundle.PIN_MANIFEST))
        with self.assertRaises(self.bundle.VerificationFailure) as refusal:
            self.bundle.reconcile_pin_manifest(root=Path(outside))
        self.assertIn(self.bundle.PIN_MANIFEST_SHAPE_INVALID, str(refusal.exception))

        # The reconstruction layout verify-build-pinned.ps1 actually creates: raw LF
        # blob bytes exported beside the manifest. POSITIVE: it byte-reconciles.
        manifest = self.pin_manifest()
        for row in manifest["subjects"] + manifest["frozen_dependencies"]:
            blob = subprocess.run(
                ["git", "-C", self.directory, "cat-file", "blob", row["git_blob"]],
                capture_output=True, check=True, timeout=120).stdout
            with open(os.path.join(outside, row["path"]), "wb") as stream:
                stream.write(blob)
        with open(os.path.join(outside, self.bundle.PIN_MANIFEST), "wb") as stream:
            stream.write((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
        section = self.bundle.reconcile_pin_manifest(root=Path(outside))
        self.assertEqual(section["status"], "PASS")
        self.assertIs(section["reconciliation_performed"], True)
        self.assertEqual(section["mode"], "PINNED_RECONSTRUCTION_BYTE_RECONCILED")
        self.assertEqual(section["subjects_reconciled"], 2)
        self.assertEqual(section["identities_not_checkable_here"], ["git_blob"])

        # ADVERSARIAL: one mutated reconstructed subject is a named per-subject failure.
        with open(os.path.join(outside, "pinned_subject.py"), "ab") as stream:
            stream.write(b"# drifted after reconstruction\n")
        with self.assertRaises(self.bundle.VerificationFailure) as refusal:
            self.bundle.reconcile_pin_manifest(root=Path(outside))
        message = str(refusal.exception)
        self.assertIn(self.bundle.PIN_RECONSTRUCTION_MISMATCH, message)
        self.assertIn("pinned_subject.py", message)

    def test_bi08_positive_a_clean_crlf_work_tree_reconciles_every_pinned_subject(self):
        """Invariant: the arm admits the RIGHT tree as readily as it refuses a drifted one.

        The control that matters is the checkout this lane actually has: `core.autocrlf`
        is true, so every working-tree file differs from the LF blob the manifest pins.
        The reconciliation reads the object store, so a clean CRLF checkout reconciles
        subject for subject — a freshness arm that hashed the files on disk would refuse
        this tree, which is a wrong number of a different kind."""
        self.install_manifest(self.pin_manifest())
        section = self.reconcile()
        self.assertEqual(section["status"], "PASS")
        self.assertIs(section["reconciliation_performed"], True)
        self.assertEqual(section["mode"], "GIT_WORK_TREE")
        self.assertEqual(section["subjects_reconciled"], 2)
        self.assertIs(section["uncommitted_drift"], False)
        self.assertIs(section["governing_commit_is_head"], True)
        self.assertEqual(sorted(section["identities_checked"]),
                         ["bytes", "git_blob", "lf_count", "lines", "sha384"])
        self.assertEqual(self.subject_status(), "")
        for name in ("pinned_subject.py", "pinned_document.json"):
            with self.subTest(subject=name), open(os.path.join(self.directory, name),
                                                  "rb") as stream:
                on_disk = stream.read()
            self.assertIn(b"\r\n", on_disk)
            pinned = {row["path"]: row for row in
                      self.pin_manifest()["subjects"]
                      + self.pin_manifest()["frozen_dependencies"]}[name]
            self.assertNotEqual(hashlib.sha384(on_disk).hexdigest().upper(),
                                pinned["sha384"])
            self.assertEqual(
                hashlib.sha384(on_disk.replace(b"\r\n", b"\n")).hexdigest().upper(),
                pinned["sha384"])


class SmokeCandidateDigestWitnesses(unittest.TestCase):
    """bi09/bi10: the smoke driver's candidate digest binds the binary Windows executes.

    RED against the pre-fold bytes: `_candidate_digest` took `split()[0]` of the command
    line, so a quoted executable path containing spaces truncated at the first space and
    the run aborted `CANDIDATE_BINARY_NOT_FOUND` on a binary `CreateProcessW` would have
    executed (codex-CLI r2 finding, 2026-08-15). The token now follows the documented
    CommandLineToArgvW first-argument rule."""

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.directory = tempfile.mkdtemp(prefix="mbcx01-smoke-digest-witness-")
        self.addCleanup(shutil.rmtree, self.directory, True)

    def _binary(self, *relative: str) -> str:
        path = os.path.join(self.directory, *relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as stream:
            stream.write(b"MZ witness candidate bytes\n")
        return path

    def test_bi09_positive_a_quoted_spaced_executable_path_digests_the_real_binary(self):
        spaced = self._binary("Program Files Witness", "candidate.exe")
        expected = self.smoke.measurement.sha384(open(spaced, "rb").read())
        self.assertEqual(
            self.smoke._candidate_digest('"%s" --arg one' % spaced), expected)
        # The unquoted form keeps its meaning: first whitespace-delimited token.
        plain = self._binary("plaindir", "candidate.exe")
        self.assertEqual(
            self.smoke._candidate_digest("%s --arg one" % plain),
            self.smoke.measurement.sha384(open(plain, "rb").read()))

    def test_bi10_adversarial_unparseable_or_absent_candidates_abort_by_name(self):
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest('"never closed --arg')
        self.assertIn("CANDIDATE_COMMAND_LINE_UNPARSEABLE", str(refusal.exception))
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest("   ")
        self.assertIn("CANDIDATE_COMMAND_LINE_EMPTY", str(refusal.exception))
        missing = os.path.join(self.directory, "Program Files Witness", "absent.exe")
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest('"%s"' % missing)
        self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))


class SmokePassCriterionWitnesses(unittest.TestCase):
    """bi11-bi13: the smoke pass criterion is a valid envelope AND the honest red.

    RED against the pre-fold bytes (codex r3, 2026-08-15). Two defects, one criterion:

    bi11 — `evaluate_production_measurement` returns at its trust/custody gate before it
    reads the envelope (the fixture manifest is `production_ready:false` and custody is
    always empty), so `verify_envelope({})` recorded `pass_criterion_met: true` for an
    EMPTY envelope. Measured on the pre-fold bytes: `admission_errors` =
    [MEASUREMENT_CUSTODY_EVIDENCE_INVALID, MEASUREMENT_TRUST_ROOT_INVALID,
    PHYSICAL_HARNESS_UNAVAILABLE, PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL],
    `pass_criterion_met` = True.

    bi13 — when the criterion was NOT met, `execute` stored the verdict and returned, and
    `main` printed `status: OK` with exit code 0. Measured on the pre-fold bytes: exit
    code 0, status OK, with `verification.pass_criterion_met` false in the same report.

    bi12 is the positive control that keeps the fold honest in the other direction: a
    genuinely produced, fixture-signed one-cell envelope must STILL meet the criterion,
    because refusing right evidence would be the same defect wearing the other sign.

    Nothing here starts an ETW session, creates a Windows Job or runs a candidate: the
    collector, consumer and producer are stubbed, and `MBCX01_BUILD_ALLOW_PHYSICAL` is
    set only inside one `mock.patch.dict` and removed with it.
    """

    maxDiff = None

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.instant = "2026-08-15T00:00:00Z"

    def _smoke_envelope(self):
        """One REAL fixture-signed smoke envelope, produced by the BUILD producer."""
        signer = producer.FixtureSigner(
            SIMULATED_KEY_ID, COMMITTED_TEST_SIGNING_PRIVATE_KEY_PEM)
        identity = self.smoke.smoke_identity(
            harness_identity=self.smoke.harness_identity(),
            signing_key_id=SIMULATED_KEY_ID,
            trust_policy_digest=self.smoke._fixture_trust_policy_digest(),
            candidate_artifact_digest=measurement.sha384("MBCX01.BI11.CANDIDATE.BINARY"))
        return signer, producer.produce_signed_measurement_receipt_v2(
            simulated_collections()[0], signer=signer, identity=identity)

    # ---- bi11 ----------------------------------------------------------------------

    def test_bi11_adversarial_an_empty_or_hollowed_envelope_is_never_a_pass(self):
        empty = self.smoke.verify_envelope({}, evaluation_instant=self.instant)
        # The refusal is still honest and still names the sentinel — and that is exactly
        # why it cannot be the whole criterion: it was reached without reading anything.
        self.assertTrue(empty["expected_red_present"])
        self.assertIn(self.smoke.EXPECTED_RED_SENTINEL, empty["admission_errors"])
        # Asserted BEFORE the detail keys on purpose: this is the pre-fold red, and it
        # must read as a wrong VERDICT, not as a missing field.
        self.assertFalse(empty["pass_criterion_met"])
        self.assertFalse(empty["envelope_independently_valid"])
        self.assertIn("MEASUREMENT_ENVELOPE_INVALID",
                      empty["envelope_validation"]["structure_errors"])
        self.assertIn("RECEIPT_SECTION_ABSENT",
                      empty["envelope_validation"]["evidence_errors"])
        self.assertFalse(empty["pass_criterion_met"])

        # A HOLLOWED envelope: the raw returned bytes of both final Job queries are
        # emptied, the unsigned digests are refreshed and the whole thing is signed again
        # with the fixture key. Structure, identity, timing cross-check and signature are
        # then impeccable and ONLY the evidence is gone — which is precisely the shape a
        # trust/custody-gate refusal can say nothing about.
        signer, hollow = self._smoke_envelope()
        for row in hollow["receipt"]["job_receipt"]["evidence"]["job_queries"].values():
            row["raw_bytes_b64"] = ""
        producer.refresh_production_receipt_hash(hollow)
        hollow["signature_b64"] = signer.sign_preimages([hollow["receipt_preimage_b64"]])[0]
        result = self.smoke.verify_envelope(hollow, evaluation_instant=self.instant)
        self.assertEqual([], result["envelope_validation"]["structure_errors"])
        self.assertTrue(result["envelope_validation"]["signature_verified"])
        self.assertEqual(["JOB_QUERY_EVIDENCE_ABSENT"],
                         result["envelope_validation"]["evidence_errors"])
        self.assertTrue(result["expected_red_present"])
        self.assertFalse(result["pass_criterion_met"])

    # ---- bi12 ----------------------------------------------------------------------

    def test_bi12_positive_a_real_fixture_signed_smoke_envelope_still_meets_the_criterion(self):
        _, envelope = self._smoke_envelope()
        result = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        self.assertEqual([], result["envelope_validation"]["structure_errors"])
        self.assertEqual([], result["envelope_validation"]["evidence_errors"])
        self.assertEqual("VERIFIED", result["envelope_validation"]["signature_note"])
        self.assertTrue(result["envelope_independently_valid"])
        # The honest red is still required: a smoke envelope can never clear admission.
        self.assertIn(self.smoke.EXPECTED_RED_SENTINEL, result["admission_errors"])
        self.assertTrue(result["pass_criterion_met"])

    # ---- bi13 ----------------------------------------------------------------------

    def _stub_execute_path(self, verification):
        """Patch every collaborator `execute` would touch on a host. Starts nothing."""
        loss = types.SimpleNamespace(events_lost=0, log_buffers_lost=0,
                                     realtime_buffers_lost=0)
        consumer = types.SimpleNamespace(
            source_id=7, start=lambda: None, configure_pmc=lambda: None,
            stop=lambda: loss)
        return [
            mock.patch.dict(os.environ, {win32.ALLOW_PHYSICAL_ENV: "1"}),
            mock.patch.object(self.smoke, "preflight", lambda *a, **k: {
                "mode": "preflight", "pmu_available": True,
                "pmu_unavailable_reasons": [], "elevated": True,
                "environment": {"execution_environment": "WITNESS_STUB"},
                # `preflight` owns the ONE candidate resolution and the ONE
                # authorization decision, so a stubbed preflight has to supply
                # what `execute` reads back out of it (r4 FOLD-3A/3B + the
                # collector's command-line/cell gate).
                "candidate_image": {
                    "image_path": "WITNESS-STUB-IMAGE",
                    "launch_command_line": "WITNESS-STUB-LAUNCH",
                    "candidate_artifact_digest": "0" * 96},
                "authorization_gate": {"evaluated": False,
                                       "not_evaluable": "WITNESS_STUB"}}),
            mock.patch.object(self.smoke.etw, "EtwPmcConsumer", lambda: consumer),
            mock.patch.object(self.smoke.etw, "make_live_etw_session_factory",
                              lambda *a, **k: (lambda: None)),
            # The raw 96/144-byte buffers are part of what `collect()` always
            # returns, and the driver now persists them BEFORE it signs (r6 FOLD-B3),
            # so the stub has to model that shape rather than a subset of it.
            mock.patch.object(self.smoke.win32, "collect", lambda *a, **k: {
                "root_process_id": 4100, "trace_facts": {},
                "basic_and_io_raw_bytes": b"\x00" * 96,
                "extended_limit_raw_bytes": b"\x00" * 144}),
            mock.patch.object(self.smoke.producer, "SimulatedCollection",
                              lambda **kwargs: types.SimpleNamespace(**kwargs)),
            mock.patch.object(self.smoke.producer, "produce_signed_measurement_receipt_v2",
                              lambda *a, **k: {"envelope": "WITNESS_STUB"}),
            mock.patch.object(self.smoke, "_write_evidence", lambda *a, **k: None),
            mock.patch.object(self.smoke, "harness_identity", lambda: {}),
            mock.patch.object(self.smoke, "_fixture_trust_policy_digest", lambda: "0" * 96),
            mock.patch.object(self.smoke, "_candidate_digest", lambda line: "0" * 96),
            mock.patch.object(self.smoke, "verify_envelope",
                              lambda envelope, **k: dict(verification)),
            mock.patch.object(self.smoke, "load_fixture_signer",
                              lambda pem, key_id: (
                                  types.SimpleNamespace(key_id="WITNESS.TEST"),
                                  "WITNESS.TEST")),
        ]

    def _run_main(self, verification):
        directory = tempfile.mkdtemp(prefix="mbcx01-smoke-criterion-witness-")
        self.addCleanup(shutil.rmtree, directory, True)
        destination = os.path.join(directory, "evidence")
        report_path = os.path.join(directory, "report.json")
        patches = self._stub_execute_path(verification)
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        with open(os.devnull, "w", encoding="utf-8") as sink:
            with contextlib.redirect_stdout(sink):
                code = self.smoke.main([
                    "execute", "--authorization", "WITNESS-NOT-READ",
                    "--destination", destination, "--cell", "0,0,0",
                    "--operator-confirms-not-nested",
                    "--fixture-signing-key-pem", "WITNESS",
                    "--fixture-signing-key-id", "WITNESS.TEST",
                    "--report", report_path])
        with open(report_path, encoding="utf-8") as stream:
            return code, json.load(stream)

    def test_bi13_adversarial_a_failed_pass_criterion_never_exits_zero(self):
        code, report = self._run_main({
            "pass_criterion_met": False, "admission_errors": [],
            "expected_red_present": False, "envelope_independently_valid": True,
            "envelope_validation": {"structure_errors": [], "evidence_errors": [],
                                    "signature_note": "VERIFIED",
                                    "signature_verified": True, "valid": True}})
        self.assertNotEqual(0, code)
        self.assertEqual(2, code)
        self.assertEqual("ABORT", report["status"])
        self.assertIn("SMOKE_PASS_CRITERION_NOT_MET", report["reason"])
        self.assertIn("ADMISSION_RETURNED_NO_ERRORS", report["reason"])
        # The run is refused, not discarded: the report that failed travels with it.
        self.assertFalse(report["partial_report"]["verification"]["pass_criterion_met"])
        self.assertTrue(report["partial_report"]["cleanup"]["etw_session_stopped"])

        # An envelope that is not independently valid fails the same way, and says so.
        code, report = self._run_main({
            "pass_criterion_met": False,
            "admission_errors": [self.smoke.EXPECTED_RED_SENTINEL],
            "expected_red_present": True, "envelope_independently_valid": False,
            "envelope_validation": {"structure_errors": ["MEASUREMENT_ENVELOPE_INVALID"],
                                    "evidence_errors": ["RECEIPT_SECTION_ABSENT"],
                                    "signature_note": "NOT_A_SIGNATURE_CANDIDATE",
                                    "signature_verified": False, "valid": False}})
        self.assertEqual(2, code)
        self.assertIn("ENVELOPE_NOT_INDEPENDENTLY_VALID", report["reason"])
        self.assertIn("MEASUREMENT_ENVELOPE_INVALID", report["reason"])

    def test_bi13_positive_a_met_pass_criterion_still_reports_ok_with_exit_zero(self):
        code, report = self._run_main({
            "pass_criterion_met": True,
            "admission_errors": [self.smoke.EXPECTED_RED_SENTINEL],
            "expected_red_present": True, "envelope_independently_valid": True,
            "envelope_validation": {"structure_errors": [], "evidence_errors": [],
                                    "signature_note": "VERIFIED",
                                    "signature_verified": True, "valid": True}})
        self.assertEqual(0, code)
        self.assertEqual("OK", report["status"])
        self.assertTrue(report["verification"]["pass_criterion_met"])


class SmokeFoldBWitnesses(unittest.TestCase):
    """bw80-bw85: the BUILD acceptance r6 FOLD-B classes (r6 synthesis ruling 6).

    Measured RED against the PRE-FOLD bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 0b3fae01cdffbf1fba5cea246526fcbb33283adb34255bb77cd6b0dfcdf397d8, loaded
    from a scratch directory placed at `sys.path[0]` so THIS test module binds the
    pre-fold module object). Three classes, each with its own measured red:

    bw80/bw81 (SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION) — the smoke conjunction's
    first half was PRESENCE-ONLY, so a re-signed but semantically INVALID receipt
    met the pass criterion. Two seats executed the same class through different
    fields: SEAT2 set `process_membership.membership_complete` to False and SEAT3
    perturbed `retired_instructions`. Pre-fold measurement: both re-signed
    envelopes returned `pass_criterion_met: True` while the harness's OWN full
    per-receipt validator (`mbcx01_build_measurement_authority._receipt_errors`)
    refuses them with PROCESS_MEMBERSHIP_INVALID and
    INSTRUCTION_ACCOUNTING_INCOMPLETE respectively.

    bw82/bw83 are the GUARDS in the other direction — refusing right evidence is
    the same defect wearing the other sign. bw82 is SEAT2's positive control (the
    honest fixture-signed envelope). bw83 is the guard SEAT2's control could NOT
    give: the shape a REAL smoke run actually produces, which differs from the
    simulated collection in exactly two fields — the runbook's default `--cell
    0,0,0` (not a registered grid coordinate) and the smoke driver's own
    `external_enforcement_record()` (no supervisor-installed denial, declared as
    such on its face). Measured against the full validator, those two produce
    MEASUREMENT_SCHEMA_INVALID and EXTERNAL_WORK_UNMEASURED — both grid/production-
    admission questions, neither a statement about what the collector produced, so
    both are excluded BY NAME and RECORDED in the report rather than dropped.

    bw84 (SMOKE-PREFLIGHT-NODE) — preflight probed elevation, virtualization and
    the two static ABIs but never `node` or the verifier script, while signature
    verification shells out to node. Pre-fold measurement: the preflight report has
    no `node_runtime` key at all and a preflight with `node` unresolvable returns
    normally.

    bw85 (SEAT3 F5, persist-raw-evidence-before-sign) — evidence was written only
    AFTER signing, so a signer failure after a successful physical collection lost
    the capture (SEAT3 raised an unhandled FileNotFoundError for node
    post-collection). Pre-fold measurement: the evidence destination is EMPTY after
    the signer raises.

    Nothing here starts an ETW session, creates a Windows Job, runs a candidate or
    reads the host registry: the collector, consumer, producer and every host probe
    are stubbed, and `MBCX01_BUILD_ALLOW_PHYSICAL` is set only inside one
    `mock.patch.dict` and removed with it.
    """

    maxDiff = None

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.instant = "2026-08-15T00:00:00Z"
        self.signer = producer.FixtureSigner(
            SIMULATED_KEY_ID, COMMITTED_TEST_SIGNING_PRIVATE_KEY_PEM)

    # ---- envelope builders ---------------------------------------------------------

    def _identity(self):
        return self.smoke.smoke_identity(
            harness_identity=self.smoke.harness_identity(),
            signing_key_id=SIMULATED_KEY_ID,
            trust_policy_digest=self.smoke._fixture_trust_policy_digest(),
            candidate_artifact_digest=measurement.sha384("MBCX01.BW80.CANDIDATE.BINARY"))

    def _envelope(self, collection=None):
        collection = collection if collection is not None else simulated_collections()[0]
        return producer.produce_signed_measurement_receipt_v2(
            collection, signer=self.signer, identity=self._identity())

    def _resign(self, envelope):
        """Re-sign a MUTATED envelope with the fixture key — the seats' own move.

        This is the whole point of the class: structure, digests, preimage and
        signature all become impeccable again, so a validator that only asks
        "is it signed and are the sections present?" cannot see the tamper.
        """
        producer.refresh_production_receipt_hash(envelope)
        envelope["signature_b64"] = self.signer.sign_preimages(
            [envelope["receipt_preimage_b64"]])[0]
        return envelope

    # ---- bw80 ----------------------------------------------------------------------

    def test_bw80_red_resigned_membership_complete_false_fails_the_smoke_criterion(self):
        envelope = self._envelope()
        envelope["receipt"]["job_receipt"]["evidence"]["process_membership"][
            "membership_complete"] = False
        self._resign(envelope)
        # The harness's OWN full validator already refuses this receipt. That is the
        # measurement the fold reuses; it is asserted here so the witness fails loudly
        # if the reused validator ever stops seeing this field.
        self.assertIn("PROCESS_MEMBERSHIP_INVALID",
                      measurement_authority._receipt_errors(envelope["receipt"])[0])
        result = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        # Asserted BEFORE the detail keys: the pre-fold red is a wrong VERDICT.
        self.assertFalse(result["pass_criterion_met"])
        self.assertFalse(result["envelope_independently_valid"])
        # Everything the presence-only half looked at is still impeccable — which is
        # exactly why presence-only could not see the defect.
        self.assertEqual([], result["envelope_validation"]["structure_errors"])
        self.assertEqual([], result["envelope_validation"]["evidence_errors"])
        self.assertTrue(result["envelope_validation"]["signature_verified"])
        self.assertEqual(["PROCESS_MEMBERSHIP_INVALID"],
                         result["envelope_validation"]["semantic_errors"])
        # The abort sentence must NAME the half and the code, not imply them.
        reason = self.smoke._pass_criterion_failure(result)
        self.assertIn("ENVELOPE_NOT_INDEPENDENTLY_VALID", reason)
        self.assertIn("PROCESS_MEMBERSHIP_INVALID", reason)

    # ---- bw81 ----------------------------------------------------------------------

    def test_bw81_red_resigned_perturbed_retired_instructions_fails_the_smoke_criterion(self):
        envelope = self._envelope()
        job = envelope["receipt"]["job_receipt"]
        job["retired_instructions"] = job["retired_instructions"] + 7
        self._resign(envelope)
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement_authority._receipt_errors(envelope["receipt"])[0])
        result = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        self.assertFalse(result["pass_criterion_met"])
        self.assertFalse(result["envelope_independently_valid"])
        self.assertEqual([], result["envelope_validation"]["structure_errors"])
        self.assertEqual([], result["envelope_validation"]["evidence_errors"])
        self.assertTrue(result["envelope_validation"]["signature_verified"])
        self.assertEqual(["INSTRUCTION_ACCOUNTING_INCOMPLETE"],
                         result["envelope_validation"]["semantic_errors"])

    # ---- bw82 ----------------------------------------------------------------------

    def test_bw82_guard_the_honest_fixture_envelope_still_meets_the_criterion(self):
        """GUARD (green both sides by design) — SEAT2's executed positive control."""
        envelope = self._envelope()
        result = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        self.assertEqual([], result["envelope_validation"]["structure_errors"])
        self.assertEqual([], result["envelope_validation"]["evidence_errors"])
        self.assertEqual([], result["envelope_validation"]["semantic_errors"])
        self.assertEqual([], result["envelope_validation"]["semantic_not_applicable"])
        self.assertTrue(result["envelope_validation"]["semantic_coordinate_registered"])
        self.assertTrue(result["envelope_independently_valid"])
        self.assertIn(self.smoke.EXPECTED_RED_SENTINEL, result["admission_errors"])
        self.assertTrue(result["pass_criterion_met"])

    # ---- bw83 ----------------------------------------------------------------------

    def test_bw83_guard_the_real_smoke_path_shape_is_not_falsely_refused(self):
        """GUARD — the shape the RUNBOOK's own default invocation produces.

        SEAT2's positive control used a simulated collection at a REGISTERED grid
        coordinate carrying the r13 baseline's external-enforcement block. A real
        `run-smoke-cell.ps1 -Execute` differs in exactly two fields, and both would
        be refused by the unrestricted production validator:

          `--cell 0,0,0`            -> MEASUREMENT_SCHEMA_INVALID (H/D/F are not
                                       registered grid coordinates)
          `external_enforcement_record()` -> EXTERNAL_WORK_UNMEASURED (the smoke
                                       driver installs NO supervisor-owned denial
                                       and says so on its face)

        Neither is a statement about what the collector produced, so neither may
        turn "this is not a 100-cell production grid" into "the collector produced
        nothing". Both are held NOT-APPLICABLE by name and recorded.
        """
        collection = dataclasses.replace(
            simulated_collections()[0], H=0, D=0, F=0,
            external_enforcement=self.smoke.external_enforcement_record())
        envelope = self._envelope(collection)
        receipt_digest_before = measurement.sha384(envelope["receipt"])
        result = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        validation = result["envelope_validation"]
        self.assertEqual([], validation["structure_errors"])
        self.assertEqual([], validation["evidence_errors"])
        self.assertEqual([], validation["semantic_errors"])
        self.assertEqual(["EXTERNAL_WORK_UNMEASURED"], validation["semantic_not_applicable"])
        self.assertFalse(validation["semantic_coordinate_registered"])
        self.assertTrue(result["envelope_independently_valid"])
        self.assertTrue(result["pass_criterion_met"])
        # The validator is READ-ONLY over the receipt it judges: the coordinate the
        # grid-registration test needs is supplied on a copy, never written back.
        self.assertEqual(receipt_digest_before, measurement.sha384(envelope["receipt"]))
        self.assertEqual([0, 0, 0], [envelope["receipt"][axis] for axis in ("H", "D", "F")])
        # And the exclusion is NARROW: the same unregistered-coordinate receipt with a
        # semantic defect is still refused, so the exclusion cannot be a hiding place.
        envelope["receipt"]["job_receipt"]["evidence"]["process_membership"][
            "membership_complete"] = False
        self._resign(envelope)
        refused = self.smoke.verify_envelope(envelope, evaluation_instant=self.instant)
        self.assertEqual(["PROCESS_MEMBERSHIP_INVALID"],
                         refused["envelope_validation"]["semantic_errors"])
        self.assertFalse(refused["pass_criterion_met"])

    # ---- bw84 ----------------------------------------------------------------------

    def _preflight_patches(self, *, node_path):
        """Stub every host probe preflight makes. Reads no registry, starts nothing."""
        consumer = types.SimpleNamespace(
            _win32=None,
            _resolve_profile_source_id=lambda name: 7,
            _query_capability_facts=lambda source_id: {"WITNESS": "STUB"})
        return [
            mock.patch.object(self.smoke, "read_authorization",
                              lambda path: {"authorization_path": "WITNESS-STUB"}),
            mock.patch.object(self.smoke, "is_elevated", lambda: True),
            mock.patch.object(self.smoke, "host_virtualization_facts", lambda: {
                "hypervisor_present": False, "is_root_partition": False,
                "nested_virtualization_readable": False,
                "host_architecture": "WINDOWS_64BIT", "probe": "WITNESS_STUB"}),
            mock.patch.object(self.smoke.etw, "EtwPmcConsumer", lambda: consumer),
            mock.patch.object(self.smoke.etw, "_etw_win32", lambda: None),
            mock.patch.object(self.smoke.etw, "granted_capability_facts",
                              lambda **kwargs: {"WITNESS": "STUB"}),
            mock.patch.object(self.smoke.etw, "evaluate_evidence_availability",
                              lambda **kwargs: (True, ())),
            mock.patch("shutil.which",
                       lambda name, *a, **k: node_path if name == "node" else None),
        ]

    def _run_preflight(self, *, node_path):
        for patch in self._preflight_patches(node_path=node_path):
            patch.start()
            self.addCleanup(patch.stop)
        return self.smoke.preflight("WITNESS-NOT-READ",
                                    operator_confirms_not_nested=True)

    def test_bw84_red_preflight_reports_node_and_the_verifier_and_fails_loudly(self):
        report = self._run_preflight(node_path=shutil.which("node"))
        # (a) node resolvable AND runnable, with the version PRINTED into the report.
        self.assertIn("node_runtime", report)
        self.assertTrue(report["node_runtime"]["resolvable"])
        self.assertTrue(report["node_runtime"]["runnable"])
        self.assertTrue(str(report["node_runtime"]["version"]).startswith("v"))
        # (b) the verifier script signature verification shells out to is PRESENT.
        self.assertIn("signature_verifier", report)
        self.assertTrue(report["signature_verifier"]["present"])
        self.assertEqual(str(measurement.VERIFIER),
                         report["signature_verifier"]["verifier_path"])
        # The PMU probe ran AFTER both — the toolchain gate precedes the capability
        # probe, and both precede any ETW session or Job work.
        self.assertIn("pmu_capability", report)

    def test_bw84_red_preflight_aborts_when_node_cannot_be_resolved(self):
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self._run_preflight(node_path=None)
        sentence = str(refusal.exception)
        self.assertIn("SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE", sentence)
        self.assertIn("NODE_NOT_ON_PATH", sentence)

    # ---- bw85 ----------------------------------------------------------------------

    def test_bw85_red_raw_evidence_is_persisted_before_the_signer_runs(self):
        """A post-collection certification failure must not destroy the capture."""
        directory = tempfile.mkdtemp(prefix="mbcx01-smoke-bw85-witness-")
        self.addCleanup(shutil.rmtree, directory, True)
        destination = os.path.join(directory, "evidence")
        loss = types.SimpleNamespace(events_lost=0, log_buffers_lost=0,
                                     realtime_buffers_lost=0)
        consumer = types.SimpleNamespace(
            source_id=7, start=lambda: None, configure_pmc=lambda: None,
            stop=lambda: loss)
        collection = {
            "root_process_id": 4100, "trace_facts": {"WITNESS": "STUB"},
            "basic_and_io_raw_bytes": b"\xa1" * 96,
            "extended_limit_raw_bytes": b"\xb2" * 144,
            "nonce": "NONCE.BUILD.B.SMOKE.BW85"}

        def signer_raises(*args, **kwargs):
            # SEAT3's actual post-collection failure, verbatim in kind.
            raise FileNotFoundError(2, "The system cannot find the file specified", "node")

        patches = [
            mock.patch.dict(os.environ, {win32.ALLOW_PHYSICAL_ENV: "1"}),
            mock.patch.object(self.smoke, "preflight", lambda *a, **k: {
                "mode": "preflight", "pmu_available": True,
                "pmu_unavailable_reasons": [], "elevated": True,
                "environment": {"execution_environment": "WITNESS_STUB"},
                # See the bi13 stub: `preflight` owns the one resolution and the
                # one authorization decision that `execute` reads back.
                "candidate_image": {
                    "image_path": "WITNESS-STUB-IMAGE",
                    "launch_command_line": "WITNESS-STUB-LAUNCH",
                    "candidate_artifact_digest": "0" * 96},
                "authorization_gate": {"evaluated": False,
                                       "not_evaluable": "WITNESS_STUB"}}),
            mock.patch.object(self.smoke.etw, "EtwPmcConsumer", lambda: consumer),
            mock.patch.object(self.smoke.etw, "make_live_etw_session_factory",
                              lambda *a, **k: (lambda: None)),
            mock.patch.object(self.smoke.win32, "collect", lambda *a, **k: dict(collection)),
            mock.patch.object(self.smoke.producer, "SimulatedCollection",
                              lambda **kwargs: types.SimpleNamespace(**kwargs)),
            mock.patch.object(self.smoke.producer,
                              "produce_signed_measurement_receipt_v2", signer_raises),
            mock.patch.object(self.smoke, "harness_identity", lambda: {}),
            mock.patch.object(self.smoke, "_fixture_trust_policy_digest", lambda: "0" * 96),
            mock.patch.object(self.smoke, "_candidate_digest", lambda line: "0" * 96),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        with self.assertRaises(FileNotFoundError):
            self.smoke.execute(
                authorization_path="WITNESS-NOT-READ", destination=destination,
                command_line="cmd.exe /c exit 0", cell=(0, 0, 0),
                signer=types.SimpleNamespace(key_id="WITNESS.TEST"),
                signing_key_id="WITNESS.TEST", operator_confirms_not_nested=True)
        # THE RED: pre-fold this directory is EMPTY — the capture was destroyed by a
        # certification failure that happened after the physical work succeeded.
        written = sorted(os.listdir(destination))
        self.assertTrue(written, "the collected capture was lost when the signer failed")
        # Named UNSIGNED on its face: raw evidence is never mistakable for a receipt.
        self.assertTrue(all(name.startswith("UNSIGNED-INCOMPLETE-") for name in written),
                        written)
        self.assertIn("UNSIGNED-INCOMPLETE-basic-and-io-raw.bin", written)
        self.assertIn("UNSIGNED-INCOMPLETE-extended-limit-raw.bin", written)
        self.assertIn("UNSIGNED-INCOMPLETE-collection-transcript.json", written)
        self.assertIn("UNSIGNED-INCOMPLETE-README.json", written)
        with open(os.path.join(destination,
                               "UNSIGNED-INCOMPLETE-basic-and-io-raw.bin"), "rb") as stream:
            self.assertEqual(collection["basic_and_io_raw_bytes"], stream.read())
        with open(os.path.join(destination,
                               "UNSIGNED-INCOMPLETE-README.json"), encoding="utf-8") as stream:
            readme = json.load(stream)
        self.assertFalse(readme["signed"])
        self.assertFalse(readme["certified"])

    # ---- bw86 ----------------------------------------------------------------------

    def test_bw86_red_the_launcher_refuses_a_shell_with_no_node_before_elevation(self):
        """The launcher's OWN precondition list names the toolchain (FOLD-B2 rider).

        `run-smoke-cell.ps1` front-loads every precondition it can read (authorization
        file, marker, elevation, nested, destination, key). It did not read the one
        thing signature verification cannot proceed without. This checks THIS shell's
        PATH; the Python preflight probes the ELEVATED session separately, because
        those are two different PATHs and only the second one signs anything.

        Pre-fold measurement (PATH scrubbed to C:\\Windows\\System32, unelevated):
        the script threw `ABORT: this session is NOT elevated`, saying nothing about
        node. RED. The launcher is invoked with -Execute but it cannot reach any
        physical work: the check under test throws before `MBCX01_BUILD_ALLOW_PHYSICAL`
        is set and before python is started at all.
        """
        pwsh = shutil.which("pwsh") or shutil.which("powershell")
        if not pwsh:
            self.skipTest("no PowerShell host on PATH")
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "run-smoke-cell.ps1")
        self.assertTrue(os.path.isfile(script), script)
        directory = tempfile.mkdtemp(prefix="mbcx01-smoke-bw86-witness-")
        self.addCleanup(shutil.rmtree, directory, True)
        authorization = os.path.join(directory, "authorization.md")
        with open(authorization, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED\n")
        destination = os.path.join(directory, "evidence-not-created")
        command = (
            "$env:PATH = 'C:\\Windows\\System32'; "
            "& '%s' -Execute -Authorization '%s' -Destination '%s' "
            "-FixtureSigningKeyPem '%s' -FixtureSigningKeyId 'WITNESS.TEST' "
            "-OperatorConfirmsNotNested"
            % (script, authorization, destination,
               os.path.join(directory, "absent-key.pem")))
        completed = subprocess.run(
            [pwsh, "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True, text=True, timeout=180, check=False)
        output = (completed.stdout or "") + (completed.stderr or "")
        self.assertIn("SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE", output)
        self.assertIn("node", output)
        # It refused BEFORE it could reach anything physical.
        self.assertFalse(os.path.exists(destination))
        self.assertNotEqual(0, completed.returncode)


class SmokePreLaunchResolutionWitnesses(unittest.TestCase):
    """bi14-bi16: ONE candidate resolution, done ONCE, BEFORE the launch.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 ae382b74430c2b3ad91747b3323a236fc15246ca96461a3c14dc45283e2d1edd, loaded
    from a scratch directory placed at `sys.path[0]` for that one import while every
    collaborator module is imported from the WORKTREE first). Two codex-CLI r4 folds,
    one resolution:

    bi14 (FOLD-3B, REFUSES RIGHT EVIDENCE) — `_candidate_digest` searched PATH for the
    LITERAL token, so an extensionless `cmd /c exit 0` — which `CreateProcessW(None,
    ...)` launches perfectly well by appending an extension — was not found. The
    physical collection COMPLETED and was persisted, and only then did certification
    abort. Pre-fix measurement: `_candidate_digest("cmd /c exit 0")` raises
    `SmokeAbort: CANDIDATE_BINARY_NOT_FOUND:'cmd'`, and `execute(...)` raises the same
    abort AFTER `UNSIGNED-INCOMPLETE-*` evidence is already on disk. On a one-shot
    elevated session that is a real capture lost to a resolution mismatch.

    bi15 (FOLD-3A, ADMITS WRONG EVIDENCE) — `harness_identity()` and
    `_candidate_digest()` first opened their files AFTER `collect()` returned, so the
    signed envelope bound POST-RUN bytes rather than the bytes that produced the
    capture. Pre-fix measurement: with the candidate image and one harness source
    replaced DURING the stubbed collection, the identity handed to the producer
    carries the POST-mutation digests.

    bi16 is the GUARD in the other direction — refusing right evidence is the same
    defect wearing the other sign — and it is labelled a GUARD, not a red. Its parts
    (a)-(c) are green on BOTH sides by construction (the ordinary `cmd.exe /c exit 0`
    form, a quoted spaced path, and the honest refusals for an absent, empty or
    unparseable candidate); its parts (d)-(e) exercise behaviour the pre-fix bytes
    did not have at all and are therefore red pre-fix (measured: `CANDIDATE_BINARY_
    NOT_FOUND:'witness'`), which is reported as new capability, not as a fold red.

    Nothing here starts an ETW session, creates a Windows Job or runs a candidate: the
    collector, consumer, producer and preflight are stubbed and no test asks the smoke
    driver to launch anything. `MBCX01_BUILD_ALLOW_PHYSICAL` is set only inside one
    `mock.patch.dict` and removed with it. The harness digests are taken over COPIES in
    a temporary directory (`ROOT` is patched), so no repository file is ever mutated.
    """

    maxDiff = None

    HARNESS_SOURCES = ("mbcx01_build_win32.py", "mbcx01_build_etw_consumer.py",
                       "mbcx01_smoke_cell.py")

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.directory = tempfile.mkdtemp(prefix="mbcx01-smoke-prelaunch-witness-")
        self.addCleanup(shutil.rmtree, self.directory, True)
        # COPIES of the harness sources, so a witness may mutate one mid-run without
        # touching the repository. `harness_identity()` reads them through `ROOT`.
        self.harness_root = os.path.join(self.directory, "harness-copy")
        os.makedirs(self.harness_root)
        worktree = os.path.dirname(os.path.abspath(__file__))
        for name in self.HARNESS_SOURCES:
            shutil.copyfile(os.path.join(worktree, name),
                            os.path.join(self.harness_root, name))
        self.launched = []
        self.sequence = []
        self.identity = None

    # ---- stubs ---------------------------------------------------------------------

    def _collect_stub(self, during_collection=None):
        """Stand in for `win32.collect`. Records the command line it was HANDED."""
        def collect(command_line, **kwargs):
            self.sequence.append("collect")
            self.launched.append(command_line)
            if during_collection is not None:
                during_collection()
            return {"root_process_id": 4100, "trace_facts": {"WITNESS": "STUB"},
                    "basic_and_io_raw_bytes": b"\xa1" * 96,
                    "extended_limit_raw_bytes": b"\xb2" * 144,
                    "nonce": "NONCE.BUILD.B.SMOKE.PRELAUNCH"}
        return collect

    def _execute_patches(self, collect):
        loss = types.SimpleNamespace(events_lost=0, log_buffers_lost=0,
                                     realtime_buffers_lost=0)
        consumer = types.SimpleNamespace(
            source_id=7, start=lambda: None, configure_pmc=lambda: None,
            stop=lambda: loss)

        def produce(collection, *, signer, identity):
            self.sequence.append("sign")
            self.identity = identity
            return {"envelope": "WITNESS_STUB"}

        def preflight(path, *, operator_confirms_not_nested,
                      command_line=None, cell=None):
            """Every HOST probe stubbed; the REAL candidate resolution kept.

            The resolution is what these witnesses are about, so it is not
            stubbed — but it is only performed when the driver actually asks
            preflight for it, which is precisely the behaviour under test.
            """
            report = {"mode": "preflight", "pmu_available": True,
                      "pmu_unavailable_reasons": [], "elevated": True,
                      "environment": {"execution_environment": "WITNESS_STUB"},
                      "candidate_image": None,
                      "authorization_gate": {"evaluated": False,
                                             "not_evaluable": "WITNESS_STUB"}}
            resolve = getattr(self.smoke, "resolve_candidate_image", None)
            if resolve is not None and command_line is not None:
                report["candidate_image"] = resolve(command_line)
            return report

        return [
            mock.patch.dict(os.environ, {win32.ALLOW_PHYSICAL_ENV: "1"}),
            mock.patch.object(self.smoke, "ROOT", self.harness_root),
            mock.patch.object(self.smoke, "preflight", preflight),
            mock.patch.object(self.smoke.etw, "EtwPmcConsumer", lambda: consumer),
            mock.patch.object(self.smoke.etw, "make_live_etw_session_factory",
                              lambda *a, **k: (lambda: None)),
            mock.patch.object(self.smoke.win32, "collect", collect),
            mock.patch.object(self.smoke.producer, "SimulatedCollection",
                              lambda **kwargs: types.SimpleNamespace(**kwargs)),
            mock.patch.object(self.smoke.producer,
                              "produce_signed_measurement_receipt_v2", produce),
            mock.patch.object(self.smoke, "_write_evidence", lambda *a, **k: None),
            mock.patch.object(self.smoke, "_fixture_trust_policy_digest",
                              lambda: "0" * 96),
            mock.patch.object(self.smoke, "verify_envelope", lambda envelope, **k: {
                "pass_criterion_met": True, "admission_errors": ["WITNESS_STUB_RED"],
                "expected_red_present": True, "envelope_independently_valid": True}),
        ]

    def _run_execute(self, command_line, *, during_collection=None, name="evidence"):
        destination = os.path.join(self.directory, name)
        for patch in self._execute_patches(self._collect_stub(during_collection)):
            patch.start()
            self.addCleanup(patch.stop)
        report = self.smoke.execute(
            authorization_path="WITNESS-NOT-READ", destination=destination,
            command_line=command_line, cell=(0, 0, 0),
            signer=types.SimpleNamespace(key_id="WITNESS.TEST"),
            signing_key_id="WITNESS.TEST", operator_confirms_not_nested=True)
        return report, destination

    def _write_file(self, relative, data):
        path = os.path.join(self.directory, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as stream:
            stream.write(data)
        return path

    def _digest_of(self, path):
        with open(path, "rb") as stream:
            return measurement.sha384(stream.read())

    # ---- bi14 ------------------------------------------------------------------------

    def test_bi14_red_an_extensionless_command_resolves_instead_of_being_refused(self):
        """FOLD-3B: `cmd /c exit 0` is what the RUNBOOK may hand this driver."""
        system_cmd = shutil.which("cmd")
        if not system_cmd:
            self.skipTest("no cmd on PATH")
        expected = self._digest_of(system_cmd)

        # (a) the unit that raised CANDIDATE_BINARY_NOT_FOUND pre-fix.
        self.assertEqual(expected, self.smoke._candidate_digest("cmd /c exit 0"))

        # (b) the whole `execute` path: the run must CERTIFY, not abort after the
        #     unrepeatable capture has already been persisted.
        report, destination = self._run_execute("cmd /c exit 0")
        self.assertEqual(["collect", "sign"], self.sequence)
        self.assertTrue(report["unsigned_evidence_written"])

        # The hashed image and the LAUNCHED image cannot diverge: the resolved
        # absolute path is what `collect` was handed.
        self.assertEqual(1, len(self.launched))
        launched = self.launched[0]
        self.assertTrue(launched.startswith('"'), launched)
        launched_image = launched[1:launched.index('"', 1)]
        self.assertTrue(os.path.isabs(launched_image), launched_image)
        self.assertTrue(os.path.isfile(launched_image), launched_image)
        self.assertTrue(os.path.samefile(system_cmd, launched_image),
                        (system_cmd, launched_image))
        self.assertEqual(" /c exit 0", launched[launched.index('"', 1) + 1:])
        self.assertEqual(expected, self._digest_of(launched_image))
        self.assertEqual(expected, self.identity.candidate_artifact_digest)
        # And the report says which image was resolved, so the operator can read it.
        self.assertTrue(os.path.samefile(
            launched_image, report["candidate_image"]["image_path"]))
        self.assertEqual(expected, report["candidate_image"]["candidate_artifact_digest"])
        self.assertEqual("cmd", report["candidate_image"]["executable_token"])

    # ---- bi15 ------------------------------------------------------------------------

    def test_bi15_red_the_envelope_binds_the_pre_launch_bytes_not_the_post_run_bytes(self):
        """FOLD-3A: an image replaced DURING the run must not be what gets signed."""
        candidate = self._write_file(os.path.join("candidate", "witness.exe"),
                                     b"MZ PRE-LAUNCH CANDIDATE BYTES\n")
        pre_launch_candidate = self._digest_of(candidate)
        mutated_harness = os.path.join(self.harness_root, "mbcx01_build_win32.py")
        with mock.patch.object(self.smoke, "ROOT", self.harness_root):
            pre_launch_harness = dict(self.smoke.harness_identity())

        def replace_everything_mid_run():
            """An updater (or anything else) rewrites the files while the cell runs."""
            with open(candidate, "wb") as stream:
                stream.write(b"MZ POST-RUN CANDIDATE BYTES -- DIFFERENT LENGTH\n")
            with open(mutated_harness, "ab") as stream:
                stream.write(b"\n# MUTATED AFTER LAUNCH\n")

        report, _ = self._run_execute('"%s" --witness' % candidate,
                                      during_collection=replace_everything_mid_run)

        # The mutation really happened — otherwise this witness would pass vacuously.
        self.assertNotEqual(pre_launch_candidate, self._digest_of(candidate))
        with mock.patch.object(self.smoke, "ROOT", self.harness_root):
            self.assertNotEqual(pre_launch_harness, self.smoke.harness_identity())

        # THE RED: pre-fix both digests are read after `collect()` returned.
        self.assertEqual(pre_launch_candidate, self.identity.candidate_artifact_digest)
        self.assertEqual(pre_launch_harness, self.identity.harness_identity)
        self.assertEqual(pre_launch_candidate,
                         report["candidate_image"]["candidate_artifact_digest"])
        self.assertEqual(pre_launch_harness, report["prelaunch_binding"]["harness_identity"])
        self.assertEqual(["collect", "sign"], self.sequence)

    # ---- bi16 ------------------------------------------------------------------------

    def test_bi16_guard_the_forms_that_already_worked_still_work_and_still_refuse(self):
        """GUARD (green both sides by design) — no right evidence is refused.

        Not a red. The pre-fix bytes pass every assertion in this test except where
        noted; it exists so the FOLD-3A/3B resolution cannot buy its green by
        admitting something it should refuse, or by dropping a form that worked.
        """
        # (a) the ordinary explicit form the runbook defaults to.
        system_cmd = shutil.which("cmd.exe")
        if system_cmd:
            self.assertEqual(self._digest_of(system_cmd),
                             self.smoke._candidate_digest("cmd.exe /c exit 0"))
        # (b) a quoted path with spaces (bi09's class) still digests the real binary.
        spaced = self._write_file(os.path.join("Program Files Witness", "candidate.exe"),
                                  b"MZ witness candidate bytes\n")
        self.assertEqual(self._digest_of(spaced),
                         self.smoke._candidate_digest('"%s" --arg one' % spaced))
        # (c) the honest refusals are still honest.
        for command_line, sentinel in (
                ('"never closed --arg', "CANDIDATE_COMMAND_LINE_UNPARSEABLE"),
                ("   ", "CANDIDATE_COMMAND_LINE_EMPTY"),
                ('"%s"' % os.path.join(self.directory, "absent.exe"),
                 "CANDIDATE_BINARY_NOT_FOUND"),
                ("mbcx01-witness-no-such-candidate", "CANDIDATE_BINARY_NOT_FOUND")):
            with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                self.smoke._candidate_digest(command_line)
            self.assertIn(sentinel, str(refusal.exception))
        # (d) RIDER, rewritten by the codex-CLI r6 SEAT1 F1 fold (see bi17). This
        #     part used to assert that PATHEXT DRIVES resolution: with
        #     `PATHEXT=.ZZZ` an extensionless `witness` resolved `witness.zzz`.
        #     That is the shell's rule, not `CreateProcessW`'s, and asserting it
        #     pinned the defect. The property asserted now is the STRONGER one —
        #     a token `CreateProcessW` would resolve to `witness.exe` is never
        #     resolved to some other extension because the operator's PATHEXT
        #     names it — and the refusal it produces is still honest and named.
        directory = os.path.dirname(
            self._write_file(os.path.join("pathext-witness", "witness.zzz"),
                             b"MZ pathext witness\n"))
        for pathext in (".ZZZ", ".QQQ"):
            with mock.patch.dict(os.environ, {"PATH": directory,
                                              "PATHEXT": pathext}):
                with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                    self.smoke._candidate_digest("witness --arg")
                self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
        # (e) and the extension CreateProcessW appends is the one that resolves,
        #     with PATHEXT set to something else entirely or not set at all.
        self._write_file(os.path.join("pathext-witness", "witness.exe"),
                         b"MZ pathext default witness\n")
        expected_exe = self._digest_of(os.path.join(directory, "witness.exe"))
        with mock.patch.dict(os.environ, {"PATH": directory, "PATHEXT": ".ZZZ"}):
            self.assertEqual(expected_exe, self.smoke._candidate_digest("witness --arg"))
        with mock.patch.dict(os.environ, {"PATH": directory}):
            os.environ.pop("PATHEXT", None)
            self.assertEqual(expected_exe, self.smoke._candidate_digest("witness --arg"))
        # (f) a command line that ALREADY names the resolved image unambiguously is
        #     handed to process creation VERBATIM. The collector's authorization gate
        #     searches the authorization document for the exact text it is about to
        #     run, so re-quoting a fully specified command line would turn an
        #     authorized run into a refusal on the one-shot elevated session.
        resolved = self.smoke.resolve_candidate_image('"%s" --arg one' % spaced)
        self.assertEqual('"%s" --arg one' % spaced, resolved["launch_command_line"])
        self.assertFalse(resolved["launch_command_line_rewritten"])
        self.assertTrue(os.path.samefile(spaced, resolved["image_path"]))

    # ---- bi17 ------------------------------------------------------------------------

    def test_bi17_red_the_hashed_image_is_the_one_createprocessw_would_have_launched(self):
        """codex-CLI r6 SEAT1 F1: PATHEXT is the SHELL's rule, not this launcher's.

        `resolve_candidate_image` exists so that the image that is HASHED and the
        image that is LAUNCHED cannot differ. Resolving an extensionless token by
        walking PATHEXT broke exactly that: PATHEXT's documented default begins
        `.COM;.EXE`, while `CreateProcessW` with a NULL application name "appends
        .exe" and never consults PATHEXT at all (Learn, *CreateProcessW*,
        `lpCommandLine`: "if the file name extension is .com, this parameter must
        include the .com extension"). With `witness.COM` and `witness.EXE` both in
        a searched directory the preflight hashed, authorized and CERTIFIED the
        `.COM` while the launch semantics select the `.EXE`.

        This is a WRONG NUMBER, not a refusal: the run completes, the envelope is
        signed, and `candidate_artifact_digest` names a program that never
        executed. Nothing downstream can catch it, because every later check binds
        the digest this function returned.
        """
        directory = os.path.dirname(
            self._write_file(os.path.join("pathext-collision", "witness.COM"),
                             b"MZ COM -- the shell's pick\n"))
        self._write_file(os.path.join("pathext-collision", "witness.EXE"),
                         b"MZ EXE -- what CreateProcessW appends and launches\n")
        com_digest = self._digest_of(os.path.join(directory, "witness.COM"))
        exe_digest = self._digest_of(os.path.join(directory, "witness.EXE"))
        self.assertNotEqual(com_digest, exe_digest)

        with mock.patch.dict(os.environ, {"PATH": directory,
                                          "PATHEXT": ".COM;.EXE;.BAT"}):
            resolved = self.smoke.resolve_candidate_image("witness --arg one")
            digest = self.smoke._candidate_digest("witness --arg one")

        # THE RED: pre-fix both of these are the .COM.
        self.assertEqual(exe_digest, resolved["candidate_artifact_digest"])
        self.assertEqual(exe_digest, digest)
        self.assertNotEqual(com_digest, resolved["candidate_artifact_digest"])
        self.assertEqual("witness.exe",
                         os.path.basename(resolved["image_path"]).lower())
        # The ONE name CreateProcessW would try for a bare extensionless token.
        # This read `["witness.exe", "witness"]` until codex-CLI r7 P1: the bare
        # fallback certified files the launch semantics never look for, and the
        # documented rule appends `.exe` and stops. Witness bi19.
        self.assertEqual(["witness.exe"], resolved["attempted_file_names"])
        # The launched command line names that same resolved image.
        self.assertTrue(resolved["launch_command_line"].lower().startswith(
            '"%s"' % os.path.join(directory, "witness.exe").lower()),
            resolved["launch_command_line"])
        # PATHEXT is still REPORTED — an observation of the operator's session,
        # which is now honest precisely because it is not an input to the answer.
        self.assertEqual([".COM", ".EXE", ".BAT"], resolved["pathext"])

        # DISCRIMINATING: a directory holding ONLY the .COM is a NAMED REFUSAL,
        # not a resolution — `CreateProcessW(NULL, "other ...")` would not find it
        # either, and certifying a program the launcher cannot start is the defect
        # this fold removes, not a capability it keeps.
        only_com = os.path.dirname(
            self._write_file(os.path.join("com-only", "other.COM"), b"MZ COM only\n"))
        with mock.patch.dict(os.environ, {"PATH": only_com, "PATHEXT": ".COM;.EXE"}):
            with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                self.smoke._candidate_digest("other --arg")
            self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
            # ... and naming the extension explicitly still runs it, because a
            # token that CARRIES an extension is used exactly as given.
            self.assertEqual(self._digest_of(os.path.join(only_com, "other.COM")),
                             self.smoke._candidate_digest("other.COM --arg"))

    # ---- bi18 ------------------------------------------------------------------------

    def _run_execute_with_consumer(self, consumer, collect, *, name):
        """`execute` with a caller-supplied consumer stub. No ETW session exists."""
        destination = os.path.join(self.directory, name)
        patches = self._execute_patches(collect)
        # Applied LAST, so this consumer is the one `execute` constructs.
        patches.append(mock.patch.object(self.smoke.etw, "EtwPmcConsumer",
                                         lambda: consumer))
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        return self.smoke.execute(
            authorization_path="WITNESS-NOT-READ", destination=destination,
            command_line="cmd.exe /c exit 0", cell=(0, 0, 0),
            signer=types.SimpleNamespace(key_id="WITNESS.TEST"),
            signing_key_id="WITNESS.TEST", operator_confirms_not_nested=True)

    def test_bi18_red_a_failing_session_stop_never_replaces_the_primary_fault(self):
        """codex-CLI r6 SEAT1 F5: the cleanup is not allowed to eat the diagnosis.

        `execute` stops the ETW session in a `finally` so the runbook's cleanup
        obligation holds even when the collection faults. Unguarded, that call
        REPLACED the in-flight exception whenever the stop failed too: the
        operator was told the session would not stop, for a run that actually
        died in `collect()`. On a one-shot elevated session the primary fault is
        the whole diagnostic value of a failed run.

        The collector already answers this at `mbcx01_build_win32.py` (:940-946)
        — the in-flight exception stays PRIMARY and the secondary is attached to
        it with `add_note` — and this is the same pattern at the driver's own
        teardown. Nothing is swallowed: with no exception in flight the cleanup
        failure IS the error.
        """
        def failing_stop():
            raise RuntimeError("WITNESS_ETW_STOP_FAILURE")

        def failing_collect(command_line, **kwargs):
            self.sequence.append("collect")
            raise win32.CollectorFault("WITNESS_PRIMARY_COLLECTION_FAULT")

        consumer = types.SimpleNamespace(
            source_id=7, start=lambda: None, configure_pmc=lambda: None,
            stop=failing_stop)

        # THE RED: pre-fix this raises RuntimeError('WITNESS_ETW_STOP_FAILURE')
        # and the collection fault is gone from the raised exception entirely.
        with self.assertRaises(win32.CollectorFault) as caught:
            self._run_execute_with_consumer(consumer, failing_collect,
                                            name="evidence-primary")
        self.assertIn("WITNESS_PRIMARY_COLLECTION_FAULT", str(caught.exception))
        self.assertEqual(["collect"], self.sequence)
        # The cleanup failure is NOT lost either — it rides on the primary.
        notes = getattr(caught.exception, "__notes__", [])
        self.assertTrue(any("ETW_SESSION_STOP_FAILED" in note and
                            "WITNESS_ETW_STOP_FAILURE" in note for note in notes),
                        notes)

    def test_bi18_guard_a_failing_session_stop_with_nothing_in_flight_is_the_error(self):
        """GUARD for bi18: the primary-preserving cleanup never SWALLOWS a failure.

        A teardown that only reported when something else had already gone wrong
        would be worse than the defect it replaces: the session really did not
        stop, and on the operator's elevated box that is the next run's problem.
        With nothing in flight the cleanup failure is raised unchanged, and on the
        ordinary path the loss counters and the cleanup record are still written.
        """
        def failing_stop():
            raise RuntimeError("WITNESS_ETW_STOP_FAILURE")

        consumer = types.SimpleNamespace(
            source_id=7, start=lambda: None, configure_pmc=lambda: None,
            stop=failing_stop)
        with self.assertRaises(RuntimeError) as caught:
            self._run_execute_with_consumer(consumer, self._collect_stub(),
                                            name="evidence-cleanup-only")
        self.assertEqual("WITNESS_ETW_STOP_FAILURE", str(caught.exception))
        self.assertEqual(["collect", "sign"], self.sequence)

        # And the honest path still records what it always recorded.
        report, _ = self._run_execute("cmd.exe /c exit 0", name="evidence-honest")
        self.assertTrue(report["cleanup"]["etw_session_stopped"])
        self.assertEqual({"events_lost": 0, "log_buffers_lost": 0,
                          "realtime_buffers_lost": 0}, report["loss_counters"])




class SmokeCreateProcessWResolutionSetWitnesses(unittest.TestCase):
    """bi19-bi22: the DOCUMENTED SET of CreateProcessW resolution rules, closed.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 a206ee9d83558bcfdc5afb56af04a1c51b0355cae4f2154d9df02838dd52bd82 — the
    worktree checkout hashes the same, byte for byte), loaded from a scratch
    directory placed at `sys.path[0]`; the runner PRINTS the bound module's
    `__file__` and sha256 and ASSERTS the pre-fix copy won.

    WHY A SET AND NOT TWO PATCHES. codex-CLI r6 SEAT1 F1 closed ONE member of
    this set (extensionless -> `.exe`, never PATHEXT) and, applying it
    UNIFORMLY, broke a second (`.exe` is NOT appended when the name contains a
    path). r7 found the breakage plus a third unmodelled member. So the members
    are ENUMERATED here from the two Learn paragraphs that define the whole
    resolution — `CreateProcessW`, *lpApplicationName* and *lpCommandLine*
    (learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
    — and every one is either IMPLEMENTED or REFUSED BY NAME. The premise is
    byte-checked, not assumed: `mbcx01_build_win32.py:787-790` calls
    `CreateProcessW(None, <command line>, ...)`, so `lpApplicationName` really is
    NULL and these really are the governing rules.

    bi19 (P1, WRONG NUMBER — both signs). "If the file name ends in a period (.)
    with no extension, or if the file name contains a path, .exe is not
    appended." The r6 fold appended `.exe` to every extensionless token, so with
    `C:\dir\tool` requested and `C:\dir\tool.exe` on disk the preflight hashed,
    authorized and CERTIFIED `tool.exe` while the launch runs `tool`; and the
    bare-name fallback certified an extensionless file that `CreateProcessW`
    would never have found. Pre-fix measurement: both below.

    bi20 (P2, WRONG REFUSAL then WRONG SEARCH). An unquoted long file name with
    a space is interpreted at SUCCESSIVE whitespace boundaries
    (`c:\program.exe`, `c:\program files\sub.exe`, ...). This driver takes the
    first token and stops, so `C:\dir\A B\tool.exe --arg` aborted
    `CANDIDATE_BINARY_NOT_FOUND:'C:\dir\A'` for a command line Windows launches.
    The close is a NAMED REFUSAL, not the progressive search: implementing the
    search would be machinery this harness has no adversary for — it writes its
    own command lines — and a refusal that tells the operator to QUOTE is the
    honest answer. Refusing is scoped so it can never eat a working shape: it
    fires only where our answer and Windows' can DIFFER.

    bi22 (WRONG NUMBER — the member NOBODY reported). Walking the set instead of
    the reported instances turned up a third break: the documented search order
    for a bare name has SIX steps and this driver enumerated FIVE. The 16-bit
    Windows system directory (`%SystemRoot%\\System`), which Learn says "is
    searched" between the 32-bit system directory and the Windows directory, was
    missing, so a collision there was decided the wrong way round. Pre-fix
    measurement: the answered sequence is the documented one with step 4 cut out.

    bi21 is the SET TABLE: every documented rule, its citation, and the
    behaviour that closes it, asserted in one place so the next fold cannot
    close one member by breaking another. It fails at its FIRST broken row, so
    each member also has its own witness above; the table is the ledger, not the
    only red.

    ⛔ Nothing here starts an ETW session, creates a Job or launches a process.
    Only `resolve_candidate_image` / `_candidate_digest` are called, and every
    file they read is written into a temporary directory.
    """

    maxDiff = None

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.directory = tempfile.mkdtemp(prefix="mbcx01-createprocessw-set-")
        self.addCleanup(shutil.rmtree, self.directory, True)

    def _write_file(self, relative, data):
        path = os.path.join(self.directory, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as stream:
            stream.write(data)
        return path

    def _digest_of(self, path):
        with open(path, "rb") as stream:
            return measurement.sha384(stream.read())

    # ---- bi19 ----------------------------------------------------------------------

    def test_bi19_red_a_path_carrying_extensionless_token_is_used_verbatim(self):
        """codex-CLI r7 P1: `.exe` is appended to a BARE name, never to a path.

        Learn, *CreateProcessW*, `lpCommandLine`: "If the file name does not
        contain an extension, .exe is appended... If the file name ends in a
        period (.) with no extension, or if the file name contains a path, .exe
        is not appended."

        With both files present the two readings name two DIFFERENT programs, so
        this is a wrong NUMBER: the run completes, the envelope is signed, and
        `candidate_artifact_digest` binds an image that never executed.
        """
        verbatim = self._write_file(os.path.join("pathy", "tool"),
                                    b"MZ the extensionless image, used verbatim\n")
        appended = self._write_file(os.path.join("pathy", "tool.exe"),
                                    b"MZ the .exe the r6 fold appended\n")
        self.assertNotEqual(self._digest_of(verbatim), self._digest_of(appended))

        resolved = self.smoke.resolve_candidate_image('"%s" --arg one' % verbatim)
        # THE RED: pre-fix both of these are the `.exe`.
        self.assertEqual(self._digest_of(verbatim),
                         resolved["candidate_artifact_digest"])
        self.assertEqual(self._digest_of(verbatim),
                         self.smoke._candidate_digest(verbatim))
        self.assertTrue(os.path.samefile(verbatim, resolved["image_path"]))
        # A path-carrying token has exactly ONE candidate: itself.
        self.assertEqual([verbatim], resolved["attempted_file_names"])
        self.assertEqual("DIRECTORY_COMPONENT", resolved["resolution"])

    def test_bi19_red_a_path_carrying_token_never_falls_back_to_the_exe(self):
        """The other sign: certifying a file the launch would never reach.

        Only `sibling.exe` exists. `CreateProcessW(NULL, "C:\\dir\\sibling ...")`
        does not append `.exe` to a name containing a path, so it finds nothing
        and the process is never created. Resolving it here would hash, authorize
        and certify a program that CANNOT be the one that ran.
        """
        self._write_file(os.path.join("exe-only", "sibling.exe"), b"MZ exe only\n")
        token = os.path.join(self.directory, "exe-only", "sibling")
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest(token)
        self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
        # ... and naming it in full still resolves, because a token that CARRIES
        # an extension is used exactly as given.
        self.assertEqual(
            self._digest_of(os.path.join(self.directory, "exe-only", "sibling.exe")),
            self.smoke._candidate_digest("%s.exe --arg" % token))

    def test_bi19_red_a_bare_extensionless_name_has_no_bare_fallback(self):
        """The r6 fold's own tail: `(token + ".exe", token)` tried the bare name.

        A searched directory holding ONLY an extensionless `witness` is a
        directory in which `CreateProcessW(NULL, "witness ...")` finds nothing:
        it appends `.exe` to a bare name and looks for `witness.exe`. The bare
        fallback resolved, hashed and certified `witness` anyway.
        """
        directory = os.path.dirname(
            self._write_file(os.path.join("bare-only", "witness"),
                             b"MZ an extensionless file on PATH\n"))
        with mock.patch.dict(os.environ, {"PATH": directory}):
            with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                self.smoke._candidate_digest("witness --arg")
        self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
        # And with the `.exe` present it resolves THAT, and only that.
        self._write_file(os.path.join("bare-only", "witness.exe"), b"MZ the exe\n")
        with mock.patch.dict(os.environ, {"PATH": directory}):
            resolved = self.smoke.resolve_candidate_image("witness --arg")
        self.assertEqual(["witness.exe"], resolved["attempted_file_names"])
        self.assertEqual(self._digest_of(os.path.join(directory, "witness.exe")),
                         resolved["candidate_artifact_digest"])

    # ---- bi20 ----------------------------------------------------------------------

    def test_bi20_red_an_unquoted_spaced_path_is_refused_by_name(self):
        """codex-CLI r7 P2: the successive-whitespace search is REFUSED, not faked.

        Learn, *CreateProcessW*, `lpApplicationName`: for
        "c:\\program files\\sub dir\\program name" the system "tries to interpret
        the possibilities in the following order: c:\\program.exe,
        c:\\program files\\sub.exe, c:\\program files\\sub dir\\program.exe,
        c:\\program files\\sub dir\\program name.exe".

        This driver models the FIRST possibility only. Pre-fix that produced
        `CANDIDATE_BINARY_NOT_FOUND:'...\\A'` — a generic not-found for a command
        line Windows launches perfectly well, on the one elevated session the
        owner gets. The refusal now NAMES the unsupported shape and the fix.
        """
        spaced = self._write_file(os.path.join("A B", "tool.exe"),
                                  b"MZ the image behind a spaced directory\n")
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest("%s --arg one" % spaced)
        message = str(refusal.exception)
        # THE RED: pre-fix this is CANDIDATE_BINARY_NOT_FOUND on the truncated
        # first token, which says nothing about what the operator should do.
        self.assertIn("SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED", message)
        self.assertIn("quote", message.lower())
        # The QUOTED form of the very same command line is untouched.
        self.assertEqual(self._digest_of(spaced),
                         self.smoke._candidate_digest('"%s" --arg one' % spaced))

    def test_bi20_red_an_unquoted_extensionless_path_with_arguments_is_refused(self):
        """The shape on which the two documented paragraphs DISAGREE.

        `lpCommandLine` says `.exe` is not appended to a name containing a path;
        the `lpApplicationName` enumeration appends `.exe` to each whitespace
        prefix (`c:\\program.exe`). With BOTH `tool` and `tool.exe` on disk those
        two readings select two different programs, and this function's whole
        purpose is that the hashed image and the launched image cannot differ. It
        refuses rather than pick one and certify it.
        """
        token = self._write_file(os.path.join("ambiguous", "tool"), b"MZ verbatim\n")
        self._write_file(os.path.join("ambiguous", "tool.exe"), b"MZ appended\n")
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest("%s --arg" % token)
        self.assertIn("SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED", str(refusal.exception))
        # Quoted, there is no ambiguity left to refuse: the quoted token is the
        # whole file name and `.exe` is not appended to a name carrying a path.
        self.assertEqual(self._digest_of(token),
                         self.smoke._candidate_digest('"%s" --arg' % token))
        # With NO arguments there is no second whitespace boundary to try, so
        # the single documented reading stands and the token resolves verbatim.
        self.assertEqual(self._digest_of(token),
                         self.smoke._candidate_digest(token))

    def test_bi20_guard_the_refusal_cannot_eat_a_shape_that_works(self):
        """GUARD — a refusal that swallowed the runbook's own command line would
        be a worse defect than the one it closes.

        The refusal fires ONLY where this driver's answer and `CreateProcessW`'s
        can differ: an unquoted command line with a further whitespace boundary
        whose first token does not resolve (Windows would go on to the next
        boundary), or whose two documented readings name different files. A
        first token that RESOLVES is the first possibility Windows tries and
        accepts, so those command lines are answered, not refused.
        """
        # (a) the runbook's default, unquoted, with arguments.
        system_cmd = shutil.which("cmd.exe")
        if system_cmd:
            self.assertEqual(self._digest_of(system_cmd),
                             self.smoke._candidate_digest("cmd.exe /c exit 0"))
            self.assertEqual(self._digest_of(system_cmd),
                             self.smoke._candidate_digest("cmd /c exit 0"))
        # (b) an unquoted ABSOLUTE path with no space in the token.
        plain = self._write_file(os.path.join("plain", "tool.exe"), b"MZ plain\n")
        self.assertEqual(self._digest_of(plain),
                         self.smoke._candidate_digest("%s --arg one" % plain))
        # (c) an absent binary with no further whitespace boundary keeps the
        #     honest not-found name; it is not relabelled as the space class.
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest(
                '"%s"' % os.path.join(self.directory, "absent.exe"))
        self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest("mbcx01-witness-no-such-candidate")
        self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))

    # ---- bi22 ----------------------------------------------------------------------

    def _documented_search_sequence(self, path_directory):
        """The six directories Learn enumerates, and what the module answers.

        `SystemRoot` is pointed at a temporary tree so steps 3-5 are exact
        strings rather than whatever this box happens to hold, and `windir` is
        removed so the fallback cannot answer for it.
        """
        root = os.path.join(self.directory, "winroot")
        os.makedirs(os.path.join(root, "System32"), exist_ok=True)
        os.makedirs(os.path.join(root, "System"), exist_ok=True)
        documented = [
            os.path.dirname(os.path.abspath(sys.executable)),   # 1. app load dir
            os.getcwd(),                                        # 2. parent cwd
            os.path.join(root, "System32"),                     # 3. 32-bit system
            os.path.join(root, "System"),                       # 4. 16-bit system
            root,                                               # 5. Windows dir
            path_directory,                                     # 6. PATH
        ]
        with mock.patch.dict(os.environ,
                             {"SystemRoot": root, "PATH": path_directory}):
            os.environ.pop("windir", None)
            answered = list(self.smoke._executable_search_directories())
        return answered, documented

    def test_bi22_red_the_bare_name_search_sequence_has_all_six_documented_steps(self):
        """The set member NOBODY named: the 16-bit Windows system directory.

        Learn, *CreateProcessW*, `lpCommandLine`, for a file name with no
        directory path: "1. The directory from which the application loaded.
        2. The current directory for the parent process. 3. The 32-bit Windows
        system directory... 4. The 16-bit Windows system directory. There is no
        function that obtains the path of this directory, but it is searched.
        The name of this directory is System. 5. The Windows directory...
        6. The directories that are listed in the PATH environment variable."

        SIX steps. The r6 fold's sweep enumerated FIVE — step 4 was simply not
        in the list — so a bare name resolvable in `%SystemRoot%\System`
        resolved to whatever a LATER directory held, or to nothing at all. This
        is the same class as the two findings codex named, found by walking the
        documented set instead of the reported instances, and it is a wrong
        NUMBER: `%SystemRoot%\System` is searched BEFORE the Windows directory
        and before PATH, so a collision there is decided the wrong way round.
        """
        directory = os.path.dirname(
            self._write_file(os.path.join("seq", "name.exe"), b"MZ seq\n"))
        answered, documented = self._documented_search_sequence(directory)
        # THE RED: pre-fix `answered` is the documented list with step 4 removed.
        self.assertEqual(documented, answered)
        self.assertIn(os.path.join(os.path.dirname(documented[2]), "System"),
                      answered)
        # ORDER is the evidence, not membership: the 16-bit directory is
        # searched AFTER System32 and BEFORE the Windows directory and PATH.
        self.assertLess(answered.index(documented[2]), answered.index(documented[3]))
        self.assertLess(answered.index(documented[3]), answered.index(documented[4]))
        self.assertLess(answered.index(documented[4]), answered.index(documented[5]))

    # ---- bi21 ----------------------------------------------------------------------

    def test_bi21_red_every_documented_resolution_rule_is_closed_by_name(self):
        """THE SET TABLE — one row per documented rule, each implemented or refused.

        Rows are quoted from Learn, *CreateProcessW*
        (`lpApplicationName` / `lpCommandLine`), the paragraphs that govern a
        NULL `lpApplicationName` — which is the call
        `mbcx01_build_win32.py:787-790` actually makes.
        """
        exe = self._write_file(os.path.join("set", "name.exe"), b"MZ name.exe\n")
        com = self._write_file(os.path.join("set", "other.com"), b"MZ other.com\n")
        pathy = self._write_file(os.path.join("set", "pathy"), b"MZ pathy\n")
        directory = os.path.dirname(exe)
        spaced = self._write_file(os.path.join("set", "S P", "tool.exe"), b"MZ SP\n")

        with mock.patch.dict(os.environ, {"PATH": directory, "PATHEXT": ".COM;.EXE"}):
            # R1 "If the file name does not contain an extension, .exe is
            #     appended." -> IMPLEMENTED, and it is the ONLY candidate.
            self.assertEqual(("name.exe",),
                             tuple(self.smoke._candidate_file_names("name")))
            self.assertEqual(self._digest_of(exe),
                             self.smoke._candidate_digest("name --arg"))
            # R2 "Therefore, if the file name extension is .com, this parameter
            #     must include the .com extension." -> IMPLEMENTED: a token that
            #     carries an extension is used AS GIVEN, and a bare `other` does
            #     not reach `other.com` however PATHEXT is spelled.
            self.assertEqual(("other.com",),
                             tuple(self.smoke._candidate_file_names("other.com")))
            self.assertEqual(self._digest_of(com),
                             self.smoke._candidate_digest("other.com --arg"))
            with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                self.smoke._candidate_digest("other --arg")
            self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))

        # R3a "If the file name ends in a period (.) with no extension ... .exe
        #      is not appended." -> IMPLEMENTED (verbatim, no candidates added).
        self.assertEqual(("name.",), tuple(self.smoke._candidate_file_names("name.")))
        # R3b "... or if the file name contains a path, .exe is not appended."
        #      -> IMPLEMENTED (bi19).
        self.assertEqual((pathy,), tuple(self.smoke._candidate_file_names(pathy)))
        self.assertEqual((os.path.join("rel", "sub", "tool"),),
                         tuple(self.smoke._candidate_file_names(
                             os.path.join("rel", "sub", "tool"))))
        self.assertEqual(self._digest_of(pathy),
                         self.smoke._candidate_digest(pathy))

        # R4 the search sequence for a bare name -> its own witness, bi22.
        self.assertEqual(6, len(self._documented_search_sequence(directory)[1]))
        # R4's exclusion is documented too: "this function does not search the
        # per-application path specified by the App Paths registry key." The
        # mechanical check, not a claim: no function on the RESOLUTION path
        # touches a registry or names that key. (The module DOES open registry
        # keys — `host_virtualization_facts` — which is why the check is scoped
        # to the resolution path instead of to the file.)
        resolution_source = "".join(
            inspect.getsource(function) for function in (
                self.smoke._executable_search_directories,
                self.smoke._candidate_file_names,
                self.smoke._split_command_line,
                self.smoke._unquoted_whitespace_ambiguity,
                self.smoke.resolve_candidate_image))
        self.assertNotIn("winreg", resolution_source)
        with open(self.smoke.__file__, encoding="utf-8") as stream:
            source = stream.read()
        self.assertNotIn("App Paths\\", source)

        # R5 the successive-whitespace interpretation -> REFUSED BY NAME (bi20).
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke._candidate_digest("%s --arg" % spaced)
        self.assertIn("SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED", str(refusal.exception))
        # R5b the same rule where the FIRST token carries NO PATH AT ALL -> also
        #     REFUSED BY NAME (bi23). The row above still has a path-carrying head
        #     (`...\set\S`); an unquoted RELATIVE spaced path does not, which is the
        #     shape the r7 reading of R5 could not see. ⚠ RIDER, FLAGGED: this row
        #     is NEW in the r8 fold; its own red is
        #     `test_bi23_red_a_relative_spaced_path_with_a_pathless_first_token_is_refused`.
        self._write_file(os.path.join("S P", "tool.exe"), b"MZ relative SP\n")
        with contextlib.chdir(self.directory):
            self.assertFalse(self.smoke._token_carries_a_path("S"))
            with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                self.smoke._candidate_digest(os.path.join("S P", "tool.exe") + " --arg")
        self.assertIn("SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED", str(refusal.exception))

        # R6 "use quoted strings to indicate where the file name ends and the
        #     arguments begin" -> IMPLEMENTED, and it is the documented fix the
        #     R5 refusal points the operator at.
        self.assertEqual(self._digest_of(spaced),
                         self.smoke._candidate_digest('"%s" --arg' % spaced))

        # And the refusal vocabulary is CLOSED: the module names every shape it
        # will not resolve, so none of them can arrive as a bare traceback.
        for sentinel in ("CANDIDATE_COMMAND_LINE_EMPTY",
                         "CANDIDATE_COMMAND_LINE_UNPARSEABLE",
                         "CANDIDATE_BINARY_NOT_FOUND",
                         "SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED"):
            self.assertIn(sentinel, source)


class SmokeRelativeSpacedPathWitnesses(unittest.TestCase):
    """bi23: the unquoted-space rule is a property of the COMMAND LINE, not its head.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 11e25e4be238327f36b6e562cafb6aa53cfb3a4532fa322d19a7cdff39e0a43c — the
    worktree checkout hashes the same, byte for byte), loaded from a scratch directory
    placed at `sys.path[0]`; the runner PRINTS the bound module's `__file__` and sha256
    and ASSERTS the pre-fix copy won.

    codex-CLI r8 P2 — THE r7 FOLD'S OWN NEIGHBOUR. bi20 closed the unquoted spaced path
    by refusing it BY NAME, but its third condition asked whether the FIRST TOKEN
    carries a path. An unquoted RELATIVE spaced path does not have one by construction:
    `tools dir\\app.exe --arg` splits to `tools`, which is a bare name, so the guard
    early-returned and the operator got `CANDIDATE_BINARY_NOT_FOUND:'tools'` — a generic
    not-found, with no guidance, for a command line `CreateProcessW` launches perfectly
    well at its SECOND whitespace boundary. Same class as bi20, one shape lower: a
    refusal whose message names neither the problem nor the one-character fix, spent on
    the one elevated session the owner gets.

    The close asks the question the documented rule actually poses — is there a later
    whitespace boundary that names a file Windows would go on to try? — and only a
    prefix that EXISTS ON DISK counts. That existence check is doing real work and not
    decoration: `ntpath.dirname("cmd /c")` is `"cmd "`, so the runbook's own
    `cmd /c exit 0` looks path-carrying at its second boundary and is saved from the
    refusal only by not being a file.

    ⛔ Nothing here launches a process, creates a Job or opens an ETW session. Only
    `resolve_candidate_image` / `_candidate_digest` are called and every file they read
    lives in a temporary directory.
    """

    maxDiff = None

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.directory = tempfile.mkdtemp(prefix="mbcx01-relative-space-")
        self.addCleanup(shutil.rmtree, self.directory, True)
        os.makedirs(os.path.join(self.directory, "tools dir"))
        os.makedirs(os.path.join(self.directory, "sub"))
        self.spaced = self._write(os.path.join("tools dir", "app.exe"),
                                  b"MZ behind a RELATIVE spaced directory\n")
        self.plain = self._write(os.path.join("sub", "plain.exe"),
                                 b"MZ a space-free relative\n")

    def _write(self, relative, data):
        path = os.path.join(self.directory, relative)
        with open(path, "wb") as stream:
            stream.write(data)
        return path

    def _digest_of(self, path):
        with open(path, "rb") as stream:
            return measurement.sha384(stream.read())

    def test_bi23_red_a_relative_spaced_path_with_a_pathless_first_token_is_refused(self):
        """codex-CLI r8 P2: the named refusal, not a generic not-found.

        THE RED: pre-fix both spellings abort `CANDIDATE_BINARY_NOT_FOUND:'tools'`.
        """
        with contextlib.chdir(self.directory):
            for command_line in (r"tools dir\app.exe --arg one",
                                 "tools dir/app.exe --arg"):
                with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                    self.smoke._candidate_digest(command_line)
                message = str(refusal.exception)
                self.assertIn(self.smoke.UNQUOTED_SPACE_PATH_UNSUPPORTED, message)
                self.assertNotIn("CANDIDATE_BINARY_NOT_FOUND", message)
                # The refusal NAMES the boundary that made it ambiguous and the fix.
                self.assertIn("quote", message.lower())
                self.assertIn("tools", message)
            # The QUOTED form of the very same command line is untouched.
            self.assertEqual(
                self._digest_of(self.spaced),
                self.smoke._candidate_digest(r'"tools dir\app.exe" --arg one'))

    def test_bi23_red_the_extended_prefixes_are_the_documented_possibilities(self):
        """The enumeration itself, asserted rather than trusted.

        Learn, *CreateProcessW*, `lpApplicationName`: the possibilities for
        `c:\\program files\\sub dir\\program name` are the whitespace-delimited
        PREFIXES, in increasing length. THE RED: pre-fix neither
        `_whitespace_extended_prefixes` nor `_extended_prefix_naming_a_file` exists,
        so nothing in the module could see past the first token.
        """
        # Learn's own four possibilities for this command line are
        #   1. c:\program.exe                        <- the first token, answered
        #   2. c:\program files\sub.exe
        #   3. c:\program files\sub dir\program.exe
        #   4. c:\program files\sub dir\program name.exe
        # and 2-4 are exactly what this returns, minus the `.exe` the caller adds.
        self.assertEqual(
            (r"c:\program files\sub",
             r"c:\program files\sub dir\program",
             r"c:\program files\sub dir\program name"),
            self.smoke._whitespace_extended_prefixes(
                r"c:\program files\sub dir\program name"))
        # The FIRST token is dropped: it is the possibility already answered.
        self.assertEqual((), self.smoke._whitespace_extended_prefixes("cmd"))
        self.assertEqual(("cmd /c", "cmd /c exit", "cmd /c exit 0"),
                         self.smoke._whitespace_extended_prefixes(" cmd /c exit 0 "))
        with contextlib.chdir(self.directory):
            self.assertEqual(
                os.path.join("tools dir", "app.exe"),
                self.smoke._extended_prefix_naming_a_file(
                    r"tools dir\app.exe --arg"))
            # `cmd /c` is path-carrying to ntpath and is NOT a file, so it is not a
            # possibility — the existence check is the guard, not the path check.
            self.assertTrue(self.smoke._token_carries_a_path("cmd /c"))
            self.assertIsNone(
                self.smoke._extended_prefix_naming_a_file("cmd /c exit 0"))

    def test_bi23_guard_the_wider_refusal_still_cannot_eat_a_shape_that_works(self):
        """GUARD — widening a refusal is where a fix becomes the next defect.

        Every one of these was answered before this fold and is answered after it.
        """
        with contextlib.chdir(self.directory):
            system_cmd = shutil.which("cmd.exe")
            if system_cmd:
                for command_line in ("cmd /c exit 0", "cmd.exe /c exit 0"):
                    self.assertEqual(self._digest_of(system_cmd),
                                     self.smoke._candidate_digest(command_line))
            # space-free relatives, both separators
            for command_line in (r"sub\plain.exe --arg", "sub/plain.exe --arg"):
                self.assertEqual(self._digest_of(self.plain),
                                 self.smoke._candidate_digest(command_line))
            # an absent bare name keeps the honest not-found name, with and without
            # a further whitespace boundary
            for command_line in ("mbcx01-witness-no-such-candidate --arg",
                                 "mbcx01-witness-no-such-candidate"):
                with self.assertRaises(self.smoke.SmokeAbort) as refusal:
                    self.smoke._candidate_digest(command_line)
                self.assertIn("CANDIDATE_BINARY_NOT_FOUND", str(refusal.exception))
            # an absolute space-free path with arguments is still answered
            self.assertEqual(self._digest_of(self.plain),
                             self.smoke._candidate_digest("%s --arg" % self.plain))


class SmokeRuntimeEnvironmentEvidenceWitnesses(unittest.TestCase):
    """bi24: the signed environment record carries RUNTIME facts, honestly labelled.

    codex-CLI r9 F3. `host_virtualization_facts()` answered `hypervisor_present` from
    the EXISTENCE of installed-component registry keys — `Services\\vmicheartbeat` and
    `CurrentVersion\\Virtualization` — and labelled the whole record
    `REGISTRY_SERVICE_PRESENCE`. Those keys persist when the component is installed and
    NOT RUNNING, so the record asserted a runtime fact it had only install-time evidence
    for, and that record is signed into the measurement envelope as the environment the
    cell ran in. Measured on the build host (2026-08-17, an ordinary bare-metal
    desktop): `Services\\vmicheartbeat` EXISTS and its service state is `Stopped`; the
    same host has `hvservice` and no `vmms`, and WMI reports a hypervisor IS present
    (VBS), so both of the pre-fix signals were wrong about it in different directions.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 312a8b8d3bbed302f4ddccd995beb3c9b2f4d1162ea5c4e4af9465c97cbbda4b, loaded
    from a scratch directory placed at `sys.path[0]`; the runner prints the bound
    module's `__file__` and sha256 and the class asserts which copy won):

        FAIL: ...bi24_red_installed_but_inactive_components_are_not_a_running_hypervisor
        AssertionError: True is not false : pre-fix `hypervisor_present` was TRUE for a
        host whose ONLY hypervisor evidence is an installed, inactive component

        FAIL: ...bi24_red_a_guest_is_not_a_root_partition_because_the_role_is_installed
        AssertionError: True is not false

    THE HARNESS INJECTS THE REGISTRY, NOT THE ANSWER. A fake `winreg` module is placed
    in `sys.modules` for the duration of each arm, which is the seam BOTH the pre-fix
    and the post-fix code read (each does a local `import winreg`), so the two sides are
    asked the same question about the same host state. The RUNTIME probe is stubbed only
    where a deterministic answer is needed, and through `getattr(..., None)`, so this
    witness still RUNS against pre-fix bytes that do not have the symbol — a red that
    errors on a missing attribute proves nothing about behaviour.

    ⛔ Nothing here starts a session, launches a candidate, or touches the real registry
    in the injected arms. The one arm that touches the live host runs the read-only
    runtime probe and asserts only its CONTRACT, never this machine's answer.
    """

    maxDiff = None

    GUEST_COMPONENT_KEYS = (
        r"SYSTEM\CurrentControlSet\Services\vmicheartbeat",
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization",
    )
    HOST_COMPONENT_KEYS = (
        r"SYSTEM\CurrentControlSet\Services\hvservice",
        r"SYSTEM\CurrentControlSet\Services\vmms",
    )

    class _FakeWinreg:
        """The registry as ONE host has it: a set of keys that EXIST. Nothing else."""

        HKEY_LOCAL_MACHINE = "HKLM.WITNESS"

        def __init__(self, present):
            self.present = set(present)
            self.asked = []

        def OpenKey(self, root, path):  # noqa: N802 - the winreg spelling
            self.asked.append(path)
            if path in self.present:
                return contextlib.nullcontext()
            raise OSError(2, "witness: key does not exist", path)

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        if os.name != "nt":
            self.skipTest("host_virtualization_facts is a Windows probe")

    def _with_registry(self, present):
        patch = mock.patch.dict(sys.modules, {"winreg": self._FakeWinreg(present)})
        patch.start()
        self.addCleanup(patch.stop)

    def _with_runtime(self, **facts):
        """Stub the RUNTIME probe when the bytes under test have one; skip when not.

        Deliberately not `create=True`: patching a symbol into a module that does not
        have it would make the pre-fix run fail on the PATCH instead of on the
        behaviour, and a red has to fail for its own reason.
        """
        if getattr(self.smoke, "runtime_virtualization_facts", None) is None:
            return
        answer = {"probe": self.smoke.RUNTIME_HYPERVISOR_PROBE,
                  "query": "WITNESS-STUB", "resolved_path": "WITNESS-STUB",
                  "hypervisor_present": None,
                  "guest_integration_services_running": None, "error": None}
        answer.update(facts)
        patch = mock.patch.object(self.smoke, "runtime_virtualization_facts",
                                  lambda: answer)
        patch.start()
        self.addCleanup(patch.stop)

    def test_bi24_red_installed_but_inactive_components_are_not_a_running_hypervisor(self):
        """THE RED: install-time evidence signed as a runtime fact.

        The injected host is the reported shape — the guest-integration component keys
        EXIST (they ship with Windows) and no hypervisor is running.
        """
        self._with_registry(self.GUEST_COMPONENT_KEYS)
        self._with_runtime(hypervisor_present=False,
                           guest_integration_services_running=[])
        facts = self.smoke.host_virtualization_facts()
        self.assertIs(False, facts["hypervisor_present"],
                      "pre-fix `hypervisor_present` was TRUE for a host whose ONLY "
                      "hypervisor evidence is an installed, inactive component")
        self.assertEqual("RUNTIME_FACT", facts["hypervisor_present_determination"])
        # The registry evidence is not discarded — it is recorded AS WHAT IT IS.
        self.assertIs(True, facts["hypervisor_guest_components_installed"])
        self.assertIs(False, facts["hypervisor_host_components_installed"])
        self.assertEqual("RUNTIME_WMI_HYPERVISOR_PLUS_REGISTRY_INSTALLED_COMPONENTS",
                         facts["probe"])
        # ...and the classifier is handed the RUNTIME fact, so this host is what it is.
        environment = self.smoke.etw.classify_execution_environment(
            hypervisor_present=facts["hypervisor_present"],
            is_root_partition=facts["is_root_partition"],
            nested_virtualization=False,
            host_architecture=facts["host_architecture"])
        self.assertEqual("BARE_METAL_WINDOWS", environment["execution_environment"])

    def test_bi24_red_a_guest_is_not_a_root_partition_because_the_role_is_installed(self):
        """THE RED: `a guest can classify as root`.

        A GUEST with the Hyper-V host components installed had `is_root_partition` TRUE
        from the key's existence alone, and classified `HYPER_V_ROOT_PARTITION` — the
        one virtualized classification the smoke authorization treats as eligible. The
        runtime fact that Hyper-V guest integration services are RUNNING (they run
        inside the VM) contradicts that reading, and a contradicted reading is refused.
        """
        self._with_registry(self.GUEST_COMPONENT_KEYS + self.HOST_COMPONENT_KEYS)
        self._with_runtime(hypervisor_present=True,
                           guest_integration_services_running=["vmicheartbeat",
                                                               "vmictimesync"])
        facts = self.smoke.host_virtualization_facts()
        self.assertIs(True, facts["hypervisor_present"])
        self.assertIs(False, facts["is_root_partition"])
        self.assertEqual("REFUSED_RUNTIME_GUEST_INTEGRATION_SERVICES_RUNNING",
                         facts["root_partition_determination"])
        self.assertEqual(["vmicheartbeat", "vmictimesync"],
                         facts["hypervisor_guest_services_running"])
        # The installed evidence is still recorded; it just does not decide.
        self.assertIs(True, facts["hypervisor_host_components_installed"])
        with self.assertRaises(self.smoke.etw.EtwConsumerFault) as refusal:
            self.smoke.etw.classify_execution_environment(
                hypervisor_present=facts["hypervisor_present"],
                is_root_partition=facts["is_root_partition"],
                nested_virtualization=False,
                host_architecture=facts["host_architecture"])
        self.assertIn("SMOKE_ENVIRONMENT_IS_A_VIRTUALIZATION_GUEST",
                      str(refusal.exception))

    def test_bi24_red_an_unanswerable_probe_is_undetermined_not_bare_metal(self):
        """THE RED: `None` must never fall through to the cheapest classification.

        A runtime probe that cannot run leaves the posture UNDETERMINED. Classifying on
        it would sign `BARE_METAL_WINDOWS` — exactly the answer a falsy default
        produces — into the envelope. `preflight` refuses instead, before the elevation
        check and before any capability probe, and names what could not be answered.
        """
        self._with_registry(self.GUEST_COMPONENT_KEYS)
        self._with_runtime(hypervisor_present=None,
                           error="RUNTIME_VIRTUALIZATION_SHELL_NOT_ON_PATH")
        facts = self.smoke.host_virtualization_facts()
        self.assertIsNone(facts["hypervisor_present"])
        self.assertEqual("UNDETERMINED", facts["hypervisor_present_determination"])
        self.assertEqual("RUNTIME_VIRTUALIZATION_SHELL_NOT_ON_PATH",
                         facts["hypervisor_present_probe_error"])

        for patch in (mock.patch.object(self.smoke, "read_authorization",
                                        lambda path: {"authorization_path": "STUB"}),
                      mock.patch.object(self.smoke, "is_elevated", lambda: True)):
            patch.start()
            self.addCleanup(patch.stop)
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self.smoke.preflight("WITNESS-NOT-READ", operator_confirms_not_nested=True)
        self.assertIn("HYPERVISOR_RUNTIME_POSTURE_UNDETERMINED", str(refusal.exception))
        self.assertIn("RUNTIME_VIRTUALIZATION_SHELL_NOT_ON_PATH",
                      str(refusal.exception))

    def test_bi24_guard_the_runtime_probe_is_expressible_on_this_host(self):
        """GUARD — a probe that only exists on paper is not a runtime fact.

        This arm asks the LIVE host, read-only, and asserts the probe's CONTRACT rather
        than any particular answer (the answer is a property of whichever machine runs
        the suite, and a witness must not assert a machine): `hypervisor_present` is a
        bool or `None`, and `None` always arrives with a stated reason.
        """
        facts = self.smoke.runtime_virtualization_facts()
        print("\nbi24 live runtime probe: %s" % json.dumps(
            {key: value for key, value in facts.items() if key != "query"},
            sort_keys=True))
        self.assertEqual(self.smoke.RUNTIME_HYPERVISOR_PROBE, facts["probe"])
        self.assertIn(type(facts["hypervisor_present"]), (bool, type(None)))
        if facts["hypervisor_present"] is None:
            self.assertIsNotNone(facts["error"])
        else:
            self.assertIsNone(facts["error"])
            self.assertIsInstance(facts["guest_integration_services_running"], list)
        # The citation the probe rests on is the one the module's query actually names.
        self.assertIn("Win32_ComputerSystem", self.smoke.RUNTIME_VIRTUALIZATION_QUERY)
        self.assertIn("HypervisorPresent", self.smoke.RUNTIME_VIRTUALIZATION_QUERY)


class SmokeFixedCandidateIdentityWitnesses(unittest.TestCase):
    """bi25: a FIXED candidate id certifies the invocation it names, and no other.

    codex-CLI r9 F4. `smoke_identity()` signs the fixed
    `CANDIDATE.BUILD.B.SMOKE.CMD-EXIT-0` with an artifact digest taken over the IMAGE
    ONLY, so a supported non-default `--command-line` produced an envelope certifying
    DIFFERENT work under that identity — and because both invocations run the same
    `cmd.exe` bytes, the digest cannot tell them apart. `cmd.exe /c whoami` is the
    smallest example, and it is a supported command line: `run-smoke-cell.ps1` passes
    `-CommandLine` straight through to `--command-line`.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_smoke_cell.py`,
    sha256 312a8b8d3bbed302f4ddccd995beb3c9b2f4d1162ea5c4e4af9465c97cbbda4b):

        FAIL: ...bi25_red_a_different_invocation_is_not_this_candidate
        AssertionError: SmokeAbort not raised

    ⚖ THIS REFUSES A WRONG RECORD, NOT A PERSON (owner ruling 2026-08-16, the same one
    that turned `authorization_mirror` into a mirror). It reads no authorization
    document, asks nothing about who is running, and stops nothing the declared
    candidate does. The alternative close — minting a fresh candidate id and an
    argument-covering artifact digest per command line — is new machinery and is not
    built here; the refusal says so and names what to do instead.

    ⛔ Nothing here starts a session or launches a candidate. The refusal is asserted to
    fire BEFORE any host probe: `is_elevated` records that it was reached and the
    consumer stub raises if a PMU probe is ever started.
    """

    maxDiff = None

    REFUSAL = "SMOKE_COMMAND_INCONSISTENT_WITH_CANDIDATE_IDENTITY"

    def setUp(self):
        import mbcx01_smoke_cell
        self.smoke = mbcx01_smoke_cell
        self.absolute = shutil.which("cmd.exe")
        if not self.absolute:
            self.skipTest("the declared smoke candidate resolves cmd.exe")
        self.probed = []
        consumer = types.SimpleNamespace(
            _win32=None,
            _resolve_profile_source_id=lambda name: 7,
            _query_capability_facts=lambda source_id: {"WITNESS": "STUB"})
        for patch in (
                mock.patch.object(self.smoke, "read_authorization",
                                  lambda path: {"authorization_path": "STUB"}),
                mock.patch.object(self.smoke, "authorization_mirror",
                                  lambda *a, **k: {"posture": "WITNESS-STUB"}),
                mock.patch.object(self.smoke, "is_elevated",
                                  lambda: self.probed.append("is_elevated") or True),
                mock.patch.object(self.smoke, "host_virtualization_facts", lambda: {
                    "hypervisor_present": False, "is_root_partition": False,
                    "nested_virtualization_readable": False,
                    "host_architecture": "WINDOWS_64BIT", "probe": "WITNESS_STUB"}),
                mock.patch.object(self.smoke, "node_runtime_facts",
                                  lambda: {"runnable": True, "error": None,
                                           "version": "WITNESS-STUB"}),
                mock.patch.object(self.smoke, "signature_verifier_facts",
                                  lambda: {"present": True, "error": None}),
                mock.patch.object(self.smoke.etw, "EtwPmcConsumer", lambda: consumer),
                mock.patch.object(self.smoke.etw, "_etw_win32", lambda: None),
                mock.patch.object(self.smoke.etw, "granted_capability_facts",
                                  lambda **kwargs: {"WITNESS": "STUB"}),
                mock.patch.object(self.smoke.etw, "evaluate_evidence_availability",
                                  lambda **kwargs: (True, ()))):
            patch.start()
            self.addCleanup(patch.stop)

    def _preflight(self, command_line):
        return self.smoke.preflight(
            "WITNESS-NOT-READ", operator_confirms_not_nested=True,
            command_line=command_line, cell=(0, 0, 0))

    def test_bi25_red_a_different_invocation_is_not_this_candidate(self):
        """THE RED: `cmd.exe /c whoami` proceeded under the fixed identity."""
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self._preflight("cmd.exe /c whoami")
        sentence = str(refusal.exception)
        self.assertIn(self.REFUSAL, sentence)
        # The message names the FIXED id and the invocation it stands for, so the
        # operator reads what this driver measures rather than a bare code.
        self.assertIn("CANDIDATE.BUILD.B.SMOKE.CMD-EXIT-0", sentence)
        self.assertIn("cmd.exe /c exit 0", sentence)
        self.assertIn("arguments=", sentence)
        # ...and it fired on the RESOLUTION path, before any host probe.
        self.assertEqual([], self.probed)

    def test_bi25_red_a_different_image_under_the_same_id_is_refused_too(self):
        """The other axis: the arguments agree and the IMAGE does not."""
        directory = tempfile.mkdtemp(prefix="mbcx01-smoke-bi25-")
        self.addCleanup(shutil.rmtree, directory, True)
        other = os.path.join(directory, "not-cmd.exe")
        with open(other, "wb") as stream:
            stream.write(b"MZ witness candidate bytes\n")
        with self.assertRaises(self.smoke.SmokeAbort) as refusal:
            self._preflight('"%s" /c exit 0' % other)
        sentence = str(refusal.exception)
        self.assertIn(self.REFUSAL, sentence)
        self.assertIn("image=", sentence)
        self.assertEqual([], self.probed)

    def test_bi25_guard_the_default_and_the_documented_variants_are_untouched(self):
        """GUARD — the runbook's own invocation must still run.

        Every spelling below IS this candidate: the runbook default
        (`cmd.exe /c exit 0`, `run-smoke-cell.ps1`'s `-CommandLine` default), the
        extensionless form FOLD-3B exists to accept, the resolved-and-quoted absolute
        form the 2026-08-16 re-entry note records the collector being handed, the
        unquoted absolute form, and a case/whitespace variant of the arguments. A
        refusal that ate any of these would be the next defect, not the fix.
        """
        for command_line in ("cmd.exe /c exit 0",
                             "cmd /c exit 0",
                             '"%s" /c exit 0' % self.absolute,
                             "%s /c exit 0" % self.absolute,
                             "cmd.exe /C  EXIT 0"):
            with self.subTest(command_line=command_line):
                self.probed.clear()
                report = self._preflight(command_line)
                self.assertEqual(
                    os.path.normcase(self.absolute),
                    os.path.normcase(report["candidate_image"]["image_path"]))
                # The preflight went ON past the candidate check, as it always did.
                self.assertEqual(["is_elevated"], self.probed)
                self.assertTrue(report["pmu_available"])
