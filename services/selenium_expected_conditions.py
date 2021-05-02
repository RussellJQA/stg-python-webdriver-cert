"""
This module contains some functions related to selenium.webdriver.support's
expected_conditions module.
"""

# pip installed

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

WAIT_TIME = 10  # Time (in seconds) for Selenium to wait for expected condition


def wait_for_element_to_be_clickable(start_element, element_to_be_located):
    WebDriverWait(start_element, WAIT_TIME).until(
        EC.element_to_be_clickable(element_to_be_located))


def is_web_driver_version_ge_4():
    major_version_num = int(
        webdriver.__version__[0:webdriver.__version__.find(".")])
    return major_version_num >= 4


# The any_of() and none_of functions from expected_conditions are not in
# Selenium until the Selenium 4 beta. So I've copied the source
# (and license information) below from:
# https://www.selenium.dev/selenium/docs/api/py/_modules/selenium/webdriver/support/expected_conditions.html

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


def any_of(*expected_conditions):
    """ An expectation that any of multiple expected conditions is true.
    Equivalent to a logical 'OR'.
    Returns results of the first matching condition, or False if none do. """

    # If the installed version of Selenium WebDriver is >= 4,
    # then just directly use its implementation of this function.
    if is_web_driver_version_ge_4():
        return EC.any_of(*expected_conditions)

    # Otherwise, use the (snapshot) copy of it from the Selenium 4 beta, below.

    def any_of_condition(driver):
        for expected_condition in expected_conditions:
            try:
                result = expected_condition(driver)
                if result:
                    return result
            except WebDriverException:
                pass
        return False

    return any_of_condition


def none_of(*expected_conditions):
    """ An expectation that none of 1 or multiple expected conditions is true.
    Equivalent to a logical 'NOT-OR'.
    Returns a Boolean """

    # If the installed version of Selenium WebDriver is >= 4,
    # then just directly use its implementation of this function.
    if is_web_driver_version_ge_4():
        return EC.none_of(*expected_conditions)

    # Otherwise, use the (snapshot) copy of it from the Selenium 4 beta, below.

    def none_of_condition(driver):
        for expected_condition in expected_conditions:
            try:
                result = expected_condition(driver)
                if result:
                    return False
            except WebDriverException:
                pass
        return True

    return none_of_condition