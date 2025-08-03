import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime, date, timedelta
from decimal import Decimal

from api.main import app
from api.dependencies.database import get_db, Base
from api.models.customers import Customer
from api.models.menu_items import MenuItem, FoodCategory
from api.models.orders import Order, OrderType, StatusType
from api.models.order_details import OrderDetail
from api.models.resources import Resource
from api.models.menu_item_ingredients import MenuItemIngredient
from api.models.payments import Payment, PaymentType, PaymentStatus
from api.models.promotions import Promotion
from api.models.reviews import Reviews

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with database dependency override"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_customer(db_session):
    """Create a sample customer for testing"""
    customer = Customer(
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="1234567890",
        customer_address="123 Main St"
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def sample_resource(db_session):
    """Create a sample resource for testing"""
    resource = Resource(
        item="Chicken Breast",
        amount=100
    )
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource


@pytest.fixture
def sample_menu_item(db_session, sample_resource):
    """Create a sample menu item for testing"""
    menu_item = MenuItem(
        name="Grilled Chicken",
        description="Delicious grilled chicken breast",
        price=Decimal("15.99"),
        calories=350,
        food_category=FoodCategory.REGULAR,  # Use enum directly
        is_available=True
    )
    db_session.add(menu_item)
    db_session.commit()
    db_session.refresh(menu_item)

    # Add ingredient relationship
    ingredient = MenuItemIngredient(
        menu_item_id=menu_item.id,
        resource_id=sample_resource.id,
        amount=1
    )
    db_session.add(ingredient)
    db_session.commit()

    return menu_item


@pytest.fixture
def sample_promotion(db_session):
    """Create a sample promotion for testing"""
    promotion = Promotion(
        code="SAVE10",
        description="10% off your order",
        discount_percent=10,
        expiration_date=datetime.now() + timedelta(days=30)
    )
    db_session.add(promotion)
    db_session.commit()
    db_session.refresh(promotion)
    return promotion