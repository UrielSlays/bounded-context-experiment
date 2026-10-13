"""TEST-ONLY owner-ceremony evidence for the BUILD witness suites.

⚠ THIS MODULE HOLDS A COMMITTED TEST PRIVATE KEY, GENERATES A SECOND TEST KEY PAIR IN
MEMORY, AND IS NEVER IMPORTED BY ANY PRODUCTION AUTHORITY MODULE. It exists so the state suite, the measurement suite and
the connected integration fixture build the SAME owner-signed activation evidence from
ONE definition (the same reasoning `mbcx01_build_integration` gives for importing the
witnesses' fixtures: a second copy of simulated evidence is free to drift from the copy
the witnesses check).

What it simulates: `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 5 — "OWNER reviews
all three, runs the BUILD verifier against the manifest + evidence (fixture-mode dry
run), and signs evidence document 4" — for a manifest whose roots are FIXTURE-ONLY test
keys over SIMULATED evidence. Nothing here activates anything: no production key is
generated, no ceremony is performed, and no manifest or key is written to the repository.

TWO owner anchors live here, and the difference is the r2 fix class
--------------------------------------------------------------------
  * the COMMITTED FIXTURE anchor (`MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json`,
    `fixture_only:true`), whose private half is the committed test key below. After the
    r2 FIXTURE-ISOLATION fold it grants NOTHING: `test_bw22` and `test_ba34` are the
    witnesses that all three production doors refuse it by name. It stays here because
    proving the refusal requires being able to present it.
  * the TEST PRODUCTION anchor (`fixture_only:false`), whose key pair is generated IN
    MEMORY at first use and never written to this repository. It is what the witness
    suites wire as the operator context so the LEGITIMATE path still has a real green.
    Its public key changes every run, which is itself a small guarantee that no witness
    can be quietly depending on committed key material.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
from typing import Any

import mbcx01_r13_common as common

import mbcx01_build_trust_anchor as trust_anchor

ROOT = os.path.dirname(os.path.abspath(__file__))

#: The committed FIXTURE anchor document (public key only).
FIXTURE_ANCHOR_PATH = os.path.join(ROOT, "MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json")

#: FIXTURE-ONLY owner root private key. Committed on purpose, exactly like the other
#: BUILD test keys: it proves the anchored-activation seam end to end without any
#: production custody. The PRODUCTION owner root is generated inside the custody
#: backend during the ceremony and never appears in this repository.
FIXTURE_OWNER_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIIEEtMNnHpGGlnuucqMhvbKtqrqmxWFMGJGTw5Yi6BD8\n"
    "-----END PRIVATE KEY-----\n")

#: A second FIXTURE-ONLY key that is NOT the anchor: witnesses use it to present an
#: activation statement signed by "some key", which must not authenticate.
FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIGNlwRx6sGj8aKnq2NOgOY19piKa7a6CmKOSnGq9jmki\n"
    "-----END PRIVATE KEY-----\n")

FIXTURE_ACTIVATION_GENERATION = 1

#: The TEST PRODUCTION anchor id and the fixed instant the witness suites verify at.
#: After the r2 FIXTURE-ISOLATION fold a `fixture_only` anchor cannot grant production
#: authority at any door, so the POSITIVE lane needs a production-SHAPED anchor. Its key
#: pair is generated IN MEMORY at first use and is never written to this repository:
#: the committed anchor document stays fixture-only and key-free, and
#: `verify-build-bundle.py check_no_production_activation` keeps proving it.
TEST_PRODUCTION_ANCHOR_ID = "MBCX01.BUILD.OWNER.ANCHOR.TEST.PRODUCTION.1"
TEST_VERIFIER_INSTANT = "2026-08-14T12:00:00Z"

#: Populated on first use by `_test_production_keypair()`. Process-local, never on disk.
_TEST_PRODUCTION_KEYPAIR: tuple[str, str] | None = None

#: Populated per label on first use by `test_production_signing_keypair()`. Process-local,
#: never on disk. See that function for why the SIGNING keys moved here too.
_TEST_PRODUCTION_SIGNING_KEYPAIRS: dict[str, tuple[str, str]] = {}


def fixture_owner_anchor_document() -> dict[str, Any]:
    with open(FIXTURE_ANCHOR_PATH, encoding="utf-8") as stream:
        return json.load(stream)


def configure_fixture_owner_anchor() -> trust_anchor.OwnerTrustAnchor:
    """OPERATOR WIRING (fixture): install the committed fixture anchor for this process.

    Retained on purpose: `test_bw22` / `test_ba34` are the witnesses that this anchor,
    correctly signing an activation that binds the exact manifest and custody set, is
    REFUSED by name at all three production doors. Installing it is legal; it just
    grants nothing.
    """
    return trust_anchor.configure_owner_trust_anchor(FIXTURE_ANCHOR_PATH)


def owner_anchor_document(*, anchor_id: str, public_key_pem: str,
                          fixture_only: bool,
                          authorities: list[str] | None = None,
                          minimum_activation_generation: int =
                          FIXTURE_ACTIVATION_GENERATION) -> dict[str, Any]:
    """An `OwnerTrustAnchorV1` document over a caller-supplied PUBLIC key."""
    return {
        "schema_id": trust_anchor.ANCHOR_SCHEMA_ID,
        "anchor_id": anchor_id,
        "fixture_only": fixture_only,
        "algorithm": trust_anchor.SIGNATURE_ALGORITHM,
        "public_key_pem": public_key_pem,
        "authorities": list(authorities or trust_anchor.AUTHORITIES),
        "minimum_activation_generation": minimum_activation_generation,
        "custody_note": (
            "TEST-ONLY owner trust anchor. Its key pair is generated in memory by the "
            "BUILD witness suites and never written to this repository; a PRODUCTION "
            "anchor is generated in the owner ceremony "
            "(MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md section 3) and delivered to the "
            "verifier through operator configuration."),
    }


def _generate_ed25519_keypair() -> tuple[str, str]:
    """A fresh Ed25519 key pair from node, in memory. Nothing is written to disk."""
    source = ("const {generateKeyPairSync}=require('node:crypto');"
              "const {publicKey,privateKey}=generateKeyPairSync('ed25519');"
              "process.stdout.write(JSON.stringify({"
              "priv:privateKey.export({type:'pkcs8',format:'pem'}),"
              "pub:publicKey.export({type:'spki',format:'pem'})}));")
    result = subprocess.run(["node", "-e", source], text=True, capture_output=True,
                            timeout=20, check=True)
    reply = json.loads(result.stdout)
    return reply["priv"], reply["pub"]


def _test_production_keypair() -> tuple[str, str]:
    global _TEST_PRODUCTION_KEYPAIR
    if _TEST_PRODUCTION_KEYPAIR is None:
        _TEST_PRODUCTION_KEYPAIR = _generate_ed25519_keypair()
    return _TEST_PRODUCTION_KEYPAIR


def test_production_signing_keypair(label: str) -> tuple[str, str]:
    """A PRODUCTION-lane TEST SIGNING pair `(private_pem, public_pem)`, in memory only.

    The r2 fold moved the owner ANCHOR of the positive lane in memory because a
    `fixture_only` anchor can no longer grant production authority. The 2026-08-15
    signing-key fold does the same for the SIGNING roots, for the harder reason: a
    council seat made the committed test signing pair the PRODUCTION measurement signing
    root and cleared admission, so a key published in a committed `*.fixture.json`
    document is now refused BY NAME at every production door
    (`mbcx01_build_trust_anchor.committed_fixture_key_material`). A production-shaped
    witness therefore needs signing material that is in NO committed document.

    One pair per `label`, generated at first use and cached for the process, so a suite
    that rebuilds its manifest dozens of times keeps ONE root and one set of signatures.
    Nothing is written to this repository and no ceremony is performed.
    """
    keypair = _TEST_PRODUCTION_SIGNING_KEYPAIRS.get(label)
    if keypair is None:
        keypair = _generate_ed25519_keypair()
        _TEST_PRODUCTION_SIGNING_KEYPAIRS[label] = keypair
    return keypair


def test_production_owner_private_key() -> str:
    """The in-memory TEST PRODUCTION owner private key. NEVER committed."""
    return _test_production_keypair()[0]


def test_production_anchor_document() -> dict[str, Any]:
    """The production-SHAPED (`fixture_only:false`) TEST anchor document."""
    return owner_anchor_document(anchor_id=TEST_PRODUCTION_ANCHOR_ID,
                                 public_key_pem=_test_production_keypair()[1],
                                 fixture_only=False)


def write_test_production_anchor(path: str) -> str:
    """Write the TEST PRODUCTION anchor document (public key only) to `path`.

    For the cold-process witness, which receives its anchor the way an operator gives it
    to a verifying process nobody wired in code: an OS configuration path. The caller
    owns the (temporary) directory; nothing here writes into the repository.
    """
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(test_production_anchor_document(), stream)
    return path


def configure_test_production_anchor(*, current_time: str | None = TEST_VERIFIER_INSTANT
                                     ) -> trust_anchor.OwnerTrustAnchor:
    """OPERATOR WIRING (test): install the TEST PRODUCTION verifier context.

    The instant is pinned by default so the witness suites are deterministic — which is
    the property Go's `VerifyOptions.CurrentTime` exists to give a caller. `test_bw24`
    is the witness that the FALLBACK, when no instant is injected, is the real clock and
    never the manifest's own `published_at`.
    """
    return trust_anchor.configure_owner_trust_anchor(
        test_production_anchor_document(), current_time=current_time)


def node_sign(private_key_pem: str, preimages_b64: list[str]) -> list[str]:
    """Sign fixture preimages with node's Ed25519 (mirrors the frozen r13 test signer)."""
    source = ("const {createPrivateKey,sign}=require('node:crypto');"
              "let d='';process.stdin.setEncoding('utf8');"
              "process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{"
              "const r=JSON.parse(d),k=createPrivateKey(r.k);"
              "process.stdout.write(JSON.stringify(r.ps.map(p=>sign(null,"
              "Buffer.from(p,'base64'),k).toString('base64'))));});")
    result = subprocess.run(["node", "-e", source],
                            input=json.dumps({"k": private_key_pem, "ps": preimages_b64}),
                            text=True, capture_output=True, timeout=20, check=True)
    return json.loads(result.stdout)


