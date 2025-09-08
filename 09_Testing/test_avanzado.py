from fastapi.testclient import TestClient
import pytest
from avanzado import app, MockDatabase, get_db