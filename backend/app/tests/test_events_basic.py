
def test_create_and_list_events(client, auth_headers):
    # Create
    payload = {
        "title": "PyDay 2025",
        "description": "Community meetup",
        "location": "Neiva",
        "start_time": "2025-09-01T10:00:00",
        "end_time": "2025-09-01T12:00:00",
        "capacity": 100
    }
    response = client.post("/api/v1/events", json=payload, headers=auth_headers)
    assert response.status_code in (200, 201), r.text
    event = response.json()
    assert event["title"] == payload["title"]
    event_id = event["id"]

    # List (pagination defaults)
    response = client.get("/api/v1/events", headers=auth_headers)
    assert response.status_code == 200
    page = response.json()
    assert "items" in page and any(e["id"] == event_id for e in page["items"])
