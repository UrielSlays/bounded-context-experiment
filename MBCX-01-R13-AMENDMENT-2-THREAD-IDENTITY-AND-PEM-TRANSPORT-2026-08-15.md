# MBCX-01 r13.2 — AMENDMENT 2: a thread is a TID **and an interval**; a PEM's newlines are transport

**Status:** ADOPTED. Owner-ruled in live chat 2026-08-15 — this defect class is an
AMENDMENT to the frozen layer, on the pattern AMENDMENT-1 set.
**Amends:** the frozen r13.2 layer (`mbcx01_r13_measurement.py`) and the BUILD lane
(`mbcx01_build_etw_consumer.py`, `mbcx01_build_win32.py`, `mbcx01_build_trust_anchor.py`).
This is the SECOND amendment to that freeze; AMENDMENT-1 (canonical world binding) stands
unchanged beside it.
**Origin:** three defects found by two independent council seats, then reproduced at the
byte by the driver before they were folded. Nothing here was inherited from a seat claim.

Three defects, and they point in **both** directions. The north star is that the numbers
are TRUE, and a measurement harness fails that twice over: by admitting evidence it should
refuse, and by refusing evidence it should admit. Defect 2 is the first kind. Defects 1
and 3 are the second — and a refusal that fires on a legal capture is not a safe default,
it is a silent ceiling on what the experiment can ever observe.

## 1. Defect 1 — a legal thread-ID reuse was FALSELY REFUSED

Windows is explicit that a thread id is not unique forever: *"the operating system may
reuse a thread ID after the thread has terminated"* (Learn, **PsGetThreadId** Remarks;
**Thread Handles and Identifiers**). Our code assumed a TID was unique within a capture in
three places:

| Layer | Byte |
|---|---|
| BUILD consumer | `mbcx01_build_etw_consumer.assemble_thread_lifetimes` keyed `starts`/`stops` by `thread_id` and raised `ETW_THREAD_LIFETIME_DUPLICATE_START:<tid>` on a second START |
| BUILD collector | `mbcx01_build_win32.consume_cswitch` built `{row["thread_id"]: row}` — one dict entry per TID, so a second lifetime silently replaced the first |
| FROZEN r13.2 | `mbcx01_r13_measurement._validate_physical_evidence` rejected a second lifetime with `thread["thread_id"] in thread_map`, then joined every observation by TID alone |

**Driver reproduction, pre-amendment** (two disjoint lifetimes for TID 77, 20..30 and
60..70, inside one process alive 10..100):

```
PROBE 1a: two DISJOINT lifetimes for TID 77 (20..30, 60..70) in process 10..100
  -> REFUSED  EtwConsumerFault ETW_THREAD_LIFETIME_DUPLICATE_START:77
PROBE 1b: each CSwitch observation resolves to the lifetime containing its QPC
  -> UNREACHABLE: 1a refused the roster, so no observation can be attributed
```

**Why it matters for the DATA.** A cell that reuses a TID is an ordinary long capture, not
a pathological one. Pre-amendment, that capture did not lose one delta — it lost the whole
receipt: the assembler faulted, so no retired-instruction total existed for that cell at
all. On the frozen side the same capture returned `INSTRUCTION_ACCOUNTING_INCOMPLETE`. The
harness would have refused true evidence and, worse, would have refused it more often the
longer and busier the cell — which correlates with the very conditions the experiment
varies (H, D, F).

## 2. Defect 2 — no process/thread interval containment (the one that ADMITS wrong evidence)

`bind_thread_start_keys` documented its own rule as a bind by *"PID **and** QPC interval"*
— and the BUILD ledger row BB-17 repeated that claim. The code read only
`kind == "START"` events and `continue`d past everything else, so **ProcessStop was never
consulted**; it picked the last start with `started <= qpc`. Nothing downstream re-checked
it: the frozen validator checked that `(process_id, process_start_key)` is a member pair
and that the thread's own interval is monotonic, never that the thread interval NESTS
inside the process interval.

**Driver reproduction, pre-amendment** (PID 5000, incarnation AA alive 10..40, incarnation
BB alive 60..90, thread 303 claiming 50..55 — when NO incarnation is alive):

