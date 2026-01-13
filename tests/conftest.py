"""
Pytest configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from main import app

# Test database URL (in-memory SQLite for faster tests)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_equipment_data():
    """Sample equipment data for testing."""
    return {
        "country": "ukraine",
        "type": "Tanks",
        "destroyed": 10,
        "abandoned": 2,
        "captured": 5,
        "damaged": 3,
        "total": 20,
        "date": "2023-01-01",
    }


@pytest.fixture
def sample_all_equipment_data():
    """Sample all equipment data for testing."""
    return {
        "country": "ukraine",
        "type": "Tanks",
        "destroyed": 100,
        "abandoned": 20,
        "captured": 50,
        "damaged": 30,
        "total": 200,
    }


@pytest.fixture
def sample_system_data():
    """Sample system data for testing."""
    return {
        "country": "ukraine",
        "origin": "USA",
        "system": "M1 Abrams",
        "status": "destroyed",
        "url": "https://example.com",
        "date": "2023-01-01",
    }


@pytest.fixture
def sample_all_system_data():
    """Sample all system data for testing."""
    return {
        "country": "ukraine",
        "system": "M1 Abrams",
        "destroyed": 5,
        "abandoned": 1,
        "captured": 2,
        "damaged": 1,
        "total": 9,
    }
