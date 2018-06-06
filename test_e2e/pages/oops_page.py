from selenium.webdriver.common.by import By
from test_e2e.config import configuration
from test_e2e.components.web_component import WebComponent


class OopsPage(WebComponent):
    """
    Abstraction of the HTML error page
    """
    TITLE_LOC = By.CSS_SELECTOR, '[data-qa=title]'
    TEXT_LOC = By.CSS_SELECTOR, '[data-qa=text]'
    SUGGESTION_LOC = By.CSS_SELECTOR, '[data-qa=suggestion]'
    BUTTON_LOC = By.CSS_SELECTOR, '[data-qa=button]'

    def open_404_page(self):
        """
        Open 404 page directly by using non-existent path
        :return:
        """
        self.driver.get(configuration['app_url'] + '/nonsense')

    def title(self) -> str:
        """
        Read the title from the HTML page
        :return: title of the page
        """
        return self.driver.find_element(*self.TITLE_LOC).text

    def text(self) -> str:
        """
        Read the text of the error from the HTML page
        :return: error text of the page
        """
        return self.driver.find_element(*self.TEXT_LOC).text

    def suggestion_text(self) -> str:
        """
        Read the suggestion from HTML page
        :return: suggestion to user
        """
        return self.driver.find_element(*self.SUGGESTION_LOC).text

    def button_text(self) -> str:
        """
        Read the text of the button from the HTML page
        :return: button text
        """
        return self.driver.find_element(*self.BUTTON_LOC).text
