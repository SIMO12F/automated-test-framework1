import os


class Config:
    # Project Root
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Browser settings
    BROWSER = os.getenv('TEST_BROWSER', 'chrome')  # Options: "chrome", "firefox", "edge"
    HEADLESS = os.getenv('TEST_HEADLESS', 'False').lower() == 'true'

    # Timeout settings
    IMPLICIT_WAIT = int(os.getenv('TEST_IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('TEST_EXPLICIT_WAIT', '20'))

    # Test execution settings
    PARALLEL_EXECUTION = os.getenv('TEST_PARALLEL', 'False').lower() == 'true'

    # Reporting settings
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, 'screenshots')
    REPORT_DIR = os.path.join(PROJECT_ROOT, 'reports')

    # Environment settings
    ENVIRONMENT = os.getenv('TEST_ENV', 'dev')  # Options: 'dev', 'staging', 'prod'

    # URLs
    BASE_URLS = {
        'dev': 'https://dev.example.com',
        'staging': 'https://staging.example.com',
        'prod': 'https://www.example.com'
    }

    API_BASE_URLS = {
        'dev': 'https://api.dev.example.com/v1/',
        'staging': 'https://api.staging.example.com/v1/',
        'prod': 'https://api.example.com/v1/'
    }

    @classmethod
    def get_base_url(cls):
        return cls.BASE_URLS.get(cls.ENVIRONMENT, cls.BASE_URLS['dev'])

    @classmethod
    def get_api_base_url(cls):
        return cls.API_BASE_URLS.get(cls.ENVIRONMENT, cls.API_BASE_URLS['dev'])

    # Logging settings
    LOG_LEVEL = os.getenv('TEST_LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', 'test_execution.log')

    @classmethod
    def get_log_dir(cls):
        log_dir = os.path.dirname(cls.LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    # Test data
    TEST_DATA_DIR = os.path.join(PROJECT_ROOT, 'test_data')

    @classmethod
    def get_test_data_file(cls, filename):
        return os.path.join(cls.TEST_DATA_DIR, filename)

    # Add any other configuration settings your project needsexport TEST_ENV=staging