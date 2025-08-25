
def test_speaker_crud(client, auth_headers):
    # create speaker
    payload = {"name": "John Doe", "bio": "Expert in Python"}
    r = client.post("/api/v1/speakers", json=payload, headers=auth_headers)
    assert r.status_code in (200,201)
    speaker = r.json()
    sp_id = speaker["id"]

    # list speakers
    r2 = client.get("/api/v1/speakers", headers=auth_headers)
    assert r2.status_code == 200
    assert any(s["id"] == sp_id for s in r2.json())

    # update speaker
    r3 = client.put(f"/api/v1/speakers/{sp_id}", json={
        "name": "Jane Doe",
        "bio": "Updated bio"
    }, headers=auth_headers)
    assert r3.status_code == 200
    assert r3.json()["name"] == "Jane Doe"

    # delete speaker
    r4 = client.delete(f"/api/v1/speakers/{sp_id}", headers=auth_headers)
    assert r4.status_code == 204
