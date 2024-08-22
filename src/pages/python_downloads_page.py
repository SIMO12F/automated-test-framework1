import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.config import Config
from src.logger import logger
from retrying import retry


class PythonDownloadsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = f"{Config.BASE_URL}/downloads/"

    def navigate(self):
        self.driver.get(self.url)
        self.wait_for_page_load()
        logger.info(f"Navigated to {self.url}")

    def wait_for_page_load(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logger.info("Page load complete")
        except TimeoutException:
            logger.error(f"Page load timed out after {timeout} seconds")

    def get_all_buttons(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.button")
        logger.info(f"Found {len(buttons)} buttons on the page")
        return buttons

    def get_download_buttons(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.button[href*='download']")
        logger.info(f"Found {len(buttons)} download buttons")
        return buttons

    def get_os_buttons(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.button[data-os]")
        if not buttons:
            # Try a more general selector if the specific one doesn't work
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.button")
        logger.info(f"Found {len(buttons)} potential OS buttons")
        return buttons

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def get_latest_python_version(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            selectors = [
                ".download-for-current-os .release-number",
                "a.button.button-primary span",
                "a.button.button-primary",
                ".release-number",
                "h1:contains('Download')",
                "h2:contains('Download')",
            ]

            for selector in selectors:
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    version_text = element.text
                    match = re.search(r'\d+\.\d+\.\d+', version_text)
                    if match:
                        version = match.group(0)
                        logger.info(f"Found latest Python version: {version}")
                        return version
                except:
                    continue

            # If we couldn't find the version, log the page source for debugging
            logger.error("Failed to find latest Python version. Page source:")
            logger.error(self.driver.page_source)

            raise ValueError("Failed to retrieve latest Python version")
        except Exception as e:
            logger.error(f"Error retrieving latest Python version: {str(e)}")
            raise

    def get_all_versions(self):
        version_elements = self.driver.find_elements(By.CSS_SELECTOR, ".release-number")
        versions = []
        for element in version_elements:
            match = re.search(r'\d+\.\d+\.\d+', element.text)
            if match:
                versions.append(match.group(0))
        logger.info(f"Found {len(versions)} Python versions")
        return sorted(versions, key=lambda v: [int(i) for i in v.split('.')], reverse=True)

    def get_download_links(self):
        links = [link.get_attribute('href') for link in self.get_download_buttons()]
        logger.info(f"Found {len(links)} download links")
        return links

    def is_valid_download_link(self, link):
        is_valid = link.startswith(Config.BASE_URL) and 'download' in link
        logger.info(f"Download link {link} is {'valid' if is_valid else 'invalid'}")
        return is_valid

    def select_os(self, os_name):
        os_buttons = self.get_os_buttons()
        for button in os_buttons:
            if os_name.lower() in button.text.lower():
                button.click()
                logger.info(f"Selected OS: {os_name}")
                return True
        logger.warning(f"OS not found: {os_name}")
        return False

    def is_version_available(self, version):
        version_elements = self.driver.find_elements(By.CSS_SELECTOR, ".release-number")
        for element in version_elements:
            if version in element.text:
                logger.info(f"Version {version} is available")
                return True
        logger.warning(f"Version {version} is not available")
        return False

    def print_detailed_page_structure(self):
        elements = self.driver.find_elements(By.XPATH, "//*")
        logger.info("Detailed page structure:")
        for element in elements:
            logger.info(
                f"{element.tag_name}: class='{element.get_attribute('class')}', id='{element.get_attribute('id')}', text='{element.text[:50]}'")