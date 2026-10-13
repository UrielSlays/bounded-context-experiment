---
title: "MBCX-01: a preregistered experiment, built and verified, waiting on a paid call"
subtitle: "The design, the review record, the build, and where it stands on 26 September 2026"
author: "Clinton Cuzzort"
date: "2026-09-26"
---

## In one paragraph

MBCX-01 is the identifier of an experiment about long-running software agents. It asks whether one agent can keep every obligation it has taken on, exactly, while the work it does at each step stays bounded by what is live at that moment. The design went through fifteen rounds with three independent reviewers and was frozen with a pinned test bundle. The two production authorities the design needs were then built and verified. Several things stand between today and a paid run. The experiment's own subject, the three carriers, is unbuilt. So are the 100-cell grid runner, the provider route client and the per-witness exactness runner. The one-cell smoke proof has not run. A review gate is still owed on the current bytes. After those come the physical gates, the route gate inside an approved ceiling, and the owner's two approvals. Every number in this document comes from files in this repository or from its git history. The experiment itself has not run. No model or provider call has been made.

## The hypothesis under test

The research question, as the design of record states it, has three parts.

1. Can one logical conductor preserve exact due-obligation continuity while its physical work remains bounded by the active decision frontier, across the full frozen ranges of history length, dependency depth and fact count?
2. If so, which carrier does it: a frontier digest, a frontier cache, or temporal normalization?
3. Conditional on a carrier passing every deterministic gate, can a frozen model working from bounded context perform without material loss against the same model working from an oracle-memory packet?

In plain words, an agent that has been running for a long time carries a growing record of what it promised, what it did, and what it learned. The experiment tests whether an agent handed a small, exact slice of that record at each step performs without material loss against an agent handed the ideal slice, where material loss is a registered margin of 0.10. The three carriers are three ways of building that small slice. The deterministic gates check that a carrier is exact and that its cost stays bounded before any model is asked anything.

The design names the ways the run can end: carrier rejection, design or implementation failure, transport inconclusive, model or interface ceiling, model or interface failure, promotion to the coordination stage, or scientifically inconclusive. It says in so many words that more calls are not an automatic escape from any of them.

## The method: what one run is

![Figure 1. The registered experiment, before a single model call.](figures/fig1-registered-experiment.svg)

The cohort is frozen before anything else. A generator produces 960 candidate scenarios. Eligibility is recomputed after one cut, and any eligibility flag supplied with a candidate is discarded. The retained cohort is exactly 768 scenarios, 128 from each of six motifs.

Each scenario becomes one pair. The bounded-context condition, BC, gives the model the object set the candidate carrier selected. The oracle-memory condition, OM, gives the model the object set the independent gold read-set selected. Both conditions share the scenario, the cut, the observation, the action universe, the neutral schema, the instructions, the descriptions, the padding, the output schema and the transport settings. They differ in one thing, which is how the object set was chosen. One population rule was added by owner-ratified amendment on 16 August 2026: scenarios in which a scored target is reopened are excluded from this experiment by the generator, and measuring that class is the declared follow-up, MBCX-02, conditional on a positive primary result.

Each condition runs three model nodes in series: A0, then B, then a writer step, then a cold A1. That is six scheduled call positions per pair and 4,608 for the run. The design caps retries separately, outside the call count, under a retry policy that is frozen at authorization.

There is one scientific look, at 768 complete or worst-case-resolved pairs. The family error is 0.05 across the two result streams. The noninferiority margin is -0.10 and the oracle-memory floor is 0.80. Missing transport outcomes can end as transport inconclusive. Schema-invalid model output is an observed failure and never counts as missing.

Before the science comes reliability. The route is qualified by 456 independent six-call trials. Each trial runs under an endpoint, a model snapshot, an authentication path, transport settings and a retry policy, all frozen at authorization. The route passes at four or fewer failed trials. That rule accepts a route with a 2 percent failure rate with probability at most 0.0495 and passes a route with a 0.5 percent failure rate with probability at least 0.919. Both bounds are rounded outward from the values in the inference contract.

