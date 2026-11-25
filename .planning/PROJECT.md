# AI-OS production API readiness

## What This Is

AI-OS contains a session-local Streamlit research demo and a separate FastAPI service with SQLite observations. This milestone selects an eligible host for the stateful API and defines the evidence needed before production approval. It does not deploy or approve the service.

## Core Value

Keep the API private until its actual host can satisfy the documented production acceptance gates.

## Requirements

### Validated

- The disposable CI container lifecycle and full-volume checks passed. These do not establish production readiness.
- Phase 1 recorded the blocked host decision and five pending evidence gates.

### Active

- [ ] Name a candidate and operator for the one-host, one-replica SQLite service.
- [ ] Assign gate owners and gather target-host evidence for volume, backup, restore, disk alerts, and security review.

### Out of Scope

- Public API exposure or production approval — needs actual host evidence and security review.
- New application, UI, database, or deployment stack — this is a decision-only milestone.
- Recovery-rule calibration — needs labeled incidents and an operator-approved target.

## Context

The Streamlit Community Cloud entrypoint is `app.py` and does not host the Docker/FastAPI service. `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md` record the four outstanding host gates. No stateful API host has been selected. Planning uses `origin/main` at `21111250686e183b55462c175e1f2d748ccb6948` on 2026-11-25.

## Constraints

- **Topology:** One host and one replica for SQLite; reassess before scaling.
- **Safety:** Never run `tests/full_volume.py` on the local or production host.
- **Evidence:** CI simulations cannot replace checks on the selected host.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Decide host before implementation | The current Streamlit site cannot provide the API's stateful storage | Pending |
| Keep the API private | Host checks and security review remain open | Active |
| Record blocked decision | No API host candidate or operator was named | Complete — Phase 1 |

---
*Last updated: 2026-11-25 after Phase 1 execution*
