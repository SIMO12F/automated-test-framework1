import requests
from src import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.API_BASE_URL

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response

    def post(self, endpoint, json=None):
        response = requests.post(f"{self.base_url}{endpoint}", json=json)
        response.raise_for_status()
        return response

    def put(self, endpoint, json=None):
        response = requests.put(f"{self.base_url}{endpoint}", json=json)
        response.raise_for_status()
        return response

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response