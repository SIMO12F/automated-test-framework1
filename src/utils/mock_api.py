import requests_mock
from src.config import Config

def mock_api_response(method, endpoint, status_code, json_data):
    with requests_mock.Mocker() as m:
        m.register_uri(method, f"{Config.API_BASE_URL}{endpoint}", status_code=status_code, json=json_data)
        yield m

# Usage in tests:
# @pytest.fixture
# def mock_get_user():
#     user_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
#     yield from mock_api_response('GET', '/users/1', 200, user_data)