from fastapi.testclient import TestClient

from src.main import app
from src.services.monitoring_service import MonitoringService


def test_evaluation_pipeline(monkeypatch):
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

    with TestClient(app) as client:
        assert client.get("/observability").json() == {
            "message": "No evaluations performed yet"
        }
        for _ in range(5):
            response = client.post("/agent/evaluate", json=stable)
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
        assert [entry["ADSI"] for entry in observability.json()["history"]] == [
            1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.0
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