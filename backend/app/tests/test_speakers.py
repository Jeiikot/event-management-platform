# Third-party imports
from fastapi.testclient import TestClient


def test_speaker_crud(client: TestClient, auth_headers: dict) -> None:
    # Create
    create_payload = {"full_name": "John Doe", "bio": "Expert in Python"}
    create_resp = client.post("/api/v1/speakers", json=create_payload, headers=auth_headers)
    assert create_resp.status_code in (200, 201), create_resp.text
    created = create_resp.json()
    assert "id" in created, f"Unexpected create payload: {created}"
    speaker_id = created["id"]

    # List (tolerate page object or plain list)
    list_resp = client.get("/api/v1/speakers", headers=auth_headers)
    assert list_resp.status_code == 200, list_resp.text
    data = list_resp.json()
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    assert any(s.get("id") == speaker_id for s in items), f"Speaker {speaker_id} not in list: {items}"

    # Update (PATCH, and field is full_name)
    update_payload = {"full_name": "Jane Doe", "bio": "Updated bio"}
    patch_resp = client.patch(f"/api/v1/speakers/{speaker_id}", json=update_payload, headers=auth_headers)
    assert patch_resp.status_code == 200, patch_resp.text
    updated = patch_resp.json()
    assert updated.get("full_name") == "Jane Doe", f"Unexpected update payload: {updated}"
    assert updated.get("bio") == "Updated bio"

    # Delete (allow 200 or 204)
    del_resp = client.delete(f"/api/v1/speakers/{speaker_id}", headers=auth_headers)
    assert del_resp.status_code in (200, 204), del_resp.text
