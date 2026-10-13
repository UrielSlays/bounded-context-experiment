"""RED-WITNESS PROBE — COMMITTED FIXTURE KEY MATERIAL relabelled as a production root.

This script is EVIDENCE, not an authority. It is written against the PRE-FIX public API
only, so the identical file runs unchanged against a byte-exact reconstruction of the
pre-fix bytes and against the post-fix tree — which is what makes the RED and the GREEN
comparable line for line.

What it exercises (an OPERATOR FOOTGUN, not an attack)
------------------------------------------------------
The custody ceremony (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0) is exactly the
moment a human hand-writes an `OwnerTrustAnchorV1` document, and the obvious way to write
one is to copy the committed example — `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json` —
and edit the fields that look like labels. Before this fold the ONLY thing standing
between that copy and a production root of trust was the `fixture_only` FLAG IN THE
DOCUMENT: flip it to `false`, give the anchor a new `anchor_id`, and
`new_production_verifier_context()` built a PRODUCTION context around a public key whose
PRIVATE half is committed at `mbcx01_build_ceremony_fixture.py:39` and is therefore
public to anyone holding this repository.

MBCX-01 has NO threat model and no untrusted caller (`MBCX-01-BUILD-ADVERSARY-PREMISE-
CORRECTION-2026-08-14.md`), so this is not an attacker path and nothing here is written
as one. It is a SELF-DECEPTION guard: an operator who believes they hold the only copy of
the root key would in fact hold a key everyone holds, and no log line would say so. The
prior art is MITRE CWE-1291 "Public Key Re-Use for Signing both Debug and Production
Code" (PeerOf CWE-321), whose mitigation phase is IMPLEMENTATION: "use different keys for
Production and Debug". We satisfy it at context construction, which is where the fix lands.

Probes
------
  P1  the committed fixture anchor document, relabelled by hand (`fixture_only` flipped,
      new `anchor_id`, public key untouched), handed to
      `new_production_verifier_context`. Expected AFTER the fix: a NAMED refusal.
  P2  the same relabelled document delivered the way an operator delivers a real one —
      an OS configuration path in `MBCX01_BUILD_OWNER_TRUST_ANCHOR`, read by
      `resolve_production_verifier_context` in a verifier nobody wired in code.
      Expected AFTER the fix: the same named refusal, at the same seam.
  C3  CONTROL (must stay green in both runs): the production-shaped TEST anchor whose
      Ed25519 pair is generated IN MEMORY per run builds a context, resolves, and admits
      the simulated production grid.
  C4  CONTROL (must stay green in both runs): the FIXTURE LANE — structural parsing of
      the committed fixture measurement manifest, and `require_production=False`
      verification of a BUILD A receipt — is untouched, because refusing fixture KEY
      MATERIAL at the production root is not refusing fixture DOCUMENTS.

NO experiment, provider call, network call, physical collection or signing ceremony
happens here. Every key is a labelled FIXTURE / TEST key, no key is generated to disk,
and nothing is written to the repository.
"""

from __future__ import annotations

import copy
import json
import os
import tempfile
from typing import Any

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_measurement_authority as measurement_authority
import mbcx01_build_state_authority as state_authority
import mbcx01_build_trust_anchor as trust_anchor

import mbcx01_build_fixtureiso_probe as iso
import test_mbcx01_build_measurement as bw
import test_mbcx01_build_state as ba

RELABELLED_ANCHOR_ID = "MBCX01.RELABELLED.ANCHOR.1"


def relabelled_document() -> dict[str, Any]:
    """The committed fixture anchor document with its two LABELS edited, key untouched."""
    document = copy.deepcopy(ceremony.fixture_owner_anchor_document())
    document["fixture_only"] = False
    document["anchor_id"] = RELABELLED_ANCHOR_ID
    document["custody_note"] = (
        "Hand-written for the production ceremony by copying the committed example "
        "document and editing the fields that look like labels.")
    return document


def committed_public_key() -> str:
    return ceremony.fixture_owner_anchor_document()["public_key_pem"]


def report_context(context: Any) -> None:
    print("  context BUILT from relabelled doc : %s" % (context is not None,))
    if context is None:
        return
    print("  its public key == COMMITTED fixture public key : %s"
          % (context.anchor.public_key_pem == committed_public_key(),))
    print("  anchor_id: %s | fixture_only: %s"
          % (context.anchor.anchor_id, context.anchor.fixture_only))


# ---- P1: relabelled document -> production verifier context -------------------------


def probe_p1() -> None:
    print("== P1: the committed fixture anchor document, RELABELLED by hand ==")
    document = relabelled_document()
    print("  edits: fixture_only true->false, anchor_id -> %r; public_key_pem UNCHANGED"
          % (RELABELLED_ANCHOR_ID,))
    print("  (the private half of that public key is committed at "
          "mbcx01_build_ceremony_fixture.py:39)")
    try:
        context = trust_anchor.new_production_verifier_context(document)
    except Exception as exc:  # noqa: BLE001 - the probe reports whatever it gets
        print("  new_production_verifier_context -> %s: %s" % (type(exc).__name__, exc))
        report_context(None)
        return
    report_context(context)


