import os
import daiquiri
from test_e2e.config import configuration
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

logger = daiquiri.getLogger(__name__)

BROWSERSTACK_DOMAIN = 'browserstack.com'
DEFAULT_SELENIUM_TIMEOUT_SEC = 20


SCREENSHOTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'screenshots')


def start_browser(test_name: str) -> Remote:
    """
    Start browser - either using local/remote selenium or using browserstack platform
    :param test_name: name of the test - will be shown in Browserstack
    """
    logger.info('Starting browser')

    remote_driver_url = configuration['remote_driver_url']

    if BROWSERSTACK_DOMAIN not in remote_driver_url:
        # we are running locally, chrome for simplicity
        desired_cap = DesiredCapabilities.CHROME
    else:
        # we are using browserstack, chrome for simplicity
        desired_cap = {
            'os': 'OS X',
            'os_version': 'High Sierra',
            'browser': 'chrome',
            'resolution': '1920x1080',
            'name': test_name,
            'browserstack.selenium_version': '3.11.0'
        }

    driver = Remote(command_executor=remote_driver_url,
                    desired_capabilities=desired_cap)

    driver.implicitly_wait(DEFAULT_SELENIUM_TIMEOUT_SEC)
    driver.set_window_size(1920, 1080)
    return driver


def stop_browser(driver: Remote):
    """
    Stop browser
    :param driver: WebDriver object
    """
    logger.info('Tearing down browser')
    driver.quit()
    del driver


def save_screenshot(driver: Remote, screenshot_name: str):
    """
    Save screenshot from the browser
    :param driver: WebDriver object
    :param screenshot_name: filename of the screenshot without path
    """
    logger.info('Saving screenshot')
    os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
    try:
        driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, screenshot_name))
    except WebDriverException as e:
        logger.error('Failed to save screenshot:')
        logger.error(e)
