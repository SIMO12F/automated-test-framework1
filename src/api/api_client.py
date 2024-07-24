import requests
from src.config import Config
from src.logger import logger

class APIClient:
    def __init__(self):
        self.base_url = Config.API_BASE_URL

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making GET request to {url}")
        response = requests.get(url, params=params)
        logger.info(f"Received response with status code: {response.status_code}")
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making POST request to {url}")
        response = requests.post(url, data=data, json=json)
        logger.info(f"Received response with status code: {response.status_code}")
        return response

    # Add more methods for other HTTP verbs as needed