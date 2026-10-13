"""Assembly: repair-ledger rows for the codex r8 folds (driver-owned edit)."""
import json

PATH = "MBCX-01-BUILD-REPAIR-LEDGER.json"
led = json.load(open(PATH, encoding="utf-8"))
inv = led["invariants"]
WU = "test_mbcx01_build_state.BuildAStoreUriEncodingWitnesses."
WP = "test_mbcx01_build_measurement.BuildEtwPhysicalPathTests."
WRS = "test_mbcx01_build_integration.SmokeRelativeSpacedPathWitnesses."
SRC = ("codex-CLI r8 fold set (MBCX-01-CODEXCLI-r8-FULL-LOG-2026-08-17.log; three findings,"
       " two of them NEIGHBOURS of the r7 folds, all red-first, 2026-08-17)")

inv["BA-25_STORE_URI_ADDRESSES_THE_REQUESTED_FILE"] = {
    "adversarial": [
        WU + "test_ba50_red_a_metacharacter_in_the_path_never_redirects_the_writer",
        WU + "test_ba50_red_a_literal_percent_escape_in_the_name_is_not_decoded",
        WU + "test_ba50_red_the_readonly_door_stays_on_the_requested_file_and_stays_readonly",
    ],
    "modules": ["mbcx01_build_state_store.py"],
    "note": ("One encoder, three call sites (writable target, ?mode=ro reader,"
             " shared-cache in-memory target) - the enumerated set, not a sampled one."
             " sqlite.org/uri.html steps 4 and 5 deliberately NOT applied, reasons"
             " in-module. The red found TWO defects beyond the reported one: ?mode=ro"
             " fell inside the discarded fragment (the read-only door was writable) and"
             " a legal literal %23 name was decoded. Neighbours BA-17/BA-19: those rows'"
             " identity check was green about a file the connection never touched."),
    "positive": [WU + "test_ba50_guard_ordinary_paths_and_in_memory_targets_are_untouched"],
    "requirement": ("Every file: URI handed to sqlite3.connect(uri=True) is percent-encoded"
                    " per sqlite.org/uri.html section 3.1 (% first, then # and ?), so the"
                    " connection addresses EXACTLY the requested path - the identity check"
                    " and the writer can no longer be looking at two different files, and"
                    " ?mode=ro can no longer fall inside a discarded fragment (codex r8 P1)."),
    "source": SRC,
}

row = inv["BB-36_PMC_IS_ATTACHED_BEFORE_THE_CONSUMER_OPENS"]
row["requirement"] += (" [AMENDED 2026-08-17, codex r8 P1: the r7 close was INCOMPLETE -"
                       " EVENT_TRACE_FLAG_CSWITCH rides StartTraceW itself, so switches"
                       " were buffered without a counter one call earlier than the pump."
                       " start() no longer passes that flag; it is turned on by"
                       " ControlTraceW(EVENT_TRACE_CONTROL_UPDATE) AFTER configure_pmc(),"
                       " carrying the whole enable-flag set because a non-zero EnableFlags"
                       " names the providers to enable or keep enabled.]")
row["adversarial"] += [
    WP + "test_bw96_red_the_cswitch_flag_is_not_enabled_until_the_counter_is_attached",
    WP + "test_bw96_red_the_attach_precedes_every_cswitch_generating_enable",
]
row["positive"].append(
    WP + "test_bw96_guard_the_update_call_carries_what_controltracew_documents")
row["note"] = (row.get("note", "") + " UNVERIFIED_UNTIL_ELEVATED_RUN: the ControlTraceW"
               " UPDATE call has never executed against a live session; its failure mode"
               " is loud and early, before any measurement.")

row = inv["BI-16_CREATEPROCESSW_RESOLUTION_SET_IS_CLOSED"]
row["requirement"] += (" [AMENDED 2026-08-17, codex r8 P2: the unquoted-whitespace rule is"
                       " a property of the COMMAND LINE, not of its first token - an"
                       " unquoted RELATIVE spaced path has a pathless head by construction"
                       " and was answered CANDIDATE_BINARY_NOT_FOUND. Ambiguity detection"
                       " now walks the whitespace-extended prefixes and refuses when one"
                       " NAMES AN EXISTING FILE.]")
row["adversarial"] += [
    WRS + "test_bi23_red_a_relative_spaced_path_with_a_pathless_first_token_is_refused",
    WRS + "test_bi23_red_the_extended_prefixes_are_the_documented_possibilities",
]
row["positive"].append(
    WRS + "test_bi23_guard_the_wider_refusal_still_cannot_eat_a_shape_that_works")

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
