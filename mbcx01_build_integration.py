"""BUILD integration — ONE connected authority graph across BUILD A and BUILD B.

This module assembles the complete authority graph the r13.2 handoff's "Integration
boundary" section asks for, and nothing else. It is a FIXTURE ASSEMBLY module, not a
new authority: every admission decision it reports is produced by calling the reviewed
BUILD verifiers unchanged —

  * `mbcx01_build_state_authority.verify_production_scorer_input` for state admission,
  * `mbcx01_build_measurement_authority.evaluate_production_measurement` for physical
    measurement admission,
  * `mbcx01_build_exactness_authority.verify_production_carrier_exactness` for carrier
    exactness,

and the frozen r13.2 verifiers still run inside those, unmodified. This module adds no
error code, discharges no sentinel, and holds no key.

WHY IT IMPORTS THE TEST MODULES (stated plainly rather than hidden)
------------------------------------------------------------------
The simulated Windows collections, the in-memory simulated `MeasurementTrustRootManifestV3`,
the committed FIXTURE-ONLY Ed25519 test keys and the state identity configuration are
defined once, in `test_mbcx01_build_state` / `test_mbcx01_build_measurement`. This module
imports those definitions instead of copying them. A second copy of simulated evidence
would be free to drift from the copy the witnesses check — and simulated evidence that
nobody can tell apart from the tested copy is exactly the failure mode the handoff calls
"fixture evidence crossing production admission". One definition, one place.

EVERY PIECE OF EVIDENCE HERE IS SIMULATED OR FIXTURE
----------------------------------------------------
- the state transition is the frozen `packet_fixture_manifest` graph, committed to a
  real SQLite `SingleWriterStateStore` in a temporary directory;
- the measurement grid is 100 SIMULATED in-memory collections; no Windows Job is
  created, no ETW session is opened, no candidate process is started;
- both trust roots are test material: the committed state manifest is
  `production_ready:false`, and the measurement manifest is built in memory and never
  written to disk, with `activation_authority: SIMULATED_TEST_INJECTION_ONLY`;
- no provider, model, network or paid call is made, and the 100-cell physical grid,
  the 4,608 scientific calls and the 456 route-qualification trials are NOT run.

`build_connected_authority_fixture()` returns the whole graph, including its own
`simulation_labels` block, so a caller cannot pick up a node of it and mistake it for
production evidence.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from typing import Any

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_exactness_authority as exactness
import mbcx01_build_measurement_authority as measurement_authority
import mbcx01_build_state_adapter as state_adapter
import mbcx01_build_state_authority as state_authority
import mbcx01_build_state_store as store_mod
import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets

# Fixture definitions (see the module docstring for why these come from the witnesses).
from test_mbcx01_build_measurement import (
    RUN_ID as MEASUREMENT_RUN_ID,
    simulated_collections,
    simulated_custody_evidence,
    simulated_production_grid,
    simulated_production_manifest,
)
from test_mbcx01_build_state import (
    ANTI_REPLAY_ANCHORS,
    IDENTITY_CONFIG as STATE_IDENTITY_CONFIG,
    TRANSACTION_ID,
    _FixtureSigner as StateFixtureSigner,
    _production_state_manifest as production_state_trust_root_manifest,
    _state_custody_evidence as state_custody_evidence,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
STORE_FILE_NAME = "mbcx01-build-integration-state.sqlite3"
NO_PAID_REPORT = "MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json"

#: Facts the frozen r13.2 no-paid report must still assert. The integration run reads
#: them from the committed report; it never restates them from memory.
NO_PAID_REPORT_FACTS = {
    "experiment_executed": False,
    "paid_calls": 0,
    "provider_calls": 0,
    "physical_harness_executed": False,
}

SIMULATION_LABELS = {
    "state_transition": "FROZEN_FIXTURE_PACKET_GRAPH",
    "state_store": "REAL_SQLITE_FILE_STORE_IN_A_TEMPORARY_DIRECTORY",
    "state_signing_key": "COMMITTED_FIXTURE_ONLY_ED25519_TEST_KEY",
    "state_trust_root": "IN_MEMORY_SIMULATED_PRODUCTION_SHAPE_OVER_FIXTURE_ONLY_KEYS",
    "owner_trust_anchor":
        "IN_MEMORY_TEST_PRODUCTION_ANCHOR_SCOPED_TO_THIS_ASSEMBLY_AND_RESTORED_ON_EXIT",
    "measurement_collections": "SIMULATED_IN_MEMORY_NO_WINDOWS_JOB_NO_ETW",
    "measurement_trust_root": "IN_MEMORY_SIMULATED_TEST_INJECTION_ONLY",
    "measurement_signing_key": "COMMITTED_FIXTURE_ONLY_ED25519_TEST_KEY",
    "physical_execution": "NOT_RUN",
    "provider_calls": "NOT_MADE",
    "production_activation": "NOT_PERFORMED",
}


def frozen_no_paid_report() -> dict[str, Any]:
    """Read the committed r13.2 no-paid verification report (never restate it)."""
    with open(os.path.join(ROOT, NO_PAID_REPORT), encoding="utf-8") as stream:
        return json.load(stream)


def build_connected_authority_fixture(*, workspace: str | None = None) -> dict[str, Any]:
    """Assemble and return the ONE connected authority graph.

    Flow, end to end, with no step faked and no verifier bypassed:

      frozen `packet_fixture_manifest` -> frozen `build_scoring_fixture` scorer input
        -> the same transition committed through the REAL file-backed
           `SingleWriterStateStore` (durable anti-replay anchors included)
        -> `mbcx01_build_state_adapter` mints a signed `StateAuthorityReceiptV2` from
           the durable rows through a custody-injected FIXTURE signer
        -> the store is CLOSED, so the receipt is verified from the durable path alone
        -> `verify_production_scorer_input` discharges exactly the one named sentinel
      100 simulated collections
        -> `produce_signed_measurement_receipt_v2` mints 100 `SignedMeasurementReceiptV2`
        -> `evaluate_production_measurement` admits them against the in-memory
           simulated manifest
        -> `verify_production_carrier_exactness` binds the V3 exactness receipt to the
           pinned suite, the exact carrier artifact, the exact harness build and the
           exact grid identity of THAT envelope set.

    The caller owns the returned `workspace` directory (`release_connected_authority_fixture`).

    OPERATOR WIRING, SCOPED — the r1 fix class's whole point, with the r2 fixture
    isolation on top. The verifier context is installed HERE, at graph construction, and
    never from any argument of the admission calls below; it is a TEST PRODUCTION anchor
    generated in memory, because after the r2 fold a `fixture_only` anchor grants
    nothing; and it is installed for the LENGTH OF THIS ASSEMBLY ONLY. Codex r2 F3 is
    exactly the missing scope: this module used to install the committed fixture anchor
    process-wide and never restore it, so every later verification in the process ran
    under a root the operator never chose. This module is a FIXTURE ASSEMBLER, not an
    operator, and it now behaves like one.
    """
    with trust_anchor.installed_production_verifier(
            ceremony.test_production_anchor_document(),
            current_time=ceremony.TEST_VERIFIER_INSTANT):
        return _assemble(workspace)


def _assemble(workspace: str | None) -> dict[str, Any]:
    """Assemble the graph INSIDE the caller-scoped verifier context."""
    workspace = workspace or tempfile.mkdtemp(prefix="mbcx01-build-integration-")
    store_path = os.path.join(workspace, STORE_FILE_NAME)

    # ---- BUILD A: frozen packet graph -> durable store -> V2 receipt -> admission ----
    manifest = packets.packet_fixture_manifest()
    scorer_input = packets.build_scoring_fixture(manifest, "OM")
    transition = scorer_input["transition_authority"]
    transition_request = {
        "transaction_commit_id": TRANSACTION_ID,
        "prestate": json.loads(json.dumps(transition["precommit_state"])),
        "proposal_event": json.loads(json.dumps(transition["proposal_event"])),
        "applied_child_event": json.loads(json.dumps(transition["applied_child_event"])),
    }
    state_trust_root_manifest = production_state_trust_root_manifest()
    state_custody = state_custody_evidence(state_trust_root_manifest)
    store = store_mod.SingleWriterStateStore.open_verified(
        store_path, store_id=STATE_IDENTITY_CONFIG["store_id"],
        namespace=STATE_IDENTITY_CONFIG["namespace"],
        namespace_version=STATE_IDENTITY_CONFIG["namespace_version"])
    try:
        terminal = store.commit_transition(transition_request,
                                           anti_replay=ANTI_REPLAY_ANCHORS)
        durable_anchors = store.anti_replay_anchors(TRANSACTION_ID)
        state_receipt = state_adapter.produce_state_authority_receipt_v2(
            store, transition_request, signer=StateFixtureSigner,
            identity_config=STATE_IDENTITY_CONFIG,
            trust_root_manifest=state_trust_root_manifest)
    finally:
        # Closed on purpose: the connected graph must verify from the DURABLE bytes,
        # not from the privilege of holding the writer object.
        store.close()

    state_admission_errors = state_authority.verify_production_scorer_input(
        scorer_input, state_receipt, expected_manifest=manifest,
        trust_root_manifest=state_trust_root_manifest,
        custody_evidence=state_custody, store_path=store_path)

    # ---- BUILD B: simulated grid -> signed V2 envelopes -> admission -> exactness ----
    collections = simulated_collections()
    measurement_envelopes = simulated_production_grid(collections)
    measurement_trust_root_manifest = simulated_production_manifest()
    measurement_custody_evidence = simulated_custody_evidence(
        measurement_trust_root_manifest)
    measurement_admission_errors = measurement_authority.evaluate_production_measurement(
        measurement_envelopes, trust_root_manifest=measurement_trust_root_manifest,
        custody_evidence=measurement_custody_evidence,
        expected_run_id=MEASUREMENT_RUN_ID)

    with open(os.path.join(ROOT, measurement.EXACTNESS_SUITE), encoding="utf-8") as stream:
        exactness_suite = json.load(stream)
    exactness_receipt = exactness.verify_production_carrier_exactness(
        {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID},
        envelopes=measurement_envelopes, suite_document=exactness_suite,
        trust_root_manifest=measurement_trust_root_manifest,
        custody_evidence=measurement_custody_evidence)

    return {
        "workspace": workspace,
        "expected_manifest": manifest,
        "scorer_input": scorer_input,
        "transition_request": transition_request,
        "store_path": store_path,
        "store_identity": {
            "store_id": STATE_IDENTITY_CONFIG["store_id"],
            "namespace": STATE_IDENTITY_CONFIG["namespace"],
            "namespace_version": STATE_IDENTITY_CONFIG["namespace_version"]},
        "state_terminal": terminal,
        "durable_anti_replay_anchors": durable_anchors,
        "state_receipt": state_receipt,
        "state_trust_root_manifest": state_trust_root_manifest,
        "state_custody_evidence": state_custody,
        "state_admission_errors": state_admission_errors,
        "measurement_collections": collections,
        "measurement_envelopes": measurement_envelopes,
        "measurement_trust_root_manifest": measurement_trust_root_manifest,
        "measurement_custody_evidence": measurement_custody_evidence,
        "measurement_admission_errors": measurement_admission_errors,
        "exactness_suite": exactness_suite,
        "exactness_receipt": exactness_receipt,
        "simulation_labels": dict(SIMULATION_LABELS),
    }


def release_connected_authority_fixture(graph: dict[str, Any]) -> None:
    """Remove the temporary workspace the connected fixture created."""
    workspace = graph.get("workspace")
    if workspace and os.path.isdir(workspace):
        shutil.rmtree(workspace, ignore_errors=True)
