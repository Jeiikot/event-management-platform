
# Third-party imports
from fastapi.testclient import TestClient


def test_me_endpoint(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200, response.text
    user_data = response.json()
    assert user_data["email"].endswith("@example.com")
    assert user_data["is_active"] is True
