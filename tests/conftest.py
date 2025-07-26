import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.dependencies.database import Base
from api.main import app
from fastapi.testclient import TestClient

# Set test environment variables
os.environ.update({
    'DB_HOST': os.getenv('DB_HOST', 'localhost'),
    'DB_NAME': os.getenv('DB_NAME', 'test_restaurant_db'),
    'DB_USER': os.getenv('DB_USER', 'test_user'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD', 'test_password'),
    'DB_PORT': os.getenv('DB_PORT', '3306'),
    'TESTING': 'true'
})

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine"""
    from api.dependencies.config import conf
    from urllib.parse import quote_plus
    
    DATABASE_URL = f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
    
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def test_session(test_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)