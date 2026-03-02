from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_auth_required():
    response = client.get("/stability")
    assert response.status_code in [401, 422]
