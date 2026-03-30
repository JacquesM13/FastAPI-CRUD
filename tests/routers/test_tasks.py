from fastapi.testclient import TestClient
from sentry_sdk.tracing_utils import add_sentry_baggage_to_headers

from app.main import app
from app import models, schemas
from app.core.security import hash_password
from app.core.auth import create_access_token

def test_get_tasks_unauthenticated(client):
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_get_tasks_authenticated(client, test_user, auth_headers_for_user):
    auth_headers = auth_headers_for_user(test_user)
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200

def test_can_access_own_task(client, auth_headers_for_user, test_user, test_user_task):
    auth_headers = auth_headers_for_user(test_user)
    response = client.get(f"/tasks/{test_user_task.id}", headers=auth_headers)
    assert response.status_code == 200

def test_cannot_access_other_users_tasks(client, auth_headers_for_user, test_user, other_user_task):
    auth_headers = auth_headers_for_user(test_user)
    response = client.get(f"/tasks/{other_user_task.id}", headers=auth_headers)
    assert response.status_code == 403

def test_unauthenticated_single_task(client, other_user_task):
    response = client.get(f"/tasks/{other_user_task.id}")
    assert response.status_code == 401

def test_access_task_does_not_exist(client, auth_headers_for_user, test_user):
    auth_headers = auth_headers_for_user(test_user)
    response = client.get("/tasks/9999999", headers=auth_headers)
    assert response.status_code == 404