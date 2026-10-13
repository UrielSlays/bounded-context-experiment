"""BUILD A — production state-owner adapter, operator 1 (GREEN STAGE).

Drives: durable store terminal -> independent durable readback -> `StateAuthorityReceiptV2`
minted through a custody-injected signer. The private key never lives here, in the
repository, in a fixture, in a log, in the packet, or in the receipt: `signer` is an
injected object exposing `key_id`, `algorithm`, and `sign(preimage_bytes) -> bytes`.

Minting law (mirrors `mbcx01_build_state_store` crash-window law):
  * only a `COMMITTED` journal terminal may mint;
  * `PENDING` / `BROKEN` / absent-transaction / committed-but-no-readback raise
    `mbcx01_build_state_store.StateStoreError` — the adapter returns NO partial receipt;
  * the postcommit evidence is the store readback bytes read through a SEPARATE reader
    connection, never the writer's in-memory poststate object;
  * both frozen reducers must replay the exact persisted child from the exact read
    prestate and reproduce the exact readback state and cut before a receipt exists.

DEVIATION FROM THE DESIGN NOTES (byte reason, documented rather than papered over):
`MBCX-01-BUILD-DESIGN-NOTES.md:96` describes this adapter as "drives store commit ->
independent readback -> mints". The executable spec is narrower and stricter:
`test_mbcx01_build_state.py:604-618` (`test_ba21`) calls the adapter on a store where
NOTHING has been committed, requires `StateStoreError`, and then asserts
`store.journal_rows(TRANSACTION_ID) == []` — i.e. the adapter must not have written
anything. So committing is the STORE's door (`SingleWriterStateStore.commit_transition`,
the caller's step); the adapter is a pure MINTER over an already durable COMMITTED
terminal, and it refuses (without writing) anything else. This is strictly more
conservative than the notes: the adapter can never create the durable fact it attests.

Receipt content is derived ONLY from the durable store bytes plus the injected
`identity_config`; nothing in the transition request may override either.
"""

from __future__ import annotations

import base64
import copy
import glob
import json
import os
from typing import Any

import mbcx01_r13_common as common
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference

import mbcx01_build_state_store as store_mod


#: Receipt shape produced by this adapter (closed key set; verified in
#: `mbcx01_build_state_authority`). V1 cannot express production — `mbcx01_r13_common`
#: pins `authority_mode="FIXTURE_ONLY_UNAVAILABLE"` (:303-305) and forces every signature
#: slot to null (:366-370) — so V2 is the explicitly versioned successor arm.
STATE_AUTHORITY_V2_SCHEMA_ID = "StateAuthorityReceiptV2"
STATE_AUTHORITY_V2_DOMAIN = "MBCX01.STATE.AUTHORITY"
STATE_AUTHORITY_V2_VERSION = 2
AUTHORITY_MODE_PRODUCTION = "PRODUCTION"
AUTHORITY_MODE_FIXTURE = "FIXTURE_CONFORMANCE"
SIGNATURE_ALGORITHM = "ED25519"

#: Trust-root manifests the producer may resolve a `trust_root_id` against. The manifest
#: is an ANCHOR, never an activation: every committed instance is `production_ready:false`.
TRUST_ROOT_MANIFEST_GLOB = "MBCX-01-BUILD-STATE-TRUST-ROOTS-*.fixture.json"

IDENTITY_CONFIG_KEYS = {
    "store_id", "namespace", "namespace_version", "producer_id", "producer_role",
    "reader_identity", "reader_role", "signer_key_id", "trust_root_id",
    "subject_identity", "scope_id", "scenario_id", "run_id",
}

_ROOT = os.path.dirname(os.path.abspath(__file__))


def resolve_trust_root_manifest(trust_root_id: str) -> dict[str, Any]:
    """Resolve the injected-by-configuration trust root manifest for `trust_root_id`.

    Producer-side anchor resolution only: the manifest supplies the policy digest and the
    signer key's validity/revocation state that the receipt must ATTEST. It never grants
    authority — the verifier re-resolves its own manifest and compares.
    """
    for path in sorted(glob.glob(os.path.join(_ROOT, TRUST_ROOT_MANIFEST_GLOB))):
        with open(path, encoding="utf-8") as stream:
            manifest = json.load(stream)
        if manifest.get("manifest_id") == trust_root_id:
            return manifest
    raise store_mod.StateStoreError("STATE_TRUST_ROOT_MANIFEST_UNRESOLVED:%s" % trust_root_id)


