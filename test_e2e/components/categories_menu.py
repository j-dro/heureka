from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent


class CategoriesMenu(WebComponent):
    """
    Abstraction of the Categories sidebar
    """
    MENU_ITEM_LOC = By.CSS_SELECTOR, '[data-qa=categories-menu-item-title]'

    def _category_names_elements(self) -> List[WebElement]:
        return self.driver.find_elements(*self.MENU_ITEM_LOC)

    def category_names(self) -> List[str]:
        """
        Get names of listed categories in the category sidebar
        :return: List of names
        """
        return [element.text for element in self._category_names_elements()]

    def go_to_category(self, category_title: str):
        """
        Clicks on the category
        :param category_title: name of the category to go to
        """
        for element in self._category_names_elements():
            if element.text == category_title:
                element.click()
                break
        else:
            Exception('Category not found: ' + category_title)
