<!-- GSD:project-start source:PROJECT.md -->
## Project

**AI-OS — Private API Deployment Readiness**

AI-OS has a Streamlit demonstration and a separate FastAPI service for scoring and recording observations. This milestone prepares the private FastAPI deployment decision and the checks an operator must complete on its actual host. No deployment host is selected yet, so the milestone cannot establish production readiness.

**Core Value:** Do not claim durable, recoverable private API observations without evidence from the actual deployment host.

### Constraints

- **Host:** No private FastAPI host yet — stop at host selection and executable check plans until access exists.
- **Security:** Keep the API private; review security before public exposure.
- **Data safety:** Do not fill a production volume or treat CI volumes as host evidence.
- **Recovery:** Do not alter the two-Stable rule without labeled incident evidence and an approved target.
- **Architecture:** Prefer the existing single-process SQLite design only when the chosen deployment topology supports it.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Runtime and languages
- Python is the application language. `Dockerfile` uses `python:3.10-slim` for both stages.
- GitHub Actions runs Python 3.10 in `.github/workflows/ci.yml`.
- `.gitlab-ci.yml` also names a Python 3.10 test image and a Docker image build.
- `app.py` is a separate Streamlit dashboard. `src/main.py` is the FastAPI API.
## Dependencies
- `requirements.txt` declares FastAPI, Uvicorn, Pydantic, NumPy, Pandas, Matplotlib, scikit-learn, pytest, pytest-cov, HTTPX, and Streamlit.
- Streamlit uses environment markers: `>=1.65,<1.66` on Python below 3.11 and `>=1.66.1` on Python 3.11+.
- `src/stability_engine.py` imports NumPy for mean and standard deviation.
- `src/services/monitoring_service.py` uses standard-library `sqlite3`, `json`, `pathlib`, and `threading`.
- No lockfile exists. The other dependencies have no version caps in `requirements.txt`.
## Build and run
- `Dockerfile` installs `requirements.txt`, copies `src/` and `app.py`, and runs one Uvicorn process on port 8000.
- The image sets `AIOS_REQUIRE_PERSISTENCE=1`; it needs an absolute `AIOS_OBSERVATION_DB` path.
- `README.md` shows `streamlit run app.py` for the dashboard. It does not start the API.
- CI invokes `pytest tests --cov=src` and `tests/container_lifecycle.py` on isolated runners.
- `tests/full_volume.py` runs only on an explicitly opted-in disposable Docker runner.
## Configuration
- `AIOS_API_KEY` protects non-health API routes through `src/auth.py`.
- `AIOS_OBSERVATION_DB` selects SQLite storage. Without image persistence mode, `:memory:` is the local default.
- `src/config.py` fixes the displayed history limit at 20 and monitor interval at 10 seconds.
- `.planning/config.json` contains local GSD workflow preferences, not application runtime config.
## Deployment distinction
- `app.py` keeps chart history in `st.session_state`. It does not call `src/main.py` or use SQLite.
- `docs/operational-readiness-005c.md` distinguishes disposable CI results from untested deployment-host gates.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Python layout
- Modules use lowercase names under `src/`; tests follow `tests/test_*.py`.
- Most functions use snake_case. `MonitoringService` and Pydantic `Telemetry` use class names.
- `src/main.py` keeps route handlers short and delegates evaluation to `MonitoringService`.
- `src/agent.py` assembles the report from score helpers and guardrail classification.
- Imports and blank-line spacing vary between modules. No formatter or linter config was found.
## Data contracts
- `src/models.py` uses strict bounded floats, forbidden extra fields, and an optional UUID.
- `src/stability_engine.py` validates the four required metrics again for direct callers.
- `src/agent.py` timestamps reports in UTC and preserves ADSI before display rounding.
- `src/services/monitoring_service.py` serializes canonical metric input with sorted compact JSON for replay checks.
- The API's display history is bounded; the SQLite observation table retains IDs beyond that window.
## Errors and state
- `src/auth.py` returns HTTP 503 for bad server key config and 401 for invalid caller credentials.
- `src/services/monitoring_service.py` returns HTTP 409 for conflicting observation ID reuse.
- SQLite evaluation begins `BEGIN IMMEDIATE` and rolls back on exceptions.
- `src/main.py` has no custom ENOSPC handler; a storage write error yields generic HTTP 500.
- `src/main.py` disables API docs and uses an async lifespan for its monitoring task.
- `tests/full_volume.py` refuses dangerous execution without opt-in, free-space, mount-type, and capacity checks.
## Tests and comments
- `tests/test_p0_integrity.py` uses pytest monkeypatch, tmp_path, parametrization, and TestClient.
- `tests/test_recovery_calibration.py` uses controlled time and a real SQLite file to characterize behavior.
- `tests/container_lifecycle.py` uses standard-library subprocess and urllib around Docker.
- Comments marked `ponytail:` in `src/services/monitoring_service.py` state explicit scope ceilings.
- `CONTRIBUTING.md` asks contributors to keep monitoring deterministic and include tests.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System boundary
- The repository holds two distinct entrypoints: `app.py` for a Streamlit demonstration and `src/main.py` for an API.
- Both use scoring from `src/stability_engine.py`, but the dashboard does not call the API or share its SQLite state.
- `Dockerfile` starts `src.main:app`, not the Streamlit dashboard.
## API data flow
## Persistence and concurrency
- `src/services/monitoring_service.py` has unique observation IDs and serializes local connection access with a lock.
- `BEGIN IMMEDIATE` protects duplicate lookup and insert across SQLite connections.
- The durable table keeps all rows. `MonitoringConfig.HISTORY_LIMIT` only limits returned history.
- Reuse of an ID with different input returns HTTP 409. Identical input with that ID returns its original report.
- Without an ID, only a consecutive equal payload is treated as replay.
- Docker mode rejects a missing or relative database path. A path check alone does not establish a host mount.
## Alert behavior
- A Critical observation latches anomaly state in `src/services/monitoring_service.py`.
- Two fresh consecutive Stable observations clear the latch. Warning or Critical resets the recovery counter.
- Elapsed time is not part of this rule. `tests/test_recovery_calibration.py` documents the one-second/day equivalence.
- `src/main.py` starts an asynchronous monitoring loop. Its `autonomous_check` reads state without adding an observation.
## Dashboard path
- `app.py` reads sidebar sliders and calls `calculate_adsi`, `detect_degradation`, and `detect_anomaly`.
- Streamlit `st.session_state.history` holds dashboard points for that user session only.
- The "Simulate Degradation" button creates random metrics, but the following sidebar assignment replaces them before scoring.
## Deployment boundary
- `tests/container_lifecycle.py` and `tests/full_volume.py` check disposable Docker volumes.
- `docs/operational-readiness-005c.md` leaves actual mount, scheduled backup, restore drill, and disk alerts open.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
