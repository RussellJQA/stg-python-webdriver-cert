"""
The SeleniumScreenshots class interfaces with Selenium's save_screenshot()
function.
"""

from pathlib import Path

# pip installed
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumScreenshots:

    # Initializer

    def __init__(self, driver: WebDriver, screenshot_fn: str) -> None:

        self.driver: WebDriver = driver
        self.screenshot_fn: str = screenshot_fn

    def take_screenshot(self, path="screenshots") -> None:

        screenshots_fldr = Path(path)

        # Create screenshots folder (if it doesn't already exist)
        screenshots_fldr.mkdir(exist_ok=True)

        self.driver.save_screenshot(str(screenshots_fldr / self.screenshot_fn))
