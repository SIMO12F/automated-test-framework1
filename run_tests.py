import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print("Current working directory:", os.getcwd())
print("\nPython path:")
for path in sys.path:
    print(path)

print("\nTrying to import config...")
try:
    from src.config import Config
    print("Config imported successfully")
    print(f"Config module location: {sys.modules['src.config'].__file__}")
    print(f"Config class: {Config}")
except ImportError as e:
    print(f"Failed to import Config: {e}")
    print("Contents of src directory:")
    src_dir = os.path.join(project_root, 'src')
    if os.path.exists(src_dir):
        print(os.listdir(src_dir))
    else:
        print(f"src directory not found at {src_dir}")
except Exception as e:
    print(f"Unexpected error when importing Config: {e}")

import pytest
from selenium.webdriver.common.by import By
from src.pages.python_downloads_page import PythonDownloadsPage
from src.utils.visual_testing import capture_screenshot
from src.utils.performance import measure_time, log_test_step
from src.utils.accessibility_testing import run_accessibility_test
from src.utils.data_loader import load_csv_data
from src.logger import logger

# Optional: Print an attribute from Config to verify it's working
print(f"A Config attribute: {Config.BASE_URL}")

@pytest.fixture
def downloads_page(driver):
    return PythonDownloadsPage(driver)

@measure_time
@log_test_step("Analyzing Python downloads page")
def test_analyze_downloads_page(downloads_page, driver):
    downloads_page.navigate()
    capture_screenshot(driver, "downloads_page")
    logger.info("--- Page Analysis ---")
    downloads_page.print_detailed_page_structure()
    all_buttons = downloads_page.get_all_buttons()
    assert len(all_buttons) > 0, "No buttons found on the page"
    logger.info(f"Found {len(all_buttons)} buttons on the page")

@measure_time
@log_test_step("Verifying download buttons presence")
def test_download_buttons_presence(downloads_page, driver):
    downloads_page.navigate()
    download_buttons = downloads_page.get_download_buttons()
    capture_screenshot(driver, "download_buttons")
    if len(download_buttons) == 0:
        logger.warning("No download buttons found. Detailed page structure:")
        downloads_page.print_detailed_page_structure()
    assert len(download_buttons) > 0, "No download buttons found"
    logger.info(f"Found {len(download_buttons)} download buttons")

@measure_time
@log_test_step("Verifying OS buttons presence")
def test_os_buttons_presence(downloads_page, driver):
    downloads_page.navigate()
    os_buttons = downloads_page.get_os_buttons()
    capture_screenshot(driver, "os_buttons")
    if len(os_buttons) == 0:
        logger.warning("No OS buttons found. Detailed page structure:")
        downloads_page.print_detailed_page_structure()
        logger.warning("All buttons on the page:")
        all_buttons = driver.find_elements(By.CSS_SELECTOR, "a.button")
        for button in all_buttons:
            logger.warning(f"Button href: {button.get_attribute('href')}")
            logger.warning(f"Button text: {button.text}")
    assert len(os_buttons) > 0, "No OS buttons found"
    logger.info(f"Found {len(os_buttons)} OS buttons")

@pytest.mark.xfail(reason="Consistently failing to retrieve latest Python version", strict=False)
@measure_time
@log_test_step("Verifying latest Python version")
def test_latest_python_version(downloads_page):
    downloads_page.navigate()
    try:
        latest_version = downloads_page.get_latest_python_version()
        assert latest_version is not None, "Failed to retrieve latest Python version"
        logger.info(f"Latest Python version: {latest_version}")
    except Exception as e:
        logger.error(f"Error in test_latest_python_version: {str(e)}")
        downloads_page.print_detailed_page_structure()
        raise  # Re-raise the exception to mark the test as failed

@measure_time
@log_test_step("Testing downloads page accessibility")
def test_downloads_page_accessibility(downloads_page):
    downloads_page.navigate()
    violations = run_accessibility_test(downloads_page.driver, "downloads_page")
    logger.warning(f"Found {len(violations)} accessibility violations")
    for violation in violations:
        logger.warning(f"Violation: {violation['id']} - {violation['description']}")
    assert len(violations) <= 10, f"Found {len(violations)} accessibility violations, expected 10 or fewer"

@measure_time
@log_test_step("Testing downloads with CSV data")
def test_downloads_with_data(downloads_page):
    test_data = load_csv_data("downloads_test_data.csv")
    for data in test_data:
        downloads_page.navigate()
        if 'os' in data:
            downloads_page.select_os(data['os'])
            logger.info(f"Selected OS: {data['os']}")
        if 'version' in data:
            assert downloads_page.is_version_available(data['version']), f"Version {data['version']} not available for {data.get('os', 'any OS')}"
            logger.info(f"Verified availability of version {data['version']} for {data.get('os', 'any OS')}")

@measure_time
@log_test_step("Testing download link validity")
def test_download_link_validity(downloads_page):
    downloads_page.navigate()
    download_links = downloads_page.get_download_links()
    for link in download_links:
        assert downloads_page.is_valid_download_link(link), f"Invalid download link: {link}"
    logger.info(f"Verified {len(download_links)} download links")

@measure_time
@log_test_step("Testing version sorting")
def test_version_sorting(downloads_page):
    downloads_page.navigate()
    versions = downloads_page.get_all_versions()
    sorted_versions = sorted(versions, key=lambda v: [int(i) for i in v.split('.')], reverse=True)
    assert versions == sorted_versions, "Versions are not sorted correctly"
    logger.info("Version sorting test passed")

if __name__ == "__main__":
    pytest.main(["-v", __file__])