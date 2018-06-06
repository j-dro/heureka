from selenium.webdriver import Remote
from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIMEOUT_SEC = 3


class WebComponent:
    """
    Base class for components objects and page objects
    """
    def __init__(self, driver: Remote):
        self.driver = driver

    def page_title(self) -> str:
        """
        Get page title of the HTML page
        :return: page title
        """
        return self.driver.title

    def wait_until(self, func_condition: (), timeout_sec: int=WAIT_TIMEOUT_SEC):
        """ Waits until the condition is met, raises TimeoutException otherwise
        :param func_condition: condition function which returns bool
        :param timeout_sec: how long to wait
        :return: the value of func_condition() if condition is met
        """
        return WebDriverWait(self.driver, timeout_sec).until(lambda driver: func_condition())
