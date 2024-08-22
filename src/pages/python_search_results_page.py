from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.pages.base_page import BasePage
from src.config import Config
from src.logger import logger

class PythonSearchResultsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_results = (By.CSS_SELECTOR, "ul.list-recent-events li")
        self.no_results_message = (By.CSS_SELECTOR, "p.introduction")

    def get_search_results_count(self):
        try:
            results = self.wait_for_elements(self.search_results)
            count = len(results)
            logger.info(f"Found {count} search results")
            return count
        except TimeoutException:
            logger.warning("No search results found")
            return 0

    def get_search_results(self):
        return [result.text for result in self.wait_for_elements(self.search_results)]

    def is_no_results_message_displayed(self):
        try:
            self.wait_for_element(self.no_results_message)
            logger.info("No results message is displayed")
            return True
        except TimeoutException:
            logger.info("No results message is not displayed")
            return False

    def get_first_result_title(self):
        results = self.wait_for_elements(self.search_results)
        if results:
            title = results[0].find_element(By.CSS_SELECTOR, "h3").text
            logger.info(f"First result title: {title}")
            return title
        logger.warning("No search results found")
        return None

    def click_first_result(self):
        results = self.wait_for_elements(self.search_results)
        if results:
            results[0].find_element(By.CSS_SELECTOR, "a").click()
            logger.info("Clicked on the first search result")
        else:
            logger.warning("No search results found to click")

    def get_result_titles(self):
        titles = [result.find_element(By.CSS_SELECTOR, "h3").text
                  for result in self.wait_for_elements(self.search_results)]
        logger.info(f"Found {len(titles)} result titles")
        return titles

    def get_result_urls(self):
        urls = [result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                for result in self.wait_for_elements(self.search_results)]
        logger.info(f"Found {len(urls)} result URLs")
        return urls