---
phase: "01"
slug: "host-and-ownership-decision"
status: draft
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-05"
---

# Phase 01 — Validation Strategy

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Markdown source assertions and GSD plan checker |
| Config file | `.planning/REQUIREMENTS.md` |
| Quick run command | `git diff --check` |
| Full suite command | `gsd_run query check.decision-coverage-plan .planning/phases/01-host-and-ownership-decision .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md` |
| Estimated runtime | Unmeasured |

## Sampling Rate

- After each task commit: run `git diff --check` and read the decision record.
- After each wave: check both HOST requirements against the decision record.
- Before `/gsd-verify-work`: check the decision record and plan coverage.
- Max feedback latency: Unmeasured.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01-01-01 | 01 | 1 | HOST-01 | — | No credentials or host access implied | Document review | `git diff --check` | ✅ | ⬜ pending |
| 01-01-01 | 01 | 1 | HOST-02 | — | Unknown topology remains blocked | Document review | `git diff --check` | ✅ | ⬜ pending |

## Wave 0 Requirements

None. Existing planning context defines both requirements.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Candidate and owner decision | HOST-01 | No candidate host exists | Read the record. Check MIA owns selection, access remains unproven, and authorized users remain undecided. |
| SQLite and volume fit | HOST-02 | Host topology is unknown | Read the record. Check process count, replica count, mount, and fit remain blocked. |

## Validation Sign-Off

- [ ] Plan tasks name both HOST requirements.
- [ ] Manual review finds no invented host evidence.
- [ ] Plan checker accepts the plan.
- [ ] Set `nyquist_compliant: true` only after the checks pass.

**Approval:** pending