def durable_anti_replay_block(store: Any, transaction_commit_id: str,
                              identity_config: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Read the receipt's anti-replay block out of the DURABLE journal row (FOLD 1).

    The adapter does not compute anchors and does not copy them out of its own
    configuration: it reads the anchor set the writer committed to, and refuses to mint
    at all if the injected configuration disagrees with that durable fact. Returns
    `(anti_replay_block, subject_identity)`.

    Before FOLD 1 the anchors were re-derived by label transform (`TXN.x -> NONCE.x`,
    `SCOPE.x -> SCENARIO.x`, `SUBJECT.x -> RUN.x`). That was a hack twice over: it could
    not express a production run whose scenario/run/nonce are independent identifiers,
    and a value any party can recompute from a label proves nothing about what was
    committed. The durable row is the anchor authority.
    """
    anchors = store.anti_replay_anchors(transaction_commit_id)
    configured = {key: identity_config[key] for key in
                  ("scope_id", "scenario_id", "run_id", "subject_identity")}
    if any(anchors[key] != value for key, value in configured.items()):
        raise store_mod.StateStoreError("STATE_ANTI_REPLAY_CONFIG_MISMATCH")
    block = {"receipt_nonce": anchors["receipt_nonce"],
             "scope_id": anchors["scope_id"],
             "scenario_id": anchors["scenario_id"],
             "run_id": anchors["run_id"],
             "transaction_commit_id": transaction_commit_id}
    return block, anchors["subject_identity"]


def produce_state_authority_receipt_v2(store: Any, transition_request: Any, *,
                                       signer: Any,
                                       identity_config: dict[str, Any],
                                       trust_root_manifest: Any = None
                                       ) -> dict[str, Any]:
    """Read the durable COMMITTED terminal back independently and mint one signed V2 receipt.

    `identity_config` is the independently configured identity source (store id,
    namespace, namespace version, producer id/role, reader identity/role, signer key id,
    trust root id, subject identity, scope/scenario/run ids). Nothing in the request may
    override it.
    """
    if not isinstance(identity_config, dict) or not IDENTITY_CONFIG_KEYS <= set(identity_config):
        raise store_mod.StateStoreError("STATE_IDENTITY_CONFIG_INVALID")
    if not isinstance(transition_request, dict) or "transaction_commit_id" not in transition_request:
        raise store_mod.StateStoreError("STATE_STORE_REQUEST_INVALID")
    if not isinstance(store, store_mod.SingleWriterStateStore):
        raise store_mod.StateStoreError("STATE_STORE_REQUIRED")

    transaction_commit_id = transition_request["transaction_commit_id"]
    expected_store_identity = {
        "store_id": identity_config["store_id"],
        "namespace": identity_config["namespace"],
        "namespace_version": identity_config["namespace_version"],
    }
    if store.store_identity != expected_store_identity:
        raise store_mod.StateStoreError("STATE_STORE_IDENTITY_MISMATCH")
    if identity_config["reader_identity"] == identity_config["producer_id"]:
        raise store_mod.StateStoreError("STATE_READER_NOT_INDEPENDENT")

    # Terminal first: PENDING / BROKEN / unknown mint NOTHING and write NOTHING.
    rows = store.journal_rows(transaction_commit_id)
    if not rows:
        raise store_mod.StateStoreError(
            "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
    if rows[0]["status"] != store_mod.TRANSACTION_COMMITTED:
        raise store_mod.StateStoreError(
            "STATE_STORE_TRANSACTION_%s:%s" % (rows[0]["status"], transaction_commit_id))

    durable = store.transaction_rows(transaction_commit_id)
    prestate_read = store.independent_readback(
        transaction_commit_id, reader_identity=identity_config["reader_identity"],
        phase=store_mod.PHASE_PRESTATE)
    postcommit_read = store.independent_readback(
        transaction_commit_id, reader_identity=identity_config["reader_identity"],
        phase=store_mod.PHASE_POSTCOMMIT)

    prestate = json.loads(prestate_read["state_utf8"])
    poststate = json.loads(postcommit_read["state_utf8"])
    proposal = json.loads(durable["proposals"]["event_utf8"])
    child = json.loads(durable["children"]["event_utf8"])

    # Dual-reducer replay of the DURABLE bytes before a receipt exists.
    reference_state, reference_result = reference.reference_apply(
        copy.deepcopy(prestate), copy.deepcopy(child))
    oracle_state, oracle_result = oracle.oracle_apply(
        copy.deepcopy(prestate), copy.deepcopy(child))
    if reference_result != "APPLIED" or oracle_result != "APPLIED":
        raise store_mod.StateStoreError("STATE_STORE_TRANSITION_REFUSED")
    if reference_state != oracle_state:
        raise store_mod.StateStoreError("STATE_STORE_REDUCER_DISAGREEMENT")
    if reference_state != poststate:
        raise store_mod.StateStoreError("STATE_STORE_POSTSTATE_MISMATCH")
    if (prestate.get("events", {}).get(proposal.get("event_id")) != common.sha384(proposal)
            or poststate.get("events", {}).get(child.get("event_id")) != common.sha384(child)):
        raise store_mod.StateStoreError("STATE_STORE_EVENT_NOT_PERSISTED")

    anti_replay, subject_identity = durable_anti_replay_block(
        store, transaction_commit_id, identity_config)

    # The manifest of record is delivered by OPERATOR configuration, outside this
    # repository (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.6). When it is injected the
    # producer attests under it; otherwise the committed fixture instances are resolved
    # from disk. Neither is authority: the verifier re-resolves its own manifest and
    # authenticates it against the operator-preconfigured owner anchor.
    if trust_root_manifest is not None:
        manifest = trust_root_manifest
        if (not isinstance(manifest, dict)
                or manifest.get("manifest_id") != identity_config["trust_root_id"]):
            raise store_mod.StateStoreError(
                "STATE_TRUST_ROOT_MANIFEST_UNRESOLVED:%s"
                % identity_config["trust_root_id"])
    else:
        manifest = resolve_trust_root_manifest(identity_config["trust_root_id"])
    root = next((entry for entry in manifest.get("roots", [])
                 if entry.get("key_id") == identity_config["signer_key_id"]), None)
    if root is None:
        raise store_mod.StateStoreError(
            "STATE_TRUST_ROOT_KEY_UNRESOLVED:%s" % identity_config["signer_key_id"])

    content = {
        "schema_id": STATE_AUTHORITY_V2_SCHEMA_ID,
        "authority_mode": AUTHORITY_MODE_PRODUCTION,
        "domain": STATE_AUTHORITY_V2_DOMAIN,
        "version": STATE_AUTHORITY_V2_VERSION,
        "store_identity": dict(expected_store_identity),
        "transaction_commit_id": transaction_commit_id,
        "prestate_read": {
            "read_id": prestate_read["read_id"],
            "state_utf8": prestate_read["state_utf8"],
            "state_hash": prestate_read["state_hash"],
            "cut": prestate_read["cut"],
        },
        "proposal_persistence": {
            "event_id": durable["proposals"]["event_id"],
            "event_utf8": durable["proposals"]["event_utf8"],
            "event_hash": durable["proposals"]["event_hash"],
            "persistence_identity": durable["proposals"]["persistence_identity"],
        },
        "applied_child": {
            "event_id": durable["children"]["event_id"],
            "event_utf8": durable["children"]["event_utf8"],
            "event_hash": durable["children"]["event_hash"],
            "next_sequence": int(durable["snapshots"]["next_sequence"]),
        },
        "postcommit_readback": {
            "read_id": postcommit_read["read_id"],
            "state_utf8": postcommit_read["state_utf8"],
            "state_hash": postcommit_read["state_hash"],
            "cut": postcommit_read["cut"],
            "reader_identity": postcommit_read["reader_identity"],
        },
        "signer_identity": {
            "producer_id": identity_config["producer_id"],
            "producer_role": identity_config["producer_role"],
            "signer_key_id": identity_config["signer_key_id"],
            "signature_algorithm": SIGNATURE_ALGORITHM,
            "trust_root_id": identity_config["trust_root_id"],
            "trust_policy_digest": manifest["trust_policy_digest"],
            "validity_not_before": root["validity"]["not_before"],
            "validity_not_after": root["validity"]["not_after"],
            "revocation_state": root["revocation_state"],
            # The attested subject is the DURABLE row's subject, not the caller's label.
            "subject_identity": subject_identity,
        },
        "anti_replay": anti_replay,
    }
    return seal_receipt(content, signer)


def seal_receipt(content: dict[str, Any], signer: Any) -> dict[str, Any]:
    """Attach the unsigned carrier fields over the EXACT canonical preimage.

    Preimage = `common.canonical_json(content)` where `content` is the receipt without
    `receipt_preimage_b64` / `signature_b64` / `receipt_digest`; the signature covers those
    exact bytes and `receipt_digest = sha384(preimage_bytes)`.
    """
    if signer is None:
        raise store_mod.StateStoreError("STATE_SIGNER_REQUIRED")
    if getattr(signer, "algorithm", None) != SIGNATURE_ALGORITHM:
        raise store_mod.StateStoreError("STATE_SIGNER_ALGORITHM_INVALID")
    if getattr(signer, "key_id", None) != content["signer_identity"]["signer_key_id"]:
        raise store_mod.StateStoreError("STATE_SIGNER_KEY_ID_MISMATCH")
    receipt = copy.deepcopy(content)
    preimage = common.canonical_json(receipt)
    signature = signer.sign(preimage)
    if not isinstance(signature, bytes) or len(signature) != 64:
        raise store_mod.StateStoreError("STATE_SIGNATURE_INVALID_LENGTH")
    receipt["receipt_preimage_b64"] = base64.b64encode(preimage).decode("ascii")
    receipt["signature_b64"] = base64.b64encode(signature).decode("ascii")
    receipt["receipt_digest"] = common.sha384(preimage)
    return receipt