Before reliability comes physics. Every carrier is measured over 100 cells: four history lengths by five dependency depths by five fact counts. For each fixed depth and fact count, the spread across the four history lengths is checked against six limits: 500,000 retired instructions, 75 million nanoseconds of CPU time, 75 million nanoseconds of elapsed time, 64 mebibytes of peak committed memory, 16 mebibytes of I/O transfer and 4,096 I/O operations. Missing evidence, an unsupported counter, trace loss or unverified external work fails the gate loudly.

The decision order is registered. Step one reconstructs the bundle from pinned git objects. Step two requires no blocking council defect. Step three runs the four physical gates: exactness, complete accounting, boundedness and affordability. Step four runs the route gate, inside a ceiling the owner has approved. Step five is the owner's explicit authorization of the paid run. Step six runs the frozen experiment once and publishes every registered result. Steps one and two have passed. Steps three to six have not run.

## How the design got frozen

![Figure 2. Every round, every seat, until three seats said the same thing.](figures/fig2-council-verdicts.svg)

Each revision of the design went to three reviewer seats at once: a Claude seat, a ChatGPT seat and a Codex seat that executes code. Round one's ChatGPT verdict is not banked. Round eight's two browser verdicts survive as an aggregate. Each seat reads the pinned bytes and runs its own probes. Each returns its verdict before it sees the other seats' verdicts; from round seven the two browser seats kept their own thread across rounds by owner ruling, so the seal is between seats, never across rounds. Three reports had that seal breached: the ChatGPT report in round three, the Claude report in round five and the ChatGPT report in round thirteen. Each was kept as technical evidence. None was counted as an independent vote. A round advances on evidence. One executed falsification controls the gate, whatever the other two seats said.

The design took fifteen rounds, from 11 to 14 August 2026. Each round's synthesis lists what the seats found and what was adopted. Round two listed 23 findings and adopted 18. Round three listed 22 and adopted 16. Round five listed 20 and adopted 17. Round six folded 25 demonstrated defects as five repair classes and declined three scope items. From round seven on every listed finding was repaired before the next round: 11, 12, 13, 14, 7, 13, 6, 3 and then 0. Rounds one and four have no banked count. Two rounds before the last had no NO-GO from any seat. The last round, r13.2, returned CONFIRMED from all three seats with no finding of any grade. The design of record at that point carried 34 pinned subjects, a clean-room reconstruction that passed 145 of 145 tests, 61 governed repair witnesses, and strict schema admission for every contract.

The reviewers changed the design. The sample size was chosen from 384, 512, 768 and 1,024 on a 10,000-replicate operating-characteristic study. At 768 pairs the four practical decision branches resolved correctly 99.76, 99.84, 99.72 and 94.30 percent of the time. At 384 pairs the same branches resolved about 56, 67, 50 and 39 percent of the time. The design makes no 90 percent promise in the numerical transition region, and it guarantees no decision at the margin of 0.10 or at the floor of 0.80; those figures describe the practical branches. The thresholds themselves carry no such promise. The reliability gate was rebuilt. The r8 design needed 98,868 route-soak calls to certify a route with zero failures at every position. The registered design certifies the route with 2,736 calls through a binomial gate with stated error rates. The contracts were versioned eight times for state, seven for packets, seven for measurement and eight for inference. From round ten on, each round's versions are pinned by git blob in that round's manifest; rounds eight and nine have no pin manifest.

## What was built, and how it was proven

![Figure 3. The witness suite grew under review while the frozen core held.](figures/fig3-suite-and-gate.svg)

The build added the two production authorities the design required. The frozen instrument changed through declared, owner-ratified amendments alone. The amendments are listed below.

One authority owns state. It is a single-writer SQLite store, a file-based database, with write-ahead logging and full synchronous commits. It records the proposal, the child state and the snapshot in one transaction before any effect. It mints a signed receipt from a committed terminal alone. A second, independent operator with its own queries and its own hashing must agree byte for byte before a receipt counts.

The other authority owns measurement. It is a Windows Job Object and Event Tracing for Windows producer. It collects retired instructions, processor time, elapsed time, memory and input and output volume for a whole process tree. It signs the envelope with a custody-separated key and refuses fixture material at every production door. The real collector exists as reviewable code. It has never executed. It refuses to run unless an environment variable and an owner authorization file carrying a specific marker line are both present.

