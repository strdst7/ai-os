# Architecture

**Analysis Date:** 2026-11-23

## System overview

```
                 HTTP clients                         Browser session
                      |                                     |
                      v                                     v
          FastAPI `src/main.py`                  Streamlit `app.py`
          auth `src/auth.py`                     session-local history
          request `src/models.py`                       |
                      |                                     |
                      v                                     |
      `src/services/monitoring_service.py`                  |
              |                  |                           |
              v                  v                           |
       `src/agent.py`     SQLite observations                |
              |            + monitor_state                  |
              v                                            v
   `src/stability_engine.py` <------------------------------+
   `src/guardrails.py`
```

The two entry points run independently: `app.py` does not call `src/main.py`, use `src/services/monitoring_service.py`, or read its SQLite store. `Dockerfile` launches only the FastAPI entry point.

## Component responsibilities

| Component           | Responsibility                                                                    | File                                 |
| ------------------- | --------------------------------------------------------------------------------- | ------------------------------------ |
| HTTP application    | Route registration, lifespan polling, storage-error translation                   | `src/main.py`                        |
| HTTP authentication | Validate configured server key and incoming `x-api-key`                           | `src/auth.py`                        |
| Input contract      | Validate telemetry shape, UUID, strict bounded floats                             | `src/models.py`                      |
| Monitoring service  | Deduplicate observations, persist reports and alert state, expose bounded history | `src/services/monitoring_service.py` |
| Report builder      | Calculate scores and classification; produce timestamped report                   | `src/agent.py`                       |
| Numerical engine    | Validate metrics; calculate AHI/IHI/DHI/ADSI, anomaly and degradation             | `src/stability_engine.py`            |
| Guardrails          | Classify ADSI into four stability tiers                                           | `src/guardrails.py`                  |
| Configuration       | Store class-level interval, history limit, and guardrail constants                | `src/config.py`                      |
| Dashboard           | Build standalone Streamlit controls and render local trend                        | `app.py`                             |

## Pattern overview

**Overall:** Two independently deployed presentation surfaces sharing pure scoring code; a layered FastAPI route → service → domain-function → SQLite path for the stateful API.

**Key characteristics:**

* Keep route orchestration in `src/main.py`; keep state transitions and database writes in `src/services/monitoring_service.py`.
* Reuse numerical functions from `src/stability_engine.py` and report assembly from `src/agent.py`; `app.py` only reuses the numerical engine.
* Store full observations and alert state in SQLite; limit the returned window to `MonitoringConfig.HISTORY_LIMIT` (`src/config.py`), not the table size.
* Keep dashboard trend in `st.session_state.history` (`app.py`); it is unrelated to the API observation history.

## Layers

**Presentation / transport:**

* Purpose: Accept HTTP telemetry or interactive dashboard slider input and format responses.
* Location: `src/main.py`, `src/models.py`, `src/auth.py`, `app.py`.
* Contains: FastAPI endpoints and dependencies, Pydantic request model, Streamlit widgets and charts.
* Depends on: `src/services/monitoring_service.py` (HTTP), `src/stability_engine.py` (dashboard).
* Used by: API clients or dashboard browser sessions respectively.

**Application / state:**

* Purpose: Coordinate evaluation, idempotency, persisted alert transitions and observability reads.
* Location: `src/services/monitoring_service.py`.
* Contains: `MonitoringService`, SQLite schema/transactions, locking, replay handling and recovery counter.
* Depends on: `src/agent.py`, `src/stability_engine.py`, `src/config.py`, SQLite.
* Used by: `src/main.py` and service-level tests in `tests/test_p0_integrity.py`.

**Domain calculations:**

* Purpose: Convert normalized inputs into scores and tier/anomaly decisions.
* Location: `src/agent.py`, `src/stability_engine.py`, `src/guardrails.py`.
* Contains: pure scoring/classification functions and a UTC timestamped report builder.
* Depends on: NumPy for the history z-score in `src/stability_engine.py`.
* Used by: `src/services/monitoring_service.py`, `app.py`, and tests under `tests/`.

