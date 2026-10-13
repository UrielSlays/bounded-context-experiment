# MBCX-01 BUILD — carrier-exactness production verifier: specification

Status: BUILD work-product 6 (specification half; the identity-binding implementation is
`mbcx01_build_exactness_authority.py`). Governs what production carrier-exactness authority
means and what remains for the smoke/production stage.

## 1. What exactness authority asserts

A `CarrierExactnessReceiptV3` in production asserts: *the exact carrier artifact named by
`carrier_artifact_digest`, executed under the exact harness build named by the trust root,
passed the pinned exactness witness suite, and this PASS is bound to the exact 100-cell
measurement grid identity it rides with.* Fixture V2 receipts assert conformance of the
verifier machinery only, never carrier behavior.

⚠ **What the BUILD-stage verifier issues is NOT that assertion** (BUILD acceptance r2,
codex F7). §3 defers the suite EXECUTION, so the implemented authority emits
`result: AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED` — an authority BINDING over an
exactness claim — and refuses a receipt that claims `PASS`
(`CARRIER_EXACTNESS_SUITE_NOT_EXECUTED`). The full assertion above becomes expressible
only when the §3 suite runner exists and its evidence is authenticated; until then no
artifact of this lane carries a word that reads as "the suite ran". Witness bw25.

## 2. What the BUILD implementation enforces (implemented + witnessed)

`verify_production_carrier_exactness(receipt, *, envelopes, suite_document, trust_root_manifest)`:

- schema V3 with closed key set; any non-V3 claim wearing production labels →
  `FIXTURE_EVIDENCE_RELABELED` before anything else;
- suite identity: injected `suite_document` canonically byte-identical to the pinned suite;
  `suite_artifact_hash` and `witness_set_hash` recomputed via the frozen
  `_exactness_suite_authority`, never trusted;
- carrier binding: `carrier_artifact_digest` equals the single digest carried by ALL 100
  signed envelopes; harness build digest equals the root's `authorized_harness_build_digest`;
- grid binding: `measurement_grid_identity_hash` recomputed from the envelopes;
- signatures: all 100 envelopes verified against the production root;
- `result` is a claim: any field the receipt carries must equal the recomputed value. The
  ONLY accepted and emitted value is `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`; a claim
  of `PASS` is refused `CARRIER_EXACTNESS_SUITE_NOT_EXECUTED` and any other value refuses
  `CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE` — the verifier never blesses, and never lends
  its label to an execution it did not witness;
- the trust context is resolved ONCE at entry like the other two production doors, and
  trust-root validity is judged at the VERIFIER's instant (BUILD acceptance r2 fold).

## 3. What is DEFERRED to the physical stage (stated, not papered over)

The per-witness EXECUTION of the pinned suite (`CARRIER.EXACTNESS.CANONICAL_INPUT`,
`CANONICAL_OUTPUT`, `REPLAY`, `BUILD_IDENTITY`) against the real carrier binary requires the
physical harness: the suite runner feeds the carrier the canonical witness inputs inside the
same supervised Job discipline and compares outputs byte-exactly. Until that runs under a
separate authorization, production exactness authority remains UNAVAILABLE by construction —
the identity-binding verifier above is necessary, not sufficient, and says so in its
docstring. The suite-runner contract for the smoke stage:

1. inputs: pinned suite document + carrier artifact (digest-checked before execution);
2. execution: one supervised run per witness, same containment discipline as measurement
   cells, evidence retained;
3. output: witness-level pass/fail + transcript digests, assembled into the V3 receipt by
   the PRODUCER role and signed under the production root;
4. any witness failure, containment gap, or digest mismatch ⇒ no receipt (fail-loud), never
   a receipt with a qualified PASS.

## 4. Custody note

The exactness receipt inherits the measurement custody model (same roots, same
signer/editor disjointness); it carries `trust_root_id` and is admitted only under the same
injected manifest + custody evidence as measurement admission
(`evaluate_production_measurement` owns the custody gate; the exactness verifier re-verifies
structure/signature/identity — a candidate hardening item recorded at green: give the
exactness verifier its own custody parameter when the suite runner lands).
