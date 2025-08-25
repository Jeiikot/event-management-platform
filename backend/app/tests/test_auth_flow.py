# Third-party imports
from fastapi.testclient import TestClient


def test_register_and_login_flow(client: TestClient, user_payload: dict) -> None:
    register_response = client.post("/api/v1/auth/register", json=user_payload)
    assert register_response.status_code in (200, 201), register_response.text

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    token_payload = login_response.json()
    assert isinstance(token_payload.get("access_token"), str) and token_payload["access_token"]
    assert token_payload.get("token_type", "bearer") == "bearer"

    headers = {"Authorization": f"Bearer {token_payload['access_token']}"}
    me_response = client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200, me_response.text
    me_data = me_response.json()
    assert me_data["is_active"] is True
    assert me_data["email"] == user_payload["email"]
