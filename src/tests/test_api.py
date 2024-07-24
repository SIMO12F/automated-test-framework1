import pytest
from src.api.api_client import APIClient
from src.utils.performance import measure_time

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@measure_time
def test_get_users(api_client):
    response = api_client.get("users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert "id" in users[0]
    assert "name" in users[0]

@measure_time
def test_create_user(api_client):
    new_user = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    response = api_client.post("users", json=new_user)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == new_user["name"]
    assert created_user["email"] == new_user["email"]

@measure_time
def test_update_user(api_client):
    user_id = 1  # Assume this user exists
    updated_data = {"name": "Jane Doe"}
    response = api_client.put(f"users/{user_id}", json=updated_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == updated_data["name"]

@measure_time
def test_delete_user(api_client):
    user_id = 2  # Assume this user exists
    response = api_client.delete(f"users/{user_id}")
    assert response.status_code == 204