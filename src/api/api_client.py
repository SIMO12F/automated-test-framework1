import requests
from src.config import Config
from src.logger import logger

class APIClient:
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AutomatedTestFramework/1.0",
            "Content-Type": "application/json"
        })

    def _send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making {method} request to {url}")
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            logger.info(f"Received response with status code: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error occurred: {err}")
            logger.error(f"Response content: {err.response.content}")
            raise
        except requests.exceptions.RequestException as err:
            logger.error(f"An error occurred while making the request: {err}")
            raise

    def get(self, endpoint, params=None):
        return self._send_request('GET', endpoint, params=params)

    def post(self, endpoint, data=None, json=None):
        return self._send_request('POST', endpoint, data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        return self._send_request('PUT', endpoint, data=data, json=json)

    def delete(self, endpoint):
        return self._send_request('DELETE', endpoint)