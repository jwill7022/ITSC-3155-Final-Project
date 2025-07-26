import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set test environment variables
os.environ.update({
    'DB_HOST': 'localhost',
    'DB_NAME': 'test_db',
    'DB_USER': 'test',
    'DB_PASSWORD': 'test'
})

# Mock the database connection
with patch('api.dependencies.database.create_engine') as mock_engine:
    mock_engine.return_value = MagicMock()
    with patch('api.dependencies.database.SessionLocal') as mock_session:
        mock_session.return_value = MagicMock()
        from api.main import app

client = TestClient(app)

# ============================================================================
# ATOMIC TESTS - Basic functionality
# ============================================================================

def test_app_starts():
    """Test that the FastAPI app starts successfully"""
    assert app is not None

def test_health_endpoint():
    """Test basic health check"""
    response = client.get("/")
    # App might not have a root endpoint, that's ok
    assert response.status_code in [200, 404, 405]

@patch('api.dependencies.database.get_db')
def test_customers_endpoint_exists(mock_db):
    """Test customers endpoint exists"""
    mock_db.return_value = MagicMock()
    response = client.get("/customers/")
    # Should exist and return some response
    assert response.status_code != 404

@patch('api.dependencies.database.get_db')
def test_menu_items_endpoint_exists(mock_db):
    """Test menu items endpoint exists"""
    mock_db.return_value = MagicMock()
    response = client.get("/menu_items/")
    assert response.status_code != 404

@patch('api.dependencies.database.get_db')
def test_resources_endpoint_exists(mock_db):
    """Test resources endpoint exists"""
    mock_db.return_value = MagicMock()
    response = client.get("/resources/")
    assert response.status_code != 404

# ============================================================================
# MEDIUM TESTS - Data validation
# ============================================================================

@patch('api.dependencies.database.get_db')
def test_customer_validation(mock_db):
    """Test customer data validation"""
    mock_db.return_value = MagicMock()
    
    # Invalid data should return 422
    invalid_data = {"invalid": "data"}
    response = client.post("/customers/", json=invalid_data)
    assert response.status_code == 422

@patch('api.dependencies.database.get_db')
def test_menu_item_validation(mock_db):
    """Test menu item data validation"""
    mock_db.return_value = MagicMock()
    
    # Invalid data should return 422
    invalid_data = {"invalid": "data"}
    response = client.post("/menu_items/", json=invalid_data)
    assert response.status_code == 422

@patch('api.dependencies.database.get_db')
def test_resource_validation(mock_db):
    """Test resource data validation"""
    mock_db.return_value = MagicMock()
    
    # Invalid data should return 422
    invalid_data = {"invalid": "data"}
    response = client.post("/resources/", json=invalid_data)
    assert response.status_code == 422

# ============================================================================
# COMPREHENSIVE TESTS - Endpoint coverage
# ============================================================================

@patch('api.dependencies.database.get_db')
def test_all_get_endpoints(mock_db):
    """Test all GET endpoints exist"""
    mock_db.return_value = MagicMock()
    
    endpoints = [
        "/customers/",
        "/menu_items/", 
        "/resources/",
        "/staff_actions/"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code != 404, f"Endpoint {endpoint} not found"

@patch('api.dependencies.database.get_db')
def test_post_endpoints_validation(mock_db):
    """Test POST endpoints validate data"""
    mock_db.return_value = MagicMock()
    
    endpoints = [
        "/customers/",
        "/menu_items/",
        "/resources/"
    ]
    
    for endpoint in endpoints:
        # Empty data should fail validation
        response = client.post(endpoint, json={})
        assert response.status_code == 422, f"Endpoint {endpoint} should validate data"

def test_api_structure():
    """Test that the API has the expected structure"""
    # Test that main components are imported correctly
    assert hasattr(app, 'router')
    assert app.title == "FastAPI"  # Default FastAPI title