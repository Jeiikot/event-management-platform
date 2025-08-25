
# Third-party imports
from fastapi.testclient import TestClient


def test_protected_endpoints_require_token(client: TestClient) -> None:
    me_response = client.get("/api/v1/users/me")
    assert me_response.status_code in (401, 403)

    create_event_response = client.post("/api/v1/events", json={})
    assert create_event_response.status_code in (401, 403, 422)
