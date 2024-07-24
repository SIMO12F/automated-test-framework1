from selenium.webdriver.common.by import By

class ExamplePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example.com"

    def navigate(self):
        self.driver.get(self.url)

    def get_title(self):
        return self.driver.title

    def get_heading(self):
        return self.driver.find_element(By.TAG_NAME, "h1").text

    def get_paragraph(self):
        return self.driver.find_element(By.TAG_NAME, "p").text