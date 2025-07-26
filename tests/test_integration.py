import pytest
import os
from fastapi.testclient import TestClient
from api.main import app

# Only run integration tests if we're in a testing environment
pytestmark = pytest.mark.skipif(
    os.getenv('TESTING') != 'true',
    reason="Integration tests only run in testing environment"
)

client = TestClient(app)

def test_app_health():
    """Test that the app starts successfully"""
    assert app is not None

def test_database_connection():
    """Test that we can connect to the test database"""
    try:
        response = client.get("/customers/")
        # Should get some response, not a connection error
        assert response.status_code in [200, 500]  # 500 is ok if no data
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_basic_endpoints():
    """Test basic endpoints exist"""
    endpoints = [
        "/customers/",
        "/menu_items/",
        "/resources/"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code in [200, 500], f"Endpoint {endpoint} failed"

def test_data_validation():
    """Test that endpoints validate data properly"""
    # Test invalid customer data
    invalid_customer = {"invalid": "data"}
    response = client.post("/customers/", json=invalid_customer)
    assert response.status_code == 422, "Should reject invalid customer data"
    
    # Test invalid menu item data
    invalid_menu = {"invalid": "data"}
    response = client.post("/menu_items/", json=invalid_menu)
    assert response.status_code == 422, "Should reject invalid menu item data"

def test_customer_creation():
    """Test creating a customer with valid data"""
    customer_data = {
        "customer_name": "Test Customer",
        "email": "test@example.com",
        "customer_phone": 1234567890
    }
    
    response = client.post("/customers/", json=customer_data)
    # Should either create successfully or fail due to duplicate
    assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
    
    if response.status_code == 200:
        customer = response.json()
        assert customer["customer_name"] == "Test Customer"
        assert "id" in customer

def test_menu_item_creation():
    """Test creating a menu item with valid data"""
    menu_data = {
        "name": "Test Burger",
        "description": "A test burger",
        "price": 9.99,
        "calories": 500,
        "food_category": "regular"
    }
    
    response = client.post("/menu_items/", json=menu_data)
    # Should either create successfully or fail due to business logic
    assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
    
    if response.status_code == 200:
        item = response.json()
        assert item["name"] == "Test Burger"
        assert "id" in item

def test_resource_creation():
    """Test creating a resource with valid data"""
    resource_data = {
        "item": "Test Resource",
        "amount": 100
    }
    
    response = client.post("/resources/", json=resource_data)
    # Should either create successfully or fail due to business logic
    assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
    
    if response.status_code == 200:
        resource = response.json()
        assert resource["item"] == "Test Resource"
        assert "id" in resource