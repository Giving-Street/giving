import pytest
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import Scope, Receive, Send

from giving_account.app import app

TEST_TOKEN = ""


@pytest.fixture
def client():
    return TestClient(app)


def test_google_auth_login_should_redirect(client):
    response = client.get("/auth/google/login", allow_redirects=False)
    assert response.status_code == 302


def test_google_auth_token_respond_401_without_valid_token(client):
    response = client.get("/auth/google/token", allow_redirects=False)
    assert response.status_code == 401


def test_google_auth_logout_without_token_should_respond_403(client):
    response = client.get("/auth/google/logout", allow_redirects=False)
    assert response.status_code == 403


def test_signup_should_return_account_info(client):
    response = client.post("/accounts", json={"email": "test@noreply.com", "provider": "google"})
    assert response.status_code == 200
    assert response.json().get("id_") is not None


def test_sign_up_without_user_info_in_session_should_return_redirect_response(client):
    response = client.post("/accounts", json={"email": "test@noreply.com", "provider": "google"})
    assert response.status_code == 403
