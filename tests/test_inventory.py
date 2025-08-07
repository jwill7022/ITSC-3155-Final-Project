from fastapi import status

from api.models.resources import Resource


def test_inventory_check(client, sample_menu_item, sample_resource):
    """Test inventory availability check"""
    order_items = [
        {"menu_item_id": sample_menu_item.id, "quantity": 2}
    ]

    response = client.post("/staff_actions/inventory/check-availability", json=order_items)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "all_available" in data
    assert "details" in data


def test_low_stock_items(client, db_session):
    """Test low stock items retrieval"""
    # Create low stock resource
    low_stock_resource = Resource(
        item="Low Stock Item",
        amount=5  # Below default threshold of 10
    )
    db_session.add(low_stock_resource)
    db_session.commit()

    response = client.get("/staff_actions/inventory/low-stock?threshold=10")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert isinstance(data, list)
    low_stock_items = [item["item"] for item in data]
    assert "Low Stock Item" in low_stock_items
