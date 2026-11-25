# Codebase Structure

**Analysis Date:** 2026-11-23

## Directory layout

```
ai-os/
├── app.py                        # Standalone Streamlit dashboard
├── src/                          # Importable Python monitoring package
│   ├── main.py                   # FastAPI entry, routes, lifespan and error mapping
│   ├── models.py                 # Telemetry request contract
│   ├── auth.py                   # Private-route API-key dependency
│   ├── agent.py                  # Timestamped report generation
│   ├── stability_engine.py       # Validation, numerical scores and anomaly logic
│   ├── guardrails.py             # ADSI classification
│   ├── config.py                 # Monitoring and guardrail constants
│   └── services/
│       └── monitoring_service.py # SQLite state, deduplication and observability
├── tests/                        # Pytest tests and opt-in Docker checks
├── data/                         # Example telemetry JSON
├── docs/                         # API, operations, architecture and visual assets
├── paper/                        # Research manuscript and bibliography
├── .github/workflows/ci.yml      # GitHub Actions tests and container checks
├── .gitlab-ci.yml                # GitLab CI configuration
├── Dockerfile                    # Production FastAPI image
├── requirements.txt              # Python dependencies
├── .planning/codebase/           # GSD codebase map documents
└── README.md                     # Project overview and usage
```

## Directory purposes

**`src/`:**

* Purpose: FastAPI transport, scoring domain and application service.
* Contains: Flat Python modules and a `services/` subpackage; `src/__init__.py` is empty.
* Key files: `src/main.py`, `src/models.py`, `src/agent.py`, `src/stability_engine.py`, `src/guardrails.py`, `src/config.py`, `src/auth.py`.

**`src/services/`:**

* Purpose: Stateful service logic and SQLite persistence.
* Contains: `MonitoringService` and an empty `__init__.py`.
* Key files: `src/services/monitoring_service.py`, `src/services/__init__.py`.

**`tests/`:**

* Purpose: Verify pure calculations, API behavior, persistence, recovery and operational paths.
* Contains: Pytest-discovered `test_*.py` modules plus manually invoked Docker scripts.
* Key files: `tests/test_p0_integrity.py`, `tests/test_evaluation_pipeline.py`, `tests/test_storage_errors.py`, `tests/test_recovery_calibration.py`, `tests/container_lifecycle.py`, `tests/full_volume.py`.

**`docs/`:**

* Purpose: Explain API contracts, configuration, local development, deployment, testing and architecture.
* Contains: Markdown and visual assets.
* Key files: `docs/API.md`, `docs/architecture.md`, `docs/CONFIGURATION.md`, `docs/DEPLOYMENT.md`, `docs/DEVELOPMENT.md`, `docs/TESTING.md`.

**`data/` and `paper/`:**

* Purpose: Hold sample input and research artifacts respectively.
* Contains: `data/sample_telemetry.json`; `paper/AI_OS_IEEE_Conference_Camera_Ready.tex` and `paper/references.bib`.
* Key files: `data/sample_telemetry.json`, `paper/AI_OS_IEEE_Conference_Camera_Ready.tex`.

**`.github/`:**

* Purpose: Repository automation and dependency update configuration.
* Contains: Workflow and Dependabot files.
* Key files: `.github/workflows/ci.yml`, `.github/dependabot.yml`.

## Key file locations

**Entry Points:**

* `src/main.py`: FastAPI ASGI app (`uvicorn src.main:app`), public health and authenticated endpoints.
* `app.py`: Standalone Streamlit dashboard (`streamlit run app.py`); does not access the FastAPI SQLite history.
* `tests/container_lifecycle.py`: Explicit Docker lifecycle runner invoked by `.github/workflows/ci.yml`.
* `tests/full_volume.py`: Explicitly opted-in disposable disk-full runner invoked by `.github/workflows/ci.yml`.

**Configuration:**

* `src/config.py`: History cap (20), polling interval (10 seconds), guardrail constants.
* `src/services/monitoring_service.py`: `AIOS_OBSERVATION_DB` and `AIOS_REQUIRE_PERSISTENCE` processing, SQLite schema.
* `src/auth.py`: `AIOS_API_KEY` lookup and request-header verification.
* `requirements.txt`: Runtime and test dependency declarations.
* `Dockerfile`: Python image and ASGI production launch.
* `.github/workflows/ci.yml`: Python test and Docker validation jobs.
* `.gitlab-ci.yml`: GitLab CI pipeline.

