# MBCX-01 BUILD acceptance round r8 — synthesis, and the ROUND-SHAPE ruling that ends the arc

Round complete at **3/3, every verdict EXECUTED**. Fifth complete round on the BUILD; third
today. Packet `dc06bae`; review target `575fb38`.

| Seat | Verdict | Rulings |
|---|---|---|
| SEAT1 Opus 5 | GO-WITH-FIXES(LEAF) | **4 ACCEPT** · omission attack EMPTY · withdrew its own r7 F6 |
| SEAT2 ChatGPT sol | NO-GO | 2 ACCEPT / 2 CHANGE (member-foreign overlap · fence not yet exact) |
| SEAT3 codex-exec | NO-GO | 2 ACCEPT / 2 CHANGE (fence not yet exact · amendment prose contradicts its own bytes) |

**Outcome: the four fold surfaces are CONFIRMED. The remaining findings are folded here, and
the COUNCIL ARC CLOSES — r9 is refused, on the round-shape rule, not on fatigue.** Reasoning
below; it is the load-bearing part of this document.

## The round-shape ruling (ANTI-DRIFT §1 + TAR-PIT Lessons 9–11)

**Every finding in r7 and r8 targeted machinery the PREVIOUS round's fold invented.** That is
not convergence; §1 names it: *"YOU are authoring the next round's findings — self-inflicted
machinery in the fold… Test at every fold: did this round's findings target something I
INVENTED last round? If yes, REVERT it, don't complete it."*

| Round | Findings landed on |
|---|---|
| r6 | the codex r1–r3 folds + AMENDMENT-2 (prior work) — and found a REAL million-instruction wrong number |
| r7 | AMENDMENT-3 (invented at the r6 fold) · `foreign_thread_intervals` (r6 fold) · the pwsh fence allowance (r6 assembly) — found a REAL signable undercount |
| r8 | the stop-only prefix (r7 fold) · the fence regex (r7 fold) · the amendment prose (r7 fold) · a fault name (r7 fold) — found **one real consistency gap, one doc defect, and a third round on our own test fence** |

The product-defect yield went `1 severe → 1 severe → 0`. The *detector* yield went
`0 → 1 → 2`. That crossover is the exact signature of TAR-PIT Lesson 11: *"consecutive reviews
stop finding product defects and start finding COVERAGE GAPS in your own detector."*

### TAR-PIT triage, run ON THE FENCE (3rd appearance of the class — trigger long since fired)

- **Q1 REACHABILITY → THEATER.** Reaching it takes a maintainer editing our own suite. Both
  dissenting seats said so unprompted ("no hostile actor is needed"). Nothing ships behind it.
- **Q2 DATA vs CODE → CODE-ONLY.** No untrusted data path exists; this lane has no threat
  model at all.
- **Q3 BOUNDED vs UNBOUNDED → UNBOUNDED.** The instance set is *the space of PowerShell
  payload strings*: script-name suffixes, trailing statements, quoting, metacharacters,
  newline smuggling. r7 closed two shapes; r8 produced two more in one round; the next round
  produces two more. A coverage claim over it is falsifiable forever.
- **Q4 WHOLESALE CLOSE → yes, and it is a DELETION.** Not a better regex: *stop claiming to
  adjudicate the payload.* The fence's finite, derivable job is the EXECUTABLE SET.
- **Q5 PRIOR ART → n/a** (our own harness).

**Matrix row THEATER ⇒ accept the residual, name it, ZERO GRIND.** Executed: the argv regex is
DELETED, `pwsh` joins the enumerated executable set, and the claim is narrowed at the site and
in the module docstring to what is actually enforced — *the executable set, not the arguments*
— with the residual named in-place. This also discharges memory
`no-adversary-means-delete-a-restriction-not-add-a-scanner`: on a no-adversary artifact, one
level up from an enumeration is DELETING the wrong restriction, not tightening it.

⚠ **Distinguish from TAR-PIT Lesson 6** (never refuse to close a named reachable bypass): a
coverage gap in a TEST-SIDE fence ships nothing. Every product bypass this arc found is closed.

## Folded here (the real remainder — all cheap, none re-rounding)

