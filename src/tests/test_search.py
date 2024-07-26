import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.pages.search_page import SearchPage
from src.test_data import TestData
from src.config import Config
from src.logger import logger
from src.utils.performance import measure_time


@pytest.fixture(params=Config.BROWSERS)
def browser(request):
    browser_name = request.param
    logger.info(f"Setting up {browser_name} browser")

    try:
        if browser_name == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=service, options=options)
        elif browser_name == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=service, options=options)
        elif browser_name == "edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            options = webdriver.EdgeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        logger.info(f"Browser setup complete. Implicit wait set to {Config.IMPLICIT_WAIT} seconds")
        yield driver
    except Exception as e:
        logger.error(f"Failed to initialize {browser_name} browser: {str(e)}")
        pytest.skip(f"Skipping test due to browser initialization failure: {str(e)}")
    finally:
        if 'driver' in locals():
            logger.info(f"Tearing down {browser_name} browser")
            driver.quit()

@measure_time
def test_python_search(browser):
    logger.info("Starting Python search test")
    page = SearchPage(browser)
    page.navigate()
    logger.info(f"Searching for '{TestData.SEARCH_QUERY}'")
    page.search(TestData.SEARCH_QUERY)
    assert page.is_search_performed(), f"Search for '{TestData.SEARCH_QUERY}' was not performed"
    result_count = page.get_search_result_count()
    logger.info(f"Found {result_count} search results")
    assert result_count > 0, f"No search results found for '{TestData.SEARCH_QUERY}'"
    results = page.get_search_results().lower()
    assert TestData.SEARCH_QUERY.lower() in results, f"Search query '{TestData.SEARCH_QUERY}' not found in results"
    logger.info("Python search test completed successfully")


@measure_time
def test_empty_search(browser):
    logger.info("Starting empty search test")
    page = SearchPage(browser)
    page.navigate()
    logger.info("Performing empty search")
    page.search("")
    assert page.is_search_performed(), "Empty search was not performed"
    results = page.get_search_results().lower()
    expected_texts = ["search", "results", "found", "enter your search"]
    assert any(text in results for text in
               expected_texts), f"Expected search-related text not found on page. Page content: {results[:500]}..."
    logger.info("Empty search test completed successfully")


@measure_time
def test_alternative_search(browser):
    logger.info("Starting alternative search test")
    page = SearchPage(browser)
    page.navigate()
    logger.info(f"Searching for '{TestData.ALTERNATIVE_SEARCH_QUERY}'")
    page.search(TestData.ALTERNATIVE_SEARCH_QUERY)
    assert page.is_search_performed(), f"Search for '{TestData.ALTERNATIVE_SEARCH_QUERY}' was not performed"
    result_count = page.get_search_result_count()
    logger.info(f"Found {result_count} search results")
    assert result_count > 0, f"No search results found for '{TestData.ALTERNATIVE_SEARCH_QUERY}'"
    results = page.get_search_results().lower()
    assert TestData.ALTERNATIVE_SEARCH_QUERY.lower() in results, f"Search query '{TestData.ALTERNATIVE_SEARCH_QUERY}' not found in results"
    logger.info("Alternative search test completed successfully")


@measure_time
@pytest.mark.parametrize("search_data", TestData.get_search_data())
def test_parameterized_search(browser, search_data):
    logger.info(f"Starting parameterized search test with query: {search_data['search_query']}")
    page = SearchPage(browser)
    page.navigate()
    page.search(search_data['search_query'])
    assert page.is_search_performed(), f"Search for '{search_data['search_query']}' was not performed"
    result_count = page.get_search_result_count()
    logger.info(f"Found {result_count} search results")
    assert result_count > 0, f"No search results found for '{search_data['search_query']}'"
    results = page.get_search_results().lower()
    assert search_data[
               'search_query'].lower() in results, f"Search query '{search_data['search_query']}' not found in search results"
    logger.info(f"Search results contain the query '{search_data['search_query']}'")
    # Optional: Check if the expected result is in the first few results
    first_result = results.split('\n')[0] if '\n' in results else results
    if search_data['expected_result'].lower() in first_result:
        logger.info(f"Expected result '{search_data['expected_result']}' found in the first search result")
    else:
        logger.warning(f"Expected result '{search_data['expected_result']}' not found in the first search result")
    logger.info(f"Parameterized search test for '{search_data['search_query']}' completed")
@measure_time
def test_search_with_invalid_query(browser):
    logger.info("Starting search with invalid query test")
    page = SearchPage(browser)
    page.navigate()
    logger.info(f"Searching for '{TestData.INVALID_SEARCH_QUERY}'")
    page.search(TestData.INVALID_SEARCH_QUERY)
    assert page.is_search_performed(), f"Search for '{TestData.INVALID_SEARCH_QUERY}' was not performed"
    result_count = page.get_search_result_count()
    logger.info(f"Found {result_count} search results")
    assert result_count == 0, f"Unexpected search results found for '{TestData.INVALID_SEARCH_QUERY}'"
    logger.info("Search with invalid query test completed successfully")