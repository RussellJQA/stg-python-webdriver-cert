"""
This module implements some pytest fixtures for use with Selenium WebDriver.
"""
import os
import time

import pytest
# pip installed
from dotenv import find_dotenv, load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver() -> WebDriver:
    # Setup: Code before the 'yield' statement is run before each test

    driver: Chrome = Chrome(ChromeDriverManager().install(
    ))  # Install and initialize Chrome WebDriver for Selenium

    driver.maximize_window()

    yield driver

    # Cleanup/Teardown: Code after the 'yield' statement is run after each test

    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    seconds_to_sleep_before_webdriver_quit = int(
        os.environ.get("SECONDS_TO_SLEEP_BEFORE_WEBDRIVER_QUIT", "0"))

    # Only do this when the corresponding environment variable has specifically been set to enable it
    # [as for development or demonstration purposes --
    #  to allow (during test execution) the then current Web page to be observed].
    if seconds_to_sleep_before_webdriver_quit:
        time.sleep(seconds_to_sleep_before_webdriver_quit)

    driver.quit()


@pytest.fixture
def wait(driver: WebDriver) -> WebDriverWait:
    """ WebDriverWait allows us to wait until a condition is True.

    For example, wait until an element is displayed
    """

    return WebDriverWait(driver, timeout=10)  # timeout is the max number of seconds to wait for.
