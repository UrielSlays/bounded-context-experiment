"""BUILD A state-authority witnesses (RED STAGE).

Every `test_ba##_*` witness below is written BEFORE the production authority path exists
and must FAIL or ERROR on the current baseline for its intended reason:

  * positive witnesses fail because the store/adapter/operator-B skeletons raise
    `NotImplementedError` and because `verify_production_scorer_input` still returns the
    frozen error set (with `STATE_AUTHORITY_UNAVAILABLE` intact);
  * adversarial witnesses fail because `verify_state_authority_receipt_v2` currently
    answers `["STATE_AUTHORITY_UNAVAILABLE"]` for every input, so no NAMED rejection is
    reachable yet.

The one deliberate exception is `test_ba19_*` (frozen-suite compatibility), which is green
by construction: a red there would mean the frozen r13.2 suite was broken.

All keys in this file are FIXTURE-ONLY test keys generated for this suite. No production
key, ceremony, or trust-root activation exists or is created here.

ba29-ba33 were added by the BUILD acceptance r1 fold (fix class
AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP) and were RED against the pre-fold authority
bytes: the fully self-authored state universe verified clean (`[]`), the ceremony
spec's own production-shaped manifest was refused, and a whitespace-injected signature
carrier was accepted. See MBCX-01-BUILD-TRUSTBOOT-RED-WITNESS-RUN-2026-08-14.txt.

ba34-ba35 were added by the BUILD acceptance r2 fold (fix class FIXTURE_ISOLATION /
INSTANCE_SCOPED_VERIFIER_CONTEXT) and were RED against the pre-fold authority bytes: the
COMMITTED fixture owner anchor — whose private half is committed and therefore public —
authorized production state admission at both doors, and a trust root that had expired at
the verifier's clock admitted because freshness was taken from the artifact under
verification. See MBCX-01-BUILD-FIXTUREISO-RED-WITNESS-RUN-2026-08-14.txt.

ba38-ba40 were added by the codex r3 fold and were RED against the pre-fold bytes of
`mbcx01_build_state_store.py` (blob 9f62b797e4834f02bc10ddeed73865dc3b1c99d5) and
`mbcx01_build_state_authority.py` (blob bd29e3351ed9d9591974d0ee8bce235e837f02b6):
two producer PROCESSES both took the writer door and both committed journal `seq = 1`;
`open_verified` wrote the store schema into an unrelated sqlite database and then
adopted it; and a malformed root PEM raised `StateAuthorityError` out of the public
verifier instead of a closed verdict list.

ba41-ba44 were added by the codex CLI r4 fold and were RED against the pre-fold bytes of
`mbcx01_build_state_store.py` (blob 98ff8d500b7e9356d9090c6e31b8cd15a7031946,
sha256 6ffe46ac1d1a3b3ed4ff2b03238cd268e568e0bc5fad2c34581bc755ce690ab2) and
`mbcx01_build_state_authority.py` (blob 7ea817b11f2791155b85997b9ffb3817e0bb3fae,
sha256 d6b12374a61d1f508ba7459d9cc0a99b8fa5ef2fb726bca77632f43208a0d094):
the persistent `journal_mode=WAL` PRAGMA rewrote an unrelated application's database
BEFORE the refusal that was about to reject it; a tableless database whose only mark was
a nonzero `user_version` was adopted and its tell overwritten; a second store opened
under a live store's identity silently replaced it in the resolution registry, so a true
receipt of the first store's COMMITTED transaction was refused; and a custody object
whose `signer_key_ids` carried a dict raised a raw `TypeError` out of the public verifier.
Each arm is labelled RED or GUARD in its own docstring.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import inspect
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import mbcx01_r13_common as common
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_state_adapter as adapter
import mbcx01_build_state_authority as authority
import mbcx01_build_state_operator_b as operator_b
import mbcx01_build_state_store as store_mod
import mbcx01_build_trust_anchor as trust_anchor


TRUST_ROOT_MANIFEST_PATH = "MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json"

#: The SIMULATED production manifest id. The committed instance stays
#: `production_ready:false` forever; the ceremony spec's production manifest is never
#: committed to this repository (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.6), so the
#: production-shaped instance the witnesses use is built IN MEMORY over the same
#: fixture-only test keys, exactly as BUILD B's `simulated_production_manifest` does.
PRODUCTION_TRUST_ROOT_ID = "STATE.TRUST.MBCX01.BUILD.SIMULATED.PRODUCTION.1"

# FIXTURE-ONLY Ed25519 private keys. Test material, never production custody.
# `FIXTURE_WRITER_PRIVATE_KEY_PEM`'s public half is the WRITER root of the COMMITTED
# state manifest, so after the 2026-08-15 signing-key fold it can no longer sign a
# PRODUCTION-shaped receipt: committed key material is refused by name at the state
# production door (`test_ba36`, which is the witness that uses this pair for exactly
# that). The production lane's keys are generated in memory below.
FIXTURE_WRITER_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIC3ejul32478Z6mW41nPMt5bDTWj8UJPX8qC6QM+XTUN\n"
    "-----END PRIVATE KEY-----\n")
FIXTURE_ATTACKER_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIKECV+ZpxEADLOrTyJylh2SuPSL0/Io6KhRyt+9AEyK+\n"
    "-----END PRIVATE KEY-----\n")

# A FRESH attacker Ed25519 key pair, generated for the r1 trust-bootstrap witnesses
# (ba29-ba32). It is in no manifest this repository ships and in no ceremony: the
# witnesses use it to author an ENTIRE state trust universe the way the r1 council's
# SEAT2/SEAT3 attacks did.
SELF_AUTHORED_KEY_ID = "ATTACKER.SELF.AUTHORED.STATE.TEST.1"
SELF_AUTHORED_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIDQz+qAQTbN/9tw5KAPKhmqByyJXcsIjovqLX+7d/1Zo\n"
    "-----END PRIVATE KEY-----\n")
SELF_AUTHORED_PUBLIC_KEY_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAvu/Y1LEMLW3gt9rXWr0WKe3JilD+nAeecpgLWD/3C0I=\n"
    "-----END PUBLIC KEY-----\n")

#: The PRODUCTION-lane state signing pairs, generated IN MEMORY at first use and never
#: written to this repository — the same move the r2 fold made for the owner ANCHOR. A
#: key published in a committed `*.fixture.json` document is refused by name at the
#: production door after the 2026-08-15 signing-key fold, so the POSITIVE lane needs
#: material that is in no committed document (`mbcx01_build_ceremony_fixture`).
STATE_WRITER_KEY_ID = "MBCX01.BUILD.STATE.FIXTURE.ED25519.WRITER.1"


def _production_signing_keypair(key_id: str) -> tuple[str, str]:
    return ceremony.test_production_signing_keypair("MBCX01.BUILD.STATE." + key_id)


PRODUCTION_WRITER_PRIVATE_KEY_PEM = _production_signing_keypair(
    STATE_WRITER_KEY_ID)[0]


def setUpModule():  # noqa: N802 - unittest name
    """OPERATOR WIRING for the suite: install the TEST PRODUCTION verifier context.

    The r1 fix class turns on exactly this seam and the r2 FIXTURE-ISOLATION fold
    tightens it: the verifier context is constructed at process construction,
    structurally apart from every per-request call. No witness below may pass an anchor
    or a context to `verify_state_authority_receipt_v2` or
    `verify_production_scorer_input` — there is no parameter for either.

    The anchor is deliberately NOT the committed fixture anchor: after the r2 fold a
    `fixture_only` anchor cannot grant production authority (codex r2 F1), so the
    positive lane runs under a production-SHAPED anchor generated in memory at run time
    and never written to this repository. `test_ba34` is the witness for the refusal.
    """
    ceremony.configure_test_production_anchor()


def tearDownModule():  # noqa: N802 - unittest name
    trust_anchor.clear_owner_trust_anchor()


IDENTITY_CONFIG = {
    "store_id": "STORE.MBCX01.BUILD.STATE.1",
    "namespace": "MBCX01.STATE",
    "namespace_version": 1,
    "producer_id": "MBCX01.BUILD.STATE.OWNER.FIXTURE",
    "producer_role": authority.ROLE_STATE_OWNER_WRITER,
    "reader_identity": "MBCX01.BUILD.STATE.READER.FIXTURE",
    "reader_role": authority.ROLE_STATE_READBACK_READER,
    "signer_key_id": "MBCX01.BUILD.STATE.FIXTURE.ED25519.WRITER.1",
    "trust_root_id": PRODUCTION_TRUST_ROOT_ID,
    "subject_identity": "SUBJECT.MBCX01.BUILD.STATE.FIXTURE",
    "scope_id": "SCOPE.SHARED",
    "scenario_id": "SCENARIO.SHARED",
    "run_id": "RUN.MBCX01.BUILD.STATE.FIXTURE",
}

CUSTODY_EVIDENCE = {
    "signer_custodian_role": "STATE_KEY_CUSTODIAN",
    "trust_root_editor_role": "STATE_TRUST_ROOT_EDITOR",
    "signer_key_ids": ["MBCX01.BUILD.STATE.FIXTURE.ED25519.WRITER.1"],
    "root_editor_key_ids": ["MBCX01.BUILD.STATE.FIXTURE.ED25519.EDITOR.1"],
    "key_custody_attestation_digest": common.sha384(
        ["SEPARATE_STATE_KEY_CUSTODY_ATTESTATION", "FIXTURE"]),
    "root_editor_approval_digest": common.sha384(
        ["SEPARATE_TRUST_ROOT_EDITOR_APPROVAL", "FIXTURE"]),
    "store_build_provenance_digest": common.sha384(
        ["STATE_STORE_BUILD_PROVENANCE", "FIXTURE"]),
    "signing_ceremony_receipt_digest": common.sha384(
        ["PRODUCTION_SIGNING_CEREMONY_RECEIPT", "FIXTURE"]),
}

TRANSACTION_ID = "TXN.MBCX01.BUILD.STATE.0001"

#: The durable anti-replay anchor set bound INTO the journal row at commit time
#: (FOLD 1). These values happen to coincide with the canonical label transforms
#: (`TXN.x -> NONCE.x`, `SCOPE.x -> SCENARIO.x`, `SUBJECT.x -> RUN.x`) so that the
#: pre-fold witnesses keep asserting exactly what they asserted before.
ANTI_REPLAY_ANCHORS = {
    "receipt_nonce": "NONCE.MBCX01.BUILD.STATE.0001",
    "scope_id": IDENTITY_CONFIG["scope_id"],
    "scenario_id": IDENTITY_CONFIG["scenario_id"],
    "run_id": IDENTITY_CONFIG["run_id"],
    "subject_identity": IDENTITY_CONFIG["subject_identity"],
}

#: A PRODUCTION-shaped anchor set: the scenario, run and nonce are independent
#: identifiers, NOT string transforms of the scope / subject / transaction id.
#: A real production run is not obliged to name its scenario after its scope, so
#: an authority that derives anchors by label transform can neither express this
#: set nor detect a forgery of it — which is exactly what FOLD 1 repairs.
PRODUCTION_ANTI_REPLAY_ANCHORS = {
    "receipt_nonce": "NONCE.MBCX01.BUILD.STATE.PRODUCTION.7A",
    "scope_id": IDENTITY_CONFIG["scope_id"],
    "scenario_id": "SCENARIO.MBCX01.BUILD.PRODUCTION.7",
    "run_id": "RUN.MBCX01.BUILD.PRODUCTION.7",
    "subject_identity": IDENTITY_CONFIG["subject_identity"],
}

PENDING_TRANSACTION_ID = "TXN.MBCX01.BUILD.STATE.0002"

#: FOLD 2 — the cold verifier a fresh interpreter runs. It imports the authority
#: module from nothing, opens nothing in advance, and answers three questions over a
#: FILE-backed store it has never seen: honest receipt with the durable path injected,
#: a PENDING-terminal receipt with the path injected, and the honest receipt with NO
#: locator at all (which must stay a transaction-identity rejection).
FRESH_PROCESS_VERIFIER_SOURCE = (
    "import json,sys\n"
    "import mbcx01_build_state_authority as authority\n"
    "payload=json.load(open(sys.argv[1],encoding='utf-8'))\n"
    "def check(receipt,**extra):\n"
    "    return authority.verify_state_authority_receipt_v2(\n"
    "        receipt,trust_root_manifest=payload['manifest'],\n"
    "        custody_evidence=payload['custody'],**extra)\n"
    "sys.stdout.write(json.dumps({\n"
    "    'honest_with_locator':check(payload['receipt'],\n"
    "                                store_path=payload['store_path']),\n"
    "    'pending_with_locator':check(payload['pending_receipt'],\n"
    "                                 store_path=payload['store_path']),\n"
    "    'honest_without_locator':check(payload['receipt'])}))\n"
)

#: The second producer PROCESS's transaction in `test_ba38`. Distinct from
#: `TRANSACTION_ID` so the two rows differ in everything except the fact under test:
#: which journal SEQUENCE number each producer is given.
SECOND_PRODUCER_TRANSACTION_ID = "TXN.MBCX01.BUILD.STATE.0003"

#: A root `public_key_pem` that is shaped like a PEM and is not usable key material.
#: It is caller-supplied authority material, so it must be able to REFUSE a receipt and
#: must not be able to crash the verification (`test_ba40`).
MALFORMED_ROOT_PUBLIC_KEY_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "this is not base64 key material at all\n"
    "-----END PUBLIC KEY-----\n")

#: r3 P1 — ONE producer PROCESS for `test_ba38`. Two of these run concurrently against
#: one file-backed store and are held at the exact seam the finding names: each pauses at
#: its first `BEGIN IMMEDIATE` until the other has arrived, so both are inside
#: `commit_transition` with the sequence still unallocated. On the pre-fold bytes both
#: had ALREADY read `MAX(seq) + 1` by that point and both wrote `seq = 1`; with the
#: sequence read moved inside the write transaction, sqlite's own single-writer rule
#: hands them 1 and 2. The pause is a wrapper around the store's connection object: it
#: injects a delay, never a different statement or a different order.
TWO_PRODUCER_WORKER_SOURCE = (
    "import json,os,sys,time\n"
    "import mbcx01_build_state_store as store_mod\n"
    "import mbcx01_r13_packets as packets\n"
    "tag,peer,database,barrier_directory,txn=sys.argv[1:6]\n"
    "def barrier():\n"
    "    open(os.path.join(barrier_directory,'ready.'+tag),'w').close()\n"
    "    deadline=time.time()+120\n"
    "    while time.time()<deadline:\n"
    "        if os.path.exists(os.path.join(barrier_directory,'ready.'+peer)):\n"
    "            return\n"
    "        time.sleep(0.01)\n"
    "    raise SystemExit('barrier timeout')\n"
    "class HeldConnection:\n"
    "    def __init__(self,inner):\n"
    "        self._inner=inner\n"
    "        self._fired=False\n"
    "    def execute(self,sql,*arguments):\n"
    "        if sql.startswith('BEGIN IMMEDIATE') and not self._fired:\n"
    "            self._fired=True\n"
    "            barrier()\n"
    "        return self._inner.execute(sql,*arguments)\n"
    "    def __getattr__(self,name):\n"
    "        return getattr(self._inner,name)\n"
    "transition=packets.build_scoring_fixture(\n"
    "    packets.packet_fixture_manifest(),'OM')['transition_authority']\n"
    "request={'transaction_commit_id':txn,\n"
    "         'prestate':transition['precommit_state'],\n"
    "         'proposal_event':transition['proposal_event'],\n"
    "         'applied_child_event':transition['applied_child_event']}\n"
    "anchors={'receipt_nonce':'NONCE.MBCX01.BUILD.STATE.PRODUCER.'+tag,\n"
    "         'scope_id':'SCOPE.SHARED','scenario_id':'SCENARIO.SHARED',\n"
    "         'run_id':'RUN.MBCX01.BUILD.STATE.FIXTURE',\n"
    "         'subject_identity':'SUBJECT.MBCX01.BUILD.STATE.FIXTURE'}\n"
    "store=store_mod.SingleWriterStateStore.open_verified(\n"
    "    database,store_id=sys.argv[6],namespace=sys.argv[7],\n"
    "    namespace_version=int(sys.argv[8]))\n"
    "store._connection=HeldConnection(store._connection)\n"
    "terminal=store.commit_transition(request,anti_replay=anchors)\n"
    "store.close()\n"
    "sys.stdout.write(json.dumps({'seq':terminal['seq'],'pid':os.getpid(),\n"
    "                             'status':terminal['status']}))\n"
)

#: The anchors a label-transform derivation WOULD produce for this transaction,
#: this scope and this subject. Byte-identical to `ANTI_REPLAY_ANCHORS`; named
#: separately because ba26 uses it as the FORGERY, not as the truth.
LABEL_DERIVED_ANCHORS = dict(ANTI_REPLAY_ANCHORS)


def _load_trust_root_manifest() -> dict:
    with open(TRUST_ROOT_MANIFEST_PATH, encoding="utf-8") as stream:
        return json.load(stream)


def _production_state_manifest(*, committed_fixture_keys: bool = False) -> dict:
    """TEST-ONLY in-memory PRODUCTION-shaped `StateTrustRootManifestV1`.

    The shape `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.3 defines for a real ceremony:
    `production_ready:true`, policy `ACTIVATED`, roots not `fixture_only`. It is never
    written to disk and it activates nothing — it exists so the authenticated production
    path has a positive witness at all. Before the r1 fold this manifest was REFUSED
    (`STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED`) while a fixture-shaped self-authored one was
    accepted; ba30/ba31 are that pair of defects.

    Its roots are generated IN MEMORY per run (2026-08-15 signing-key fold): the ceremony
    requires every key in a production manifest to be generated in the ceremony rather
    than copied out of a committed fixture document (§3 steps 0 and 3), and that rule is
    now mechanical. `committed_fixture_keys=True` asks for the pre-fold shape — the
    COMMITTED test keys in a production-shaped manifest — which is exactly what `ba36`
    must present in order to witness the refusal.
    """
    manifest = _load_trust_root_manifest()
    manifest["manifest_id"] = PRODUCTION_TRUST_ROOT_ID
    manifest["production_ready"] = True
    manifest["trust_policy"]["status"] = authority.TRUST_POLICY_STATUS_ACTIVATED
    manifest["trust_policy_digest"] = common.sha384(manifest["trust_policy"])
    for root in manifest["roots"]:
        root["fixture_only"] = False
        root["trust_policy_digest"] = manifest["trust_policy_digest"]
        if not committed_fixture_keys:
            root["public_key_pem"] = _production_signing_keypair(root["key_id"])[1]
    return manifest


def _owner_activation(manifest: dict, custody: dict, **kwargs) -> dict:
    """The owner-signed `OwnerCeremonyActivationV1` for this manifest + custody set."""
    binding = authority.production_activation_binding(manifest, custody)
    return ceremony.activation_statement(manifest=manifest, **binding, **kwargs)


def _state_custody_evidence(manifest: dict | None = None, **kwargs) -> dict:
    """The custody evidence PLUS the owner-signed activation statement (r1 fix class)."""
    manifest = manifest if manifest is not None else _production_state_manifest()
    custody = copy.deepcopy(CUSTODY_EVIDENCE)
    custody[authority.OWNER_ACTIVATION_EVIDENCE] = _owner_activation(
        manifest, custody, **kwargs)
    return custody


def _node_sign(private_key_pem: str, preimages_b64: list[str]) -> list[str]:
    """Sign fixture preimages with node's Ed25519, mirroring the frozen r13 test signer."""
    source = ("const {createPrivateKey,sign}=require('node:crypto');"
              "let d='';process.stdin.setEncoding('utf8');"
              "process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{"
              "const r=JSON.parse(d),k=createPrivateKey(r.k);"
              "process.stdout.write(JSON.stringify(r.ps.map(p=>sign(null,"
              "Buffer.from(p,'base64'),k).toString('base64'))));});")
    request = {"k": private_key_pem, "ps": preimages_b64}
    result = subprocess.run(["node", "-e", source], input=json.dumps(request), text=True,
                            capture_output=True, timeout=20, check=True)
    return json.loads(result.stdout)


def _read_id(transaction_commit_id: str, phase: str) -> str:
    return "READ." + common.sha256([transaction_commit_id, phase])


def _seal(content: dict, private_key_pem: str = PRODUCTION_WRITER_PRIVATE_KEY_PEM) -> dict:
    """Attach the signed carrier fields: an attacker repairs every hash they control."""
    receipt = {key: value for key, value in content.items()
               if key not in authority.V2_UNSIGNED_KEYS}
    preimage = common.canonical_json(receipt)
    preimage_b64 = base64.b64encode(preimage).decode("ascii")
    receipt["receipt_preimage_b64"] = preimage_b64
    receipt["signature_b64"] = _node_sign(private_key_pem, [preimage_b64])[0]
    receipt["receipt_digest"] = common.sha384(preimage)
    return receipt


def _v2_receipt(precommit: dict, proposal: dict, child: dict, postcommit: dict, *,
                transaction_commit_id: str = TRANSACTION_ID,
                identity: dict | None = None,
                private_key_pem: str = PRODUCTION_WRITER_PRIVATE_KEY_PEM) -> dict:
    """Build one production-shaped `StateAuthorityReceiptV2` over exact frozen bytes."""
    config = dict(IDENTITY_CONFIG)
    config.update(identity or {})
    prestate_utf8 = common.canonical_json(precommit).decode("utf-8")
    proposal_utf8 = common.canonical_json(proposal).decode("utf-8")
    child_utf8 = common.canonical_json(child).decode("utf-8")
    poststate_utf8 = common.canonical_json(postcommit).decode("utf-8")
    content = {
        "schema_id": authority.STATE_AUTHORITY_V2_SCHEMA_ID,
        "authority_mode": authority.AUTHORITY_MODE_PRODUCTION,
        "domain": "MBCX01.STATE.AUTHORITY",
        "version": 2,
        "store_identity": {
            "store_id": config["store_id"],
            "namespace": config["namespace"],
            "namespace_version": config["namespace_version"],
        },
        "transaction_commit_id": transaction_commit_id,
        "prestate_read": {
            "read_id": _read_id(transaction_commit_id, "PRESTATE"),
            "state_utf8": prestate_utf8,
            "state_hash": common.sha384(prestate_utf8.encode("utf-8")),
            "cut": common.current_cut(precommit),
        },
        "proposal_persistence": {
            "event_id": proposal["event_id"],
            "event_utf8": proposal_utf8,
            "event_hash": common.sha384(proposal_utf8.encode("utf-8")),
            "persistence_identity": "ROW." + common.sha256(
                [transaction_commit_id, proposal["event_id"]]),
        },
        "applied_child": {
            "event_id": child["event_id"],
            "event_utf8": child_utf8,
            "event_hash": common.sha384(child_utf8.encode("utf-8")),
            "next_sequence": postcommit["next_seq"],
        },
        "postcommit_readback": {
            "read_id": _read_id(transaction_commit_id, "POSTCOMMIT"),
            "state_utf8": poststate_utf8,
            "state_hash": common.sha384(poststate_utf8.encode("utf-8")),
            "cut": common.current_cut(postcommit),
            "reader_identity": config["reader_identity"],
        },
        "signer_identity": {
            "producer_id": config["producer_id"],
            "producer_role": config["producer_role"],
            "signer_key_id": config["signer_key_id"],
            "signature_algorithm": authority.SIGNATURE_ALGORITHM,
            "trust_root_id": config["trust_root_id"],
            "trust_policy_digest": config.get(
                "trust_policy_digest", _production_state_manifest()["trust_policy_digest"]),
            "validity_not_before": "2026-08-13T00:00:00.000000Z",
            "validity_not_after": "2027-08-13T00:00:00.000000Z",
            "revocation_state": "NOT_REVOKED",
            "subject_identity": config["subject_identity"],
        },
        "anti_replay": {
            "receipt_nonce": "NONCE.MBCX01.BUILD.STATE.0001",
            "scope_id": config["scope_id"],
            "scenario_id": config["scenario_id"],
            "run_id": config["run_id"],
            "transaction_commit_id": transaction_commit_id,
        },
    }
    return _seal(content, private_key_pem)


def _repair_read(row: dict, state: dict) -> None:
    """Repair every hash/cut an attacker controls after substituting state bytes."""
    row["state_utf8"] = common.canonical_json(state).decode("utf-8")
    row["state_hash"] = common.sha384(row["state_utf8"].encode("utf-8"))
    row["cut"] = common.current_cut(state)


def _repair_event(row: dict, event: dict) -> None:
    """Repair the event id and hash an attacker controls after substituting an event."""
    event["event_id"] = common.canonical_event_id(event)
    row["event_id"] = event["event_id"]
    row["event_utf8"] = common.canonical_json(event).decode("utf-8")
    row["event_hash"] = common.sha384(row["event_utf8"].encode("utf-8"))


class _FixtureSigner:
    """Custody-injected FIXTURE signer (never a production key or ceremony)."""

    key_id = IDENTITY_CONFIG["signer_key_id"]
    algorithm = authority.SIGNATURE_ALGORITHM

    @staticmethod
    def sign(preimage: bytes) -> bytes:
        return base64.b64decode(_node_sign(
            PRODUCTION_WRITER_PRIVATE_KEY_PEM,
            [base64.b64encode(preimage).decode("ascii")])[0])


class BuildAStateAuthorityWitnesses(unittest.TestCase):
    """Named BUILD-A state-authority witnesses (handoff r13.2 'State authority' list)."""

    maxDiff = None

    def setUp(self):
        # The manifest of record is the OPERATOR-injected production instance, and its
        # activation is authenticated against the anchor `setUpModule` wired in. A
        # witness that wants the committed fixture instance asks for it by name.
        ceremony.configure_test_production_anchor()
        self.addCleanup(ceremony.configure_test_production_anchor)
        # Store hygiene (r4 FOLD-2B). Several witnesses below open a store and never
        # close it, which used to be invisible: the live-store registry was keyed by
        # store identity and LAST WRITE WON, so the next witness's store silently took
        # the leaked one's place. With that replacement refused by name, a leaked store
        # would make every later witness fail — so each witness now releases exactly the
        # stores IT opened. This is test hygiene, not a production mechanism: a producer
        # process opens one store and closes it (`mbcx01_build_integration.py:169-184`).
        self.addCleanup(self.release_stores_opened_by_this_witness,
                        {id(store) for store in store_mod._OPEN_WRITERS.values()})
        self.trust_root_manifest = _production_state_manifest()
        self.custody = _state_custody_evidence(self.trust_root_manifest)
        self.manifest = packets.packet_fixture_manifest()
        self.scorer_input = packets.build_scoring_fixture(self.manifest, "OM")
        self.frozen_errors = packets.validate_scorer_input(
            self.manifest, self.scorer_input, require_production_authority=True)

    # ---- fixture graph helpers (drive the FROZEN constructors only) ----------------

    def frozen_graph(self):
        """Return (precommit, proposal, child, postcommit) from frozen constructors."""
        state = reference.initial_state()
        handoff = reference.handoff_fixture_payload()
        state = self.apply_both(state, reference.make_event(
            "open_handoff", handoff, state=state))
        response = reference.response_fixture_payload(handoff)
        state = self.apply_both(state, reference.make_event(
            "record_call_response", response, state=state))
        proposal = reference.make_event("propose_handoff_result", {
            "handoff_id": handoff["handoff_id"],
            "worker_handoff_hash": response["worker_handoff_hash"],
            "originating_cut_hash": handoff["originating_cut_hash"],
            "action_ids": [handoff["action_catalog"][0]["action_id"]],
        }, state=state)
        precommit = self.apply_both(state, proposal)
        child = reference.make_event("commit_handoff_result", {
            "handoff_id": handoff["handoff_id"],
            "proposal_event_id": proposal["event_id"],
        }, state=precommit)
        postcommit = self.apply_both(precommit, child)
        return precommit, proposal, child, postcommit

    def apply_both(self, state, event):
        ref_state, ref_result = reference.reference_apply(
            copy.deepcopy(state), copy.deepcopy(event))
        ora_state, ora_result = oracle.oracle_apply(
            copy.deepcopy(state), copy.deepcopy(event))
        self.assertEqual(ref_result, "APPLIED")
        self.assertEqual(ora_result, "APPLIED")
        self.assertEqual(ref_state, ora_state)
        return ref_state

    def packet_graph(self):
        """Return the exact graph the frozen scorer input's transition authority pins."""
        transition = self.scorer_input["transition_authority"]
        return (copy.deepcopy(transition["precommit_state"]),
                copy.deepcopy(transition["proposal_event"]),
                copy.deepcopy(transition["applied_child_event"]),
                copy.deepcopy(transition["postcommit_state"]))

    def packet_receipt(self, **kwargs):
        precommit, proposal, child, postcommit = self.packet_graph()
        return _v2_receipt(precommit, proposal, child, postcommit, **kwargs)

    def verify(self, receipt, *, trust_root_manifest=None, custody=None):
        return authority.verify_state_authority_receipt_v2(
            receipt,
            trust_root_manifest=trust_root_manifest or self.trust_root_manifest,
            custody_evidence=custody or self.custody,
            require_production=True)

    def admit(self, receipt, *, scorer_input=None):
        return authority.verify_production_scorer_input(
            scorer_input or self.scorer_input, receipt,
            expected_manifest=self.manifest,
            trust_root_manifest=self.trust_root_manifest,
            custody_evidence=self.custody)

    def assert_named_rejection(self, errors, named):
        """Invariant: a defect yields its NAMED error AND never discharges the sentinel."""
        self.assertIn(named, errors)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, errors)

    # ---- 1. positive production path ----------------------------------------------

    def test_ba01_positive_production_transition_discharges_only_the_named_sentinel(self):
        """Invariant: store commit -> independent readback -> V2 receipt is the ONLY way
        `STATE_AUTHORITY_UNAVAILABLE` is discharged, and discharge is exact — a fully
        valid production graph admits with an EMPTY error list, with every frozen check
        still executed under production semantics."""
        precommit, proposal, child, postcommit = self.packet_graph()
        store = store_mod.SingleWriterStateStore.open_verified(
            ":memory:", store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        transition_request = {
            "transaction_commit_id": TRANSACTION_ID,
            "prestate": precommit,
            "proposal_event": proposal,
            "applied_child_event": child,
        }
        terminal = store.commit_transition(transition_request,
                                           anti_replay=ANTI_REPLAY_ANCHORS)
        self.assertEqual(terminal["status"], store_mod.TRANSACTION_COMMITTED)
        readback = store.independent_readback(
            TRANSACTION_ID, reader_identity=IDENTITY_CONFIG["reader_identity"])
        self.assertEqual(json.loads(readback["state_utf8"]), postcommit)

        class _FixtureSigner:
            key_id = IDENTITY_CONFIG["signer_key_id"]
            algorithm = authority.SIGNATURE_ALGORITHM

            @staticmethod
            def sign(preimage: bytes) -> bytes:
                return base64.b64decode(_node_sign(
                    PRODUCTION_WRITER_PRIVATE_KEY_PEM,
                    [base64.b64encode(preimage).decode("ascii")])[0])

        receipt = adapter.produce_state_authority_receipt_v2(
            store, transition_request, signer=_FixtureSigner,
            identity_config=IDENTITY_CONFIG,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(self.verify(receipt), [])
        self.assertEqual(self.admit(receipt), [])

    # ---- 2. fixture V1 with no V2 alongside ---------------------------------------

    def test_ba02_adversarial_fixture_v1_receipt_without_v2_leaves_admission_unchanged(self):
        """Invariant: a fixture `StateAuthorityReceiptV1` can never express production
        (`mbcx01_r13_common.py:303-305`, `:366-370`); with no V2 alongside, production
        admission is byte-for-byte the frozen behaviour and the sentinel stays."""
        self.assertEqual(self.admit(None), self.frozen_errors)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, self.admit(None))
        v1 = self.scorer_input["state_authority_receipt"]
        self.assertEqual(v1["authority_mode"], common.STATE_AUTHORITY_FIXTURE_MODE)
        self.assert_named_rejection(
            self.verify(v1), authority.STATE_AUTHORITY_V2_SCHEMA_INVALID)

    # ---- 3. self-authored signer / root injection ---------------------------------

    def test_ba03_adversarial_self_authored_signer_key_is_not_a_trusted_root(self):
        """Invariant: a cryptographically valid signature from a key absent from the
        INJECTED manifest is not authority; roots come from the injected manifest only."""
        receipt = self.packet_receipt(
            identity={"signer_key_id": "ATTACKER.SELF.AUTHORED.1"},
            private_key_pem=FIXTURE_ATTACKER_PRIVATE_KEY_PEM)
        self.assert_named_rejection(
            self.verify(receipt), authority.STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)

    def test_ba04_adversarial_envelope_supplied_trust_root_cannot_authorize_itself(self):
        """Invariant: a trust root named only by the receipt envelope is self-authored;
        the verifier resolves roots exclusively from the injected manifest."""
        receipt = self.packet_receipt(
            identity={"trust_root_id": "STATE.TRUST.ATTACKER.SELF.AUTHORED.1",
                      "trust_policy_digest": common.sha384(["ATTACKER", "POLICY"])},
            private_key_pem=FIXTURE_ATTACKER_PRIVATE_KEY_PEM)
        self.assert_named_rejection(
            self.verify(receipt), authority.STATE_AUTHORITY_V2_ROOT_SELF_AUTHORED)

    def test_ba05_adversarial_signature_over_mutated_bytes_fails_before_any_semantics(self):
        """Invariant: the signature covers the whole receipt content; a repaired inner
        hash without a re-sign is a signature failure, never a repairable label."""
        receipt = self.packet_receipt()
        receipt["anti_replay"]["run_id"] = "RUN.MBCX01.BUILD.STATE.OTHER"
        self.assert_named_rejection(
            self.verify(receipt), authority.STATE_AUTHORITY_V2_SIGNATURE_INVALID)

    # ---- 4. custody separation -----------------------------------------------------

    def test_ba06_adversarial_signer_and_trust_root_editor_must_be_disjoint(self):
        """Invariant (I13): the signing-key custodian cannot edit or approve the trust
        root. Same role, or the signer key id inside the editor approval chain, is a
        CUSTODY_SEPARATION-class rejection checked mechanically, not merely declared."""
        collided = copy.deepcopy(self.custody)
        collided["trust_root_editor_role"] = collided["signer_custodian_role"]
        collided["root_editor_key_ids"] = list(collided["signer_key_ids"])
        receipt = self.packet_receipt()
        self.assert_named_rejection(
            self.verify(receipt, custody=collided),
            authority.STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID)

    def test_ba07_adversarial_fixture_manifest_relabelled_production_ready_is_refused(self):
        """Invariant: relabeling fixture evidence never creates production authority —
        flipping `production_ready` on a manifest of fixture-only roots is not a ceremony."""
        relabelled = _load_trust_root_manifest()
        relabelled["production_ready"] = True
        relabelled["trust_policy"]["status"] = "ACTIVATED"
        receipt = self.packet_receipt()
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=relabelled),
            authority.STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)

    def test_ba08_adversarial_revoked_or_expired_key_cannot_sign_production_authority(self):
        """Invariant: validity window and revocation list are enforced at verification
        time, from the injected manifest, not from the receipt's own claim."""
        receipt = self.packet_receipt(
            identity={"signer_key_id": "MBCX01.BUILD.STATE.FIXTURE.ED25519.WRITER.RETIRED.1"})
        self.assert_named_rejection(
            self.verify(receipt), authority.STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED)

    # ---- 5. writer-owned readback masquerade --------------------------------------

    def test_ba09_adversarial_writer_owned_readback_is_not_independent_evidence(self):
        """Invariant (r13.2 Opus residual): postcommit authority requires an independently
        identified reader. `reader_identity == producer_id` is a writer self-attestation
        wearing a readback label and is a named rejection in production mode."""
        receipt = self.packet_receipt(
            identity={"reader_identity": IDENTITY_CONFIG["producer_id"]})
        self.assert_named_rejection(
            self.verify(receipt), authority.STATE_AUTHORITY_V2_READER_NOT_INDEPENDENT)

    # ---- 6. wrong store / namespace / version / transaction ------------------------

    def test_ba10_adversarial_store_namespace_version_and_transaction_are_injected(self):
        """Invariant: store id, namespace, namespace version, and the transaction commit
        id come from the independently configured identity; a receipt that claims a
        different one fails loudly instead of redefining the store."""
        cases = (
            ({"store_id": "STORE.MBCX01.OTHER"},
             authority.STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH),
            ({"namespace": "MBCX01.OTHER.NAMESPACE"},
             authority.STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH),
            ({"namespace_version": 2},
             authority.STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH),
        )
        for override, named in cases:
            with self.subTest(override=override):
                receipt = self.packet_receipt(identity=override)
                self.assert_named_rejection(self.verify(receipt), named)
        with self.subTest(override="transaction_commit_id"):
            receipt = self.packet_receipt(
                transaction_commit_id="TXN.MBCX01.BUILD.STATE.9999")
            self.assert_named_rejection(
                self.verify(receipt),
                authority.STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH)

    # ---- 7. stale / future cut ------------------------------------------------------

    def test_ba11_adversarial_stale_and_fabricated_cuts_are_rejected(self):
        """Invariant: the readback cut must be the exact `current_cut` of the readback
        bytes and must strictly advance past the prestate cut. A stale cut (readback cut
        <= prestate cut) and a fabricated future cut are both named rejections."""
        stale = self.packet_receipt()
        stale["postcommit_readback"]["cut"] = copy.deepcopy(
            stale["prestate_read"]["cut"])
        self.assert_named_rejection(
            self.verify(_seal(stale)), authority.STATE_AUTHORITY_V2_CUT_INVALID)

        future = self.packet_receipt()
        future["postcommit_readback"]["cut"]["journal_seq"] += 5
        future["postcommit_readback"]["cut"]["valid_time"] = "2099-01-01T00:00:00.000000Z"
        self.assert_named_rejection(
            self.verify(_seal(future)), authority.STATE_AUTHORITY_V2_CUT_INVALID)

    # ---- 8. proposal / child / event-id / sequence substitution ---------------------

    def test_ba12_adversarial_child_substitution_with_repaired_hashes_is_caught(self):
        """Invariant: a substituted applied child with every attacker-controlled hash and
        canonical event id repaired and the receipt re-signed still fails, because both
        FROZEN reducers must replay the exact persisted child from the exact read prestate
        and reproduce the exact readback bytes."""
        precommit, proposal, child, postcommit = self.packet_graph()
        forged_child = copy.deepcopy(child)
        forged_child["payload"]["proposal_event_id"] = (
            "EV." + common.sha256(["ATTACKER", "PROPOSAL"]))
        receipt = self.packet_receipt()
        _repair_event(receipt["applied_child"], forged_child)
        self.assert_named_rejection(
            self.verify(_seal(receipt)),
            authority.STATE_AUTHORITY_V2_EVENT_SUBSTITUTION)

    def test_ba13_adversarial_proposal_substitution_with_repaired_hashes_is_caught(self):
        """Invariant: the proposal must be the exact event persisted in the read prestate
        journal (`prestate.events[event_id] == sha384(event)`); a re-canonicalized
        substitute proposal is a named rejection."""
        precommit, proposal, child, postcommit = self.packet_graph()
        forged_proposal = copy.deepcopy(proposal)
        forged_proposal["payload"]["action_ids"] = [
            common.action_id("SCOPE.SHARED", "OBL.PREREQ")]
        receipt = self.packet_receipt()
        _repair_event(receipt["proposal_persistence"], forged_proposal)
        receipt["proposal_persistence"]["persistence_identity"] = (
            "ROW." + common.sha256([TRANSACTION_ID, forged_proposal["event_id"]]))
        self.assert_named_rejection(
            self.verify(_seal(receipt)),
            authority.STATE_AUTHORITY_V2_EVENT_SUBSTITUTION)

    def test_ba14_adversarial_next_sequence_substitution_is_caught(self):
        """Invariant: `applied_child.next_sequence` is bound to the readback state's
        `next_seq`; a shifted sequence cannot be relabelled into agreement."""
        receipt = self.packet_receipt()
        receipt["applied_child"]["next_sequence"] += 1
        self.assert_named_rejection(
            self.verify(_seal(receipt)), authority.STATE_AUTHORITY_V2_SEQUENCE_INVALID)

    # ---- 9. prestate / poststate substitution with every hash repaired -------------

    def test_ba15_adversarial_poststate_substitution_with_repaired_hashes_is_caught(self):
        """Invariant: substituted readback bytes with `state_hash` and `cut` repaired and
        the receipt re-signed still fail: the reducers reproduce the true poststate, and
        the V2 bytes must byte-bind to the scorer input's `transition_authority`."""
        precommit, proposal, child, postcommit = self.packet_graph()
        forged_post = copy.deepcopy(postcommit)
        forged_post["last_observed_at"] = common.T1
        forged_post["next_seq"] += 1
        receipt = self.packet_receipt()
        _repair_read(receipt["postcommit_readback"], forged_post)
        receipt["postcommit_readback"]["reader_identity"] = (
            IDENTITY_CONFIG["reader_identity"])
        receipt["applied_child"]["next_sequence"] = forged_post["next_seq"]
        self.assert_named_rejection(
            self.verify(_seal(receipt)), authority.STATE_AUTHORITY_V2_STATE_SUBSTITUTION)

    def test_ba16_adversarial_foreign_graph_receipt_fails_byte_binding_to_the_packet(self):
        """Invariant: a fully self-consistent production receipt minted over a DIFFERENT
        transition graph cannot admit this scorer input — the V2 prestate/proposal/child/
        readback bytes must equal the scorer input's `transition_authority` exactly."""
        precommit, proposal, child, postcommit = self.frozen_graph()
        foreign = _v2_receipt(precommit, proposal, child, postcommit)
        self.assert_named_rejection(
            self.admit(foreign), authority.STATE_AUTHORITY_V2_BYTE_BINDING_MISMATCH)

    def test_ba17_adversarial_prestate_substitution_with_repaired_hashes_is_caught(self):
        """Invariant: the read prestate bytes are load bearing — substituting them and
        repairing `state_hash`/`cut` breaks proposal persistence and the replay identity."""
        precommit, proposal, child, postcommit = self.packet_graph()
        forged_pre = copy.deepcopy(precommit)
        forged_pre["events"].pop(proposal["event_id"], None)
        receipt = self.packet_receipt()
        _repair_read(receipt["prestate_read"], forged_pre)
        self.assert_named_rejection(
            self.verify(_seal(receipt)), authority.STATE_AUTHORITY_V2_STATE_SUBSTITUTION)

    # ---- 10. receipt replay across scope / transaction / subject / run -------------

    def test_ba18_adversarial_receipt_replay_across_identity_axes_is_rejected(self):
        """Invariant: the anti-replay block (nonce, scope, scenario, run, transaction) is
        inside the signed preimage and is checked against the injected identity; a
        re-signed receipt with one axis changed is a replay, not a new authority."""
        axes = (
            ("scope_id", "SCOPE.OTHER"),
            ("scenario_id", "SCENARIO.OTHER"),
            ("run_id", "RUN.MBCX01.BUILD.STATE.OTHER"),
            ("transaction_commit_id", "TXN.MBCX01.BUILD.STATE.0002"),
        )
        for field, value in axes:
            with self.subTest(field=field):
                receipt = self.packet_receipt()
                receipt["anti_replay"][field] = value
                self.assert_named_rejection(
                    self.verify(_seal(receipt)),
                    authority.STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID)
        with self.subTest(field="subject_identity"):
            receipt = self.packet_receipt(
                identity={"subject_identity": "SUBJECT.MBCX01.OTHER"})
            self.assert_named_rejection(
                self.verify(receipt),
                authority.STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID)

    # ---- 11. crash windows ----------------------------------------------------------

    def test_ba19_adversarial_crash_before_commit_leaves_pending_and_mints_nothing(self):
        """Invariant (crash-window law): a crash before the commit fsync leaves a PENDING
        distinguished terminal. PENDING is not "probably committed" — no receipt is
        mintable, and a hand-built receipt over those bytes fails verification."""
        store = store_mod.SingleWriterStateStore.open_verified(
            ":memory:", store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, _postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        with self.assertRaises(store_mod.StateStoreError):
            store.commit_transition(request, anti_replay=ANTI_REPLAY_ANCHORS,
                                    crash_point=store_mod.CRASH_BEFORE_COMMIT)
        rows = store.journal_rows(TRANSACTION_ID)
        self.assertEqual([row["status"] for row in rows], [store_mod.TRANSACTION_PENDING])
        with self.assertRaises(store_mod.StateStoreError):
            adapter.produce_state_authority_receipt_v2(
                store, request, signer=None, identity_config=IDENTITY_CONFIG)
        self.assert_named_rejection(
            self.verify(self.packet_receipt()),
            authority.STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED)

    def test_ba20_adversarial_partial_persistence_is_broken_and_mints_nothing(self):
        """Invariant: a proposal row with no applied-child row and no poststate snapshot
        is BROKEN — never silently repaired, never promoted, never mintable."""
        store = store_mod.SingleWriterStateStore.open_verified(
            ":memory:", store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, _postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        with self.assertRaises(store_mod.StateStoreError):
            store.commit_transition(
                request, anti_replay=ANTI_REPLAY_ANCHORS,
                crash_point=store_mod.CRASH_AFTER_PROPOSAL_ROW)
        rows = store.journal_rows(TRANSACTION_ID)
        self.assertEqual([row["status"] for row in rows], [store_mod.TRANSACTION_BROKEN])
        with self.assertRaises(store_mod.StateStoreError):
            adapter.produce_state_authority_receipt_v2(
                store, request, signer=None, identity_config=IDENTITY_CONFIG)

    def test_ba21_adversarial_committed_without_readback_mints_nothing(self):
        """Invariant: postcommit authority is a durable readback, not the writer's
        in-memory poststate. A commit whose readback never happened yields no receipt."""
        store = store_mod.SingleWriterStateStore.open_verified(
            ":memory:", store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, _postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        with self.assertRaises(store_mod.StateStoreError):
            adapter.produce_state_authority_receipt_v2(
                store, request, signer=None, identity_config=IDENTITY_CONFIG,
                )
        self.assertEqual(store.journal_rows(TRANSACTION_ID), [])

    # ---- 12. independent reducer disagreement --------------------------------------

    def test_ba22_adversarial_reducer_disagreement_is_fatal_and_never_discharges(self):
        """Invariant: reference/oracle reducer independence is load bearing. If the two
        FROZEN reducers disagree on the receipt's own child replay, the receipt is fatal —
        the verifier never picks a winner and never discharges the sentinel."""
        receipt = self.packet_receipt()
        original = oracle.oracle_apply

        def divergent(state, event):
            result_state, result = original(state, event)
            if isinstance(result_state, dict) and "next_seq" in result_state:
                result_state = copy.deepcopy(result_state)
                result_state["next_seq"] += 1
            return result_state, result

        try:
            oracle.oracle_apply = divergent
            errors = self.verify(receipt)
        finally:
            oracle.oracle_apply = original
        self.assert_named_rejection(
            errors, authority.STATE_AUTHORITY_V2_REDUCER_DISAGREEMENT)

    # ---- 13. operator independence ---------------------------------------------------

    def test_ba23_positive_operator_b_derives_byte_identical_receipt_content(self):
        """Invariant: operator B, sharing only schema and frozen hashing, must derive
        byte-identical receipt CONTENT from the same durable store bytes."""
        store = store_mod.SingleWriterStateStore.open_verified(
            ":memory:", store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, _postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        store.commit_transition(request, anti_replay=ANTI_REPLAY_ANCHORS)
        derived = operator_b.derive_receipt_content_independent(
            store.path, TRANSACTION_ID, identity_config=IDENTITY_CONFIG,
            trust_root_manifest=self.trust_root_manifest)
        receipt = self.packet_receipt()
        expected = {key: value for key, value in receipt.items()
                    if key not in authority.V2_UNSIGNED_KEYS}
        self.assertEqual(common.canonical_json(derived),
                         common.canonical_json(expected))
        self.assertEqual(
            authority.compare_operator_receipt_content(receipt, derived), [])

    def test_ba24_adversarial_poisoned_operator_b_finalizer_is_detected_not_absorbed(self):
        """Invariant: a poisoned operator-B finalizer must surface as DETECTED operator
        disagreement — the gate never averages, prefers, or silently drops one operator."""
        receipt = self.packet_receipt()
        content = {key: value for key, value in receipt.items()
                   if key not in authority.V2_UNSIGNED_KEYS}
        poisoned = copy.deepcopy(content)
        poisoned["postcommit_readback"]["reader_identity"] = "MBCX01.POISONED.READER"
        original = operator_b._finalize_readback_content

        def poison(*_args, **_kwargs):
            return poisoned["postcommit_readback"]

        try:
            operator_b._finalize_readback_content = poison
            errors = authority.compare_operator_receipt_content(receipt, poisoned)
        finally:
            operator_b._finalize_readback_content = original
        self.assert_named_rejection(
            errors, authority.STATE_AUTHORITY_V2_OPERATOR_DISAGREEMENT)

    # ---- 14. frozen-suite compatibility ---------------------------------------------

    def test_ba25_positive_frozen_state_suite_stays_green_alongside_build_modules(self):
        """Invariant: the BUILD-A modules are purely additive. The frozen r13.2 state
        suite runs untouched-green with them imported, and the frozen fixture path still
        answers exactly `STATE_AUTHORITY_UNAVAILABLE` under production admission.

        NOTE: this is the ONE witness that is green at the red stage by construction —
        a red here would mean the frozen suite had been broken."""
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "test_mbcx01_r13_state", "-v"],
            capture_output=True, text=True, timeout=600)
        self.assertEqual(result.returncode, 0, result.stderr[-4000:])
        self.assertIn("OK", result.stderr)
        v1 = self.scorer_input["state_authority_receipt"]
        self.assertEqual(
            reference.verify_state_authority_receipt(v1, require_production=True),
            [authority.STATE_AUTHORITY_SENTINEL])
        self.assertEqual(
            oracle.verify_state_authority_receipt(v1, require_production=True),
            [authority.STATE_AUTHORITY_SENTINEL])

    # ---- 15. durable anti-replay anchors (FOLD 1) -----------------------------------

    def release_stores_opened_by_this_witness(self, already_live):
        """Close every store THIS witness opened (see the note in `setUp`)."""
        for registry in (store_mod._OPEN_WRITERS, store_mod._STORES_BY_IDENTITY):
            for store in list(registry.values()):
                if id(store) not in already_live:
                    store.close()

    def open_store(self, path=store_mod.MEMORY_PATH):
        return store_mod.SingleWriterStateStore.open_verified(
            path, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])

    def committed_production_store(self, path=store_mod.MEMORY_PATH,
                                   anchors=None):
        """Commit the packet graph with a DURABLE anti-replay anchor set."""
        anchors = anchors or PRODUCTION_ANTI_REPLAY_ANCHORS
        store = self.open_store(path)
        precommit, proposal, child, _postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        store.commit_transition(request, anti_replay=anchors)
        config = dict(IDENTITY_CONFIG)
        config.update({key: value for key, value in anchors.items()
                       if key != "receipt_nonce"})
        return store, request, config

    def test_ba26_adversarial_anchors_matching_their_own_labels_but_not_the_durable_row(self):
        """Invariant (FOLD 1): the anti-replay anchor set is a DURABLE FACT written
        into the journal row at commit time, not a string transform of the receipt's
        own labels. Two halves, both load bearing:

        * control — a production-shaped anchor set whose scenario/run/nonce are
          INDEPENDENT identifiers (not `SCOPE.x -> SCENARIO.x`, `SUBJECT.x -> RUN.x`,
          `TXN.x -> NONCE.x`) is minted from the durable row and verifies clean;
        * forgery — a receipt whose anchors are exactly what a label transform would
          derive from its OWN labels, but which are NOT the durable row's anchors, is
          a named replay rejection even though every hash is repaired and the receipt
          is re-signed."""
        store, request, config = self.committed_production_store()
        self.assertEqual(store.anti_replay_anchors(TRANSACTION_ID),
                         PRODUCTION_ANTI_REPLAY_ANCHORS)
        receipt = adapter.produce_state_authority_receipt_v2(
            store, request, signer=_FixtureSigner, identity_config=config,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(receipt["anti_replay"], {
            "receipt_nonce": PRODUCTION_ANTI_REPLAY_ANCHORS["receipt_nonce"],
            "scope_id": PRODUCTION_ANTI_REPLAY_ANCHORS["scope_id"],
            "scenario_id": PRODUCTION_ANTI_REPLAY_ANCHORS["scenario_id"],
            "run_id": PRODUCTION_ANTI_REPLAY_ANCHORS["run_id"],
            "transaction_commit_id": TRANSACTION_ID})
        self.assertEqual(self.verify(receipt), [])

        forged = copy.deepcopy(receipt)
        forged["anti_replay"].update(
            receipt_nonce=LABEL_DERIVED_ANCHORS["receipt_nonce"],
            scenario_id=LABEL_DERIVED_ANCHORS["scenario_id"],
            run_id=LABEL_DERIVED_ANCHORS["run_id"])
        self.assert_named_rejection(
            self.verify(_seal(forged)),
            authority.STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID)

    def test_ba27_positive_operator_b_reproduces_the_anchors_from_the_store_alone(self):
        """Invariant (FOLD 1): operator B re-derives the anti-replay anchors and the
        attested subject identity from the DURABLE STORE ROW alone. An
        `identity_config` poisoned on every anchor axis cannot move them, and operator
        1's independently minted receipt still compares byte-identical."""
        store, request, config = self.committed_production_store()
        poisoned = dict(IDENTITY_CONFIG)
        poisoned.update(scope_id="SCOPE.POISONED", scenario_id="SCENARIO.POISONED",
                        run_id="RUN.POISONED", subject_identity="SUBJECT.POISONED")
        derived = operator_b.derive_receipt_content_independent(
            store.path, TRANSACTION_ID, identity_config=poisoned,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(derived["anti_replay"], {
            "receipt_nonce": PRODUCTION_ANTI_REPLAY_ANCHORS["receipt_nonce"],
            "scope_id": PRODUCTION_ANTI_REPLAY_ANCHORS["scope_id"],
            "scenario_id": PRODUCTION_ANTI_REPLAY_ANCHORS["scenario_id"],
            "run_id": PRODUCTION_ANTI_REPLAY_ANCHORS["run_id"],
            "transaction_commit_id": TRANSACTION_ID})
        self.assertEqual(derived["signer_identity"]["subject_identity"],
                         PRODUCTION_ANTI_REPLAY_ANCHORS["subject_identity"])
        receipt = adapter.produce_state_authority_receipt_v2(
            store, request, signer=_FixtureSigner, identity_config=config,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(
            authority.compare_operator_receipt_content(receipt, derived), [])

    # ---- 16. fresh-process file-backed verification (FOLD 2) ------------------------

    def test_ba28_positive_fresh_process_verifies_a_file_backed_receipt_cold(self):
        """Invariant (FOLD 2): production verification cannot depend on the verifying
        process having been the one that opened the store. A FRESH interpreter, with an
        empty live-store registry and nothing opened in advance, must resolve a
        FILE-backed store read-only from its injected durable path and reach the same
        verdicts: `[]` for the honest receipt, the named `TRANSACTION_NOT_COMMITTED`
        rejection for a receipt over a PENDING terminal, and — with NO locator injected
        — `TRANSACTION_IDENTITY_MISMATCH`, which proves the cold registry really is
        empty and the durable path is doing the work."""
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        store_path = os.path.join(directory, "mbcx01-build-state.sqlite3")
        try:
            store, request, config = self.committed_production_store(
                path=store_path, anchors=ANTI_REPLAY_ANCHORS)
            receipt = adapter.produce_state_authority_receipt_v2(
                store, request, signer=_FixtureSigner, identity_config=config,
                trust_root_manifest=self.trust_root_manifest)
            pending_request = dict(request,
                                   transaction_commit_id=PENDING_TRANSACTION_ID)
            with self.assertRaises(store_mod.StateStoreError):
                store.commit_transition(pending_request,
                                        anti_replay=ANTI_REPLAY_ANCHORS,
                                        crash_point=store_mod.CRASH_BEFORE_COMMIT)
            pending_receipt = self.packet_receipt(
                transaction_commit_id=PENDING_TRANSACTION_ID)
            store.close()
            self.assertIsNone(store_mod.registered_store(
                IDENTITY_CONFIG["store_id"], IDENTITY_CONFIG["namespace"],
                IDENTITY_CONFIG["namespace_version"]))

            answers = self.fresh_process_verify(store_path, receipt, pending_receipt)
            self.assertEqual(answers["honest_with_locator"], [])
            self.assert_named_rejection(
                answers["pending_with_locator"],
                authority.STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED)
            self.assert_named_rejection(
                answers["honest_without_locator"],
                authority.STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH)
        finally:
            shutil.rmtree(directory, ignore_errors=True)

    def fresh_process_verify(self, store_path, receipt, pending_receipt) -> dict:
        """Verify in a COLD interpreter: no imports, no registry, no open store."""
        payload = {"store_path": store_path, "receipt": receipt,
                   "pending_receipt": pending_receipt,
                   "manifest": self.trust_root_manifest, "custody": self.custody}
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8",
                                         delete=False) as stream:
            json.dump(payload, stream)
            payload_path = stream.name
        # The fresh interpreter receives the anchor the way an OPERATOR gives it to a
        # verifying process that nobody wired in code: an OS configuration path. It is
        # still not something the receipt, the manifest or the custody set can supply.
        # The document at that path is the TEST PRODUCTION anchor written to a temporary
        # file for this witness only — never committed — because after the r2 fold a
        # `fixture_only` anchor at that path is a REFUSAL, not a production root.
        # ⚠ DECLARED TIME DEPENDENCE: an anchor resolved from the OS path carries no
        # injected instant, so this witness judges the trust root at the REAL clock (the
        # r2 fold's F4 answer). It is therefore the ONE witness in this suite that is
        # time-dependent: it goes red when the committed fixture manifest's validity
        # window closes (`not_after` 2027-08-13), which is a correct refusal and a
        # reminder to re-issue the fixture window, not a defect in the verifier.
        anchor_directory = tempfile.mkdtemp(prefix="mbcx01-build-anchor-")
        self.addCleanup(shutil.rmtree, anchor_directory, True)
        environment = dict(os.environ)
        environment[trust_anchor.ANCHOR_PATH_ENV] = (
            ceremony.write_test_production_anchor(
                os.path.join(anchor_directory, "owner-trust-anchor.json")))
        try:
            result = subprocess.run(
                [sys.executable, "-c", FRESH_PROCESS_VERIFIER_SOURCE, payload_path],
                capture_output=True, text=True, timeout=300, check=False,
                env=environment)
        finally:
            os.unlink(payload_path)
        self.assertEqual(result.returncode, 0,
                         (result.stdout + result.stderr)[-4000:])
        return json.loads(result.stdout)

    # ---- 17. authenticated production trust bootstrap (BUILD acceptance r1) ---------

    def self_authored_manifest(self) -> dict:
        """An ENTIRELY attacker-authored `StateTrustRootManifestV1`.

        Fixture-SHAPED on purpose: this is the exact universe SEAT3's F1 probe built,
        and before the r1 fold the verifier DEMANDED that shape for production, so it
        cleared admission with `[]`.
        """
        manifest = _load_trust_root_manifest()
        manifest["manifest_id"] = "ATTACKER.SELF.AUTHORED.STATE.MANIFEST"
        policy = manifest["trust_policy"]
        policy["signer_custodian_role"] = "ATTACKER_NAMED_STATE_CUSTODIAN"
        policy["trust_root_editor_role"] = "ATTACKER_NAMED_STATE_EDITOR"
        manifest["trust_policy_digest"] = common.sha384(policy)
        manifest["custody_roles"]["signer_custodian_role"] = (
            "ATTACKER_NAMED_STATE_CUSTODIAN")
        manifest["custody_roles"]["trust_root_editor_role"] = (
            "ATTACKER_NAMED_STATE_EDITOR")
        for root in manifest["roots"]:
            root["trust_policy_digest"] = manifest["trust_policy_digest"]
        manifest["roots"][0]["key_id"] = SELF_AUTHORED_KEY_ID
        manifest["roots"][0]["public_key_pem"] = SELF_AUTHORED_PUBLIC_KEY_PEM
        return manifest

    def self_authored_custody(self) -> dict:
        """Custody evidence the attacker writes for itself (codex F1 used "A"*96)."""
        return {
            "signer_custodian_role": "ATTACKER_NAMED_STATE_CUSTODIAN",
            "trust_root_editor_role": "ATTACKER_NAMED_STATE_EDITOR",
            "signer_key_ids": [SELF_AUTHORED_KEY_ID],
            "root_editor_key_ids": ["ATTACKER.SELF.AUTHORED.STATE.EDITOR.TEST.1"],
            "key_custody_attestation_digest": "A" * 96,
            "root_editor_approval_digest": "A" * 96,
            "store_build_provenance_digest": "A" * 96,
            "signing_ceremony_receipt_digest": "A" * 96,
        }

    def committed_packet_store(self):
        """Commit the packet graph so the durable half of the receipt is honest."""
        store = self.open_store()
        precommit, proposal, child, postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        store.commit_transition(request, anti_replay=ANTI_REPLAY_ANCHORS)
        self.addCleanup(store.close)
        return store

    def test_ba29_adversarial_fully_self_authored_state_universe_is_refused(self):
        """Invariant: a fresh attacker Ed25519 key + an attacker-authored manifest +
        attacker-authored custody evidence + an attacker-signed activation + an
        attacker-signed `StateAuthorityReceiptV2` over a genuinely committed
        transaction is refused BY NAME and never reaches scientific admission.

        This is the r1 deciding attack on BUILD A (SEAT3 F1, EXECUTED). Before the fold
        both `verify_state_authority_receipt_v2` and `verify_production_scorer_input`
        answered `[]` for exactly this input."""
        self.committed_packet_store()
        manifest = self.self_authored_manifest()
        custody = self.self_authored_custody()
        custody[authority.OWNER_ACTIVATION_EVIDENCE] = _owner_activation(
            manifest, custody, private_key_pem=SELF_AUTHORED_PRIVATE_KEY_PEM)
        precommit, proposal, child, postcommit = self.packet_graph()
        receipt = _v2_receipt(
            precommit, proposal, child, postcommit,
            identity={"signer_key_id": SELF_AUTHORED_KEY_ID,
                      "trust_root_id": manifest["manifest_id"],
                      "trust_policy_digest": manifest["trust_policy_digest"]},
            private_key_pem=SELF_AUTHORED_PRIVATE_KEY_PEM)
        errors = self.verify(receipt, trust_root_manifest=manifest, custody=custody)
        self.assert_named_rejection(
            errors, authority.STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)
        admitted = authority.verify_production_scorer_input(
            self.scorer_input, receipt, expected_manifest=self.manifest,
            trust_root_manifest=manifest, custody_evidence=custody)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, admitted)
        self.assertIn(authority.STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED, admitted)
        # The frozen production verdict is preserved in full: nothing was discharged.
        self.assertTrue(set(self.frozen_errors) <= set(admitted), admitted)

    def test_ba30_adversarial_production_manifest_without_owner_signature_is_refused(self):
        """Invariant: PRODUCTION shape is not authority. The same production-shaped
        manifest, presented with an activation that is signed by a key that is not the
        anchor / binds a different manifest / predates the operator's generation / is
        missing, is a named refusal every time."""
        self.committed_packet_store()
        manifest = _production_state_manifest()
        receipt = self.packet_receipt()
        cases = {
            "not-the-anchor": _state_custody_evidence(
                manifest,
                private_key_pem=ceremony.FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM),
            "binds-another-manifest": _state_custody_evidence(
                manifest,
                overrides={"manifest_digest": common.sha384("SOME.OTHER.MANIFEST")}),
            "rolled-back-generation": _state_custody_evidence(
                manifest, overrides={"activation_generation": 0}),
            "anchor-id-substituted": _state_custody_evidence(
                manifest, overrides={"anchor_id": "ATTACKER.SELF.AUTHORED.ANCHOR.1"}),
        }
        for label, custody in cases.items():
            with self.subTest(case=label):
                self.assert_named_rejection(
                    self.verify(receipt, trust_root_manifest=manifest, custody=custody),
                    authority.STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED)
        absent = _state_custody_evidence(manifest)
        del absent[authority.OWNER_ACTIVATION_EVIDENCE]
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=absent),
            authority.STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID)

    def test_ba31_positive_anchored_ceremony_manifest_admits_and_takes_no_anchor_param(self):
        """Invariant: the LEGITIMATE authenticated ceremony path is green. The ceremony
        spec's own production-shaped manifest (`production_ready:true`, `ACTIVATED`,
        roots not `fixture_only`) — which the pre-fold verifier REFUSED with
        `STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED` — is admitted when, and only when, the
        operator-preconfigured owner anchor has signed it; and no anchor can be passed
        to either production entry point, which is what makes the api-caller unable to
        supply one."""
        for name in ("verify_state_authority_receipt_v2",
                     "verify_production_scorer_input"):
            parameters = set(inspect.signature(getattr(authority, name)).parameters)
            self.assertNotIn("anchor", " ".join(parameters))
            self.assertNotIn("trust_anchor", parameters)
        manifest = _production_state_manifest()
        self.assertIs(manifest["production_ready"], True)
        self.assertEqual(manifest["trust_policy"]["status"], "ACTIVATED")
        self.assertTrue(all(root["fixture_only"] is False
                            for root in manifest["roots"]))
        store = self.committed_packet_store()
        request = {"transaction_commit_id": TRANSACTION_ID,
                   "prestate": self.packet_graph()[0],
                   "proposal_event": self.packet_graph()[1],
                   "applied_child_event": self.packet_graph()[2]}
        receipt = adapter.produce_state_authority_receipt_v2(
            store, request, signer=_FixtureSigner, identity_config=IDENTITY_CONFIG,
            trust_root_manifest=manifest)
        self.assertEqual(
            self.verify(receipt, trust_root_manifest=manifest,
                        custody=_state_custody_evidence(manifest)), [])
        self.assertEqual(
            authority.verify_production_scorer_input(
                self.scorer_input, receipt, expected_manifest=self.manifest,
                trust_root_manifest=manifest,
                custody_evidence=_state_custody_evidence(manifest)), [])

    def test_ba32_adversarial_unconfigured_anchor_fails_closed(self):
        """Invariant: "nobody configured a root of trust" must never read as "no root of
        trust was required". With the process anchor cleared, the ONLY otherwise-clean
        production path is a named refusal that keeps the sentinel."""
        store = self.committed_packet_store()
        manifest = _production_state_manifest()
        custody = _state_custody_evidence(manifest)
        request = {"transaction_commit_id": TRANSACTION_ID,
                   "prestate": self.packet_graph()[0],
                   "proposal_event": self.packet_graph()[1],
                   "applied_child_event": self.packet_graph()[2]}
        receipt = adapter.produce_state_authority_receipt_v2(
            store, request, signer=_FixtureSigner, identity_config=IDENTITY_CONFIG,
            trust_root_manifest=manifest)
        self.assertEqual(self.verify(receipt, trust_root_manifest=manifest,
                                     custody=custody), [])
        trust_anchor.clear_owner_trust_anchor()
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody),
            authority.STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE)

    def test_ba33_adversarial_whitespace_injected_signature_carrier_is_refused(self):
        """Invariant (MBCX01-BUILD-R1-SIGNATURE-CARRIER / codex F6): one signature has
        exactly ONE accepted carrier. A whitespace-injected but otherwise valid Ed25519
        carrier — which a permissive base64 decoder accepts, giving one receipt many
        accepted byte strings — is a named refusal, on the receipt AND on the owner
        activation statement."""
        self.committed_packet_store()
        receipt = self.packet_receipt()
        self.assertEqual(self.verify(receipt), [])
        carrier = receipt["signature_b64"]
        self.assertTrue(trust_anchor.strict_signature_carrier_ok(carrier))
        for mutation in (carrier[:8] + "\n" + carrier[8:],
                         carrier[:8] + " " + carrier[8:],
                         carrier.replace("+", "-").replace("/", "_")):
            if mutation == carrier:
                continue
            with self.subTest(carrier=mutation[:16]):
                forged = copy.deepcopy(receipt)
                forged["signature_b64"] = mutation
                self.assert_named_rejection(
                    self.verify(forged),
                    authority.STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID)
        manifest = _production_state_manifest()
        custody = _state_custody_evidence(manifest)
        statement = custody[authority.OWNER_ACTIVATION_EVIDENCE]
        statement["signature_b64"] = (statement["signature_b64"][:8] + "\n"
                                      + statement["signature_b64"][8:])
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody),
            authority.STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID)

    # ---- 18. in-memory route isolation ----------------------------------------------

    def test_ba37_adversarial_a_second_in_memory_store_cannot_answer_the_first_ones_reader(self):
        """Invariant (codex BUILD acceptance finding on `mbcx01_build_state_store.py:270`):
        an in-memory store's INDEPENDENT reader reads THAT store's durable bytes.

        RED against the pre-fold bytes: every `open_verified(":memory:")` overwrote one
        shared `_MEMORY_TARGETS[":memory:"]` entry, so opening a second in-memory store
        silently re-pointed the FIRST store's independent readback and operator B at the
        second store's database — a cross-store read, or a false `READBACK_MISSING` for a
        transaction the first store had durably committed. Each store now carries its own
        routing key; the bare `":memory:"` and the key of a CLOSED store name no store at
        all and are refused rather than answered with whatever is live."""
        precommit, proposal, child, postcommit = self.packet_graph()
        request = {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                   "proposal_event": proposal, "applied_child_event": child}
        first = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        self.addCleanup(first.close)
        first.commit_transition(request, anti_replay=ANTI_REPLAY_ANCHORS)

        second = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, store_id="STORE.MBCX01.BUILD.STATE.SECOND",
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        self.addCleanup(second.close)

        # Two LIVE in-memory stores: two routing keys, two databases, no shared entry.
        self.assertNotEqual(first.path, second.path)
        first_uri = store_mod.readonly_connection_uri(first.path)
        self.assertNotEqual(first_uri, store_mod.readonly_connection_uri(second.path))

        # The first store still reads its OWN committed poststate back...
        readback = first.independent_readback(
            TRANSACTION_ID, reader_identity=IDENTITY_CONFIG["reader_identity"])
        self.assertEqual(json.loads(readback["state_utf8"]), postcommit)
        # ...and operator B, addressing it by its own key, derives the same store's rows.
        derived = operator_b.derive_receipt_content_independent(
            first.path, TRANSACTION_ID, identity_config=IDENTITY_CONFIG,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(derived["postcommit_readback"]["state_utf8"],
                         readback["state_utf8"])
        # The second store never heard of that transaction and says so, rather than
        # answering with the first store's bytes.
        with self.assertRaises(operator_b.OperatorBError) as unknown:
            operator_b.derive_receipt_content_independent(
                second.path, TRANSACTION_ID, identity_config=IDENTITY_CONFIG,
                trust_root_manifest=self.trust_root_manifest)
        self.assertIn("OPERATOR_B_TRANSACTION_UNKNOWN", str(unknown.exception))

        # The bare `":memory:"` is not a durable identity: it names no store.
        with self.assertRaises(store_mod.StateStoreError) as unresolved:
            store_mod.readonly_connection_uri(store_mod.MEMORY_PATH)
        self.assertEqual(str(unresolved.exception), "STATE_STORE_TARGET_UNRESOLVED")

        # Closing one in-memory store retires ONLY its own route.
        retired = second.path
        second.close()
        with self.assertRaises(store_mod.StateStoreError) as closed:
            store_mod.readonly_connection_uri(retired)
        self.assertEqual(str(closed.exception), "STATE_STORE_TARGET_UNRESOLVED")
        self.assertEqual(store_mod.readonly_connection_uri(first.path), first_uri)
        self.assertEqual(
            json.loads(first.independent_readback(
                TRANSACTION_ID,
                reader_identity=IDENTITY_CONFIG["reader_identity"])["state_utf8"]),
            postcommit)

    # ---- 19. interprocess journal sequence allocation (r3 P1) -----------------------

    def test_ba38_adversarial_two_producer_processes_cannot_mint_the_same_journal_seq(self):
        """Invariant (codex r3 P1, `mbcx01_build_state_store.py:298-300`): the durable
        journal sequence is allocated by the DATABASE, inside the write transaction that
        writes the row — never by a read that precedes it.

        RED against the pre-fold bytes: `_OPEN_WRITERS` is a process-local dict, so both
        producer processes below took the writer door, both read `MAX(seq) + 1` before
        either opened its transaction, and both committed `seq = 1` — two durable rows
        wearing the same journal sequence number under a docstring that advertised a
        single-writer invariant. The two processes are held at the exact seam the finding
        names (between the sequence read and the write transaction) so the interleaving
        is deterministic rather than hoped for.

        What the fold does NOT claim: nothing here is an interprocess lock or lease, and
        the writer door is not mutual exclusion across processes. The serialization is
        sqlite's own one-writer-at-a-time write transaction, and `journal_seq_unique` is
        the durable constraint behind it."""
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        self.addCleanup(shutil.rmtree, directory, True)
        barrier_directory = os.path.join(directory, "barrier")
        os.makedirs(barrier_directory)
        store_path = os.path.join(directory, "mbcx01-build-state.sqlite3")
        # The store exists before either producer starts: this witness is about SEQUENCE
        # allocation, not about two processes racing the initial DDL.
        self.open_store(store_path).close()

        processes = [
            subprocess.Popen(
                [sys.executable, "-c", TWO_PRODUCER_WORKER_SOURCE, tag, peer,
                 store_path, barrier_directory, txn, IDENTITY_CONFIG["store_id"],
                 IDENTITY_CONFIG["namespace"],
                 str(IDENTITY_CONFIG["namespace_version"])],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for tag, peer, txn in (("A", "B", TRANSACTION_ID),
                                   ("B", "A", SECOND_PRODUCER_TRANSACTION_ID))]
        answers = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=300)
            self.assertEqual(process.returncode, 0, (stdout + stderr)[-4000:])
            answers.append(json.loads(stdout))
        self.assertEqual(len({answer["pid"] for answer in answers}), 2)

        connection = sqlite3.connect(store_path)
        try:
            rows = connection.execute(
                "SELECT transaction_commit_id, seq FROM journal ORDER BY seq").fetchall()
            indexes = connection.execute("PRAGMA index_list('journal')").fetchall()
        finally:
            connection.close()
        sequences = [row[1] for row in rows]
        self.assertEqual(len(rows), 2, rows)
        self.assertEqual(sequences, [1, 2], rows)
        self.assertEqual(sorted(answer["seq"] for answer in answers), [1, 2])
        self.assertTrue(any(row[1] == "journal_seq_unique" and row[2] == 1
                            for row in indexes), indexes)

    # ---- 20. a mistaken path is refused, never adopted (r3 P2) ----------------------

    def test_ba39_adversarial_an_unrelated_database_is_refused_before_any_ddl_runs(self):
        """Invariant (codex r3 P2, `mbcx01_build_state_store.py:316-317`): a path that
        names somebody else's sqlite database is REFUSED by name, with no store schema
        written into it.

        RED against the pre-fold bytes: the store DDL ran first, and because the `meta`
        table it had just created was empty, the very next branch read that emptiness as
        "fresh store" and stamped the unrelated database as this store — mutating and
        claiming it instead of refusing the mistaken path. The identity signals are
        sqlite's own (`sqlite_master`, `application_id`), read BEFORE any DDL.

        Both honest arms are witnessed alongside the refusal, because a store that
        refuses right paths is not a fix: an empty file still initializes and gets
        stamped, and a real store file still re-opens."""
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        self.addCleanup(shutil.rmtree, directory, True)
        foreign_path = os.path.join(directory, "someone-elses-accounting.sqlite3")
        foreign = sqlite3.connect(foreign_path)
        try:
            foreign.execute("CREATE TABLE invoices (id INTEGER PRIMARY KEY, amount TEXT)")
            foreign.execute("INSERT INTO invoices (id, amount) VALUES (1, '42.00')")
            foreign.commit()
        finally:
            foreign.close()

        def objects(path):
            connection = sqlite3.connect(path)
            try:
                return (sorted(row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                    " AND name NOT LIKE 'sqlite_%'")),
                    connection.execute("PRAGMA application_id").fetchone()[0])
            finally:
                connection.close()

        before = objects(foreign_path)
        self.assertEqual(before, (["invoices"], 0))
        with self.assertRaises(store_mod.StateStoreError) as refused:
            self.open_store(foreign_path)
        self.assertEqual(str(refused.exception), "STATE_STORE_FOREIGN_DATABASE")
        self.assertEqual(objects(foreign_path), before)
        connection = sqlite3.connect(foreign_path)
        try:
            self.assertEqual(connection.execute("SELECT * FROM invoices").fetchall(),
                             [(1, "42.00")])
        finally:
            connection.close()

        # An empty file with another application's `application_id` is equally not ours.
        stamped_path = os.path.join(directory, "other-application.sqlite3")
        stamped = sqlite3.connect(stamped_path)
        try:
            stamped.execute("PRAGMA application_id=252")
            stamped.commit()
        finally:
            stamped.close()
        with self.assertRaises(store_mod.StateStoreError) as stamped_refusal:
            self.open_store(stamped_path)
        self.assertEqual(str(stamped_refusal.exception), "STATE_STORE_FOREIGN_DATABASE")

        # Honest arms: a fresh file initializes and is stamped, and re-opens.
        store_path = os.path.join(directory, "mbcx01-build-state.sqlite3")
        self.open_store(store_path).close()
        tables, application_id = objects(store_path)
        self.assertEqual(tables, ["children", "journal", "meta", "proposals", "snapshots"])
        self.assertEqual(application_id, store_mod.STORE_APPLICATION_ID)
        reopened = self.open_store(store_path)
        self.addCleanup(reopened.close)
        self.assertEqual(reopened.store_identity, {
            "store_id": IDENTITY_CONFIG["store_id"],
            "namespace": IDENTITY_CONFIG["namespace"],
            "namespace_version": IDENTITY_CONFIG["namespace_version"]})

    # ---- 21. the verifier answers with a closed list, always (r3 P2) ----------------

    def test_ba40_adversarial_unusable_root_material_is_refused_not_raised(self):
        """Invariant (codex r3 P2, `mbcx01_build_state_authority.py:862-866`): the public
        verifier answers with a CLOSED LIST for every input, including one whose own
        authority material cannot be used.

        RED against the pre-fold bytes: a malformed root PEM in the injected manifest
        made the node verifier exit non-zero, `_invoke_signature_verifier` raised, and
        the raw `StateAuthorityError` escaped `verify_state_authority_receipt_v2` — so
        caller-supplied material CRASHED verification instead of being refused by it, and
        no `STATE_AUTHORITY_UNAVAILABLE` was retained for the caller to see. Both arms of
        the finding are witnessed: unusable key material, and a verifier program that
        cannot be run at all.

        The refusal is its own code, not `..._SIGNATURE_INVALID`: "this signature was not
        checked" is a different fact from "this signature is wrong"."""
        receipt = self.packet_receipt()
        broken = copy.deepcopy(self.trust_root_manifest)
        for root in broken["roots"]:
            if root["key_id"] == receipt["signer_identity"]["signer_key_id"]:
                root["public_key_pem"] = MALFORMED_ROOT_PUBLIC_KEY_PEM
        verdict = self.verify(receipt, trust_root_manifest=broken)
        self.assertIsInstance(verdict, list)
        self.assert_named_rejection(
            verdict, authority.STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE)
        self.assertNotIn(authority.STATE_AUTHORITY_V2_SIGNATURE_INVALID, verdict)

        # Second arm: the verifier program itself is unreachable.
        original = authority.SIGNATURE_VERIFIER
        self.addCleanup(setattr, authority, "SIGNATURE_VERIFIER", original)
        authority.SIGNATURE_VERIFIER = os.path.join(
            os.path.dirname(original), "no-such-receipt-verifier.mjs")
        unreachable = self.verify(receipt)
        self.assertIsInstance(unreachable, list)
        self.assert_named_rejection(
            unreachable, authority.STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE)

    # ---- 22. the refusal happens before the first byte is written (r4 FOLD-2A) -------

    @staticmethod
    def file_digest(path):
        with open(path, "rb") as stream:
            return hashlib.sha256(stream.read()).hexdigest()

    @staticmethod
    def database_signals(path):
        """`(user objects, application_id, user_version, journal_mode)` of a db file."""
        connection = sqlite3.connect(path)
        try:
            return (sorted(row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
                " AND name NOT LIKE 'sqlite_%'")),
                int(connection.execute("PRAGMA application_id").fetchone()[0]),
                int(connection.execute("PRAGMA user_version").fetchone()[0]),
                str(connection.execute("PRAGMA journal_mode").fetchone()[0]).upper())
        finally:
            connection.close()

    def test_ba41_adversarial_a_foreign_database_is_refused_without_being_written_to(self):
        """Invariant (codex r4 FOLD-2A, `mbcx01_build_state_store.py:330-331`): a path that
        names an unrelated sqlite database is refused with that database's BYTES exactly as
        they were — no PRAGMA, no DDL, no sidecar files, nothing.

        RED against the pre-fold bytes: `PRAGMA journal_mode=WAL` ran BEFORE any identity
        signal was read, and WAL is a PERSISTENT property stored in the database header, so
        `STATE_STORE_FOREIGN_DATABASE` was raised only after another application's database
        had already been rewritten (`journal_mode` DELETE -> WAL) by this store. ba39 could
        not see it: it compared the table list and `application_id`, neither of which the
        PRAGMA touches. The discriminator here is the file digest itself.

        Arm labels, honestly: the two refusal arms and the digest assertions are RED
        pre-fold. The 'not a database at all' arm and the fresh-file arms are GUARDS — they
        pass pre-fold and are here so the repair cannot buy untouched-ness by refusing
        paths it should accept, or by swallowing an unreadable file into a false verdict.
        """
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        self.addCleanup(shutil.rmtree, directory, True)

        # Arm 1 (RED pre-fold): somebody else's database, with rows in it.
        foreign_path = os.path.join(directory, "someone-elses-accounting.sqlite3")
        foreign = sqlite3.connect(foreign_path)
        try:
            foreign.execute("CREATE TABLE invoices (id INTEGER PRIMARY KEY, amount TEXT)")
            foreign.execute("INSERT INTO invoices (id, amount) VALUES (1, '42.00')")
            foreign.commit()
        finally:
            foreign.close()
        before_digest = self.file_digest(foreign_path)
        self.assertEqual(self.database_signals(foreign_path),
                         (["invoices"], 0, 0, "DELETE"))
        with self.assertRaises(store_mod.StateStoreError) as refused:
            self.open_store(foreign_path)
        self.assertEqual(str(refused.exception), "STATE_STORE_FOREIGN_DATABASE")
        self.assertEqual(self.file_digest(foreign_path), before_digest)
        self.assertEqual(self.database_signals(foreign_path),
                         (["invoices"], 0, 0, "DELETE"))
        self.assertEqual(sorted(os.listdir(directory)),
                         ["someone-elses-accounting.sqlite3"])

        # Arm 2 (RED pre-fold): another application's stamped, tableless database.
        stamped_path = os.path.join(directory, "other-application.sqlite3")
        stamped = sqlite3.connect(stamped_path)
        try:
            stamped.execute("PRAGMA application_id=252")
            stamped.execute("CREATE TABLE ledger (id INTEGER PRIMARY KEY)")
            stamped.commit()
        finally:
            stamped.close()
        stamped_digest = self.file_digest(stamped_path)
        with self.assertRaises(store_mod.StateStoreError) as stamped_refusal:
            self.open_store(stamped_path)
        self.assertEqual(str(stamped_refusal.exception), "STATE_STORE_FOREIGN_DATABASE")
        self.assertEqual(self.file_digest(stamped_path), stamped_digest)
        self.assertEqual(self.database_signals(stamped_path),
                         (["ledger"], 252, 0, "DELETE"))

        # Arm 3 (GUARD, passes pre-fold): a file that is not a database at all is still
        # a loud sqlite failure and is still left exactly as it was. The repair must not
        # quietly turn an unreadable file into "fresh store" or into a foreign verdict it
        # never actually read.
        garbage_path = os.path.join(directory, "operator-notes.txt")
        with open(garbage_path, "wb") as stream:
            stream.write(b"this is not a sqlite database\n" * 64)
        garbage_digest = self.file_digest(garbage_path)
        with self.assertRaises(sqlite3.DatabaseError):
            self.open_store(garbage_path)
        self.assertEqual(self.file_digest(garbage_path), garbage_digest)

        # Arm 4 (GUARD): the honest arms still work — a path with no file, and a
        # zero-length file, both initialize and are stamped, and re-open.
        for name in ("mbcx01-build-state.sqlite3", "pre-touched.sqlite3"):
            store_path = os.path.join(directory, name)
            if name == "pre-touched.sqlite3":
                with open(store_path, "wb"):
                    pass
                self.assertEqual(os.path.getsize(store_path), 0)
            self.open_store(store_path).close()
            objects, application_id, user_version, _mode = self.database_signals(
                store_path)
            self.assertEqual(objects,
                             ["children", "journal", "meta", "proposals", "snapshots"])
            self.assertEqual(application_id, store_mod.STORE_APPLICATION_ID)
            self.assertEqual(user_version, store_mod.STORE_SCHEMA_VERSION)
            reopened = self.open_store(store_path)
            self.assertEqual(reopened.store_identity, {
                "store_id": IDENTITY_CONFIG["store_id"],
                "namespace": IDENTITY_CONFIG["namespace"],
                "namespace_version": IDENTITY_CONFIG["namespace_version"]})
            reopened.close()

    def test_ba44_adversarial_a_tableless_database_with_a_user_version_is_not_adopted(self):
        """Invariant (codex r4 FOLD-2A, second discriminator): `user_version` is an
        identity signal like `sqlite_master` and `application_id`. A database that carries
        a nonzero `user_version` this store did not write is not this store's file.

        RED against the pre-fold bytes: the refusal condition read only
        `(existing_objects or stamped_application_id)`, so a tableless database whose only
        mark was `user_version = 4242` passed the foreign check, had the store schema
        written into it, and was ADOPTED — the tell was then destroyed by the very
        initialization that adopted it (`PRAGMA user_version=2` overwrote 4242), leaving
        no trace that another application's file had just been taken over.

        The GUARD half is the same one ba41 carries: an unmarked empty database still
        initializes, so the signal refuses foreign files without refusing fresh ones."""
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        self.addCleanup(shutil.rmtree, directory, True)
        tableless_path = os.path.join(directory, "other-application-tableless.sqlite3")
        tableless = sqlite3.connect(tableless_path)
        try:
            tableless.execute("PRAGMA user_version=4242")
            tableless.commit()
        finally:
            tableless.close()
        self.assertEqual(self.database_signals(tableless_path), ([], 0, 4242, "DELETE"))
        before_digest = self.file_digest(tableless_path)

        with self.assertRaises(store_mod.StateStoreError) as refused:
            self.open_store(tableless_path)
        self.assertEqual(str(refused.exception), "STATE_STORE_FOREIGN_DATABASE")
        self.assertEqual(self.file_digest(tableless_path), before_digest)
        self.assertEqual(self.database_signals(tableless_path), ([], 0, 4242, "DELETE"))

        # GUARD: an unmarked database (no objects, no application_id, no user_version)
        # is a fresh store and still initializes.
        fresh_path = os.path.join(directory, "fresh.sqlite3")
        unmarked = sqlite3.connect(fresh_path)
        unmarked.close()
        self.assertEqual(self.database_signals(fresh_path), ([], 0, 0, "DELETE"))
        self.open_store(fresh_path).close()
        self.assertEqual(self.database_signals(fresh_path)[1:3],
                         (store_mod.STORE_APPLICATION_ID, store_mod.STORE_SCHEMA_VERSION))

    # ---- 23. one live store per store identity (r4 FOLD-2B) --------------------------

    def test_ba42_adversarial_a_second_store_cannot_take_a_live_stores_identity(self):
        """Invariant (codex r4 FOLD-2B, `mbcx01_build_state_store.py:401`): the identity
        `(store_id, namespace, namespace_version)` resolves to ONE live durable store, and
        a second store that claims a live identity is refused by name.

        RED against the pre-fold bytes: `_STORES_BY_IDENTITY[identity] = store` replaced
        the entry unconditionally, so opening a SECOND database file under the same
        identity silently re-pointed verification at it. The receipt of a transaction
        durably COMMITTED in the first store then resolved against the second store, where
        that transaction does not exist: `transaction_terminal` answered `None` and the
        verifier answered `TRANSACTION_IDENTITY_MISMATCH` for a receipt that is true. That
        is right evidence refused, and (with a colliding transaction id) wrong evidence
        admitted. Closing the second store then removed resolution for the first one
        entirely, because `close()` only deletes the entry it still owns.

        Design choice, stated: the repair REFUSES the second open rather than making
        resolution path-aware. Path-aware resolution is the larger change and is not even
        well defined here — `registered_store` is reached from a RECEIPT
        (`mbcx01_build_state_authority.py:672`), a receipt carries store IDENTITY and never
        a path (deliberately: a receipt must not point a verifier at a store its own holder
        chose), and an in-memory store has no durable path at all. Refusal also matches the
        door already next to it, `STATE_STORE_WRITER_ALREADY_OPEN`.

        The reopen arm is a GUARD: the refusal is about a LIVE identity, not a permanent
        ban, so once the first store closes the identity is free again."""
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-")
        self.addCleanup(shutil.rmtree, directory, True)
        first_path = os.path.join(directory, "first.sqlite3")
        second_path = os.path.join(directory, "second.sqlite3")

        first, request, config = self.committed_production_store(path=first_path)
        receipt = adapter.produce_state_authority_receipt_v2(
            first, request, signer=_FixtureSigner, identity_config=config,
            trust_root_manifest=self.trust_root_manifest)
        self.assertEqual(self.verify(receipt), [])

        second = None
        refusal = None
        try:
            second = self.open_store(second_path)
        except store_mod.StateStoreError as exc:
            refusal = str(exc)
        if second is not None:
            self.addCleanup(second.close)

        # The harm first: the live first store still owns its identity and its receipt.
        self.assertEqual(
            store_mod.transaction_terminal(
                IDENTITY_CONFIG["store_id"], IDENTITY_CONFIG["namespace"],
                IDENTITY_CONFIG["namespace_version"], TRANSACTION_ID),
            store_mod.TRANSACTION_COMMITTED)
        self.assertIs(store_mod.registered_store(
            IDENTITY_CONFIG["store_id"], IDENTITY_CONFIG["namespace"],
            IDENTITY_CONFIG["namespace_version"]), first)
        self.assertEqual(self.verify(receipt), [])
        # Then the refusal itself, by name, with no second store and no second file.
        self.assertEqual(refusal, "STATE_STORE_IDENTITY_ALREADY_OPEN")
        self.assertIsNone(second)
        self.assertFalse(os.path.exists(second_path))

        # GUARD: a CLOSED identity is free again — this refuses live collisions only.
        first.close()
        reopened = self.open_store(second_path)
        self.addCleanup(reopened.close)
        self.assertIs(store_mod.registered_store(
            IDENTITY_CONFIG["store_id"], IDENTITY_CONFIG["namespace"],
            IDENTITY_CONFIG["namespace_version"]), reopened)

    # ---- 24. the verifier answers a closed list for malformed custody lists (r4 2C) ---

    def test_ba43_adversarial_a_malformed_custody_key_list_is_a_named_refusal(self):
        """Invariant (codex r4 FOLD-2C, `mbcx01_build_state_authority.py:545`): the public
        verifier answers with a CLOSED LIST for every input — caller-supplied custody
        material can refuse a receipt, it cannot crash the verification.

        RED against the pre-fold bytes: `set(signer_keys) & set(editor_keys)` was built
        from list elements nobody had checked, so an otherwise valid custody object whose
        `signer_key_ids` carried a dict raised a raw `TypeError: unhashable type: 'dict'`
        out of `verify_state_authority_receipt_v2`. Same family as the ETW thread-roster
        row fold: posture unchanged, refusal named.

        Third arm, also RED: an element that is hashable but is not a key id at all (an
        integer) never raised — it was silently ACCEPTED by the custody check, so a custody
        object carrying junk alongside the real key passed the separation test. Element
        validation closes both."""
        receipt = self.packet_receipt()
        honest = self.verify(receipt)
        self.assertIsInstance(honest, list)
        self.assertNotIn(authority.STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID, honest)

        signer_key_id = receipt["signer_identity"]["signer_key_id"]
        self.assertIn(signer_key_id, self.custody["signer_key_ids"])
        editor_key_id = self.custody["root_editor_key_ids"][0]

        for label, mutation in (
                ("unhashable dict in signer_key_ids",
                 {"signer_key_ids": [signer_key_id, {}]}),
                ("unhashable list in root_editor_key_ids",
                 {"root_editor_key_ids": [editor_key_id, ["nested"]]}),
                ("hashable non-identifier in signer_key_ids",
                 {"signer_key_ids": [signer_key_id, 12]})):
            with self.subTest(label):
                custody = copy.deepcopy(self.custody)
                custody.update(mutation)
                verdict = self.verify(receipt, custody=custody)
                self.assertIsInstance(verdict, list)
                self.assert_named_rejection(
                    verdict, authority.STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID)
                self.assertTrue(all(isinstance(code, str) for code in verdict))


    # ---- 25. a dict is not a STATE: the closed verdict covers that too (r5 P2) ------

    def test_ba45_adversarial_a_state_shaped_non_state_returns_the_closed_verdict(self):
        """Invariant (codex r5 P2): `verify_state_authority_receipt_v2` answers with a
        CLOSED ERROR LIST for every input, including a receipt whose state bytes parse
        to a dict that is not a STATE.

        RED against the pre-fix bytes: `_structural_errors` asked only
        `isinstance(json.loads(state_utf8), dict)`, so canonical `{}` — a dict, exactly
        canonical, with an exactly recomputed hash — was carried as NON-fatal, and
        `_semantic_errors` then raised a raw `KeyError('next_seq')` out of
        `mbcx01_r13_common.current_cut` (:111) and out of the public verifier. The
        POSTURE is unchanged — such a receipt never verified — and the refusal is now
        named, exactly as the `_custody_errors` key-list fold (ba43) and the ETW
        roster-row fold (bw93) did for their sites.

        RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_state_authority.py`,
        sha256 593a21d6b7fe590c564a50e89c6a2fa5d643cfa0b411acf5c8a3fdf64776f5b0, loaded
        under the real module name and hash-asserted before the run) — errors=4:

            ERROR [prestate is canonical {}] / [readback is canonical {}] /
                  [prestate carries every state key but next_seq]
            File "mbcx01_build_state_authority.py", line 778, in _semantic_errors
              if (pre_cut != common.current_cut(prestate) ...
            File "mbcx01_r13_common.py", line 111, in current_cut
              return {"journal_seq": state["next_seq"] - 1,
            KeyError: 'next_seq'

            ERROR [prestate next_seq is a string]
            TypeError: unsupported operand type(s) for -: 'str' and 'int'
        """
        honest = self.verify(self.packet_receipt())
        self.assertNotIn(authority.STATE_AUTHORITY_V2_SCHEMA_INVALID, honest)

        for label, name, state in (
                ("prestate is canonical {}", "prestate_read", {}),
                ("readback is canonical {}", "postcommit_readback", {}),
                ("prestate carries every state key but next_seq", "prestate_read",
                 {key: value for key, value in common.initial_state().items()
                  if key != "next_seq"}),
                ("prestate next_seq is a string", "prestate_read",
                 dict(common.initial_state(), next_seq="1"))):
            with self.subTest(label):
                receipt = self.packet_receipt()
                row = receipt[name]
                row["state_utf8"] = common.canonical_json(state).decode("utf-8")
                row["state_hash"] = common.sha384(row["state_utf8"].encode("utf-8"))
                receipt = _seal(receipt)
                verdict = self.verify(receipt)
                self.assertIsInstance(verdict, list)
                self.assertTrue(all(isinstance(code, str) for code in verdict))
                self.assert_named_rejection(
                    verdict, authority.STATE_AUTHORITY_V2_SCHEMA_INVALID)

    # ---- 26. instants, not text: validity endpoints are parsed before ordering ------

    def test_ba46_adversarial_mixed_precision_validity_windows_compare_as_instants(self):
        """Invariant (codex r5 P2, second class): a validity window is an interval
        between two CALENDAR INSTANTS, and the verifier's instant is compared to it as
        an instant.

        RED against the pre-fix bytes, in two directions at once, because the
        comparison was LEXICAL and the two sides are written in different spellings —
        state manifests carry six fractional digits (`mbcx01_r13_common.UTC`, :71) and
        `ProductionVerifierContext.current_instant` emits whole seconds
        (`mbcx01_build_trust_anchor.py:445-450`):

          * WRONG REFUSAL — `'Z'` (0x5A) sorts after `'.'` (0x2E), so a legal
            `not_after` of `...00.500000Z` read EXPIRED at `...00Z`. Right evidence was
            refused up to a second early, which on a measurement harness is a wrong
            number, not a safe default;
          * WRONG ADMISSION — the same lexical compare happily ORDERED a window whose
            endpoints are not calendar instants at all, so
            `2020-00-00T00:00:00.000000Z .. 2030-99-99T99:99:99.999999Z` admitted. That
            arm is the state-plane twin of bw64 and is carried here rather than left
            unwitnessed.

        RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_state_authority.py`,
        sha256 593a21d6b7fe590c564a50e89c6a2fa5d643cfa0b411acf5c8a3fdf64776f5b0, loaded
        under the real module name and hash-asserted before the run):

            FAIL: AssertionError: Lists differ:
            ['STATE_AUTHORITY_UNAVAILABLE', 'STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED']
            != []

        and, on the non-calendar arm, the same pre-fix bytes returned `[]` — the window
        `2020-00-00 .. 2030-99-99` ADMITTED (driver-reproducible: both modules loaded
        side by side, pre-fix `[]` vs post-fix
        `['STATE_AUTHORITY_UNAVAILABLE', 'STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED']`).
        """
        store = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, postcommit = self.packet_graph()
        store.commit_transition(
            {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
             "proposal_event": proposal, "applied_child_event": child},
            anti_replay=ANTI_REPLAY_ANCHORS)
        receipt = _v2_receipt(precommit, proposal, child, postcommit)
        instant = "2026-08-14T00:00:00Z"

        def verdict_for(not_after):
            manifest = _production_state_manifest()
            manifest["validity"] = {"not_before": "2026-08-12T00:00:00.000000Z",
                                    "not_after": not_after}
            trust_anchor.configure_owner_trust_anchor(
                ceremony.test_production_anchor_document(), current_time=instant)
            return self.verify(receipt, trust_root_manifest=manifest,
                               custody=_state_custody_evidence(manifest))

        # The premise, at the byte: the instant is INSIDE the window in time and
        # OUTSIDE it in text.
        self.assertFalse(instant < "2026-08-14T00:00:00.500000Z")
        # CONTROL — a whole second of window, which text and time agree about.
        self.assertEqual(verdict_for("2026-08-14T00:00:01.000000Z"), [])
        # The half second the two disagreed about: still admitted, by the clock.
        self.assertEqual(verdict_for("2026-08-14T00:00:00.500000Z"), [])

        non_calendar = _production_state_manifest()
        non_calendar["validity"] = {"not_before": "2020-00-00T00:00:00.000000Z",
                                    "not_after": "2030-99-99T99:99:99.999999Z"}
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document(), current_time=instant)
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=non_calendar,
                        custody=_state_custody_evidence(non_calendar)),
            authority.STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)
        # Both document spellings parse, and they order by TIME; nothing else parses.
        self.assertLess(authority.parse_instant(instant),
                        authority.parse_instant("2026-08-14T00:00:00.500000Z"))
        for value in ("2026-02-30T00:00:00.000000Z", "2026-08-14T24:00:00.000000Z",
                      "2026-08-14T00:00:00.500Z", "2026-08-14T00:00:00",
                      None, 20260814, {}):
            with self.subTest(value=value):
                self.assertIsNone(authority.parse_instant(value))
        store.close()

    def test_ba47_adversarial_the_root_window_comparison_orders_instants_not_text(self):
        """Invariant (codex r5 P2 class — the ENUMERATED remaining member of the same
        site set): `_root_errors` compares the receipt's attested `knowledge_time`
        against the ROOT and MANIFEST validity windows; those comparisons are between
        CALENDAR INSTANTS, not strings.

        The site set, enumerated from the module rather than from the finding
        (the four-partial-fixes law): `:527-530`-class window comparison — folded in the
        r5 round; `_root_errors` `:691-695` — THIS fold; `:863` — homogeneous by
        construction (both sides come from `common.current_cut`), left as-is.

        RED against the pre-fold bytes (the worktree state after the r5 folds, before
        this one — the fold's own commit message carries the hash): a MANIFEST validity
        window written in the WHOLE-SECOND spelling (`...T00:00:00Z`), chronologically
        containing the microsecond attested instant, was REFUSED
        `STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED`, because `'.'` (0x2E) sorts before
        `'Z'` (0x5A) and the microsecond instant read as EARLIER than the whole-second
        `not_before` — right evidence refused. The non-calendar-window admission arm of
        this site comes free from the same parse (a window that does not parse is
        inside the refusal disjunction); its independent red lives at the sibling
        sites (bw64, ba46), and mutating the ROOT window here would additionally
        require mutating signed receipt material, which would refuse for a different
        reason first — enumerated honestly rather than faked.
        """
        store = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        precommit, proposal, child, postcommit = self.packet_graph()
        store.commit_transition(
            {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
             "proposal_event": proposal, "applied_child_event": child},
            anti_replay=ANTI_REPLAY_ANCHORS)
        receipt = _v2_receipt(precommit, proposal, child, postcommit)
        instant = "2026-08-14T00:00:00Z"

        manifest = _production_state_manifest()
        # Whole-second spelling; chronologically the attested microsecond instant sits
        # AT not_before (<= holds) and the context instant is inside; lexically the
        # microsecond spelling sorts BEFORE the whole-second not_before.
        manifest["validity"] = {"not_before": "2026-08-13T00:00:00Z",
                                "not_after": "2026-08-15T00:00:00Z"}
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document(), current_time=instant)
        self.assertEqual(
            self.verify(receipt, trust_root_manifest=manifest,
                        custody=_state_custody_evidence(manifest)), [])
        store.close()

    # ---- 27. the closed verdict is TOTAL at the boundary, not per shape (r6) --------

    def _receipt_with_prestate(self, state):
        """A resealed receipt whose prestate bytes are exactly `state`."""
        receipt = self.packet_receipt()
        row = receipt["prestate_read"]
        row["state_utf8"] = common.canonical_json(state).decode("utf-8")
        row["state_hash"] = common.sha384(row["state_utf8"].encode("utf-8"))
        return _seal(receipt)

    def test_ba48_adversarial_a_scope_map_whose_values_are_not_scopes_is_named(self):
        """Invariant (codex-CLI r6 SEAT1 F3, `mbcx01_build_state_authority.py:312`):
        `_is_state_shaped` decides whether the frozen reducers can be RUN on a state,
        so it has to look at the scope MAP's values, not only at its type.

        RED against the pre-fix bytes: the r5 guard asked `isinstance(value["scopes"],
        dict)` and stopped there, so a receipt whose prestate maps a scope id to
        `null` (or to a list) was carried as a STATE, reached the dual-reducer replay
        in `_semantic_errors`, and raised a raw `TypeError` out of the public verifier
        — the same broken promise ba43 and ba45 each closed at their own site.

        The POSTURE is unchanged: such a receipt never verified. Both arms are the
        `_is_state_shaped` refusal now; ba49 covers the shapes no site-level guard
        anticipates.

        Measured RED against the PRE-FIX bytes (`git show
        HEAD:mbcx01_build_state_authority.py`, sha256
        b617f9a2424b9831341f49b070dbd9447d7d8341cd6cd58e17798b862b96221e, exported to a
        scratch tree and hash-asserted before the run):

            ERROR [scope id maps to null]
            File "mbcx01_build_state_authority.py", line 935,
              in verify_state_authority_receipt_v2
            File "mbcx01_build_state_authority.py", line 1024,
              in _verify_state_authority_receipt_v2
                errors.extend(_semantic_errors(receipt, prestate, poststate, ...
            File "mbcx01_build_state_authority.py", line 890, in _semantic_errors
                reference_state, reference_result = reference.reference_apply(
            File "mbcx01_r13_state_reference.py", line 129, in _apply_effect
                obligations = scope["obligations"]
            TypeError: 'NoneType' object is not subscriptable

            ERROR [scope id maps to a list]   (same frames)
            TypeError: list indices must be integers or slices, not str

            ERROR [scope id maps to a string]  (same frames)
            TypeError: string indices must be integers, not 'str'
        """
        honest = self.packet_graph()[0]
        self.assertNotIn(authority.STATE_AUTHORITY_V2_SCHEMA_INVALID,
                         self.verify(self.packet_receipt()))
        self.assertTrue(authority._is_state_shaped(honest))

        for label, scopes in (
                ("scope id maps to null", {"SCOPE.SHARED": None}),
                ("scope id maps to a list", {"SCOPE.SHARED": ["not", "a", "scope"]}),
                ("scope id maps to a string", {"SCOPE.SHARED": "SCOPE"})):
            with self.subTest(label):
                state = copy.deepcopy(honest)
                state["scopes"] = scopes
                # The verifier is asked FIRST, so the pre-fix red is the raw
                # traceback escaping the public boundary, not a helper's answer.
                verdict = self.verify(self._receipt_with_prestate(state))
                self.assertIsInstance(verdict, list)
                self.assertTrue(all(isinstance(code, str) for code in verdict))
                self.assert_named_rejection(
                    verdict, authority.STATE_AUTHORITY_V2_SCHEMA_INVALID)
                self.assertFalse(authority._is_state_shaped(state))

        # DISCRIMINATING: the guard reads the scope VALUES, and an EMPTY scope map is
        # still a state — refusing it would refuse a legal state and cost a true
        # receipt. The honest receipt above already pins the populated case.
        empty_scopes = copy.deepcopy(honest)
        empty_scopes["scopes"] = {}
        self.assertTrue(authority._is_state_shaped(empty_scopes))

    def test_ba49_adversarial_the_closed_verdict_covers_shapes_nobody_enumerated(self):
        """Invariant (codex-CLI r6 SEAT1 F3/F4 WHOLESALE CLOSE): the closed error list
        is a property of the BOUNDARY `verify_state_authority_receipt_v2`, not a
        property of the shapes three rounds of findings happened to name.

        The three preceding folds (ba43 custody key list, ba45 state-shaped non-state,
        ba48 non-scope scope values) each closed ONE site, and each time the next
        unanticipated malformed shape found the next site. The complement closes the
        class: every member of
        `authority.MALFORMED_CALLER_INPUT_EXCEPTIONS` raised anywhere under the public
        call is converted to the named schema refusal plus the sentinel.

        THE SHAPE BELOW IS CONSTRUCTED FOR THIS WITNESS AND NO PER-SITE GUARD
        ANTICIPATES IT — deliberately, because a shape some guard catches would prove
        nothing about the complement. `applied_child.event_utf8` parses to a dict (so
        `_structural_errors` passes it) whose `event_id` is itself a dict, and
        `_semantic_errors` uses that value as a MAPPING KEY.

        Measured RED against the PRE-FIX bytes (`git show
        HEAD:mbcx01_build_state_authority.py`, sha256
        b617f9a2424b9831341f49b070dbd9447d7d8341cd6cd58e17798b862b96221e):

            ERROR [applied_child event_id is a dict]
            File "mbcx01_build_state_authority.py", line 884, in _semantic_errors
              or poststate.get("events", {}).get(child.get("event_id"))
            TypeError: unhashable type: 'dict'

        ⚠ HONESTY, ASSERTED NOT MERELY DOCUMENTED: the complement catches the
        enumerated tuple and nothing else. An internal defect outside it — here an
        `AssertionError` injected into the private verifier — still escapes LOUD, and
        the module's own `StateAuthorityError` is re-raised rather than answered as a
        caller schema code. A verifier that converted its own bugs into "your input is
        malformed" would be reporting a wrong number about itself.
        """
        receipt = self.packet_receipt()
        child = json.loads(receipt["applied_child"]["event_utf8"])
        child["event_id"] = {"unhashable": True}
        receipt["applied_child"]["event_utf8"] = (
            common.canonical_json(child).decode("utf-8"))
        receipt["applied_child"]["event_hash"] = common.sha384(
            receipt["applied_child"]["event_utf8"].encode("utf-8"))
        verdict = self.verify(_seal(receipt))
        self.assertIsInstance(verdict, list)
        self.assertTrue(all(isinstance(code, str) for code in verdict))
        self.assert_named_rejection(verdict,
                                    authority.STATE_AUTHORITY_V2_SCHEMA_INVALID)

        # The FIXTURE lane answers with the same named code and no sentinel to
        # discharge, which is the contract `require_production=False` already has.
        fixture_verdict = authority.verify_state_authority_receipt_v2(
            _seal(receipt), trust_root_manifest=self.trust_root_manifest,
            custody_evidence=self.custody, require_production=False)
        self.assertEqual([authority.STATE_AUTHORITY_V2_SCHEMA_INVALID],
                         fixture_verdict)

        # The complement is EXACTLY the enumerated tuple, and the enumeration is the
        # lane's own (`mbcx01_build_cohort_packet`'s `frozen_verdict`).
        self.assertEqual(
            (AttributeError, IndexError, KeyError, StopIteration, TypeError,
             UnicodeError, ValueError),
            authority.MALFORMED_CALLER_INPUT_EXCEPTIONS)

        # HONESTY ARM 1: a defect of THIS module is not a caller-shaped refusal.
        # HONESTY ARM 2: the module's OWN named error is a ValueError subclass and is
        # still raised, not converted — when this module speaks, the caller hears it.
        original = authority._verify_state_authority_receipt_v2
        for raised, expected in ((AssertionError("WITNESS_INTERNAL_DEFECT"),
                                  AssertionError),
                                 (authority.StateAuthorityError("WITNESS_MODULE_FAULT"),
                                  authority.StateAuthorityError)):
            with self.subTest(raised=type(raised).__name__):
                def broken(*args, _raised=raised, **kwargs):
                    raise _raised

                authority._verify_state_authority_receipt_v2 = broken
                try:
                    with self.assertRaises(expected) as caught:
                        self.verify(self.packet_receipt())
                finally:
                    authority._verify_state_authority_receipt_v2 = original
                self.assertIs(raised, caught.exception)

        # DISCRIMINATING: the complement did not turn the verifier into a black box.
        # A well-formed receipt is still judged on its MERITS and still gets the
        # specific codes for what is wrong with it — here the uncommitted transaction
        # — never the schema catch-all.
        specific = self.verify(self.packet_receipt())
        self.assertIn(authority.STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH,
                      specific)
        self.assertNotIn(authority.STATE_AUTHORITY_V2_SCHEMA_INVALID, specific)

    # ---- 19. the read-only door answers for the SCHEMA too (codex-CLI r9 F2) --------

    def _committed_file_store_and_receipt(self, directory):
        """A real COMMITTED file-backed store, its receipt, and the store CLOSED.

        Closed on purpose: with the live registry empty, `_resolve_store` has to reach
        the durable bytes through the injected path, which is the arm under test.
        """
        store_path = os.path.join(directory, "mbcx01-build-state.sqlite3")
        store, request, config = self.committed_production_store(
            path=store_path, anchors=ANTI_REPLAY_ANCHORS)
        receipt = adapter.produce_state_authority_receipt_v2(
            store, request, signer=_FixtureSigner, identity_config=config,
            trust_root_manifest=self.trust_root_manifest)
        store.close()
        self.assertIsNone(store_mod.registered_store(
            IDENTITY_CONFIG["store_id"], IDENTITY_CONFIG["namespace"],
            IDENTITY_CONFIG["namespace_version"]))
        return store_path, receipt

    def test_ba51_red_a_truncated_store_is_a_verdict_not_a_raw_sqlite_error(self):
        """codex-CLI r9 F2: the public verifier ANSWERS about a store it cannot read.

        THE SHAPE. A store file that carries every IDENTITY signal — the `meta` header
        rows, `application_id`, `user_version` — but has lost a table a reader is
        answered from. `ReadOnlyStateStoreView.open_verified_readonly` checked exactly
        the identity signals, admitted the file, and the first question asked of it
        (`SELECT * FROM journal`, `mbcx01_build_state_authority.py:842`) raised a raw
        `sqlite3.OperationalError`. That class is NOT in
        `MALFORMED_CALLER_INPUT_EXCEPTIONS` — correctly, because a driver-level sqlite
        fault is not a statement about the caller's receipt — so the r6 wholesale
        boundary did not close it and it escaped the documented closed contract.

        Measured RED against the PRE-FIX bytes of `mbcx01_build_state_store.py`
        (`git show HEAD:mbcx01_build_state_store.py`, sha256
        9b353df56bb0580321ceb60f2f68e2f0e597d0e4c2bf7672f3621f7714df4414) and
        `mbcx01_build_state_authority.py` (sha256
        de42cbb06fbaba554c8042bfd166c7584ea88d195f250ae76fce9173df138f3d):

            ERROR: ...test_ba51_red... (dropped='journal')
              File "mbcx01_build_state_authority.py", line 842, in _durable_terminal_errors
                rows = store.journal_rows(receipt["transaction_commit_id"])
              File "mbcx01_build_state_store.py", line 973, in journal_rows
                cursor = self._connection.execute(
            sqlite3.OperationalError: no such table: journal

            ERROR: ...test_ba51_red... (dropped='proposals' / 'children' / 'snapshots')
              File "mbcx01_build_state_authority.py", line 868, in _durable_evidence_errors
                durable = store.transaction_rows(receipt["transaction_commit_id"])
              File "mbcx01_build_state_store.py", line 990, in transaction_rows
                row = self._connection.execute(
            sqlite3.OperationalError: no such table: proposals

        THE RED FOUND MORE THAN THE REPORTED MEMBER, which is why the arms below are
        the enumerated required set rather than the one table the finding named: the
        raw sqlite fault escapes at TWO sites, `:842` (`_durable_terminal_errors`) for
        `journal` and `:868` (`_durable_evidence_errors` -> `transaction_rows`) for
        each of `proposals`, `children` and `snapshots`. Closing `:842` alone would
        have left three siblings live.

        THE FIX IS AT THE DOOR, NOT AT THE BOUNDARY. Widening the boundary's
        exception tuple to swallow `sqlite3.Error` would make "I could not read my own
        store" come out as "your receipt is malformed" — the wrong number that
        boundary's own honesty constraint forbids. So the read-only view refuses by
        name (`STATE_STORE_SCHEMA_INCOMPLETE`) before it answers anything, and
        `_resolve_store` reads that as "no durable store resolved": the documented
        transaction-identity refusal plus the sentinel.

        ⛔ Every database here lives in a temporary directory this witness removes.
        """
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-truncated-")
        self.addCleanup(shutil.rmtree, directory, True)
        store_path, receipt = self._committed_file_store_and_receipt(directory)

        # GUARD FIRST, so the refusal below cannot be an artefact of the fixture: the
        # UNTRUNCATED store at this very path verifies clean through the injected path.
        self.assertEqual([], authority.verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=self.trust_root_manifest,
            custody_evidence=self.custody, store_path=store_path))

        # The enumerated required set, one member at a time — the reported member
        # (`journal`) and its neighbours, because a fix that closed only the shape
        # somebody reported is the defect this lane has now met three times.
        for table in ("journal", "proposals", "children", "snapshots"):
            with self.subTest(dropped=table):
                truncated = os.path.join(directory, "truncated-%s.sqlite3" % table)
                shutil.copyfile(store_path, truncated)
                connection = sqlite3.connect(truncated, isolation_level=None)
                connection.execute("DROP TABLE %s" % table)
                connection.close()

                # The IDENTITY signals all survive the truncation: this file still
                # looks exactly like this store to every check that existed before.
                objects, application_id, user_version = (
                    store_mod.pre_existing_identity_signals(truncated))
                self.assertNotIn(table, objects)
                self.assertIn("meta", objects)
                self.assertEqual(store_mod.STORE_APPLICATION_ID, application_id)
                self.assertEqual(store_mod.STORE_SCHEMA_VERSION, user_version)

                verdict = authority.verify_state_authority_receipt_v2(
                    receipt, trust_root_manifest=self.trust_root_manifest,
                    custody_evidence=self.custody, store_path=truncated)
                self.assertIsInstance(verdict, list)
                self.assertTrue(all(isinstance(code, str) for code in verdict))
                self.assert_named_rejection(
                    verdict,
                    authority.STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH)

                # And the store module says WHICH table by name, rather than leaving
                # the operator to read a driver message.
                with self.assertRaises(store_mod.StateStoreError) as refusal:
                    store_mod.ReadOnlyStateStoreView.open_verified_readonly(
                        truncated, store_id=IDENTITY_CONFIG["store_id"],
                        namespace=IDENTITY_CONFIG["namespace"],
                        namespace_version=IDENTITY_CONFIG["namespace_version"])
                self.assertEqual("STATE_STORE_SCHEMA_INCOMPLETE:" + table,
                                 str(refusal.exception))

    def test_ba51_guard_the_untruncated_store_is_untouched_by_the_new_door(self):
        """GUARD — a door that refused a WHOLE store would be a new defect, not a fix.

        The complete store answers `[]`, its read-only view opens and reads rows, and
        the required-table set is the store's own schema rather than a list this
        witness maintains: it is derived from `_SCHEMA`, so a table added there and
        forgotten here cannot silently leave the door narrower than the store.
        """
        directory = tempfile.mkdtemp(prefix="mbcx01-build-state-complete-")
        self.addCleanup(shutil.rmtree, directory, True)
        store_path, receipt = self._committed_file_store_and_receipt(directory)
        view = store_mod.ReadOnlyStateStoreView.open_verified_readonly(
            store_path, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        self.addCleanup(view.close)
        self.assertEqual(store_mod.TRANSACTION_COMMITTED,
                         view.journal_rows(TRANSACTION_ID)[0]["status"])
        self.assertEqual(ANTI_REPLAY_ANCHORS, view.anti_replay_anchors(TRANSACTION_ID))
        self.assertEqual([], authority.verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=self.trust_root_manifest,
            custody_evidence=self.custody, store_path=store_path))
        # The set the door enforces IS the set the schema creates.
        created = {statement.split("EXISTS ")[1].split(" ")[0].strip("(")
                   for statement in store_mod._SCHEMA
                   if statement.startswith("CREATE TABLE")}
        self.assertEqual(created, set(store_mod.STORE_REQUIRED_TABLES))


class BuildAFixtureIsolationWitnesses(unittest.TestCase):
    """ba34-ba35: the r2 fix class FIXTURE_ISOLATION on BUILD A.

    Same ONE invariant as bw22-bw27 on BUILD B: production verification accepts exactly
    an immutable, instance-scoped verifier context whose anchor is operator-supplied and
    not fixture-marked, carrying its own current time, and refuses everything else.
    """

    maxDiff = None

    def setUp(self):
        ceremony.configure_test_production_anchor()
        self.addCleanup(ceremony.configure_test_production_anchor)
        self.manifest = packets.packet_fixture_manifest()
        self.scorer_input = packets.build_scoring_fixture(self.manifest, "OM")

    def packet_graph(self):
        transition = self.scorer_input["transition_authority"]
        return (copy.deepcopy(transition["precommit_state"]),
                copy.deepcopy(transition["proposal_event"]),
                copy.deepcopy(transition["applied_child_event"]),
                copy.deepcopy(transition["postcommit_state"]))

    def committed_packet_store(self):
        store = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, store_id=IDENTITY_CONFIG["store_id"],
            namespace=IDENTITY_CONFIG["namespace"],
            namespace_version=IDENTITY_CONFIG["namespace_version"])
        self.addCleanup(store.close)
        precommit, proposal, child, _postcommit = self.packet_graph()
        store.commit_transition(
            {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
             "proposal_event": proposal, "applied_child_event": child},
            anti_replay=ANTI_REPLAY_ANCHORS)
        return store

    def produce(self, store, manifest):
        precommit, proposal, child, _postcommit = self.packet_graph()
        return adapter.produce_state_authority_receipt_v2(
            store, {"transaction_commit_id": TRANSACTION_ID, "prestate": precommit,
                    "proposal_event": proposal, "applied_child_event": child},
            signer=_FixtureSigner, identity_config=IDENTITY_CONFIG,
            trust_root_manifest=manifest)

    def verify(self, receipt, *, trust_root_manifest, custody):
        return authority.verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=trust_root_manifest,
            custody_evidence=custody, require_production=True)

    def assert_named_rejection(self, errors, named):
        self.assertIn(named, errors)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, errors)

    def test_ba34_adversarial_committed_fixture_anchor_cannot_grant_state_production(self):
        """Invariant (codex r2 F1 on BUILD A): the COMMITTED fixture owner anchor, whose
        private half is committed and therefore public, cannot authorize production state
        admission — not at `verify_state_authority_receipt_v2` and not at
        `verify_production_scorer_input` — while the FIXTURE LANE
        (`require_production=False`) over the very same receipt stays green."""
        store = self.committed_packet_store()
        manifest = _production_state_manifest()
        document = ceremony.fixture_owner_anchor_document()
        custody = _state_custody_evidence(
            manifest, anchor_id=document["anchor_id"],
            private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
        receipt = self.produce(store, manifest)
        ceremony.configure_fixture_owner_anchor()
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody),
            authority.STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY)
        admitted = authority.verify_production_scorer_input(
            self.scorer_input, receipt, expected_manifest=self.manifest,
            trust_root_manifest=manifest, custody_evidence=custody)
        self.assertIn(authority.STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY, admitted)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, admitted)
        # The FIXTURE LANE is untouched: the same receipt still parses and verifies
        # structurally with production authority NOT required.
        self.assertEqual(
            authority.verify_state_authority_receipt_v2(
                receipt, trust_root_manifest=manifest, custody_evidence=custody,
                require_production=False), [])

    def test_ba35_adversarial_state_trust_root_stale_at_the_verifier_clock(self):
        """Invariant (codex r2 F4 on BUILD A): trust-root freshness is judged at the
        VERIFIER's instant. A manifest whose validity window contains the receipt's own
        attested `knowledge_time` but closed before the verifier's clock is refused by
        name — a verifier must not accept a root because the artifact under verification
        says the root was fresh when the artifact was made."""
        store = self.committed_packet_store()
        manifest = _production_state_manifest()
        manifest["validity"] = {"not_before": "2026-08-12T00:00:00.000000Z",
                                "not_after": "2026-08-14T00:00:00.000000Z"}
        custody = _state_custody_evidence(manifest)
        receipt = self.produce(store, manifest)
        instant = receipt["postcommit_readback"]["cut"]["knowledge_time"]
        self.assertTrue(manifest["validity"]["not_before"] <= instant
                        < manifest["validity"]["not_after"])
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody),
            authority.STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED)
        # The same manifest under a verifier context whose instant IS inside the window
        # admits: the refusal is the clock, not the manifest.
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document(),
            current_time="2026-08-13T00:00:00Z")
        self.assertEqual(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody), [])

    def test_ba36_adversarial_committed_test_signing_key_is_not_state_production_signing_material(self):
        """Invariant (BUILD acceptance r4 seat finding, EXECUTED on BUILD B and closed on
        BOTH planes): the committed-key refusal covers the SIGNING key class, not only
        the anchor class.

        A council seat made the committed test signing pair the PRODUCTION measurement
        signing root under an independently generated owner anchor — so this is NOT the
        anchor class ba34 already closes — and cleared production admission with
        `production_admission_errors = []`. The state plane has the same shape: the
        committed `MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json` writer key,
        relabelled into a production-shaped manifest, signed a receipt that admitted.
        `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 steps 0 and 3 forbid exactly this —
        every key in a production manifest is generated in the ceremony, never copied
        out of a committed fixture document — but prose is not a control.

        Both state production doors refuse it by name, and the FIXTURE lane
        (`require_production=False`) over the very same receipt stays green."""
        store = self.committed_packet_store()
        manifest = _production_state_manifest(committed_fixture_keys=True)
        # The premise, at the byte: this production-shaped manifest's writer root IS the
        # committed fixture document's writer root, and the owner anchor is independent.
        self.assertEqual(
            manifest["roots"][0]["public_key_pem"],
            _load_trust_root_manifest()["roots"][0]["public_key_pem"])
        self.assertIs(manifest["production_ready"], True)
        self.assertEqual({root["fixture_only"] for root in manifest["roots"]}, {False})
        self.assertNotIn(
            trust_anchor.public_key_identity(
                ceremony.test_production_anchor_document()["public_key_pem"]),
            trust_anchor.committed_fixture_key_material())
        custody = _state_custody_evidence(manifest)
        receipt = _v2_receipt(*self.packet_graph(),
                              private_key_pem=FIXTURE_WRITER_PRIVATE_KEY_PEM)
        self.assert_named_rejection(
            self.verify(receipt, trust_root_manifest=manifest, custody=custody),
            authority.STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL)
        admitted = authority.verify_production_scorer_input(
            self.scorer_input, receipt, expected_manifest=self.manifest,
            trust_root_manifest=manifest, custody_evidence=custody)
        self.assertIn(authority.STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL, admitted)
        self.assertIn(authority.STATE_AUTHORITY_SENTINEL, admitted)
        # CONTROL — the FIXTURE lane is untouched: the same receipt over the same
        # manifest still verifies structurally with production authority NOT required.
        self.assertEqual(
            authority.verify_state_authority_receipt_v2(
                receipt, trust_root_manifest=manifest, custody_evidence=custody,
                require_production=False), [])
        # CONTROL — the same production path over roots generated IN MEMORY for this run,
        # which are in no committed document, is green.
        generated = _production_state_manifest()
        self.assertEqual(
            self.verify(self.produce(store, generated),
                        trust_root_manifest=generated,
                        custody=_state_custody_evidence(generated)), [])


class BuildAStoreUriEncodingWitnesses(unittest.TestCase):
    """ba50: the store opens the file it was ASKED for, not one sqlite parsed out of it.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_state_store.py`,
    sha256 eb5778d0749420e06421b7f208fd178c3baecef317f7ae12fa46c0fe50cac375 — the
    worktree checkout hashes the same, byte for byte), loaded from a scratch directory
    placed at `sys.path[0]`; the runner PRINTS the bound module's `__file__` and sha256
    and ASSERTS the pre-fix copy won, because a red harness that silently binds the
    worktree copy reports PASS and FAIL exactly like a real one.

    codex-CLI r8 P1 (WRONG STORE, ADMITTED BEHIND A GREEN CHECK). Three `file:` URIs
    were built by string concatenation and handed to `sqlite3.connect(..., uri=True)`,
    which parses `#` as a fragment separator, `?` as a query separator and `%` as an
    escape introducer. `#` and `%` are both LEGAL WINDOWS FILENAME CHARACTERS, so:

      * a store requested at `<dir>\\a#b.sqlite` OPENED `<dir>\\a`. `refuse_foreign_
        database()` inspected the REQUESTED path — which does not exist, so it returned
        without refusing anything — while the writer connection addressed a DIFFERENT
        file and stamped this store's schema, `application_id` and `user_version` into
        somebody else's database. The identity check was green about a file the
        connection never touched;
      * the read-only door had the same defect twice over: `readonly_connection_uri()`
        appends `?mode=ro` AFTER the path, so with a `#` in the name the whole
        `?mode=ro` fell inside the discarded fragment and the "non-writing" connection
        was not read-only either;
      * and a file literally named `a%23b.sqlite` — legal on NTFS — was decoded to
        `a#b.sqlite`, so the requested store and the opened store were different files
        with no metacharacter mistake anywhere in the operator's configuration.

    THE FIX IS ONE ENCODER, and the SET of URI-construction sites is enumerated rather
    than sampled: `sqlite_file_uri()` (writable target), the same function under
    `readonly_connection_uri()` (`?mode=ro`), and `sqlite_memory_uri()` (the shared-cache
    in-memory target, whose name this module mints itself). `grep -n '"file:'` over the
    module returns exactly those two constructions plus the docstring quotation.

    ⛔ Nothing here signs, mints or verifies a receipt, and every database it opens
    lives in a temporary directory it removes.
    """

    maxDiff = None

    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix="mbcx01-store-uri-")
        self.addCleanup(shutil.rmtree, self.directory, True)
        self.addCleanup(store_mod._OPEN_WRITERS.clear)
        self.addCleanup(store_mod._STORES_BY_IDENTITY.clear)

    def _identity(self, store_id="STORE.MBCX01.BUILD.STATE.URI"):
        return {"store_id": store_id, "namespace": IDENTITY_CONFIG["namespace"],
                "namespace_version": IDENTITY_CONFIG["namespace_version"]}

    def _foreign_database(self, name):
        """A file that is unmistakably SOMEBODY ELSE'S database."""
        path = os.path.join(self.directory, name)
        connection = sqlite3.connect(path, isolation_level=None)
        connection.execute("PRAGMA application_id=305419896")
        connection.execute("CREATE TABLE somebody_elses_table (x)")
        connection.execute("INSERT INTO somebody_elses_table VALUES ('do not touch')")
        connection.close()
        return path

    def _digest(self, path):
        with open(path, "rb") as stream:
            return hashlib.sha256(stream.read()).hexdigest()

    def _addressed_by(self, connection):
        return connection.execute("PRAGMA database_list").fetchall()[0][2]

    def test_ba50_red_a_metacharacter_in_the_path_never_redirects_the_writer(self):
        """codex-CLI r8 P1: the WRITABLE URI addresses the requested file.

        THE RED: pre-fix `open_verified('<dir>/a#b.sqlite')` succeeded, created NOTHING
        at that path, and wrote this store's schema into the decoy `<dir>/a` — a foreign
        database adopted with `STATE_STORE_FOREIGN_DATABASE` never raised, because the
        check and the connection were looking at two different files.
        """
        decoy = self._foreign_database("a")
        before = self._digest(decoy)
        requested = os.path.join(self.directory, "a#b.sqlite")
        store = store_mod.SingleWriterStateStore.open_verified(
            requested, **self._identity())
        self.addCleanup(store.close)
        self.assertTrue(os.path.isfile(requested))
        self.assertEqual(before, self._digest(decoy))
        self.assertEqual(os.path.normcase(os.path.abspath(requested)),
                         os.path.normcase(self._addressed_by(store._connection)))
        self.assertEqual([], store._connection.execute(
            "SELECT name FROM sqlite_master WHERE name='somebody_elses_table'"
        ).fetchall())
        # The encoding is the documented one (sqlite.org/uri.html §3.1 step 2).
        self.assertEqual(
            "file:" + os.path.abspath(requested).replace("\\", "/").replace(
                "#", "%23"),
            store._target)

    def test_ba50_red_a_literal_percent_escape_in_the_name_is_not_decoded(self):
        """The `%` member of the set: `a%23b.sqlite` is a FILE NAME, not an escape.

        THE RED: pre-fix the requested `a%23b.sqlite` opened the decoy `a#b.sqlite`,
        because sqlite decodes `%HH` in a URI path (sqlite.org/uri.html §3, "Zero or
        more escape sequences of the form %HH ... can occur in the path"). This is why
        `%` -> `%25` has to run BEFORE `#` -> `%23`, not after.
        """
        decoy = self._foreign_database("a#b.sqlite")
        before = self._digest(decoy)
        requested = os.path.join(self.directory, "a%23b.sqlite")
        store = store_mod.SingleWriterStateStore.open_verified(
            requested, **self._identity())
        self.addCleanup(store.close)
        self.assertTrue(os.path.isfile(requested))
        self.assertEqual(before, self._digest(decoy))
        self.assertEqual(os.path.normcase(os.path.abspath(requested)),
                         os.path.normcase(self._addressed_by(store._connection)))
        self.assertIn("%2523b.sqlite", store._target)

    def test_ba50_red_the_readonly_door_stays_on_the_requested_file_and_stays_readonly(self):
        """The read-only URI: same redirection, plus a `?mode=ro` swallowed by a fragment.

        THE RED: pre-fix `readonly_connection_uri('<dir>/a#b.sqlite')` produced
        `file:.../a#b.sqlite?mode=ro`, in which everything after `#` is a FRAGMENT — so
        the connection opened `<dir>/a` AND was writable, and
        `pre_existing_identity_signals()` (the "non-writing door") reported the decoy's
        tables as if they were the requested file's.
        """
        decoy = self._foreign_database("a")
        requested = os.path.join(self.directory, "a#b.sqlite")
        seeded = store_mod.SingleWriterStateStore.open_verified(
            os.path.join(self.directory, "seed.sqlite"), **self._identity())
        seeded.close()
        store_mod._OPEN_WRITERS.clear()
        store_mod._STORES_BY_IDENTITY.clear()
        with open(os.path.join(self.directory, "seed.sqlite"), "rb") as source:
            with open(requested, "wb") as destination:
                destination.write(source.read())

        self.assertEqual(
            "file:" + os.path.abspath(requested).replace("\\", "/").replace("#", "%23")
            + "?mode=ro",
            store_mod.readonly_connection_uri(requested))
        connection = store_mod.open_readonly_connection(requested)
        self.addCleanup(connection.close)
        self.assertEqual(os.path.normcase(os.path.abspath(requested)),
                         os.path.normcase(self._addressed_by(connection)))
        # It is genuinely read-only: the `?mode=ro` reached sqlite as a QUERY.
        connection.execute("PRAGMA query_only=OFF")
        with self.assertRaises(sqlite3.OperationalError):
            connection.execute("CREATE TABLE mbcx01_probe_write (x)")
        # And the identity signals are the REQUESTED file's, which is the whole point:
        # `refuse_foreign_database` now inspects the file the writer will address.
        objects, application_id, _ = store_mod.pre_existing_identity_signals(requested)
        self.assertNotIn("somebody_elses_table", objects)
        self.assertEqual(store_mod.STORE_APPLICATION_ID, application_id)
        self.assertTrue(os.path.isfile(decoy))

    def test_ba50_guard_ordinary_paths_and_in_memory_targets_are_untouched(self):
        """GUARD — an encoder that changed a URI with nothing to encode would be a new
        defect, not a fix. A path with no `%`, `#` or `?` produces the SAME string it
        produced before this fold, and the in-memory routing key still resolves to its
        shared-cache URI.

        ⚠ Reported honestly: this reaches symbols the PRE-FIX bytes do not have
        (`MEMORY_DATABASE_NAME_FORMAT`, `_percent_encode_uri_path`), so pre-fix it errors
        as NEW CAPABILITY rather than failing as a fold red. The behaviour it guards —
        the URI a metacharacter-free path produces — is asserted against the literal
        pre-fold string, which is what makes it a guard and not a restatement."""
        plain = os.path.join(self.directory, "plain.sqlite")
        store = store_mod.SingleWriterStateStore.open_verified(
            plain, **self._identity())
        self.addCleanup(store.close)
        self.assertEqual("file:" + os.path.abspath(plain).replace("\\", "/"),
                         store._target)
        self.assertEqual(store._target + "?mode=ro",
                         store_mod.readonly_connection_uri(plain))
        memory = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, **self._identity("STORE.MBCX01.BUILD.STATE.URIMEM"))
        self.addCleanup(memory.close)
        self.assertTrue(store_mod.readonly_connection_uri(memory.path).endswith(
            "?mode=memory&cache=shared"))
        self.assertTrue(store_mod.readonly_connection_uri(memory.path).startswith(
            "file:" + store_mod.MEMORY_DATABASE_NAME_FORMAT.split("%")[0]))
        # The encoder is a no-op on every character that is not URI syntax, including
        # the spaces and drive letter an ordinary Windows path carries.
        self.assertEqual(r"C:/Program Files/x/db.sqlite",
                         store_mod._percent_encode_uri_path(
                             r"C:/Program Files/x/db.sqlite"))
        self.assertEqual("a%25b%23c%3fd",
                         store_mod._percent_encode_uri_path("a%b#c?d"))


class BuildAStoreIdentityBeforeWriteWitnesses(unittest.TestCase):
    """ba52: a path holding ANOTHER MBCX STORE is refused with that store UNTOUCHED.

    codex-CLI r9 F1. `refuse_foreign_database` (BA-19/r4 FOLD-2A) settled the case one
    application over: a database belonging to somebody ELSE is inspected through a
    non-writing connection and refused before this store's first PRAGMA. The case one
    STORE over was still decided after the fact. `open_verified` set
    `PRAGMA journal_mode=WAL` — a PERSISTENT header property — and executed the whole of
    `_SCHEMA` before it ever read the persisted `meta` header, so
    `STATE_STORE_IDENTITY_MISMATCH` was raised over a file this open had already
    rewritten. The operator mistake it costs is the ordinary one: a stale or mistyped
    store path in a configuration, which is exactly the mistake FOLD-2A was written for.

    And the same ordering ADOPTED a headerless database of this application: with rows
    present but `meta` empty, the `if not header:` arm stamped THIS caller's identity
    into somebody else's store and returned it as a live store — the tell destroyed by
    the adoption, one application-id short of the defect FOLD-2A closed.

    Measured RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_state_store.py`,
    sha256 9b353df56bb0580321ceb60f2f68e2f0e597d0e4c2bf7672f3621f7714df4414 — the
    worktree checkout hashed the same before the fold, byte for byte). The runner prints
    the bound module's `__file__` and sha256 and this class ASSERTS which copy won,
    because a red harness that silently binds the post-fix copy reports PASS and FAIL
    exactly like a real one.

    ⛔ Nothing here signs, mints or verifies a receipt, and every database it opens lives
    in a temporary directory it removes.
    """

    maxDiff = None

    #: The identity the WITNESS asks for. Every store built below is somebody else's.
    ASKED = {"store_id": "STORE.MBCX01.BUILD.STATE.ASKED",
             "namespace": IDENTITY_CONFIG["namespace"],
             "namespace_version": IDENTITY_CONFIG["namespace_version"]}
    OTHER_STORE_ID = "STORE.MBCX01.BUILD.STATE.OTHER"

    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix="mbcx01-store-identity-")
        self.addCleanup(shutil.rmtree, self.directory, True)
        self.addCleanup(store_mod._OPEN_WRITERS.clear)
        self.addCleanup(store_mod._STORES_BY_IDENTITY.clear)

    def _digest(self, path):
        with open(path, "rb") as stream:
            return hashlib.sha256(stream.read()).hexdigest()

    def _sidecars(self):
        return sorted(os.listdir(self.directory))

    def _another_store(self, name, *, header, user_version=None, rows=True):
        """A database that is ANOTHER MBCX STORE: this application, not this identity.

        Written with plain `sqlite3` and therefore in the DEFAULT (`delete`) journal
        mode, which is what makes the pre-fix mutation visible in the file's own bytes:
        `PRAGMA journal_mode=WAL` writes bytes 18 and 19 of the sqlite header.
        """
        path = os.path.join(self.directory, name)
        connection = sqlite3.connect(path, isolation_level=None)
        try:
            connection.execute("PRAGMA application_id=%d"
                               % store_mod.STORE_APPLICATION_ID)
            connection.execute("PRAGMA user_version=%d"
                               % (store_mod.STORE_SCHEMA_VERSION
                                  if user_version is None else user_version))
            for statement in store_mod._SCHEMA:
                connection.execute(statement)
            if header:
                connection.executemany(
                    "INSERT INTO meta (key, value) VALUES (?, ?)",
                    sorted(header.items()))
            if rows:
                connection.execute(
                    "INSERT INTO journal (transaction_commit_id, seq, status,"
                    " prestate_utf8, prestate_hash, anti_replay_utf8, anti_replay_hash)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("TXN.THE.OTHER.STORES.TRANSACTION", 1,
                     store_mod.TRANSACTION_COMMITTED, "{}", "", "{}", ""))
        finally:
            connection.close()
        return path

    def test_ba52_harness_the_bound_module_is_the_one_this_witness_names(self):
        """The harness proves itself before it proves anything about the store."""
        source = inspect.getsourcefile(store_mod)
        with open(source, "rb") as stream:
            digest = hashlib.sha256(stream.read()).hexdigest()
        print("\nba52 bound module: %s sha256=%s" % (source, digest))
        self.assertTrue(hasattr(store_mod, "refuse_mismatched_pre_existing_store"),
                        "the POST-FIX copy of mbcx01_build_state_store did not win; "
                        "the bound module is %s (sha256 %s)" % (source, digest))

    def test_ba52_red_another_stores_bytes_are_identical_after_the_refusal(self):
        """THE RED: pre-fix the refused open had already rewritten the other store.

        Pre-fix `open_verified` on a path holding another MBCX store raised
        `STATE_STORE_IDENTITY_MISMATCH` — after `PRAGMA journal_mode=WAL` had persisted
        a new journal mode into that store's header and `_SCHEMA` had run over it. The
        refusal was right and the file was already changed:

            AssertionError: '5cf2...' != 'a0c1...'
            the refused open rewrote <dir>/another-store.sqlite3

        Post-fix the comparison is settled through the read-only door and the bytes are
        the bytes.
        """
        path = self._another_store("another-store.sqlite3", header={
            "store_id": self.OTHER_STORE_ID,
            "namespace": IDENTITY_CONFIG["namespace"],
            "namespace_version": str(IDENTITY_CONFIG["namespace_version"]),
            "schema_version": str(store_mod.STORE_SCHEMA_VERSION)})
        before, listing = self._digest(path), self._sidecars()

        with self.assertRaises(store_mod.StateStoreError) as refusal:
            store_mod.SingleWriterStateStore.open_verified(path, **self.ASKED)
        self.assertEqual("STATE_STORE_IDENTITY_MISMATCH", str(refusal.exception))
        self.assertEqual(before, self._digest(path),
                         "the refused open rewrote %s" % path)
        self.assertEqual(listing, self._sidecars())
        # The other store's own rows are still its own, and its identity is intact.
        self.assertEqual({"store_id": self.OTHER_STORE_ID,
                          "namespace": IDENTITY_CONFIG["namespace"],
                          "namespace_version": str(
                              IDENTITY_CONFIG["namespace_version"]),
                          "schema_version": str(store_mod.STORE_SCHEMA_VERSION)},
                         store_mod.pre_existing_store_header(path))
        # Nothing was registered: a refused open leaves no live writer and no identity.
        self.assertEqual({}, store_mod._OPEN_WRITERS)
        self.assertEqual({}, store_mod._STORES_BY_IDENTITY)

    def test_ba52_red_a_headerless_database_of_this_application_is_never_adopted(self):
        """THE RED: pre-fix the open SUCCEEDED and took another store's rows with it.

        A database carrying this application's `application_id`, this schema's
        `user_version` and this store's tables, but an EMPTY `meta`, hit the
        `if not header:` arm: this caller's identity was stamped in, the store was
        returned live, and its FIRST answer was another store's committed transaction.

            AssertionError: StateStoreError not raised
            (and, once the adopted store was queried:
             journal_rows('TXN.THE.OTHER.STORES.TRANSACTION') -> [{'status':
             'COMMITTED', ...}])
        """
        path = self._another_store("headerless.sqlite3", header={})
        before, listing = self._digest(path), self._sidecars()

        with self.assertRaises(store_mod.StateStoreError) as refusal:
            store_mod.SingleWriterStateStore.open_verified(path, **self.ASKED)
        self.assertEqual("STATE_STORE_IDENTITY_MISMATCH", str(refusal.exception))
        self.assertEqual(before, self._digest(path),
                         "the refused open rewrote %s" % path)
        self.assertEqual(listing, self._sidecars())
        self.assertEqual({}, store_mod.pre_existing_store_header(path))
        self.assertEqual({}, store_mod._STORES_BY_IDENTITY)

    def test_ba52_red_an_older_schema_version_is_refused_before_it_is_migrated(self):
        """THE RED: a store at another schema version was rewritten, then refused.

        The version check lived after the DDL too, so a store file written by an
        earlier schema had this schema's `CREATE TABLE IF NOT EXISTS` statements and a
        persistent journal-mode change applied to it before anybody compared versions.
        A store at a version this build does not own is refused BY VERSION, and it is
        refused with its bytes intact — nothing here migrates anything.
        """
        path = self._another_store("older-schema.sqlite3", user_version=1, header={
            "store_id": self.ASKED["store_id"],
            "namespace": self.ASKED["namespace"],
            "namespace_version": str(self.ASKED["namespace_version"]),
            "schema_version": "1"})
        before, listing = self._digest(path), self._sidecars()

        with self.assertRaises(store_mod.StateStoreError) as refusal:
            store_mod.SingleWriterStateStore.open_verified(path, **self.ASKED)
        self.assertEqual(before, self._digest(path),
                         "the refused open rewrote %s" % path)
        self.assertEqual(listing, self._sidecars())
        self.assertEqual("STATE_STORE_SCHEMA_VERSION_MISMATCH", str(refusal.exception))

    def test_ba52_guard_right_paths_are_still_opened_and_still_reopened(self):
        """GUARD — refusing RIGHT paths is not a repair.

        Four shapes that must be untouched by the new preflight, each one a shape the
        store already accepted: a path with no file, a zero-length file, a fresh store
        that gets stamped, and that same store REOPENED under its own identity (which
        is the reopen an operator does every run and the one arm a header comparison
        run too early would have broken).
        """
        fresh = os.path.join(self.directory, "fresh.sqlite3")
        store = store_mod.SingleWriterStateStore.open_verified(fresh, **self.ASKED)
        self.assertEqual(store_mod.STORE_JOURNAL_MODE, store.journal_mode)
        store.close()

        reopened = store_mod.SingleWriterStateStore.open_verified(fresh, **self.ASKED)
        self.addCleanup(reopened.close)
        self.assertEqual(store_mod.expected_store_header(**self.ASKED),
                         store_mod.pre_existing_store_header(fresh))
        self.assertEqual([], reopened.journal_rows())
        reopened.close()

        empty = os.path.join(self.directory, "zero-length.sqlite3")
        with open(empty, "wb"):
            pass
        self.assertEqual(0, os.path.getsize(empty))
        stamped = store_mod.SingleWriterStateStore.open_verified(empty, **self.ASKED)
        self.addCleanup(stamped.close)
        self.assertEqual(store_mod.expected_store_header(**self.ASKED),
                         {row["key"]: row["value"] for row
                          in stamped._connection.execute("SELECT key, value FROM meta")})
        stamped.close()

        # An in-memory target has nothing pre-existing to inspect and is unaffected.
        memory = store_mod.SingleWriterStateStore.open_verified(
            store_mod.MEMORY_PATH, **self.ASKED)
        self.addCleanup(memory.close)
        self.assertTrue(memory.path.startswith(store_mod.MEMORY_PATH + "#"))
        memory.close()

        # A FOREIGN database is still the foreign-database refusal, by its own name:
        # the new preflight sits beside `refuse_foreign_database`, it does not replace
        # it, and the two answers stay distinguishable.
        foreign = os.path.join(self.directory, "foreign.sqlite3")
        connection = sqlite3.connect(foreign, isolation_level=None)
        connection.execute("PRAGMA application_id=305419896")
        connection.execute("CREATE TABLE somebody_elses_table (x)")
        connection.close()
        before = self._digest(foreign)
        with self.assertRaises(store_mod.StateStoreError) as refusal:
            store_mod.SingleWriterStateStore.open_verified(foreign, **self.ASKED)
        self.assertEqual("STATE_STORE_FOREIGN_DATABASE", str(refusal.exception))
        self.assertEqual(before, self._digest(foreign))


if __name__ == "__main__":
    unittest.main()
