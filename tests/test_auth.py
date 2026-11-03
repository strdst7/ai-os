from secrets import token_urlsafe

from fastapi.testclient import TestClient
from src.main import app
from src.services.monitoring_service import MonitoringService


def test_private_endpoints_require_key(monkeypatch):
    key = token_urlsafe(32)
    monkeypatch.setenv("AIOS_API_KEY", key)
    monitor = MonitoringService()
    monkeypatch.setattr("src.main.monitor", monitor)
    telemetry = {"kpi_error": 0.0, "retrieval_score": 1.0,
                 "latency_dev": 0.0, "embedding_shift": 0.0}

    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        for method, path, kwargs in (
            ("post", "/agent/evaluate", {"json": telemetry}),
            ("get", "/observability", {}),
        ):
            request = getattr(client, method)
            for headers in ({}, {"x-api-key": token_urlsafe(32)},
                            {"x-api-key": "dev-key"}):
                response = request(path, headers=headers, **kwargs)
                assert response.status_code == 401
            response = request(path, headers={"x-api-key": key}, **kwargs)
            assert response.status_code == 200

        assert len(client.get("/observability", headers={"x-api-key": key}).json()["history"]) == 1
        for path in ("/docs", "/redoc", "/openapi.json"):
            assert client.get(path).status_code == 404


def test_weak_server_keys_fail_closed(monkeypatch):
    with TestClient(app) as client:
        for server_key in (None, "", "dev-key", "changeme", "a" * 31, " " * 32):
            if server_key is None:
                monkeypatch.delenv("AIOS_API_KEY", raising=False)
            else:
                monkeypatch.setenv("AIOS_API_KEY", server_key)
            for headers in ({}, {"x-api-key": server_key or token_urlsafe(32)}):
                assert client.get("/observability", headers=headers).status_code == 503
                assert client.post("/agent/evaluate", headers=headers, json={}).status_code == 503
