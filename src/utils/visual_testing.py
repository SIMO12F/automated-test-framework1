import os
from PIL import Image, ImageChops
from src.logger import logger
from src.config import Config

def capture_screenshot(driver, name):
    """
    Take a screenshot and save it to the screenshots directory.

    :param driver: Selenium WebDriver instance
    :param name: Name of the screenshot
    :return: Path to the saved screenshot
    """
    screenshot_path = os.path.join(Config.SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    logger.info(f"Screenshot saved: {screenshot_path}")
    return screenshot_path

def compare_images(baseline_path, current_path, diff_path, threshold=Config.VISUAL_DIFF_THRESHOLD):
    """
    Compare two images and generate a diff image if they're different.

    :param baseline_path: Path to the baseline image
    :param current_path: Path to the current image
    :param diff_path: Path to save the diff image
    :param threshold: Threshold for considering images different
    :return: True if images are similar, False otherwise
    """
    logger.info(f"Comparing images: Baseline: {baseline_path}, Current: {current_path}")
    if not os.path.exists(baseline_path):
        logger.warning(f"Baseline image does not exist: {baseline_path}")
        return False
    if not os.path.exists(current_path):
        logger.warning(f"Current image does not exist: {current_path}")
        return False

    with Image.open(baseline_path) as baseline_img, Image.open(current_path) as current_img:
        if baseline_img.size != current_img.size:
            logger.warning(f"Image size mismatch: Baseline {baseline_img.size}, Current {current_img.size}")
            return False

        diff = ImageChops.difference(baseline_img, current_img)
        diff_pixels = diff.getbbox()
        if diff_pixels:
            diff_count = sum(diff.convert("L").getdata())
            logger.info(f"Difference count: {diff_count}, Threshold: {threshold}")
            if diff_count > threshold:
                diff.save(diff_path)
                logger.warning(f"Visual difference detected. Diff saved: {diff_path}")
                return False
        logger.info("Visual test passed: No significant differences detected")
        return True