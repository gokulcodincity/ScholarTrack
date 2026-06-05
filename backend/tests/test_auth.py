from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200


def test_login_endpoint_exists():
    response = client.post("/auth/login", json={})

    assert response.status_code in [401, 422]