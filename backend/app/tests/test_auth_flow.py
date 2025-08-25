
# Third-party imports
from fastapi.testclient import TestClient


def test_register_and_login_flow(client: TestClient, user_payload: dict) -> None:
    # Register
    register_response = client.post("/api/v1/auth/register", json=user_payload)
    assert register_response.status_code in (200, 201), register_response.text
    registered_user = register_response.json()
    assert registered_user["email"] == user_payload["email"]
    assert registered_user["is_active"] is True

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json().get("access_token")
    assert isinstance(access_token, str) and len(access_token) > 0
