import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from math import nan
from secrets import token_urlsafe
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.agent import generate_stability_report
from src.main import app
from src.services.monitoring_service import MonitoringService
from src.stability_engine import calculate_adsi


STABLE = {"kpi_error": 0.0, "retrieval_score": 1.0,
          "latency_dev": 0.0, "embedding_shift": 0.0}
CRITICAL = {"kpi_error": 1.0, "retrieval_score": 0.0,
            "latency_dev": 1.0, "embedding_shift": 1.0}


def test_missing_drift_never_looks_healthy(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    with TestClient(app, headers={"x-api-key": key}) as client:
        for field in ("latency_dev", "embedding_shift"):
            incomplete = {name: value for name, value in STABLE.items() if name != field}
            for calculate in (calculate_adsi, generate_stability_report):
                with pytest.raises(ValueError, match="insufficient_data"):
                    calculate(incomplete)
            assert client.post("/agent/evaluate", json=incomplete).status_code == 422


def test_missing_any_metric_is_insufficient():
    for field in STABLE:
        metrics = {name: value for name, value in STABLE.items() if name != field}
        with pytest.raises(ValueError, match="insufficient_data"):
            generate_stability_report(metrics)


@pytest.mark.parametrize("value", [None, nan, float("inf"), -1, 2, "bad", True])
def test_invalid_drift_is_rejected(value):
    metrics = {**STABLE, "latency_dev": value}
    for calculate in (calculate_adsi, generate_stability_report):
        with pytest.raises(ValueError, match="(invalid_data|insufficient_data)"):
            calculate(metrics)


def test_api_rejects_invalid_drift(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    with TestClient(app, headers={"x-api-key": key}) as client:
        for value in (None, "NaN", "Infinity", -1, 2, "bad", True):
            response = client.post("/agent/evaluate", json={**STABLE, "latency_dev": value})
            assert response.status_code == 422
        assert client.post("/agent/evaluate", json={**STABLE, "unexpected": 1}).status_code == 422


def test_invalid_submission_keeps_history_unchanged(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monkeypatch.setattr("src.main.monitor", MonitoringService())
    with TestClient(app, headers={"x-api-key": key}) as client:
        assert client.post("/agent/evaluate", json=STABLE).status_code == 200
        before = client.get("/observability").json()
        assert client.post("/agent/evaluate", json={**STABLE, "latency_dev": None}).status_code == 422
        assert client.get("/observability").json() == before


def test_valid_score_paths_remain_consistent():
    metrics = {"kpi_error": 0.1, "retrieval_score": 0.9,
               "latency_dev": 0.1, "embedding_shift": 0.05}
    assert calculate_adsi(metrics) == generate_stability_report(metrics)["scores"]["ADSI"]
    assert calculate_adsi(0.9, 0.9, 0.925) == calculate_adsi(metrics)


def test_replay_preserves_anomaly_and_fresh_recovery(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monitor = MonitoringService()
    monkeypatch.setattr("src.main.monitor", monitor)
    with TestClient(app, headers={"x-api-key": key}) as client:
        for offset in range(19):
            assert client.post("/agent/evaluate", json={**STABLE, "kpi_error": offset / 1000}).status_code == 200
        critical_response = client.post("/agent/evaluate", json=CRITICAL)
        assert critical_response.status_code == 200
        initial = client.get("/observability").json()
        assert len(initial["history"]) == 20
        assert initial["anomaly"] is True
        identifiers = [row["observation_id"] for row in initial["history"]]
        assert len(set(identifiers)) == 20
        for identifier in identifiers:
            UUID(identifier)
        for entry in initial["history"]:
            assert datetime.fromisoformat(entry["timestamp"]).utcoffset() == timezone.utc.utcoffset(None)

        for _ in range(25):
            assert client.post("/agent/evaluate", json=CRITICAL).json() == critical_response.json()
            monitor.autonomous_check()
        unchanged = client.get("/observability").json()
        assert unchanged == initial

        first = client.post("/agent/evaluate", json=STABLE)
        assert first.status_code == 200
        after_first = client.get("/observability").json()
        assert len(after_first["history"]) == 20
        assert after_first["anomaly"] is True
        assert after_first["current"]["observation_id"] != identifiers[-1]
        assert after_first["history"][0]["observation_id"] == identifiers[1]
        assert after_first["current"]["ADSI"] == 1.0
        client.post("/agent/evaluate", json=STABLE)
        assert client.get("/observability").json() == after_first

        second = client.post("/agent/evaluate", json={**STABLE, "kpi_error": 0.01})
        assert second.status_code == 200
        recovered = client.get("/observability").json()
        assert recovered["anomaly"] is False
        assert recovered["degradation"] == "stable"
        assert recovered["current"]["ADSI"] < after_first["current"]["ADSI"]
        assert recovered["history"][-2]["observation_id"] == after_first["current"]["observation_id"]


def test_observation_identity_allows_fresh_equal_values_and_rejects_conflicts(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monkeypatch.setattr("src.main.monitor", MonitoringService())
    observation_id = str(uuid4())
    with TestClient(app, headers={"x-api-key": key}) as client:
        first = {**STABLE, "observation_id": observation_id}
        response = client.post("/agent/evaluate", json=first)
        assert response.status_code == 200
        assert client.get("/observability").json()["current"]["observation_id"] == observation_id
        assert client.post("/agent/evaluate", json=first).json() == response.json()
        assert len(client.get("/observability").json()["history"]) == 1
        assert client.post("/agent/evaluate", json={**CRITICAL, "observation_id": observation_id}).status_code == 409
        assert len(client.get("/observability").json()["history"]) == 1

        second_id = str(uuid4())
        second = client.post("/agent/evaluate", json={**STABLE, "observation_id": second_id})
        assert second.status_code == 200
        assert [row["observation_id"] for row in client.get("/observability").json()["history"]] == [
            observation_id, second_id
        ]


def test_concurrent_duplicate_keeps_one_observation():
    monitor = MonitoringService()
    metrics = {**CRITICAL, "observation_id": str(uuid4())}
    with ThreadPoolExecutor(max_workers=8) as executor:
        reports = list(executor.map(monitor.evaluate, [metrics] * 32))
    assert all(report == reports[0] for report in reports)
    assert len(monitor.get_observability()["history"]) == 1


def test_stale_id_replay_cannot_replace_evicted_observation():
    monitor = MonitoringService()
    observation_id = str(uuid4())
    original = {**CRITICAL, "observation_id": observation_id}
    first = monitor.evaluate(original)
    for offset in range(21):
        monitor.evaluate({**STABLE, "kpi_error": offset / 1000,
                          "observation_id": str(uuid4())})
    before = monitor.get_observability()
    assert monitor.evaluate(original) == first
    assert monitor.get_observability() == before
    with pytest.raises(HTTPException, match="Observation ID already used"):
        monitor.evaluate({**STABLE, "observation_id": observation_id})


def test_file_store_survives_restart_and_replay(tmp_path):
    path = tmp_path / "observations.db"
    first = MonitoringService(path)
    observation_id = str(uuid4())
    critical = {**CRITICAL, "observation_id": observation_id}
    report = first.evaluate(critical)
    before = first.get_observability()
    assert before["anomaly"] is True
    first.close()

    restarted = MonitoringService(path)
    assert restarted.get_observability() == before
    assert restarted.evaluate(critical) == report
    assert restarted.get_observability() == before
    with pytest.raises(HTTPException) as conflict:
        restarted.evaluate({**STABLE, "observation_id": observation_id})
    assert conflict.value.status_code == 409
    assert restarted.get_observability() == before
    stable_id = str(uuid4())
    restarted.evaluate({**STABLE, "observation_id": stable_id})
    assert restarted.get_observability()["anomaly"] is True
    restarted.close()

    recovered = MonitoringService(path)
    assert recovered.get_observability()["anomaly"] is True
    recovered.evaluate({**STABLE, "kpi_error": 0.01, "observation_id": str(uuid4())})
    assert recovered.get_observability()["anomaly"] is False
    recovered.close()


def test_two_connections_share_atomic_idempotency(tmp_path):
    path = tmp_path / "shared.db"
    first, second = MonitoringService(path), MonitoringService(path)
    observation = {**CRITICAL, "observation_id": str(uuid4())}
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda service: service.evaluate(observation), (first, second)))
    assert results[0] == results[1]
    assert len(second.get_observability()["history"]) == 1
    assert second.get_observability()["anomaly"] is True
    first.close()
    second.close()


def test_unwritable_store_path_fails_closed(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        MonitoringService(tmp_path / "missing-directory" / "observations.db")


def test_container_mode_requires_explicit_absolute_database_path(monkeypatch, tmp_path):
    monkeypatch.setenv("AIOS_REQUIRE_PERSISTENCE", "1")
    for path in (":memory:", "relative.db"):
        with pytest.raises(ValueError, match="absolute persistent file path"):
            MonitoringService(path)
    monkeypatch.delenv("AIOS_OBSERVATION_DB", raising=False)
    with pytest.raises(ValueError, match="absolute persistent file path"):
        MonitoringService()
    path = tmp_path / "observations.db"
    monkeypatch.setenv("AIOS_OBSERVATION_DB", str(path))
    monitor = MonitoringService()
    monitor.evaluate({**CRITICAL, "observation_id": str(uuid4())})
    monitor.close()
    assert path.is_file()


def test_sqlite_backup_restores_history_and_anomaly(tmp_path):
    original = tmp_path / "observations.db"
    backup = tmp_path / "backup.db"
    restored = tmp_path / "restored.db"
    monitor = MonitoringService(original)
    critical = {**CRITICAL, "observation_id": str(uuid4())}
    monitor.evaluate(critical)
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    before = monitor.get_observability()
    assert before["anomaly"] is True
    with sqlite3.connect(backup) as destination:
        monitor.db.backup(destination)
    monitor.close()
    with sqlite3.connect(backup) as source, sqlite3.connect(restored) as destination:
        assert source.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        source.backup(destination)
    recovered = MonitoringService(restored)
    assert recovered.get_observability() == before
    assert recovered.evaluate(critical)["stability_tier"] == "Critical"
    assert recovered.get_observability() == before
    recovered.evaluate({**STABLE, "observation_id": str(uuid4())})
    assert recovered.get_observability()["anomaly"] is False
    recovered.close()


def test_sqlite_full_rolls_back_observation_and_alert(tmp_path):
    path = tmp_path / "observations.db"
    monitor = MonitoringService(path)
    monitor.evaluate({**CRITICAL, "observation_id": str(uuid4())})
    before = monitor.get_observability()
    pages = monitor.db.execute("PRAGMA page_count").fetchone()[0]
    monitor.db.execute(f"PRAGMA max_page_count={pages}")
    with pytest.raises(sqlite3.OperationalError, match="database or disk is full"):
        monitor.evaluate({**STABLE, "observation_id": str(uuid4()), "padding": "x" * 32768})
    assert monitor.get_observability() == before
    monitor.close()
    restarted = MonitoringService(path)
    assert restarted.get_observability() == before
    assert restarted.db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    restarted.close()
