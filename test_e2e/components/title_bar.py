from selenium.webdriver.common.by import By
from test_e2e.components.web_component import WebComponent


class TitleBar(WebComponent):
    HOME_LOC = By.CSS_SELECTOR, '[data-qa=home]'

    def go_home(self):
        """
        Clicks on title bar
        """
        self.driver.find_element(*self.HOME_LOC).click()
