import pytest
from fastapi.testclient import TestClient

from giving_account.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_google_auth_login_should_redirect(client):
    response = client.get("/auth/google/login", allow_redirects=False)
    assert response.status_code == 302


def test_google_auth_token_respond_401_without_valid_token(client):
    response = client.get("/auth/google/auth", allow_redirects=False)
    assert response.status_code == 401


def test_google_auth_logout_without_token_should_respond_403(client):
    response = client.get("/auth/google/logout", allow_redirects=False)
    assert response.status_code == 403
