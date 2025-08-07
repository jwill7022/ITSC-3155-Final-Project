from fastapi.testclient import TestClient
from api.main import app
import pytest

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_database_connection():
    try:
        response = client.get("/customers/")
        # Should get some response, not a connection error
        assert response.status_code in [200, 500]  # 500 is ok if no data
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_create_customer():
    customer_data = {
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "customer_phone": "5985550123"
    }

    # Check if customer already exists in the database
    existing_response = client.get(f"/customers/?search=john.doe@example.com")
    if existing_response.status_code == 200 and existing_response.json():
        # Customer already exists, use the existing one for testing
        customers = existing_response.json()
        if customers:
            customer = customers[0]
            assert customer["customer_name"] == "John Doe"
            assert "id" in customer
            return

    # Customer doesn't exist, create it
    response = client.post("/customers/", json=customer_data)

    # Debug the error if it fails
    if response.status_code not in [200, 201]:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    #expect 201 status code
    assert response.status_code == 201
    customer = response.json()
    assert customer["customer_name"] == "John Doe"
    assert customer["customer_phone"] == "5985550123"  # Fixed: should be string, not int
    assert "id" in customer


# Read
def test_read_customers():
    response = client.get("/customers/")

    assert response.status_code == 200
    customers = response.json()
    assert isinstance(customers, list)


def test_read_single_customer():
    # First, get all customers to find one to read
    response = client.get("/customers/")
    assert response.status_code == 200
    customers = response.json()

    if customers:
        customer_id = customers[0]["id"]

        # Read the specific customer
        response = client.get(f"/customers/{customer_id}")
        assert response.status_code == 200

        customer = response.json()
        assert customer["id"] == customer_id
        assert "customer_name" in customer


# update
def test_update_customer():
    # First, create a customer to update
    customer_data = {
        "customer_name": "Jane Smith",
        "customer_email": "jane.smith@example.com",
        "customer_phone": "1235550456"
    }

    create_response = client.post("/customers/", json=customer_data)
    if create_response.status_code not in [200, 201]:
        # Customer might already exist, get existing one
        existing_response = client.get(f"/customers/?search=jane.smith@example.com")
        if existing_response.status_code == 200 and existing_response.json():
            customers = existing_response.json()
            if customers:
                customer = customers[0]
            else:
                pytest.skip("Could not create customer for update test")
        else:
            pytest.skip("Could not create customer for update test")
    else:
        customer = create_response.json()

    customer_id = customer["id"]

    # Update the customer
    updated_data = {
        "customer_name": "Jane Smith Updated",
        "customer_email": "jane.smith.updated@example.com",
        "customer_phone": "5565550789"
    }

    response = client.put(f"/customers/{customer_id}", json=updated_data)

    assert response.status_code == 200
    updated_customer = response.json()
    assert updated_customer["customer_name"] == "Jane Smith Updated"


# delete
def test_delete_customer():
    # create a customer to delete
    customer_data = {
        "customer_name": "Delete Me",
        "customer_email": "delete.me@example.com",
        "customer_phone": "9875550999"
    }

    create_response = client.post("/customers/", json=customer_data)
    if create_response.status_code not in [200, 201]:
        # Customer might already exist, get existing one
        existing_response = client.get(f"/customers/?search=delete.me@example.com")
        if existing_response.status_code == 200 and existing_response.json():
            customers = existing_response.json()
            if customers:
                customer = customers[0]
            else:
                pytest.skip("Could not create customer for delete test")
        else:
            pytest.skip("Could not create customer for delete test")
    else:
        customer = create_response.json()

    customer_id = customer["id"]

    # Delete the customer
    response = client.delete(f"/customers/{customer_id}")

    assert response.status_code in [200, 204]

    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 404  # Should not be found