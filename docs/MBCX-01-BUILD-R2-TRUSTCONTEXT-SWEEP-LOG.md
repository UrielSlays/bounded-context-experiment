# MBCX-01 BUILD r2 — driver sweep log: verifier trust context (the r2 fix class)

Run 2026-08-14 by the BUILD-lane driver, BEFORE ruling on the r2 fix class.
Purpose: does the outside world settle HOW a verifier holds its root of trust, its
current time, and its test material — or is this a design question for the owner?
(BEFORE-YOU-ASK §2 lanes: standards · vendor practice · prior art · footguns · our shelf.)

## PRIMARY sources OPENED at origin this session

1. **Go `crypto/x509/verify.go`** (raw source at `raw.githubusercontent.com/golang/go/master/src/crypto/x509/verify.go`, ranged read) — **SEARCHED, PRIMARY.**
   - Deciding bytes: `func (c *Certificate) isValid(certType int, currentChain []*Certificate, opts *VerifyOptions) error`
     and inside it `now := opts.CurrentTime; if now.IsZero() { now = time.Now() }`; plus the doc line
     *"Verify attempts to verify c by building one or more chains from c to a certificate in `opts.Roots`."*
   - What it settles: in the reference implementation of exactly our problem shape, **the roots AND the
     current time are fields of a per-call options value the VERIFIER constructs and passes in.** There is
     no process-global mutable trust store, and no way for the artifact under verification to supply either.
   - Note the seam it also settles for us: Go's fallback when no time is supplied is **the real clock**
     (`time.Now()`), never a value read out of the artifact being checked. Our current default —
     the manifest's own `published_at` — takes its freshness input from the thing under test.

2. **TUF specification** (`raw.githubusercontent.com/theupdateframework/specification/master/tuf-spec.md`, ranged read, §Update the root role) — **SEARCHED, PRIMARY.**
   - Deciding bytes: *"We assume that a good, trusted copy of this file was shipped with the package manager
     or software updater using an out-of-band process"*; then step 4 (a new root MUST be signed by a threshold
     of keys in the ALREADY-TRUSTED root) and step 5 *"Check for a rollback attack. The version number of the
     new root metadata MUST be exactly the version in the trusted root metadata incremented by one."*
   - What it settles: **the bootstrap root arrives OUT OF BAND**, never from the claimant, and rollback is
     resisted by a monotonic version the verifier already holds. Our `minimum_activation_generation` is that
     idea; keeping it in the operator-held anchor (not the manifest) is the conforming placement.

3. **SLSA v1.2 "Verifying artifacts", Step 1** (`slsa.dev/spec/v1.2/verifying-artifacts`, opened earlier this
   session, ranged read) — **SEARCHED, PRIMARY.** *"Verify the envelope's signature using the roots of trust,
   resulting in a list of recognized public keys"* — the roots are the verifier's own configured roster, with
   per-entry trust ceilings. Confirms the anchor model the fold adopted; it does NOT bless a global mutable one.

4. **MITRE CWE-321, "Use of Hard-coded Cryptographic Key"** — cited by the codex seat as the footgun class for
   the committed fixture owner key. **RECALLED-with-seat-pointer** (I did not open cwe.mitre.org myself this
   session). It is NOT load-bearing for the ruling: the deciding evidence is our own executed byte
   (a `fixture_only:true` anchor resolves as the production anchor for both authorities), not the CWE text.

## Internal shelf

- `docs/fips-crypto-inventory.md` (read in full this session): the bridge's own pins are compile-time constants
  (RFC-7469 SPKI pin `run-ca.ts:81`), i.e. the repo has **no operator-config trust-anchor loader to adopt** —
  confirmed by grep for `trust anchor|pinned owner|SPKI|preconfigured root` across `src/` (hits are CRL chain
  verification + the compile-time pin). So the shape must come from the OUTSIDE shelf, which it does (1)+(2).
- `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.6 already states a production manifest is injected out-of-band and
  never committed. The r2 findings are the implementation failing to enforce the spec it already carries —
  same shape as the r1 finding.

## RULING (BEFORE-YOU-ASK §3 row A — the sweep answers it; recorded, no owner row)

**The mechanism is settled by converging primaries and is ADOPTED, not invented: an immutable, instance-scoped
verifier trust context — constructed by the operator/verifier, carrying the anchor and the current time,
passed in per verification — replacing the process-global mutable anchor.** Go's `VerifyOptions` is the
shape; TUF supplies the out-of-band bootstrap and the monotonic anti-rollback; SLSA supplies the
verifier-configured-roster model.

This collapses codex-r2 F1/F2/F3 into ONE invariant rather than three patches, and it is expressible as a
COMPLEMENT (TAR-PIT Q4), which is what makes it a wholesale close rather than an enumeration:
**production verification accepts exactly one thing — a verifier-constructed context whose anchor is
operator-supplied and not fixture-marked — and refuses everything else.**

**Scope call (TAR-PIT Lesson 15 / Shelf-Zero Q-ZERO-B):** this is a FOLD, not a new machine. It re-shapes
existing BUILD-lane modules into a standard, named, off-the-shelf pattern and adds no engine, lifecycle, or
subsystem; the capability it serves is the one the committed ceremony spec already specifies. ⚠ The codex seat
judged it "bigger than the bug" and asked for a design gate — that disagreement is recorded in the r2
synthesis and surfaced to the owner rather than settled silently, because it is a scope judgement rather than
a mechanism question. It does not block the fold: the fold's shape is the one the standards prescribe under
either answer.

**Not settled by this sweep, carried into the fix spec as open:** whether the exactness authority's PASS
binding should require proof-of-execution of the carrier suite (codex F7) — that is our own product semantics,
not an external standard, and is ruled in-lane against the exactness spec §3.
