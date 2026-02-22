"""Pytest configuration and fixtures."""
import os
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Import all models to ensure they are registered
from app.models.product import Producto
from app.models.venta import Venta
from app.core.db import Base, get_db
from app.main import app
from app.services.auth_service import create_user, create_token_for_user
from app.schemas.user import UserCreate

# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def test_db(test_engine):
    """Create test database session factory."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return TestingSessionLocal

@pytest.fixture
def db_session(test_db):
    """Provide a test database session."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(test_engine):
    """Provide test client with override dependency."""
    def override_get_db():
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Ensure fresh schema for each test to avoid state leakage
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        # Create a default test user and attach Authorization header
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        db = TestingSessionLocal()
        try:
            user_in = UserCreate(email="test@example.com", password="testpass", business_id="testbiz")
            user = create_user(db, user_in)
            token = create_token_for_user(user)
            test_client.headers.update({"Authorization": f"Bearer {token}"})
        finally:
            db.close()
        yield test_client

    app.dependency_overrides.clear()


