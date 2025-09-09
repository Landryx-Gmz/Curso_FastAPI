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