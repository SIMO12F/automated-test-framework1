import pytest
import datetime
import subprocess

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Run pytest tests
    pytest.main([
        "-v",
        "-n", "auto",
        "--html", f"reports/report_{timestamp}.html",
        "--self-contained-html",
        "src/tests/test_api.py",
        "src/tests/test_python_org.py",
        "src/tests/test_database.py"
    ])

    # Run Behave tests
    subprocess.run(["behave", "features"])

    # Run Locust load test
    subprocess.run(
        ["locust", "-f", "src/load_tests/locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1m"])

    # Run ZAP security scan
    from src.security.zap_scan import run_zap_scan

    alerts = run_zap_scan()
    print("Security Scan Alerts:", alerts)