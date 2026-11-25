# Requirements: AI-OS production API readiness

**Defined:** 2026-11-07
**Core Value:** Keep the API private until its actual host can satisfy the documented production acceptance gates.

## v1 Requirements

### Host decision

- [ ] **HOST-01**: An operator can select a named stateful API host, or record a blocked decision when none meets the one-host, one-replica SQLite constraint.
- [ ] **HOST-02**: The decision records the operator, API runtime, persistent mount path, and why Streamlit Community Cloud is not the API host.

### Acceptance evidence

- [ ] **GATE-01**: The decision records the host-volume, backup schedule, restore drill, and disk-monitoring checks with an owner and evidence source for each.
- [ ] **GATE-02**: The decision records security review as a separate prerequisite to public exposure and distinguishes proposed checks from completed host evidence.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Deploy the API or mark it production-approved | No host or real host evidence exists yet |
| Build a new app, database, or dashboard | Existing services cover the research demo and API |
| Change anomaly recovery policy | Labeled incidents and a false-clear target are absent |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| HOST-01 | Phase 1 | Pending |
| HOST-02 | Phase 1 | Pending |
| GATE-01 | Phase 1 | Pending |
| GATE-02 | Phase 1 | Pending |

**Coverage:** 4 v1 requirements; 4 mapped; 0 unmapped.

---
*Requirements defined: 2026-11-07*
