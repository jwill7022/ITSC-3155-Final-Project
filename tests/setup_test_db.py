#!/usr/bin/env python3

# sets up the test database for GitHub Actions
import os
import sys
from sqlalchemy import create_engine
from urllib.parse import quote_plus

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from api.dependencies.database import Base
from api.dependencies.config import conf

def setup_test_database():
    # create tables
    try:
        DATABASE_URL = f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
        
        print(f"Connecting to database: {conf.db_host}:{conf.db_port}/{conf.db_name}")
        engine = create_engine(DATABASE_URL)
        
        print("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("Test database setup complete!")
        return True
        
    except Exception as e:
        print(f"Error setting up test database: {e}")
        return False

if __name__ == "__main__":
    success = setup_test_database()
    sys.exit(0 if success else 1)