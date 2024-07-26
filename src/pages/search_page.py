from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.config import Config
from src.logger import logger

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = Config.get_base_url()
        self.search_input = (By.NAME, "q")
        self.search_button = (By.ID, "submit")
        self.search_results = (By.CSS_SELECTOR, "#content")

    def navigate(self):
        logger.info(f"Navigating to {self.url}")
        self.driver.get(self.url)

    def search(self, query):
        logger.info(f"Performing search with query: '{query}'")
        try:
            search_box = WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
                EC.presence_of_element_located(self.search_input)
            )
            search_box.clear()
            search_box.send_keys(query)

            # Handle browser-specific differences
            if self.driver.capabilities['browserName'] == 'firefox':
                logger.info("Handling search for Firefox browser")
                search_box.send_keys(Keys.RETURN)
                WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
                    EC.presence_of_element_located(self.search_results)
                )
            else:
                logger.info("Handling search for non-Firefox browser")
                search_box.send_keys(Keys.RETURN)
                WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
                    EC.presence_of_element_located(self.search_results)
                )
        except TimeoutException:
            logger.error(f"Timeout waiting for search results with query: '{query}'")
        except NoSuchElementException:
            logger.error(f"Search input element not found")

    def is_search_performed(self):
        return "search" in self.driver.current_url.lower()

    def get_search_result_count(self):
        try:
            results = self.driver.find_elements(*self.search_results)
            return len(results)
        except NoSuchElementException:
            logger.warning("No search results found")
            return 0

    def get_search_results(self):
        try:
            return self.driver.find_element(*self.search_results).text
        except NoSuchElementException:
            logger.warning("Search results element not found")
            return ""