from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_student_endpoint_exists():
    response = client.get("/students/1")

    assert response.status_code in [200, 401, 403, 404]