**Persistence:**

* Purpose: Retain observations and alert/recovery state across requests and optionally restarts.
* Location: SQLite statements inside `src/services/monitoring_service.py` (no ORM or migrations directory).
* Contains: `observations` table (fingerprinted telemetry, report, entry) and single-row `monitor_state` table.
* Depends on: `AIOS_OBSERVATION_DB` file path or in-memory default (`src/services/monitoring_service.py`).
* Used by: `MonitoringService.evaluate()` and `MonitoringService.get_observability()`.

## Data flow

### Primary request path

1. `POST /agent/evaluate` invokes `verify_api_key`, parses `Telemetry`, and calls the module-level service (`src/main.py:64`, `src/auth.py:5`, `src/models.py:6`).
2. `MonitoringService.evaluate()` generates a report, fingerprints metrics, starts `BEGIN IMMEDIATE`, checks explicit observation ID or latest id-less duplicate, and inserts a fresh observation (`src/services/monitoring_service.py:41`).
3. The service reads the latest 20 scores, updates the persisted anomaly/recovery latch only for fresh observations, commits, and returns the report (`src/services/monitoring_service.py:80`, `src/main.py:66`).
4. `generate_stability_report()` validates metrics, calls score functions and `evaluate_guardrails()`, and returns a UTC timestamp, scores, tier and flag (`src/agent.py:12`).

### Read and polling flow

1. `GET /observability` delegates to `monitor.get_observability()` after key validation (`src/main.py:69`).
2. The service reads newest entries (reversing to oldest-first), persisted alert state, and current degradation; an empty store returns a message (`src/services/monitoring_service.py:111`).
3. FastAPI lifespan creates a single process-local `monitoring_loop()` task, calling `autonomous_check()` each configured interval; that check only reads current observability and does not add history (`src/main.py:13`, `src/services/monitoring_service.py:130`).

### Dashboard flow

1. Streamlit sidebar collects four normalized metrics into a dict (`app.py:42`).
2. Dashboard calls `calculate_adsi(metrics)` and `detect_degradation()`, appends ADSI to `st.session_state.history`, and calculates an anomaly from that session's list (`app.py:57`).
3. Streamlit displays metric cards and a trend line without calling the API or persisting SQLite observations (`app.py:68`).

**State management:** `src/main.py:56` owns one process-local `MonitoringService`; `src/services/monitoring_service.py:25` protects its single connection with a `threading.Lock` and SQLite write transaction. SQLite holds alert/recovery state across restart when file-backed. `app.py:5` holds a distinct per-session Streamlit list.

## Key abstractions

**Telemetry:**

* Purpose: Boundary schema rejecting unknown fields, nonfinite numbers, out-of-range values and non-float inputs.
* Examples: `src/models.py`, `src/main.py`.
* Pattern: Pydantic `BaseModel` with `StrictFloat`, `Field` bounds and `ConfigDict`.

**MonitoringService:**

* Purpose: Unit of stateful evaluation and observability, with configurable database location.
* Examples: `src/services/monitoring_service.py`, `tests/test_p0_integrity.py`.
* Pattern: Stateful class wrapping SQLite connection plus local mutex and explicit transactions.

**Report / observation entry:**

* Purpose: Keep public evaluation result separate from persisted observability metadata (observation ID, mode).
* Examples: `src/agent.py:32`, `src/services/monitoring_service.py:68`.
* Pattern: JSON-serializable dictionaries, persisted as TEXT columns in SQLite.

## Entry points

**FastAPI:**

* Location: `src/main.py`.
* Triggers: `uvicorn src.main:app` (`Dockerfile:26`) or TestClient (`tests/test_evaluation_pipeline.py`).
* Responsibilities: Routes, API-key dependency, background read task and SQLite error-to-503 mapping.

**Streamlit:**

