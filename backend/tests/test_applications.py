from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_applications_endpoint_exists():
    response = client.get("/applications")

    assert response.status_code in [200, 401, 403]