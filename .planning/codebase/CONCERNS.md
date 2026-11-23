# Codebase Concerns

**Analysis Date:** 2026-11-23

## Tech Debt

**Duplicated stability thresholds and unused configuration:**
- Issue: `src/guardrails.py` and `src/stability_engine.py` independently encode the same tier boundaries; `GuardrailConfig` defines other thresholds that neither path reads.
- Files: `src/guardrails.py`, `src/stability_engine.py`, `src/config.py`, `src/agent.py`, `app.py`.
- Impact: A threshold change in one path can make API reports, API observability, and the dashboard disagree; editing `GuardrailConfig` has no effect on these decisions.
- Fix approach: Define one tier policy consumed by both classifiers and the dashboard; either wire up or remove unused configuration. Keep boundary tests in `tests/test_guardrails.py`, `tests/test_stability_edges.py`, and `tests/test_evaluation_pipeline.py`.

**Read-only autonomous loop without useful effect:**
- Issue: The lifespan task calls `MonitoringService.autonomous_check()` every ten seconds, but that method only reads current observability and discards it. It performs no fresh evaluation, alert delivery, or logging.
- Files: `src/main.py`, `src/services/monitoring_service.py`, `src/config.py`.
- Impact: Periodic work consumes resources but does not provide autonomous monitoring; an exception in the task can stop it without an operator-facing signal.
- Fix approach: Specify the actual source of new telemetry and observable action, or remove the loop. If retained, supervise failures and expose task health independently of request health.

**Process-global database lifecycle:**
- Issue: `monitor = MonitoringService()` constructs a SQLite connection at module import; the lifespan hook cancels its task but does not close that connection. Tests replace the global with `monkeypatch`.
- Files: `src/main.py`, `src/services/monitoring_service.py`, `tests/test_p0_integrity.py`, `tests/test_evaluation_pipeline.py`.
- Impact: Importing the app immediately creates schema and may fail before lifespan; tests and repeated app setups can leave connections open; configuration and dependency injection are hard to isolate.
- Fix approach: Initialize and close the service in the lifespan context and inject it through request/app state; retain single-process serialization until the storage model changes.

**Unpinned dependency and interpreter inputs:**
- Issue: Most `requirements.txt` packages are unpinned, including API, database-adjacent test, and numerical libraries; `Dockerfile` uses a floating `python:3.10-slim` tag. There is no committed Python dependency lockfile.
- Files: `requirements.txt`, `Dockerfile`, `.github/workflows/ci.yml`, `.gitlab-ci.yml`.
- Impact: Rebuilds can resolve different compatible or incompatible versions without source changes; CI and deployed image behavior can drift.
- Fix approach: Pin/lock runtime and test dependencies, use a reviewed base-image digest, and update deliberately with CI compatibility checks.

## Known Bugs

**Dashboard simulation is immediately overwritten:**
- Symptoms: Clicking “Simulate Degradation” creates randomized metrics but the sidebar slider values immediately replace `metrics` before scoring; displayed ADSI does not reflect simulated values.
- Files: `app.py` (button and metric reassignment), `tests/test_evaluation_pipeline.py` (only slider scoring is checked).
- Trigger: Open `app.py` in Streamlit and click “Simulate Degradation” without changing the sliders.
- Workaround: Set sidebar sliders to the desired degraded telemetry manually.

**Duplicate id-less readings cannot form a fresh observation:**
- Symptoms: Consecutive equal telemetry without `observation_id` replays the last report; the second reading cannot advance a recovery counter even if it represents a later real-world measurement.
- Files: `src/services/monitoring_service.py`, `tests/test_recovery_calibration.py`.
- Trigger: Submit a Critical reading, then submit the same Stable metrics twice without observation IDs.
- Workaround: Supply a new UUID `observation_id` for each genuinely new reading; reuse the same UUID only for retries.

## Security Considerations

