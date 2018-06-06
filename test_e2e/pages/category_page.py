from typing import List
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent
from test_e2e.config import configuration

CATEGORY_URI = '/categories/{category_id}?page={page_number}'


class Using(Enum):
    PRODUCT_TITLE = 0
    COMPARE_BUTTON = 1


class CategoryPage(WebComponent):
    """
    Abstraction of the category page
    """
    PRODUCT_ROW_CSS = '[data-qa="product {product_title}"]'
    PRODUCT_TITLE_LOC = By.CSS_SELECTOR, '[data-qa=product-title]'
    PRODUCT_COMPARE_BUTTON_LOC = By.CSS_SELECTOR, '[data-qa="product-compare"]'
    PRODUCT_IMAGE_LOC = By.CSS_SELECTOR, '[data-qa="product-image"]'
    PRODUCT_SHORT_DESCRIPTION_LOC = By.CSS_SELECTOR, '[data-qa="product-short-description"]'
    PRODUCT_MIN_PRICE_LOC = By.CSS_SELECTOR, '[data-qa="product-min-price"]'
    PRODUCT_MAX_PRICE_LOC = By.CSS_SELECTOR, '[data-qa="product-max-price"]'

    def _product_row_element(self, product_title) -> WebElement:
        return self.driver.find_element_by_css_selector(self.PRODUCT_ROW_CSS.format(product_title=product_title))

    def _compare_button_element(self, product_title) -> WebElement:
        return self._product_row_element(product_title).find_element(*self.PRODUCT_COMPARE_BUTTON_LOC)

    def _product_name_element(self, product_title) -> WebElement:
        return self._product_row_element(product_title).find_element(*self.PRODUCT_TITLE_LOC)

    def _product_name_elements(self) -> List[WebElement]:
        return self.driver.find_elements(*self.PRODUCT_TITLE_LOC)

    def product_names(self) -> List[str]:
        """
        Read product names from the HTML page
        :return: list of product names
        """
        return [element.text for element in self._product_name_elements()]

    def product_short_descriptions(self) -> List[str]:
        """
        Read product short descriptions from the HTML page
        :return: list of product short descriptions
        """
        return [element.text for element in self.driver.find_elements(*self.PRODUCT_SHORT_DESCRIPTION_LOC)]

    def product_images(self) -> List[str]:
        """
        Get products' image urls from the HTML page
        :return: list of image urls
        """
        return [element.get_attribute('src') for element in self.driver.find_elements(*self.PRODUCT_IMAGE_LOC)]

    def product_min_prices(self) -> List[str]:
        """
        Read minimal prices of the products from the HTML page
        :return: list of minimal prices
        """
        return [element.text for element in self.driver.find_elements(*self.PRODUCT_MIN_PRICE_LOC)]

    def product_max_prices(self) -> List[str]:
        """
        Read maximal prices of the products from the HTML page
        :return: list of maximal prices
        """
        return [element.text for element in self.driver.find_elements(*self.PRODUCT_MAX_PRICE_LOC)]

    def go_to_product(self, product_title: str, using: Using=Using.PRODUCT_TITLE):
        """
        Go to a particular product page
        :param product_title: name of the product
        :param using: choose whether to click on the title or on the 'Compare prices' button
        """
        if using == Using.PRODUCT_TITLE:
            self._product_name_element(product_title).click()
        else:
            self._compare_button_element(product_title).click()

    def open(self, category_id: int=1, page_number: int=1):
        """
        Open the HTML page directly
        :param category_id: ID of the category
        :param page_number: page number to open
        """
        self.driver.get(
            configuration['app_url'] + CATEGORY_URI.format(category_id=category_id, page_number=page_number))
