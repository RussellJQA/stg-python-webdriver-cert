"""
This module implements some pytest fixtures for use with Selenium WebDriver.
"""

# pip installed

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver() -> WebDriver:

    # Setup: Code before the 'yield' statement is run before each test

    driver = webdriver.Chrome(ChromeDriverManager().install(
    ))  # Install and initialize Chrome WebDriver for Selenium

    driver.maximize_window()

    yield driver

    # Cleanup/Teardown: Code after the 'yield' statement is run after each test

    driver.quit()


@pytest.fixture
def wait(driver: WebDriver) -> WebDriverWait:
    """ WebDriverWait allows us to wait until a condition is True.

    For example, wait until an element is displayed
    """
    # timeout is the max number of seconds to wait for.
    return WebDriverWait(driver, timeout=10)
