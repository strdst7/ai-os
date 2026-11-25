# Testing Patterns

**Analysis Date:** 2026-11-23

## Test framework

**Runner:**

* pytest, unpinned in `requirements.txt`; Python 3.10 in `.github/workflows/ci.yml` and `.gitlab-ci.yml`.
* Config: No `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini`, or `conftest.py` in the repo; the root `pytest` entry is an empty file, not a runner configuration. CI sets `PYTHONPATH=.` (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).

**Assertion Library:**

* Built-in `assert` plus `pytest.raises` and `pytest.mark.parametrize` (`tests/test_p0_integrity.py`, `tests/test_storage_errors.py`); FastAPI `TestClient` uses HTTP response assertions (`tests/test_auth.py`).

**Run Commands:**

```bash
PYTHONPATH=. pytest tests --cov=src                # GitHub CI suite with source coverage (.github/workflows/ci.yml)
PYTHONPATH=. pytest tests -x                       # Stop after first failure; no watch runner configured (requirements.txt)
PYTHONPATH=. pytest tests --cov=src --cov-report=term --cov-report=xml --junitxml=report.xml  # GitLab CI (.gitlab-ci.yml)
PYTHONPATH=. pytest tests/test_p0_integrity.py::test_file_store_survives_restart_and_replay  # focused test (tests/test_p0_integrity.py)
```

* Watch mode: Not detected (`requirements.txt`, `.github/workflows/ci.yml`); use standard pytest `-x` to stop after first failure, not as a watch command.

## Test file organization

**Location:**

* Place pytest tests in separate repo-root `tests/`, not beside implementations in `src/` (`tests/test_p0_integrity.py`, `tests/test_recovery_calibration.py`). Standalone Docker host checks also live under `tests/` but are run explicitly (`tests/container_lifecycle.py`, `tests/full_volume.py`).

**Naming:**

* Name collected files `test_*.py`, functions `test_<scenario>` (`tests/test_auth.py`, `tests/test_storage_errors.py`). `tests/container_lifecycle.py` and `tests/full_volume.py` are executable scripts, not pytest suites.

**Structure:**

```
src/stability_engine.py       -> tests/test_engine_branches.py, tests/test_stability_edges.py
src/main.py + src/auth.py     -> tests/test_auth.py, tests/test_api_health.py
src/services/monitoring_service.py -> tests/test_p0_integrity.py, tests/test_recovery_calibration.py
app.py                       -> tests/test_evaluation_pipeline.py
Dockerfile                   -> tests/container_lifecycle.py, tests/full_volume.py
```

## Test structure

**Suite Organization:**

```python
# tests/test_storage_errors.py
@pytest.mark.parametrize(
    "message,expected",
    [
        ("database or disk is full", "storage_full:"),
        ("database is locked", "storage_busy:"),
    ],
)
def test_operational_error_messages_map_to_distinct_details(message, expected):
    response = main.storage_error_handler(None, sqlite3.OperationalError(message))
    assert response.status_code == 503
    assert json.loads(response.body)["detail"].startswith(expected)
```

* The code block shows representative cases/assertions from `tests/test_storage_errors.py`; use its full list of error classes when expanding mapping coverage. Related standalone test functions group by scenario in `tests/test_p0_integrity.py`, without test classes or global `conftest.py`.

**Patterns:**

* Setup: construct `MonitoringService()` for in-memory isolation or `MonitoringService(tmp_path / "observations.db")` for persistence (`tests/test_p0_integrity.py`); for API tests, generate an ephemeral key, `monkeypatch.setenv`, replace `src.main.monitor`, and use `with TestClient(app, headers={...}) as client` (`tests/test_evaluation_pipeline.py`).
* Teardown: `monkeypatch` restores env and attributes automatically; explicitly `monitor.close()` after file-based SQLite checks (`tests/test_p0_integrity.py`); TestClient context closes lifespan (`tests/test_auth.py`).
* Assertions: assert HTTP status and parsed JSON plus state invariants (`tests/test_evaluation_pipeline.py`); compare history before/after rejected writes or replay (`tests/test_storage_errors.py`, `tests/test_p0_integrity.py`); use `pytest.raises(..., match=...)` for specific exception behavior (`tests/test_p0_integrity.py`).

## Mocking

**Framework:**

* pytest's `monkeypatch` fixture, not a project-specific mock library (`tests/test_storage_errors.py`, `tests/test_recovery_calibration.py`).

**Patterns:**

```python
# tests/test_storage_errors.py
key = token_urlsafe(32)
monkeypatch.setenv("AIOS_API_KEY", key)
monitor = MonitoringService(tmp_path / "observations.db")
monkeypatch.setattr("src.main.monitor", monitor)

def boom(telemetry, mode="manual_trigger"):
    raise sqlite3.OperationalError("database or disk is full")

monkeypatch.setattr(monitor, "evaluate", boom)
with TestClient(app, headers={"x-api-key": key}) as client:
    assert client.post("/agent/evaluate", json=STABLE).status_code == 503
```

