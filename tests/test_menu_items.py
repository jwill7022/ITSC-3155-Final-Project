from fastapi import status

def test_create_menu_item_success(client):
    """Test successful menu item creation"""
    menu_item_data = {
        "name": "Caesar Salad",
        "description": "Fresh romaine with caesar dressing",
        "price": "12.99",
        "calories": 280,
        "food_category": "vegetarian",
        "is_available": True
    }

    response = client.post("/menu_items/", json=menu_item_data)

    # Debug output if test fails
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Caesar Salad"
    assert float(data["price"]) == 12.99
    assert data["food_category"] == "vegetarian"


def test_create_duplicate_menu_item(client, sample_menu_item):
    """Test creating menu item with duplicate name"""
    menu_item_data = {
        "name": "Grilled Chicken",  # Same as sample_menu_item
        "description": "Another chicken dish",
        "price": "14.99",
        "calories": 300,
        "food_category": "regular"
    }

    response = client.post("/menu_items/", json=menu_item_data)

    # Debug output
    if response.status_code not in [400, 409]:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    # Should be either 400 or 409 for duplicate/conflict
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]
