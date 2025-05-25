import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def authenticated_client(client: TestClient, test_user_data):
    """Create authenticated client"""
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["data"]["access_token"]
    
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_get_current_user(authenticated_client: TestClient, test_user_data):
    """Test get current user info"""
    response = authenticated_client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["username"] == test_user_data["username"]
    assert data["data"]["email"] == test_user_data["email"]

def test_update_current_user(authenticated_client: TestClient):
    """Test update current user"""
    update_data = {
        "full_name": "Updated Name"
    }
    response = authenticated_client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["full_name"] == "Updated Name"

def test_get_user_unauthorized(client: TestClient):
    """Test get user without authentication"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401