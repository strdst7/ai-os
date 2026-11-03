# Concerns

Mapped: 2026-11-03. These are observed gaps or source-level risks, not production incident claims.

## Deployment and data safety

- `app.py` is a session-local Streamlit demonstration. It does not write to the API's SQLite store.
- `docs/operational-readiness-005c.md` leaves actual host-volume validation, automated backup schedule, isolated restore drill, and disk alerts pending.
- `Dockerfile` sets `AIOS_REQUIRE_PERSISTENCE=1`, but no production mount manifest exists in the repository.
- `src/services/monitoring_service.py` opens SQLite by absolute path. That path alone does not prove persistent host storage.
- `SECURITY.md` restricts API deployment until security review. Do not expose `src/main.py` publicly on CI evidence alone.
- The public GitHub source and a Streamlit webhook do not establish a persistent API deployment.

## Correctness and operations

- `src/services/monitoring_service.py` clears a latched anomaly after two fresh Stable observations, regardless of elapsed time.
- `tests/test_recovery_calibration.py` characterizes one-second and one-day gaps, but labeled incident calibration is absent.
- SQLite rows retain replay identities indefinitely. `MonitoringConfig.HISTORY_LIMIT` bounds display only, not disk growth.
- A full-volume write returns generic HTTP 500. `tests/full_volume.py` proves no false success on disposable tmpfs, not operational alerting.
- `src/main.py` creates the monitoring service at import time. A bad file path fails startup rather than serving a degraded API.
- `app.py` assigns random metrics when "Simulate Degradation" is clicked, then overwrites them with slider values. The button has no visible simulation effect.

## Build and repository hygiene

- `requirements.txt` has mostly unbounded dependencies and no lockfile. Dependabot previously selected a Streamlit release incompatible with Python 3.10.
- Its environment markers now keep CI installable on 3.10, but future dependency updates still need both runtime checks.
- `.github/workflows/ci.yml` triggers automatically for PRs to main and pushes to dev, not pushes to main.
- `.gitlab-ci.yml` contains a mirror pipeline with a literal masked-token placeholder in its push URL. Its operational state is unconfirmed.
- `src/main.py.save`, `src/models.py.save`, and `src/__init__.pyPYTHONPATH=.` are tracked leftover files.
- Tracked `tests/__pycache__/` bytecode and `tests/.DS_Store` remain despite `.gitignore`.
- `README.md` now labels the Streamlit path as a demo, but older `CONTRIBUTING.md` still uses production-grade language.

## Immediate safe priorities

- Keep API exposure blocked until the actual host, operator, storage, backup, restore, alerting, and security boundary are checked.
- Calibrate recovery against labeled incidents and an approved false-clear target before treating the two-Stable rule as production policy.
- Resolve the Streamlit simulation button only if that interaction is needed; it is separate from API durability.
