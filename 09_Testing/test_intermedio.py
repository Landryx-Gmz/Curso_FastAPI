from fastapi.testclient import TestClient
from intermedio import app

client = TestClient(app)

def test_get_user():
    response = client.get("/users/1", headers={"X-Token":"misupertoken"})
    assert response.status_code == 200
    assert response.json() == {
        "id":"1",
        "username":"Andy",
        "email": "andy@mail.com",
    }
def test_get_user_bad_token():
    response = client.get("/users/1", headers={"X-Token": "accesodenegado"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token"}

def test_get_not_existent_user():
    response = client.get("/users/4", headers={"X-Token": "misupertoken"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not foun"}

def test_create_user():
    response = client.post(
        "/users/",
        headers={"X-Token": "misupertoken"},
        json={"id": "4","username": "user4", "email": "user4@mail.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": "4","username": "user4", "email": "user@mail.com"}

def test_create_user_bad_token():
    response = client.post(
        "/users/",
        headers={"X-Token": "estanoeseltoken"},
        json={"id": "5","username": "user5", "email": "user5@mail.com"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token"}

def test_creat_existing_user():
    response = client.post(
        "/users/",
        headers={"X-Token": "misupertoken"},
        json={
        "id":"1",
        "username":"Andy",
        "email": "andy@mail.com"}
        )
    assert response.status_code == 409
    assert response.json() == {"detail": "User already exist "}