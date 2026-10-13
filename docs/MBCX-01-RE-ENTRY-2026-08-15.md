# MBCX-01 — RE-ENTRY, session close 2026-08-15

For a session that arrives cold. Read this, then **the GitHub issues** —
`gh issue list --repo <private-repo>` — which is where owed work now lives — **count them by
negation-of-closed, never trust a number written here**. Filed 2026-08-15: the original 16 (one for
EVERY not-closed row; **#1 is the next action**), then **#17–#22 = the ENGINE slices** (scenario
generator · carriers FD/FC/TN · grid runner · route client — the producing half of the instrument,
which is ZERO LINES; everything built to date is the verification half), then **#23 = the DoR
reconciliation sweep** (owner-ordered: the DoR needs amendments for what the build learned).
`MBCX-01-OPEN-ISSUES.json` (29 rows)
remains the DETAILED record: it carries the four fields and the executed evidence and it
reconstructs from the pin manifest, which an issue does not. ⛔ Nothing owed is off the board: the driver first filed only 13, holding three back as
"disclosure only" — an exemption he invented, when the playbook's only one is the theater carve-out.
If it is not CLOSED, it has an issue. Byte-check anything you act on. **Supersedes `MBCX-01-RE-ENTRY-2026-08-14.md`**
for state; that file's TRAPS section still binds and is not repeated in full here.

## ⛔ THE THING TO INTERNALISE BEFORE YOU TOUCH ANYTHING

