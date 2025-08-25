
# Third-party imports
from fastapi.testclient import TestClient

# Local imports
from .helpers import make_event_payload, make_session_payload


def test_sessions_under_event_crud(client: TestClient, auth_headers: dict) -> None:
    # Create event to host sessions
    event_payload = make_event_payload(name="SessConf")
    event_response = client.post("/api/v1/events", json=event_payload, headers=auth_headers)
    assert event_response.status_code in (200, 201), event_response.text
    event_id = event_response.json()["id"]

    # Create session
    session_payload = make_session_payload(title="Talk 1")
    create_session_response = client.post(
        f"/api/v1/sessions/events/{event_id}", json=session_payload, headers=auth_headers
    )
    assert create_session_response.status_code in (200, 201), create_session_response.text
    session_id = create_session_response.json()["id"]

    # List sessions for event
    list_sessions_response = client.get(f"/api/v1/sessions/events/{event_id}", headers=auth_headers)
    assert list_sessions_response.status_code == 200, list_sessions_response.text
    sessions = list_sessions_response.json()
    assert any(single_session["id"] == session_id for single_session in sessions)

    # Update session
    update_session_payload = {"room": "B2"}
    update_session_response = client.patch(
        f"/api/v1/sessions/{session_id}", json=update_session_payload, headers=auth_headers
    )
    assert update_session_response.status_code == 200, update_session_response.text
    assert update_session_response.json()["room"] == "B2"

    # Delete session
    delete_session_response = client.delete(f"/api/v1/sessions/{session_id}", headers=auth_headers)
    assert delete_session_response.status_code in (200, 204), delete_session_response.text
