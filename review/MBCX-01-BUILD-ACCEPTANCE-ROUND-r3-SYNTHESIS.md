# MBCX-01 BUILD acceptance — round r3 synthesis (driver)

Status: round CLOSED **NO-GO**, and — more important than the verdict — **THE STOP RULE FIRED.**
Recorded 2026-08-14. **No fold #3 was dispatched.** BUILD acceptance remains WITHHELD; the class is
escalated to the owner as a SCOPE decision (`OPEN-OWNER-DECISIONS` row 68). The r13.2 experiment
design remains CONFIRMED and untouched (145/145 frozen, zero frozen files modified across all folds).

Pins: packet `e2e6c662` · code `aa3d0b1a` · manifest blob `3e2a6753` · fold under review `e89168b5`.

## 1. Verdicts

| Seat | Verdict | What it varied |
|---|---|---|
| SEAT1 Opus 5 Extra (<council-browser-port>) | **GO** | The committed fixture key first (the knob it missed at r2); every context constructor; the freeze on five axes; the whole r2 set re-run under a real context |
| SEAT2 ChatGPT Sol (<council-browser-port>) | **NO VERDICT — seat capability failure** | Every Moonwalker call failed at the MCP boundary with `Unknown tool`; it refused to manufacture a verdict (correct). Logged to `Dogfood.md`. |
| SEAT3 codex-exec sol/xhigh | **NO-GO — 3 Critical** | The same `object.__setattr__` sequences SEAT1 found — but ruled them IN scope, and drove them to full admission |

**The round is INCOMPLETE on 2/3 (SEAT2 blocked) and is NOT rolled on for acceptance.** It is
nonetheless DECISIVE against the fold, because a constructed EXECUTED bypass outranks a pass over
ground the bypass was never run against (§3 ladder), and the driver reproduced the bypass.

## 2. The disagreement, and why the NO-GO governs

Both seats found the SAME two sequences (`object.__setattr__` on the anchor / on a built context).
They split on SCOPE, not on fact:

- **SEAT1** listed them as A7/A9, called them out of scope under the fold's own declared T2 ceiling
  ("an adversary who can define a Python class in the verifier's process is already past the
  api-caller-via-DATA boundary"), and returned GO.
- **SEAT3** answered that the exclusion is incoherent, in one sentence that settles it:
  *"The same callback capability cannot be in scope when it invokes the public rewire function but
  out of scope when it invokes `object.__setattr__`."*

**SEAT3 is right, and the packet's own text is the proof.** Claim C-R3-2 explicitly puts
caller-supplied objects WITH BEHAVIOUR (`.get`, `__getitem__`, `__iter__`, `__eq__`, properties) in
scope — and the entire r2 freeze rider exists to defend against exactly such an object. Once a
behaving object is admitted, its callback runs arbitrary Python, including `object.__setattr__`.
You cannot admit the callback and exclude what the callback may do. Either behaving objects are out
of scope (and then the freeze rider was defending a non-threat), or they are in scope (and then
"immutable context" is not a defence, because Python cannot make it one).

Python's own documentation is the external anchor SEAT3 cited: frozen instances only *emulate*
immutability; true immutable Python objects cannot generally be created.

## 3. Driver reproduction at the byte (LAW ZERO — run before this was written)

Both mechanisms reproduce against the pinned bytes, at the fold's own single resolution point:

```
PATH 1 — object.__new__ + object.__setattr__, then the PUBLIC installer:
  configure_production_verifier_context(hand-built ctx carrying the COMMITTED FIXTURE anchor) -> ACCEPTED
  resolve_production_verifier_context(MEASUREMENT) -> code=None (i.e. VALID FOR PRODUCTION)
                                    ctx anchor = MBCX01.BUILD.OWNER.ANCHOR.FIXTURE.1, fixture_only=True

PATH 2 — mutate a LEGITIMATE installed context in place (the F2 shape):
  before mutation: MBCX01.LEGIT.OPERATOR.ANCHOR.1
  after  mutation: MBCX01.BUILD.OWNER.ANCHOR.FIXTURE.1  fixture_only=False  resolve code=None
  the installed production root is now the COMMITTED fixture key: True
```

**Why PATH 1 matters most:** the fixture refusal lives in `ProductionVerifierContext.__init__`, but
`configure_production_verifier_context` admits any object that merely passes `isinstance`. So the
refusal is reachable-around by construction, not "structural" as the class docstring claims. The
same docstring's promise — *"Nothing that runs later in that evaluation can change the answer"* — is
falsified for the context's CONTENTS by PATH 2.

⚠ **SEAT1's B3 check was too weak, and this is the transferable lesson:** it verified the wiring
OBJECT IDENTITY was preserved across a failed verification (`before is after = True`). SEAT3 mutated
the CONTENTS of that same object. Identity preserved ≠ semantics preserved.

SEAT3's other findings, not reproduced individually but recorded: F3 (overlapping thread scopes
restore the WRONG global on exit — the unsafe direction SEAT1 did not test; consistent with the
driver-confirmed fact that `threading` is never imported and `_VERIFICATION_DEPTH` is a plain module
int mutated with `+=`), F4 (exactness reads caller-controlled receipt fields BEFORE resolving the
context — clock steering), F5 (validity endpoints disagree across doors), F6 (internal prior art
missed), F7 (the "totality" claim is syntactic, not semantic).

