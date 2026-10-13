"""Assembly: repair-ledger rows for the codex r9 folds (driver-owned edit)."""
import json

PATH = "MBCX-01-BUILD-REPAIR-LEDGER.json"
led = json.load(open(PATH, encoding="utf-8"))
inv = led["invariants"]
WSI = "test_mbcx01_build_state.BuildAStoreIdentityBeforeWriteWitnesses."
WSA = "test_mbcx01_build_state.BuildAStateAuthorityWitnesses."
WRE = "test_mbcx01_build_integration.SmokeRuntimeEnvironmentEvidenceWitnesses."
WFC = "test_mbcx01_build_integration.SmokeFixedCandidateIdentityWitnesses."
SRC = ("codex-CLI r9 fold set (MBCX-01-CODEXCLI-r9-FULL-LOG-2026-08-17.log; four P2"
       " findings, all red-first; the dispatched IsProcessorFeaturePresent candidate was"
       " REFUTED at the Learn byte and WMI HypervisorPresent adopted instead, 2026-08-17)")

def wits(prefix, names):
    return [prefix + n for n in names]

inv["BA-26_STORE_IDENTITY_IS_SETTLED_BEFORE_ANY_WRITE"] = {
    "adversarial": wits(WSI, [
        "test_ba52_red_another_stores_bytes_are_identical_after_the_refusal",
        "test_ba52_red_a_headerless_database_of_this_application_is_never_adopted",
        "test_ba52_red_an_older_schema_version_is_refused_before_it_is_migrated",
        "test_ba52_harness_the_bound_module_is_the_one_this_witness_names",
    ]),
    "modules": ["mbcx01_build_state_store.py"],
    "note": ("The headerless red was STRONGER than the report: pre-fix the open SUCCEEDED"
             " and returned a live store holding another store's committed journal row."
             " Post-DDL checks retained (they cover :memory: and freshly stamped files)."),
    "positive": wits(WSI, [
        "test_ba52_guard_right_paths_are_still_opened_and_still_reopened",
    ]),
    "requirement": ("open_verified settles the persisted store identity THROUGH THE"
                    " NON-WRITING DOOR before any journal-mode change or DDL: a"
                    " same-application store with different identity, an older schema"
                    " version, or a headerless database with rows is refused by name with"
                    " the file byte-identical after the refusal (codex r9 P2)."),
    "source": SRC,
}
inv["BA-27_READONLY_DOOR_VALIDATES_THE_REQUIRED_SCHEMA"] = {
    "adversarial": wits(WSA, [
        "test_ba51_red_a_truncated_store_is_a_verdict_not_a_raw_sqlite_error",
    ]),
    "modules": ["mbcx01_build_state_store.py", "mbcx01_build_state_authority.py"],
    "note": ("Refused at the store's read-only DOOR (STORE_REQUIRED_TABLES,"
             " STATE_STORE_SCHEMA_INCOMPLETE), not by widening the boundary tuple - the"
             " boundary's own honesty constraint forbids answering 'your receipt is"
             " malformed' when the truth is 'I could not read my own store'. The red"
             " found TWO escape sites (:842 journal, :868 transaction_rows); the door"
             " closes both. Declared limit: a door, not a TOCTOU shield."),
    "positive": wits(WSA, [
        "test_ba51_guard_the_untruncated_store_is_untouched_by_the_new_door",
    ]),
    "requirement": ("The read-only store view validates the required table set at open,"
                    " so a truncated database that passes identity signals yields the"
                    " closed transaction-identity refusal + sentinel from the public"
                    " verifier, never a raw sqlite3.OperationalError (codex r9 P2)."),
    "source": SRC,
}
inv["BI-17_ENVIRONMENT_EVIDENCE_IS_RUNTIME_OR_UNDETERMINED"] = {
    "adversarial": wits(WRE, [
        "test_bi24_red_installed_but_inactive_components_are_not_a_running_hypervisor",
        "test_bi24_red_a_guest_is_not_a_root_partition_because_the_role_is_installed",
        "test_bi24_red_an_unanswerable_probe_is_undetermined_not_bare_metal",
    ]),
    "note": ("Split by axis: hypervisor-present = REAL runtime probe"
             " (Win32_ComputerSystem.HypervisorPresent, Learn-quoted in-module;"
             " IsProcessorFeaturePresent REFUTED - PF_HYPERVISOR_PRESENT does not exist,"
             " 21 is PF_VIRT_FIRMWARE_ENABLED); root-vs-guest = honest relabel"
             " (INSTALLED_COMPONENT_EVIDENCE, falsifiable by running guest integration"
             " services, never provable - residual stated in-module). Live-verified on"
             " the build host: the owner's own run classifies HYPER_V_ROOT_PARTITION,"
             " nothing walled. Governs mbcx01_smoke_cell.py - BI-12 convention, no"
             " modules field. UNVERIFIED_UNTIL_ELEVATED_RUN: the WMI probe adds one"
             " abort path (HYPERVISOR_RUNTIME_POSTURE_UNDETERMINED) that has never"
             " fired in an elevated session; it aborts before any ETW/Job work."),
    "positive": wits(WRE, [
        "test_bi24_guard_the_runtime_probe_is_expressible_on_this_host",
    ]),
    "requirement": ("Signed environment evidence is RUNTIME-backed or labelled"
                    " UNDETERMINED: hypervisor presence comes from a runtime WMI fact,"
                    " installed-component registry keys are recorded as installed-"
                    "component evidence by name and used only to REFUSE a root reading,"
                    " and an unanswerable probe aborts by name rather than signing a"
                    " bare-metal claim (codex r9 P2)."),
    "source": SRC,
}
inv["BI-18_FIXED_CANDIDATE_ID_CERTIFIES_ONLY_ITS_INVOCATION"] = {
    "adversarial": wits(WFC, [
        "test_bi25_red_a_different_invocation_is_not_this_candidate",
        "test_bi25_red_a_different_image_under_the_same_id_is_refused_too",
    ]),
    "note": ("Discriminator audit recorded (the #28 shadow): this refusal stops a LYING"
             " RECORD - an envelope certifying a different invocation under the fixed"
             " CMD-EXIT-0 identity - and the guard proves all five documented spellings"
             " of the owner's real invocation untouched (runbook default, FOLD-3B short"
             " form, the resolved absolute form, unquoted absolute, case/space"
             " variants). It fires in preflight before elevation and before any probe."
             " Governs mbcx01_smoke_cell.py - BI-12 convention, no modules field."),
    "positive": wits(WFC, [
        "test_bi25_guard_the_default_and_the_documented_variants_are_untouched",
    ]),
    "requirement": ("A fixed candidate identity certifies only the invocation it names:"
                    " a resolved image or argument set inconsistent with"
                    " SMOKE_CANDIDATE_ID's declared command line is refused"
                    " SMOKE_COMMAND_INCONSISTENT_WITH_CANDIDATE_IDENTITY before any host"
                    " work, naming the id and the differing axis (codex r9 P2)."),
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
