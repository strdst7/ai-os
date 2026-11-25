---
phase: "01"
slug: host-selection-and-evidence-plan
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-25"
---

# Phase 01 — Validation Strategy

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | pytest |
| Config file | `requirements.txt` |
| Quick run command | `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pytest -q tests/test_host_decision_record.py` |
| Full suite command | Not run for this documentation-only phase; `tests/full_volume.py` requires a disposable environment. |
| Targeted runtime | 0.01 seconds for two tests |

## Sampling Rate

- **After task changes:** Run the targeted document tests.
- **After this wave:** The targeted document tests passed, 2/2.
- **Before host approval:** Run checks against the named target host. These tests do not provide host evidence.
- **Feedback latency:** Under one second for the targeted tests.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01-01-01 | 01 | 1 | HOST-01, HOST-02 | T-01-01, T-01-03 | Decision blocked; API private | document | `python3 -m pytest -q tests/test_host_decision_record.py` using the Python path above | Yes | Green |
| 01-01-02 | 01 | 1 | GATE-01, GATE-02 | T-01-02, T-01-04, T-01-SC | Five pending gates; CI stays background | document | `python3 -m pytest -q tests/test_host_decision_record.py` using the Python path above | Yes | Green |

## Wave 0 Requirements

Existing pytest infrastructure covers both tasks. No dependency was installed.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Target-host readiness | HOST-01, HOST-02, GATE-01, GATE-02 | No host or operator exists. | Name both, assign gate owners, then gather real host evidence. |

## Validation Sign-Off

- [x] Both tasks have automated checks.
- [x] No consecutive tasks lack automated checks.
- [x] No missing test infrastructure remains for this document.
- [x] Tests run without watch mode.
- [x] Targeted feedback completes within one second.
- [x] `nyquist_compliant: true` covers document checks only.

**Approval:** Document-check coverage only. Production approval remains pending.
