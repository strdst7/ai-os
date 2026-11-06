# Requirements: AI-OS production API readiness

**Defined:** 2026-11-07
**Core Value:** Keep the API private until its actual host satisfies the production acceptance gates.

## v1 Requirements

### Host decision

- [ ] **HOST-01**: Record a named stateful API host and operator, or a blocked decision when no eligible host is selected.
- [ ] **HOST-02**: Record the runtime, persistent mount path, one-host/one-replica constraint, and Streamlit's separate role.

### Acceptance evidence

- [ ] **GATE-01**: Record host-volume, backup schedule, restore drill, and disk-alert checks with evidence requirements and owners.
- [ ] **GATE-02**: Record security review as a separate prerequisite to public exposure and distinguish proposed from completed evidence.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Deployment or approval | Actual host and evidence are unavailable |
| New app, database, or dashboard | Existing runtimes cover these |
| Recovery policy change | Labeled incidents and false-clear target are absent |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| HOST-01 | Phase 1 | Pending |
| HOST-02 | Phase 1 | Pending |
| GATE-01 | Phase 1 | Pending |
| GATE-02 | Phase 1 | Pending |

**Coverage:** 4 v1 requirements; 4 mapped; 0 unmapped.
