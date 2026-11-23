# Coding Conventions

**Analysis Date:** 2026-11-23

## Naming Patterns

**Files:**
- Use lowercase `snake_case.py` for Python modules (`src/stability_engine.py`, `src/services/monitoring_service.py`); name collected tests `tests/test_<behavior>.py` (`tests/test_storage_errors.py`). Standalone Docker checks have descriptive names without the `test_` prefix (`tests/container_lifecycle.py`, `tests/full_volume.py`).

**Functions:**
- Use lowercase `snake_case` and verb-led names: `calculate_adsi` and `validate_metrics` in `src/stability_engine.py`, `generate_stability_report` in `src/agent.py`, `verify_api_key` in `src/auth.py`, `test_recovery_sequences` in `tests/test_recovery_calibration.py`.
- Keep FastAPI handlers short and route-oriented (`health`, `agent_evaluate`, `observability` in `src/main.py`); put persistence operations in `MonitoringService.evaluate` and `MonitoringService.get_observability` in `src/services/monitoring_service.py`.

**Variables:**
- Use `snake_case` for local values and telemetry keys (`observation_id`, `recovery_count`, `kpi_error` in `src/services/monitoring_service.py`); keep externally visible score acronyms uppercase in response dictionaries (`AHI`, `IHI`, `DHI`, `ADSI` in `src/agent.py`).
- Use uppercase for module constants and test inputs (`METRIC_NAMES` in `src/stability_engine.py`, `STABLE`/`CRITICAL` in `tests/test_p0_integrity.py`, `IMAGE`/`VOLUME` in `tests/container_lifecycle.py`). Use uppercase for configuration class attributes (`HISTORY_LIMIT`, `MONITOR_INTERVAL_SECONDS` in `src/config.py`).

**Types:**
- Use `PascalCase` for classes (`Telemetry` in `src/models.py`, `MonitoringService` in `src/services/monitoring_service.py`, `MonitoringConfig` in `src/config.py`). Define API payloads with Pydantic `BaseModel` and field constraints (`Telemetry` in `src/models.py`); annotate function parameters/returns when practical (`generate_stability_report(metrics: dict) -> dict` in `src/agent.py`, `verify_api_key(x_api_key: str | None = ...)` in `src/auth.py`). Most mathematical/service helpers remain unannotated (`src/stability_engine.py`, `src/services/monitoring_service.py`); do not imply static type checking is enforced.

## Code Style

**Formatting:**
- No formatter configuration or formatting command is present in tracked repository files (`requirements.txt`, `.github/workflows/ci.yml`); follow surrounding Python four-space indentation and blank-line separation (`src/main.py`, `src/stability_engine.py`).
- Multi-line function calls and dicts use parenthesized continuation/trailing commas where convenient (`src/agent.py`, `src/main.py`). Formatting is not uniform across modules (`src/auth.py`, `tests/test_engine_branches.py`); keep changes locally consistent rather than treating any formatting width as enforced.