```
PROBE 2a: -> ADMITTED  {'process_id': 5000, 'process_start_key': '00000000000000AA',
                        'thread_id': 303, 'started_qpc': 50, 'ended_qpc': 55}
PROBE 2b (FROZEN VALIDATOR, process 1..30, observations untouched):
  thread starts BEFORE the process  process 1..30 thread 0..29 -> errors []
  thread ends AFTER the process     process 1..30 thread 2..31 -> errors []
```

**Why it matters for the DATA.** This is the direction that corrupts a number instead of
losing it. A PID is reused, so a thread observed in the gap between two incarnations is
some *other* process's thread; binding it to the exited incarnation attributes a
stranger's retired instructions to a signed Job member and sums them into that cell's
total. The receipt stays signed, the roster stays complete, every existing check stays
green — and the reported instruction count is simply wrong, in a direction no downstream
consistency check can see.

**The docstring was part of the defect.** It asserted a property the code did not have,
which is how the hole survived review: a reader who trusted it had no reason to look. It
is corrected in the same commit, and so is the ledger row that inherited the claim.

## 3. Defect 3 — valid RFC 7468 PEM carriers were FALSELY REFUSED

`OwnerTrustAnchor.__init__` required `public_key_pem` to start with
`-----BEGIN PUBLIC KEY-----\n` and end with `-----END PUBLIC KEY-----\n`, and
`strict_public_key_carrier_ok` required literal-LF framing plus a final EOL. RFC 7468 §2
directs parsers to handle the differing newline conventions in use (CRLF, CR, LF), and its
§3 ABNF makes the EOL after the final boundary OPTIONAL. **CRLF is the native Windows line
ending**, and the custody ceremony (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0) has
a human hand-writing an anchor document on the operator's Windows box.

**Driver reproduction, pre-amendment** (one freshly generated, non-committed Ed25519 key):

```
  LF, final EOL present  (RFC 7468 §3)       identity=ED25519:19C6BB1178DB7FEF36D416...
      strict_public_key_carrier_ok : True     OwnerTrustAnchor(...) : CONSTRUCTED
  CRLF, final EOL present (RFC 7468 §2)      identity=ED25519:19C6BB1178DB7FEF36D416...
      strict_public_key_carrier_ok : False    OwnerTrustAnchor(...) : REFUSED OWNER_TRUST_ANCHOR_INVALID
  LF, final EOL ABSENT   (RFC 7468 §3 ABNF)  identity=ED25519:19C6BB1178DB7FEF36D416...
      strict_public_key_carrier_ok : False    OwnerTrustAnchor(...) : REFUSED OWNER_TRUST_ANCHOR_INVALID

what an independent RFC 7468 parser (openssl pkey -pubin) says:
  LF / CRLF / no-final-EOL : exit 0, exit 0, exit 0
```

