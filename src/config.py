import os

class Config:
    # Browser settings
    BROWSER = "chrome"  # Options: "chrome", "firefox", "edge"
    HEADLESS = False

    # Timeout settings
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20

    # URL settings
    BASE_URL = "https://www.python.org"

    # Test environment
    ENVIRONMENT = "test"  # Options: "test", "staging", "production"

    # Project root directory
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Reporting settings
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshots")
    REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

    # Test data
    TEST_DATA_DIR = os.path.join(PROJECT_ROOT, "test_data")
    TEST_DATA_FILE = os.path.join(PROJECT_ROOT, "src", "test_data", "search_data.csv")

    # Parallel execution
    PARALLEL_EXECUTION = True

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = os.path.join(PROJECT_ROOT, "automation.log")
    # API Settings
    API_BASE_URL = "https://api.python.org/v1/"  # Replace with actual API base URL
    # Browser settings
    BROWSERS = ["chrome", "firefox", "edge"]  # Add or remove browsers as needed
    HEADLESS = False

    # Test execution settings
    RUN_UI_TESTS = True
    RUN_API_TESTS = True
    PARALLEL_EXECUTION = True

    @classmethod
    def get_browser(cls):
        return cls.BROWSER.lower()

    @classmethod
    def get_base_url(cls):
        if cls.ENVIRONMENT == "test":
            return cls.BASE_URL
        elif cls.ENVIRONMENT == "staging":
            return "https://staging.python.org"  # Replace with actual staging URL if different
        elif cls.ENVIRONMENT == "production":
            return "https://www.python.org"
        else:
            raise ValueError(f"Invalid environment: {cls.ENVIRONMENT}")

    @classmethod
    def get_screenshot_dir(cls):
        if not os.path.exists(cls.SCREENSHOT_DIR):
            os.makedirs(cls.SCREENSHOT_DIR)
        return cls.SCREENSHOT_DIR

    @classmethod
    def get_report_dir(cls):
        if not os.path.exists(cls.REPORT_DIR):
            os.makedirs(cls.REPORT_DIR)
        return cls.REPORT_DIR

    @classmethod
    def get_test_data_file(cls):
        if not os.path.exists(cls.TEST_DATA_DIR):
            os.makedirs(cls.TEST_DATA_DIR)
        return cls.TEST_DATA_FILE