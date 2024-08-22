import pytest
import requests
from src.api.api_client import APIClient
from src.utils.performance import measure_time, log_test_step, benchmark_api
from src.config import Config
@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@measure_time
@log_test_step("Testing GET /posts endpoint")
def test_get_all_posts(api_client):
    response = api_client.get("/posts")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    posts = response.json()
    assert len(posts) > 0, "No posts returned"

@measure_time
@log_test_step("Testing GET /posts/1 endpoint")
def test_get_single_post(api_client):
    response = api_client.get("/posts/1")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    post = response.json()
    assert post["id"] == 1, "Incorrect post returned"

@measure_time
@log_test_step("Testing POST /posts endpoint")
def test_create_post(api_client):
    new_post = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    response = api_client.post("/posts", json=new_post)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    created_post = response.json()
    assert created_post["title"] == new_post["title"], "Post title doesn't match"
    assert created_post["body"] == new_post["body"], "Post body doesn't match"
    assert created_post["userId"] == new_post["userId"], "Post userId doesn't match"

@measure_time
@log_test_step("Testing PUT /posts/1 endpoint")
def test_update_post(api_client):
    updated_post = {
        "id": 1,
        "title": "Updated Test Post",
        "body": "This post has been updated",
        "userId": 1
    }
    response = api_client.put("/posts/1", json=updated_post)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json() == updated_post, "Updated post doesn't match the sent data"

@measure_time
@log_test_step("Testing DELETE /posts/1 endpoint")
def test_delete_post(api_client):
    response = api_client.delete("/posts/1")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

@measure_time
@log_test_step("Testing GET /posts/{post_id} endpoint")
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_multiple_posts(api_client, post_id):
    response = api_client.get(f"/posts/{post_id}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json()["id"] == post_id, f"Incorrect post returned for id {post_id}"

@measure_time
@log_test_step("Testing invalid endpoint")
def test_invalid_endpoint(api_client):
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        api_client.get("/invalid_endpoint")
    assert excinfo.value.response.status_code == 404, f"Expected status code 404, but got {excinfo.value.response.status_code}"

@measure_time
@log_test_step("Testing API performance")
def test_api_performance(api_client):
    benchmark_api(api_client, "/posts")

@measure_time
@log_test_step("Testing non-existent post (designed to fail)")
def test_non_existent_post(api_client):
    try:
        response = api_client.get("/posts/9999")
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 404
    else:
        pytest.fail("Expected HTTPError was not raised")