The build's witnesses were written red before green, with the exceptions the round records name as pins: a pin is a witness that already passed on the pre-fix bytes and was kept to catch a future silent change. The ledger of invariants grew from 34 rows and 76 witnesses at the content-final commit to 118 rows and 289 witnesses at the last fold, over three days. Each point on that line is a count of witness names in the ledger at that commit. The last point, 289, is the set the verifier runs today. A witness removed along the way, such as the wiring-freeze witness deleted in the revert at fd26275, is counted at the commits whose ledger names it and at no later point, and nothing was re-run at the historical commits for the figure. Most steps in that line are one fold from one review round; the others are the content-final commit, the trace-consumer build, the cohort engine slice and one revert, each named in the data record. The frozen suite started the build at 145 and ended at 156. After the freeze the frozen code files changed in four commits: the three owner-ratified amendments and the round-seven acceptance fold. Each of those raised the frozen test count on purpose, with the reason written at the constant the verifier checks. One further commit, on 16 August and ratified by the owner in its own message, amended three frozen documents and no test. Its six items: the physical harness is built and witness-covered but has never executed against a live trace session; the retained-set root is a flat list digest, a Merkle tree having been considered and declined; the authority order's concrete artifacts are superseded by the r13.2 closure while its principle stands; the trace provider is machine-wide and a capture on a busy host may abort, which is the correct loud outcome; scored-target reopen episodes are excluded from the population and deferred to MBCX-02; and motif content semantics belong to the cohort content design. No other commit touched a frozen file.

The build went through its own reviews. The three-seat acceptance council ran eight rounds. The Codex command-line gate ran nine rounds over the same code and returned 5, 7, 10, 6, 4, 5, 4, 3 and 4 findings, 48 in all, each graded P1 or P2 on the reviewer's own priority scale. All but one were folded red first, and each fold commit is named in the record. The exception was a round-four finding whose fix, an authorization gate, refused the owner's own run and was reverted in full. The ninth round returned P2 findings and no P1. A tenth round was not run.

One thing in the build record is a paid lesson. Build-acceptance rounds one to three reviewed the code against a declared adversary, an outside caller of an application programming interface, on a system that has no such interface. The declaration was inherited from round to round without a byte check. It cost three rounds, eight verdicts and one capability report, and a wiring-freeze mechanism was built for that phantom and then reverted. The owner caught it in chat. The correction is a file in this repository; it names the rider that was reverted, and the revert commit's message names the mechanism and its four call sites.

## Where it stands today

![Figure 4. Where the arc stands: the committed tracker of 15 August 2026 beside the live tracker of 26 September 2026.](figures/fig4-issue-ledger.svg)

On 26 September 2026 the repository was run from a clean clone of the production-build branch.

| Check | Result |
|---|---|
| Full test discovery | 601 tests, all passing |
| Frozen r13.2 suite inside the bundle verifier | 156 of 156 |
| Build suite inside the bundle verifier | 289 of 289 |
| Repair ledger totality | 118 invariants over 289 witnesses, two-way |
| Bundle verifier exit code | 0 |
| Readiness word printed by the verifier | BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED |

Two trackers exist. The committed tracker file is a snapshot from 15 August 2026, at commit 5269375. It carries 29 items: eleven closed or discharged, one void, one superseded, one half closed, fifteen open. The live tracker is the private working repository's issue list on GitHub, opened once the remote existed; as of 26 September 2026 at 10:11 UTC it holds 32 issues, 23 open and 9 closed; that listing is committed as docs/presentation/data/github-issues-2026-09-26.json. Thirty-one of the issues date from 15 to 17 August 2026. The thirty-second was filed on 26 September by the presentation work itself, a test-hygiene item (a temp directory the integration suite leaks on Windows) that sits outside the readiness sets named next. Read together they say this. Before the smoke proof: the elevated one-cell run itself, an owner action, and the machine-wide trace provider the consumer must scope. Unbuilt before the route gate: the per-witness exactness runner, the three carriers that are the experiment's subject, the 100-cell grid runner and the provider route client. A review gate on the current bytes is still owed. The other open items are named gaps, document fixes and residuals.

