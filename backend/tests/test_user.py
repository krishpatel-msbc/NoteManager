import pytest

def test_create_user(client):
    response = client.post("/users/", json={"username": "user1", "email": "user1@example.com", "password": "securepass"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert data["username"] == "user1"

def test_get_user(client, auth_header):
    res = client.post("/users/", json={"username": "user2", "email": "user2@example.com", "password": "securepass"})
    user_id = res.json()["id"]
    # Login as user2 to get correct token
    login_res = client.post("/login", data={"username": "user2@example.com", "password": "securepass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user2@example.com"
