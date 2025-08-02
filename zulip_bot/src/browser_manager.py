from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class BrowserManager:
    """
    Manages the Selenium Chrome WebDriver instance.
    Supports headless and visible modes, sets recommended options for stability.
    """
    def __init__(self, wait_time=15, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless=new")  # Use new headless mode
            options.add_argument("--window-size=1920,1080")  # Set window size for headless
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.wait = WebDriverWait(self.driver, wait_time)

    def quit(self):
        if self.driver:
            self.driver.quit()