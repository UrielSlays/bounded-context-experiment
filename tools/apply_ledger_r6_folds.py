"""Assembly: repair-ledger rows for the codex r6 folds (driver-owned edit)."""
import json

PATH = "MBCX-01-BUILD-REPAIR-LEDGER.json"
led = json.load(open(PATH, encoding="utf-8"))
inv = led["invariants"]
WI = "test_mbcx01_build_integration.SmokePreLaunchResolutionWitnesses."
WM = "test_mbcx01_build_measurement.BuildEtwConsumerTests."
WS = "test_mbcx01_build_state.BuildAStateAuthorityWitnesses."
WC = "test_mbcx01_build_cohort.BuildCohortSliceClosingWitnesses."
SRC = ("codex-CLI r6 fold set (MBCX-01-CODEXCLI-r6-FULL-LOG-2026-08-16.log; five findings"
       " + the wholesale closed-verdict boundary, all red-first, 2026-08-16)")

row = inv["BI-12_CANDIDATE_IMAGE_RESOLUTION_MIRRORS_CREATEPROCESSW"]
row["requirement"] += (" [AMENDED 2026-08-16, codex r6 F1: the earlier text claimed PATHEXT"
                       " mirroring - FALSE. CreateProcessW appends .exe only; PATHEXT is the"
                       " shell's rule. Extensionless resolution is .exe-only as of this fold"
                       " (BI-14 owns the property); this row keeps the resolve-once and"
                       " hash-what-launches invariant.]")

