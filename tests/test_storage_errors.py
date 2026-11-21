import json
import sqlite3

import pytest
from fastapi.testclient import TestClient
from secrets import token_urlsafe

import src.main as main
from src.main import app
from src.services.monitoring_service import MonitoringService

STABLE = {"kpi_error": 0.0, "retrieval_score": 1.0,
          "latency_dev": 0.0, "embedding_shift": 0.0}
CRITICAL = {"kpi_error": 1.0, "retrieval_score": 0.0,
            "latency_dev": 1.0, "embedding_shift": 1.0}


@pytest.mark.parametrize(
    "message,expected",
    [
        ("database or disk is full", "storage_full:"),
        ("database is locked", "storage_busy:"),
        ("attempt to write a readonly database", "storage_unavailable:"),
        ("unable to open database file", "storage_unavailable:"),
        ("disk I/O error", "storage_error:"),
    ],
)
def test_operational_error_messages_map_to_distinct_details(message, expected):
    """Every mapped branch returns a retryable 503 with a stable prefix."""
    response = main.storage_error_handler(None, sqlite3.OperationalError(message))
    assert response.status_code == 503
    assert response.headers["retry-after"] == "5"
    payload = json.loads(response.body)
    assert payload["retryable"] is True
    assert payload["detail"].startswith(expected)


def test_storage_error_body_does_not_leak_sqlite_internals():
    response = main.storage_error_handler(None, sqlite3.OperationalError("database or disk is full"))
    text = response.body.decode().lower()
    assert "disk is full" not in text
    assert "sqlite" not in text
    assert "traceback" not in text


def test_api_maps_storage_failure_to_structured_503(monkeypatch, tmp_path):
    """End-to-end: a genuine SQLite failure on the API path is not a bare 500."""
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monitor = MonitoringService(tmp_path / "observations.db")
    monkeypatch.setattr("src.main.monitor", monitor)

    def boom(telemetry, mode="manual_trigger"):
        raise sqlite3.OperationalError("database or disk is full")

    monkeypatch.setattr(monitor, "evaluate", boom)
    with TestClient(app, headers={"x-api-key": key}) as client:
        response = client.post("/agent/evaluate", json=STABLE)
        assert response.status_code == 503
        body = response.json()
        assert body["retryable"] is True
        assert body["detail"].startswith("storage_full:")
        assert response.headers["retry-after"] == "5"


def test_rejected_write_leaves_history_and_alert_untouched(monkeypatch, tmp_path):
    """Contract from docs/operational-readiness-005c.md."""
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monitor = MonitoringService(tmp_path / "observations.db")
    monkeypatch.setattr("src.main.monitor", monitor)

    with TestClient(app, headers={"x-api-key": key}) as client:
        assert client.post("/agent/evaluate", json=CRITICAL).status_code == 200
        before = client.get("/observability").json()

        original = monitor.evaluate
        monkeypatch.setattr(
            monitor, "evaluate",
            lambda telemetry, mode="manual_trigger": (_ for _ in ()).throw(
                sqlite3.OperationalError("database or disk is full")
            ),
        )
        assert client.post("/agent/evaluate", json=STABLE).status_code == 503
        assert client.get("/observability").json() == before
        monkeypatch.setattr(monitor, "evaluate", original)


def test_service_layer_still_raises_operational_error(tmp_path):
    """The service keeps its native exception; only the HTTP layer remaps it."""
    monitor = MonitoringService(tmp_path / "observations.db")
    monitor.db.execute("PRAGMA query_only=1")
    with pytest.raises(sqlite3.OperationalError):
        monitor.evaluate({**CRITICAL})
    monitor.close()
