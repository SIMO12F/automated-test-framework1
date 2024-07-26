import csv
import os
from src.config import Config
from src.logger import logger

class TestData:
    @staticmethod
    def get_search_data():
        data = []
        csv_file = os.path.join(Config.PROJECT_ROOT, 'src', 'test_data', 'search_data.csv')
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            logger.error(f"Test data file not found at {csv_file}")
        return data

    # Static test data (kept as fallback)
    PYTHON_URL = "https://www.python.org"
    SEARCH_QUERY = "pycon"
    ALTERNATIVE_SEARCH_QUERY = "django"
    INVALID_SEARCH_QUERY = "xyzabcdefg"

    @staticmethod
    def get_python_data():
        return {
            "url": TestData.PYTHON_URL,
            "search_query": TestData.SEARCH_QUERY,
            "alternative_query": TestData.ALTERNATIVE_SEARCH_QUERY,
            "invalid_query": TestData.INVALID_SEARCH_QUERY
        }

    @staticmethod
    def get_all_search_queries():
        return [
            TestData.SEARCH_QUERY,
            TestData.ALTERNATIVE_SEARCH_QUERY,
            TestData.INVALID_SEARCH_QUERY
        ]

    @staticmethod
    def get_valid_search_queries():
        return [
            TestData.SEARCH_QUERY,
            TestData.ALTERNATIVE_SEARCH_QUERY
        ]