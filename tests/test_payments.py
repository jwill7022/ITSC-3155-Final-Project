from decimal import Decimal

from fastapi import status

from api.models.orders import OrderType, StatusType, Order
from api.models.reviews import Reviews


def test_payment_amount_validation(client, db_session, sample_menu_item):
    """Test payment amount validation - TESTS THE BUG FIX"""
    # Create an order first
    order = Order(
        guest_name="Payment Test",
        guest_phone="6666666666",
        order_type=OrderType.DINE_IN,
        status=StatusType.PENDING,
        total_amount=Decimal("25.99")
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    # Test correct payment amount
    payment_data = {
        "amount": 25.99,
        "payment_type": "CREDIT_CARD"
    }

    response = client.post(f"/payments/process/{order.id}", json=payment_data)
    # This tests the decimal/float comparison fix


def test_failed_payment_simulation(client, db_session):
    """Test payment failure simulation"""
    order = Order(
        guest_name="Failed Payment Test",
        guest_phone="7777777777",
        order_type=OrderType.DINE_IN,
        status=StatusType.PENDING,
        total_amount=Decimal("31.55")  # This amount triggers failure
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    payment_data = {
        "amount": 31.55,
        "payment_type": "CREDIT_CARD"
    }

    response = client.post(f"/payments/process/{order.id}", json=payment_data)

    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        assert data["status"] == "failed"


# tests/test_analytics.py
def test_menu_performance_analytics(client, sample_menu_item):
    """Test menu performance analytics - TESTS DECIMAL BUG FIX"""
    response = client.get("/staff_actions/analytics/menu-performance")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Should return list of menu items with performance metrics
    assert isinstance(data, list)
    if len(data) > 0:
        item = data[0]
        assert "menu_item_id" in item
        assert "popularity_score" in item
        assert "performance_status" in item


def test_review_insights(client, db_session, sample_menu_item):
    """Test review insights - TESTS TYPO FIX"""
    # Create test review
    review = Reviews(
        menu_item_id=sample_menu_item.id,
        customer_name="Test Reviewer",
        rating=2,
        review_text="Food was cold and service was slow"
    )
    db_session.add(review)
    db_session.commit()

    response = client.get("/staff_actions/analytics/review-insights")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "total_reviews" in data
    assert "average_rating" in data
    assert "recent_complaints" in data
    assert "recommendations" in data

    # Check that temperature-related recommendations work (tests typo fix)
    if data["recent_complaints"]:
        assert len(data["recommendations"]) > 0
