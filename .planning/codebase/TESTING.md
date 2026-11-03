# Testing

Mapped: 2026-11-03. Source: checked local AI-OS checkout and recorded CI evidence.

## Framework and entrypoint

- `requirements.txt` declares pytest, pytest-cov, HTTPX, and Streamlit for tests.
- `.github/workflows/ci.yml` runs `pytest tests --cov=src` under Python 3.10.
- `.gitlab-ci.yml` declares a separate Python 3.10 pytest job with XML reports.
- The latest checked PR #9 run recorded 47 passed, one warning, and 97% coverage.
- That CI result checks a branch, not the production Streamlit revision or a host mount.

## Unit and API coverage

- `tests/test_adsi.py`, `tests/test_stability.py`, and `tests/test_stability_edges.py` exercise scoring.
- `tests/test_guardrails.py`, `tests/test_engine_branches.py`, and `tests/test_health.py` cover classifiers and branches.
- `tests/test_auth.py` checks public health, private routes, weak keys, and disabled docs.
- `tests/test_evaluation_pipeline.py` drives authenticated TestClient writes and reads.
- Its Streamlit AppTest compares local dashboard scoring against API output. It does not prove dashboard-to-API requests.
- `tests/test_p0_integrity.py` checks strict input, durable UUID replay, concurrency, rollback, backup, and restart.
- `tests/test_recovery_calibration.py` checks two Stable observations under interruptions, replays, and different elapsed times.

## Container and failure checks

- `tests/container_lifecycle.py` builds a disposable volume case with Docker restart, recreation, backup, restore, and integrity.
- `tests/full_volume.py` fills only a checked 16 MiB tmpfs. It tests HTTP failure, backup failure, unchanged state, integrity, retry, and cleanup.
- `.github/workflows/ci.yml` runs the full-volume job only with `workflow_dispatch` and `run_full_volume=true`.
- `docs/operational-readiness-005c.md` links the opt-in disposable-runner log. It does not claim production-host coverage.

## Known test limits

- CI's remaining warning comes from FastAPI TestClient and installed HTTPX compatibility, as recorded in `docs/operational-readiness-005c.md`.
- `tests/test_integration.py` checks local arithmetic without invoking the application path.
- No test can establish a backup schedule, host mount, alert delivery, or independent restore on an unidentified deployment host.
- No labeled incidents statistically calibrate the two-Stable recovery policy.
