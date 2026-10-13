"""BUILD A — operator-independence twin, operator B (GREEN STAGE).

Independently derives `StateAuthorityReceiptV2` CONTENT from the same durable store
bytes. It shares ONLY the closed schema and the frozen hashing primitives with operator 1
(`mbcx01_build_state_adapter`); it does not import the adapter, and it re-derives every
field (read ids, canonical bytes, hashes, cuts, sequence, persistence identity) from the
store rows itself, with its own connection, its own SQL, and its own calls into the frozen
`mbcx01_r13_common` primitives.

Operator B recomputes every hash from the canonical BYTES it reads; it never copies the
hash columns the writer stored. A writer that stored a hash disagreeing with its own bytes
therefore shows up as operator disagreement, not as silent agreement.

The gate is byte-identical receipt CONTENT (the signed preimage region, i.e. the receipt
without `receipt_preimage_b64` / `signature_b64` / `receipt_digest`). A poisoned finalizer
must produce DETECTED disagreement, never a silently-averaged result.

Operator B never signs and never holds signer custody; it cannot mint authority alone.
"""

from __future__ import annotations

import glob
import json
import os
from typing import Any

import mbcx01_r13_common as common

import mbcx01_build_state_store as store_mod


OPERATOR_B_ID = "MBCX01.BUILD.STATE.OPERATOR.B"
V2_SCHEMA_ID = "StateAuthorityReceiptV2"
V2_DOMAIN = "MBCX01.STATE.AUTHORITY"
V2_VERSION = 2
V2_AUTHORITY_MODE_PRODUCTION = "PRODUCTION"
V2_SIGNATURE_ALGORITHM = "ED25519"
#: Operator B's OWN copy of the durable anchor key set (shared schema, not shared code).
ANTI_REPLAY_KEYS = {"receipt_nonce", "scope_id", "scenario_id", "run_id",
                    "subject_identity"}

_ROOT = os.path.dirname(os.path.abspath(__file__))
_TRUST_ROOT_GLOB = "MBCX-01-BUILD-STATE-TRUST-ROOTS-*.fixture.json"


class OperatorBError(ValueError):
    """Closed, fail-loud operator-B derivation error."""


def _trust_root_rows(trust_root_id: str, signer_key_id: str,
                     trust_root_manifest: Any = None) -> tuple[dict, dict]:
    """Operator B's OWN resolution of the trust-root anchor (no shared helper).

    `trust_root_manifest` is the OPERATOR-delivered manifest of record. The ceremony
    spec is explicit that a production manifest is never committed to this repository
    and reaches the verifier as an injected input (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md`
    §3.6), so operator B must be able to derive under it; the committed-fixture glob
    remains the fallback for the fixture path. Injection is not authority either way:
    operator B's content is compared byte-for-byte against operator 1's, and the
    verifier authenticates the manifest against the owner anchor separately.
    """
    candidates: list[Any] = []
    if trust_root_manifest is not None:
        candidates.append(trust_root_manifest)
    for path in sorted(glob.glob(os.path.join(_ROOT, _TRUST_ROOT_GLOB))):
        with open(path, encoding="utf-8") as stream:
            candidates.append(json.load(stream))
    for manifest in candidates:
        if not isinstance(manifest, dict) or manifest.get("manifest_id") != trust_root_id:
            continue
        for root in manifest.get("roots", []):
            if root.get("key_id") == signer_key_id:
                return manifest, root
        raise OperatorBError("OPERATOR_B_TRUST_ROOT_KEY_UNRESOLVED:%s" % signer_key_id)
    raise OperatorBError("OPERATOR_B_TRUST_ROOT_UNRESOLVED:%s" % trust_root_id)


def _read_identity(transaction_commit_id: str, phase: str) -> str:
    return "READ." + common.sha256([transaction_commit_id, phase])


def _finalize_readback_content(readback_row: Any, identity_config: dict[str, Any]) -> dict[str, Any]:
    """Operator-B's own postcommit finalizer.

    Declared as a named seam so the operator-independence witness can monkeypatch a
    POISONED finalizer and prove that divergence is detected rather than absorbed.
    """
    state_utf8 = readback_row["state_utf8"]
    state = json.loads(state_utf8)
    if common.canonical_json(state).decode("utf-8") != state_utf8:
        raise OperatorBError("OPERATOR_B_CANONICAL_BYTES_INVALID")
    return {
        "read_id": _read_identity(readback_row["transaction_commit_id"], "POSTCOMMIT"),
        "state_utf8": state_utf8,
        "state_hash": common.sha384(state_utf8.encode("utf-8")),
        "cut": common.current_cut(state),
        "reader_identity": identity_config["reader_identity"],
    }


