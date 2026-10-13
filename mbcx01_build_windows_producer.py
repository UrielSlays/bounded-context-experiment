"""BUILD B Windows Job/ETW evidence producer.

Role: assemble one `SignedMeasurementReceiptV2` per grid cell from what a real
Windows collector observed, without ever inventing a value. The OS collection
itself lives behind a collection interface: this module only ever sees a
`SimulatedCollection` (fixture tests) or the identical structure returned by
the reviewed real collector (`mbcx01_build_win32.collect`, which this task
never executes). No function here starts a process, creates a Job Object,
opens an ETW session or touches a PMU.

Producer / adapter split (load-bearing, do not blur):

- the producer is a FAITHFUL RECORDER. It copies observed bytes and observed
  facts verbatim, recomputes only digests and canonical aggregates that are
  *derivations of the recorded observations*, and never substitutes, defaults
  or estimates a missing observation. A perturbed observation (a short query
  buffer, a scalar that disagrees with the raw bytes, a lost completion
  message) is recorded as observed and travels to the adapter.
- the adapter (`mbcx01_build_measurement_authority.evaluate_production_measurement`)
  is the JUDGE: it is the only place a value is refused. Structural faults the
  collector could not have produced at all (a non-`bytes` buffer, a missing
  scalar key, a signer whose key id is not the run's signing key) raise
  `ProducerFault` here, because a partial receipt must never be minted — the
  Gravity slice0c FAULT-is-not-a-verdict discipline.

Envelope shape — the compatibility boundary with the frozen r13
`SignedMeasurementReceiptV1` (`mbcx01_r13_measurement.py:430-433,505-514`):

- key set  = frozen `ENVELOPE_KEYS` (16) ∪ {`nonce`, `timing_cross_check`} (18);
- `schema_id` = `SignedMeasurementReceiptV2`, `domain` =
  `MBCX01.SIGNED-MEASUREMENT-RECEIPT.V2`, `version` = 2;
- signed preimage = the frozen 12 fields (`domain`, `version`, `algorithm`,
  `signing_key_id`, `run_id`, `cell_id`, `fixture_kind`, `producer_role`,
  `trust_policy_digest`, `subject_digest`, `environment_digest`, `receipt`)
  ∪ {`nonce`, `timing_cross_check`} — 14 fields, sorted-key canonical JSON
  (`measurement.canonical_json`), Ed25519 over those exact bytes, SHA-384
  `receipt_digest` over the same bytes. Digest discipline is identical to V1;
  only the field set grows, which is why this is a re-version and never an
  edit of the frozen envelope;
- the `MeasurementReceiptV3` evidence tree is reused VERBATIM (frozen closed
  key sets `RECEIPT_KEYS`/`JOB_KEYS`/`EVIDENCE_KEYS`), so every frozen
  evidence validator applies unchanged to a V2 receipt;
- `nonce` is a supervisor-minted per-cell anti-replay value (harness
  requirements §5, "nonce, subject digest and receipt digest");
- `timing_cross_check` is the V2-only tightening of the r13 soft spot at
  `mbcx01_r13_measurement.py:1099`, where `elapsed_monotonic_ns` is only
  checked `> 0`: it binds the signed QPC frequency and the signed member
  lifetimes span so the adapter can recompute elapsed nanoseconds exactly.

`FixtureSigner` is a test-only custody seam. It reuses the house Node
`node:crypto` Ed25519 mechanism already used by
`test_mbcx01_r13_measurement.py:19-36` (the repository has no Python
`cryptography` dependency and this task adds none). The private key is always
injected by the caller; no key material is embedded in this module, and the
candidate and evaluator never receive it.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from typing import Any

import mbcx01_r13_measurement as measurement

PRODUCTION_ENVELOPE_SCHEMA_ID = "SignedMeasurementReceiptV2"
PRODUCTION_ENVELOPE_DOMAIN = "MBCX01.SIGNED-MEASUREMENT-RECEIPT.V2"
PRODUCTION_ENVELOPE_VERSION = 2
PRODUCTION_FIXTURE_KIND = "PHYSICAL_HARNESS_RECEIPT"
PRODUCTION_PRODUCER_ROLE = "PHYSICAL_MEASUREMENT_PRODUCER"
PRODUCTION_RECEIPT_SOURCE = "WINDOWS_JOB_OBJECT_HARNESS_V2"

# Closed key set of the V2 envelope: the frozen V1 keys plus the two V2-only
# additions. A field addition is a re-version, never an edit.
PRODUCTION_ENVELOPE_KEYS = frozenset(
    measurement.ENVELOPE_KEYS | {"nonce", "timing_cross_check"})

# Ordered signed-preimage fields; canonical JSON is sorted-key, so this tuple
# documents coverage, not byte order.
PRODUCTION_PREIMAGE_FIELDS = (
    "domain", "version", "algorithm", "signing_key_id", "run_id", "cell_id",
    "fixture_kind", "producer_role", "trust_policy_digest", "subject_digest",
    "environment_digest", "nonce", "timing_cross_check", "receipt",
)

# V2-only cross-check block: elapsed monotonic nanoseconds must be reproducible
# from the signed QPC lifetimes span at the signed QPC frequency.
TIMING_CROSS_CHECK_KEYS = frozenset({
    "qpc_frequency_hz", "lifetimes_span_qpc", "elapsed_qpc_ticks",
    "elapsed_monotonic_ns", "tolerance_ns",
})

# The cross-check is exact: no slack is admissible between a signed QPC span
# converted at a signed frequency and a signed elapsed value.
TIMING_TOLERANCE_NS = 0

# Exact final-query classes and sizes the collector must return, byte for byte.
BASIC_AND_IO_CLASS = "JobObjectBasicAndIoAccountingInformation"
BASIC_AND_IO_SIZE_BYTES = 96
EXTENDED_LIMIT_CLASS = "JobObjectExtendedLimitInformation"
EXTENDED_LIMIT_SIZE_BYTES = 144
PEAK_COMMITTED_OFFSET = 136

# Canonical scalar aggregates the collector must supply, exactly these.
SCALAR_FIELDS = frozenset({
    "user_time_ns", "kernel_time_ns", "total_page_faults", "total_processes",
    "active_processes_at_final_query", "total_terminated_processes",
    "read_operations", "write_operations", "other_operations",
    "read_transfer_bytes", "write_transfer_bytes", "other_transfer_bytes",
    "peak_committed_bytes", "retired_instructions",
})

# ETW/instruction facts the collector must supply, exactly these. They are the
# frozen job-level names so the evidence tree needs no translation table.
TRACE_FACT_FIELDS = frozenset({
    "instruction_backend", "instruction_profile_source", "instruction_event_list",
    "instruction_attribution", "etw_capability_query_succeeded",
    "etw_pmc_source_available", "etw_max_pmc_counters",
    "etw_counter_owner_conflict_count", "etw_pmc_strict_mode",
    "etw_pmc_multiplexing_detected", "etw_events_lost", "etw_log_buffers_lost",
    "etw_realtime_buffers_lost", "etw_attribution_complete",
})

# Query-call metadata the collector records alongside the raw buffer; the raw
# bytes and their digest are recomputed here from the buffer itself.
QUERY_METADATA_KEYS = frozenset(
    measurement.QUERY_KEYS - {"raw_bytes_b64", "raw_bytes_sha384"})


class ProducerFault(RuntimeError):
    """A collection that could not have come from a working collector at all.

    A fault is never a verdict: it aborts receipt production instead of
    minting a partial or repaired envelope. Observed-but-wrong values are NOT
    faults — they are recorded and refused by the admission adapter.
    """


@dataclass(frozen=True)
class ProductionRunIdentity:
    """Grid-wide identity every cell of one production run must share.

    One candidate / generator / harness / host / trust-root / run identity
    governs all 100 cells; the adapter recomputes the grid identity hash from
    these fields (`mbcx01_r13_measurement._grid_identity_preimage`).
    """

    run_id: str
    candidate_id: str
    candidate_artifact_digest: str
    generator_digest: str
    harness_identity: dict[str, str]
    signing_key_id: str
    trust_policy_digest: str
    external_work_policy: str = "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE"
    fixture_kind: str = PRODUCTION_FIXTURE_KIND
    producer_role: str = PRODUCTION_PRODUCER_ROLE


@dataclass(frozen=True)
class SimulatedCollection:
    """Everything one Windows collection of one cell yields — and nothing else.

    Every field is what the OS returned. The producer may recompute derived
    values from these inputs and must fail loudly on any inconsistency; it may
    never substitute, default or estimate a missing observation. The same
    structure is what the reviewed real collector must return, so a fixture
    collection and a physical collection differ only in provenance, never in
    shape.
    """

    # Cell coordinate.
    H: int
    D: int
    F: int

    # Process control facts established before resume.
    job_object_id: str
    root_process_id: int
    root_process_start_key: str
    created_suspended: bool
    completion_port_associated_before_resume: bool
    assigned_before_resume: bool
    breakaway_enabled: bool
    silent_breakaway_enabled: bool

    # Raw final query buffers exactly as returned, plus their call metadata.
    basic_and_io_raw_bytes: bytes
    basic_and_io_query: dict[str, Any]
    extended_limit_raw_bytes: bytes
    extended_limit_query: dict[str, Any]

    # Signed lifetimes: every root and descendant bound to PID + start key,
    # including terminated members, and every thread bound to its process.
    process_lifetimes: tuple[dict[str, Any], ...]
    thread_lifetimes: tuple[dict[str, Any], ...]

    # Ordered per-processor CSwitch/PMC observations attributed to OldThreadId.
    cswitch_observations: tuple[dict[str, Any], ...]

    # Capability and attachment records for the strict ETW PMC session.
    trace_capability_query: dict[str, Any]
    trace_event_attachment: dict[str, Any]
    trace_facts: dict[str, Any]

    # Recomputed canonical scalars (CPU, I/O, memory, elapsed, instructions).
    scalars: dict[str, int]

    # QPC evidence backing the V2 elapsed-time cross-check.
    qpc_frequency_hz: int
    elapsed_qpc_ticks: int
    elapsed_monotonic_ns: int

    # Host/environment, supervisor-owned enforcement, completion diagnostics.
    environment: dict[str, Any]
    external_enforcement: dict[str, Any]
    completion: dict[str, Any]

    # Anti-replay nonce minted per cell by the supervisor, never by the candidate.
    nonce: str

    # AMENDMENT-3 (2026-08-16), REQUIRED — deliberately NO default (r7, three
    # seats convergent: a defaulted field made a forgetful caller's omission
    # indistinguishable from a true capture-start, and the old undercount
    # signed and cleared full production admission wrong by 1,000,000).
    # Per-processor predecessor baselines from the CSwitch scoping
    # ({"processor", "counter_value"} rows, one for EVERY observed processor —
    # the r7 totality rule; capture-start rows carry the first record's own
    # counter). A caller that omits this observation faults at construction,
    # before anything is signed.
    cswitch_first_member_baselines: tuple[dict[str, Any], ...]

    # Free-form collector provenance (labels only; never load-bearing evidence).
    collector_labels: dict[str, Any] = field(default_factory=dict)


class FixtureSigner:
    """Test-only Ed25519 signing seam with an injected private key.

    Reuses the repository's existing Node `node:crypto` signing mechanism (see
    `test_mbcx01_r13_measurement.py:19-36`); no new Python dependency is added.
    A production signer is a different, reviewed seam bound to a ceremony and
    an offline custodian: this class refuses any key id that is not marked as a
    test key, and it never reads key material from disk or the environment.
    """

    # Ed25519 is deterministic (RFC 8032 §5.1.6): the same key over the same
    # preimage always yields the same 64-byte signature. The fixture suite
    # rebuilds the same 100-cell simulated grid dozens of times, so signatures
    # are memoised per (key, preimage) to avoid ~4,000 Node spawns. This cache
    # is a FIXTURE-ONLY affordance: a production ceremony signer must never
    # memoise, because each production signature is an auditable ceremony act.
    _SIGNATURE_CACHE: dict[tuple[str, str], str] = {}

    def __init__(self, key_id: str, private_key_pem: str, *,
                 fixture_only: bool = True) -> None:
        if fixture_only is not True:
            raise ValueError("FixtureSigner signs fixture/simulated material only")
        if ".TEST." not in str(key_id) and not str(key_id).endswith(".TEST"):
            raise ValueError("FixtureSigner refuses a non-test key id")
        if (not isinstance(private_key_pem, str)
                or not private_key_pem.startswith("-----BEGIN PRIVATE KEY-----\n")
                or not private_key_pem.rstrip("\n").endswith("-----END PRIVATE KEY-----")):
            raise ValueError("FixtureSigner requires an injected PKCS#8 private key")
        self.key_id = key_id
        self.fixture_only = True
        self._private_key_pem = private_key_pem
        self._cache_scope = hashlib.sha384(
            private_key_pem.encode("utf-8")).hexdigest().upper()

    def sign_preimages(self, preimages_b64: list[str]) -> list[str]:
        """Return base64 Ed25519 signatures over the supplied base64 preimages."""
        if not preimages_b64:
            return []
        pending = [value for value in preimages_b64
                   if (self._cache_scope, value) not in self._SIGNATURE_CACHE]
        if pending:
            source = ("const {createPrivateKey,sign}=require('node:crypto');"
                      "let d='';process.stdin.setEncoding('utf8');"
                      "process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{"
                      "const r=JSON.parse(d),k=createPrivateKey(r.k);"
                      "process.stdout.write(JSON.stringify(r.ps.map(p=>sign(null,"
                      "Buffer.from(p,'base64'),k).toString('base64'))));});")
            request = {"k": self._private_key_pem, "ps": list(pending)}
            result = subprocess.run(["node", "-e", source], input=json.dumps(request),
                                    text=True, capture_output=True, timeout=30, check=True)
            signatures = json.loads(result.stdout)
            if not isinstance(signatures, list) or len(signatures) != len(pending):
                raise ValueError("fixture signer response invalid")
            for preimage, signature in zip(pending, signatures):
                self._SIGNATURE_CACHE[(self._cache_scope, preimage)] = signature
        return [self._SIGNATURE_CACHE[(self._cache_scope, value)]
                for value in preimages_b64]


def production_receipt_preimage(envelope: dict[str, Any]) -> bytes:
    """Canonical signed preimage of a V2 envelope (14 fields).

    Mirrors the frozen `mbcx01_r13_measurement._receipt_preimage` (:505-514)
    field-for-field and adds exactly `nonce` and `timing_cross_check`. Same
    canonicalisation (`canonical_json`: sorted keys, no NaN, UTF-8), so a V1
    and a V2 preimage differ only by the two added members.
    """
    return measurement.canonical_json(
        {name: envelope[name] for name in PRODUCTION_PREIMAGE_FIELDS})


def refresh_production_receipt_hash(envelope: dict[str, Any]) -> None:
    """Refresh only unsigned preimage/digest fields of a V2 envelope.

    Mirrors frozen `refresh_receipt_hash` (:534-548); it never confers
    signature authority — a refreshed envelope still has to be signed, and a
    mutated envelope that is merely refreshed loses its old signature.
    """
    if not isinstance(envelope, dict) or "receipt" not in envelope:
        raise ValueError("signed measurement envelope required")
    envelope["subject_digest"] = measurement.sha384(envelope["receipt"])
    try:
        envelope["environment_digest"] = envelope["receipt"]["job_receipt"]["evidence"][
            "harness_identity"]["host_environment_digest"]
    except (KeyError, TypeError):
        envelope.setdefault("environment_digest", "0" * 96)
    preimage = production_receipt_preimage(envelope)
    envelope["receipt_preimage_b64"] = base64.b64encode(preimage).decode("ascii")
    envelope["receipt_digest"] = hashlib.sha384(preimage).hexdigest().upper()


def _query_row(metadata: Any, raw: Any) -> dict[str, Any]:
    """One signed final-query record: recorded call metadata + the exact bytes.

    Shape is the frozen `_query_evidence` row (`mbcx01_r13_measurement.py:562-568`).
    The recorded class identity, structure/returned sizes and barrier ordering
    are copied exactly as the collector observed them; the buffer is passed
    through byte for byte and only its base64 form and SHA-384 digest are
    recomputed — a short, padded or mis-laid-out buffer reaches the adapter
    intact and is refused there, never repaired here.
    """
    if not isinstance(raw, (bytes, bytearray)):
        raise ProducerFault("QUERY_BUFFER_NOT_RAW_BYTES")
    if not isinstance(metadata, dict) or set(metadata) != QUERY_METADATA_KEYS:
        raise ProducerFault("QUERY_METADATA_STRUCTURE_INVALID")
    raw = bytes(raw)
    row = copy.deepcopy(metadata)
    row["raw_bytes_b64"] = base64.b64encode(raw).decode("ascii")
    row["raw_bytes_sha384"] = measurement.sha384(raw)
    return row


def _membership_complete(collection: SimulatedCollection) -> bool:
    """Membership completeness is DERIVED from signed control facts, never asserted.

    Harness requirements §2/§3: a member can only escape the roster if the root
    ran before assignment or a breakaway mode was enabled; the roster is closed
    only once every member is terminal and the final active-process count is
    zero. Each conjunct below is an observation this collection carries.
    """
    completion = collection.completion
    return bool(
        collection.created_suspended is True
        and collection.assigned_before_resume is True
        and collection.completion_port_associated_before_resume is True
        and collection.breakaway_enabled is False
        and collection.silent_breakaway_enabled is False
        and isinstance(completion, dict)
        and completion.get("all_members_terminal") is True
        and completion.get("final_active_processes") == 0)


def _timing_cross_check(collection: SimulatedCollection) -> dict[str, Any]:
    """V2-only evidence block backing the exact elapsed/QPC cross-check."""
    lifetimes = collection.process_lifetimes
    if not isinstance(lifetimes, tuple) or not lifetimes:
        raise ProducerFault("PROCESS_LIFETIMES_MISSING")
    try:
        span = (max(int(row["ended_qpc"]) for row in lifetimes)
                - min(int(row["started_qpc"]) for row in lifetimes))
    except (KeyError, TypeError, ValueError) as exc:
        raise ProducerFault("PROCESS_LIFETIME_QPC_MISSING") from exc
    return {
        "qpc_frequency_hz": collection.qpc_frequency_hz,
        "lifetimes_span_qpc": span,
        "elapsed_qpc_ticks": collection.elapsed_qpc_ticks,
        "elapsed_monotonic_ns": collection.elapsed_monotonic_ns,
        "tolerance_ns": TIMING_TOLERANCE_NS,
    }


def _evidence_tree(collection: SimulatedCollection,
                   identity: ProductionRunIdentity) -> dict[str, Any]:
    """The frozen `MeasurementReceiptV3` evidence tree, filled from observations."""
    processes = [copy.deepcopy(row) for row in collection.process_lifetimes]
    facts = collection.trace_facts
    observations = [copy.deepcopy(row) for row in collection.cswitch_observations]
    aggregate = 0
    for observation in observations:
        delta = observation.get("delta_from_previous") if isinstance(observation, dict) else None
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise ProducerFault("CSWITCH_OBSERVATION_STRUCTURE_INVALID")
        aggregate += delta
    return {
        "harness_identity": copy.deepcopy(identity.harness_identity),
        "environment": copy.deepcopy(collection.environment),
        "process_membership": {
            "root_process_id": collection.root_process_id,
            "root_process_start_key": collection.root_process_start_key,
            "membership_complete": _membership_complete(collection),
            "membership_snapshot_digest": measurement.sha384(processes),
            "processes": processes},
        "job_queries": {
            "basic_and_io": _query_row(collection.basic_and_io_query,
                                       collection.basic_and_io_raw_bytes),
            "extended_limit": _query_row(collection.extended_limit_query,
                                         collection.extended_limit_raw_bytes)},
        "completion": copy.deepcopy(collection.completion),
        "external_enforcement": copy.deepcopy(collection.external_enforcement),
        "trace": {
            "mode": facts["instruction_backend"],
            "profile_source": facts["instruction_profile_source"],
            "event_list": facts["instruction_event_list"],
            "attribution": facts["instruction_attribution"],
            "capability_query_succeeded": facts["etw_capability_query_succeeded"],
            "pmc_source_available": facts["etw_pmc_source_available"],
            "max_pmc_counters": facts["etw_max_pmc_counters"],
            "counter_owner_conflict_count": facts["etw_counter_owner_conflict_count"],
            "strict_mode": facts["etw_pmc_strict_mode"],
            "multiplexing_detected": facts["etw_pmc_multiplexing_detected"],
            "events_lost": facts["etw_events_lost"],
            "log_buffers_lost": facts["etw_log_buffers_lost"],
            "realtime_buffers_lost": facts["etw_realtime_buffers_lost"],
            "attribution_complete": facts["etw_attribution_complete"],
            "capability_query": copy.deepcopy(collection.trace_capability_query),
            "event_attachment": copy.deepcopy(collection.trace_event_attachment),
            "thread_lifetimes": [copy.deepcopy(row)
                                 for row in collection.thread_lifetimes],
            "cswitch_observations": observations,
            "cswitch_first_member_baselines": [
                copy.deepcopy(row)
                for row in collection.cswitch_first_member_baselines],
            "aggregate_retired_instructions": aggregate},
    }


def _job_receipt(collection: SimulatedCollection,
                 identity: ProductionRunIdentity) -> dict[str, Any]:
    """The frozen closed `JOB_KEYS` job receipt, filled from observations only."""
    scalars = collection.scalars
    facts = collection.trace_facts
    if not isinstance(scalars, dict) or set(scalars) != SCALAR_FIELDS:
        raise ProducerFault("SCALAR_STRUCTURE_INVALID")
    if not isinstance(facts, dict) or set(facts) != TRACE_FACT_FIELDS:
        raise ProducerFault("TRACE_FACT_STRUCTURE_INVALID")
    if not isinstance(collection.completion, dict):
        raise ProducerFault("COMPLETION_STRUCTURE_INVALID")
    job = {
        "receipt_source": PRODUCTION_RECEIPT_SOURCE,
        "job_object_id": collection.job_object_id,
        "root_process_id": collection.root_process_id,
        "created_suspended": collection.created_suspended,
        "completion_port_associated_before_resume":
            collection.completion_port_associated_before_resume,
        "assigned_before_resume": collection.assigned_before_resume,
        "breakaway_enabled": collection.breakaway_enabled,
        "silent_breakaway_enabled": collection.silent_breakaway_enabled,
        # Diagnostic mirror of the completion evidence, recorded as observed:
        # message delivery is not guaranteed (harness requirements §3).
        "completion_port_drained": collection.completion.get("completion_port_drained"),
        "elapsed_monotonic_ns": collection.elapsed_monotonic_ns,
    }
    job.update({name: scalars[name] for name in sorted(SCALAR_FIELDS)})
    job.update({name: facts[name] for name in sorted(TRACE_FACT_FIELDS)})
    job["evidence"] = _evidence_tree(collection, identity)
    if set(job) != measurement.JOB_KEYS:
        raise ProducerFault("JOB_RECEIPT_KEY_SET_INVALID")
    return job


def produce_signed_measurement_receipt_v2(collection: SimulatedCollection, *,
                                          signer: FixtureSigner,
                                          identity: ProductionRunIdentity) -> dict[str, Any]:
    """Build one signed `SignedMeasurementReceiptV2` envelope from a collection.

    The collection's raw 96/144-byte query buffers pass through verbatim; every
    scalar, control fact, lifetime and ETW record is recorded as observed; the
    evidence tree, the QPC cross-check block, the canonical preimage and the
    SHA-384 digests are recomputed from those observations, and only the
    preimage bytes are handed to the injected signer. Nothing is guessed: a
    collection that is structurally impossible raises `ProducerFault`, and a
    collection that is merely wrong is recorded and refused by the adapter.
    """
    if not isinstance(collection, SimulatedCollection):
        raise ProducerFault("COLLECTION_STRUCTURE_INVALID")
    if not isinstance(identity, ProductionRunIdentity):
        raise ProducerFault("RUN_IDENTITY_STRUCTURE_INVALID")
    if signer is None or getattr(signer, "key_id", None) != identity.signing_key_id:
        raise ProducerFault("SIGNER_IDENTITY_MISMATCH")
    receipt = {
        "schema_id": "MeasurementReceiptV3",
        "candidate_id": identity.candidate_id,
        "candidate_artifact_digest": identity.candidate_artifact_digest,
        "generator_digest": identity.generator_digest,
        "H": collection.H, "D": collection.D, "F": collection.F,
        "external_work_policy": identity.external_work_policy,
        "job_receipt": _job_receipt(collection, identity),
    }
    if set(receipt) != measurement.RECEIPT_KEYS:
        raise ProducerFault("RECEIPT_KEY_SET_INVALID")
    envelope = {
        "schema_id": PRODUCTION_ENVELOPE_SCHEMA_ID,
        "domain": PRODUCTION_ENVELOPE_DOMAIN,
        "version": PRODUCTION_ENVELOPE_VERSION,
        "algorithm": measurement.SIGNATURE_ALGORITHM,
        "signing_key_id": identity.signing_key_id,
        "run_id": identity.run_id,
        "cell_id": measurement._cell_id(receipt),
        "receipt": receipt,
        "receipt_preimage_b64": "", "receipt_digest": "", "signature_b64": "",
        "fixture_kind": identity.fixture_kind,
        "producer_role": identity.producer_role,
        "trust_policy_digest": identity.trust_policy_digest,
        "subject_digest": "", "environment_digest": "",
        "nonce": collection.nonce,
        "timing_cross_check": _timing_cross_check(collection),
    }
    if set(envelope) != set(PRODUCTION_ENVELOPE_KEYS):
        raise ProducerFault("ENVELOPE_KEY_SET_INVALID")
    refresh_production_receipt_hash(envelope)
    envelope["signature_b64"] = signer.sign_preimages(
        [envelope["receipt_preimage_b64"]])[0]
    return envelope