Same key, same identity, three answers. **Why it matters for the DATA:** the ceremony is
the door every production number comes through. A refusal here does not produce a wrong
number, it produces NO numbers — and it produces them with a message ("owner trust anchor
invalid") that points the operator at their key rather than at our line-ending rule.

## 4. What is NOT claimed

- **No banked result changes.** No physical harness has ever run (`physical_harness_executed: false`,
  readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`), so there is no
  measured instruction total in existence that these rules could have altered. What was
  false is what the frozen validator and the BUILD consumer *would have done* to the first
  real capture, and what the anchor door *would have done* to the first real key.
- **No estimand, route, inference, cohort or n=768 change.** Nothing here touches the
  candidate world, the reducer, the scorer or the grid.
- **Not a security finding.** No threat model, no untrusted caller; this is
  scientific-validity work (`MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`).
- **No new subsystem.** Three functions gained an interval; two gained a named fault; one
  gained a text normaliser. No new state, no new evidence field, no schema change.
- **The base64/DER canonicality of a key carrier is NOT relaxed** — see §5, and bw62,
  which re-runs every pre-existing refusal through the new spellings.

## 5. The change

| File | Change |
|---|---|
| `mbcx01_build_etw_consumer.py` | new `process_incarnation_intervals()`; `bind_thread_start_keys` binds to the incarnation whose START/STOP interval CONTAINS the thread's QPC (none → `ETW_THREAD_START_KEY_UNBINDABLE`, two → new `ETW_PROCESS_INCARNATION_AMBIGUOUS`), and its docstring no longer claims a bind it does not perform; `assemble_thread_lifetimes` pairs starts/stops per TID in QPC order, permits DISJOINT reuse, and adds `ETW_THREAD_LIFETIME_OVERLAPPING_REUSE` and `ETW_THREAD_LIFETIME_OUTSIDE_PROCESS` |
| `mbcx01_build_win32.py` | new `resolve_thread_lifetime(lifetimes, tid, qpc)`; `consume_cswitch` joins by TID **and** QPC instead of one dict entry per TID |
| `mbcx01_r13_measurement.py` (FROZEN) | new `_process_intervals()`; `_validate_physical_evidence` keeps a LIST of lifetimes per TID, refuses overlapping/touching lives, requires every thread lifetime to nest inside its process incarnation, and resolves each observation by QPC containment |
| `mbcx01_build_trust_anchor.py` | new `normalize_pem_eol()`, applied in `OwnerTrustAnchor.__init__` (which stores the normalised carrier) and at the head of `strict_public_key_carrier_ok` — **before** every existing check, replacing none of them |
| `test_mbcx01_build_measurement.py` | **five new red witnesses** bw58-bw62 |
| `test_mbcx01_r13_measurement.py` | **three new frozen witnesses** (one of them a guard, see §6) |
| `MBCX-01-BUILD-REPAIR-LEDGER.json` | two new rows — `BB-18_THREAD_IDENTITY_IS_A_TID_AND_AN_INTERVAL`, `AB-11_RFC7468_TRANSPORT_SPELLING_IS_NOT_KEY_IDENTITY`; totals 46/125 → 48/130 |
| `verify-build-bundle.py` | `FROZEN_TEST_TOTAL` 147 → 150, reason recorded at the constant |

**Vocabulary discipline.** `ETW_THREAD_LIFETIME_DUPLICATE_START` is KEPT, narrowed to a
second START at the *same* QPC (a duplicated event, not a second life). The impossible
world — two lives of one TID overlapping or touching — gets its own name rather than
inheriting that one, because "you sent the same event twice" and "this TID was alive
twice" are different facts for whoever reads the fault.

## 6. Red witnesses (RED before the fix, GREEN after — the contract, not a formality)

The five BUILD witnesses and two of the three frozen witnesses were written and run
**against the pre-fix bytes** with the source files provably untouched
(`git diff --stat` empty on all four sources at the time of the run).

```
BUILD, pre-fix:  Ran 5 tests — FAILED (failures=20, errors=1)
  ERROR: test_bw58 ... EtwConsumerFault: ETW_THREAD_LIFETIME_DUPLICATE_START:77
  FAIL : test_bw59 (case='overlapping intervals') / (case='touching intervals share an instant')
  FAIL : test_bw60 ... ETW_THREAD_START_KEY_UNBINDABLE:5000@50 not raised
  FAIL : test_bw61 (CRLF / CR / no-final-EOL / CRLF-no-final-EOL)
  FAIL : test_bw62 (committed key re-spelled; every carrier mutant through CRLF and no-final-EOL)

FROZEN, pre-fix: Ran 3 tests — FAILED (failures=3)
  FAIL: test_i11_adversarial_thread_lifetime_outside_its_process_is_refused (starts before the process)
        AssertionError: 'INSTRUCTION_ACCOUNTING_INCOMPLETE' not found in set()
  FAIL: test_i11_adversarial_thread_lifetime_outside_its_process_is_refused (ends after the process)
        AssertionError: 'INSTRUCTION_ACCOUNTING_INCOMPLETE' not found in set()
  FAIL: test_i11_positive_a_reused_thread_id_carries_one_lifetime_per_use
        AssertionError: Items in the first set but not the second: 'INSTRUCTION_ACCOUNTING_INCOMPLETE'
```

```
BUILD, post-fix:  Ran 5 tests — OK
FROZEN, post-fix: Ran 3 tests — OK
```

**One of the three frozen witnesses is a GUARD, not a red**, and it is recorded as such:
`test_i11_adversarial_overlapping_lifetimes_for_one_thread_id_are_refused` passed
pre-amendment too — trivially, because pre-amendment *every* repeated TID was refused. Its
job begins now, when refusal is no longer automatic. Calling it a red witness would be a
false claim about what it discriminates.

**The standalone probes are reproducible after the fact.** Each loads the HEAD copy of the
module (`git show HEAD:<file>` into a scratch directory placed at `sys.path[0]`), PRINTS
and ASSERTS the imported module's `__file__` and SHA-256 against the HEAD blob hash, and
asserts that the function the fix introduces is ABSENT. Re-run after the fix landed, they
still produce the pre-fix reds above; run with `MBCX01_PROBE_POSTFIX=1` against the
worktree they produce:

```
PROBE 1a -> ADMITTED [77 20..30, 77 60..70]      PROBE 1c -> ETW_THREAD_LIFETIME_OVERLAPPING_REUSE:77
PROBE 2a -> REFUSED  ETW_THREAD_START_KEY_UNBINDABLE:5000@50
PROBE 2b -> ['INSTRUCTION_ACCOUNTING_INCOMPLETE'] in BOTH directions
PROBE 3  -> LF / CRLF / CR / no-final-EOL: one identity, carrier_ok True, anchor CONSTRUCTED;
            whitespace-in-body, line-wrapped and base64url bodies still False
```

## 7. Gates, with real exit codes

| Gate | Result |
|---|---|
| `python -m unittest test_mbcx01_build_state test_mbcx01_build_measurement test_mbcx01_build_integration` | `Ran 130 tests — OK`, exit **0** |
| `python -m unittest test_mbcx01_r13_state test_mbcx01_r13_packets test_mbcx01_r13_measurement test_mbcx01_r13_inference test_mbcx01_r13_integration` | `Ran 150 tests — OK`, exit **0** |
| `python verify-build-bundle.py` | exit **0**; seven sections PASS; frozen 150/150; ledger 48 invariants / 130 witnesses, `two_way_total: true`; readiness unchanged at `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED` |

`FROZEN_TEST_TOTAL` was raised only after the suite was green, and the number is the
DECLARATION that the frozen layer moved — exactly as AMENDMENT-1 recorded it. A future
reader who finds it at 150 should expect this document beside it.

## 8. Ripple

- **No hash literals were hand-updated.** The frozen layer recomputes every digest at
  runtime, and this amendment adds no field to any signed document, so nothing recomputes
  differently: `canonical_world_hash`, `manifest_hash` and the receipt digests are
  untouched by these changes (unlike AMENDMENT-1, which did move them).
- **The anchor now stores a NORMALISED carrier.** `OwnerTrustAnchor.public_key_pem` is the
  LF spelling whatever the operator wrote, so every downstream comparison keeps seeing one
  text for one key. An anchor whose document was CRLF will therefore not be byte-identical
  to its own source document at that field — deliberate, and the alternative (keeping the
  operator's spelling) would have re-introduced two texts for one key.
- **The pin manifests pin file BLOBS** and must be regenerated at the accepted commit —
  the same pin-freshness row AMENDMENT-1 named (`MBCX01-R4-PIN-MANIFEST-STALE-AND-FALSE-PACKET-CLAIM`).
- **Not closed here (declared, not hidden):** the literal-LF PEM assumption also lives at
  `mbcx01_build_measurement_authority.py:324-325`, `mbcx01_r13_measurement.py:148`, and in
  the `pattern` of `MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json:48` and
  `MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json:14`. Those govern MANIFEST documents,
  which this lane GENERATES rather than receives from an operator's keyboard, so the same
  argument does not automatically transfer — but the claim "we handle RFC 7468 carriers"
  is not true of them, and someone must rule on it rather than assume.
- **Reviewed, not executed:** `mbcx01_smoke_cell.py`'s dry-run fixture (thread 900 alive
  11..29 inside process 4100 alive 10..30, records at qpc 12 and 20) satisfies both new
  containment rules by inspection. It was NOT run — no ETW session, no Job Object, no
  `MBCX01_BUILD_ALLOW_PHYSICAL`, no `run-smoke-cell.ps1` — so that is a byte reading, not
  a green.

## 9. Re-review

Same trigger as AMENDMENT-1: this amends an invariant consumer in the frozen layer, so the
amended bytes go back to council with the other folds rather than straight to a gate. Two
items deserve a reviewer's attention first: the decision to accept a **bare-CR** carrier
that `openssl pkey -pubin` rejects (§3), and the decision to keep
`ETW_THREAD_LIFETIME_DUPLICATE_START` for same-QPC duplicates while giving the overlap its
own name (§5).
