import csv
import os
import json
from typing import List, Dict, Optional
from src.config import Config
from src.logger import logger
from faker import Faker

class TestData:
    fake = Faker()

    PYTHON_URL = "https://www.python.org"
    SEARCH_QUERY = "pycon"
    ALTERNATIVE_SEARCH_QUERY = "django"
    INVALID_SEARCH_QUERY = "xyzabcdefg"

    @staticmethod
    @staticmethod
    @staticmethod
    def get_search_data() -> List[Dict[str, str]]:
        data = []
        csv_file = os.path.join(Config.TEST_DATA_DIR, 'search_data.csv')
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'search_query' in row and 'expected_result' in row:
                        data.append(row)
                    else:
                        logger.warning(f"Skipping invalid row in CSV: {row}")
            logger.info(f"Loaded {len(data)} search data entries from {csv_file}")
        except FileNotFoundError:
            logger.warning(f"Test data file not found at {csv_file}. Using default data.")
            data = [
                {"search_query": "python", "expected_result": "Python programming language"},
                {"search_query": "django", "expected_result": "Django web framework"},
                {"search_query": "flask", "expected_result": "Flask web framework"},
            ]
        except Exception as e:
            logger.error(f"Error loading test data: {str(e)}")
            data = [
                {"search_query": "selenium", "expected_result": "Selenium WebDriver"},
                {"search_query": "pytest", "expected_result": "pytest testing framework"},
            ]

        if not data:
            logger.warning("No data loaded or generated. Creating random test data.")
            data = TestData.generate_test_data(3)  # Generate 3 random test data entries

        return data

    @classmethod
    def get_random_search_query(cls) -> str:
        return cls.fake.word()

    @classmethod
    def get_random_invalid_search_query(cls) -> str:
        return cls.fake.bothify(text='?#?#?#?')

    @classmethod
    def get_user_data(cls) -> Dict[str, str]:
        return {
            "username": cls.fake.user_name(),
            "email": cls.fake.email(),
            "password": cls.fake.password()
        }

    @staticmethod
    def load_json_data(filename: str) -> Optional[Dict]:
        file_path = os.path.join(Config.TEST_DATA_DIR, filename)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded JSON data from {file_path}")
            return data
        except FileNotFoundError:
            logger.error(f"JSON file not found at {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file {file_path}")
        except Exception as e:
            logger.error(f"Error loading JSON data: {str(e)}")
        return None

    @classmethod
    def get_python_data(cls) -> Dict[str, str]:
        return {
            "url": cls.PYTHON_URL,
            "search_query": cls.SEARCH_QUERY,
            "alternative_query": cls.ALTERNATIVE_SEARCH_QUERY,
            "invalid_query": cls.INVALID_SEARCH_QUERY
        }

    @classmethod
    def get_all_search_queries(cls) -> List[str]:
        return [cls.SEARCH_QUERY, cls.ALTERNATIVE_SEARCH_QUERY, cls.INVALID_SEARCH_QUERY]

    @classmethod
    def get_valid_search_queries(cls) -> List[str]:
        return [cls.SEARCH_QUERY, cls.ALTERNATIVE_SEARCH_QUERY]

    @classmethod
    def generate_test_data(cls, num_entries: int) -> List[Dict[str, str]]:
        return [
            {
                "search_query": cls.fake.word(),
                "expected_result": cls.fake.sentence(),
                "user": cls.get_user_data(),
                "timestamp": cls.fake.iso8601(),
                "category": cls.fake.random_element(elements=('Python', 'Django', 'Flask', 'Pandas', 'NumPy'))
            }
            for _ in range(num_entries)
        ]

    @classmethod
    def get_random_python_version(cls) -> str:
        major = cls.fake.random_int(min=3, max=3)
        minor = cls.fake.random_int(min=5, max=9)
        patch = cls.fake.random_int(min=0, max=15)
        return f"{major}.{minor}.{patch}"

    @classmethod
    def get_random_library(cls) -> Dict[str, str]:
        return {
            "name": cls.fake.word(),
            "version": f"{cls.fake.random_int(min=0, max=5)}.{cls.fake.random_int(min=0, max=15)}.{cls.fake.random_int(min=0, max=99)}",
            "description": cls.fake.sentence(),
            "author": cls.fake.name(),
            "website": cls.fake.url()
        }