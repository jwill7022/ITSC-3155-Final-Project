import pytest
from fastapi import status


def test_foreign_key_constraint_error(client, db_session):
    """Test foreign key constraint error handling"""
    # Try to create order detail with non-existent menu item
    order_detail_data = {
        "order_id": 1,
        "menu_item_id": 99999,  # Non-existent
        "amount": 2
    }

    response = client.post("/orderdetails/", json=order_detail_data)
    # Should handle the constraint error gracefully


def test_duplicate_resource_creation(client, sample_resource):
    """Test duplicate resource creation error handling"""
    duplicate_resource = {
        "item": "Chicken Breast",  # Same as sample_resource
        "amount": 50
    }

    response = client.post("/resources/", json=duplicate_resource)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])