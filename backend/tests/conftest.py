import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture
def client():
    """Create a test client and clear storage before each test."""
    storage.clear()
    with TestClient(app) as test_client:
        yield test_client
