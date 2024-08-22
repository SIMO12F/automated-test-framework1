import pytest
from src.utils.database import setup_database, teardown_database, add_user, get_user
from src.utils.performance import measure_time, log_test_step

@pytest.fixture(scope="module")
def setup_teardown_database():
    setup_database()
    yield
    teardown_database()

@measure_time
@log_test_step("Testing user addition to database")
def test_add_user(setup_teardown_database):
    add_user("John Doe", "john@example.com")
    user = get_user(1)
    assert user is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

@measure_time
@log_test_step("Testing user retrieval from database")
def test_get_user(setup_teardown_database):
    add_user("Jane Doe", "jane@example.com")
    user = get_user(2)
    assert user is not None
    assert user.name == "Jane Doe"
    assert user.email == "jane@example.com"