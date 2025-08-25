
def test_me_endpoint(client, auth_headers, user_payload):
    r = client.get("/api/v1/users/me", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == user_payload["email"]

def test_me_unauthorized(client):
    r = client.get("/api/v1/users/me")
    assert r.status_code == 401
