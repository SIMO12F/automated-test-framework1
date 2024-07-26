import sys
import os
import pytest
from datetime import datetime
from src.config import Config
from src.logger import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException

def setup_environment():
    """Set up the test environment."""
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs(Config.get_log_dir(), exist_ok=True)

def get_pytest_args():
    """Generate pytest arguments."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(Config.REPORT_DIR, f"test_report_{timestamp}.html")

    args = [
        "-v",
        f"--html={report_file}",
        "--self-contained-html",
        "--capture=tee-sys",
        f"--log-file={Config.LOG_FILE}",
        f"--log-file-level={Config.LOG_LEVEL}",
        f"--metadata=Environment,{Config.ENVIRONMENT}",
        f"--metadata=Browsers,{', '.join(Config.BROWSERS)}",
        f"--metadata=Headless,{'Enabled' if Config.HEADLESS else 'Disabled'}",
        "src/tests/test_search.py",
        "-n", "auto"
    ]

    return args

def create_driver(browser_name):
    if browser_name == "chrome":
        try:
            chrome_driver_path = r"C:\path\to\chromedriver.exe"  # Replace with the actual path to the Chrome driver
            service = ChromeService(chrome_driver_path)
            options = webdriver.ChromeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            return webdriver.Chrome(service=service, options=options)
        except WebDriverException as e:
            logger.error(f"WebDriverException occurred during {browser_name} browser initialization: {str(e)}")
            logger.error(f"Failed to initialize {browser_name} browser.")
            return None
    elif browser_name == "firefox":
        try:
            firefox_driver_path = r"C:\path\to\geckodriver.exe"  # Replace with the actual path to the Firefox driver
            service = FirefoxService(firefox_driver_path)
            options = webdriver.FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            return webdriver.Firefox(service=service, options=options)
        except WebDriverException as e:
            logger.error(f"WebDriverException occurred during {browser_name} browser initialization: {str(e)}")
            logger.error(f"Failed to initialize {browser_name} browser.")
            return None
    elif browser_name == "edge":
        try:
            edge_driver_path = r"C:\path\to\msedgedriver.exe"  # Replace with the actual path to the Edge driver
            service = EdgeService(edge_driver_path)
            options = webdriver.EdgeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            return webdriver.Edge(service=service, options=options)
        except WebDriverException as e:
            logger.error(f"WebDriverException occurred during {browser_name} browser initialization: {str(e)}")
            logger.error(f"Failed to initialize {browser_name} browser.")
            return None
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

def main():
    logger.info("Starting test execution")
    logger.info(f"Running tests in {Config.ENVIRONMENT} environment")
    logger.info(f"Browsers: {', '.join(Config.BROWSERS)}")
    logger.info(f"Headless mode: {'Enabled' if Config.HEADLESS else 'Disabled'}")
    logger.info(f"Base URL: {Config.get_base_url()}")
    logger.info(f"API Base URL: {Config.get_api_base_url()}")

    setup_environment()

    pytest_args = get_pytest_args()
    logger.info(f"Running tests with arguments: {pytest_args}")

    exit_code = 0
    for browser_name in Config.BROWSERS:
        logger.info(f"Setting up {browser_name} browser")
        driver = create_driver(browser_name)
        if driver:
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            logger.info(f"Browser setup complete. Implicit wait set to {Config.IMPLICIT_WAIT} seconds")

            exit_code = pytest.main(pytest_args)

            logger.info(f"Tearing down {browser_name} browser")
            driver.quit()
        else:
            logger.error(f"Failed to initialize {browser_name} browser. Skipping tests for this browser.")
            exit_code = 1

    logger.info(f"Test execution completed with exit code: {exit_code}")

    if exit_code == 0:
        logger.info("All tests passed successfully")
    elif exit_code == 1:
        logger.warning("Some tests failed")
    elif exit_code == 2:
        logger.error("Test execution was interrupted by the user")
    elif exit_code == 3:
        logger.error("Internal error occurred in pytest")
    elif exit_code == 4:
        logger.error("pytest command line usage error")
    elif exit_code == 5:
        logger.error("No tests were collected")

    logger.info(f"Test report generated at: {os.path.join(Config.REPORT_DIR, 'test_report_*.html')}")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())