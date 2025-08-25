
# Third-party imports
from fastapi.testclient import TestClient


def test_speakers_crud(client: TestClient, auth_headers: dict) -> None:
    # Create
    create_response = client.post(
        "/api/v1/speakers",
        json={"full_name": "Grace Hopper", "bio": "Pioneer"},
        headers=auth_headers,
    )
    assert create_response.status_code in (200, 201), create_response.text
    created_speaker = create_response.json()
    speaker_id = created_speaker["id"]

    # List
    list_response = client.get("/api/v1/speakers", headers=auth_headers)
    assert list_response.status_code == 200, list_response.text
    speakers_page = list_response.json()
    assert any(single_speaker["id"] == speaker_id for single_speaker in speakers_page["items"])

    # Update
    update_response = client.patch(
        f"/api/v1/speakers/{speaker_id}", json={"bio": "COBOL legend"}, headers=auth_headers
    )
    assert update_response.status_code == 200, update_response.text
    assert update_response.json()["bio"] == "COBOL legend"

    # Delete
    delete_response = client.delete(f"/api/v1/speakers/{speaker_id}", headers=auth_headers)
    assert delete_response.status_code in (200, 204), delete_response.text