**Linting:**
- No Black, Ruff, Flake8, isort, or mypy dependency/configuration or lint CI job is detected (`requirements.txt`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`); do not assume automated style/type gates. Maintain clear imports and validate with the pytest commands in `TESTING.md`.
- Follow contributor rules: service-layer separation, Pydantic models, deterministic monitoring, tests for new logic (`CONTRIBUTING.md`).

## Import Organization

**Order:**
1. Standard-library modules (`sqlite3`, `pathlib`, `threading` in `src/services/monitoring_service.py`).
2. Third-party libraries (`fastapi` in `src/main.py`; `numpy` in `src/stability_engine.py`).
3. Local absolute imports rooted at `src` (`src.agent`, `src.config`, `src.stability_engine` in `src/services/monitoring_service.py`). Existing order varies in `src/agent.py` and `tests/test_evaluation_pipeline.py`; prefer this grouping for new files.

**Path Aliases:**
- No import aliases or installed package indirection: import `src.<module>` directly (`src/main.py`, `tests/test_p0_integrity.py`). Run from repo root with `PYTHONPATH=.` as CI does (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).

## Error Handling

**Patterns:**
- Validate untrusted telemetry at the boundary with constrained `Telemetry` fields (`src/models.py`) and again for direct pure-function calls with `validate_metrics` (`src/stability_engine.py`). Reject missing/out-of-range inputs with `ValueError`; FastAPI returns 422 for schema errors (`tests/test_p0_integrity.py`).
- Use `HTTPException` for authorization failures and observation-ID conflicts (`src/auth.py`, `src/services/monitoring_service.py`). Keep storage exceptions native inside the service: roll back and re-raise on failure (`src/services/monitoring_service.py`); map `sqlite3.OperationalError` to sanitized 503 JSON only in `src/main.py`.
- For resources, use `try/finally` cleanup (`src/main.py` lifespan task cancellation, `tests/container_lifecycle.py` Docker cleanup); do not silently swallow original errors when rollback itself fails (`src/services/monitoring_service.py`).

## Logging

**Framework:** No application logging framework or logger calls are detected in `src/main.py`, `src/services/monitoring_service.py`, or `app.py`; standalone Docker checks print status (`tests/container_lifecycle.py`, `tests/full_volume.py`).

**Patterns:**
- Preserve explicit HTTP response details, rather than relying on logs for client-facing errors (`src/main.py`); for test-only external process checks, print human-readable progress and cleanup results (`tests/full_volume.py`).

## Comments

**When to Comment:**
- Explain non-obvious operational invariants and safety conditions, not every statement: replay must not alter alerts (`src/services/monitoring_service.py`), transactions preserve an original error (`src/services/monitoring_service.py`), and the full-volume script refuses non-tmpfs mounts (`tests/full_volume.py`).
- Mark provisional tuning with the existing `ponytail:` convention (`src/services/monitoring_service.py`), rather than presenting it as calibrated production policy.

**JSDoc/TSDoc:**
- Not applicable: this is Python (`src/agent.py`, `src/stability_engine.py`). Use concise Python docstrings for public calculation contracts, route error mapping, and behavioral tests where useful (`src/stability_engine.py`, `src/main.py`, `tests/test_storage_errors.py`).

## Function Design

**Size:**
- Keep numerical helpers pure and small (`calculate_ahi`, `calculate_dhi`, `detect_degradation` in `src/stability_engine.py`). Keep orchestration in `src/agent.py` and database transactions in `src/services/monitoring_service.py`, not in route handlers (`src/main.py`).

**Parameters:**
- Pass a metrics dictionary with the four named telemetry fields to calculations/report generation (`src/stability_engine.py`, `src/agent.py`); accept `Telemetry` at the HTTP boundary and convert with `model_dump(mode="json")` (`src/main.py`). Pass an optional database path to `MonitoringService(db_path=None)` for isolated tests (`src/services/monitoring_service.py`, `tests/test_p0_integrity.py`).

**Return Values:**
- Return numbers or tier strings from pure math helpers (`src/stability_engine.py`, `src/guardrails.py`), dictionaries from report/service functions (`src/agent.py`, `src/services/monitoring_service.py`), and route dictionaries/JSON responses from `src/main.py`. Preserve stable response keys and case (`tests/test_evaluation_pipeline.py`).

## Module Design

**Exports:**
- Import functions/classes directly from their defining modules (`src.main.app`, `src.agent.generate_stability_report`, `src.services.monitoring_service.MonitoringService` in `tests/test_p0_integrity.py`); keep HTTP concerns in `src/main.py`, API schemas in `src/models.py`, scoring in `src/stability_engine.py`, and persistence in `src/services/monitoring_service.py`.

**Barrel Files:**
- No re-export/barrel convention is present; `src/__init__.py` and `src/services/__init__.py` are empty. Import concrete modules directly (`src/main.py`, `src/services/monitoring_service.py`).

---

*Convention analysis: 2026-11-23*
