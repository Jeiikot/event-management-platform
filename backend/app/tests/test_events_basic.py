# Third-party imports
from fastapi.testclient import TestClient


def test_create_and_list_events(client: TestClient, auth_headers: dict) -> None:
    # Create
    payload = {
        "name": "PyDay 2025",
        "description": "Community meetup",
        "venue": "Neiva",
        "start_at": "2025-09-01T10:00:00",
        "end_at": "2025-09-01T12:00:00",
        "capacity_total": 100,
        "capacity_available": 100
    }
    response = client.post("/api/v1/events", json=payload, headers=auth_headers)
    assert response.status_code in (200, 201), response.text
    event = response.json()
    assert event["name"] == payload["name"]
    event_id = event["id"]

    # List (pagination defaults)
    response = client.get("/api/v1/events", headers=auth_headers)
    assert response.status_code == 200, response.text
    page = response.json()
    items = page["items"] if isinstance(page, dict) and "items" in page else page
    assert any(e["id"] == event_id for e in items)
