"""Driver reproductions, cohort-BUILD acceptance r1 — every acted-on finding re-run at the byte.

Read-only against the repo; prints evidence; asserts nothing silently.
"""
import copy, hashlib, json, sys

import mbcx01_build_cohort_generator as generator
import mbcx01_build_cohort_authority as authority
import mbcx01_build_cohort_packet as packet

print("== GENERATE (once, reused) ==")
gen = generator.generate_cohort()
retained = gen.context.retained_candidates
print("generated", len(gen.candidates), "retained", len(retained),
      "root", gen.retained_set_root()[:16])

# R1 — S1-A: gold constancy across the retained 768
golds = {row["gold_action_id_by_cut"][row["chosen_cut_id"]] for row in retained}
print("\n== R1 S1-A distinct gold_action_id over retained 768:", len(golds))
print("   values:", sorted(golds))

# R2 — S3-F1: observation signature -> motif codebook
sig_to_motifs = {}
for row in retained:
    rec = row["observation_authority_by_cut"][row["chosen_cut_id"]]
    sig = (rec["family"], rec["code"], rec["cardinality"], rec["order"])
    sig_to_motifs.setdefault(sig, set()).add(row["motif"])
unique = {s: m for s, m in sig_to_motifs.items() if len(m) == 1}
count_unique_rows = sum(
    1 for row in retained
    if len(sig_to_motifs[(row["observation_authority_by_cut"][row["chosen_cut_id"]]["family"],
                          row["observation_authority_by_cut"][row["chosen_cut_id"]]["code"],
                          row["observation_authority_by_cut"][row["chosen_cut_id"]]["cardinality"],
                          row["observation_authority_by_cut"][row["chosen_cut_id"]]["order"])]) == 1)
print("\n== R2 S3-F1 signatures:", len(sig_to_motifs), "single-motif signatures:", len(unique),
      "retained rows carrying a single-motif signature:", count_unique_rows)
for sig in sorted(unique)[:6]:
    print("   ", sig, "->", sorted(unique[sig]))

# R3 — S3-F2: coverage numerator APPLIED-only vs all executed events
target = sorted((a, b) for a in generator.EVENT_ALPHABET for b in generator.EVENT_ALPHABET)
applied_pairs, all_pairs = set(), set()
for cand in gen.candidates:
    evs_applied = [e["event_type"] for e, c in zip(cand["event_program"], cand["event_result_codes"]) if c == "APPLIED"]
    evs_all = [e["event_type"] for e in cand["event_program"]]
    for seq, sink in ((evs_applied, applied_pairs), (evs_all, all_pairs)):
        for i, a in enumerate(seq):
            for b in seq[i + 1:]:
                sink.add((a, b))
print("\n== R3 S3-F2 numerator: APPLIED-only", len(applied_pairs), "all-events", len(all_pairs),
      "reported", gen.coverage["covered_pair_count"])
print("   missing-from-APPLIED:", sorted(all_pairs - applied_pairs))

# R4 — S1-B/S3-F3: placement shortfall on a one-stratum draft set
one_stratum = []
for i in range(12):
    row = copy.deepcopy(gen.candidates[0])
    row["scenario_id"] = "SCENARIO.PROBE.%d" % i
    one_stratum.append(row)
placements = generator._plan_placements(one_stratum, [], 12)
print("\n== R4 placement shortfall: requested 12, one joint stratum -> len(placements) =", len(placements))

# R5 — S2-F1: ghost FACT through the SERVING path with a rebuilt self-consistent context
victim = None
for row in gen.candidates:
    if gen.context.retained_position(row["scenario_id"]) is not None:
        victim = copy.deepcopy(row)
        break
# find the retained (enriched) twin's chosen cut
chosen = next(r["chosen_cut_id"] for r in retained if r["scenario_id"] == victim["scenario_id"])
ghost = {"object_id": "FACT.GHOST.NO.JOURNAL", "object_kind": "FACT",
         "fields": {"subject_id": "GHOST", "predicate_id": "PRED.GHOST",
                    "value_code": "VALUE.GHOST", "valid_from": generator.T0, "valid_to": None},
         "source_event_ids": []}
mutated = copy.deepcopy(gen.candidates)
for row in mutated:
    if row["scenario_id"] == victim["scenario_id"]:
        world = row["canonical_world_by_cut"][chosen]
        world.append(copy.deepcopy(ghost))
        world.sort(key=lambda r: r["object_id"].encode("utf-8"))
        bc = set(row["bc_selected_object_ids_by_cut"][chosen])
        bc.add("FACT.GHOST.NO.JOURNAL")
        row["bc_selected_object_ids_by_cut"][chosen] = sorted(bc, key=lambda v: v.encode("utf-8"))
        victim_mut = row
