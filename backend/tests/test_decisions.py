from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_decisions_endpoint_exists():
    response = client.get("/admin/decisions")

    assert response.status_code in [200, 401, 403]