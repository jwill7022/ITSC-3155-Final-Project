import pytest
from fastapi import status


def test_create_customer_success(client):
    """Test successful customer creation"""
    customer_data = {
        "customer_name": "Jane Smith",
        "customer_email": "jane@example.com",
        "customer_phone": "9876543210",
        "customer_address": "456 Oak Ave"
    }

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_name"] == "Jane Smith"
    assert data["customer_email"] == "jane@example.com"
    assert data["customer_phone"] == "9876543210"
    assert "id" in data


def test_create_customer_invalid_phone(client):
    """Test customer creation with invalid phone number"""
    customer_data = {
        "customer_name": "Invalid Phone",
        "customer_email": "invalid@example.com",
        "customer_phone": "123",  # Too short
        "customer_address": "123 Street"
    }

    response = client.post("/customers/", json=customer_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_customers(client, sample_customer):
    """Test retrieving customers"""
    response = client.get("/customers/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert any(customer["customer_name"] == "John Doe" for customer in data)


def test_get_customer_by_id(client, sample_customer):
    """Test retrieving specific customer"""
    response = client.get(f"/customers/{sample_customer.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["id"] == sample_customer.id


def test_get_customer_not_found(client):
    """Test retrieving non-existent customer"""
    response = client.get("/customers/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_customers(client, sample_customer):
    """Test customer search functionality"""
    response = client.get("/customers/?search=John")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert data[0]["customer_name"] == "John Doe"