import sys
import os

# Add the parent directory of src to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.database import setup_database

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
