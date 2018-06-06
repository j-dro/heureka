from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent
from test_e2e.config import configuration


class HomePage(WebComponent):
    """
    Abstraction of the home page
    """
    CATEGORIES_GRID_ITEM_TITLE_LOC = By.CSS_SELECTOR, '[data-qa=categories-grid-item-title]'

    def _grid_category_names_elements(self) -> List[WebElement]:
        return self.driver.find_elements(*self.CATEGORIES_GRID_ITEM_TITLE_LOC)

    def grid_category_names(self) -> List[str]:
        """
        Read category names from the category grid in the HTML page
        :return: list of category names
        """
        return [element.text for element in self._grid_category_names_elements()]

    def go_to_category(self, category_title: str):
        """
        Click on the category in the category grid
        :param category_title: Name of the category
        """
        for element in self._grid_category_names_elements():
            if element.text == category_title:
                element.click()
                break
        else:
            Exception('Category not found: ' + category_title)

    def open(self):
        """
        Open the home page in the browser
        """
        self.driver.get(configuration['app_url'])
