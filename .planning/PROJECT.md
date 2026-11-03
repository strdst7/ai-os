# AI-OS — Private API Deployment Readiness

## What This Is

AI-OS has a Streamlit demonstration and a separate FastAPI service for scoring and recording observations. This milestone prepares the private FastAPI deployment decision and the checks an operator must complete on its actual host. No deployment host is selected yet, so the milestone cannot establish production readiness.

## Core Value

Do not claim durable, recoverable private API observations without evidence from the actual deployment host.

## Requirements

### Validated

- ✓ The FastAPI service authenticates non-health routes and stores observation, replay identity, and anomaly state in SQLite — existing code and CI checks.
- ✓ Disposable Docker checks cover restart, recreation, backup, restore, SQLite integrity, and ENOSPC recovery — CI evidence in `docs/operational-readiness-005c.md`.
- ✓ Streamlit dashboard history remains session-local and separate from API storage — existing code.

### Active

- [ ] Identify a private FastAPI host and an operator responsible for storage, backups, alerts, and restore drills.
- [ ] Decide whether the host's topology supports a single API process and persistent SQLite volume.
- [ ] Define checks for the actual mount, database path, ownership, permissions, and state after restart and recreation.
- [ ] Define an automated backup schedule, retention, off-volume destination, and error notification check.
- [ ] Define an isolated restore drill covering observation history, anomaly state, replay identity, and SQLite integrity.
- [ ] Define host disk-capacity alerts and backup/write error handling without filling production storage.
- [ ] Require a security review before any public API exposure.

### Out of Scope

- Production-readiness approval now — no private API host or operator is identified.
- Changing recovery thresholds — labeled incidents, cadence, and an accepted false-clear target are missing.
- Streamlit demo changes — session-local UI is a separate workstream.
- New database, Redis, or architecture refactor — no deployment topology calls for them.

## Context

- The public Streamlit Community Cloud URL starts `app.py`, not the Docker/FastAPI service.
- The Docker image requires an absolute `AIOS_OBSERVATION_DB` path; this does not prove a persistent host mount.
- The seven `.planning/codebase/` maps document existing behavior and source-level concerns.
- `docs/operational-readiness-005c.md` records passing disposable CI checks and four open deployment-host gates.
- PR #9 remains open for documentation and Python 3.10 dependency compatibility. This planning work remains local unless the user asks to publish it.

## Constraints

- **Host:** No private FastAPI host yet — stop at host selection and executable check plans until access exists.
- **Security:** Keep the API private; review security before public exposure.
- **Data safety:** Do not fill a production volume or treat CI volumes as host evidence.
- **Recovery:** Do not alter the two-Stable rule without labeled incident evidence and an approved target.
- **Architecture:** Prefer the existing single-process SQLite design only when the chosen deployment topology supports it.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Separate Streamlit demo from API readiness | They do not share durable observation state. | ✓ Existing boundary |
| Plan host and operator discovery first | Neither is available yet. | — Pending |
| Keep API private | Security review is incomplete. | — Pending |
| Keep PR #9 and planning changes separate | Avoid changing the active pull request's scope. | — Pending |

## Evolution

Review requirements, core value, boundaries, and decisions after each phase and milestone. Move active requirements only when actual evidence supports them.

---
*Last updated: 2026-11-03 after project initialization*
