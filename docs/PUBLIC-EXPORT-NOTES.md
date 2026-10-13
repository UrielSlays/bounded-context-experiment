# Public export notes

This repository is a public-facing export of the private working repository used to develop and review MBCX-01.

The experiment preserves provenance through pinned hashes. A small number of reviewed files are therefore published without rewriting workstation paths or references to sibling private repositories, because changing those bytes would break the pins that identify what was reviewed.

## Differences from the working repository

- Raw review-tool logs are omitted.
- Sensitive material printed in retained logs is redacted.
- Seven pinned files retain workstation paths because they are published as reviewed:
  - `MBCX-01-BUILD-SHELF-LOG.md`
  - `MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md`
  - `MBCX-01-R12-PRIOR-ART-AND-SHELF-MEMO.md`
  - `MBCX-01-R13.1-SHELF-QUERY-LOG.md`
  - `run-smoke-cell.ps1`
  - `verify-r10-pinned.ps1`
  - `verify-r10-schema-ajv.mjs`
- Names of sibling private repositories are left as written. They appear in pinned files, in scripts from earlier rounds, and in the review record under `review/`.
- Vendor bundles retain relative build paths from their source.
- Keys present in the repository are test fixtures, not production credentials.

## Reproduction boundary

Most of the test suite runs from this export. One test (`bc14`) and one verifier reference a commit from the private working repository and therefore stop early here rather than silently substituting a different provenance root.

A full run log produced from the working repository is retained under `docs/presentation/data/`.

The export preserves these boundaries deliberately: a public copy should not claim to reproduce checks whose exact private inputs are unavailable.
