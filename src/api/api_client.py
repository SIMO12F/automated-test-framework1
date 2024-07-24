import requests
from src.config import Config
from src.logger import logger

class APIClient:
    def __init__(self):
        self.base_url = Config.get_api_base_url()
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

    def patch(self, endpoint, data=None, json=None):
        return self._send_request('PATCH', endpoint, data=data, json=json)

    def head(self, endpoint):
        return self._send_request('HEAD', endpoint)

    def options(self, endpoint):
        return self._send_request('OPTIONS', endpoint)

    def get_json(self, endpoint, params=None):
        response = self.get(endpoint, params)
        return response.json()

    def post_json(self, endpoint, data=None):
        response = self.post(endpoint, json=data)
        return response.json()

    def put_json(self, endpoint, data=None):
        response = self.put(endpoint, json=data)
        return response.json()

    def patch_json(self, endpoint, data=None):
        response = self.patch(endpoint, json=data)
        return response.json()