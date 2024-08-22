import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from src.pages.python_home_page import PythonHomePage
from src.pages.python_search_results_page import PythonSearchResultsPage
from src.pages.python_downloads_page import PythonDownloadsPage
from src.utils.screenshot import capture_screenshot
from src.utils.performance import measure_time, log_test_step, measure_page_load_time
from src.config import Config
from src.logger import logger


@pytest.fixture
def python_home(driver):
    return PythonHomePage(driver)


@pytest.fixture
def python_search_results(driver):
    return PythonSearchResultsPage(driver)


@pytest.fixture
def python_downloads(driver):
    return PythonDownloadsPage(driver)


@measure_time
@log_test_step("Verifying main navigation elements")
def test_main_navigation(python_home, driver):
    python_home.navigate()
    python_home.wait_for_page_load()
    menu_items = python_home.get_main_menu_items()
    capture_screenshot(driver, "main_navigation")

    assert len(menu_items) > 0, "No menu items found"
    non_empty_items = [item for item in menu_items if item.text.strip()]
    assert len(non_empty_items) > 0, "All menu items are empty"
    for item in non_empty_items:
        logger.info(f"Menu item text: {item.text}")


@measure_time
@log_test_step("Testing search functionality and autocomplete")
def test_search_functionality(python_home, python_search_results, driver):
    python_home.navigate()
    python_home.wait_for_page_load()

    search_term = "python"
    python_home.perform_search(search_term)
    results_count = python_search_results.get_search_results_count()
    capture_screenshot(driver, "search_results")
    assert results_count > 0, f"No search results found for '{search_term}'"

    python_home.navigate()
    python_home.wait_for_page_load()
    python_home.enter_search_term("py")
    autocomplete_items = python_home.get_autocomplete_items()
    if autocomplete_items:
        logger.info(f"Autocomplete suggestions: {autocomplete_items}")
    else:
        logger.warning("No autocomplete suggestions displayed")


@measure_time
@log_test_step("Testing invalid search")
def test_invalid_search(python_home, python_search_results, driver):
    python_home.navigate()
    python_home.wait_for_page_load()
    invalid_search_term = "xyzabcdefghijklmnop"
    python_home.perform_search(invalid_search_term)
    results_count = python_search_results.get_search_results_count()
    capture_screenshot(driver, "invalid_search_results")
    assert results_count == 0, f"Unexpected search results found for invalid term: '{invalid_search_term}'"


@measure_time
@log_test_step("Verifying downloads page loads")
def test_downloads_page_loads(python_downloads, driver):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            python_downloads.navigate()
            WebDriverWait(driver, Config.EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".download-widget"))
            )
            assert "/downloads/" in driver.current_url, "Not on downloads page"
            logger.info("Downloads page loaded successfully")
            return
        except (TimeoutException, AssertionError) as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2)
            else:
                logger.error(f"All attempts failed to load downloads page: {str(e)}")
                capture_screenshot(driver, "downloads_page_error")
                pytest.fail(f"Failed to load downloads page after {max_retries} attempts")


@measure_time
@log_test_step("Testing page load performance")
def test_page_load_performance(python_home, driver):
    logger.info(f"Starting page load performance test. Threshold: {Config.PERFORMANCE_THRESHOLD} seconds")
    python_home.navigate()

    load_time = measure_page_load_time(driver)

    if load_time is None:
        logger.error("Failed to measure page load time")
        pytest.fail("Failed to measure page load time")

    logger.info(f"Measured page load time: {load_time:.2f} seconds")

    try:
        assert load_time < Config.PERFORMANCE_THRESHOLD, f"Page load time ({load_time:.2f}s) exceeded threshold of {Config.PERFORMANCE_THRESHOLD}s"
        logger.info("Page load performance test passed successfully")
    except AssertionError as e:
        logger.error(f"Page load performance test failed: {str(e)}")
        pytest.fail(str(e))


@measure_time
@log_test_step("Testing navigation to key pages")
def test_key_page_navigation(python_home, driver):
    key_pages = {
        "about": f"{Config.BASE_URL}/about/",
        "documentation": f"{Config.BASE_URL}/doc/"
    }

    for page, url in key_pages.items():
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to navigate to {page} page (attempt {attempt + 1})")
                driver.get(url)
                WebDriverWait(driver, Config.EXPLICIT_WAIT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                current_url = driver.current_url
                logger.info(f"Current URL after navigation: {current_url}")

                # Check if the current URL contains either the full page name or its shorthand
                assert page in current_url.lower() or (page == "documentation" and "/doc/" in current_url.lower()), \
                    f"Failed to navigate to {page} page. Current URL: {current_url}"

                logger.info(f"Successfully navigated to {page} page")
                break
            except (TimeoutException, WebDriverException, AssertionError) as e:
                logger.warning(f"Attempt {attempt + 1} failed for {page} page: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                    time.sleep(2)
                else:
                    logger.error(f"All attempts failed for {page} page")
                    capture_screenshot(driver, f"navigation_error_{page}")
                    pytest.fail(f"Failed to navigate to {page} page after {max_retries} attempts. Last error: {str(e)}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])