def sign_activation(statement: dict[str, Any], *,
                    private_key_pem: str | None = None) -> dict[str, Any]:
    """Attach the owner signature over the EXACT canonical bytes of the signed region."""
    private_key_pem = private_key_pem or test_production_owner_private_key()
    signed = {key: value for key, value in statement.items()
              if key not in trust_anchor.ACTIVATION_UNSIGNED_KEYS}
    preimage_b64 = base64.b64encode(common.canonical_json(signed)).decode("ascii")
    signed["signature_b64"] = node_sign(private_key_pem, [preimage_b64])[0]
    return signed


def activation_statement(*, authority: str, manifest: Any, manifest_validity: Any,
                         signing_key_id: str, editor_key_ids: list[str],
                         custody_evidence_digests: dict[str, str],
                         provenance_digest: str,
                         activation_generation: int = FIXTURE_ACTIVATION_GENERATION,
                         anchor_id: str | None = None,
                         private_key_pem: str | None = None,
                         overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build (and owner-sign) one `OwnerCeremonyActivationV1` statement.

    Defaults to the TEST PRODUCTION anchor and its in-memory key, because that is the
    only shape that can carry a production admission after the r2 fold. A witness that
    wants the COMMITTED FIXTURE anchor — `test_bw22` / `test_ba34`, whose whole point is
    that it must be refused — asks for it by name with `anchor_id=` and
    `private_key_pem=`.

    `overrides` is applied to the SIGNED region before signing, so a witness can present
    a statement that is genuinely owner-signed but binds the wrong thing — which must
    still fail, because authentication is not the same as authorization.
    """
    statement = {
        "schema_id": trust_anchor.ACTIVATION_SCHEMA_ID,
        "anchor_id": anchor_id or TEST_PRODUCTION_ANCHOR_ID,
        "authority": authority,
        "activation_generation": activation_generation,
        "manifest_digest": trust_anchor.manifest_activation_digest(manifest),
        "manifest_validity": manifest_validity,
        "authorized_signing_key_id": signing_key_id,
        "authorized_editor_key_ids": list(editor_key_ids),
        "custody_evidence_digests": dict(custody_evidence_digests),
        "provenance_digest": provenance_digest,
    }
    statement.update(overrides or {})
    return sign_activation(statement, private_key_pem=private_key_pem)
