# Technology Stack

**Analysis Date:** 2026-11-23

## Languages

**Primary:**

* Python 3.10 in CI and container - API, dashboard, scoring engine, and tests (`Dockerfile`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`, `src/main.py`, `app.py`, `tests/test_p0_integrity.py`). `src/auth.py` and `src/models.py` use Python 3.10 union syntax.

**Secondary:**

* YAML (version not applicable) - GitHub Actions, GitLab CI, and Dependabot (`.github/workflows/ci.yml`, `.gitlab-ci.yml`, `.github/dependabot.yml`).
* Dockerfile syntax - Python image build and Uvicorn startup (`Dockerfile`).

## Runtime

**Environment:**

* CPython 3.10, Linux in CI and the Docker image (`Dockerfile`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`). Local Python versions are not pinned separately; `requirements.txt` selects Streamlit by Python version.
* Separate processes/entrypoints: `uvicorn src.main:app` serves the FastAPI service (`src/main.py`, `Dockerfile`); `streamlit run app.py` serves the standalone dashboard (`app.py`, `docs/GETTING-STARTED.md`). Do not assume the dashboard calls the API or shares its SQLite state.

**Package Manager:**

* pip, version unpinned (`Dockerfile`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`). Install with `pip install -r requirements.txt`.
* Lockfile: missing; `requirements.txt` does not pin exact versions (except conditional Streamlit ranges).

## Frameworks

**Core:**

* FastAPI, version unpinned - HTTP service and dependency-based API-key checks (`requirements.txt`, `src/main.py`, `src/auth.py`).
* Streamlit, `>=1.65,<1.66` for Python <3.11 or `>=1.66.1` for Python >=3.11 - independent interactive demo (`requirements.txt`, `app.py`).
* Pydantic, version unpinned; code requires v2 interfaces (`ConfigDict`, `model_dump`) - telemetry request validation (`requirements.txt`, `src/models.py`, `src/main.py`).

**Testing:**

* pytest and pytest-cov, versions unpinned - functional and coverage suites (`requirements.txt`, `.github/workflows/ci.yml`, `tests/test_p0_integrity.py`).
* FastAPI `TestClient` and Streamlit `AppTest` - API and dashboard tests (`tests/test_auth.py`, `tests/test_evaluation_pipeline.py`).

**Build/Dev:**

* Uvicorn, version unpinned - ASGI server (`requirements.txt`, `Dockerfile`, `docs/DEVELOPMENT.md`).
* Docker with Python `3.10-slim` multi-stage build - backend image; exposed port 8000 (`Dockerfile`).
* GitHub Actions and GitLab CI - test, container validation, image publication and mirroring (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).

## Key dependencies

**Critical:**

* `fastapi`, `uvicorn`, `pydantic` (all unpinned) - HTTP routing, serving, strict float/UUID validation (`requirements.txt`, `src/main.py`, `src/models.py`).
* `streamlit` (conditional ranges above) - standalone session-state dashboard (`requirements.txt`, `app.py`).
* `numpy` (unpinned) - z-score anomaly calculation (`requirements.txt`, `src/stability_engine.py`).
* `sqlite3` (Python standard library) - transactional observations and anomaly state (`src/services/monitoring_service.py`).

**Infrastructure:**

* `httpx` (unpinned) - test-client dependency; no application HTTP client usage (`requirements.txt`, `tests/test_auth.py`).
* `pytest`, `pytest-cov` (unpinned) - automated tests and coverage (`requirements.txt`, `.gitlab-ci.yml`).
* `pandas`, `matplotlib`, `scikit-learn` (unpinned) - listed dependencies with no direct import in current Python application/test files (`requirements.txt`, `src/`, `app.py`, `tests/`).

## Configuration

**Environment:**

* API secrets and persistence are process environment variables, not a dotenv loader: `AIOS_API_KEY` (private-route key), `AIOS_OBSERVATION_DB` (SQLite path, local default `:memory:`), `AIOS_REQUIRE_PERSISTENCE=1` (require absolute file path) (`src/auth.py`, `src/services/monitoring_service.py`, `docs/CONFIGURATION.md`).
* Set a strong `AIOS_API_KEY` (at least 32 characters) before calling private routes; set a writable absolute database path on a persistent mount in the Docker image (`src/auth.py`, `src/services/monitoring_service.py`, `Dockerfile`).
* Fixed monitoring and guardrail constants are Python class attributes (`src/config.py`); the dashboard uses `st.session_state`, not API environment variables (`app.py`).

**Build:**

* `requirements.txt` supplies dependencies; `Dockerfile` installs them in a Python 3.10 builder, copies site-packages and `src/` plus `app.py` to the image, then runs `uvicorn src.main:app` (`requirements.txt`, `Dockerfile`).
* `.dockerignore` controls build context; `.github/workflows/ci.yml` and `.gitlab-ci.yml` define CI jobs.

## Platform requirements

**Development:**

* Use Python 3.10 and pip for parity with CI; install `requirements.txt`, set `PYTHONPATH=.` when running pytest (`.github/workflows/ci.yml`, `docs/DEVELOPMENT.md`).
* Docker is needed for container lifecycle and optional full-volume checks (`tests/container_lifecycle.py`, `tests/full_volume.py`, `.github/workflows/ci.yml`).

**Production:**

* The repository image targets a single-host FastAPI process on port 8000 with an operator-supplied absolute SQLite path and persistent mount; no host deployment manifest exists (`Dockerfile`, `docs/DEPLOYMENT.md`, `src/services/monitoring_service.py`).
* The Streamlit dashboard has a separate named Community Cloud demo URL; it does not run the backend. The stateful API is not production-approved (`docs/DEPLOYMENT.md`, `docs/operational-readiness-005c.md`).

***

_Stack analysis: 2026-11-23_
