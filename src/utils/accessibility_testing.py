from axe_selenium_python import Axe
from src.config import Config
from src.logger import logger

def run_accessibility_test(driver, name):
    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    violations = results["violations"]
    logger.info(f"Accessibility test for {name}: Found {len(violations)} violations")

    for violation in violations:
        logger.warning(f"Violation: {violation['id']} - {violation['description']}")
        logger.warning(f"Impact: {violation['impact']}")
        logger.warning(f"Help: {violation['help']}")
        logger.warning(f"Help URL: {violation['helpUrl']}")

    if Config.GENERATE_ACCESSIBILITY_REPORT:
        report_path = Config.REPORT_DIR / f"accessibility_report_{name}.html"
        axe.write_results(results, report_path)
        logger.info(f"Accessibility report generated: {report_path}")

    return violations