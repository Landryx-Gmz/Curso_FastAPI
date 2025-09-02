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
