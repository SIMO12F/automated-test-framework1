from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.config import Config
from src.logger import logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = Config

    def wait_for_element(self, locator, timeout=Config.EXPLICIT_WAIT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found with locator: {locator}")
            raise

    def wait_for_elements(self, locator, timeout=Config.EXPLICIT_WAIT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            logger.error(f"Elements not found with locator: {locator}")
            raise

    def wait_for_element_clickable(self, locator, timeout=Config.EXPLICIT_WAIT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            logger.error(f"Element not clickable with locator: {locator}")
            raise

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Clicked element with locator: {locator}")

    def enter_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Entered text '{text}' into element with locator: {locator}")

    def get_text(self, locator):
        element = self.wait_for_element(locator)
        text = element.text
        logger.info(f"Got text '{text}' from element with locator: {locator}")
        return text

    def is_element_displayed(self, locator, timeout=Config.EXPLICIT_WAIT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except TimeoutException:
            logger.warning(f"Element not visible with locator: {locator}")
            return False