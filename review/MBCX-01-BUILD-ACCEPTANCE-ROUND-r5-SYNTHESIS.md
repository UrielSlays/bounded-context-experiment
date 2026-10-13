# MBCX-01 BUILD acceptance round r5 — synthesis

Round complete at **3/3, every verdict EXECUTED**. Second complete round in this lane.

| Seat | Verdict | Ruled | Did NOT rule |
|---|---|---|---|
| SEAT1 Opus 5 | GO-WITH-FIXES(COMMITTED-KEY-HARVEST-SCOPE · CEREMONY-CARRIER-DISCLOSURE) — *conditional NO-GO if read as authorising the ceremony* | items 1, 4-inverse, 5, 7 | items 2, 3, 6 (said so plainly) |
| SEAT2 ChatGPT Sol | NO-GO | items 1–7 | — |
| SEAT3 codex-exec | NO-GO | items 1–7 | — |

**Outcome: NO-GO, folded.** All four classes are now closed at `5269375`.

⭐ **The filter worked.** §0 of the r5 packet required every finding to name how it makes the
experiment produce a wrong number, admit wrong evidence, or refuse right evidence. Every finding
returned did so. Zero findings this round were hardening against an actor evading a check — the
failure mode that cost r1/r2/r3 three rounds and nine verdicts.

⭐ **Two seats converged independently on three classes.** Model-diverse convergence on one class is
as strong a signal as disagreement (ANTI-DRIFT §1, the #509 lesson), and it held here.

## What the round found, and why each one matters to the DATA

The driver read the design of record IN FULL after this round opened (it had only been grepped
before — a real gap, recorded). That read changed the framing: closure-architecture §7 makes the
physical claim a **DIFFERENCE** — max-minus-min retired instructions across the four H values
against a **500,000** threshold. So an attribution error does not merely perturb a figure; it can
flip a carrier's BOUNDEDNESS verdict, which is the experiment's actual answer.

Every fold discharges a line the DoR already required — verified at the byte:

| Fold | DoR line it discharges |
|---|---|
| thread/process interval containment | closure-architecture:100 — *"containment gaps ... fail loud"* |
| TID reuse, one lifetime per use | closure-architecture:74 — *"process/thread QPC lifetimes"* |
| the binder | closure-architecture:79 — *"PID/start-key/TID attribution"* |
| committed-key harvest | closure-architecture:83 — *"Fixture keys structurally cannot authenticate physical evidence"* |

1. **Interval containment — ADMITTED WRONG EVIDENCE (the serious one).** `bind_thread_start_keys`
   documented a "PID *and* QPC interval" bind but only ever read `kind == "START"`, so ProcessStop
   was never consulted. Driver-reproduced: incarnation AA alive 10–40, BB alive 60–90, a thread
   claiming 50–55 — when neither was alive — ADMITTED against AA. SEAT2 carried the same shape
   through the **signed production path** to `production_admission_errors = []`.
2. **TID reuse — REFUSED RIGHT EVIDENCE.** Windows permits thread-ID reuse after termination
   (Microsoft primaries opened by two seats). The assembler, `consume_cswitch` and the **frozen**
   evaluator all assumed global TID uniqueness, so an ordinary capture on an ordinary machine was
   thrown out whole.
3. **RFC 7468 carrier — REFUSED RIGHT EVIDENCE.** CRLF / CR / absent-final-EOL forms of the *same
   decoded key* were refused; OpenSSL parses them; on Windows CRLF is native. The owner's real root
   key could have been refused at ceremony activation.
4. **Committed-key harvest — ADMITTED WRONG EVIDENCE (SEAT1 alone).** The refused set selected on a
   `.fixture.json` **filename suffix**, so `MBCX-01-R13/R12-MEASUREMENT-TRUST-ROOTS.json` — committed,
   publishing a key whose private half is committed in the test modules — could sign production
   measurement evidence. Differentially executed: fixture-document key refused, this one `errors=[]`.

## The two seat conflicts, and how the driver ruled them

⛔ Not averaged. Both resolved at the byte by the driver.

**(a) Normalize the PEM line endings, or don't?** SEAT2 + SEAT3 said normalize; SEAT1 said do NOT —
"that would loosen a check to fix a documentation gap." **Driver ruled WITH 2/3 and AGAINST SEAT1**,
on the merits: key identity is computed from the DECODED key, so EOL normalization cannot admit a
wrong key, while refusing CRLF can block the ceremony. SEAT1's *other* half was ADOPTED — the
ceremony doc gap and the uninformative refusal code are real and are tracked
(`MBCX01-R5-CEREMONY-DOC-STALE-AND-SILENT-ON-CARRIER`). The witness `bw62` re-runs every
pre-existing refusal through the new spellings, proving nothing else got weaker.

**(b) Is the frozen-count guard a defect?** SEAT3 executed a wholly replaced 147-test suite through
it and it PASSED. SEAT1 called it clean, because byte identity lives in the pin manifest. **Both are
right about different things**, confirmed at the byte: `verify-build-bundle.py` does NO byte-checking
of frozen modules (its only digest work is JSON parity), so the BUNDLE alone is blind; the separate
pinned run does bind bytes. Resolved to the already-tracked owed bundle arm, not a new class — and
the r5 packet's own item-7 claim was FALSE as written (recorded as a driver defect).

## The tar-pit call

The committed-key class appeared for the **THIRD** time (committed anchor key → committed test
signing key → this). ANTI-DRIFT §1 and TAR-PIT both say stop folding instances at the third and go
one level up. The driver's first instinct was the total complement — *"a production key must not
appear ANYWHERE in this repository"*, i.e. a repo-wide key census.

⛔ **The owner stopped that, and was right:** *"don't start building fucking crazy machinery and shit
that tries to protect a scientific experiment that actually has no adversary."* The actor here is an
operator copying a committed template during a one-time supervised ceremony — a footgun, not an
adversary. **The close is a SUBTRACTION: the filename filter WAS the defect, so it was deleted**
(5 → 6 keys). The remainder — a key published only in prose or a witness bank — is NAMED at the
finding site and tracked, not chased. Recorded as standing law:
`no-adversary-means-delete-a-restriction-not-add-a-scanner`.

## Gates after the fold

BUILD **130/130** · frozen **150/150** · `verify-build-bundle.py` REAL exit **0** · ledger **48
invariants / 130 witnesses**, `two_way_total: true` · readiness unchanged
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. `FROZEN_TEST_TOTAL` 147 → **150**, declared
with its reason at the constant. AMENDMENT-2 records the frozen-layer change.

**Driver verification, independent of every builder:** each red re-run with the pre-fix module proven
in play by hash before the red was accepted; each green re-run on the driver's own probes, including
the check that matters for a loosening fix — **overlapping lifetimes for one TID still fault**, so
only the wrong thing was loosened.

## Honest ceiling

- The consumer has **still never executed against a live ETW session**. A green suite means the logic
  is right *if the platform behaves as documented*.
- One of AMENDMENT-2's three frozen witnesses is a **guard, not a red** (it passed pre-fix); the
  builder said so rather than claiming 3/3 reds, and it is tracked.
- The frozen witnesses drive a **private seam**, not the signed envelope path — tracked.
- **codex-CLI has never run on this lane.** It is the last local gate and it is still owed.

## What r5 did not touch

Machine-wide Kernel-Process provider (smoke-run blocker, tracked) · exactness suite runner (unbuilt,
non-claimed) · `ProcessTelemetryIdInformation = 64` (smoke-stage check) · witness `ba28`'s 2027-08-13
expiry. None was promoted, because no seat could show any of them corrupting a number.
