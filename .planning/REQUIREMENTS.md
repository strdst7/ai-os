# Requirements: AI-OS Private API Deployment Readiness

**Defined:** 2026-11-03
**Core Value:** Do not claim durable, recoverable private API observations without evidence from the actual deployment host.

## v1 Requirements

This milestone ends with a host decision and runnable check plan. Live deployment checks remain blocked without host access.

### Host decision

- [ ] **HOST-01**: Operator can identify a candidate private FastAPI host, owner, and access prerequisites, or record that none exists.
- [ ] **HOST-02**: Operator can decide whether a single process and persistent SQLite volume fit the candidate topology, or mark the decision blocked until topology is known.

### Deployment checks

- [ ] **DATA-01**: Operator can follow a host-specific check for mount, database path, ownership, permissions, and state after restart and recreation.
- [ ] **BACK-01**: Operator can follow a backup check that records frequency, retention, off-volume destination, and error notification.
- [ ] **BACK-02**: Operator can follow an isolated restore check for history, anomaly state, replay identity, and SQLite integrity.
- [ ] **ALRT-01**: Operator can follow a disk-alert and storage-error check without filling production storage.
- [ ] **SECU-01**: Operator can keep API exposure private until a security review explicitly approves the boundary.

## v2 Requirements

- **LIVE-01**: Operator can run the checks on the selected host and record actual evidence after access exists.
- **RECV-01**: Operator can calibrate recovery against labeled incidents, cadence, and an approved false-clear target.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Production approval | Host and operator are not identified. |
| Streamlit dashboard updates | Separate session-local demo. |
| Redis, database migration, architecture refactor | Deployment topology has not shown a need. |
| Production disk-filling test | Risks data loss; use non-destructive checks. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| HOST-01 | Phase 1 | Pending |
| HOST-02 | Phase 1 | Pending |
| DATA-01 | Phase 2 | Pending |
| BACK-01 | Phase 2 | Pending |
| BACK-02 | Phase 2 | Pending |
| ALRT-01 | Phase 2 | Pending |
| SECU-01 | Phase 2 | Pending |

**Coverage:** Seven v1 requirements, seven mapped, zero unmapped.

---
*Requirements defined: 2026-11-03*
*Last updated: 2026-11-03 after initial definition*
