# Third-party imports
from fastapi.testclient import TestClient

# Local imports
from app.tests.helpers import make_event_payload


def test_register_to_event_and_conflict(client: TestClient, auth_headers: dict) -> None:
    # Create event with capacity 1
    event_payload = make_event_payload(name="Cap1", capacity_total=1, capacity_available=1)
    event_response = client.post("/api/v1/events", json=event_payload, headers=auth_headers)
    assert event_response.status_code in (200, 201), event_response.text
    event_id = event_response.json()["id"]

    # First registration ok
    first_registration_response = client.post(
        f"/api/v1/registrations/events/{event_id}", headers=auth_headers
    )
    assert first_registration_response.status_code in (200, 201), first_registration_response.text

    # Second registration should conflict (409/400) because user already registered or full
    second_registration_response = client.post(
        f"/api/v1/registrations/events/{event_id}", headers=auth_headers
    )
    assert second_registration_response.status_code in (400, 409), second_registration_response.text

    # "My registrations" lists it
    my_regs_response = client.get("/api/v1/registrations/events", headers=auth_headers)
    assert my_regs_response.status_code == 200, my_regs_response.text
    my_regs = my_regs_response.json()
    assert any(registration["event_id"] == event_id for registration in my_regs)