**Public API deployment boundary:**
- Risk: The API binds `0.0.0.0:8000` in the image and authenticates private routes with one shared static key. The application itself provides no TLS termination, per-client identity, key rotation mechanism, or request-rate controls. Do not expose it publicly without a security review.
- Files: `Dockerfile`, `src/main.py`, `src/auth.py`, `SECURITY.md`, `docs/DEPLOYMENT.md`.
- Current mitigation: `/agent/evaluate` and `/observability` require an `x-api-key`; `src/auth.py` rejects absent, short, and known-default server keys and uses constant-time comparison; documentation routes are disabled.
- Recommendations: Put the API behind TLS and an access-controlled gateway; provision and rotate secrets via the deployment environment; add rate limiting and audited client identities for multi-tenant use.

**Production data and process permissions:**
- Risk: The image runs with its default root user; telemetry and reports are stored as SQLite JSON in the operator-supplied database file, and `MonitoringService` does not configure file permissions or encryption.
- Files: `Dockerfile`, `src/services/monitoring_service.py`, `docs/DEPLOYMENT.md`, `SECURITY.md`.
- Current mitigation: Container mode requires an absolute, non-memory database path; documented deployment requires a private persistent volume.
- Recommendations: Run as a dedicated non-root user, restrict mount/file permissions, encrypt backups/storage as needed, and validate access on the real deployment host.

## Performance Bottlenecks

**Synchronous database operations serialize evaluation:**
- Problem: All evaluate and observability requests sharing a service acquire one `threading.Lock`; each write holds the lock through transaction, history JSON decoding, anomaly calculation, and commit. SQLite writers on other connections can wait up to 30 seconds.
- Files: `src/services/monitoring_service.py`, `src/main.py`, `src/config.py`.
- Cause: One `check_same_thread=False` SQLite connection plus in-process lock and `BEGIN IMMEDIATE`; history processing reads up to `HISTORY_LIMIT` (20) entries for each write.
- Improvement path: Measure latency under concurrent load; shorten the transaction/read section or use a separate shared transactional service before adding replicas. Retain atomic replay and alert-state semantics exercised by `tests/test_p0_integrity.py`.

**Unbounded observation retention:**
- Problem: The API returns only the latest 20 entries, but every unique observation and full report remains in `observations` indefinitely.
- Files: `src/services/monitoring_service.py`, `src/config.py`, `tests/test_p0_integrity.py`.
- Cause: `HISTORY_LIMIT` limits SELECT results, not database size; no pruning, archival, quota, or capacity monitoring is implemented.
- Improvement path: Set a retention/audit policy and implement archival or transaction-safe pruning while preserving UUID replay requirements; monitor database and volume capacity.

**Unbounded Streamlit session history:**
- Problem: Each dashboard rerun appends to `st.session_state.history`, and the entire list is passed to anomaly detection and the trend chart.
- Files: `app.py`, `src/stability_engine.py`.
- Cause: Session history has no cap; `detect_anomaly()` computes mean and standard deviation over the entire list for every rerun.
- Improvement path: Bound session history to a documented window or persist sampled/aggregated data; test behavior after long sessions.

## Fragile Areas

**Recovery policy and anomaly latch:**
- Files: `src/services/monitoring_service.py`, `src/stability_engine.py`, `tests/test_recovery_calibration.py`, `docs/operational-readiness-005c.md`.
- Why fragile: Two fresh consecutive Stable observations clear an alert without any minimum elapsed time; `tests/test_recovery_calibration.py` explicitly verifies that one-second and one-day gaps behave alike. This policy has no labeled-incident calibration or approved false-clear target.
- Safe modification: Define incident labels, observation cadence, and operator-approved false-clear criteria; evaluate candidate rules on held-out incidents before changing the state machine. Preserve transactional replay and restart behavior in `tests/test_p0_integrity.py`.
- Test coverage: Synthetic transitions and restart/replay are tested; production-incident calibration and false-clear rates are not.

