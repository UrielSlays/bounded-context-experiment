// Strict Draft 2020-12 compilation + fixture/mutant validation for the two BUILD
// trust-root schemas. Mirrors verify-r13-schema-ajv.mjs (same vendored AJV bundle,
// same strict-mode contract, same "a schema that accepts a mutant is a failure" shape).
//
// Subjects:
//   MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json   (schema under .schema)
//     + MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json
//   MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json (the document IS the schema)
//     + MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json
//
// Usage: node verify-build-schema-ajv.mjs [--compile-only]

import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { createAjv } = require(path.join(root, "vendor", "ajv-r12.bundle.cjs"));

const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));

function fail(message, errors = []) {
  process.stderr.write(`${message}\n${JSON.stringify(errors, null, 2)}\n`);
  process.exit(1);
}

const ajv = createAjv();
const subjects = {
  state_trust_root_manifest_v1: {
    validate: ajv.compile(
      readJson("MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json").schema),
    fixture: "MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json",
  },
  measurement_trust_root_manifest_v3: {
    validate: ajv.compile(
      readJson("MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json")),
    fixture: "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json",
  },
};

if (process.argv[2] === "--compile-only") {
  process.stdout.write("AJV_BUILD_STRICT_COMPILE_OK\n");
  process.exit(0);
}
if (process.argv.length !== 2) {
  fail("usage: node verify-build-schema-ajv.mjs [--compile-only]");
}

// Each mutant must be REJECTED. A schema that accepts one is not a closed contract.
const mutants = [
  ["extra top-level field", (row) => { row.__unexpected_build_field = true; }],
  ["missing schema_id", (row) => { delete row.schema_id; }],
  ["extra field inside a root row", (row) => { row.roots[0].__unexpected = true; }],
  ["fabricated validity window", (row) => { row.validity.not_before = "whenever"; }],
  ["non-SHA-384 policy digest", (row) => {
    if ("trust_policy_digest" in row) row.trust_policy_digest = "not-a-digest";
    else row.roots[0].trust_policy_digest = "not-a-digest";
  }],
  ["public key replaced by a label", (row) => { row.roots[0].public_key_pem = "TRUSTED"; }],
];

const report = {};
for (const [name, subject] of Object.entries(subjects)) {
  const fixture = readJson(subject.fixture);
  if (!subject.validate(fixture)) {
    fail(`schema rejected the committed ${name} fixture`, subject.validate.errors);
  }
  if (fixture.production_ready !== false) {
    fail(`committed ${name} fixture is not production_ready:false`);
  }
  for (const [label, mutate] of mutants) {
    const mutant = structuredClone(fixture);
    mutate(mutant);
    if (subject.validate(mutant)) fail(`schema accepted mutant: ${name} / ${label}`);
  }
  report[name] = { fixture: subject.fixture, mutants_rejected: mutants.length };
}
process.stdout.write(`${JSON.stringify({ ok: true, subjects: report })}\n`);
process.stdout.write("AJV_BUILD_FIXTURE_AND_MUTANTS_OK\n");
