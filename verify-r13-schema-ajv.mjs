import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { createAjv } = require(path.join(root, "vendor", "ajv-r12.bundle.cjs"));

const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
const ajv = createAjv();
const stateContract = readJson("MBCX-01-STATE-TRANSITION-CONTRACT-v8.json");
const measurementContract = readJson("MBCX-01-MEASUREMENT-CONTRACT-v7.json");
const validators = {
  event: ajv.compile(stateContract.event_schema),
  state_authority_receipt: ajv.compile(stateContract.state_authority_receipt_schema),
  scorer_input: ajv.compile(readJson("MBCX-01-PACKET-SCHEMAS-v7.json").schema),
  signed_measurement_envelope: ajv.compile(measurementContract.signed_measurement_envelope_schema),
  carrier_exactness_receipt: ajv.compile(measurementContract.carrier_exactness_receipt_schema),
};

function fail(message, errors = []) {
  process.stderr.write(`${message}\n${JSON.stringify(errors, null, 2)}\n`);
  process.exit(1);
}

if (process.argv[2] === "--compile-only") {
  process.stdout.write("AJV_R13_STRICT_COMPILE_OK\n");
  process.exit(0);
}
if (process.argv.length !== 3) {
  fail("usage: node verify-r13-schema-ajv.mjs <fixture.json> | --compile-only");
}

const fixture = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
for (const [name, validate] of Object.entries(validators)) {
  if (!validate(fixture[name])) fail(`schema rejected valid ${name}`, validate.errors);
  const mutant = structuredClone(fixture[name]);
  mutant.__unexpected_r13_field = true;
  if (validate(mutant)) fail(`schema accepted extra-field ${name}`);
}

const nestedMutants = [
  ["calendar-impossible UTC", "event", (row) => { row.observed_at = "2026-99-99T99:99:99.999999Z"; }],
  ["state authority production forgery", "state_authority_receipt", (row) => { row.authority_mode = "PRODUCTION"; }],
  ["transition authority extra field", "scorer_input", (row) => { row.transition_authority.__unexpected_r13_field = true; }],
  ["state receipt extra field", "scorer_input", (row) => { row.state_authority_receipt.__unexpected_r13_field = true; }],
  ["signed evidence omission", "signed_measurement_envelope", (row) => { delete row.receipt.job_receipt.evidence.completion; }],
  ["signature algorithm confusion", "signed_measurement_envelope", (row) => { row.algorithm = "NONE"; }],
  ["exactness production label forgery", "carrier_exactness_receipt", (row) => { row.authority_mode = "PRODUCTION"; }],
];
for (const [label, schemaName, mutate] of nestedMutants) {
  const mutant = structuredClone(fixture[schemaName]);
  mutate(mutant);
  if (validators[schemaName](mutant)) fail(`schema accepted nested mutant: ${label}`);
}
process.stdout.write("AJV_R13_FIXTURE_AND_MUTANTS_OK\n");
