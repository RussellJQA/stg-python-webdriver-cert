"""
This module contains a class which interfaces with Selenium's save_screenshot()
function.
"""

from pathlib import Path


class SeleniumScreenshots:

    # Initializer

    def __init__(self, driver, screenshot_fn):
        self.driver = driver
        self.screenshot_fn = screenshot_fn

    def take_screenshot(self, path="screenshots"):
        screenshots_fldr = Path(path)
        # Create screenshots folder (if it doesn't already exist)
        screenshots_fldr.mkdir(exist_ok=True)
        self.driver.save_screenshot(str(screenshots_fldr / self.screenshot_fn))