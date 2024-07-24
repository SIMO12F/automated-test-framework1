import pytest
from src.api.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

def test_get_python_events(api_client):
    response = api_client.get("events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) > 0
    assert "title" in events[0]

def test_search_python_events(api_client):
    params = {"q": "pycon"}
    response = api_client.get("events/search", params=params)
    assert response.status_code == 200
    search_results = response.json()
    assert len(search_results) > 0
    assert any("pycon" in event["title"].lower() for event in search_results)

# Add more API tests as needed