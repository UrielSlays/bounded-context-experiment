"""Witnesses for expect_suite_outcome.py.

A probe suite holds one test for every way `unittest` can report a test as
not passing. The checker must accept the run only when each of those tests is
documented, and must name whatever differs.

Run from the repository root:

    python -m unittest discover -s .github/scripts -p "test_*.py"
"""

from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import expect_suite_outcome  # noqa: E402


PROBE_MODULE = "probe_outcomes"
PROBE_SOURCE = textwrap.dedent(
    '''
    import unittest


    class Probe(unittest.TestCase):
        def test_passes(self):
            pass

        def test_fails(self):
            self.fail("fails")

        def test_errors(self):
            raise RuntimeError("errors")

        def test_fails_in_a_subtest(self):
            for value in (1, 2):
                with self.subTest(value=value):
                    self.assertEqual(value, 1)

        @unittest.expectedFailure
        def test_fails_as_expected(self):
            self.fail("expected failure")

        @unittest.expectedFailure
        def test_passes_unexpectedly(self):
            pass

        @unittest.skip("skipped")
        def test_is_skipped(self):
            pass
    '''
)

# Every probe test that does not pass, one per unittest result bucket:
# failures, errors, a failing subTest, expectedFailures, unexpectedSuccesses.
NOT_PASSING = tuple(
    f"{PROBE_MODULE}.Probe.{name}"
    for name in (
        "test_fails",
        "test_errors",
        "test_fails_in_a_subtest",
        "test_fails_as_expected",
        "test_passes_unexpectedly",
    )
)
PASSING = f"{PROBE_MODULE}.Probe.test_passes"
SKIPPED = f"{PROBE_MODULE}.Probe.test_is_skipped"
RAN = 7


class ExpectSuiteOutcomeTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        Path(directory.name, f"{PROBE_MODULE}.py").write_text(
            PROBE_SOURCE, encoding="utf-8"
        )
        previous = os.getcwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(directory.name)
        # Discovery puts the start directory on sys.path and caches the probe
        # module; undo both so every test loads its own copy.
        path_before = list(sys.path)
        self.addCleanup(sys.path.__setitem__, slice(None), path_before)
        self.addCleanup(sys.modules.pop, PROBE_MODULE, None)

    def check(self, *arguments: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = expect_suite_outcome.main(
                ["--pattern", f"{PROBE_MODULE}.py", *arguments]
            )
        return code, output.getvalue()

    def test_the_documented_outcome_is_accepted(self) -> None:
        code, output = self.check(
            "--ran", str(RAN), "--skipped", "1", "--not-passing", *NOT_PASSING
        )
        self.assertEqual(code, 0, output)
        self.assertIn("outcome matches the documented one", output)

    def test_every_kind_of_non_pass_must_be_documented(self) -> None:
        for undocumented in NOT_PASSING:
            with self.subTest(undocumented=undocumented):
                documented = [test for test in NOT_PASSING if test != undocumented]
                code, output = self.check(
                    "--ran", str(RAN), "--skipped", "1", "--not-passing", *documented
                )
                self.assertEqual(code, 1, output)
                self.assertIn(
                    f"OUTCOME MISMATCH: not passing and not documented: {undocumented}\n",
                    output,
                )

    def test_a_documented_failure_that_passes_is_reported(self) -> None:
        code, output = self.check(
            "--ran", str(RAN), "--skipped", "1", "--not-passing", *NOT_PASSING, PASSING
        )
        self.assertEqual(code, 1, output)
        self.assertIn(
            f"OUTCOME MISMATCH: documented as not passing, but passed: {PASSING}\n",
            output,
        )

    def test_a_different_test_count_is_reported(self) -> None:
        code, output = self.check(
            "--ran", str(RAN + 1), "--skipped", "1", "--not-passing", *NOT_PASSING
        )
        self.assertEqual(code, 1, output)
        self.assertIn(f"OUTCOME MISMATCH: ran {RAN} tests, expected {RAN + 1}\n", output)

    def test_a_skipped_test_is_reported_by_name(self) -> None:
        code, output = self.check("--ran", str(RAN), "--not-passing", *NOT_PASSING)
        self.assertEqual(code, 1, output)
        self.assertIn("OUTCOME MISMATCH: skipped 1 tests, expected 0\n", output)
        self.assertIn(f"OUTCOME MISMATCH: skipped: {SKIPPED}\n", output)

    def test_a_module_that_does_not_import_is_reported(self) -> None:
        Path(f"{PROBE_MODULE}.py").write_text("import no_such_module\n", encoding="utf-8")
        code, output = self.check("--ran", "1")
        self.assertEqual(code, 1, output)
        self.assertIn("OUTCOME MISMATCH: not passing and not documented: ", output)
        self.assertIn(PROBE_MODULE, output)


if __name__ == "__main__":
    unittest.main()