1. **Member/foreign TID interval overlap** (SEAT2 F1, EXECUTED) — a TID claimed alive as both
   member and foreign at one instant is a contradictory trace and now fails loud by name
   (`ETW_THREAD_MEMBER_FOREIGN_INTERVAL_OVERLAP`) instead of being silently resolved
   member-first. **bw92, RED on hash-proven pre-fold bytes** (consumer blob `48feb3bc`: the
   overlap was admitted, both records kept). Platform-impossible input — a consistency gate
   between two of our OWN derived structures, written at correctness volume, no adversary
   implied. bw91's disjoint arrangement verified unaffected in the same witness.
2. **The amendment's own prose contradicted its bytes** (SEAT3 F2, byte-confirmed by the
   driver) — `AMENDMENT-3 §4` still described the pre-totality contract ("empty baseline list
   — first delta 0 accepted"), and TWO source comments still said capture-start emits "no
   row". All three corrected. **These were mine, written at r6 and not updated when r7 moved
   the behaviour.** The seats caught the prose; the code was right.
3. **`ETW_THREAD_ROSTER_ROW_INVALID` was unwitnessed** (SEAT1 F6) — now pinned by **bw93,
   labelled a PIN and not a red**: driver-verified passing on the pre-r8 bytes, because the
   r7 fold already emitted the name. Its job is a future silent rename.
4. **SEAT1's r7 F6 withdrawn on the record** — the r7 synthesis now carries the withdrawal
   above the adjudication it confirms, so the banked verdict stops carrying a phantom.

## Conflicts, adjudicated — named winners

- **The fence (SEAT2 CHANGE / SEAT3 CHANGE / SEAT1 ACCEPT):** both CHANGE seats are FACTUALLY
  RIGHT — the regex does admit `evilrun-smoke-cell.ps1` and a trailing `; Write-Output EXTRA`
  (SEAT1 found the same trailing-tail hole and classed it a residual). **Neither remedy is
  adopted, and the disagreement is not averaged:** the driver rules the CLASS out of scope by
  the TAR-PIT matrix above and removes the claim instead of chasing the shapes. Named winner:
  the protocol, over three seats' shared instinct to close it better. This is precisely
  Lesson 9 — *"reaching for a cleverer mechanism on a theater-lane class is the grind in a
  tuxedo."*
- **Item 1 totality (ACCEPT 3/3, unanimous):** SEAT1 ran 190 randomised truthful captures with
  zero would-be false refusals; SEAT2 confirmed the producer `TypeError` before signing and
  found no pacifier `()` at any constructor; SEAT3 confirmed refusal on removing any row.
  **AMENDMENT-3's shape of record is settled and all three seats support ratification (#27).**
- **Item 2 prefix interval:** SEAT1 built the worst case (a prefix covering the member's whole
  life) and the member branch still won every contained record with the total exactly ground
  truth. SEAT2's overlap case is the one gap and is folded above.

## Convergence signature (ANTI-DRIFT §1) — read honestly

1. **Findings flipping to "delete X / already right":** YES — the round's own strongest seat
   withdrew a finding, and the driver's ruling on the biggest remaining item is a deletion.
2. **Seats describing the same fixed point:** YES on items 1, 2-core and 4 (unanimous ACCEPT).
3. **Omission attack empty:** SEAT1 YES, explicitly. SEAT2/SEAT3 returned only the fence and
   the overlap — both now closed.

All three hold at the product layer. What remains open is a residual we NAMED rather than a
defect we missed.

## What this arc actually bought (so the cost is on the record)

Five acceptance rounds and three codex rounds closed: a silent 1,000,000-instruction
undercount that signed and cleared full production admission; a signable empty-baseline
ambiguity; two false refusals that would have destroyed a one-shot elevated capture (TID
reuse, machine-wide scope); an unverified-event-version decode; a presence-only smoke
criterion; a lost-capture-on-signer-failure ordering. **Those are real, and the instrument is
materially better.** The last round bought one contradiction gate and a prose fix — which is
the signal to stop, and we are stopping.

## Next, in order

1. **codex-CLI r4 to literal GREEN (#1)** — the last local gate; serialized, sol at xhigh.
2. **Draft PR into Selene + `@codex review`** (owner-authorised; destination has no workflows).
3. **#27 ratification** rides the PR — all three r8 seats support the amended draft.
4. **Then the ENGINE (#17–#22)** — the carriers FD/FC/TN and the 768-scenario generator, which
   are the experiment's actual subject and are still zero lines.