inv["BI-14_EXTENSIONLESS_RESOLUTION_IS_EXE_ONLY"] = {
    "adversarial": [WI + "test_bi17_red_the_hashed_image_is_the_one_createprocessw_would_have_launched"],
    "modules": ["mbcx01_smoke_cell.py"],
    "note": "Positive half (resolve-once + hash-what-launches on the honest path) rides BI-12.",
    "positive": [],
    "positive_covered_by": "BI-12_CANDIDATE_IMAGE_RESOLUTION_MIRRORS_CREATEPROCESSW",
    "requirement": ("An extensionless candidate resolves by appending .exe and by no other"
                    " extension, so the hashed and certified image is the one the launch"
                    " semantics select; PATHEXT is never an input to resolution (codex r6 P1)."),
    "source": SRC,
}
inv["BI-15_SMOKE_TEARDOWN_NEVER_MASKS_THE_PRIMARY_FAULT"] = {
    "adversarial": [WI + "test_bi18_red_a_failing_session_stop_never_replaces_the_primary_fault"],
    "modules": ["mbcx01_smoke_cell.py"],
    "note": ("Sibling of BB-27 one layer up: that row is the consumer's own teardown; this is"
             " the driver's finally. With nothing in flight the cleanup failure IS the error"
             " (the positive/guard witness)."),
    "positive": [WI + "test_bi18_guard_a_failing_session_stop_with_nothing_in_flight_is_the_error"],
    "requirement": ("A failing ETW session stop in the smoke driver's finally never replaces"
                    " the primary setup/collection fault: it is attached as a note (the"
                    " collector's own add_note pattern) and surfaces alone only when no"
                    " exception is in flight (codex r6 P2)."),
    "source": SRC,
}
inv["BB-35_THREAD_LIFETIME_PAIRING_AGREES_ON_THE_PROCESS"] = {
    "adversarial": [WM + "test_bw100_adversarial_a_stop_from_another_member_cannot_close_a_lifetime"],
    "modules": ["mbcx01_build_etw_consumer.py"],
    "note": ("Fourth member of the AMENDMENT-2 thread-identity set: a thread is a TID AND an"
             " interval AND the process incarnation BOTH halves belong to. New fault"
             " ETW_THREAD_LIFETIME_PROCESS_MISMATCH joins BB-18's fault vocabulary."),
    "positive": [],
    "positive_covered_by": "BB-18_THREAD_IDENTITY_IS_A_TID_AND_AN_INTERVAL",
    "requirement": ("A thread lifetime pairs a START and a STOP that agree on the member"
                    " process identity; a STOP naming another member cannot close a lifetime"
                    " opened under a different process, so signed lifetime evidence is never"
                    " misattributed (codex r6 P2)."),
    "source": SRC,
}
inv["BA-23_STATE_SCOPE_MAP_VALUES_ARE_SCOPES_AT_THIS_SITE"] = {
    "adversarial": [WS + "test_ba48_adversarial_a_scope_map_whose_values_are_not_scopes_is_named"],
    "modules": ["mbcx01_build_state_authority.py"],
    "note": "Third site in the BA-21/BA-22 series; the class close is BA-24.",
    "positive": [],
    "positive_covered_by": "BA-15_FRESH_PROCESS_DURABLE_VERIFICATION",
    "requirement": ("A state whose scopes map carries non-scope values (null, list, string)"
                    " is the named schema refusal before reducer replay, never a raw"
                    " TypeError out of the public verifier (codex r6 P2)."),
    "source": SRC,
}
inv["BA-24_MALFORMED_CALLER_INPUT_IS_A_CLOSED_REFUSAL_AT_THE_PUBLIC_BOUNDARY"] = {
    "adversarial": [WS + "test_ba49_adversarial_the_closed_verdict_covers_shapes_nobody_enumerated"],
    "modules": ["mbcx01_build_state_authority.py"],
    "note": ("THE WHOLESALE CLOSE of the closed-list-escape class (third recurrence; tar-pit"
             " second-appearance ruling). COMPLEMENT: any caller input that makes the"
             " validator raise from the malformed-input tuple is the named schema refusal."
             " HONESTY CARVE-OUT, witnessed: only that tuple - the module's own errors and"
             " non-tuple classes (an internal defect) still fault loud and unconverted."
             " Cross-references BC-25, the same class on the cohort plane."),
    "positive": [],
    "positive_covered_by": "BA-15_FRESH_PROCESS_DURABLE_VERIFICATION",
    "requirement": ("verify_state_authority_receipt_v2 answers with its closed error list for"
                    " EVERY caller input: the public boundary converts the malformed-input"
                    " exception tuple to STATE_AUTHORITY_V2_SCHEMA_INVALID (plus the sentinel"
                    " where the contract requires it), and ONLY that tuple - a genuine"
                    " internal defect still faults loud (codex r6 P2 class, wholesale)."),
    "source": SRC,
}
inv["BC-24_COHORT_CUT_MAP_IS_A_MAP_AT_BOTH_DOORS"] = {
    "adversarial": [WC + "test_bc24_red_a_cut_map_that_is_not_a_map_refuses_by_name"],
    "modules": ["mbcx01_build_cohort_authority.py"],
    "note": ("The falsy spellings ([], null) were previously refused only as an opaque"
             " SOURCE_PROVENANCE_MISMATCH; all non-map shapes are now the named schema"
             " refusal, at the validator door AND the selection door."),
    "positive": [],
    "positive_covered_by": "BC-08_SCORER_JOIN_END_TO_END_ON_THE_BUILD_PATH",
    "requirement": ("A candidate whose canonical_state_by_cut is not a mapping is"
                    " BUILD_CANDIDATE_SCHEMA_INVALID by name at both public doors"
                    " (validate_build_source_provenance and select_build_cohort), never an"
                    " AttributeError escape (codex r6 P2)."),
    "source": SRC,
}
inv["BC-25_MALFORMED_CALLER_INPUT_IS_A_CLOSED_REFUSAL_AT_THE_PUBLIC_BOUNDARY"] = {
    "adversarial": [WC + "test_bc25_red_the_closed_verdict_covers_shapes_nobody_enumerated"],
    "modules": ["mbcx01_build_cohort_authority.py"],
    "note": ("The cohort-plane half of the wholesale close; cross-references BA-24. Covers"
             " BOTH public doors (the validator and select_build_cohort, which reaches"
             " pop_declared_eligibility first). Same honesty carve-out, witnessed."),
    "positive": [],
    "positive_covered_by": "BC-08_SCORER_JOIN_END_TO_END_ON_THE_BUILD_PATH",
    "requirement": ("validate_build_source_provenance and select_build_cohort answer with the"
                    " closed vocabulary for EVERY caller input: the malformed-input exception"
                    " tuple converts to BUILD_CANDIDATE_SCHEMA_INVALID, and only that tuple -"
                    " internal defects still fault loud (codex r6 P2 class, wholesale)."),
    "source": SRC,
}

witnesses = set()
for r in inv.values():
    witnesses.update(r.get("positive") or [])
    witnesses.update(r.get("adversarial") or [])
led["totals"] = {"invariants": len(inv), "witnesses": len(witnesses)}
print("totals:", led["totals"])
with open(PATH, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(led, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("written")
