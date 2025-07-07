import pytest

def test_create_note(client, auth_header):
    response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"}, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test content"

def test_read_notes(client, auth_header):
    client.post("/notes/", json={"title": "Read Note", "content": "Read content"}, headers=auth_header)
    response = client.get("/notes/", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(note["title"] == "Read Note" for note in data)

def test_update_note(client, auth_header):
    res = client.post("/notes/", json={"title": "Old Title", "content": "Old content"}, headers=auth_header)
    note_id = res.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"title": "New Title", "content": "New content"}, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New content"

def test_delete_note(client, auth_header):
    res = client.post("/notes/", json={"title": "Delete Me", "content": "Delete content"}, headers=auth_header)
    note_id = res.json()["id"]
    response = client.delete(f"/notes/{note_id}", headers=auth_header)
    assert response.status_code == 204
    get_res = client.get(f"/notes/{note_id}", headers=auth_header)
    assert get_res.status_code == 404
