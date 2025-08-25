
# Standard library imports
import os

# Third-party imports
import pytest
from fastapi.testclient import TestClient

# Local imports
from app.api import create_app
from app.core.db import init_db


# Configure default environment for isolated tests
os.environ.setdefault("ENV", "dev")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault("API_V1_PREFIX", "/api/v1")
os.environ.setdefault("DOCS_ENABLED", "false")
os.environ.setdefault("ALLOWED_ORIGINS", "*")


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Provide a FastAPI TestClient with an in-memory database for each test."""
    application = create_app()
    init_db()  # ENV=dev triggers create_all
    with TestClient(application) as test_client:
        yield test_client


@pytest.fixture
def user_payload() -> dict:
    """Default valid user payload for registration and login tests."""
    return {
        "email": "alice@example.com",
        "password": "StrongPass!123",
        "full_name": "Alice Doe"
    }


@pytest.fixture
def auth_headers(client: TestClient, user_payload: dict) -> dict:
    """Return Authorization headers for an authenticated test user."""
    register_response = client.post("/api/v1/auth/register", json=user_payload)
    assert register_response.status_code in (200, 201), register_response.text

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text

    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
