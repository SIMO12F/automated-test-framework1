import csv
import os
from src.config import Config
from src.logger import logger

class TestData:
    @staticmethod
    def get_search_data():
        data = []
        try:
            with open(Config.TEST_DATA_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            if not data:
                logger.warning(f"No data found in {Config.TEST_DATA_FILE}")
            else:
                logger.info(f"Loaded {len(data)} rows from {Config.TEST_DATA_FILE}")
                logger.debug(f"Data: {data}")
        except FileNotFoundError:
            logger.error(f"Test data file not found at {Config.TEST_DATA_FILE}")
        except Exception as e:
            logger.error(f"Error reading test data file: {str(e)}")
        return data

    # Static test data (kept as fallback)
    EXAMPLE_URL = "https://example.com"
    PYTHON_URL = "https://www.python.org"
    SEARCH_QUERY = "pycon"
    ALTERNATIVE_SEARCH_QUERY = "django"
    EXAMPLE_TITLE = "Example Domain"
    EXAMPLE_HEADING = "Example Domain"
    EXAMPLE_PARAGRAPH_CONTENT = "for use in illustrative examples in documents"
    INVALID_SEARCH_QUERY = "xyzabcdefg"

    @staticmethod
    def get_example_data():
        return {
            "url": TestData.EXAMPLE_URL,
            "title": TestData.EXAMPLE_TITLE,
            "heading": TestData.EXAMPLE_HEADING,
            "paragraph_content": TestData.EXAMPLE_PARAGRAPH_CONTENT
        }

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