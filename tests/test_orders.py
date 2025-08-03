def test_create_guest_order_success(client, sample_menu_item):
    """Test successful guest order creation - TESTS THE BUG FIXES"""
    guest_info = {
        "guest_name": "Guest Customer",
        "guest_phone": "5555555555",
        "guest_email": "guest@example.com",
        "order_type": "dine_in"
    }

    order_items = [
        {"menu_item_id": sample_menu_item.id, "quantity": 2}
    ]

    response = client.post("/orders/guest", json=guest_info, params={"order_items": order_items})

def test_create_guest_order_via_customer_actions(client, sample_menu_item):
    """Test guest order via customer actions endpoint"""
    guest_data = {
        "guest_name": "Guest Customer",
        "guest_phone": "5555555555",
        "guest_email": "guest@example.com",
        "order_type": "dine_in"
    }

    order_items = [
        {"menu_item_id": sample_menu_item.id, "quantity": 2}
    ]

    response = client.post("/customer_actions/orders/guest",
                            json={"guest_info": guest_data, "order_items": order_items})

