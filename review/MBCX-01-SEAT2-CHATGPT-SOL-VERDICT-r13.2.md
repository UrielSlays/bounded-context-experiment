# MBCX-01 SEAT2 (ChatGPT GPT-5.6 Sol) verdict — r13.2 — banked verbatim from the live seat thread

> Banked 2026-08-14 by the BUILD-lane driver from conversation `<id>`
> (CDP <council-browser-port>, the conversation named in `MBCX-01-COUNCIL-R13.2-DISPATCH-RECEIPT.json`), read-only
> attachment, `wait_quiesced` capture (state `indeterminate/lineage-unavailable` — expected: the
> banking session did not send the dispatch; text was settled and terminal). Reply text below is
> verbatim.

---

MBCX-01 r13.2 — Targeted Closure Confirmation
CONFIRMED

EXECUTED. All three targeted r13.1 repairs hold under fresh adversarial execution against the pinned r13.2 bytes. I found no P0–P3 defect in C1, C2, or C3.

Conceptual council rounds should stop. The next authorized work is the two separately reviewed BUILD artifacts—not experiment execution.

Seat / seal

Model: GPT-5.6 Sol
Harness: ChatGPT + Moonwalker MCP + native web
Posture: longitudinal; prior own-lane r13.1 context used as explicitly permitted.
r13.2 lateral seal: HELD. I did not inspect any other r13.2 seat chat, output, log, marker, or verdict.

No provider/model calls, paid inference, experiment, physical harness, 100-cell physical grid, route qualification, or production adapter was run.

Pin and reconstruction

Governing commit:

d97d654e21918450994cfddb5a53dc5da2e962bb

Pin manifest:

407a1cd73197af7dbad767976f5c077d91986c87

Pinned launcher:

1bb8c15d1fd14303fa0a10fa615a881cb65e0d96

I extracted the launcher from its Git blob before execution. Fresh authentication returned:

LAUNCHER_HASH=1bb8c15d1fd14303fa0a10fa615a881cb65e0d96

The authenticated reconstruction verified 34 exact subjects and passed:

145 unit tests

61 governed repair witnesses

strict Draft 2020-12 AJV admission

all 768 retained-source joins

connected pipeline

provider_calls: 0

paid_calls: 0

experiment_executed: false

physical_harness_executed: false

The changed implementation, tests, contracts, and exactness-suite working files I read also matched their pinned commit:path blobs.

C1 — EpisodeReceipt → outcome authority
HOLDS

I constructed two independently valid complete episodes for the same retained scenario.

Episode A:

episode validation = []
outcome = (1, 1)

Episode B used a separately durable BC A0 response whose scorer graph genuinely derives zero:

episode validation = []
outcome = (0, 1)

Both were internally valid and their episode_hash values differed.

Then I presented B's fully formed ScenarioOutcomeReceiptV2 against episode A:

['SCENARIO_OUTCOME_AUTHORITY_INVALID']

I also drove the inference API with 768 retained scenarios, with A as the one complete episode:

inference(A) = TRANSPORT_INCONCLUSIVE

inference(B outcome against episode A)
= ValueError SCENARIO_OUTCOME_AUTHORITY_INVALID

inference(A again)
= TRANSPORT_INCONCLUSIVE

So B cannot silently change the inference result over A.

The load-bearing implementation is mbcx01_r13_packets.py:1212–1388: ScenarioOutcomeReceiptV2 carries the exact episode hash and six ordered ledger/call-record bindings; validation reconstructs and compares the full durable-call lineage before recomputing the bits. mbcx01_r13_inference.py:168–191 selects the exact episode by scenario before admitting the outcome.

C1 confirmed.

C2 — TotalTerminatedProcesses
HOLDS

I reopened the governing Microsoft primary source this session. Microsoft defines the four DWORDs in the expected order and defines TotalTerminatedProcesses specifically as processes terminated because of a Job limit violation, while TotalProcesses includes processes associated during the Job lifetime.
learn.microsoft.com

Fresh clean-normal-exit attack

Signed fixture:

TotalProcesses               = 1
ActiveProcesses              = 0
TotalTerminatedProcesses     = 0
terminal lifetime status     = EXITED

Result:

['PHYSICAL_HARNESS_UNAVAILABLE']

No Job-accounting failure. Correct.

Fresh limit-violation attack

I changed only the fourth DWORD/scalar to:

TotalTerminatedProcesses = 1

rebuilt the raw 96-byte query, hashes, signed preimage, and fixture signature.

Result:

['JOB_QUERY_EVIDENCE_INVALID',
 'PHYSICAL_HARNESS_UNAVAILABLE']