## 4. ⛔ THE STOP RULE FIRED — why there is no fold #3

ANTI-DRIFT §1: *"FOUR PARTIAL FIXES IN A ROW IS NOT FOUR MISSES — IT IS ONE HABIT… when the count
reaches three, stop folding entirely — the problem is no longer the code, it is that your closes are
being scoped by whoever reported the bug. The honest move at that point is one level up (the door,
the API, the contract), and if that is bigger than the slice it is an OWNER call, never a fold."*

The count is three, and each close was scoped by the report that produced it:

1. **r1 fold** — the caller supplies its own trust root ⇒ added an operator-supplied anchor.
2. **r2 fold** — our own committed fixture material is a root ⇒ added a fixture refusal + an
   instance-scoped context + a wiring freeze.
3. **r3 would be** — the caller's behaving object edits the anchor/context around those checks.

Every round the adversary is the SAME (a caller-supplied object with behaviour reaching authority
state); every fold closed the instance that round reported. TAR-PIT Q3 says the instance set here is
UNBOUNDED — the space of Python sequences an untrusted object's callback can execute is not
enumerable — so per-instance work cannot terminate. And the fold's own machinery is now authoring
the findings (ANTI-DRIFT §1 self-inflicted machinery: the freeze rider added at r2 is what F3
probes at r3).

## 5. The one-level-up close, and why it is NOT the driver's to take

**The wholesale close is the DOOR CONTRACT, expressible as a COMPLEMENT (TAR-PIT Q4):**
*every production door accepts exactly one thing — INERT DATA (values that survive a JSON
round-trip into exact built-in containers) — and refuses everything else at the door, before any
authority state is read.* Behaving objects then cannot reach the authority at all; the gadget class
dies wholesale rather than one sequence at a time; and much of the current defensive machinery (the
freeze, the emulated immutability) becomes deletable — findings flipping from "add X" to "delete X"
is the convergence signature we have not seen in three rounds.

This is ADOPTED, not invented: it is parse-don't-validate, it is `serde`'s `deny_unknown_fields`
shape, and this repo already holds the pattern twice (`seal-chain.ts`'s own-key walk with the
ownKeys↔descriptor cross-check for lying proxies; `authorization-json.ts:rejectUnknownKeys`).
**Codex proposed exactly this at r2** ("inert bytes or a verified immutable model at the trust
boundary") and the r2 fold DEFERRED it, in the worker's own words, as *"a larger interface change
than this issue's spec."* That deferral is what bit at r3.

**Why it is an OWNER call (TAR-PIT Lesson 14):** it changes the PUBLIC CONTRACT of all three
production doors on a lane whose next gates are a physical smoke run and a key ceremony, and it is
bigger than the slice that spawned it. A wholesale close bigger than the slice is a scope decision,
not a fold. ⚖ It also gives fresh weight to SEAT3's standing dissent — twice now — that this
trust-bootstrap layer never had its own design gate.

⚠ **REACHABILITY, unchanged from r2 and stated so the owner can size the risk honestly:** none of
this is reachable by an api-caller today, because there is no production runtime — every installer of
production/fixture material is fixture, demo, test or verifier code, and readiness is
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. The exposure begins at the ceremony.

## 6. What is genuinely CLOSED and must not be re-ground

- **The r1 class** (a caller supplying its own trust root, without the anchor key): closed, and
  confirmed by three independent constructions across r2/r3 — SEAT1's and SEAT2's fresh-key
  universes at r2, SEAT1's re-run under a real context at r3, plus the driver's probes.
- The seven activation splice axes incl. the same-`manifest_id` mutation; all four carrier
  spellings (C-R3-5 passes per SEAT3 too); the r1 false-REJECT repair; fail-closed-when-unanchored;
  the exactness binding-only labelling (C-R3-4 passes per both seats).
- Suites: BUILD 95/95, frozen 145/145, `verify-build-bundle.py` exit 0, clean-room reconstruction
  COMPLETE at `aa3d0b1a` — all re-run by the driver.

## 7. Not authorized by this round (unchanged)

No experiment, no provider/model calls, no route qualification or freeze, no physical grid, no
Job/ETW collection, no signing ceremony, no spend.
