---
phase: "01"
slug: host-selection-and-evidence-plan
status: verified
threats_open: 0
asvs_level: 1
created: "2026-11-25"
---

# Phase 01 — Security

This check covers the decision record's mitigations. It grants no production security approval.

## Trust Boundaries

| Boundary | Description | Data Crossing |
| --- | --- | --- |
| Disposable CI → production decision | CI cannot establish target-host readiness. | CI test results |
| Streamlit demo → stateful API | The session-local demo cannot host the SQLite writer. | Observation history |
| Private API → public exposure | Host evidence and separate security approval remain prerequisites. | API requests and observations |

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-01-01 | Spoofing | Decision record host identity | high | mitigate | Candidate and operator remain pending. The user names both before reopening. | closed |
| T-01-02 | Tampering | Evidence matrix | high | mitigate | Every source remains pending. CI results remain background only. | closed |
| T-01-03 | Information disclosure | API exposure boundary | high | mitigate | The API stays private until host evidence and separate security approval exist. | closed |
| T-01-04 | Denial of service | SQLite storage | medium | mitigate | Disk alert checks remain pending. The plan forbids filling production storage. | closed |
| T-01-SC | Tampering | Package supply chain | high | mitigate | This documentation phase installed no packages. Future installs require a package audit. | closed |

These closures describe the Phase 1 document. Host controls and public-exposure approval remain pending.

## Accepted Risks Log

No risks accepted.

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
| --- | --- | --- | --- | --- |
| 2026-11-25 | 5 | 5 | 0 | Phase 1 documentation check |

## Sign-Off

- [x] All registered threats have a disposition.
- [x] No risks were accepted.
- [x] `threats_open: 0` for the Phase 1 documentation mitigations.
- [x] `status: verified` for the Phase 1 documentation check.

**Approval:** Documentation check complete. Production security approval remains pending.