def derive_receipt_content_independent(store_path: Any, transaction_commit_id: str, *,
                                       identity_config: dict[str, Any],
                                       trust_root_manifest: Any = None
                                       ) -> dict[str, Any]:
    """Re-derive the unsigned receipt content for `transaction_commit_id` from store bytes.

    Returns the content mapping only. Operator B never signs and never holds signer
    custody; it cannot mint authority on its own.
    """
    if not isinstance(identity_config, dict):
        raise OperatorBError("OPERATOR_B_IDENTITY_CONFIG_INVALID")
    connection = store_mod.open_readonly_connection(store_path)
    try:
        journal = connection.execute(
            "SELECT transaction_commit_id, status, prestate_utf8, anti_replay_utf8,"
            " anti_replay_hash FROM journal"
            " WHERE transaction_commit_id = ?", (transaction_commit_id,)).fetchone()
        if journal is None:
            raise OperatorBError("OPERATOR_B_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        if journal["status"] != store_mod.TRANSACTION_COMMITTED:
            raise OperatorBError("OPERATOR_B_TRANSACTION_%s" % journal["status"])
        proposal_row = connection.execute(
            "SELECT event_id, event_utf8 FROM proposals WHERE transaction_commit_id = ?",
            (transaction_commit_id,)).fetchone()
        child_row = connection.execute(
            "SELECT event_id, event_utf8 FROM children WHERE transaction_commit_id = ?",
            (transaction_commit_id,)).fetchone()
        snapshot_row = connection.execute(
            "SELECT state_utf8 FROM snapshots WHERE transaction_commit_id = ?",
            (transaction_commit_id,)).fetchone()
    finally:
        connection.close()
    if proposal_row is None or child_row is None or snapshot_row is None:
        raise OperatorBError("OPERATOR_B_TRANSACTION_ROWS_INCOMPLETE")

    prestate_utf8 = journal["prestate_utf8"]
    prestate = json.loads(prestate_utf8)
    poststate = json.loads(snapshot_row["state_utf8"])
    proposal = json.loads(proposal_row["event_utf8"])
    child = json.loads(child_row["event_utf8"])
    for parsed, encoded in ((prestate, prestate_utf8),
                            (poststate, snapshot_row["state_utf8"]),
                            (proposal, proposal_row["event_utf8"]),
                            (child, child_row["event_utf8"])):
        if common.canonical_json(parsed).decode("utf-8") != encoded:
            raise OperatorBError("OPERATOR_B_CANONICAL_BYTES_INVALID")
    for event, row in ((proposal, proposal_row), (child, child_row)):
        if (common.canonical_event_id(event) != event.get("event_id")
                or event.get("event_id") != row["event_id"]):
            raise OperatorBError("OPERATOR_B_EVENT_IDENTITY_INVALID")

    # FOLD 1: the anti-replay anchors and the attested subject identity are DURABLE
    # facts of the journal row. Operator B re-decodes and re-digests them itself — it
    # never reads them from `identity_config`, so a caller who poisons the config
    # cannot move operator B's answer, and it never re-derives them by label transform.
    anti_replay = json.loads(journal["anti_replay_utf8"])
    if (not isinstance(anti_replay, dict)
            or set(anti_replay) != ANTI_REPLAY_KEYS
            or common.canonical_json(anti_replay).decode("utf-8")
            != journal["anti_replay_utf8"]
            or journal["anti_replay_hash"]
            != common.sha384(journal["anti_replay_utf8"].encode("utf-8"))):
        raise OperatorBError("OPERATOR_B_ANTI_REPLAY_INVALID")

    manifest, root = _trust_root_rows(identity_config["trust_root_id"],
                                      identity_config["signer_key_id"],
                                      trust_root_manifest)
    if not transaction_commit_id.startswith("TXN."):
        raise OperatorBError("OPERATOR_B_TRANSACTION_IDENTITY_INVALID")

    return {
        "schema_id": V2_SCHEMA_ID,
        "authority_mode": V2_AUTHORITY_MODE_PRODUCTION,
        "domain": V2_DOMAIN,
        "version": V2_VERSION,
        "store_identity": {
            "store_id": identity_config["store_id"],
            "namespace": identity_config["namespace"],
            "namespace_version": identity_config["namespace_version"],
        },
        "transaction_commit_id": transaction_commit_id,
        "prestate_read": {
            "read_id": _read_identity(transaction_commit_id, "PRESTATE"),
            "state_utf8": prestate_utf8,
            "state_hash": common.sha384(prestate_utf8.encode("utf-8")),
            "cut": common.current_cut(prestate),
        },
        "proposal_persistence": {
            "event_id": proposal["event_id"],
            "event_utf8": proposal_row["event_utf8"],
            "event_hash": common.sha384(proposal_row["event_utf8"].encode("utf-8")),
            "persistence_identity": "ROW." + common.sha256(
                [transaction_commit_id, proposal["event_id"]]),
        },
        "applied_child": {
            "event_id": child["event_id"],
            "event_utf8": child_row["event_utf8"],
            "event_hash": common.sha384(child_row["event_utf8"].encode("utf-8")),
            "next_sequence": poststate["next_seq"],
        },
        "postcommit_readback": _finalize_readback_content(
            {"transaction_commit_id": transaction_commit_id,
             "state_utf8": snapshot_row["state_utf8"]}, identity_config),
        "signer_identity": {
            "producer_id": identity_config["producer_id"],
            "producer_role": identity_config["producer_role"],
            "signer_key_id": identity_config["signer_key_id"],
            "signature_algorithm": V2_SIGNATURE_ALGORITHM,
            "trust_root_id": identity_config["trust_root_id"],
            "trust_policy_digest": manifest["trust_policy_digest"],
            "validity_not_before": root["validity"]["not_before"],
            "validity_not_after": root["validity"]["not_after"],
            "revocation_state": root["revocation_state"],
            "subject_identity": anti_replay["subject_identity"],
        },
        "anti_replay": {
            "receipt_nonce": anti_replay["receipt_nonce"],
            "scope_id": anti_replay["scope_id"],
            "scenario_id": anti_replay["scenario_id"],
            "run_id": anti_replay["run_id"],
            "transaction_commit_id": transaction_commit_id,
        },
    }
