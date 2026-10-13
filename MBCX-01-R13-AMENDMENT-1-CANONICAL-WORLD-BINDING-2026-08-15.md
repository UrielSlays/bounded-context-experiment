# MBCX-01 r13.2 — AMENDMENT 1: the canonical world binds SUBJECT and OWNER ROLE

**Status:** ADOPTED. Owner-ruled in live chat 2026-08-15 — *"Put them in as amendment. its Fine."*
**Amends:** the frozen r13.2 layer (`mbcx01_r13_packets.py`, `mbcx01_r13_measurement.py`), which was
3/3 CONFIRMED and otherwise unchanged. This is the FIRST amendment to that freeze.
**Origin:** BUILD acceptance council round 4 (2026-08-15), SEAT2 finding F1, EXECUTED; independently
reproduced at the byte by the driver before it was escalated or folded.

## 1. The defect, plainly

The design of record says the canonical experiment world records, for every visible obligation, its
**subject** and **owner role**:

> `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:35` — *"all visible obligation IDs with subject, owner
> role, lifecycle, due time, critical flag and sorted prerequisite IDs"*

The frozen implementation recorded neither. `project_state_world` projected five fields
(`lifecycle · critical · due_at · completion_action_id · prerequisite_obligation_ids`), and
`_fixture_authoritative_state` supplied `subject_id` / `owner_role` as flat defaults that the reduced
field set then overwrote — so the two fields were never bound to the manifest at any point.

**Why it mattered rather than being cosmetic.** `owner_role` is not a constant of the experiment. Two
legal transitions in the experiment's own reducer rewrite it:
`mbcx01_r13_state_reference.py:222` (`delegate_obligation`) and `:216` (`reopen_obligation`). So a
legal delegation at the same cut produced a state that the canonical world could not express, and
invariant **I02** — whose contract is that a legal same-cut obligation change must yield
`MANIFEST_CUT_STATE_MISMATCH` — passed it.

**Driver reproduction, pre-amendment:**

```
target obligation : OBL.DECOY
owner_role BEFORE : WORKER          owner_role AFTER : ROLE.FRESH.ADVERSARY
subject_id BEFORE : SUB.SHARED      subject_id AFTER : SUB.SUBSTITUTED
projection byte-IDENTICAL across the change : True
projection hash BEFORE : D743C7834F09AE52823765D53740F85A56F2EBEF7481261D847A385EC9B5DCA6...
projection hash AFTER  : D743C7834F09AE52823765D53740F85A56F2EBEF7481261D847A385EC9B5DCA6...  (equal)
```

**Why the frozen suite never caught it.** The banked I02 falsification witness mutates `critical` —
one of the five fields that *was* projected. The witness could only ever exercise the fields the
projection already carried, so 145/145 stayed green over the hole. This is the same author-blind-spot
class the round found in BUILD witness `bw28`.

## 2. What is NOT claimed

- **No banked result is wrong.** Because the two fields were never projected, they also never fed
  `legal_action_ids_from_world`, so no gold answer and no score changes as a consequence of this
  amendment. What was false is the design of record's claim about what the canonical world binds,
  and I02's promise about legal same-cut changes.
- **No estimand, route, inference, or n=768 change.** The amendment is additive and touches only the
  world projection and the world the fixture generator emits.
- **Not a security finding.** This lane's design carries no threat model; this is a
  scientific-validity defect. See `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`.

## 3. The change

| File | Change |
|---|---|
| `mbcx01_r13_packets.py` `project_state_world` | projects `subject_id` and `owner_role` alongside the original five fields |
| `mbcx01_r13_measurement.py` `_candidate_world` | the three OBLIGATION rows now declare `subject_id` and `owner_role` |
| `test_mbcx01_r13_packets.py` | **two new red witnesses** (below) |
| `verify-build-bundle.py` | `FROZEN_TEST_TOTAL` 145 → 147, with the reason recorded at the constant |

**Values are truthful, not invented.** `SUB.SHARED` / `WORKER` are exactly what
`mbcx01_r13_state_reference.initial_state()` already assigns to both pre-existing obligations, and
exactly the defaults `mbcx01_r13_packets.py:365` already applied to `OBL.DECOY`. The amendment makes an
existing unstated fact explicit; it does not change any obligation's owner or subject.

## 4. Red witnesses (RED before the fix, GREEN after — the contract, not a formality)

`test_i02_same_cut_owner_role_change_is_rejected` and `test_i02_same_cut_subject_change_is_rejected`.

**RED, on pre-fix bytes, source confirmed untouched (`git diff --stat` empty on both source files):**

```
FAIL: test_i02_same_cut_owner_role_change_is_rejected
    self.assertFalse(self._matrix(forged)["I02"])
AssertionError: True is not false

FAIL: test_i02_same_cut_subject_change_is_rejected
    self.assertFalse(self._matrix(forged)["I02"])
AssertionError: True is not false

Ran 2 tests — FAILED (failures=2)
```

**GREEN, post-fix:** both pass; frozen suite `Ran 147 tests — OK`; BUILD suite `Ran 114 tests — OK`;
`verify-build-bundle.py` exit **0**, seven sections PASS, ledger 44 invariants / 114 witnesses,
`two_way_total: true`, readiness unchanged at `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.

⚠ **The freeze guard fired correctly in between**, and that is worth recording: with the fix in and the
count still pinned at 145, the bundle verifier refused with
`BUILD VERIFICATION FAILED: frozen r13.2 suite total changed: 147 != 145` (real exit 1). Raising
`FROZEN_TEST_TOTAL` is how a frozen-layer change gets **declared**. It is not routine maintenance, and
a future reader who finds that number moved should expect an amendment document like this one beside it.

## 5. Ripple

Adding two fields to the world changes `canonical_world_hash`, and therefore `manifest_hash` and every
hash derived from it. **Nothing was hand-updated**: the frozen layer computes these at runtime rather
than pinning hash literals in tests, so all 147 recompute consistently. The R13 and BUILD pin manifests
pin *file blobs* and must be regenerated at the accepted commit — tracked with the pin-freshness row the
same council round opened (`MBCX01-R4-PIN-MANIFEST-STALE-AND-FALSE-PACKET-CLAIM`).

## 6. Re-review

The amendment changes an invariant consumer, so the r4 packet's §13 re-review trigger fires: the frozen
layer's amended bytes go back to council with the other r4 folds, not straight to a gate.
