# MBCX-01 — RE-ENTRY, session close 2026-08-16

**Supersedes `MBCX-01-RE-ENTRY-2026-08-15b.md` for STATE.** That file's traps still bind and are
not repeated. Byte-check anything you act on.

---

## ⛔⛔⛔ STANDING ORDER — THE FIRST WORK OF THE NEXT SESSION (owner, 2026-08-16)

Owner, verbatim, twice in one session:

> *"Bro, you better not be building a fucking security product here. There better not be any
> adversaries, any advanced blocking, treating the owner as a hostile... like, this is a research
> harness bro. It needs to be output accurate data. that's not what's happening."*

> *"read your canonical artifact for antidrift. You need to search the chat and find all of the
> issues. They all need to be rebite verified. in the next session. with... should they even be
> issues? Did we fucking build shit that's not supposed to be here? Refucking read the d o r. Stop
> fucking building security mechanisms. For attackers that do not exist."*

**THE ORDER, in four parts. Do these BEFORE any new build, any council round, any codex gate:**

1. **Re-read the DoR IN FULL** — `MBCX-01-EXPERIMENT-DESIGN-r9.md`, `MBCX-01-R10-ARCHITECTURE-SPEC.md`,
   `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`, `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`, amendments
   1–3. Grepping does not count. Read `ANTI-DRIFT-PLAYBOOK.md` §1 too.
2. **BYTE-VERIFY EVERY ISSUE** on the board (§"The audit" below enumerates all 29 — do not re-search
   the chat, the list is here and `gh issue list --state all` is the authority). For each: open the
   code it names and confirm the claim is still true at the byte. Several were written by a driver
   who had inherited a stale premise.
3. **APPLY THE DISCRIMINATOR TO EACH ONE, and to the machinery already built:**

   > **Does this stop the experiment from producing a WRONG NUMBER, admitting WRONG EVIDENCE, or
   > refusing RIGHT evidence? — or does it stop a PERSON from doing something?**
   >
   > If it stops a person, and that person is the owner running his own harness: **DELETE IT.**

