from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_resource():
    """Test creating a basic resource"""
    resource_data = {
        "item": "Bread",
        "amount": 100
    }

    response = client.post("/resources/", json=resource_data)

    # Debug the error if it fails
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == 200
    resource = response.json()
    assert resource["item"] == "Bread"
    assert resource["amount"] == 100
    assert "id" in resource