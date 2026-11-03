# Coding Conventions

Mapped: 2026-11-03. Describe existing source, not an enforced formatter.

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
