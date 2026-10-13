# Security

## Committed private keys

This repository contains eight Ed25519 private keys, committed on purpose. They are test and attacker fixtures and are deliberately public. The test suite uses them to sign test material and to prove that the production doors refuse committed and attacker-authored keys; they are never used for anything else. They appear in these six files:

- `mbcx01_build_ceremony_fixture.py`
- `mbcx01_build_trustboot_probe.py`
- `test_mbcx01_build_measurement.py`
- `test_mbcx01_build_state.py`
- `test_mbcx01_r12_measurement.py`
- `test_mbcx01_r13_measurement.py`

## Reporting a problem

To report a real security problem, email contact@moonwalkercorp.com.
