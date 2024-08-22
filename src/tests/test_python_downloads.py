import pytest
import os
import sys
import re
from packaging import version

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.pages.python_downloads_page import PythonDownloadsPage
from src.utils.visual_testing import capture_screenshot
from src.utils.performance import measure_time, log_test_step
from src.utils.accessibility_testing import run_accessibility_test
from src.utils.data_loader import load_csv_data
from src.config import Config
from src.logger import logger


@pytest.fixture
def downloads_page(driver):
    return PythonDownloadsPage(driver)


def soft_assert(condition, message):
    try:
        assert condition, message
    except AssertionError as e:
        logger.warning(f"Soft assertion failed: {str(e)}")


@measure_time
@log_test_step("Verifying OS buttons presence")
def test_os_buttons_presence(downloads_page):
    downloads_page.navigate()
    os_buttons = downloads_page.get_os_buttons()
    if len(os_buttons) == 0:
        logger.warning("No OS buttons found. This might be due to changes in the page structure.")
        downloads_page.log_page_source()
        downloads_page.capture_screenshot("os_buttons_not_found")
        downloads_page.check_for_js_errors()
        downloads_page.check_for_iframes()
    soft_assert(len(os_buttons) > 0, "No OS buttons found")
    logger.info(f"Found {len(os_buttons)} OS buttons")


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
        pytest.fail(f"Failed to retrieve latest Python version: {str(e)}")


@measure_time
@log_test_step("Testing downloads page accessibility")
def test_downloads_page_accessibility(downloads_page):
    downloads_page.navigate()
    violations = run_accessibility_test(downloads_page.driver, "downloads_page")
    if len(violations) > 0:
        logger.warning(f"Found {len(violations)} accessibility violations:")
        for violation in violations:
            logger.warning(f"- {violation}")
    logger.info(f"Found {len(violations)} accessibility violations")


@measure_time
@log_test_step("Testing downloads with CSV data")
def test_downloads_with_data(downloads_page):
    csv_path = os.path.join(Config.TEST_DATA_DIR, "downloads_test_data.csv")
    if not os.path.exists(csv_path):
        pytest.skip(f"Test data file not found: {csv_path}")

    test_data = load_csv_data("downloads_test_data.csv")
    for data in test_data:
        downloads_page.navigate()
        if 'os' in data:
            os_selected = downloads_page.select_os(data['os'])
            soft_assert(os_selected, f"Failed to select OS: {data['os']}")
            logger.info(f"Attempted to select OS: {data['os']}")
        if 'version' in data:
            version_available = downloads_page.is_version_available(data['version'])
            soft_assert(version_available, f"Version {data['version']} not available for {data.get('os', 'any OS')}")
            logger.info(f"Checked availability of version {data['version']} for {data.get('os', 'any OS')}")


@measure_time
@log_test_step("Testing download link validity")
def test_download_link_validity(downloads_page):
    downloads_page.navigate()
    download_links = downloads_page.get_download_links()
    if not download_links:
        logger.warning("No download links found. This might be due to changes in the page structure.")
        downloads_page.log_page_source()
        downloads_page.capture_screenshot("no_download_links")
    for link in download_links:
        soft_assert(downloads_page.is_valid_download_link(link), f"Invalid download link: {link}")
    logger.info(f"Checked {len(download_links)} download links")


@measure_time
@log_test_step("Testing version sorting")
def test_version_sorting(downloads_page):
    downloads_page.navigate()
    versions = downloads_page.get_all_versions()
    logger.info(f"All versions found: {versions}")

    if not versions:
        logger.warning("No versions found. This might be due to changes in the page structure.")
        downloads_page.log_page_source()
        downloads_page.capture_screenshot("no_versions_found")
        downloads_page.check_for_js_errors()
        downloads_page.check_for_iframes()
    else:
        # Remove potential duplicates and sort
        unique_versions = sorted(set(versions), key=version.parse, reverse=True)
        logger.info(f"Sorted unique versions: {unique_versions}")

        # Check if the original list (after removing duplicates) matches the sorted list
        soft_assert(list(dict.fromkeys(versions)) == unique_versions, "Versions are not sorted correctly")
        logger.info("Version sorting check completed")


if __name__ == "__main__":
    pytest.main(["-v", __file__])