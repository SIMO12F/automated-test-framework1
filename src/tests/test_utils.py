import pytest
import os
from src.utils.accessibility_testing import run_accessibility_test
from src.utils.database import setup_database, teardown_database, add_user, get_user
from src.utils.visual_testing import capture_screenshot, compare_images
from src.utils.data_loader import load_csv_data, load_json_data
from src.utils.performance import measure_time, log_test_step
from src.config import Config


@pytest.fixture(scope="module")
def setup_teardown_db():
    setup_database()
    yield
    teardown_database()


@measure_time
@log_test_step("Testing accessibility")
def test_accessibility(driver):
    driver.get(Config.BASE_URL)
    violations = run_accessibility_test(driver, "homepage")
    assert len(violations) == 0, f"Found {len(violations)} accessibility violations"


@measure_time
@log_test_step("Testing database operations")
def test_database(setup_teardown_db):
    add_user("Test User", "test@example.com")
    user = get_user(1)
    assert user.name == "Test User"
    assert user.email == "test@example.com"


@measure_time
@log_test_step("Testing visual comparison")
def test_visual_testing(driver):
    driver.get(Config.BASE_URL)
    screenshot_path = capture_screenshot(driver, "homepage")
    assert os.path.exists(screenshot_path)

    baseline_path = os.path.join(Config.SCREENSHOT_DIR, "baseline_homepage.png")
    if not os.path.exists(baseline_path):
        driver.save_screenshot(baseline_path)
        pytest.skip("Baseline image created. Run the test again for comparison.")

    result = compare_images(baseline_path, screenshot_path, os.path.join(Config.SCREENSHOT_DIR, "diff_homepage.png"))
    assert result, "Visual difference detected"


@measure_time
@log_test_step("Testing data loader")
def test_data_loader():
    # Create sample CSV and JSON files in the test_data directory
    csv_content = "name,age\nAlice,30\nBob,25"
    json_content = '{"users": [{"name": "Charlie", "age": 35}, {"name": "David", "age": 28}]}'

    csv_path = os.path.join(Config.TEST_DATA_DIR, "sample.csv")
    json_path = os.path.join(Config.TEST_DATA_DIR, "sample.json")

    with open(csv_path, "w") as f:
        f.write(csv_content)
    with open(json_path, "w") as f:
        f.write(json_content)

    csv_data = load_csv_data("sample.csv")
    json_data = load_json_data("sample.json")

    assert len(csv_data) == 2
    assert csv_data[0]["name"] == "Alice"
    assert len(json_data["users"]) == 2
    assert json_data["users"][0]["name"] == "Charlie"

    # Clean up
    os.remove(csv_path)
    os.remove(json_path)


if __name__ == "__main__":
    pytest.main(["-v", __file__])