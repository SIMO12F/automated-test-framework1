from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.pages.base_page import BasePage
from src.config import Config
from src.logger import logger

class PythonHomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.BASE_URL
        self.search_input = (By.ID, "id-search-field")
        self.search_button = (By.ID, "submit")
        self.main_menu = (By.CSS_SELECTOR, "#mainnav ul li a")
        self.autocomplete_items = (By.CSS_SELECTOR, ".autocomplete-suggestions .autocomplete-suggestion")

    def navigate(self):
        self.driver.get(self.url)
        self.wait_for_page_load()
        logger.info(f"Navigated to {self.url}")

    def wait_for_page_load(self, timeout=Config.EXPLICIT_WAIT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logger.info("Page loaded successfully")
        except TimeoutException:
            logger.error(f"Page load timed out after {timeout} seconds")
            raise

    def perform_search(self, query):
        self.enter_search_term(query)
        self.wait_for_element(self.search_button).click()
        logger.info(f"Performed search with query: {query}")

    def enter_search_term(self, query):
        search_input = self.wait_for_element(self.search_input)
        search_input.clear()
        search_input.send_keys(query)
        logger.info(f"Entered search term: {query}")

    def get_main_menu_items(self):
        menu_items = self.wait_for_elements(self.main_menu)
        logger.info(f"Found {len(menu_items)} main menu items")
        return menu_items

    def click_main_menu_item(self, item_text):
        menu_items = self.get_main_menu_items()
        for item in menu_items:
            if item_text.lower() in item.text.lower():
                item.click()
                logger.info(f"Clicked main menu item: {item_text}")
                return
        logger.warning(f"Main menu item not found: {item_text}")

    def get_autocomplete_items(self):
        try:
            items = WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
                EC.presence_of_all_elements_located(self.autocomplete_items)
            )
            return [item.text for item in items]
        except TimeoutException:
            logger.warning("No autocomplete items found")
            return []