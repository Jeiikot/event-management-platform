
# Third-party imports
from fastapi.testclient import TestClient

# Local imports
from .helpers import make_event_payload


def test_event_capacity_validation(client: TestClient, auth_headers: dict) -> None:
    invalid_payload = make_event_payload(capacity_total=10, capacity_available=11)
    response = client.post("/api/v1/events", json=invalid_payload, headers=auth_headers)

    assert response.status_code == 422, response.text
