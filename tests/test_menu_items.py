def test_create_menu_item_success(client):
    """Test successful menu item creation"""
    menu_item_data = {
        "name": "Caesar Salad",
        "description": "Fresh romaine with caesar dressing",
        "price": 12.99,
        "calories": 280,
        "food_category": "vegetarian",
        "is_available": True
    }

    response = client.post("/menu_items/", json=menu_item_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Caesar Salad"
    assert data["price"] == 12.99
    assert data["food_category"] == "vegetarian"


def test_create_duplicate_menu_item(client, sample_menu_item):
    """Test creating menu item with duplicate name"""
    menu_item_data = {
        "name": "Grilled Chicken",  # Same as sample_menu_item
        "description": "Another chicken dish",
        "price": 14.99,
        "calories": 300,
        "food_category": "regular"
    }

    response = client.post("/menu_items/", json=menu_item_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_menu_items(client, sample_menu_item):
    """Test retrieving menu items"""
    response = client.get("/menu_items/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert any(item["name"] == "Grilled Chicken" for item in data)


def test_search_menu_items(client, sample_menu_item):
    """Test menu item search functionality"""
    response = client.get("/menu_items/search?search_term=Grilled&category=regular")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Grilled Chicken"


def test_get_nutrition_info(client, sample_menu_item):
    """Test nutrition info retrieval - TESTS THE BUG FIX"""
    response = client.get(f"/menu_items/{sample_menu_item.id}/nutrition")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "menu_item" in data
    assert "ingredients" in data
    assert data["menu_item"]["name"] == "Grilled Chicken"
    assert len(data["ingredients"]) >= 1


def test_toggle_availability(client, sample_menu_item):
    """Test menu item availability toggle"""
    response = client.patch(f"/menu_items/{sample_menu_item.id}/availability?available=false")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_available"] == False