**This is a scientific measurement instrument. It has NO adversary.** No network service, no
production runtime, no external submitter; every caller is the harness and its own tests. The design
of record carries no threat model — verify it yourself, one command from the repo root:

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
```

Zero hits. **The only test that matters: does a change stop the experiment producing a WRONG NUMBER,
admitting WRONG evidence, or refusing RIGHT evidence?** Anything else is out of model.

⛔⛔ **OWNER RULING 2026-08-15, verbatim:** *"don't start building fucking crazy machinery and shit
that tries to protect a scientific experiment that actually has no adversary."* When a class recurs
and you reach for the wholesale close, ask first whether the honest level-up is **DELETING a wrong
restriction** rather than adding a census/scanner. It was, twice. Standing law:
memory `no-adversary-means-delete-a-restriction-not-add-a-scanner`.

## ⛔⛔ REQUIRED BEFORE ANY WORK: READ THE DESIGN OF RECORD IN COMPLETION (OWNER-ORDERED 2026-08-15)

**This is a handoff REQUIREMENT, not advice. Before any packet, fold, issue, or answer in this
lane, read ALL of the following in full — grepping does not count:**

1. `MBCX-01-EXPERIMENT-DESIGN-r9.md` (74 lines)
2. `MBCX-01-R10-ARCHITECTURE-SPEC.md` (104 lines — normative per the design's own authority order)
3. `MBCX-01-R13-CLOSURE-ARCHITECTURE.md` (118 lines)
4. `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`
5. Both frozen amendments: `MBCX-01-R13-AMENDMENT-1-*` and `MBCX-01-R13-AMENDMENT-2-*`

⚠ **And know the DoR's own limits before trusting a sentence in it:** the build has since
falsified some of its statements (e.g. closure-architecture §6 "the physical harness remains
absent" — the ETW consumer and Windows producer now exist), and the lane learned requirements the
DoR never states (the machine-wide Kernel-Process provider constraint, the unpublished platform
ordinals). **The reconciliation sweep is issue #23** — a DoR sentence about *build state* is
checked against #23 and the issues before it is relied on; the DoR's *scientific* content
(estimand, 768, gates, inference) stands frozen and is not in question.

**Why this rule exists — the driver's own paid lesson:** I drove four folds while having only
*grepped* the design and closure architecture, reasoning instead from the invariant matrix (which
is DOWNSTREAM of them). The owner caught it.

What the read changed, and it is not cosmetic: **closure-architecture §7 makes the physical claim a
DIFFERENCE** — max-minus-min retired instructions across the four H values, per fixed (D,F), against
a **500,000** threshold. The thesis is that work stays BOUNDED as history grows. So a
misattributed thread does not merely perturb a figure — **it can flip a carrier's boundedness
verdict, which is the experiment's actual answer.** Judge every future change against that, not
against generic correctness.

Also load-bearing from the DoR: authority order puts the **pin manifest ABOVE the design docs**
(design r9 §"Authority order"); there is **one terminal look** at 768 pairs, family error 0.05,
noninferiority margin −0.10, OM floor 0.80 — one shot, no second run to fix a bad instrument with.

## Where the lane is

**Branch `codex/mbcx01-production-build`. ⛔ RESOLVE HEAD, never trust a pinned value in this doc** —
`git rev-parse --short HEAD` and `git rev-parse --short origin/codex/mbcx01-production-build`; they were
equal at session close. (A HEAD written into prose goes stale within hours; this lane has already been
bitten twice by stale pins.) The last content commit of the r5 arc was `5269375`; everything after it is
records, ledger and the regenerated pin manifest. **The remote now exists** —
`<private-repo>`, PRIVATE, owner-named 2026-08-15; both branches pushed and
verified off-box (`git ls-remote` matches local). The single-disk risk is discharged and the `@codex`
bot gate is reachable for the first time.

Gates: BUILD **130/130** · frozen **150/150** · `verify-build-bundle.py` REAL exit 0 (48 invariants /
130 witnesses, `two_way_total`) · readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
**Zero spend, zero provider calls, no ceremony, no experiment.**

**TWO frozen-layer AMENDMENTS now exist**, both owner-ruled, both documented:
- `MBCX-01-R13-AMENDMENT-1-CANONICAL-WORLD-BINDING-2026-08-15.md` — the canonical world binds
  `subject_id` + `owner_role` (145 → 147 frozen tests).
- `MBCX-01-R13-AMENDMENT-2-THREAD-IDENTITY-AND-PEM-TRANSPORT-2026-08-15.md` — a thread's identity is
  its TID **and** its interval; RFC 7468 transport spelling is not key identity (147 → 150).

`FROZEN_TEST_TOTAL` is the DECLARATION mechanism for a frozen change. It is at 150 with its reason
recorded at the constant. ⛔ Raising it is never routine maintenance.

## Councils: two complete rounds, both NO-GO, both folded

**r4** (3/3 EXECUTED): I02 underbinding in the frozen layer, trust-root identity computed over the
key's *spelling*, three ETW defects, a committed test signing key clearing production. All folded.
**r5** (3/3 EXECUTED): interval containment admitting an impossible thread/process relation, TID
reuse falsely refused, RFC 7468 carriers falsely refused, and the committed-key harvest keying on a
filename suffix. All folded at `5269375`.

Verdicts banked: `MBCX-01-BUILD-SEAT{1,2,3}-*-VERDICT-r{4,5}.md`. Syntheses:
`MBCX-01-BUILD-ACCEPTANCE-ROUND-r{4,5}-SYNTHESIS.md` — the r5 one records BOTH seat conflicts and how
the driver ruled them at the byte rather than averaging.

## Do this next, in this order

1. **codex-CLI to GREEN — issue #1.** It has **NEVER been run on this lane** and it is the last local gate.
   `codex exec -m gpt-5.6-sol -c service_tier=default -c model_reasoning_effort=xhigh`. ⛔ SERIALIZE —
   never alongside a codex-exec seat; two heavy runs exhausted the org TPM bucket once and killed
   both with no verdict. ⛔ `exit 0 ≠ reviewed`: read the log tail and grep for real errors before
   calling it green (⚠ and grep PRECISELY — a bare `429` pattern matches line numbers; this session
   raised a false alarm that way).
2. **Draft PR into Selene + `@codex review`.** Owner has authorised the PR and said *"green without a
   CI"* — the destination has no workflows, so nothing billed fires. Pre-PR gate is council-GO +
   codex-GREEN; the merge stays owner-only.
3. **The elevated smoke run — issue #2** — owner action, still outstanding, and now gated behind
   **issue #3** (`MBCX01-SMOKE-MACHINE-WIDE-KERNEL-PROCESS-PROVIDER`): the consumer enables Kernel-Process
   machine-wide with no member filter, so on a non-idle host foreign processes' thread events fault
   and the run is expected to ABORT. Settle that before spending an elevated session.

## Traps (2026-08-14's still bind; these are NEW)

- ⛔ **PROVE YOUR HARNESS BEFORE BELIEVING ITS VERDICT.** Two of my own verification harnesses were
  wrong before they were right, and both wrong answers looked exactly like real findings: (a)
  `PYTHONPATH` loses to `unittest`, which puts the repo dir at `sys.path[0]`, so the "pre-fix" module
  never loaded and every witness PASSED — reading as *the red is fake*; (b) a control run from the
  wrong cwd threw `FileNotFoundError` on a relative fixture path and read as *42 tests broken*. Print
  the imported `__file__` **and a hash**, assert the intended copy won, assert inputs resolved
  non-empty (an EMPTY derived set makes a red fake), and diagnose ONE traceback before reporting a
  class. Memory: `prove-the-harness-before-believing-its-verdict`.
- ⛔ **A seat's `wait_quiesced` can return the PREVIOUS round's verdict.** Seat 2 returned its r4
  verdict verbatim while `state: generating` on r5. Check the COMMIT the verdict names, not the shape
  of the text. Banking that would have folded the wrong round's findings.
- ⚠ **The manifest records LF blobs; `core.autocrlf=true` checks the 32 frozen deps out as CRLF.** A
  manifest-freshness arm written against the WORKING TREE would false-fire on all 32 — read blobs via
  `git cat-file`, not the tree. (SEAT1, unprompted; carried on the pin-manifest row.)
- ⚠ **Regenerate the pin manifest after ANY content commit** — it bit twice now, including in the
  commit that added the warning.

## ANTI-DRIFT §1 audit of the session that produced this state

Run at closeout, at the byte. Recorded because a fresh session should inherit what went wrong here,
not just what got built. **Most of these were caught by the OWNER or by a SEAT, not by me** — which
is the honest headline.

**FIRED — claim outran its witness (×4).** Three packet claims I wrote were falsified by execution:
r4 §14 "no BUILD source changed after the pin" (false — `mbcx01_build_win32.py` at `0521752`);
r5 item 7 "the guard fails on any frozen-suite change" (false — a replaced 147-test suite passes);
and I repeated the fold's own docstring claim "PID + QPC interval" without checking the code, which
never read ProcessStop. Fourth: I reported "14 open" from a status-string prefix match when 16 were
owed. All four are issue **#16** / the standing memories.

**FIRED — stale bytes (×2).** The pin manifest governed a commit four behind the reviewed bytes for
the whole r4 round; the re-entry doc pinned a HEAD that went stale inside the same session. Both
fixed; the doc now tells you to RESOLVE HEAD rather than trusting a written value.

**FIRED — self-inflicted machinery / a machine the product never needed.** I was one step from
building a repository-wide key census to close the third instance of the committed-key class. The
owner stopped it. The honest level-up was a SUBTRACTION — delete the filename filter — not a
scanner. Standing law: `no-adversary-means-delete-a-restriction-not-add-a-scanner`.

**FIRED — a green nobody aimed at (×2, both caught by others).** Witness `bw28`'s variant was
constructed from `public_key_identity`, the normalizer under test, so it could only ever confirm its
own fixed points (SEAT1 found it). One of AMENDMENT-2's three frozen witnesses is a GUARD, not a red
— it passed pre-fix (the builder disclosed it rather than claiming 3/3 reds). ⚠ **And name what the
mechanical green does NOT cover:** `packet:check` passed GREEN on both the r4 and r5 packets, and
BOTH carried false claims. Shape-green is not truth-green — its own header says so.

**HANDLED CORRECTLY — three partial fixes is one habit.** The committed-key class hit its third
instance and the fold stopped closing instances and went one level up. That is the rule working.

**HANDLED CORRECTLY — a seat verdict is a pointer, including the GO.** Every finding acted on was
re-derived by the driver at the byte before it entered a synthesis or a commit — including running
my own probes rather than the builder's, and including the check that a loosening fix demands
(overlapping TID lifetimes still fault).

**HANDLED CORRECTLY — seat conflicts.** Two genuine conflicts (normalize PEM EOL or not; is the
frozen-count guard a defect). Both resolved at the byte with a named winner, neither averaged.

**NOT FIRED but LIVE FOR YOU:** the *diff-scoped reviewer cannot discharge a class-closure claim*
symptom. codex-CLI has not run yet. When it does, its green covers the LINES THAT CHANGED — it is
not evidence that any class is closed across all sites. Do not let a green CLI stand in for the
council's closure claim.

**CONTEXT.** The session that produced this state ran very long. §0 says pull the playbook out
proactively when that happens, because context rot precedes the window filling. Starting fresh here
is the correct call, not a formality.

## Claim ceiling — unchanged and still true

The BUILD's verification half is exercised and clean-room reproducible. **The MEASUREMENT half has
never executed a single instruction against a live ETW session.** A green suite means the logic is
right *if the platform behaves as documented*; it does not mean the consumer works. Several constants
are flagged in-source as unverified and the Kernel-Process provider identity has no Microsoft page —
every one of them faults loudly rather than degrading to a number, which is the property that makes
the smoke run safe to trust.
