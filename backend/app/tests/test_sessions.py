
def test_session_crud(client, auth_headers):
    # First create event
    event_payload = {
        "title": "Session Event",
        "description": "Event with sessions",
        "location": "Neiva",
        "start_time": "2025-09-01T10:00:00",
        "end_time": "2025-09-01T18:00:00",
        "capacity": 100
    }
    ev = client.post("/api/v1/events", json=event_payload, headers=auth_headers).json()
    event_id = ev["id"]

    # create session
    payload = {
        "title": "Morning Session",
        "description": "Intro",
        "event_id": event_id,
        "start_time": "2025-09-01T10:00:00",
        "end_time": "2025-09-01T12:00:00"
    }
    r = client.post("/api/v1/sessions", json=payload, headers=auth_headers)
    assert r.status_code in (200,201), r.text
    session = r.json()
    s_id = session["id"]

    # list sessions
    r2 = client.get("/api/v1/sessions", headers=auth_headers)
    assert r2.status_code == 200
    assert any(s["id"] == s_id for s in r2.json())

    # update session
    r3 = client.put(f"/api/v1/sessions/{s_id}", json={
        "title": "Updated Session",
        "description": "Updated desc",
        "event_id": event_id,
        "start_time": "2025-09-01T11:00:00",
        "end_time": "2025-09-01T13:00:00"
    }, headers=auth_headers)
    assert r3.status_code == 200
    assert r3.json()["title"] == "Updated Session"

    # delete
    r4 = client.delete(f"/api/v1/sessions/{s_id}", headers=auth_headers)
    assert r4.status_code == 204
