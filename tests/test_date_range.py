from datetime import timedelta, date, datetime
from decimal import Decimal

from fastapi import status

from api.models.orders import Order, OrderType, StatusType


def test_get_orders_by_date_range_success(client, db_session, sample_menu_item):
    """Test date range query"""
    # Create test orders with specific dates
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Create order for yesterday
    order1 = Order(
        guest_name="Test Customer 1",
        guest_phone="1111111111",
        order_date=datetime.combine(yesterday, datetime.min.time().replace(hour=10)),
        order_type=OrderType.DINE_IN,
        status=StatusType.COMPLETED,
        total_amount=Decimal("25.99")
    )

    # Create order for today
    order2 = Order(
        guest_name="Test Customer 2",
        guest_phone="2222222222",
        order_date=datetime.combine(today, datetime.min.time().replace(hour=14)),
        order_type=OrderType.TAKEOUT,
        status=StatusType.PENDING,
        total_amount=Decimal("18.50")
    )

    db_session.add_all([order1, order2])
    db_session.commit()

    # Test date range query
    response = client.get(f"/orders/date-range?start_date={yesterday}&end_date={today}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Should return both orders
    assert len(data) == 2

    # Verify order details
    order_names = [order["customer_name"] for order in data]
    assert "Test Customer 1" in order_names
    assert "Test Customer 2" in order_names


def test_date_range_validation(client):
    """Test date range validation"""
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Test invalid range (start > end)
    response = client.get(f"/orders/date-range?start_date={tomorrow}&end_date={today}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Start date must be before" in response.json()["detail"]


def test_daily_revenue_calculation(client, db_session):
    """Test daily revenue calculation - TESTS THE BUG FIX"""
    target_date = date.today()

    # Create test orders for today
    order1 = Order(
        guest_name="Revenue Test 1",
        guest_phone="3333333333",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=9)),
        status=StatusType.COMPLETED,
        total_amount=Decimal("45.00")
    )

    order2 = Order(
        guest_name="Revenue Test 2",
        guest_phone="4444444444",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=18)),
        status=StatusType.COMPLETED,
        total_amount=Decimal("32.50")
    )

    # Cancelled order (should not be included)
    order3 = Order(
        guest_name="Cancelled Order",
        guest_phone="5555555555",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=12)),
        status=StatusType.CANCELLED,
        total_amount=Decimal("20.00")
    )

    db_session.add_all([order1, order2, order3])
    db_session.commit()

    # Test daily revenue
    response = client.get(f"/staff_actions/revenue/daily?target_date={target_date}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Should total $77.50 (45.00 + 32.50, excluding cancelled)
    assert data["total_revenue"] == 77.50
    assert data["order_count"] == 2
    assert data["date"] == target_date.isoformat()