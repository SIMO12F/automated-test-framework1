import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.example_page import ExamplePage

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_example_page_title(browser):
    page = ExamplePage(browser)
    page.navigate()
    assert "Example Domain" in page.get_title()

def test_example_page_heading(browser):
    page = ExamplePage(browser)
    page.navigate()
    assert page.get_heading() == "Example Domain"

def test_example_page_paragraph(browser):
    page = ExamplePage(browser)
    page.navigate()
    assert "for use in illustrative examples in documents" in page.get_paragraph()