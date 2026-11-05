<!-- generated-by: gsd-doc-writer -->
# Testing

## Test framework and setup

AI-OS uses pytest and pytest-cov for Python tests. `requirements.txt` does not pin their versions. Use Python 3.10 (the GitHub Actions and GitLab CI test runtime) from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

The tests exercise the stability engine, guardrails, authentication, FastAPI endpoints via `fastapi.testclient.TestClient`, Streamlit scoring via `streamlit.testing.v1.AppTest`, and SQLite persistence. Docker is needed only for the separate container checks below. CI sets `PYTHONPATH=.`; when running locally, invoke pytest from the repository root with the same setting.

## Running tests

Run the pytest suite with source coverage, as in GitHub Actions:

```bash
PYTHONPATH=. pytest tests --cov=src
```

Select a file or one test:

```bash
PYTHONPATH=. pytest tests/test_p0_integrity.py
PYTHONPATH=. pytest tests/test_p0_integrity.py::test_sqlite_full_rolls_back_observation_and_alert
```

The Docker lifecycle check is a standalone Python script, **not** a pytest test. With a running Docker daemon, build the image and run it from the repository root:

```bash
docker build -t ai-os-lifecycle:ci .
python3 tests/container_lifecycle.py
```

It checks fail-closed database path configuration, restart and recreation of the container using a persistent named volume, idempotent observations, SQLite backup/restore, integrity, and recovery. The script creates and removes its own Docker container and volume.

**Do not run `tests/full_volume.py` on a local or production host.** It deliberately fills a disposable 16 MiB Docker tmpfs to trigger ENOSPC. GitHub Actions runs it only through the manual `workflow_dispatch` input `run_full_volume`, on a hosted runner, after checking at least 4 GiB of free disk. The script also requires `AIOS_RUN_ENOSPC_TEST=1`, verifies the mount type and capacity before filling it, and checks cleanup. Its CI job first injects `AIOS_FAIL_AFTER_MOUNT=1` to test cleanup on failure, then checks the real full-volume behavior.

## Writing new tests

Add pytest-discovered `test_*.py` files under `tests/` and name test functions `test_*`. Existing tests use plain assertions, `@pytest.mark.parametrize`, `monkeypatch` for environment and application state, and `tmp_path` for isolated SQLite files. API tests use `TestClient(src.main.app)`; persistence tests instantiate `MonitoringService` with a temporary database path. There is no shared `conftest.py` or global fixture setup. Keep Docker-host checks separate from ordinary pytest tests, following `tests/container_lifecycle.py`.

## Coverage requirements

| Type | Threshold |
| --- | --- |
| Lines, branches, functions, statements | No coverage threshold configured. |

GitHub Actions reports `--cov=src` without `--cov-fail-under`; GitLab CI generates terminal and XML coverage reports, but does not enforce a minimum. The README coverage badge is not a CI threshold.

## CI integration

- **GitHub Actions:** `.github/workflows/ci.yml`, workflow `AI-OS CI Pipeline`. Pushes to `dev`, pull requests targeting `main`, and manual dispatch run the `test` job on Ubuntu with Python 3.10: `pytest tests --cov=src`. The separate `container-lifecycle` job builds the image and runs `python3 tests/container_lifecycle.py` on those triggers. Only manual dispatch with `run_full_volume=true` enables the `full-volume` job described above.
- **GitLab CI:** `.gitlab-ci.yml` runs the `test` job for branch and merge-request pipelines in `python:3.10-slim`, with `PYTHONPATH=.`. Its command is `pytest tests --cov=src --cov-report=term --cov-report=xml --junitxml=report.xml`; JUnit and Cobertura coverage reports are published as artifacts. The GitLab pipeline does not run the Docker lifecycle or ENOSPC scripts.
