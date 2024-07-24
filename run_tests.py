import pytest
import os
from datetime import datetime
from src.config import Config
from src.logger import logger


def main():
    logger.info("Starting test execution")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Config.get_report_dir()
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_file = os.path.join(report_dir, f"test_report_{timestamp}.html")

    pytest_args = [
        "-v",
        f"--html={report_file}",
        "--self-contained-html",
        "src/tests"
    ]

    if Config.PARALLEL_EXECUTION:
        pytest_args.extend(["-n", "auto"])

    if Config.RUN_UI_TESTS:
        pytest_args.append("src/tests/test_search.py")
        pytest_args.append("src/tests/test_example.py")

    if Config.RUN_API_TESTS:
        pytest_args.append("src/tests/test_api.py")

    logger.info(f"Running tests with arguments: {pytest_args}")
    logger.info(f"Browser: {Config.BROWSER}")
    logger.info(f"Headless mode: {'Enabled' if Config.HEADLESS else 'Disabled'}")
    logger.info(f"Base URL: {Config.get_base_url()}")
    logger.info(f"API Base URL: {Config.API_BASE_URL}")

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

    logger.info(f"Test report generated at: {report_file}")

    return exit_code


if __name__ == "__main__":
    main()