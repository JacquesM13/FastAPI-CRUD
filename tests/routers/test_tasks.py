from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_tasks_unauthenticated():
    response = client.get("/tasks/")
    assert response.status_code == 401