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
