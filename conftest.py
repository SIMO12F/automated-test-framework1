import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.config import Config
from src.logger import logger


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests (chrome, firefox, edge)")


@pytest.fixture(scope="session")
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        chrome_options = Config.get_chrome_options()

        # Create a custom Chrome profile
        user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')
        chrome_options.add_argument(f'user-data-dir={user_data_dir}')

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument('-headless')
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if Config.HEADLESS:
            options.add_argument('headless')
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()

    logger.info(f"Started {browser} browser in {'headless' if Config.HEADLESS else 'normal'} mode")

    yield driver

    driver.quit()
    logger.info(f"Closed {browser} browser")


@pytest.fixture(autouse=True)
def run_around_tests(driver):
    # Setup: can be used for any pre-test operations
    yield
    # Teardown: can be used for any post-test cleanup operations


def pytest_sessionstart(session):
    logger.info("Starting test session")


def pytest_sessionfinish(session, exitstatus):
    logger.info(f"Test session finished with exit status: {exitstatus}")


def pytest_runtest_setup(item):
    logger.info(f"Setting up test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    logger.info(f"Tearing down test: {item.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            logger.error(f"Test failed: {item.name}")
            driver.save_screenshot(f"{Config.SCREENSHOT_DIR}/{item.name}_failure.png")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")


@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()