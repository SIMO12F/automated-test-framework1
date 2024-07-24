import pytest
import os
import sys
from datetime import datetime
from src.config import Config
from src.logger import logger

def setup_environment():
    """Set up the test environment."""
    # Ensure necessary directories exist
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs(Config.get_log_dir(), exist_ok=True)

def get_pytest_args():
    """Generate pytest arguments."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(Config.REPORT_DIR, f"test_report_{timestamp}.html")

    args = [
        "-v",
        f"--html={report_file}",
        "--self-contained-html",
        "--capture=tee-sys",
        f"--log-file={Config.LOG_FILE}",
        f"--log-file-level={Config.LOG_LEVEL}",
        "src/tests"
    ]

    if Config.PARALLEL_EXECUTION:
        args.extend(["-n", "auto"])

    return args

def main():
    logger.info("Starting test execution")
    logger.info(f"Running tests in {Config.ENVIRONMENT} environment")
    logger.info(f"Browser: {Config.BROWSER}")
    logger.info(f"Headless mode: {'Enabled' if Config.HEADLESS else 'Disabled'}")
    logger.info(f"Base URL: {Config.get_base_url()}")
    logger.info(f"API Base URL: {Config.get_api_base_url()}")

    setup_environment()

    pytest_args = get_pytest_args()
    logger.info(f"Running tests with arguments: {pytest_args}")

    exit_code = pytest.main(pytest_args)

    logger.info(f"Test execution completed with exit code: {exit_code}")

    if exit_code == 0:
        logger.info("All tests passed successfully")
    elif exit_code == 1:
        logger.warning("Some tests failed")
    elif exit_code == 2:
        logger.error("Test execution was interrupted by the user")
    elif exit_code == 3:
        logger.error("Internal error occurred in pytest")
    elif exit_code == 4:
        logger.error("pytest command line usage error")
    elif exit_code == 5:
        logger.error("No tests were collected")

    logger.info(f"Test report generated at: {os.path.join(Config.REPORT_DIR, 'test_report_*.html')}")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())