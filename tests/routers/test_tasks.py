from fastapi.testclient import TestClient
from app.main import app
from app import models, schemas
from app.core.security import hash_password
from app.core.auth import create_access_token

def test_get_tasks_unauthenticated(client):
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_get_tasks_authenticated(client, auth_headers):
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200