4. **Then the ENGINE (#17–#22).** The experiment's actual subject — the FD/FC/TN carriers and the
   768-scenario generator — is **ZERO LINES** (driver byte-verified 2026-08-16: no carrier file, no
   carrier class, no generator). Everything built so far is the instrument that measures them.

⚠ **Some of the suspect machinery is DoR-MANDATED** (invariant matrix rows I13/I14: trust roots,
custody evidence, producer roles, "the signer must not control trust-root editing"). Deleting those
is not a fold — it is a DoR amendment, which is **#23** and the owner's ruling. Do not quietly
delete a DoR row; propose the amendment.

---

## ⭐⭐ AMENDMENT TO THE STANDING ORDER — OWNER-RULED 2026-08-16 (later session, live chat): THE ORDER IS INVERTED

The owner, after the DoR re-read (step 1) was completed in full: *"you tell me everything built to
the date is a referee for machines that don't exist, and you say we're gonna do that next, and then
you just keep on polishing the referee… a research harness that was supposed to be built still
isn't built."* Driver diagnosis, owner-confirmed with an explicit **"go"**: every gate in the loop
points at whatever EXISTS — the referee exists and the engine doesn't, so "audit first, then
engine" was the referee-polishing pattern wearing a discipline costume.

**The standing order's steps 2–3 (byte-verify every issue · discriminator audit) are DEMOTED from
a standalone first-work project to an ON-CONTACT RULE; step 4 (the ENGINE) is promoted to THE
FIRST WORK.** Binding form:

1. **ENGINE FIRST: #17 (scenario generator) → #18/#19/#20 (carriers FD/FC/TN) → #21 (grid runner)
   → #22 (route client, route-agnostic).** Zero spend, zero frozen files, unchanged.
2. **The discriminator applies ON CONTACT:** the moment any existing machinery refuses honest
   engine work, run it through *"does this stop a WRONG NUMBER, or does it stop a PERSON?"* right
   there — person + that person is the owner ⇒ DELETE (or propose via **#23** if the row is
   DoR-mandated). ⛔ No standalone referee-audit session is scheduled, ever, unless the owner
   re-orders one.
3. **⛔ NO NEW REFEREE MACHINERY** — unchanged, and now doubly binding: a codex/council severity
   label is not authority (the reverted authorization gate is the proof), and an idle loop pointed
   at a finished referee invents more referee.

Steps 1–4 above are PRESERVED as the record of the earlier ruling; this amendment governs on
conflict (newer owner byte wins, ANTI-DRIFT §3).

---

## What happened this session (short, and the honest part first)

**A gate got built that treated the owner as the adversary, and the owner caught it.** codex-CLI r4
returned a "P1" saying the collector accepted any authorization document that merely CONTAINED the
marker string, ignoring the command line and cell the document named. The driver took the framing
because it arrived with a severity label, and built a gate that **refuses the owner's own elevated
run unless the owner's own document names the exact command string**. It then proved its own harm
inside the same session: composed with the r4 candidate-resolution fold, it refused the runbook's
DEFAULT invocation (`cmd.exe /c exit 0` in the document vs the resolved
`"C:\WINDOWS\System32\cmd.exe" /c exit 0` handed to the gate). The driver's next move had been to
write plumbing to work around the machine it had just built.

**REVERTED IN FULL** at `24c7f17`: `_require_authorization` is back to the marker check it always
was; `authorization_gate_facts` became `authorization_mirror` (reads the document, REPORTS whether
it mentions the command line and cell beside what will run, **never raises, never refuses, returns
no verdict**); ten witnesses that existed only to prove the gate are deleted; #28 closed won't-do.

**The council arc also closed at r8** on the round-shape rule (ANTI-DRIFT §1 + TAR-PIT 9–11): every
r7 and r8 finding targeted machinery the previous round's fold invented, product-defect yield went
`1 severe → 1 severe → 0` while findings about our own test-side fence went `0 → 1 → 2`. The pwsh
spawn fence's argv-regex ambition was DELETED rather than tightened a third time. Full reasoning:
`MBCX-01-BUILD-ACCEPTANCE-ROUND-r8-SYNTHESIS.md`.

## Where the lane is

Branch `codex/mbcx01-production-build`, remote `<private-repo>` (private).
⛔ **RESOLVE HEAD** (`git rev-parse --short HEAD` vs origin) — never trust a SHA written in prose.
At close: local == origin == `24c7f17`.

Gates at that commit: BUILD **197/197** · frozen **156/156** · `verify-build-bundle.py` REAL exit 0
(ledger **79 invariants / 197 witnesses**, two-way total) · clean-room `verify-build-pinned.ps1`
→ `PINNED RECONSTRUCTION COMPLETE`. Readiness unchanged:
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. Zero spend, zero provider calls, no
ceremony, no experiment, no physical run.

**codex-CLI r4 ran and is NOT green** — 6 findings; 5 folded (data-accuracy), 1 reverted (the
authorization gate). A codex r5 has NOT been run. Do not run one until the audit above is done:
codex reasons in security terms and will keep proposing gates this harness does not want.

## The audit — all 29 issues, with a FIRST-PASS classification to attack, not to trust

The classification below is the outgoing driver's opinion and is itself a claim. Byte-verify it.

**🔴 SECURITY-SHAPED — audit first, default toward DELETE**
| # | What it is | Why suspect |
|---|---|---|
| 14 (closed) | Fixture-key gaps: a committed test key must not become a production root | Prevents a MISTAKE by the owner; no adversary. Closed, but the CODE it blessed is live |
| 15 | "Committed-key census is a directory scan, not a git-object read" | A **census/scanner** — the exact shape the owner's standing law names. Ask whether the census should exist at all |
| 5 | Ceremony doc stale / silent on carrier | Documents the key-custody CEREMONY; audit whether the ceremony is needed for a one-owner harness |
| 10 | AMENDMENT-2 frozen witnesses drive a private seam, not the signed envelope path | Signature-path machinery |
| 29 | Raw exceptions escape the closed-error-list contract at 4 sites | Robustness, not accuracy. May be over-built; filed by the outgoing driver |

**🟡 MIXED — real data concern wrapped in gate language**
| # | What it is | Note |
|---|---|---|
| 9 | Literal-LF PEM assumptions remain | Actually ANTI-blocking (stops a false refusal of a valid key) — probably keep |
| 25 | `sqlite3.OperationalError` escapes as a raw exception | Crash-honesty, mild |
| 13 | ba28 goes RED on 2027-08-13 | A dated landmine in a witness; housekeeping |

**🟢 DATA ACCURACY / THE EXPERIMENT — these are the point**
| # | What it is |
|---|---|
| **17–22** | **THE ENGINE: scenario generator, carriers FD/FC/TN, grid runner, route client — ZERO LINES** |
| 2 | The elevated smoke run — owner action, settles seven unverified platform facts |
| 3 | Machine-wide Kernel-Process provider — the smoke run may ABORT on a busy host |
| 4 | Cohort identity root moved with AMENDMENT-1 and nothing records it — owner ratifies the number |
| 7 | Exactness suite runner unbuilt — "exactness" is a binding claim with no execution behind it |
| 11 | Smoke fixture containment satisfied BY INSPECTION ONLY |
| 12 | `ProcessTelemetryIdInformation = 64` unpublished ordinal — verify before the first physical run |
| 27 | AMENDMENT-3 ratification — the first-member-interval undercount (a real wrong number) |
| 23 | **DoR reconciliation sweep — the HOME for any "this row should not exist" finding** |

**⚪ PROCESS / HOUSEKEEPING**
| # | What it is |
|---|---|
| 1 | codex-CLI gate state |
| 6 (closed), 8 (closed), 24 (closed), 28 (closed won't-do) | Discharged rounds/rulings |
| 16 | Standing behavioural correction (driver packet claims falsified by execution) |
| 26 | Relocate the lane out of Downloads to `source/Selene` |

## Machinery ALREADY BUILT that is NOT on the issue board — audit it too

The board does not list what was already built and blessed in earlier rounds. Put each of these
through the discriminator:

- **The whole production-admission / trust-root layer** (matrix rows I13, I14): trust anchors,
  custody evidence, producer roles, "the signer must not control trust-root editing", the
  `PRODUCTION_*_FIXTURE_KEY_MATERIAL` refusals, the committed-key harvest. **DoR-mandated ⇒ amend
  via #23, do not silently delete.** Ask plainly: in a harness one person runs on his own box, what
  does a trust root buy the DATA?
- **`ExecutionPosture`** in `verify-build-bundle.py` — blocks network calls and allowlists spawned
  executables during verification. Defensible on ONE ground only: it proves the no-paid-call claim
  (zero spend is a real experiment constraint). Keep it for that, and only that; its argv-shape
  ambition was already deleted at r8.
- **`STATE_STORE_IDENTITY_ALREADY_OPEN`** (new this session, BA-20) — refuses a second store taking
  a live store's identity. Justified as data accuracy (a committed transaction resolved to `None`),
  but it IS a new refusal. Re-check.
- **Fixture isolation** (I13/I16 — fixture material cannot create an experiment-eligible score).
  The outgoing driver would DEFEND this one: it stops test data becoming a published result, which
  is squarely "do not produce a wrong number."

## Kept from codex r4 (each is data accuracy, not access control)

- **BI-12** candidate image resolved once before launch, mirroring CreateProcessW/PATHEXT
  *[CORRECTED 2026-08-16, codex r6 F1: the PATHEXT half of this sentence was FALSE —
  CreateProcessW appends `.exe` only; extensionless resolution is `.exe`-only as of the r6
  fold, BI-14. RE-CORRECTED same day, codex r7: `.exe`-only holds for BARE tokens only —
  path-carrying extensionless tokens are verbatim; BI-16 owns the full documented set]*;
  the same image is hashed and launched. `cmd /c exit 0` previously **completed a real capture and then threw
  it away** at certification — right evidence refused, on the one-shot session.
- **BI-13** harness/candidate digests read and HELD before launch, so the envelope binds the bytes
  that actually produced the capture.
- **BA-19** identity signals read through a read-only connection before any PRAGMA — a foreign
  database was being **rewritten by the open that then refused it**; a tableless database with only
  a `user_version` was silently adopted.
- **BA-20** live store identity single-occupancy (see caveat above).
- **BA-21** malformed custody key list → named code, **scoped to ONE site on purpose**; the class is
  open at #29 and no row claims it closed.

## Traps (the older ones still bind)

- ⛔ **A pipe hides an exit code.** `git commit -m "…" | tail -2` swallowed a pathspec failure this
  session (nested double quotes broke the message); the fold landed under the NEXT commit's message
  with a stale pin manifest. Use `-F <file>` for multi-line messages and read the real `rc`.
- ⛔ **A probe that catches the wrong exception lies.** A driver reproduction caught an
  `AttributeError` (wrong API name) and reported it as a refusal. Assert the API exists before
  trusting a refusal.
- ⛔ **Shared scratch dirs poison harnesses.** Two workers collided in
  `…\scratchpad\prefix\`; a stale test-module copy won an import and produced six bogus failures.
  One private scratch dir per worker, containing ONLY the module under test.
- ⚠ Regenerate the pin manifest after ANY content commit, and run the clean-room via **pwsh 7**
  (Windows PowerShell 5.1 fails on `Get-FileHash`).

## Claim ceiling — unchanged

The verification half is exercised and clean-room reproducible. **The measurement half has still
never executed against a live ETW session.** Every unverifiable platform constant faults loudly by
name rather than degrading to a number — that property is what makes the smoke run safe to trust,
and the smoke run is still the only thing that can settle the rest.