## Why it has not run

![Figure 5. What it costs to press go, in calls, and why the number is what it is.](figures/fig5-calls-and-cost.svg)

The design itself authorizes no model or provider call. The route gate at step four runs inside a ceiling the owner has approved, and step five is his separate authorization of the paid experiment run. Neither approval has been given, and no price, token ceiling, retry ceiling, endpoint or model snapshot has been frozen. The scheduled call count is fixed: 2,736 calls for the route gate and 4,608 for the experiment, 7,344 before the one look. The dollar figures in the figure are illustrative and are not part of the record.

The other reason is order. The carriers, the grid runner and the route client are unbuilt, and the physical gates need them and the smoke proof. The smoke proof needs an elevated run that the build deliberately cannot perform on its own.

## How to verify this document

Every claim above can be checked from a clone of this repository. Two observations are dated and would read differently on a later day, today's run and the live tracker's counts, so both are committed as snapshots under docs/presentation/data: suite-run-2026-09-26.log and github-issues-2026-09-26.json. The commands below were the ones run on 26 September 2026.

```
python -m unittest discover -s . -p "test_*.py"
python verify-build-bundle.py
```

In this public copy the verifier stops at its first check: the pin manifest names a governing commit of the private working repository, and this copy's history cannot resolve it. One of the 601 tests, bc14, exercises that same check and fails here for the same reason; the other 600 pass. The measured-state numbers above come from the working repository's run of 26 September 2026, committed byte-exact at docs/presentation/data/suite-run-2026-09-26.log.

The pinned reconstruction authenticates its own launcher from a git blob. It rebuilds every subject into a temporary directory and checks blob identity, byte count, line-ending count and the SHA-384 digest for each. After those checks it runs the verifier inside the reconstruction. The command is:

```
powershell -NoProfile -ExecutionPolicy Bypass -File verify-build-pinned.ps1 -Commit <commit> -ManifestBlob <blob>
```

The figures are regenerated by the commands below. The renderer is the one thing here that needs a package outside the standard library.

```
python -m pip install -r docs/presentation/requirements.txt
python docs/presentation/make_figures.py
```

The data behind the figures is `docs/presentation/data/mbcx01-record-2026-09-26.json`. Each block in it names the file it was read from, with line ranges where a range exists, or says that it was derived by counting. The council's three round-one verdicts, banked beside the packet, re-derived the ledger series, the gate counts, the seat tables and the banked-file hashes.

## What has not run

- The experiment, and every model or provider call.
- The 456 route-qualification trials.
- The 100-cell physical grid.
- Any real Job Object or trace collection.
- The one-cell smoke proof.
- The signing ceremony and any trust-root activation.
- The per-witness exactness suite on the physical stage.
- A tenth Codex gate round.

The signing keys in this repository are test fixtures generated for the suite. They hold no production authority. Each production door the build enumerates refuses them, and the suite exercises each door. The trust anchor's own docstring names one accepted gap: a committed test private key whose public half appears in no committed document is outside its census, because deriving a public key from a private one needs an Ed25519 implementation the module does not carry.

## Sources in this repository

- `MBCX-01-EXPERIMENT-DESIGN-r9.md`, the design of record's prose.
- `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`, the physical gates and the closure architecture.
- `MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md`, the build commission and the r13.2 confirmation.
- `MBCX-01-COUNCIL-R*-SYNTHESIS*.md` and `MBCX-01-BUILD-ACCEPTANCE-ROUND-r*-SYNTHESIS.md`, the round records.
- `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`, the correction.
- `MBCX-01-BUILD-REPAIR-LEDGER.json`, the invariant ledger, at every commit in the branch history.
- `docs/presentation/data/codex-gate-findings-2026-09-26.md`, the final findings block of each of the nine gate logs, excerpted; the raw logs are withheld from this public copy.
- `MBCX-01-OPEN-ISSUES.json`, the tracker.
- `MBCX-01-BUILD-SMOKE-RUNBOOK.md`, the runbook for the authorized smoke proof.
