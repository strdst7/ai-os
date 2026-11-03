# Repository Structure

Mapped: 2026-11-03. Paths are relative to this repository.

## Root entrypoints

- `app.py` runs the independent Streamlit dashboard.
- `Dockerfile` launches `src.main:app` through Uvicorn.
- `requirements.txt` defines Python dependencies for both paths and tests.
- `README.md` describes the project and links the demo.
- `SECURITY.md` describes API-key and private deployment expectations.

## Application modules

- `src/main.py` owns FastAPI routes and the monitoring loop lifecycle.
- `src/models.py` defines Pydantic telemetry input.
- `src/auth.py` owns API-key validation.
- `src/services/monitoring_service.py` owns SQLite writes, reads, replay, and anomaly state.
- `src/agent.py` assembles UTC reports from scores and guardrails.
- `src/stability_engine.py` validates metrics and computes scores, degradation, and statistical anomalies.
- `src/guardrails.py` classifies ADSI into four tiers.
- `src/config.py` contains history and loop constants.

## Tests and CI

- `tests/test_evaluation_pipeline.py` compares authenticated API results and dashboard scoring.
- `tests/test_p0_integrity.py` covers invalid inputs, replay, concurrency, persistence, backup, and page-limit behavior.
- `tests/test_recovery_calibration.py` characterizes the provisional recovery rule.
- `tests/test_auth.py` checks access behavior.
- `tests/container_lifecycle.py` exercises restart, recreation, backup, and restore on a disposable Docker volume.
- `tests/full_volume.py` exercises a manually opted-in 16 MiB tmpfs ENOSPC run.
- Other `tests/test_*.py` files cover score, health, guardrail, and edge cases.
- `.github/workflows/ci.yml` runs Python tests and Docker lifecycle for PRs. The full-volume job needs explicit dispatch.
- `.gitlab-ci.yml` declares a separate GitLab test/build/mirror pipeline.

## Documentation and other material

- `docs/architecture.md` sketches layers and the uncalibrated recovery rule.
- `docs/operational-readiness-005c.md` records CI evidence and open host gates.
- `data/sample_telemetry.json` contains example input. `paper/` holds research materials.
- `.planning/config.json` is local GSD config; `.planning/codebase/` holds this generated map.

## Tracked cleanup candidates

- `src/main.py.save`, `src/models.py.save`, and `src/__init__.pyPYTHONPATH=.` appear in Git's tracked file list.
- Tracked `tests/__pycache__/` bytecode and `tests/.DS_Store` remain despite `.gitignore` rules.
- This map does not remove them. Review tracked contents and ownership before cleanup.
