# External Integrations

**Analysis Date:** 2026-11-23

## APIs and external services

**Inbound HTTP:**

* FastAPI serves `GET /health`, `POST /agent/evaluate`, and `GET /observability`; `/docs`, `/redoc`, and `/openapi.json` are disabled (`src/main.py`, `docs/API.md`).
  * SDK/Client: FastAPI and Uvicorn server (`requirements.txt`, `Dockerfile`); clients send HTTP requests, not an in-repo SDK (`src/main.py`).
  * Auth: `AIOS_API_KEY` passed via `x-api-key` for evaluation and observability; health is public (`src/auth.py`, `src/main.py`).

**Outbound APIs:**

* Not detected in runtime code: scoring and dashboard operate locally; `httpx` is declared but not imported by application code (`requirements.txt`, `src/`, `app.py`). Docker test harnesses use standard-library HTTP requests to their temporary local containers (`tests/container_lifecycle.py`, `tests/full_volume.py`).

## Data storage

**Databases:**

* SQLite, Python standard-library `sqlite3` - observations, cached reports, and persistent anomaly/recovery state in `observations` and `monitor_state` tables (`src/services/monitoring_service.py`).
  * Connection: `AIOS_OBSERVATION_DB`; defaults to `:memory:` outside persistence-enforced mode; use a writable absolute file path with the container (`src/services/monitoring_service.py`, `Dockerfile`).
  * Client: `sqlite3.connect(..., check_same_thread=False, isolation_level=None)` guarded by a process-local `threading.Lock`, explicit `BEGIN IMMEDIATE`/commit/rollback on writes (`src/services/monitoring_service.py`). Treat this as a one-writer, one-host store (`docs/DEPLOYMENT.md`).

**File Storage:**

* Local filesystem only: SQLite database at the configured path; the image does not create or mount persistent storage. Backups are exercised using SQLite's backup API in disposable tests, not scheduled by the application (`src/services/monitoring_service.py`, `Dockerfile`, `tests/container_lifecycle.py`, `docs/DEPLOYMENT.md`).
* Dashboard history lives in per-browser-session `st.session_state` rather than the SQLite store (`app.py`). `data/sample_telemetry.json` is repository sample input, not an external store.

**Caching:**

* No external cache. In-memory SQLite is the API local default and dashboard state is session-local (`src/services/monitoring_service.py`, `app.py`).

## Authentication and identity

**Auth Provider:**

* Custom static API-key check; no external identity provider (`src/auth.py`, `src/main.py`).
  * Implementation: `verify_api_key` validates the configured `AIOS_API_KEY` length and format, compares `x-api-key` with `hmac.compare_digest`, returns HTTP 401 on mismatch or HTTP 503 when server key is invalid/missing (`src/auth.py`). Attach `Depends(verify_api_key)` to private routes as in `src/main.py`. `app.py` is separate and has no API-key integration.

## Monitoring and observability

**Error Tracking:**

* No external error-tracking service detected (`src/main.py`, `src/services/monitoring_service.py`, `requirements.txt`). SQLite operational failures map to retryable HTTP 503 responses without exposing SQLite internals (`src/main.py`).

**Logs:**

* Uvicorn process output; `PYTHONUNBUFFERED=1` is set in the image. No configured log sink or alert delivery appears in the repository (`Dockerfile`, `src/main.py`, `docs/DEPLOYMENT.md`).
* API `GET /observability` returns recent history and anomaly state; an asyncio lifespan task calls read-only `autonomous_check` on the `src/config.py` interval (`src/main.py`, `src/services/monitoring_service.py`). `GET /health` reports service status but does not test database health (`src/main.py`).

## CI/CD and deployment

**Hosting:**

* Streamlit Community Cloud is identified as the separate dashboard's named demo host, but deployed source revision/live behavior are unconfirmed (`docs/DEPLOYMENT.md`, `app.py`).
* Docker image hosts the FastAPI API on port 8000 when run by an operator; the GitLab CI build publishes images to its container registry but does not deploy a running backend (`Dockerfile`, `.gitlab-ci.yml`, `docs/DEPLOYMENT.md`). No Docker Compose, Kubernetes, or stateful host deployment manifest is present (`docs/DEPLOYMENT.md`).

**CI Pipeline:**

* GitHub Actions tests `dev` pushes, `main` pull requests and manual dispatch; runs pytest with source coverage and a Docker lifecycle test. Manual opt-in runs disposable full-volume checks (`.github/workflows/ci.yml`, `tests/container_lifecycle.py`, `tests/full_volume.py`).
* GitLab CI tests branches/merge requests, builds and pushes commit-SHA and `latest` images on the default branch, and mirrors refs to GitHub using CI credentials (`.gitlab-ci.yml`). Dependabot checks pip, Docker, and GitHub Actions dependencies weekly (`.github/dependabot.yml`).

## Environment configuration

**Required env vars:**

* `AIOS_API_KEY` to enable protected API routes, supplied to clients as `x-api-key` (`src/auth.py`, `src/main.py`).
* `AIOS_OBSERVATION_DB` absolute writable file path for container startup; the container sets `AIOS_REQUIRE_PERSISTENCE=1`. Local non-container API defaults to in-memory SQLite (`src/services/monitoring_service.py`, `Dockerfile`).
* `PYTHONPATH=/app`, `PYTHONDONTWRITEBYTECODE=1`, and `PYTHONUNBUFFERED=1` are Docker defaults; `PYTHONPATH=.` is set for CI tests (`Dockerfile`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`).
* GitLab CI uses built-in registry variables and a CI-managed `GITHUB_TOKEN` for repository mirroring; no runtime application dependency on these CI values (`.gitlab-ci.yml`).

**Secrets location:**

* Inject `AIOS_API_KEY` via the runtime environment; no dotenv config loader or example secret file is in the repository (`src/auth.py`, `docs/CONFIGURATION.md`). GitLab mirror token is a CI/CD variable rather than an application secret (`.gitlab-ci.yml`). Do not commit key values.

## Webhooks and callbacks

**Incoming:**

* No webhook handler detected; the HTTP endpoints are `/health`, `/agent/evaluate`, `/observability` (`src/main.py`). CI responds to repository push, pull-request, merge-request and manual events through platform workflows rather than application webhooks (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).

**Outgoing:**

* No outbound webhook or notification sender detected (`src/main.py`, `src/services/monitoring_service.py`, `app.py`). GitLab CI pushes images and mirrors git refs but this is not an application callback (`.gitlab-ci.yml`).

***

_Integration audit: 2026-11-23_
