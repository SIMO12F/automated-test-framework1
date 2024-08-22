import os
import platform
import requests
import zipfile
import io

# Define the ChromeDriver URL for Chrome version 127.0.6533.100
chrome_version = '127.0.6533.100'
chrome_driver_version = '127.0.6533.100'  # Use the correct driver version matching Chrome version
chrome_driver_url = f'https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_win32.zip'


# Detect system architecture
def get_system_architecture():
    if platform.architecture()[0] == '64bit':
        return '64-bit'
    else:
        return '32-bit'


# Download and extract ChromeDriver
def download_and_extract(url, driver_name):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(driver_name)
    else:
        raise Exception(f"Failed to download {driver_name} from {url}")


# Replace ChromeDriver executable
def replace_chromedriver():
    architecture = get_system_architecture()
    if architecture == '64-bit':
        driver_name = 'chromedriver_win32'
    else:
        driver_name = 'chromedriver_win32'

    url = chrome_driver_url
    print(f"Downloading and replacing ChromeDriver for {architecture}...")
    download_and_extract(url, driver_name)
    print(f"ChromeDriver updated successfully!")


# Main function to update ChromeDriver
def update_chromedriver():
    replace_chromedriver()


if __name__ == '__main__':
    update_chromedriver()
