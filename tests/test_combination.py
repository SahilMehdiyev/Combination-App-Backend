import pytest
from fastapi.testclient import TestClient

def test_create_combination(authenticated_client: TestClient, test_combination_data):
    """Test create combination"""
    response = authenticated_client.post("/api/v1/combinations/", json=test_combination_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == test_combination_data["title"]
    assert data["data"]["items"] == test_combination_data["items"]

def test_get_combinations(authenticated_client: TestClient, test_combination_data):
    """Test get combinations"""
    authenticated_client.post("/api/v1/combinations/", json=test_combination_data)
    
    response = authenticated_client.get("/api/v1/combinations/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["combinations"]) > 0

def test_get_my_combinations(authenticated_client: TestClient, test_combination_data):
    """Test get my combinations"""
    authenticated_client.post("/api/v1/combinations/", json=test_combination_data)
    
    response = authenticated_client.get("/api/v1/combinations/my")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["combinations"]) > 0

def test_update_combination(authenticated_client: TestClient, test_combination_data):
    """Test update combination"""
    create_response = authenticated_client.post("/api/v1/combinations/", json=test_combination_data)
    combination_id = create_response.json()["data"]["id"]
    
    update_data = {"title": "Updated Title"}
    response = authenticated_client.put(f"/api/v1/combinations/{combination_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Updated Title"

def test_delete_combination(authenticated_client: TestClient, test_combination_data):
    """Test delete combination"""
    create_response = authenticated_client.post("/api/v1/combinations/", json=test_combination_data)
    combination_id = create_response.json()["data"]["id"]
    
    response = authenticated_client.delete(f"/api/v1/combinations/{combination_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_create_combination_unauthorized(client: TestClient, test_combination_data):
    """Test create combination without authentication"""
    response = client.post("/api/v1/combinations/", json=test_combination_data)
    assert response.status_code == 401