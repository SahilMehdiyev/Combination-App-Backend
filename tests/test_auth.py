import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["username"] == test_user_data["username"]
    assert data["data"]["user"]["email"] == test_user_data["email"]

def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test duplicate user registration"""
    client.post("/api/v1/auth/register", json=test_user_data)
    
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400

def test_login_user(client: TestClient, test_user_data):
    """Test user login"""
    client.post("/api/v1/auth/register", json=test_user_data)
    
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"

def test_login_invalid_user(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401