# Architecture

Mapped: 2026-11-03. Source: checked local AI-OS checkout.

## System boundary

- The repository holds two distinct entrypoints: `app.py` for a Streamlit demonstration and `src/main.py` for an API.
- Both use scoring from `src/stability_engine.py`, but the dashboard does not call the API or share its SQLite state.
- `Dockerfile` starts `src.main:app`, not the Streamlit dashboard.

## API data flow

1. `src/main.py` accepts a POST at `/agent/evaluate`.
2. `src/models.py` parses four strict float metrics plus an optional UUID.
3. `src/auth.py` checks the API key before evaluation.
4. `src/services/monitoring_service.py` calls `src/agent.py` to generate a report.
5. `src/agent.py` calls `src/stability_engine.py` for scores and `src/guardrails.py` for the tier.
6. `src/services/monitoring_service.py` commits observation, replay identity, and anomaly state to SQLite in one transaction.
7. `/observability` reads the most recent 20 entries and current anomaly state.

## Persistence and concurrency

- `src/services/monitoring_service.py` has unique observation IDs and serializes local connection access with a lock.
- `BEGIN IMMEDIATE` protects duplicate lookup and insert across SQLite connections.
- The durable table keeps all rows. `MonitoringConfig.HISTORY_LIMIT` only limits returned history.
- Reuse of an ID with different input returns HTTP 409. Identical input with that ID returns its original report.
- Without an ID, only a consecutive equal payload is treated as replay.
- Docker mode rejects a missing or relative database path. A path check alone does not establish a host mount.

## Alert behavior

- A Critical observation latches anomaly state in `src/services/monitoring_service.py`.
- Two fresh consecutive Stable observations clear the latch. Warning or Critical resets the recovery counter.
- Elapsed time is not part of this rule. `tests/test_recovery_calibration.py` documents the one-second/day equivalence.
- `src/main.py` starts an asynchronous monitoring loop. Its `autonomous_check` reads state without adding an observation.

## Dashboard path

- `app.py` reads sidebar sliders and calls `calculate_adsi`, `detect_degradation`, and `detect_anomaly`.
- Streamlit `st.session_state.history` holds dashboard points for that user session only.
- The "Simulate Degradation" button creates random metrics, but the following sidebar assignment replaces them before scoring.

## Deployment boundary

- `tests/container_lifecycle.py` and `tests/full_volume.py` check disposable Docker volumes.
- `docs/operational-readiness-005c.md` leaves actual mount, scheduled backup, restore drill, and disk alerts open.
