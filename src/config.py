from pathlib import Path
import os
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Config:
    # Project structure
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    SCREENSHOT_DIR = PROJECT_ROOT / 'screenshots'
    REPORT_DIR = PROJECT_ROOT / 'reports'
    LOG_DIR = PROJECT_ROOT / 'logs'
    TEST_DATA_DIR = PROJECT_ROOT / 'test_data'

    # Test execution settings
    BROWSER = os.getenv('TEST_BROWSER', 'chrome')
    BROWSERS = os.getenv('TEST_BROWSERS', 'chrome,firefox,edge').split(',')
    HEADLESS = os.getenv('TEST_HEADLESS', 'False').lower() == 'true'
    ENVIRONMENT = os.getenv('TEST_ENVIRONMENT', 'development')

    # URLs
    BASE_URL = "https://www.python.org"
    API_BASE_URL = "https://jsonplaceholder.typicode.com"

    # Timeouts and waits
    IMPLICIT_WAIT = int(os.getenv('TEST_IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('TEST_EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    API_TIMEOUT = float(os.getenv('API_TIMEOUT', '5.0'))

    # Logging
    LOG_LEVEL = os.getenv('TEST_LOG_LEVEL', 'INFO')
    LOG_FILE = LOG_DIR / 'test_execution.log'

    # Performance and visual testing
    PERFORMANCE_THRESHOLD = float(os.getenv('PERFORMANCE_THRESHOLD', '5.0'))
    VISUAL_DIFF_THRESHOLD = float(os.getenv('VISUAL_DIFF_THRESHOLD', '0.1'))

    # Accessibility testing
    GENERATE_ACCESSIBILITY_REPORT = os.getenv('GENERATE_ACCESSIBILITY_REPORT', 'False').lower() == 'true'
    ACCESSIBILITY_STANDARD = os.getenv('ACCESSIBILITY_STANDARD', 'WCAG2AA')

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')

    # Test data
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'test@example.com')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', 'password123')

    # CI/CD
    CI_EXECUTION = os.getenv('CI', 'False').lower() == 'true'

    @classmethod
    def setup(cls):
        """Create necessary directories if they don't exist."""
        for directory in [cls.SCREENSHOT_DIR, cls.REPORT_DIR, cls.LOG_DIR, cls.TEST_DATA_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_chrome_options():
        chrome_options = ChromeOptions()
        if Config.HEADLESS:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-search-engine-choice-screen')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            "distribution.suppress_first_run_bubble": True,
            "distribution.import_search_engine_dialog_shown": True,
            "distribution.import_bookmarks_dialog_shown": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

# Create necessary directories
Config.setup()