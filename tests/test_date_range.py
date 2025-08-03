from fastapi import status
from datetime import timedelta, date, datetime
from decimal import Decimal
from sqlalchemy import func
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

    # CRITICAL: Ensure test isolation by cleaning up first
    db_session.query(Order).filter(
        func.date(Order.order_date) == target_date
    ).delete(synchronize_session=False)
    db_session.commit()

    # Create test orders for today with EXPLICIT status setting
    order1 = Order(
        guest_name="Revenue Test 1",
        guest_phone="3333333333",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=9)),
        order_type=OrderType.DINE_IN,
        status=StatusType.COMPLETED,  # EXPLICIT
        total_amount=Decimal("45.00")
    )

    order2 = Order(
        guest_name="Revenue Test 2",
        guest_phone="4444444444",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=18)),
        order_type=OrderType.TAKEOUT,
        status=StatusType.COMPLETED,  # EXPLICIT
        total_amount=Decimal("32.50")
    )

    # Cancelled order (should NOT be included in revenue)
    order3 = Order(
        guest_name="Cancelled Order",
        guest_phone="5555555555",
        order_date=datetime.combine(target_date, datetime.min.time().replace(hour=12)),
        order_type=OrderType.DINE_IN,
        status=StatusType.CANCELLED,  # EXPLICIT
        total_amount=Decimal("20.00")
    )

    db_session.add_all([order1, order2, order3])
    db_session.commit()

    # Verify orders were created with correct status
    created_orders = db_session.query(Order).filter(
        func.date(Order.order_date) == target_date
    ).all()

    assert len(created_orders) == 3, f"Expected 3 orders, got {len(created_orders)}"

    completed_count = sum(1 for o in created_orders if o.status == StatusType.COMPLETED)
    assert completed_count == 2, f"Expected 2 completed orders, got {completed_count}"

    # Test the API endpoint
    response = client.get(f"/staff_actions/revenue/daily?target_date={target_date}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Debug output if assertion fails
    if data["total_revenue"] != 77.50:
        print(f"FAILURE DEBUG:")
        print(f"Expected revenue: 77.50")
        print(f"Actual revenue: {data['total_revenue']}")
        print(f"Order count: {data['order_count']}")

        for order in created_orders:
            print(f"Order: {order.guest_name}, Amount: {order.total_amount}, Status: {order.status.value}")

    # Should total $77.50 (45.00 + 32.50, excluding cancelled $20.00)
    assert data["total_revenue"] == 77.50, f"Expected 77.50, got {data['total_revenue']}"
    assert data["order_count"] == 2, f"Expected 2 orders, got {data['order_count']}"
    assert data["date"] == target_date.isoformat()