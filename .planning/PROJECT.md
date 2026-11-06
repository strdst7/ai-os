# AI-OS production API readiness

## What This Is

AI-OS has a session-local Streamlit demo and a separate FastAPI/SQLite service. This milestone selects an eligible stateful API host and records the evidence needed before production approval. It does not deploy or approve the API.

## Core Value

Keep the API private until its actual host satisfies the production acceptance gates.

## Requirements

### Active

- [ ] Select a host and operator, or record a blocked decision.
- [ ] Define host-specific volume, backup, restore, disk-alert, and security evidence.

### Out of Scope

- Production deployment or approval — target-host evidence and security review are missing.
- New application, UI, database, or deployment stack — this is a decision-only milestone.
- Recovery-rule calibration — labeled incidents and an operator-approved false-clear target are absent.

## Context

`app.py` runs the Streamlit demo, not the stateful API. `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md` list the outstanding host gates. No API host is selected. Main matches `origin/main` at `2893451d1a2cab3682e5c65d30568a23868520e8`.

## Constraints

- **Topology:** One host and one replica for SQLite.
- **Safety:** Do not run `tests/full_volume.py` on local or production storage.
- **Evidence:** CI simulations cannot substitute for target-host checks.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Select a host before implementation | Streamlit Community Cloud does not host the API | Pending |
| Keep the API private | Host checks and security review remain open | Active |

---
*Last updated: 2026-11-07 after milestone scoping*
