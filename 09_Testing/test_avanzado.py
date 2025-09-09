from fastapi.testclient import TestClient
import pytest
from avanzado import app, MockDatabase, get_db

client = TestClient(app)

# Fixtures (Forma limpia estructurada de repetir codigo o utilizar los valores ejmeplo: BD codigos, http, Item etc)
@pytest.fixture
def test_db():
    return MockDatabase

@pytest.fixture 
def client_with_db(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def sample_item():
    return{
        "id" : "test1",
        "name" : "Test Item",
        "price" : 12.99
    }
def test_create_and_read_item(client_with_db, sample_item):
    client = client_with_db
    response = client.post("/items/", json=sample_item)
    assert response.status_code==200

    response = client.get(f"/items/{sample_item['id']}")
    assert response.status_code == 200
    assert response.json() == sample_item

