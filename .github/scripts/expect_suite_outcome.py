"""Run the test suite and compare the outcome with the documented one.

This export cannot be all-green: one test needs a commit that exists only in
the private working repository (docs/PUBLIC-EXPORT-NOTES.md). The exit code of
a plain `unittest` run would therefore be red on every run, and a new failure
would hide behind the known one.

This script runs the same discovery as the README command, from the repository
root, and fails unless the tests that do not pass are exactly the ones named
with --not-passing. A new failure, an expected failure nobody documented, a
module that no longer imports, a skipped test and a documented failure that
starts passing are each reported by name.
"""

from __future__ import annotations

import argparse
import sys
import unittest


def _test_id(case: unittest.TestCase) -> str:
    # A failing subTest reports as "<test id> (<parameters>)"; the documented
    # id is the test's own. Class- and module-level fixture errors have no
    # dotted first word and are reported whole.
    full = case.id()
    first = full.split(" ", 1)[0]
    return first if "." in first else full


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument(
        "--pattern",
        default="test_*.py",
        help="discovery pattern (default: %(default)s)",
    )
    parser.add_argument(
        "--ran",
        type=int,
        required=True,
        help="number of tests the run must execute",
    )
    parser.add_argument(
        "--skipped",
        type=int,
        default=0,
        help="number of tests the run may skip (default: %(default)s)",
    )
    parser.add_argument(
        "--not-passing",
        nargs="*",
        default=[],
        metavar="TEST_ID",
        help="ids of the tests documented as not passing",
    )
    args = parser.parse_args(argv)

    # A loader of its own: the shared default loader keeps the top-level
    # directory of any earlier discovery in the process on Python 3.11.
    suite = unittest.TestLoader().discover(".", pattern=args.pattern)
    result = unittest.TextTestRunner(verbosity=1).run(suite)

    # Every bucket of unittest.TestResult other than a pass or a skip. A test
    # marked expectedFailure does not pass either way, so it has to be
    # documented like any other.
    not_passing = {
        _test_id(case)
        for case, _ in (*result.failures, *result.errors, *result.expectedFailures)
    }
    not_passing.update(_test_id(case) for case in result.unexpectedSuccesses)
    documented = set(args.not_passing)

    problems: list[str] = []
    if result.testsRun != args.ran:
        problems.append(f"ran {result.testsRun} tests, expected {args.ran}")
    if len(result.skipped) != args.skipped:
        problems.append(f"skipped {len(result.skipped)} tests, expected {args.skipped}")
        problems.extend(f"skipped: {_test_id(case)}" for case, _ in result.skipped)
    problems.extend(
        f"not passing and not documented: {test_id}"
        for test_id in sorted(not_passing - documented)
    )
    problems.extend(
        f"documented as not passing, but passed: {test_id}"
        for test_id in sorted(documented - not_passing)
    )

    print()
    print(
        f"ran={result.testsRun} not_passing={len(not_passing)} "
        f"skipped={len(result.skipped)}"
    )
    for problem in problems:
        print(f"OUTCOME MISMATCH: {problem}")
    if problems:
        return 1
    print("outcome matches the documented one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