**What to Mock:**

* Stub expensive/fault-path boundaries, e.g. inject `sqlite3.OperationalError` into `monitor.evaluate` to verify HTTP mapping (`tests/test_storage_errors.py`); patch `src.services.monitoring_service.generate_stability_report` to control timestamps (`tests/test_recovery_calibration.py`). Set API key with `monkeypatch.setenv`, never commit test credentials (`tests/test_auth.py`).

**What NOT to Mock:**

* Exercise real calculation/guardrail functions (`tests/test_evaluation_pipeline.py`), real SQLite file persistence, rollback, backup, and multi-connection transactions (`tests/test_p0_integrity.py`), and real container lifecycle in separate CI Docker checks (`tests/container_lifecycle.py`).

## Fixtures and factories

**Test Data:**

```python
# tests/test_p0_integrity.py
STABLE = {"kpi_error": 0.0, "retrieval_score": 1.0,
          "latency_dev": 0.0, "embedding_shift": 0.0}
CRITICAL = {"kpi_error": 1.0, "retrieval_score": 0.0,
            "latency_dev": 1.0, "embedding_shift": 1.0}
observation = {**CRITICAL, "observation_id": str(uuid4())}
```

**Location:**

* Keep small scenario dicts in test modules (`tests/test_p0_integrity.py`, `tests/test_recovery_calibration.py`, `tests/test_storage_errors.py`); there is no shared fixtures module or `tests/conftest.py`. Use built-in pytest `tmp_path` and `monkeypatch` fixtures (`tests/test_p0_integrity.py`). `data/sample_telemetry.json` is sample application data, not a shared test fixture.

## Coverage

**Requirements:** No coverage minimum/fail-under is configured (`.github/workflows/ci.yml`, `.gitlab-ci.yml`); the badge in `README.md` is not a CI gate.

**View Coverage:**

```bash
PYTHONPATH=. pytest tests --cov=src --cov-report=term-missing  # per-line missed-source report (.github/workflows/ci.yml)
PYTHONPATH=. pytest tests --cov=src --cov-report=xml           # XML artifact (.gitlab-ci.yml)
```

## Test types

**Unit Tests:**

* Cover scoring inputs, ADSI paths, guardrail/degradation tiers, validation branches, and storage error mappings in `tests/test_adsi.py`, `tests/test_engine_branches.py`, `tests/test_p0_integrity.py`, `tests/test_storage_errors.py`. Prefer exact expected values where behavior is defined (`tests/test_evaluation_pipeline.py`).

**Integration Tests:**

* Test FastAPI with `fastapi.testclient.TestClient`, including auth, failure status, observability, and Pydantic validation (`tests/test_auth.py`, `tests/test_storage_errors.py`); test persisted SQLite restart/idempotency, concurrency and backup via `tmp_path` and two service instances (`tests/test_p0_integrity.py`). `tests/test_integration.py` only checks a local arithmetic expression; use `tests/test_evaluation_pipeline.py` for the actual pipeline contract.

**E2E Tests:**

* Streamlit component-level UI runs in-process with `streamlit.testing.v1.AppTest.from_file` and compares dashboard scores to API scores (`tests/test_evaluation_pipeline.py`). Docker host lifecycle checks use `docker build -t ai-os-lifecycle:ci .` then `python3 tests/container_lifecycle.py` (`.github/workflows/ci.yml`, `tests/container_lifecycle.py`). `tests/full_volume.py` requires an approved disposable host, explicit `AIOS_RUN_ENOSPC_TEST=1`, a 16 MiB Docker tmpfs and manual GitHub workflow dispatch; **do not run locally or on production hosts** (`tests/full_volume.py`, `.github/workflows/ci.yml`). No browser E2E framework is detected (`requirements.txt`, `tests/test_evaluation_pipeline.py`).

## Common patterns

**Async Testing:**

```python
# tests/test_evaluation_pipeline.py: TestClient drives FastAPI lifespan in-process.
with TestClient(app, headers={"x-api-key": api_key}) as client:
    response = client.post("/agent/evaluate", json=stable)
    assert response.status_code == 200
```

* No `pytest-asyncio` or async test functions are detected (`requirements.txt`, `tests/test_evaluation_pipeline.py`); use synchronous `TestClient` even though `src/main.py` defines an async lifespan/monitoring loop.

**Error Testing:**

```python
# tests/test_p0_integrity.py
with pytest.raises(ValueError, match="insufficient_data"):
    generate_stability_report(metrics)
# tests/test_storage_errors.py: assert sanitized retryable 503 at HTTP boundary.
```

* Assert both failure and unchanged state on rejected writes (`tests/test_storage_errors.py`, `tests/test_p0_integrity.py`); parametrize representative failure classes (`tests/test_storage_errors.py`).

***

_Testing analysis: 2026-11-23_
