# Third-party imports
from fastapi.testclient import TestClient


def test_session_crud(client: TestClient, auth_headers: dict) -> None:
    event_payload = {
        "name": "Session Event",
        "description": "Event with sessions",
        "venue": "Neiva",
        "start_at": "2025-09-01T10:00:00",
        "end_at": "2025-09-01T18:00:00",
        "capacity_total": 100,
        "capacity_available": 100,
    }
    ev_resp = client.post("/api/v1/events", json=event_payload, headers=auth_headers)
    assert ev_resp.status_code in (200, 201), ev_resp.text
    event_id = ev_resp.json()["id"]

    session_payload = {
        "title": "Morning Session",
        "description": "Intro",
        "room": "A1",
        "start_at": "2025-09-01T10:00:00",
        "end_at": "2025-09-01T12:00:00",
        "capacity_total": 50,
        "capacity_available": 50,
        "speaker_ids": []
    }
    create_resp = client.post(
        f"/api/v1/sessions/events/{event_id}",
        json=session_payload,
        headers=auth_headers,
    )
    assert create_resp.status_code in (200, 201), create_resp.text
    created = create_resp.json()
    assert "id" in created, f"Esperaba id en la respuesta de creación: {created}"
    session_id = created["id"]

    list_resp = client.get(f"/api/v1/sessions/events/{event_id}", headers=auth_headers)
    assert list_resp.status_code == 200, list_resp.text
    sessions = list_resp.json()
    assert any(s["id"] == session_id for s in sessions)

    update_payload = {
        "title": "Updated Session",
        "description": "Updated desc",
        "room": "B2",
        "capacity_total": created.get("capacity_total", session_payload["capacity_total"]),
        "capacity_available": created.get("capacity_available", session_payload["capacity_available"]),
    }
    patch_resp = client.patch(
        f"/api/v1/sessions/{session_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert patch_resp.status_code == 200, patch_resp.text
    assert patch_resp.json()["title"] == "Updated Session"
    assert patch_resp.json()["room"] == "B2"

    del_resp = client.delete(f"/api/v1/sessions/{session_id}", headers=auth_headers)
    assert del_resp.status_code in (200, 204), del_resp.text
