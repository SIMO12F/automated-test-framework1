import os
from datetime import datetime
from src.config import Config
from src.logger import logger


def capture_screenshot(driver, name):
    """
    Capture a screenshot and save it with a timestamp.

    :param driver: Selenium WebDriver instance
    :param name: Base name for the screenshot
    :return: Path to the saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)

    try:
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {str(e)}")
        return None


def capture_element_screenshot(driver, element, name):
    """
    Capture a screenshot of a specific element.

    :param driver: Selenium WebDriver instance
    :param element: WebElement to capture
    :param name: Base name for the screenshot
    :return: Path to the saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{name}_element_{timestamp}.png"
    screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)

    try:
        element.screenshot(screenshot_path)
        logger.info(f"Element screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to capture element screenshot: {str(e)}")
        return None