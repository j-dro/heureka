from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent


class Pagination(WebComponent):
    PREV_PAGE_LOC = By.CSS_SELECTOR, '[data-qa=prev-page]'
    NEXT_PAGE_LOC = By.CSS_SELECTOR, '[data-qa=next-page]'
    PAGE_LOC = By.CSS_SELECTOR, '[data-qa=page-number]'
    SPECIFIC_PAGE_CSS = '[data-qa=page-{page_number}]'

    def _prep_page_element(self) -> WebElement:
        return self.driver.find_element(*self.PREV_PAGE_LOC)

    def _next_page_element(self) -> WebElement:
        return self.driver.find_element(*self.NEXT_PAGE_LOC)

    def _page_number_element(self, page_number) -> WebElement:
        return self.driver.find_element_by_css_selector(self.SPECIFIC_PAGE_CSS.format(page_number=page_number))

    def page_numbers(self):
        """
        Returns page number that are shown in pagination component
        :return: List of page numbers
        """
        return [element.text for element in self.driver.find_elements(*self.PAGE_LOC)]

    def prev_page_is_disabled(self):
        """
        Checks whether Previous button is disabled or enabled
        :return: True is enabled, False otherwise
        """
        return 'disabled' in self._prep_page_element().get_attribute('class')

    def next_page_is_disabled(self):
        """
        Checks whether Next button is disabled or enabled
        :return: True is enabled, False otherwise
        """
        return 'disabled' in self._next_page_element().get_attribute('class')

    def go_to_prev_page(self):
        """
        Clicks on the Prev page button
        """
        self._prep_page_element().click()

    def go_to_next_page(self):
        """
        Clicks on the Next page button
        """
        self._next_page_element().click()

    def go_to_page(self, page_number: int):
        """
        Clicks on a particular page number
        :param page_number: page number to click on
        """
        self._page_number_element(page_number).click()
