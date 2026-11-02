from fastapi.testclient import TestClient
from secrets import token_urlsafe
from pathlib import Path
from streamlit.testing.v1 import AppTest

from src.main import app
from src.services.monitoring_service import MonitoringService


def test_evaluation_pipeline(monkeypatch):
    api_key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", api_key)
    monitor = MonitoringService()
    monkeypatch.setattr("src.main.monitor", monitor)
    stable = {
        "kpi_error": 0.0,
        "retrieval_score": 1.0,
        "latency_dev": 0.0,
        "embedding_shift": 0.0,
    }
    critical = {
        "kpi_error": 1.0,
        "retrieval_score": 0.0,
        "latency_dev": 1.0,
        "embedding_shift": 1.0,
    }

    with TestClient(app, headers={"x-api-key": api_key}) as client:
        assert client.get("/observability").json() == {
            "message": "No evaluations performed yet"
        }
        for offset in range(5):
            response = client.post("/agent/evaluate", json={**stable, "kpi_error": offset / 1000})
            assert response.status_code == 200
            assert response.json()["stability_tier"] == "Stable"
            assert response.json()["guardrail_flags"] == "stable"

        assert client.get("/observability").json()["anomaly"] is False

        mixed = {"kpi_error": 0.1, "retrieval_score": 0.9,
                 "latency_dev": 0.1, "embedding_shift": 0.1}
        response = client.post("/agent/evaluate", json=mixed)
        assert response.status_code == 200
        assert response.json()["scores"]["ADSI"] == 0.9
        assert response.json()["stability_tier"] == "Stable"

        response = client.post("/agent/evaluate", json=critical)
        assert response.status_code == 200
        assert response.json()["scores"]["ADSI"] == 0.0
        assert response.json()["stability_tier"] == "Critical"
        assert response.json()["guardrail_flags"] == "critical"

        observability = client.get("/observability")
        assert observability.status_code == 200
        assert observability.json()["current"]["ADSI"] == 0.0
        assert [round(entry["ADSI"], 6) for entry in observability.json()["history"]] == [
            1.0, 0.999667, 0.999333, 0.999, 0.998667, 0.9, 0.0
        ]
        assert observability.json()["degradation"] == "critical"
        assert observability.json()["anomaly"] is True

        response = client.post("/agent/evaluate", json={**stable, "retrieval_score": 0.4})
        assert response.json()["stability_tier"] == "Warning"
        assert response.json()["guardrail_flags"] == "warning"

        response = client.post("/agent/evaluate", json={**stable, "retrieval_score": 0.0})
        assert response.json()["stability_tier"] == "Degrading"
        assert response.json()["guardrail_flags"] == "degrading"
        assert client.get("/observability").json()["degradation"] == "degrading"


def test_dashboard_scoring_matches_api(monkeypatch):
    """Compare shared scoring; the dashboard does not call the backend API."""
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monkeypatch.setattr("src.main.monitor", MonitoringService())
    dashboard = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "app.py", default_timeout=30
    ).run()
    assert not dashboard.exception

    with TestClient(app, headers={"x-api-key": key}) as client:
        for values in ((0.1, 0.9, 0.1, 0.05), (1.0, 0.0, 1.0, 1.0)):
            for slider, value in zip(dashboard.sidebar.slider, values):
                slider.set_value(value)
            dashboard.run()
            assert not dashboard.exception
            metrics = dict(zip(
                ("kpi_error", "retrieval_score", "latency_dev", "embedding_shift"),
                values,
            ))
            response = client.post("/agent/evaluate", json=metrics)
            assert response.status_code == 200
            report = response.json()
            assert dashboard.metric[0].value == str(round(report["scores"]["ADSI"], 3))
            assert dashboard.metric[1].value == report["stability_tier"].upper()