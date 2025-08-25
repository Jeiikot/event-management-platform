# Third-party imports
from fastapi.testclient import TestClient

def test_create_list_get_update_delete_event(client: TestClient, auth_headers: dict) -> None:
    # create
    payload = {
        "name": "TechConf",
        "description": "Annual conference",
        "venue": "Bogota",
        "start_at": "2025-09-01T09:00:00",
        "end_at": "2025-09-01T17:00:00",
        "capacity_total": 200,
        "capacity_available": 200,
    }
    response = client.post("/api/v1/events", json=payload, headers=auth_headers)
    assert response.status_code in (200, 201), response.text
    event = response.json()
    event_id = event["id"]
    assert event["name"] == payload["name"]

    # list
    response = client.get("/api/v1/events", headers=auth_headers)
    assert response.status_code == 200, response.text
    page = response.json()
    items = page["items"] if isinstance(page, dict) and "items" in page else page
    assert any(e["id"] == event_id for e in items)

    # get by id
    response = client.get(f"/api/v1/events/{event_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == event_id

    response = client.get(f"/api/v1/events/{event_id}", headers=auth_headers)
    current = response.json()
    update_payload = {
        "name": "TechConf Updated",
        "description": "Updated desc",
        "venue": "Medellin",
        "start_at": "2025-09-02T09:00:00",
        "end_at": "2025-09-02T17:00:00",
        "capacity_total": current.get("capacity_total", 200),
        "capacity_available": current.get("capacity_available", 200),
    }
    response = client.patch(f"/api/v1/events/{event_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "TechConf Updated"

    # delete (soft)
    response = client.delete(f"/api/v1/events/{event_id}", headers=auth_headers)
    assert response.status_code in (200, 204), response.text
