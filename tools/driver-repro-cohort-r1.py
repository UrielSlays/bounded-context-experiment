"""Driver byte-reproduction of council r1 findings (read-only; no repo writes)."""
import copy, json, sys

import mbcx01_r13_common as common
import mbcx01_r13_state_reference as ref
import mbcx01_r13_state_oracle as orc
import mbcx01_r13_measurement as m
import mbcx01_r13_packets as p


def unpack(res):
    if isinstance(res, tuple):
        st = next((x for x in res if isinstance(x, dict)), None)
        rc = next((x for x in res if isinstance(x, str)), None)
        return st, rc
    return res, "?"


def apply_both(state_r, state_o, ev):
    rr = ref.reference_apply(copy.deepcopy(state_r), copy.deepcopy(ev))
    oo = orc.oracle_apply(copy.deepcopy(state_o), copy.deepcopy(ev))
    return rr, oo


print("=== P1: assert -> correct -> retract(correction): is anything visible? ===")
state = common.initial_state()
o_state = common.initial_state()
e1 = common.make_event("assert_fact", {"subject_id": "SUB.F", "predicate_id": "PRED.F",
                                        "value_code": "V1"}, state=state)
state, rc1 = unpack(ref.reference_apply(state, e1))
o_state, oc1 = unpack(orc.oracle_apply(o_state, e1))
print("apply1:", rc1, "|", oc1)

e2 = common.make_event("correct_fact", {"subject_id": "SUB.F", "predicate_id": "PRED.F",
                                         "parent_event_id": e1["event_id"],
                                         "value_code": "V2"}, state=state, valid_from=common.T1)
state, rc2 = unpack(ref.reference_apply(state, e2))
o_state, oc2 = unpack(orc.oracle_apply(o_state, e2))
print("apply2:", rc2, "|", oc2)

e3 = common.make_event("retract_fact", {"subject_id": "SUB.F", "predicate_id": "PRED.F",
                                         "target_event_id": e2["event_id"]}, state=state, valid_from=common.T1)
state, rc3 = unpack(ref.reference_apply(state, e3))
o_state, oc3 = unpack(orc.oracle_apply(o_state, e3))
print("apply3:", rc3, "|", oc3)

print("dual byte-identical:", common.canonical_json(state) == common.canonical_json(o_state))
facts = state["scopes"]["SCOPE.SHARED"]["facts"]
print("facts structure:")
print(json.dumps(facts, indent=1, sort_keys=True, default=str)[:1500])

print()
print("=== P2: FACT row never in journal + contradictory observation pass manifest validation ===")
baseline = p.packet_fixture_manifest()
mutant = copy.deepcopy(baseline)
mutant["canonical_world"].append({
    "object_id": "FACT.NEVER.IN.JOURNAL", "object_kind": "FACT",
    "fields": {"fact_key": common.fact_key("SUB.GHOST", "PRED.GHOST"),
               "value_code": "GHOST", "valid_from": common.T0, "valid_to": None},
    "source_event_ids": ["EV.GHOST"]})
obs = next(r for r in mutant["canonical_world"] if r["object_kind"] == "OBSERVATION")
obs["fields"]["code"] = "WORLD_SAYS_FALSE"
mutant["observation"]["code"] = "TOP_LEVEL_SAYS_TRUE"
mutant["canonical_world"].sort(key=lambda r: r["object_id"].encode("utf-8"))
mutant["canonical_world_hash"] = p.sha384(mutant["canonical_world"])
mutant["gold_read_set"] = p._expected_gold_read_set(mutant, mutant["gold_action_id"])
mutant["manifest_hash"] = p.hash_without(mutant, "manifest_hash")
errs = p.validate_expected_manifest(mutant)
print("mutant manifest errors:", errs)

print()
print("=== P3: catalog authority - distinct catalog hashes across retained 768 ===")
cands, prov = m.synthetic_candidates_r13()
sel = m.select_cohort(cands, prov)
hashes = set()
carries_catalog = set()
for row in sel:
    man = p.manifest_for_retained_candidate(row)
    hashes.add(man["action_catalog_hash"])
    carries_catalog.add("action_catalog" in row)
print("selected:", len(sel), "distinct manifest catalog hashes:", len(hashes),
      "candidate carries its own catalog field:", carries_catalog)
one = p.manifest_for_retained_candidate(sel[0])
print("catalog rows in manifest:", len(one["action_catalog"]),
      "candidate action_ids at chosen cut:", len(sel[0]["action_ids_by_cut"][sel[0]["chosen_cut_id"]]))

print()
print("=== P4: envelope - seat-3 shape (30 obligations, long IDs, 29 deps, 12 actions, 4 source events) ===")
big = copy.deepcopy(baseline)
world = [r for r in big["canonical_world"] if r["object_kind"] == "OBSERVATION"]
catalog = []
scope = big["scope_id"]
obl_ids = []
for i in range(30):
    oid = ("OBL.%02d." % i) + "X" * (128 - 7)
    obl_ids.append(oid)
    aid = p.action_id(scope, oid)
    world.append({"object_id": oid, "object_kind": "OBLIGATION",
                  "fields": {"subject_id": ("SUB.%02d." % i) + "Y" * (128 - 7),
                             "owner_role": "WORKER",
                             "lifecycle": "OPEN", "critical": i == 0,
                             "due_at": common.T0 if i == 0 else "2027-01-01T00:00:00.000000Z",
                             "completion_action_id": aid,
                             "prerequisite_obligation_ids": []},
                  "source_event_ids": [("EV.%02d.%d." % (i, k)) + "Z" * (128 - 9) for k in range(4)]})
    if len(catalog) < 12:
        catalog.append({"action_id": aid, "action_kind": "ACT_ON_OBLIGATION",
                        "scope_id": scope, "obligation_id": oid})
dep_rows = 0
for i in range(1, 30):
    if dep_rows >= 29:
        break
    parent = obl_ids[(i - 1) // 3]  # width<=3 fanout, depth<=3-ish
    child = obl_ids[i]
    if parent == child:
        continue
    did = "DEP.%02d." % i + "W" * (128 - 7)
    world.append({"object_id": did, "object_kind": "DEPENDENCY",
                  "fields": {"obligation_id": child, "prerequisite_obligation_id": parent},
                  "source_event_ids": [("EVD.%02d." % i) + "Q" * (128 - 8)]})
    dep_rows += 1
world.sort(key=lambda r: r["object_id"].encode("utf-8"))
big["canonical_world"] = world
big["action_catalog"] = sorted(catalog, key=lambda r: r["action_id"].encode("utf-8"))
big["canonical_world_hash"] = p.sha384(big["canonical_world"])
big["action_catalog_hash"] = p.sha384(big["action_catalog"])
gold = p._unique_gold_action(big)
print("unique gold:", bool(gold))
big["gold_action_id"] = gold
big["gold_read_set"] = p._expected_gold_read_set(big, gold)
big["manifest_hash"] = p.hash_without(big, "manifest_hash")
print("manifest errors:", p.validate_expected_manifest(big))
for cond in ("BC", "OM"):
    try:
        pkt = p.build_decision_packet(big, cond, "A0_PRECOMMIT")
        raw = p.canonical_json(pkt)
        try:
            served = p.render_served_input(pkt)
            print(cond, "unpadded:", len(raw), "served:", len(served))
        except Exception as exc:
            print(cond, "unpadded:", len(raw), "render REFUSED:", exc)
    except Exception as exc:
        print(cond, "packet build REFUSED:", exc)
