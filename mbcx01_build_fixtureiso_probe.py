"""RED-WITNESS PROBE — the r2 FIXTURE-ISOLATION class, on whatever bytes it runs against.

This script is EVIDENCE, not an authority. It constructs the six executed attack /
observation shapes the BUILD acceptance r2 round banked (codex-exec seat findings F1, F2,
F3, F4, F6, F7) and prints what the BUILD verifiers in the SAME directory answer. It is
written against the PRE-FIX public API only, so the identical file runs unchanged against
a `git archive HEAD` reconstruction of the pre-fix bytes and against the post-fix tree —
which is what makes the RED and the GREEN comparable line for line.

Probes
------
  P1  F1 — the COMMITTED fixture owner anchor (`fixture_only:true`, private half
      committed at `mbcx01_build_ceremony_fixture.py:39`, therefore public) is configured
      as the process anchor and signs the activation. All three production doors are
      asked. Expected AFTER the fix: a NAMED refusal at every door, while the fixture
      LANE (structural parsing / `require_production=False`) stays green.
  P2  F2 — a `dict` subclass whose `.get`/`__getitem__` reconfigure the process anchor is
      passed as the trust-root manifest, with a reviewer-authored owner anchor, manifest,
      custody set, activation and grid. Expected AFTER the fix: the in-flight decision is
      made against the anchor the OPERATOR wired, so the swap buys nothing.
  P3  F3 — an operator wires its OWN (non-fixture) anchor, then a caller builds and
      releases the integration fixture. Expected AFTER the fix: the operator's anchor is
      still installed afterwards, and a fixture-anchored universe does not admit.
  P4  F4 — a manifest whose validity window closed in 2001, carrying a 2000 revocation
      `published_at`, correctly activated by the operator's own anchor. Expected AFTER the
      fix: refused at the VERIFIER's clock, never admitted at the artifact's own instant.
  P5  F7 — a binding-only exactness evaluation. Expected AFTER the fix: the emitted
      `result` does not read as "the carrier suite executed".
  P6  F6 — an anchor document with a duplicate member. Expected AFTER the fix: refused by
      name at the loader instead of accepted last-member-wins.

NO experiment, provider call, network call, physical collection or signing ceremony
happens here. Every key is a labelled FIXTURE / TEST / attacker key, and the two key
pairs this probe needs beyond the committed fixture material are generated IN MEMORY at
run time and never written to the repository.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import tempfile
from typing import Any

import mbcx01_r13_common as common
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_exactness_authority as exactness
import mbcx01_build_integration as integration
import mbcx01_build_measurement_authority as measurement_authority
import mbcx01_build_state_authority as state_authority
import mbcx01_build_state_store as store_mod
import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_build_windows_producer as producer

import test_mbcx01_build_measurement as bw
import test_mbcx01_build_state as ba

OPERATOR_ANCHOR_ID = "MBCX01.BUILD.OWNER.ANCHOR.PROBE.OPERATOR.1"
ATTACKER_ANCHOR_ID = "ATTACKER.SELF.AUTHORED.OWNER.ANCHOR.1"

EXPIRED_WINDOW = {"not_before": "2000-01-01T00:00:00Z",
                  "not_after": "2001-01-01T00:00:00Z"}
EXPIRED_PUBLISHED_AT = "2000-06-01T00:00:00Z"


def generate_keypair() -> tuple[str, str]:
    """A FRESH Ed25519 key pair, generated in memory. Never written to the repository."""
    source = ("const {generateKeyPairSync}=require('node:crypto');"
              "const {publicKey,privateKey}=generateKeyPairSync('ed25519');"
              "process.stdout.write(JSON.stringify({"
              "priv:privateKey.export({type:'pkcs8',format:'pem'}),"
              "pub:publicKey.export({type:'spki',format:'pem'})}));")
    result = subprocess.run(["node", "-e", source], text=True, capture_output=True,
                            timeout=20, check=True)
    reply = json.loads(result.stdout)
    return reply["priv"], reply["pub"]


def anchor_document(anchor_id: str, public_key_pem: str, *,
                    fixture_only: bool) -> dict[str, Any]:
    return {
        "schema_id": "OwnerTrustAnchorV1",
        "anchor_id": anchor_id,
        "fixture_only": fixture_only,
        "algorithm": "ED25519",
        "public_key_pem": public_key_pem,
        "authorities": [trust_anchor.AUTHORITY_MEASUREMENT, trust_anchor.AUTHORITY_STATE],
        "minimum_activation_generation": 1,
        "custody_note": "PROBE-ONLY anchor, generated in memory for the RED/GREEN run.",
    }


# ---- shared fixture assembly (pre-fix API only) ------------------------------------


def measurement_universe(manifest: dict[str, Any], *, anchor_id: str,
                         private_key_pem: str) -> tuple[dict[str, Any], list[dict]]:
    """The four custody documents + an owner activation signed by the named key."""
    documents = copy.deepcopy(bw.CUSTODY_DOCUMENTS)
    roots = measurement_authority.validate_production_trust_root_manifest(manifest)
    binding = measurement_authority.production_activation_binding(
        manifest, roots, documents)
    documents[measurement_authority.OWNER_ACTIVATION_EVIDENCE] = (
        ceremony.activation_statement(manifest=manifest, anchor_id=anchor_id,
                                      private_key_pem=private_key_pem, **binding))
    return documents, bw.simulated_production_grid()


def packet_graph():
    expected_manifest = packets.packet_fixture_manifest()
    scorer_input = packets.build_scoring_fixture(expected_manifest, "OM")
    transition = scorer_input["transition_authority"]
    return expected_manifest, scorer_input, (
        copy.deepcopy(transition["precommit_state"]),
        copy.deepcopy(transition["proposal_event"]),
        copy.deepcopy(transition["applied_child_event"]),
        copy.deepcopy(transition["postcommit_state"]))


def committed_state_store(graph):
    precommit, proposal, child, _postcommit = graph
    store = store_mod.SingleWriterStateStore.open_verified(
        store_mod.MEMORY_PATH, store_id=ba.IDENTITY_CONFIG["store_id"],
        namespace=ba.IDENTITY_CONFIG["namespace"],
        namespace_version=ba.IDENTITY_CONFIG["namespace_version"])
    store.commit_transition(
        {"transaction_commit_id": ba.TRANSACTION_ID, "prestate": precommit,
         "proposal_event": proposal, "applied_child_event": child},
        anti_replay=ba.ANTI_REPLAY_ANCHORS)
    return store


def state_universe(manifest: dict[str, Any], *, anchor_id: str,
                   private_key_pem: str) -> dict[str, Any]:
    return ba._state_custody_evidence(manifest, anchor_id=anchor_id,
                                      private_key_pem=private_key_pem)


def exactness_suite() -> dict[str, Any]:
    with open(measurement.EXACTNESS_SUITE, encoding="utf-8") as stream:
        return json.load(stream)


def three_doors(manifest, custody, grid, *, label: str) -> None:
    """Ask all three production doors with one universe and print each verdict."""
    print("  measurement door ->", measurement_authority.evaluate_production_measurement(
        grid, trust_root_manifest=manifest, custody_evidence=custody,
        expected_run_id=bw.RUN_ID))
    try:
        receipt = exactness.verify_production_carrier_exactness(
            {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
            suite_document=exactness_suite(), trust_root_manifest=manifest,
            custody_evidence=custody)
        print("  exactness door   -> ADMITTED result=%r authority_mode=%r"
              % (receipt.get("result"), receipt.get("authority_mode")))
    except Exception as exc:  # noqa: BLE001 - the probe reports whatever it gets
        print("  exactness door   -> %s: %s" % (type(exc).__name__, exc))
    print("  (%s)" % label)


def state_doors(manifest, custody, *, label: str) -> None:
    expected_manifest, scorer_input, graph = packet_graph()
    precommit, proposal, child, postcommit = graph
    store = committed_state_store(graph)
    try:
        receipt = ba._v2_receipt(
            precommit, proposal, child, postcommit,
            identity={"trust_root_id": manifest["manifest_id"],
                      "trust_policy_digest": manifest["trust_policy_digest"]})
        print("  state verify door ->", state_authority.verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=manifest, custody_evidence=custody,
            require_production=True))
        print("  state scorer door ->", state_authority.verify_production_scorer_input(
            scorer_input, receipt, expected_manifest=expected_manifest,
            trust_root_manifest=manifest, custody_evidence=custody))
        print("  state FIXTURE lane (require_production=False) ->",
              state_authority.verify_state_authority_receipt_v2(
                  receipt, trust_root_manifest=manifest, custody_evidence=custody,
                  require_production=False))
    finally:
        store.close()
    print("  (%s)" % label)


# ---- P1: the committed FIXTURE anchor grants production authority (codex F1) --------


def probe_p1() -> None:
    print("== P1 (F1): the COMMITTED fixture-only owner anchor, whose private half is "
          "committed ==")
    fixture_document = ceremony.fixture_owner_anchor_document()
    print("  configured anchor: anchor_id=%r fixture_only=%r"
          % (fixture_document["anchor_id"], fixture_document["fixture_only"]))
    ceremony.configure_fixture_owner_anchor()
    manifest = bw.simulated_production_manifest()
    custody, grid = measurement_universe(
        manifest, anchor_id=fixture_document["anchor_id"],
        private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
    three_doors(manifest, custody, grid,
                label="activation signed by the COMMITTED fixture owner private key")
    state_manifest = ba._production_state_manifest()
    state_custody = state_universe(
        state_manifest, anchor_id=fixture_document["anchor_id"],
        private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
    state_doors(state_manifest, state_custody,
                label="same committed fixture owner key, BUILD A")
    # The fixture LANE must stay green either way: structural parsing of the committed
    # fixture manifest is not an activation and never was.
    committed = bw.committed_fixture_manifest()
    roots = measurement_authority.validate_production_trust_root_manifest(committed)
    print("  fixture LANE: committed fixture manifest parses, roots=%d fixture_only=%s"
          % (len(roots), sorted({row["fixture_only"] for row in roots.values()})))


# ---- P2: a mapping object substitutes the process anchor mid-evaluation (codex F2) --


def probe_p2(operator_anchor: dict[str, Any]) -> None:
    print("== P2 (F2): a caller-supplied mapping object reconfigures the anchor from "
          "inside .get/__getitem__ ==")
    attacker_private, attacker_public = generate_keypair()
    attacker_anchor = anchor_document(ATTACKER_ANCHOR_ID, attacker_public,
                                      fixture_only=False)

    class AnchorInjectingDict(dict):
        """codex F2's gadget: authority state mutated by reading the request data."""

        swaps = 0

        def _swap(self):
            type(self).swaps += 1
            trust_anchor.configure_owner_trust_anchor(copy.deepcopy(attacker_anchor))

        def get(self, key, default=None):
            self._swap()
            return super().get(key, default)

        def __getitem__(self, key):
            self._swap()
            return super().__getitem__(key)

    documents = bw.attacker_custody_documents()
    manifest = bw.attacker_manifest(documents)
    roots = measurement_authority.validate_production_trust_root_manifest(manifest)
    binding = measurement_authority.production_activation_binding(
        manifest, roots, documents)
    documents[measurement_authority.OWNER_ACTIVATION_EVIDENCE] = (
        ceremony.activation_statement(manifest=manifest, anchor_id=ATTACKER_ANCHOR_ID,
                                      private_key_pem=attacker_private, **binding))
    grid = bw.simulated_production_grid(
        signer=producer.FixtureSigner(bw.ATTACKER_KEY_ID, bw.ATTACKER_PRIVATE_KEY_PEM),
        identity=bw.simulated_identity(
            signing_key_id=bw.ATTACKER_KEY_ID,
            trust_policy_digest=manifest["roots"][0]["trust_policy_digest"]))

    for door in ("measurement", "exactness"):
        trust_anchor.configure_owner_trust_anchor(copy.deepcopy(operator_anchor))
        before = trust_anchor.resolve_owner_trust_anchor(
            trust_anchor.AUTHORITY_MEASUREMENT)
        AnchorInjectingDict.swaps = 0
        armed = AnchorInjectingDict(copy.deepcopy(manifest))
        if door == "measurement":
            verdict = measurement_authority.evaluate_production_measurement(
                grid, trust_root_manifest=armed, custody_evidence=documents,
                expected_run_id=bw.RUN_ID)
            printed = repr(verdict)
        else:
            try:
                receipt = exactness.verify_production_carrier_exactness(
                    {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
                    suite_document=exactness_suite(), trust_root_manifest=armed,
                    custody_evidence=documents)
                printed = "ADMITTED result=%r" % (receipt.get("result"),)
            except Exception as exc:  # noqa: BLE001
                printed = "%s: %s" % (type(exc).__name__, exc)
        after = trust_anchor.resolve_owner_trust_anchor(
            trust_anchor.AUTHORITY_MEASUREMENT)
        print("  %s door -> %s" % (door, printed))
        print("     anchor before=%s after=%s swaps_fired=%d"
              % (getattr(before, "anchor_id", None), getattr(after, "anchor_id", None),
                 AnchorInjectingDict.swaps))

    # BUILD A, same gadget.
    trust_anchor.configure_owner_trust_anchor(copy.deepcopy(operator_anchor))
    state_manifest = ba._production_state_manifest()
    state_custody = state_universe(state_manifest, anchor_id=ATTACKER_ANCHOR_ID,
                                   private_key_pem=attacker_private)
    AnchorInjectingDict.swaps = 0
    armed_state = AnchorInjectingDict(copy.deepcopy(state_manifest))
    expected_manifest, scorer_input, graph = packet_graph()
    precommit, proposal, child, postcommit = graph
    store = committed_state_store(graph)
    try:
        receipt = ba._v2_receipt(
            precommit, proposal, child, postcommit,
            identity={"trust_root_id": state_manifest["manifest_id"],
                      "trust_policy_digest": state_manifest["trust_policy_digest"]})
        print("  state verify door ->", state_authority.verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=armed_state, custody_evidence=state_custody,
            require_production=True))
    finally:
        store.close()
    print("     anchor after=%s swaps_fired=%d"
          % (getattr(trust_anchor.resolve_owner_trust_anchor(
              trust_anchor.AUTHORITY_STATE), "anchor_id", None),
             AnchorInjectingDict.swaps))


