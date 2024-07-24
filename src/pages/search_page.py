from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.config import Config
from src.logger import logger

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = Config.get_base_url()
        self.search_input = (By.NAME, "q")
        self.search_button = (By.ID, "submit")
        self.search_results = (By.CLASS_NAME, "list-recent-events")
        self.search_result_items = (By.CSS_SELECTOR, ".list-recent-events li")

    def navigate(self):
        logger.info(f"Navigating to {self.url}")
        self.driver.get(self.url)

    def search(self, query):
        logger.info(f"Performing search with query: '{query}'")
        search_box = self.driver.find_element(*self.search_input)
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
                EC.url_contains("search")
            )
        except TimeoutException:
            logger.warning(f"Search URL did not change after searching for '{query}'")

    def is_search_performed(self):
        return "search" in self.driver.current_url.lower()

    def get_search_result_count(self):
        try:
            results = self.driver.find_elements(*self.search_result_items)
            count = len(results)
            logger.info(f"Found {count} search results")
            return count
        except NoSuchElementException:
            logger.warning("No search result elements found")
            return 0

    def get_search_results(self):
        try:
            results = self.driver.find_elements(*self.search_result_items)
            if results:
                text_results = [result.text for result in results]
                full_text = "\n".join(text_results)
            else:
                # If no specific result items found, get text from a more general container
                full_text = self.driver.find_element(By.ID, "content").text
            logger.info(f"Retrieved search results (first 200 chars): {full_text[:200]}...")
            return full_text
        except NoSuchElementException:
            logger.warning("No search result elements found, returning full page text")
            return self.driver.find_element(By.TAG_NAME, "body").text

    def get_first_result_title(self):
        try:
            first_result = self.driver.find_element(*self.search_result_items)
            title = first_result.find_element(By.CSS_SELECTOR, "h3").text
            logger.info(f"First result title: {title}")
            return title
        except NoSuchElementException:
            logger.warning("Could not find first result title")
            return ""

    def is_result_present(self, text):
        results = self.get_search_results().lower()
        is_present = text.lower() in results
        logger.info(f"Checking if '{text}' is present in results: {is_present}")
        return is_present
