"""R11-owned inference, missingness, route, and planning-diagnostic kernels.

This module is deliberately self-contained.  Its synthetic simulations are design
diagnostics, never experimental evidence and never an authorization for paid calls.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import struct
from typing import Any, Iterable


SCIENTIFIC_N = 768
KAPPA = 0.25
STREAM_ALPHA = 0.025
PAIR_ALPHABET = ((0, 0), (0, 1), (1, 0), (1, 1))
DECISION_BRANCHES = {
    "DESIGN_OR_IMPLEMENTATION_FAIL", "TRANSPORT_INCONCLUSIVE",
    "MODEL_OR_INTERFACE_CEILING", "MODEL_INTERFACE_FAIL",
    "PROMOTE_TO_COORDINATION_STAGE", "INCONCLUSIVE_OR_UNDERFUNDED",
}


def psi_e(value: float) -> float:
    if not 0.0 <= value < 1.0:
        raise ValueError("psi_E input must be in [0,1)")
    return -math.log1p(-value) - value


def stream_statistics(xs: list[float], kappa: float = KAPPA) -> tuple[float, float]:
    if not xs or any(not 0.0 <= value <= 1.0 for value in xs):
        raise ValueError("observations must be a nonempty sequence in [0,1]")
    if not isinstance(kappa, (int, float)) or isinstance(kappa, bool) or kappa <= 0.0:
        raise ValueError("kappa must be positive")
    total = 0.0
    variance = 1.0 / (2.0 * kappa * kappa)
    for index, value in enumerate(xs, 1):
        estimate = (0.5 + total) / index
        variance += psi_e(abs(value - estimate))
        total += value
    return total, variance


def mixture_integral_analytic(y: float, variance: float) -> float:
    if variance < 0.0:
        raise ValueError("variance must be nonnegative")
    if variance == 0.0:
        return 2.0 if y == 0.0 else 2.0 * math.sinh(y) / y
    root = math.sqrt(variance)
    shift = y / (2.0 * variance)
    difference = math.erf(root * (1.0 - shift)) - math.erf(root * (-1.0 - shift))
    return (math.exp(y * y / (4.0 * variance)) * math.sqrt(math.pi)
            * difference / (2.0 * root))


def _mixture_threshold(alpha: float, kappa: float) -> float:
    if not 0.0 < alpha < 1.0 or kappa <= 0.0:
        raise ValueError("alpha and kappa must be positive and alpha must be below one")
    normalizer = math.erf(1.0 / (kappa * math.sqrt(2.0)))
    return kappa * normalizer * math.sqrt(2.0 * math.pi) / alpha


def mixture_boundary(variance: float, alpha: float = STREAM_ALPHA,
                     kappa: float = KAPPA) -> float:
    threshold = _mixture_threshold(alpha, kappa)
    low, high = 0.0, 1.0
    while mixture_integral_analytic(high, variance) < threshold:
        high *= 2.0
        if high > 4096.0:
            raise ArithmeticError("failed to bracket mixture boundary")
    for _ in range(80):
        mid = (low + high) / 2.0
        if mixture_integral_analytic(mid, variance) < threshold:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def mixture_interval(xs: list[float], alpha: float = STREAM_ALPHA,
                     kappa: float = KAPPA) -> tuple[float, float]:
    total, variance = stream_statistics(xs, kappa)
    half_width = mixture_boundary(variance, alpha, kappa) / len(xs)
    mean = total / len(xs)
    return max(0.0, mean - half_width), min(1.0, mean + half_width)


def paired_intervals(pairs: list[tuple[int, int]]) -> tuple[tuple[float, float],
                                                             tuple[float, float]]:
    valid_pair = lambda pair: (isinstance(pair, tuple) and len(pair) == 2
                               and all(isinstance(value, int) and not isinstance(value, bool)
                                       and value in (0, 1) for value in pair))
    if len(pairs) != SCIENTIFIC_N or any(not valid_pair(pair) for pair in pairs):
        raise ValueError("scientific intervals require exactly 768 binary pairs")
    delta_unit = mixture_interval([(bc - om + 1.0) / 2.0 for bc, om in pairs])
    delta = (2.0 * delta_unit[0] - 1.0, 2.0 * delta_unit[1] - 1.0)
    om = mixture_interval([float(pair[1]) for pair in pairs])
    return delta, om


def ordered_paired_intervals(rows: list[dict[str, Any]],
                             manifest_scenario_ids: list[str]) -> tuple[tuple[float, float],
                                                                        tuple[float, float]]:
    expected = sorted(manifest_scenario_ids,
                      key=lambda value: hashlib.sha256(value.encode("utf-8")).digest())
    if (len(rows) != SCIENTIFIC_N or len(expected) != SCIENTIFIC_N
            or len(set(expected)) != SCIENTIFIC_N
            or expected != manifest_scenario_ids
            or any(not isinstance(row, dict) or set(row) != {"scenario_id", "bc", "om"}
                   for row in rows)
            or [row["scenario_id"] for row in rows] != expected):
        raise ValueError("outcomes must exactly match the frozen SHA-256 scenario order")
    pairs = [(row["bc"], row["om"]) for row in rows]
    return paired_intervals(pairs)


def ordered_decision_with_missingness(observed_rows: list[dict[str, Any]],
                                      missing_scenario_ids: list[str],
                                      manifest_scenario_ids: list[str], *,
                                      design_ok: bool = True) -> str:
    expected = sorted(manifest_scenario_ids,
                      key=lambda value: hashlib.sha256(value.encode("utf-8")).digest())
    missing = set(missing_scenario_ids)
    observed_ids = [row.get("scenario_id") for row in observed_rows
                    if isinstance(row, dict)]
    expected_observed = [sid for sid in expected if sid not in missing]
    if (len(expected) != SCIENTIFIC_N or manifest_scenario_ids != expected
            or len(missing) != len(missing_scenario_ids) or not missing.issubset(expected)
            or any(not isinstance(row, dict) or set(row) != {"scenario_id", "bc", "om"}
                   for row in observed_rows)
            or observed_ids != expected_observed):
        raise ValueError("observed and missing outcomes must partition the frozen manifest order")
    observed_pairs = [(row["bc"], row["om"]) for row in observed_rows]
    missing_positions = [index for index, sid in enumerate(expected) if sid in missing]
    return decision_with_missingness(observed_pairs, missing_positions, design_ok=design_ok)


def scientific_decision(delta_interval: tuple[float, float],
                        om_interval: tuple[float, float]) -> str:
    if om_interval[1] < 0.80:
        return "MODEL_OR_INTERFACE_CEILING"
    if delta_interval[1] < -0.10 and om_interval[0] >= 0.80:
        return "MODEL_INTERFACE_FAIL"
    if delta_interval[0] > -0.10 and om_interval[0] >= 0.80:
        return "PROMOTE_TO_COORDINATION_STAGE"
    return "INCONCLUSIVE_OR_UNDERFUNDED"


def _stream_hull(values: list[float | None], choices: tuple[float, ...]) -> tuple[float, float]:
    if not values:
        raise ValueError("stream must contain at least one position")
    scale = 2
    states: dict[int, float] = {0: 1.0 / (2.0 * KAPPA * KAPPA)}
    for index, observed in enumerate(values, 1):
        next_states: dict[int, float] = {}
        possible = choices if observed is None else (observed,)
        for scaled_sum, variance in states.items():
            estimate = (0.5 + scaled_sum / scale) / index
            for value in possible:
                new_sum = scaled_sum + int(round(scale * value))
                new_variance = variance + psi_e(abs(value - estimate))
                next_states[new_sum] = max(next_states.get(new_sum, -math.inf), new_variance)
        states = next_states
    n = len(values)
    endpoints = []
    for scaled_sum, variance in states.items():
        mean = (scaled_sum / scale) / n
        half_width = mixture_boundary(variance) / n
        endpoints.append((max(0.0, mean - half_width), min(1.0, mean + half_width)))
    return min(row[0] for row in endpoints), max(row[1] for row in endpoints)


def _streams_from_observed(observed_pairs: list[tuple[int, int]],
                           missing_positions: list[int]) -> tuple[list[float | None],
                                                                  list[float | None]]:
    n = len(observed_pairs) + len(missing_positions)
    missing = set(missing_positions)
    if (n != SCIENTIFIC_N or len(missing) != len(missing_positions)
            or any(not isinstance(pos, int) or isinstance(pos, bool) or not 0 <= pos < n
                   for pos in missing_positions)
            or any(not isinstance(pair, tuple) or len(pair) != 2
                   or any(not isinstance(value, int) or isinstance(value, bool)
                          or value not in (0, 1) for value in pair)
                   or pair not in PAIR_ALPHABET for pair in observed_pairs)):
        raise ValueError("observed pairs and unique positions must partition 768")
    observed_iterator = iter(observed_pairs)
    delta: list[float | None] = []
    om: list[float | None] = []
    for position in range(n):
        if position in missing:
            delta.append(None)
            om.append(None)
        else:
            bc, oracle = next(observed_iterator)
            delta.append((bc - oracle + 1.0) / 2.0)
            om.append(float(oracle))
    return delta, om


def missing_completion_bounds(observed_pairs: list[tuple[int, int]],
                              missing_positions: list[int]) -> tuple[float, float, float, float]:
    delta, om = _streams_from_observed(observed_pairs, missing_positions)
    delta_unit = _stream_hull(delta, (0.0, 0.5, 1.0))
    om_hull = _stream_hull(om, (0.0, 1.0))
    return 2.0 * delta_unit[0] - 1.0, 2.0 * delta_unit[1] - 1.0, *om_hull


def exhaustive_missing_completion_bounds(
        observed_pairs: list[tuple[int, int]],
        missing_positions: list[int]) -> tuple[float, float, float, float]:
    if len(missing_positions) > 7:
        raise ValueError("exhaustive cross-check is restricted to seven missing pairs")
    _streams_from_observed(observed_pairs, missing_positions)
    missing = set(missing_positions)
    results = []
    for completion in itertools.product(PAIR_ALPHABET, repeat=len(missing_positions)):
        observed_iterator = iter(observed_pairs)
        completion_iterator = iter(completion)
        pairs = [next(completion_iterator) if position in missing else next(observed_iterator)
                 for position in range(SCIENTIFIC_N)]
        delta, om = paired_intervals(pairs)
        results.append((delta[0], delta[1], om[0], om[1]))
    return (min(row[0] for row in results), max(row[1] for row in results),
            min(row[2] for row in results), max(row[3] for row in results))


def decision_with_missingness(observed_pairs: list[tuple[int, int]],
                              missing_positions: list[int], *, design_ok: bool = True) -> str:
    if not isinstance(design_ok, bool):
        raise ValueError("design_ok must be an exact Boolean")
    if not design_ok:
        return "DESIGN_OR_IMPLEMENTATION_FAIL"
    if not missing_positions:
        return scientific_decision(*paired_intervals(observed_pairs))
    delta_lower, delta_upper, om_lower, om_upper = missing_completion_bounds(
        observed_pairs, missing_positions)
    if om_upper < 0.80:
        return "MODEL_OR_INTERFACE_CEILING"
    if delta_upper < -0.10 and om_lower >= 0.80:
        return "MODEL_INTERFACE_FAIL"
    if delta_lower > -0.10 and om_lower >= 0.80:
        return "PROMOTE_TO_COORDINATION_STAGE"
    return "TRANSPORT_INCONCLUSIVE"


def binomial_cdf(allowed_failures: int, trials: int, probability: float) -> float:
    if (not isinstance(allowed_failures, int) or isinstance(allowed_failures, bool)
            or not isinstance(trials, int) or isinstance(trials, bool)
            or not 0 <= allowed_failures <= trials or not 0 <= probability <= 1):
        raise ValueError("invalid binomial arguments")
    if probability == 0.0:
        return 1.0
    if probability == 1.0:
        return 1.0 if allowed_failures == trials else 0.0
    term = (1.0 - probability) ** trials
    total = term
    odds = probability / (1.0 - probability)
    for failures in range(1, allowed_failures + 1):
        term *= (trials - failures + 1) / failures * odds
        total += term
    return total


def smallest_reliability_plan(p_bad: float, p_good: float, consumer_risk: float,
                              producer_risk: float) -> tuple[int, int]:
    if not 0 <= p_good < p_bad <= 1 or not 0 < consumer_risk < 1 or not 0 < producer_risk < 1:
        raise ValueError("invalid reliability-plan arguments")
    for trials in range(1, 10000):
        for allowed in range(trials + 1):
            if (binomial_cdf(allowed, trials, p_bad) <= consumer_risk
                    and binomial_cdf(allowed, trials, p_good) >= 1.0 - producer_risk):
                return trials, allowed
    raise ValueError("no plan found")


def route_acceptance_bound(*, trials: int, allowed_failures: int, probability: float,
                           direction: str, assumption: str = "conditional_hazard") -> float:
    """Finite-horizon conditional-expectation recursion reduced to a binomial tail.

    ``direction='lower'`` means every conditional failure hazard is at least p, so
    acceptance is at most the returned value. ``upper`` reverses both statements.
    The result does not follow from marginal failure probabilities alone.
    """
    if assumption != "conditional_hazard":
        raise ValueError("route bound requires a per-trial full-past conditional hazard")
    if direction not in ("lower", "upper"):
        raise ValueError("direction must be lower or upper")
    # Backward recursion: V(t,k)=q V(t-1,k-1)+(1-q)V(t-1,k).  Monotonicity
    # makes the extremal q equal the stated hazard boundary at every history.
    values = [1.0 if failures <= allowed_failures else 0.0
              for failures in range(trials + 1)]
    for remaining in range(1, trials + 1):
        limit = trials - remaining
        next_values = []
        for failures in range(limit + 1):
            next_values.append((1.0 - probability) * values[failures]
                               + probability * values[failures + 1])
        values = next_values
    return values[0]


def route_qualification_bounds() -> dict[str, float | int | str]:
    bad = route_acceptance_bound(trials=456, allowed_failures=4, probability=.02,
                                 direction="lower")
    good = route_acceptance_bound(trials=456, allowed_failures=4, probability=.005,
                                  direction="upper")
    return {
        "trials": 456,
        "accept_failures_at_most": 4,
        "proof": "FINITE_HORIZON_CONDITIONAL_EXPECTATION_RECURSION",
        "bad_route_acceptance_max": bad,
        "good_route_acceptance_min": good,
        "good_route_rejection_max": 1.0 - good,
    }


def registered_planning_cells() -> list[dict[str, Any]]:
    common = {"claim_kind": "DETERMINISTIC_PLANNING_FREQUENCY",
              "experiment_evidence": False}
    rows = [
        {"id": "OM90_EQUAL", "p00": .05, "p01": .05, "p10": .05, "p11": .85,
         "expected_branch": "PROMOTE_TO_COORDINATION_STAGE"},
        {"id": "LOW_DISCORD_EQUAL", "p00": .09, "p01": .01, "p10": .01, "p11": .89,
         "expected_branch": "PROMOTE_TO_COORDINATION_STAGE"},
        {"id": "DELTA_NEG20_OM90", "p00": .10, "p01": .20, "p10": 0.0, "p11": .70,
         "expected_branch": "MODEL_INTERFACE_FAIL"},
        {"id": "CEILING_OM70_EQUAL", "p00": .25, "p01": .05, "p10": .05, "p11": .65,
         "expected_branch": "MODEL_OR_INTERFACE_CEILING"},
        {"id": "R10_COUNTEREXAMPLE", "p00": 0.0, "p01": .30, "p10": .10, "p11": .60,
         "expected_branch": "MODEL_INTERFACE_FAIL", "diagnostic_only": True},
    ]
    return [{**row, **common} for row in rows]


def _counter_uniforms(seed_parts: list[str], count: int) -> Iterable[float]:
    seed = b"".join(len(part.encode("utf-8")).to_bytes(8, "big")
                    + part.encode("utf-8") for part in seed_parts)
    produced = 0
    counter = 0
    denominator = float(1 << 64)
    while produced < count:
        digest = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        for integer in struct.unpack(">QQQQ", digest):
            if produced >= count:
                break
            yield integer / denominator
            produced += 1
        counter += 1


def _draw_pair(value: float, cell: dict[str, Any]) -> tuple[int, int]:
    if value < cell["p00"]:
        return 0, 0
    if value < cell["p00"] + cell["p01"]:
        return 0, 1
    if value < cell["p00"] + cell["p01"] + cell["p10"]:
        return 1, 0
    return 1, 1


def simulate_registered_cells(replicates: int = 10000,
                              seed: str = "MBCX01-R11-OC-V1") -> dict[str, Any]:
    if not isinstance(replicates, int) or isinstance(replicates, bool) or replicates <= 0:
        raise ValueError("replicates must be a positive integer")
    output = []
    for cell in registered_planning_cells():
        probabilities = [cell[key] for key in ("p00", "p01", "p10", "p11")]
        if any(value < 0.0 for value in probabilities) or not math.isclose(
                sum(probabilities), 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError(f"invalid registered cell {cell['id']}")
        counts: dict[str, int] = {}
        for replicate in range(replicates):
            pairs = [_draw_pair(value, cell) for value in _counter_uniforms(
                [seed, cell["id"], str(replicate)], SCIENTIFIC_N)]
            branch = scientific_decision(*paired_intervals(pairs))
            counts[branch] = counts.get(branch, 0) + 1
        output.append({
            "id": cell["id"],
            "expected_branch": cell["expected_branch"],
            "replicates": replicates,
            "branch_counts": dict(sorted(counts.items())),
            "expected_branch_frequency": counts.get(cell["expected_branch"], 0) / replicates,
        })
    return {
        "schema_id": "MBCX01R11DeterministicPlanningFrequencyV1",
        "experiment_evidence": False,
        "claim_kind": "DETERMINISTIC_PLANNING_FREQUENCY",
        "seed": seed,
        "n": SCIENTIFIC_N,
        "replicates_per_cell": replicates,
        "cells": output,
    }
