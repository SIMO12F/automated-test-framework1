import csv
import json
import os
from src.config import Config
from src.logger import logger

def load_csv_data(file_name):
    file_path = os.path.join(Config.TEST_DATA_DIR, file_name)
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        logger.info(f"Successfully loaded CSV data from {file_name}")
        return data
    except FileNotFoundError:
        logger.error(f"CSV file not found: {file_path}")
        raise
    except csv.Error as e:
        logger.error(f"Error reading CSV file {file_name}: {str(e)}")
        raise

def load_json_data(file_name):
    file_path = os.path.join(Config.TEST_DATA_DIR, file_name)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON data from {file_name}")
        return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file {file_name}: {str(e)}")
        raise