**Storage failure and readiness reporting:**
- Files: `src/main.py`, `src/services/monitoring_service.py`, `tests/test_storage_errors.py`, `tests/full_volume.py`, `docs/operational-readiness-005c.md`.
- Why fragile: Write-time `sqlite3.OperationalError` maps to retryable HTTP 503 and rolls back, but public `/health` always says running without checking database writeability, disk headroom, task status, or backup freshness. The optional full-volume script checks for any HTTP 5xx, not the exact 503 contract.
- Safe modification: Keep liveness distinct from readiness; implement a non-destructive readiness check plus volume/backup alerts. Extend the disposable full-volume test to assert the structured 503 response while retaining isolation guards.
- Test coverage: Injected failure and SQLite max-page-count tests cover rollback/503; the end-to-end ENOSPC script is opt-in and no production host readiness or alert-delivery check exists.

## Scaling Limits

**Single-host, single-replica SQLite writer:**
- Current capacity: One application process/service and one local SQLite writer connection; recent API history is limited to 20 records, while stored observations are unbounded.
- Limit: No measured throughput limit is recorded; `threading.Lock` protects only one process and the deployment contract explicitly excludes multiple hosts or replicas against a shared SQLite file.
- Scaling path: Benchmark actual write rate and volume use; migrate observation identity, report history, and anomaly state together to a shared transactional store before horizontal scaling.
- Files: `src/services/monitoring_service.py`, `src/config.py`, `docs/DEPLOYMENT.md`, `tests/test_p0_integrity.py`.

## Dependencies at Risk

**Python 3.10 / Streamlit version split:**
- Risk: `requirements.txt` selects different Streamlit ranges by Python version, while `Dockerfile` and CI target Python 3.10; dependency versions other than Streamlit are unconstrained.
- Impact: Dashboard test behavior and rebuild results can vary with interpreter and resolver updates; the Python 3.10 image cannot pick the `>=1.66.1` branch.
- Migration plan: Choose supported interpreter targets, lock each dependency set, and run dashboard/API compatibility tests on every supported target.
- Files: `requirements.txt`, `Dockerfile`, `.github/workflows/ci.yml`, `tests/test_evaluation_pipeline.py`.

## Missing Critical Features

**Operational API release gates:**
- Problem: No actual host-volume verification, scheduled off-volume backup/retention, restore drill, disk alert delivery, or approved production recovery policy is implemented; container lifecycle tests only exercise disposable volumes.
- Blocks: Production approval and safe public exposure of the stateful FastAPI service.
- Files: `docs/operational-readiness-005c.md`, `docs/DEPLOYMENT.md`, `tests/container_lifecycle.py`, `tests/full_volume.py`, `Dockerfile`.

**Dashboard/API observability integration:**
- Problem: The Streamlit UI calculates session-local scores and trends; it does not query authenticated `/observability`, show durable API alert state, or publish observations to `/agent/evaluate`.
- Blocks: Using the hosted dashboard as a view or control surface for the persistent API deployment.
- Files: `app.py`, `src/main.py`, `docs/DEPLOYMENT.md`, `tests/test_evaluation_pipeline.py`.

## Test Coverage Gaps

**Autonomous task supervision and shutdown:**
- What's not tested: Failure or cancellation of `monitoring_loop()`, whether the background task remains healthy, and whether the process-global connection is closed on shutdown.
- Files: `src/main.py`, `src/services/monitoring_service.py`, `tests/test_api_health.py`, `tests/test_health.py`.
- Risk: Background checks can stop silently while `/health` continues to return success.
- Priority: Medium.

**Multi-client abuse and secret lifecycle:**
- What's not tested: Key rotation, per-client revocation, high request rates, public proxy/TLS configuration, and database file permissions.
- Files: `src/auth.py`, `src/main.py`, `Dockerfile`, `tests/test_auth.py`.
- Risk: One stolen shared key or missing edge controls can grant broad access or enable resource exhaustion.
- Priority: High before public exposure.

**Long-lived storage growth and operational alerting:**
- What's not tested: Sustained high-volume ingestion, retention policy, storage capacity alarms, backup scheduling/failure notifications, and readiness when disk is full.
- Files: `src/services/monitoring_service.py`, `src/main.py`, `tests/test_p0_integrity.py`, `tests/full_volume.py`, `docs/DEPLOYMENT.md`.
- Risk: An otherwise correct single-request rollback cannot prevent a full production disk or missed backups.
- Priority: High before stateful deployment.

---

*Concerns audit: 2026-11-23*
