import os
from datetime import datetime
from src.config import Config

def capture_screenshot(driver, name):
    screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), Config.SCREENSHOT_DIR)
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)
    driver.save_screenshot(screenshot_path)
    return screenshot_path