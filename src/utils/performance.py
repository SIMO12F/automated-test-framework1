import time
from functools import wraps
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.logger import logger

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {execution_time:.2f} seconds to execute")
        return result
    return wrapper

def log_test_step(step_description):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Executing: {step_description}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def measure_page_load_time(driver):
    navigation_start = driver.execute_script("return performance.timing.navigationStart")
    load_event_end = driver.execute_script("return performance.timing.loadEventEnd")

    # If loadEventEnd is 0, it means the page load hasn't completed yet
    if load_event_end == 0:
        # Wait for a short time and try again
        time.sleep(1)
        load_event_end = driver.execute_script("return performance.timing.loadEventEnd")

    load_time = (load_event_end - navigation_start) / 1000  # Convert to seconds
    logger.info(f"Page load time: {load_time:.2f} seconds")
    return load_time

def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        logger.warning(f"Error waiting for AJAX: {str(e)}")

def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.element_to_be_clickable(locator))
        return element
    except TimeoutException:
        logger.error(f"Element not clickable: {locator}")
        return None

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts. Error: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator