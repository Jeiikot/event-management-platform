
def test_create_list_get_update_delete_event(client, auth_headers):
    # create
    payload = {
        "title": "TechConf",
        "description": "Annual conference",
        "location": "Bogota",
        "start_time": "2025-09-01T09:00:00",
        "end_time": "2025-09-01T17:00:00",
        "capacity": 200
    }
    response = client.post("/api/v1/events", json=payload, headers=auth_headers)
    assert r.status_code in (200,201), r.text
    event = response.json()
    event_id = event["id"]
    assert event["title"] == payload["title"]

    # list
    response = client.get("/api/v1/events", headers=auth_headers)
    assert response.status_code == 200
    items = response.json()["items"]
    assert any(e["id"] == event_id for e in items)

    # get by id
    response = client.get(f"/api/v1/events/{event_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == event_id

    # update
    response = client.put(f"/api/v1/events/{event_id}", json={
        "title": "TechConf Updated",
        "description": "Updated desc",
        "location": "Medellin",
        "start_time": "2025-09-02T09:00:00",
        "end_time": "2025-09-02T17:00:00",
        "capacity": 150
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "TechConf Updated"

    # delete
    response = client.delete(f"/api/v1/events/{event_id}", headers=auth_headers)
    assert response.status_code == 204