prov2 = authority.build_source_provenance(mutated, gen.coverage)
ctx2 = authority.BuildRetainedAuthorityContext(mutated, prov2, packet.ELIGIBILITY_PREDICATE)
# The serving path takes the RETAINED (enriched) copy — the raw draft is not what the
# context indexes (first probe run failed here: broken harness, not a disproof).
victim_mut = next(r for r in ctx2.retained_candidates
                  if r["scenario_id"] == victim["scenario_id"])
chosen = victim_mut["chosen_cut_id"]
vm = packet.validate_build_manifest(
    packet.build_manifest_for_candidate(victim_mut, chosen, context=ctx2), victim_mut, chosen, context=ctx2)
print("\n== R5 S2-F1 ghost FACT:")
print("   validate_build_manifest:", vm)
try:
    fx = packet.build_scoring_fixture_for_candidate(victim_mut, "BC", context=ctx2, cut_id=chosen)
    a0 = json.dumps(fx["a0_packet"])
    print("   build_scoring_fixture: BUILT; ghost in BC A0:", "FACT.GHOST.NO.JOURNAL" in a0)
    rec = packet.render_all_six_nodes(victim_mut, context=ctx2, cut_id=chosen)
    print("   render_all_six_nodes admitted:", rec["admitted"])
except Exception as exc:
    print("   serving path REFUSED:", type(exc).__name__, exc)

# R6 — S2-F2: forged observation record carrying the literal gold action id
victim2 = None
for row in gen.candidates:
    if gen.context.retained_position(row["scenario_id"]) is not None and row["scenario_id"] != victim["scenario_id"]:
        victim2 = row["scenario_id"]
        break
chosen2 = next(r["chosen_cut_id"] for r in retained if r["scenario_id"] == victim2)
mutated2 = copy.deepcopy(gen.candidates)
for row in mutated2:
    if row["scenario_id"] == victim2:
        gold = row["gold_action_id_by_cut"][chosen2]
        rec = row["observation_authority_by_cut"][chosen2]
        rec["code"] = gold
        for i, obs_row in enumerate(rec["rows"]):
            obs_row["code"] = "%s.%d" % (gold, i)
        rec["record_hash"] = packet.observation_record_hash(rec)
        row["observation_by_cut"][chosen2] = packet.observation_manifest_representation(rec)
        world = [r for r in row["canonical_world_by_cut"][chosen2] if r["object_kind"] != "OBSERVATION"]
        world += packet.observation_world_rows(rec)
        world.sort(key=lambda r: r["object_id"].encode("utf-8"))
        row["canonical_world_by_cut"][chosen2] = world
        victim2_mut = row
prov3 = authority.build_source_provenance(mutated2, gen.coverage)
ctx3 = authority.BuildRetainedAuthorityContext(mutated2, prov3, packet.ELIGIBILITY_PREDICATE)
victim2_mut = next(r for r in ctx3.retained_candidates if r["scenario_id"] == victim2)
chosen2 = victim2_mut["chosen_cut_id"]
rec = victim2_mut["observation_authority_by_cut"][chosen2]
print("\n== R6 S2-F2 forged observation record:")
print("   validate_observation_authority_record:", packet.validate_observation_authority_record(rec))
vm2 = packet.validate_build_manifest(
    packet.build_manifest_for_candidate(victim2_mut, chosen2, context=ctx3), victim2_mut, chosen2, context=ctx3)
print("   validate_build_manifest:", vm2)
fresh = generator.derive_observation_authority(victim2_mut["scenario_id"], chosen2, rec["projection"])
print("   fresh derivation matches forged:", fresh["code"] == rec["code"], "(expected code:", fresh["code"] + ")")
try:
    fx2 = packet.build_scoring_fixture_for_candidate(victim2_mut, "BC", context=ctx3, cut_id=chosen2)
    a0 = json.dumps(fx2["a0_packet"])
    print("   build_scoring_fixture: BUILT; gold-as-observation served:", rec["code"] in a0)
    rr = packet.render_all_six_nodes(victim2_mut, context=ctx3, cut_id=chosen2)
    print("   render_all_six_nodes admitted:", rr["admitted"])
except Exception as exc:
    print("   serving path REFUSED:", type(exc).__name__, exc)

print("\n== DONE ==")
