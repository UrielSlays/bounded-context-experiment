# MBCX-01: Bounded Context for Long-Running Agents

[![tests](https://github.com/UrielSlays/bounded-context-experiment/actions/workflows/tests.yml/badge.svg)](https://github.com/UrielSlays/bounded-context-experiment/actions/workflows/tests.yml)

A preregistered experiment on whether a long-running agent can operate from a small, mechanically selected slice of its history instead of carrying the whole record in context.

The repository root is flat on purpose. Five pin manifests identify the reviewed files by path and hash, so every pinned file stays where its manifest says it is. [Start here](#start-here) lists the entry points.

## The problem

A long-running agent accumulates history: instructions, commitments, observations, decisions, and unfinished work. Keeping that entire record in context becomes more expensive as the history grows. Summarizing it reduces the load, but can discard details that later become important.

MBCX-01 tests a narrower alternative: keep the durable record outside the model, construct only the context needed for the current step, and determine whether that bounded view is sufficient to preserve the obligations and state required for correct behavior.

## Why this experiment

I wanted an assistant that could remain useful over time without keeping its entire history in one model session. That led to a systems question: could a persistent orchestrator load the state needed for a decision, save the changes, and release that context without losing track of its commitments?

MBCX-01 tests a prerequisite for that design: whether a bounded view of durable external state can preserve required facts and obligations, avoid construction costs that grow with total history, and support correct model behavior. The aim is to test that foundation before building the larger system around it.

## What is being tested

The full record lives in an append-only journal. At each step, a **carrier** constructs a live slice containing the information needed now, such as current facts, due obligations, and work in progress.

The experiment asks two separate questions:

1. **Exactness:** can the carrier produce the expected live slice without losing required state?
2. **Bounded cost:** can the work required to produce that slice depend primarily on the live set rather than total history length?

Three carrier designs are candidates: an active-frontier digest, a cache of that frontier, and a normalized temporal view.

## Experimental design

The experiment has two stages.

### Stage 1 — carrier evaluation without a model

Each carrier runs over a grid of synthetic histories spanning four history lengths, five dependency depths, and five fact counts.

For every cell:

- the produced slice is compared with the expected slice;
- CPU instructions, memory, and I/O are measured inside a Windows job object;
- exactness must hold across the full grid; and
- cost growth across history lengths must remain within a preregistered tolerance.

If no carrier passes, the experiment stops.

### Stage 2 — model evaluation

A carrier that passes Stage 1 is evaluated against an ideal slice constructed directly from ground truth.

The same frozen model runs the same scenarios in two conditions:

- the carrier-produced bounded slice; and
- the ideal ground-truth slice.

Each scenario is a chain of three model steps with a state write between steps. Output correctness is checked programmatically. The preregistered analysis asks whether the bounded-slice condition remains within the allowed margin of the ideal condition across 768 scenarios.

The scenario generator, scoring rules, contracts, analysis plan, and relevant artifacts are pinned by hash before any model call.

## Current status

The model-independent foundation is built and tested:

- append-only journal and state store;
- measurement producer;
- scoring and exactness machinery; and
- synthetic cohort generator.

The three carriers, grid runner, and model-side client are not yet complete. The experiment has not run yet.

## Running the current checks

```text
python -m unittest discover -s . -p "test_*.py"
python verify-build-bundle.py
```

Requirements: Windows, Python 3.11, and Node.js on the `PATH`. Run both commands from the repository root.

On Windows the suite runs 601 tests and all but one pass. That test (`bc14`) and `verify-build-bundle.py` stop early in this export because they reference a commit available only in the private working repository; see [Public export notes](docs/PUBLIC-EXPORT-NOTES.md). A full working-repository run log is retained in [docs/presentation/data/](docs/presentation/data/).

The measurement layer is written against Windows job objects and Event Tracing for Windows. On Linux the 106 tests that exercise it, all in `test_mbcx01_build_measurement.py` and `test_mbcx01_build_integration.py`, do not pass. The round r11 to r13 tests and the state store tests do not depend on Windows, and all 372 pass on Linux:

```text
python3 -m unittest discover -s . -p "test_mbcx01_r1*.py"
python3 -m unittest test_mbcx01_build_state
```

CI runs the full suite on Windows and checks that `bc14` is the only test that does not pass. On Linux it runs the two commands above.

## Start here

- **Experiment design:** [MBCX-01-EXPERIMENT-DESIGN-r9.md](MBCX-01-EXPERIMENT-DESIGN-r9.md)
- **Current closure architecture:** [MBCX-01-R13-CLOSURE-ARCHITECTURE.md](MBCX-01-R13-CLOSURE-ARCHITECTURE.md)
- **Implementation:** `mbcx01_*.py`; entry points include [build integration](mbcx01_build_integration.py) and [r13 integration](mbcx01_r13_integration.py).
- **Tests:** `test_*.py`; start with [build integration tests](test_mbcx01_build_integration.py) and [r13 integration tests](test_mbcx01_r13_integration.py).
- **Pinned contracts and manifests:** [build manifest](MBCX-01-BUILD-PIN-MANIFEST.json) and [r13 manifest](MBCX-01-R13-PIN-MANIFEST.json).
- **Longer write-up, figures, and prior art:** [illustrated write-up](docs/presentation/MBCX-01-PRESENTATION-2026-09-26.md) and [documentation](docs/).
- **Independent review record:** [review/](review/)
- **Review tooling:** [tools/](tools/), scripts from earlier rounds kept as they were run. They were written for the original root layout and are not re-pathed.

The repository retains earlier design and contract revisions because the evolution of the experiment is part of its audit trail. The current design and closure artifacts above are the intended entry points.

## License

Copyright (c) 2026 Clinton Cuzzort. All rights reserved. See [LICENSE](LICENSE).

Third-party components bundled under `vendor/` keep their own licenses; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