# ---- P3: the integration fixture leaves the fixture anchor installed (codex F3) -----


def probe_p3(operator_anchor: dict[str, Any]) -> None:
    print("== P3 (F3): the integration fixture is built and RELEASED by a caller ==")
    trust_anchor.configure_owner_trust_anchor(copy.deepcopy(operator_anchor))
    before = trust_anchor.resolve_owner_trust_anchor(trust_anchor.AUTHORITY_MEASUREMENT)
    print("  operator anchor before: anchor_id=%r fixture_only=%r"
          % (before.anchor_id, before.fixture_only))
    graph = integration.build_connected_authority_fixture()
    integration.release_connected_authority_fixture(graph)
    after = trust_anchor.resolve_owner_trust_anchor(trust_anchor.AUTHORITY_MEASUREMENT)
    print("  operator anchor after build+release: anchor_id=%r fixture_only=%r"
          % (getattr(after, "anchor_id", None), getattr(after, "fixture_only", None)))
    # The consequence, executed: the NEXT production evaluation in this process runs
    # under whatever anchor the fixture left behind.
    fixture_document = ceremony.fixture_owner_anchor_document()
    manifest = bw.simulated_production_manifest()
    custody, grid = measurement_universe(
        manifest, anchor_id=fixture_document["anchor_id"],
        private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
    print("  subsequent production evaluation under the fixture-signed universe ->",
          measurement_authority.evaluate_production_measurement(
              grid, trust_root_manifest=manifest, custody_evidence=custody,
              expected_run_id=bw.RUN_ID))


# ---- P4: an expired manifest admits at its own instant (codex F4) -------------------


def probe_p4(operator_anchor: dict[str, Any], operator_private: str) -> None:
    print("== P4 (F4): a manifest whose validity window closed in 2001 ==")
    trust_anchor.configure_owner_trust_anchor(copy.deepcopy(operator_anchor))
    template = bw.simulated_production_manifest()
    revocation = dict(template["revocation"], published_at=EXPIRED_PUBLISHED_AT)
    manifest = bw.simulated_production_manifest(
        root_overrides={"validity": dict(EXPIRED_WINDOW)},
        manifest_overrides={"validity": dict(EXPIRED_WINDOW), "revocation": revocation})
    custody, grid = measurement_universe(manifest, anchor_id=OPERATOR_ANCHOR_ID,
                                         private_key_pem=operator_private)
    print("  manifest validity=%s revocation.published_at=%s"
          % (manifest["validity"], manifest["revocation"]["published_at"]))
    print("  measurement door (verifier default instant) ->",
          measurement_authority.evaluate_production_measurement(
              grid, trust_root_manifest=manifest, custody_evidence=custody,
              expected_run_id=bw.RUN_ID))
    # The same manifest, judged at an instant the VERIFIER supplies to the structural
    # validator, has always been refused — which is what makes the default the defect.
    try:
        measurement_authority.validate_production_trust_root_manifest(
            manifest, evaluation_instant="2026-08-14T00:00:00Z")
        print("  structural validator at 2026-08-14T00:00:00Z -> ADMITTED")
    except measurement_authority.MeasurementAuthorityError as exc:
        print("  structural validator at 2026-08-14T00:00:00Z ->", exc)
    # BUILD A: a state trust root whose window closed before the verifier's clock but
    # still contains the receipt's own attested authority instant.
    state_manifest = ba._production_state_manifest()
    state_manifest["validity"] = {"not_before": "2026-08-12T00:00:00.000000Z",
                                  "not_after": "2026-08-14T00:00:00.000000Z"}
    state_custody = state_universe(state_manifest, anchor_id=OPERATOR_ANCHOR_ID,
                                   private_key_pem=operator_private)
    state_doors(state_manifest, state_custody,
                label="state trust root stale at the verifier's clock, valid at the "
                      "receipt's own knowledge_time")


# ---- P5: binding-only exactness presents as PASS (codex F7) -------------------------


def probe_p5(operator_anchor: dict[str, Any], operator_private: str) -> None:
    print("== P5 (F7): a binding-only exactness evaluation (the suite is NOT executed) ==")
    trust_anchor.configure_owner_trust_anchor(copy.deepcopy(operator_anchor))
    manifest = bw.simulated_production_manifest()
    custody, grid = measurement_universe(manifest, anchor_id=OPERATOR_ANCHOR_ID,
                                         private_key_pem=operator_private)
    receipt = exactness.verify_production_carrier_exactness(
        {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
        suite_document=exactness_suite(), trust_root_manifest=manifest,
        custody_evidence=custody)
    print("  emitted receipt result=%r authority_mode=%r"
          % (receipt.get("result"), receipt.get("authority_mode")))
    try:
        claimed = exactness.verify_production_carrier_exactness(
            {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID, "result": "PASS"},
            envelopes=grid, suite_document=exactness_suite(),
            trust_root_manifest=manifest, custody_evidence=custody)
        print("  a receipt CLAIMING result='PASS' -> ADMITTED result=%r"
              % (claimed.get("result"),))
    except Exception as exc:  # noqa: BLE001
        print("  a receipt CLAIMING result='PASS' -> %s: %s" % (type(exc).__name__, exc))


# ---- P6: duplicate-member anchor document (codex F6) --------------------------------


def probe_p6() -> None:
    print("== P6 (F6): an anchor document with a DUPLICATE member ==")
    document = ceremony.fixture_owner_anchor_document()
    serialized = json.dumps(document)
    ambiguous = serialized[:-1] + ', "fixture_only": false}'
    directory = tempfile.mkdtemp(prefix="mbcx01-build-fixtureiso-")
    path = os.path.join(directory, "ambiguous-owner-anchor.json")
    with open(path, "w", encoding="utf-8") as stream:
        stream.write(ambiguous)
    print("  document carries fixture_only TWICE: true then false")
    try:
        anchor = trust_anchor.load_owner_trust_anchor(path)
        print("  loader -> ACCEPTED anchor_id=%r fixture_only=%r"
              % (anchor.anchor_id, anchor.fixture_only))
    except Exception as exc:  # noqa: BLE001
        print("  loader -> %s: %s" % (type(exc).__name__, exc))


def main() -> int:
    print("MBCX-01 BUILD — FIXTURE-ISOLATION probe (codex r2 F1/F2/F3/F4/F6/F7)")
    print("cwd: %s" % os.getcwd())
    operator_private, operator_public = generate_keypair()
    operator_anchor = anchor_document(OPERATOR_ANCHOR_ID, operator_public,
                                      fixture_only=False)
    print("operator anchor (generated in memory, NOT committed): anchor_id=%r "
          "fixture_only=False" % OPERATOR_ANCHOR_ID)
    print()
    probe_p1()
    print()
    probe_p2(operator_anchor)
    print()
    probe_p3(operator_anchor)
    print()
    probe_p4(operator_anchor, operator_private)
    print()
    probe_p5(operator_anchor, operator_private)
    print()
    probe_p6()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
