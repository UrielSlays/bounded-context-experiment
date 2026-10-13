"""Assembly: repair-ledger rows for the codex r7 folds (driver-owned edit)."""
import json

PATH = "MBCX-01-BUILD-REPAIR-LEDGER.json"
led = json.load(open(PATH, encoding="utf-8"))
inv = led["invariants"]
WP = "test_mbcx01_build_measurement.BuildEtwPhysicalPathTests."
WR = "test_mbcx01_build_integration.SmokeCreateProcessWResolutionSetWitnesses."
SRC = ("codex-CLI r7 fold set (MBCX-01-CODEXCLI-r7-FULL-LOG-2026-08-16.log; four findings"
       " + the CreateProcessW documented-set close incl. one member codex never reported,"
       " all red-first, 2026-08-16)")

# BI-14 amendment: its .exe-only claim holds for BARE tokens only.
row = inv["BI-14_EXTENSIONLESS_RESOLUTION_IS_EXE_ONLY"]
row["requirement"] += (" [AMENDED 2026-08-16, codex r7: the .exe-only rule holds for a BARE"
                       " extensionless token only - a PATH-CARRYING extensionless token is"
                       " used VERBATIM with no candidates and no fallback, per CreateProcessW's"
                       " path-sensitive rule; BI-16 owns the full documented set.]")

inv["BB-36_PMC_IS_ATTACHED_BEFORE_THE_CONSUMER_OPENS"] = {
    "adversarial": [
        WP + "test_bw96_red_the_pmc_counter_is_attached_before_the_pump_opens",
        WP + "test_bw96_red_an_early_cswitch_without_pmc_rejects_the_whole_run",
    ],
    "modules": ["mbcx01_build_etw_consumer.py"],
    "note": ("The second witness is the CONSEQUENCE half (green both sides by design: one"
             " PMC-less CSwitch rejects the whole one-shot run - which is exactly why the"
             " ordering matters). configure_pmc is idempotent as of this fold (rider,"
             " red-covered by bw98 part a)."),
    "positive": [WP + "test_bw98_guard_the_fixes_refuse_nothing_that_was_right_before"],
    "requirement": ("The PMC counter list and its sampling event are attached to the session"
                    " BEFORE OpenTraceW/ProcessTrace opens, so no context switch can be"
                    " delivered without a PMC extended-data item and no right capture is"
                    " refused as ETW_PMC_EXTENDED_DATA_ABSENT (codex r7 P1 - the class that"
                    " would have aborted the owner's one elevated session)."),
    "source": SRC,
}
inv["BB-37_PROCESS_PARENT_IDENTITY_COMES_FROM_THE_PAYLOAD"] = {
    "adversarial": [
        WP + "test_bw97_red_the_parent_identity_comes_from_the_payload_not_the_header",
        WP + "test_bw97_red_the_scoped_roster_follows_the_payload_parent",
    ],
    "modules": ["mbcx01_build_etw_consumer.py"],
    "note": ("Brokered/explicit-parent creation makes the emitting context differ from the"
             " declared parent; the header pid is retained as event_header_process_id,"
             " diagnostic only, deciding no membership. Positive half (an honest tree"
             " scoping correctly) rides BB-19's live-member-population positive."),
    "positive": [],
    "positive_covered_by": "BB-19_LIVE_MEMBER_POPULATION_IS_THE_JOB_TREE",
    "requirement": ("A ProcessStart's parent tuple is decoded from the v3/v4 payload"
                    " (ParentProcessID @20, ParentProcessSequenceNumber @24, per the"
                    " TDH-verified layout); EventHeader.ProcessId decides no membership, so"
                    " the signed member tree can neither omit a legitimate descendant nor"
                    " admit a foreign process (codex r7 P2)."),
    "source": SRC,
}
inv["BI-16_CREATEPROCESSW_RESOLUTION_SET_IS_CLOSED"] = {
    "adversarial": [
        WR + "test_bi19_red_a_path_carrying_extensionless_token_is_used_verbatim",
        WR + "test_bi19_red_a_path_carrying_token_never_falls_back_to_the_exe",
        WR + "test_bi19_red_a_bare_extensionless_name_has_no_bare_fallback",
        WR + "test_bi20_red_an_unquoted_spaced_path_is_refused_by_name",
        WR + "test_bi20_red_an_unquoted_extensionless_path_with_arguments_is_refused",
        WR + "test_bi21_red_every_documented_resolution_rule_is_closed_by_name",
        WR + "test_bi22_red_the_bare_name_search_sequence_has_all_six_documented_steps",
    ],
    "note": ("THE DOCUMENTED-SET CLOSE (four-partial-fixes law): every CreateProcessW"
             " (NULL lpApplicationName) resolution rule from the Learn page is implemented"
             " or refused by name, in one table-driven witness - including the 16-bit"
             " System search step NO review round ever reported (bi22), and the"
             " unquoted-whitespace interpretation refused as"
             " SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED (the harness controls its own command"
             " lines; the refusal tells the operator to quote). A live doc ambiguity"
             " (path-carrying extensionless with an .exe sibling under the unquoted rule)"
             " is refused by name rather than guessed. Governs mbcx01_smoke_cell.py, which"
             " is a pinned subject deliberately OUTSIDE the module registration - the"
             " BI-12 convention: no modules field."),
    "positive": [WR + "test_bi20_guard_the_refusal_cannot_eat_a_shape_that_works"],
    "requirement": ("Every documented CreateProcessW resolution rule is either implemented"
                    " or refused by name: .exe appended to a BARE extensionless token only;"
                    " path-carrying tokens verbatim with no fallback; the six-step bare-name"
                    " search including the 16-bit System directory; App-Paths never"
                    " consulted (asserted mechanically); unquoted-whitespace paths refused"
                    " SMOKE_UNQUOTED_SPACE_PATH_UNSUPPORTED (codex r7 P1/P2 + the set"
                    " members nobody reported)."),
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