* Location: `app.py`.
* Triggers: `streamlit run app.py` (`docs/DEVELOPMENT.md:20`).
* Responsibilities: Independently calculate and visualize browser-session telemetry.

**Operational checks:**

* Location: `tests/container_lifecycle.py`, `tests/full_volume.py`.
* Triggers: `.github/workflows/ci.yml` container job and opt-in dispatch respectively.
* Responsibilities: Check Docker persistence lifecycle and isolated disk-full behavior; not application entry points.

## Architectural constraints

* **Threading:** `src/main.py:65` uses synchronous FastAPI handlers; the service shares a `sqlite3` connection with `check_same_thread=False` and serializes accesses with `Lock` (`src/services/monitoring_service.py:25`). The `asyncio` polling task invokes a synchronous read in the event loop (`src/main.py:13`).
* **Global state:** `monitor = MonitoringService()` is created at import time in `src/main.py:56`; each worker process owns its own service instance. Streamlit holds per-session `st.session_state.history` (`app.py:5`).
* **Circular imports:** Not detected in `src/` imports; the dependency direction is routes → service → report/domain.
* **Single-host persistence:** Docker enforces an absolute file path via `AIOS_REQUIRE_PERSISTENCE=1` (`Dockerfile:14`, `src/services/monitoring_service.py:20`); no multi-host transaction coordinator is present (`src/services/monitoring_service.py:24`).
* **No automatic ingestion:** Only explicit `POST /agent/evaluate` creates observations; the periodic `autonomous_check()` is a read (`src/main.py:13`, `src/services/monitoring_service.py:130`).

## Anti-patterns

### Treating dashboard and API histories as one store

**What happens:** `app.py:62` appends to session-local history, whereas `src/services/monitoring_service.py:76` inserts to SQLite. **Why it's wrong:** A dashboard score is not an API observation and cannot be retrieved from `/observability` (`src/main.py:69`). **Do this instead:** Route persisted observations through `MonitoringService.evaluate()` (`src/services/monitoring_service.py:41`); explicitly integrate `app.py` with the API if shared history is required.

### Treating the background check as telemetry ingestion

**What happens:** `src/services/monitoring_service.py:130` returns `get_observability()` without writing anything. **Why it's wrong:** Assuming periodic polling adds measurements or advances recovery misrepresents alert behavior (`src/services/monitoring_service.py:87`). **Do this instead:** Supply fresh telemetry through `POST /agent/evaluate` (`src/main.py:64`); keep read-only checks separate.

## Error handling

**Strategy:** Validate before mutating state, roll back failed transactions, and translate known storage errors at the HTTP boundary.

**Patterns:**

* Pydantic `Telemetry` rejects malformed HTTP payloads with framework 422 (`src/models.py:6`); domain `validate_metrics()` raises `ValueError` for invalid direct calls (`src/stability_engine.py:9`).
* Duplicate observation IDs with changed metrics raise HTTP 409; same-ID/same-metrics replays return stored reports without advancing alerts (`src/services/monitoring_service.py:49`).
* Failed writes roll back and re-raise (`src/services/monitoring_service.py:102`); SQLite operational errors become retryable HTTP 503 with `Retry-After` (`src/main.py:32`).
* Invalid or missing server key returns HTTP 503; incorrect client key returns HTTP 401 (`src/auth.py:5`).

## Cross-cutting concerns

**Logging:** No structured application logger is configured in `src/main.py` or `src/services/monitoring_service.py`; server/runtime output is managed by Uvicorn (`Dockerfile:26`). **Validation:** Enforce the HTTP contract in `src/models.py`; preserve domain validation for direct engine/service use in `src/stability_engine.py:9`. **Authentication:** Protect private FastAPI routes with `Depends(verify_api_key)` from `src/auth.py`; public `/health` is defined in `src/main.py:59`. The standalone `app.py` has no corresponding API-key dependency.

***

_Architecture analysis: 2026-11-23_
