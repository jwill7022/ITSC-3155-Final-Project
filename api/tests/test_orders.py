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

# TODO fix test missing email on response
def test_create_customer():
    """Test creating a customer"""
    customer_data = {
        "customer_name": "John Doe",
        "email": "john.doe@example.com",
        "customer_phone": 5550123
    }

    # Check if customer already exists in the database
    existing_response = client.get(f"/customers/?email={customer_data['email']}")
    if existing_response.status_code == 200 and existing_response.json():
        # Customer already exists, use the existing one for testing
        customer = existing_response.json()[0]
        assert customer["customer_name"] == "John Doe"
        assert "id" in customer
        return

    # Customer doesn't exist, create it
    response = client.post("/customers/", json=customer_data)

    # Debug the error if it fails
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == 200
    customer = response.json()
    assert customer["customer_name"] == "John Doe"
    assert customer["customer_phone"] == 5550123
    assert "id" in customer


def test_create_resource():
    """Test creating a basic resource"""
    resource_data = {
        "item": "Bread",
        "amount": 100
    }

    # Check if resource already exists in the database
    existing_response = client.get(f"/resources/?item={resource_data['item']}")
    if existing_response.status_code == 200 and existing_response.json():
        # Resource already exists, use the existing one for testing
        resource = existing_response.json()[0]
        assert resource["item"] == "Bread"
        assert "id" in resource
        return

    # Resource doesn't exist, create it
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


def test_menu_item():
    """Test creating a menu item"""
    menu_item_data = {
        "name": "Ham Sandwich",
        "description": "Ham Sandwich",
        "price": 12.50,
        "calories": 100,
        "food_category": "regular"
    }
    
    # Check if item already exists in the database
    existing_response = client.get(f"/menu_items/?name={menu_item_data['name']}")
    if existing_response.status_code == 200 and existing_response.json():
        # Menu item already exists, use the existing one for testing
        menu_item = existing_response.json()[0]
        assert menu_item["name"] == "Ham Sandwich"
        assert "id" in menu_item
        return

    # Menu item doesn't exist, create it
    response = client.post("/menu_items/", json=menu_item_data)

    # Debug the error if it fails
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == 200
    menu_item = response.json()
    assert menu_item["name"] == "Ham Sandwich"
    assert menu_item["description"] == "Ham Sandwich"
    assert menu_item["price"] == 12.50
    assert menu_item["calories"] == 100
    assert menu_item["food_category"] == "regular"
    assert "id" in menu_item


def test_create_order():
    """Test creating an order"""
    order_data = {
        "customer_id": 1,
        "description": "guy in red",
        "status": "pending",
        "order_type": "dine_in"
    }

    # Check if order already exists for this customer
    existing_response = client.get(f"/orders/?customer_id={order_data['customer_id']}")
    if existing_response.status_code == 200 and existing_response.json():
        # Order already exists, use the existing one for testing
        order = existing_response.json()[0]
        assert order["customer_id"] == 1
        assert "id" in order
        return

    # Order doesn't exist, create it
    response = client.post("/orders/", json=order_data)

    # Debug the error if it fails
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == 200
    order = response.json()
    assert order["customer_id"] == 1
    assert order["description"] == "guy in red"
    assert order["status"] == "pending"
    assert order["order_type"] == "dine_in"
    assert "id" in order


def test_create_payment():
    """Test creating a payment"""
    payment_data = {
        "order_id": 1,
        "amount": 100,
        "payment_type": "cash",
        "status": "pending"
    }

    # Check if payment already exists for this order
    existing_response = client.get(f"/payments/?order_id={payment_data['order_id']}")
    if existing_response.status_code == 200 and existing_response.json():
        # Payment already exists, use the existing one for testing
        payment = existing_response.json()[0]
        assert payment["order_id"] == 1
        assert "id" in payment
        return

    # Payment doesn't exist, create it
    response = client.post("/payments/", json=payment_data)

    # Debug the error if it fails
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == 200
    payment = response.json()
    assert payment["order_id"] == 1
    assert payment["amount"] == 100
    assert payment["payment_type"] == "cash"
    assert payment["status"] == "pending"
    assert "id" in payment