# ---- P2: the same document delivered through OS configuration -----------------------


def probe_p2() -> None:
    print("== P2: the same relabelled document delivered as OS configuration ==")
    directory = tempfile.mkdtemp(prefix="mbcx01-build-fixturekey-")
    path = os.path.join(directory, "owner-trust-anchor.json")
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(relabelled_document(), stream)
    saved_env = os.environ.get(trust_anchor.ANCHOR_PATH_ENV)
    trust_anchor.clear_owner_trust_anchor()
    os.environ[trust_anchor.ANCHOR_PATH_ENV] = path
    print("  %s=<tmp>/owner-trust-anchor.json (no in-code wiring at all)"
          % (trust_anchor.ANCHOR_PATH_ENV,))
    try:
        context, refusal = trust_anchor.resolve_production_verifier_context(
            trust_anchor.AUTHORITY_MEASUREMENT)
        print("  resolve_production_verifier_context -> refusal=%r" % (refusal,))
        report_context(context)
    except Exception as exc:  # noqa: BLE001
        print("  resolve_production_verifier_context -> %s: %s"
              % (type(exc).__name__, exc))
        report_context(None)
    finally:
        if saved_env is None:
            os.environ.pop(trust_anchor.ANCHOR_PATH_ENV, None)
        else:
            os.environ[trust_anchor.ANCHOR_PATH_ENV] = saved_env


# ---- C3: the legitimate positive path (in-memory TEST PRODUCTION key) ---------------


def control_c3() -> None:
    print("== C3 CONTROL: the in-memory TEST PRODUCTION anchor (key generated per run) ==")
    document = ceremony.test_production_anchor_document()
    print("  anchor_id: %s | fixture_only: %s" % (document["anchor_id"],
                                                  document["fixture_only"]))
    print("  its public key == COMMITTED fixture public key : %s"
          % (document["public_key_pem"] == committed_public_key(),))
    context = trust_anchor.new_production_verifier_context(
        document, current_time=ceremony.TEST_VERIFIER_INSTANT)
    print("  context BUILT: %s | current_instant=%s"
          % (context is not None, context.current_instant()))
    ceremony.configure_test_production_anchor()
    resolved, refusal = trust_anchor.resolve_production_verifier_context(
        trust_anchor.AUTHORITY_MEASUREMENT)
    print("  resolve_production_verifier_context -> anchor_id=%r refusal=%r"
          % (getattr(getattr(resolved, "anchor", None), "anchor_id", None), refusal))
    manifest = bw.simulated_production_manifest()
    custody = bw.simulated_custody_evidence(manifest)
    print("  measurement door (legitimate operator-anchored grid) ->",
          bw.admit(bw.simulated_production_grid(), manifest=manifest, custody=custody))


# ---- C4: the fixture LANE is untouched ----------------------------------------------


def control_c4() -> None:
    print("== C4 CONTROL: the FIXTURE LANE (documents, not authority) ==")
    committed = bw.committed_fixture_manifest()
    roots = measurement_authority.validate_production_trust_root_manifest(committed)
    print("  committed fixture measurement manifest parses: roots=%d fixture_only=%s"
          % (len(roots), sorted({row["fixture_only"] for row in roots.values()})))
    document = ceremony.fixture_owner_anchor_document()
    print("  committed anchor document still loads: anchor_id=%r fixture_only=%r"
          % (document["anchor_id"], document["fixture_only"]))
    state_manifest = ba._production_state_manifest()
    state_custody = ba._state_custody_evidence(
        state_manifest, anchor_id=document["anchor_id"],
        private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
    _expected, _scorer_input, graph = iso.packet_graph()
    precommit, proposal, child, postcommit = graph
    store = iso.committed_state_store(graph)
    try:
        receipt = ba._v2_receipt(
            precommit, proposal, child, postcommit,
            identity={"trust_root_id": state_manifest["manifest_id"],
                      "trust_policy_digest": state_manifest["trust_policy_digest"]})
        print("  state FIXTURE lane (require_production=False) ->",
              state_authority.verify_state_authority_receipt_v2(
                  receipt, trust_root_manifest=state_manifest,
                  custody_evidence=state_custody, require_production=False))
    finally:
        store.close()


def main() -> int:
    print("MBCX-01 BUILD — COMMITTED-FIXTURE-KEY probe (operator footgun, MITRE CWE-1291)")
    print("cwd: %s" % os.getcwd())
    document = ceremony.fixture_owner_anchor_document()
    print("committed fixture anchor: anchor_id=%r fixture_only=%r"
          % (document["anchor_id"], document["fixture_only"]))
    print()
    probe_p1()
    print()
    probe_p2()
    print()
    control_c3()
    print()
    control_c4()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
