import pytest
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import Scope, Receive, Send

from giving_account.app import app

TEST_TOKEN = ""


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def session_client():
    class MockSessionMiddleware(SessionMiddleware):
        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            scope["headers"].append(("cookie".encode("utf-8"), f"session={TEST_TOKEN}".encode("utf-8")))
            await super().__call__(scope, receive, send)

    client_ = TestClient(app, raise_server_exceptions=False)
    app.add_middleware(MockSessionMiddleware, secret_key="!test")
    return client_


def test_google_auth_login_should_redirect(client):
    response = client.get("/auth/google/login", allow_redirects=False)
    assert response.status_code == 302


def test_google_auth_token_respond_401_without_valid_token(client):
    response = client.get("/auth/google/auth", allow_redirects=False)
    assert response.status_code == 401


def test_google_auth_logout_without_token_should_respond_403(client):
    response = client.get("/auth/google/logout", allow_redirects=False)
    assert response.status_code == 403


def test_signup_should_return_account_info(session_client):
    response = session_client.post("/accounts", json={"email": "test@noreply.com", "provider": "google"})
    assert response.status_code == 200
    assert response.json().get("id_") is not None


def test_sign_up_without_user_info_in_session_should_return_redirect_response(client):
    response = client.post("/accounts", json={"email": "test@noreply.com", "provider": "google"})
    assert response.status_code == 403
