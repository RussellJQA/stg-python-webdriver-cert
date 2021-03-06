# STG Python/WebDriver Certification - Level 1 Challenges

This repository contains my solutions to the Level 1 challenges specified
in Carlos Kidman's [Python WebDriver STG Certification: Level 1 & 2](https://github.com/ElSnoMan/python-stg-cert-one) repository.

They are written using Python, pytest (with the pytest-check plugin), and the Python bindings for Selenium WebDriver.

## Setup Instructions:

1. Download Python 3.7 or higher from [python.org](https://www.python.org/downloads/), and install it
2. Clone this repository to a folder on your computer
3. Set your working directory to the folder where you cloned this repository
4. Optionally: Create and activate a virtual environment in that folder
5. Within that folder, install this repository's dependencies, by typing:

   <pre>pip install -r requirements.txt</pre>

That installs the following Python packages, along with their dependencies:

- [pytest:](https://pypi.org/project/pytest/) a Python testing framework
  - Because pytest is a dependency of pytest-check (below), it would be installed even if it was omitted from requirements.txt.
  - But it's been included in requirements.txt to make its use explicit.
- [pytest-check:](https://pypi.org/project/pytest-check/) a pytest plugin that allows multiple failures per test
- [python-dotenv:](https://pypi.org/project/python-dotenv/) reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the [12-factor](https://12factor.net/) principles. [Factor 3 is "Store configuration in the environment."]
- [selenium:](https://pypi.org/project/selenium/) the Python bindings for Selenium WebDriver
- [webdriver-manager:](https://pypi.org/project/webdriver-manager/) manages WebDriver installs, so you don't have to

## Implementation Notes

1. This code has been tested (using virtual environments) with both Python 3.7.9 and Python 3.9.5, using the Chrome browser in Windows 8.1 Professional.

2. This code uses the [webdriver_manager](https://pypi.org/project/webdriver-manager/) package to simplify managing WebDriver instances for different browsers.

3. This code uses soft, non-blocking (delayed) asserts -- as implemented in Brian Okken's [pytest-check](https://pypi.org/project/pytest-check/) pytest plugin -- to handle the multiple assert() statements in test challenges 4 and 7. See [Non Blocking Assertion Failures with Pytest-check](https://blog.testproject.io/2020/08/11/non-blocking-assertion-failures-with-pytest-check/).

4. Several of the test challenges use Python 3's print() function. For example, test challenge 3 prints the name of each Make or Model from Copart.com's Most Popular Items section, along with its URL, as in:
   <pre>SILVERADO - https://www.copart.com/popular/model/silverado</pre>
   Because pytest captures stdout/stderr by default, in order to see this output, you'll need to run pytest with the "-s" (or "-rP") parameter, as in:
   <pre><code>pytest challenges\test_challenge3.py -s</code></pre>
   If you're running pytest through VS Code, you can instead enable "-s" for all the test challenges. To do that, include "-s" as an argument to pytest in a VS Code settings file for this repository. In Windows, this file is (relative to this repository) in .vscode\settings.json.\
   \
   That's what I have done. So, for your information, I've included a copy of my .vscode\settings.json file below:
   ```
   {
      "python.testing.pytestArgs": [
         "challenges",
         "-s"
      ],
      "python.testing.unittestEnabled": false,
      "python.testing.nosetestsEnabled": false,
      "python.testing.pytestEnabled": true,
      "python.testing.autoTestDiscoverOnSaveEnabled": false,
      "editor.formatOnSave": true
   }
   ```
