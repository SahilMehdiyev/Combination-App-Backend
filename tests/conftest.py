import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from combination_app.main import app
from combination_app.config.database import get_db, Base
from combination_app.config.settings import get_settings

# Test database
settings = get_settings()
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }

@pytest.fixture
def test_combination_data():
    return {
        "title": "Test Combination",
        "description": "Bu test combination-ıdır",
        "items": [
            {"name": "Item 1", "value": "Value 1"},
            {"name": "Item 2", "value": "Value 2"}
        ],
        "category": "test",
        "tags": ["test", "example"]
    }