The relevant pinned evaluator at mbcx01_r13_measurement.py:783–794 now compares the real four-DWORD ABI and explicitly requires total_terminated_processes == 0 for a clean admitted cell. Normal completion remains proven separately through signed member lifetimes and final ActiveProcesses == 0.

C2 confirmed.

C3 — Carrier exactness authority / exact-build binding
HOLDS

Baseline fixture exactness against its own signed 100-cell grid:

_valid_exactness_receipt = True
measurement grid = ['PHYSICAL_HARNESS_UNAVAILABLE']
Fresh self-authored PASS attack

I replaced the exactness suite and witness-set digests with attacker-chosen SHA-384 values and repaired receipt_hash.

Result:

_valid_exactness_receipt = False

derive_engineering_candidate_evidence(...)
= ValueError ENGINEERING_SELECTION_INVALID
Production relabel attack

I changed:

authority_mode = PRODUCTION
trust_root_id   = ATTACKER.ROOT

and repaired the receipt hash.

Result:

_valid_exactness_receipt(... production ...) = False

derive_engineering_candidate_evidence(...)
= ValueError CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE

There is no r13.2 label-based production activation path.

Cross-artifact replay

I built a second internally valid, fully re-signed 100-cell grid with a different candidate_artifact_digest.

The second grid remained valid except for the deliberate physical sentinel:

['PHYSICAL_HARNESS_UNAVAILABLE']

Its grid identity differed from the first.

Replaying the first grid's exactness receipt:

_valid_exactness_receipt = False

derive_engineering_candidate_evidence(...)
= ValueError ENGINEERING_SELECTION_INVALID
Cross-harness-build replay

I separately rebuilt all 100 signed cells with another consistent harness_build_digest.

Again:

new grid valid except physical sentinel
grid identity changed
old exactness receipt valid = False

The pinned CarrierExactnessReceiptV2 implementation at mbcx01_r13_measurement.py:1546–1630 binds the exact pinned suite/witness hashes, carrier artifact, complete measurement-grid identity, fixture producer, and fixture authority mode. Production authority is deliberately unavailable until the physical BUILD supplies a reviewed production verifier.

C3 confirmed.

Findings

P0: NONE
P1: NONE
P2: NONE
P3: NONE

I found no reachable false result introduced by these three repairs.

The two standing red statuses remain exactly the published BUILD boundary:

STATE_AUTHORITY_UNAVAILABLE
PHYSICAL_HARNESS_UNAVAILABLE

They are not r13.2 defects.

Build-decision challenge

ALREADY-BUILT? — EXECUTED / SEARCHED. The underlying primitives already exist—Windows Job accounting and Moonwalker's receipt/operator-separation patterns—but the exact episode/outcome join and MBCX production authority receipts are experiment-specific. I spot-ran the pinned shelf query and opened docs/167-3b-live-wiring-DESIGN-v14-2026-08-05.md:596–616; its independent receipt, supervisor-owned Job, and authority-separation patterns remain appropriate to reuse rather than reinvent.

PRODUCT-FIT? — YES. These repairs preserve fail-loud governed measurement: uncertainty or absent external authority stays red instead of becoming evidence.

BIGGER-THAN-THE-BUG? — NO. r13.2 consists of three bounded authority/semantic corrections. It did not create another subsystem or change the experiment.

SEARCHED external sweep

Query:

site:learn.microsoft.com JOBOBJECT_BASIC_ACCOUNTING_INFORMATION TotalTerminatedProcesses limit violation

Opened Microsoft's governing structure documentation; it directly settled C2, so further secondary sourcing was unnecessary.
learn.microsoft.com

Direct answers

Are the three r13.1 fixes actually closed?
Yes. C1, C2, and C3 all HOLDS under fresh execution.

Can conceptual council rounds stop now?

Yes.

I see no evidentiary basis for r14 or another conceptual closure round.

Is the next authorized step BUILD rather than experiment execution?

Yes.

The next work is exactly:

Production state-owner adapter/store/readback authority BUILD

Production Windows Job/ETW evidence producer + custody-separated signing BUILD

Those BUILD reviews do not authorize the 100-cell physical run, 456 route trials, 4,608 scientific calls, provider calls, or spending.

Side effects / cleanup

Repository edits: NONE
Commits/pushes/labels: NONE
Provider/model calls: NONE
Paid inference: NONE
Experiment calls: NONE
Physical execution: NONE

Transient authenticated launcher: removed.
Transient verifier report used for checking: removed.
No verdict artifact was written.

Final: CONFIRMED — stop conceptual rounds and move to the two BUILD gates.
