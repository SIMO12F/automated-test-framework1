import os


class Config:
    # Project Root
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Browser settings
    BROWSER = os.getenv('TEST_BROWSER', 'chrome')
    BROWSERS = os.getenv('TEST_BROWSERS', 'chrome,firefox,edge').split(',')
    HEADLESS = os.getenv('TEST_HEADLESS', 'False').lower() == 'true'

    # Timeout settings
    IMPLICIT_WAIT = int(os.getenv('TEST_IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('TEST_EXPLICIT_WAIT', '20'))

    # Test execution settings
    # In config.py
    PARALLEL_EXECUTION = os.getenv('TEST_PARALLEL', 'True').lower() == 'true'

    # Reporting settings
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, 'screenshots')
    REPORT_DIR = os.path.join(PROJECT_ROOT, 'reports')

    # Environment settings
    ENVIRONMENT = os.getenv('TEST_ENV', 'dev')  # Options: 'dev', 'staging', 'prod'

    # URLs
    BASE_URLS = {
        'dev': 'https://www.python.org',
        'staging': 'https://www.python.org',
        'prod': 'https://www.python.org'
    }

    API_BASE_URLS = {
        'dev': 'https://jsonplaceholder.typicode.com/',
        'staging': 'https://jsonplaceholder.typicode.com/',
        'prod': 'https://jsonplaceholder.typicode.com/'
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