**Core Logic:**

* `src/stability_engine.py`: Input validation, score formulae, z-score anomaly and degradation tiers.
* `src/guardrails.py`: Report guardrail tier classification.
* `src/agent.py`: UTC-stamped structured score report.
* `src/services/monitoring_service.py`: Observation write/replay, anomaly recovery latch and history reads.
* `src/models.py`: Strict HTTP telemetry schema.

**Testing:**

* `tests/test_p0_integrity.py`: Boundary, idempotency, concurrency and SQLite restart coverage.
* `tests/test_evaluation_pipeline.py`: API-to-service request/response coverage.
* `tests/test_recovery_calibration.py`: Alert latch and recovery sequences.
* `tests/test_storage_errors.py`: Storage failure response and rollback behavior.
* `tests/test_auth.py`: API-key enforcement.
* `tests/test_stability.py`, `tests/test_stability_edges.py`, `tests/test_engine_branches.py`, `tests/test_adsi.py`: Scoring paths.

## Naming conventions

**Files:**

* Use snake\_case Python modules such as `src/stability_engine.py` and `src/services/monitoring_service.py`.
* Use `test_*.py` for pytest-discovered suites such as `tests/test_p0_integrity.py`; standalone operational runners are `tests/container_lifecycle.py` and `tests/full_volume.py`.
* Use uppercase Markdown names for operational references (`docs/API.md`, `docs/DEPLOYMENT.md`); note the existing lowercase `docs/architecture.md`.

**Directories:**

* Keep application modules under `src/`, persistent service implementation under `src/services/`, and tests under `tests/`.
* Keep guide documents under `docs/`, samples under `data/`, manuscript files under `paper/`, and CI configuration under `.github/workflows/`.

## Where to add new code

**New Feature:**

* Primary code: Add a route to `src/main.py` if exposed through HTTP; put stateful coordination beside `MonitoringService` in `src/services/monitoring_service.py`, numerical calculations in `src/stability_engine.py`, and report fields in `src/agent.py`.
* Tests: Add a `tests/test_<feature>.py` suite; use `tests/test_evaluation_pipeline.py` for existing API flow examples and `tests/test_p0_integrity.py` for persistence/replay examples.
* API contract: Add request fields in `src/models.py` and update `docs/API.md` alongside an HTTP change.

**New Component/Module:**

* Implementation: Add a narrowly scoped `src/<module>.py` for stateless domain logic; add a `src/services/<module>_service.py` when it owns state or storage, following `src/services/monitoring_service.py`.
* Independent dashboard feature: Add UI controls and presentation logic in `app.py`; explicitly connect to the API before expecting shared history with `src/main.py`.

**Utilities:**

* Shared helpers: Prefer domain-level functions in `src/stability_engine.py` for metrics and `src/guardrails.py` for tier decisions. No generic `utils/` directory exists under `src/`.
* Settings: Extend `src/config.py` for constants and use the existing environment read patterns in `src/auth.py` and `src/services/monitoring_service.py` for runtime settings.

## Special directories

**`.planning/codebase/`:**

* Purpose: GSD architecture and codebase-reference documents.
* Generated: Yes, by codebase mapping.
* Committed: Determined by orchestrator; document content is stored in `.planning/codebase/ARCHITECTURE.md` and `.planning/codebase/STRUCTURE.md`.

**`.venv/`, `.venv310/`, `.pytest_cache/`, `src/__pycache__/`, `tests/__pycache__/`:**

* Purpose: Local interpreter environments, test caches and Python bytecode.
* Generated: Yes.
* Committed: No; `.gitignore` covers `__pycache__/` and `.pytest_cache/`, and local environments must stay out of the codebase map (`.gitignore`, `docs/DEVELOPMENT.md`).

**`docs/` visual assets:**

* Purpose: Static diagrams and benchmark imagery referenced by project documentation.
* Generated: Not detected for `docs/architecture.png`, `docs/cover.png`, `docs/adsi_benchmark.svg`.
* Committed: Repository assets under `docs/`.

***

_Structure analysis: 2026-11-23_
