# Technology Stack

Mapped: 2026-11-03. Source: checked local AI-OS checkout.

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
