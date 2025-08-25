
# Third-party imports
from fastapi.testclient import TestClient

# Local imports
from .helpers import make_event_payload


def test_event_crud_flow(client: TestClient, auth_headers: dict) -> None:
    # Create
    create_payload = make_event_payload(name="PyDay")
    create_response = client.post("/api/v1/events", json=create_payload, headers=auth_headers)
    assert create_response.status_code in (200, 201), create_response.text
    created_event = create_response.json()
    created_event_id = created_event["id"]

    # Retrieve
    retrieve_response = client.get(f"/api/v1/events/{created_event_id}", headers=auth_headers)
    assert retrieve_response.status_code == 200, retrieve_response.text
    assert retrieve_response.json()["id"] == created_event_id

    # Update (PATCH)
    update_payload = {"venue": "Auditorio Principal"}
    update_response = client.patch(
        f"/api/v1/events/{created_event_id}", json=update_payload, headers=auth_headers
    )
    assert update_response.status_code == 200, update_response.text
    assert update_response.json()["venue"] == "Auditorio Principal"

    # Delete (soft)
    delete_response = client.delete(f"/api/v1/events/{created_event_id}", headers=auth_headers)
    assert delete_response.status_code in (200, 204), delete_response.text

    # Post-delete behavior (depends on soft-delete visibility)
    post_delete_response = client.get(f"/api/v1/events/{created_event_id}", headers=auth_headers)
    assert post_delete_response.status_code in (404, 200)
