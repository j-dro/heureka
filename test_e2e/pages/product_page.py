from enum import Enum
from typing import List
from test_e2e.config import configuration
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent

PRODUCT_URI = '/products/{product_id}'


class ProductTabs(Enum):
    PRODUCT_COMPARISON = 0
    PRODUCT_SPECIFICATION = 1


class ProductPage(WebComponent):
    """
    Abstraction of the Product page
    """
    PRODUCT_TITLE_LOC = By.CSS_SELECTOR, '[data-qa=product-title]'
    PRODUCT_SHORT_DESCRIPTION_LOC = By.CSS_SELECTOR, '[data-qa=product-short-description]'
    PRODUCT_DESCRIPTION_LOC = By.CSS_SELECTOR, '[data-qa=product-description]'
    PRODUCT_NAVIGATION_LOC = By.CSS_SELECTOR, '[data-qa=product-navigation]'
    PRODUCT_MAIN_IMAGE_LOC = By.CSS_SELECTOR, '[data-qa=product-main-image]'
    PRODUCT_SMALL_IMAGE_LOC = By.CSS_SELECTOR, '[data-qa=product-small-image]'
    PRODUCT_COMPARISON_PANE_LOC = By.CSS_SELECTOR, '[data-qa=product-comparison]'
    PRODUCT_SPECIFICATION_PANE_LOC = By.CSS_SELECTOR, '[data-qa=product-specification]'
    PRODUCT_OFFER_LOC = By.CSS_SELECTOR, '[data-qa=product-offer]'
    SHOP_NAME_LOC = By.CSS_SELECTOR, '[data-qa=shop-name]'
    PRODUCT_BUY_BUTTON_LOC = By.CSS_SELECTOR, '[data-qa=product-buy-button]'
    PRODUCT_PRICE_LOC = By.CSS_SELECTOR, '[data-qa=product-price]'
    BUTTON_SHOW_REMAINING_LOC = By.CSS_SELECTOR, '[data-qa=button-show-remaining]'
    PRODUCT_TABS_LOC = {
        ProductTabs.PRODUCT_SPECIFICATION: (By.CSS_SELECTOR, '[data-qa=product-spec-tab]'),
        ProductTabs.PRODUCT_COMPARISON: (By.CSS_SELECTOR, '[data-qa=product-comparison-tab]'),
    }
    PRODUCT_GALLERY_BUTON_LOC = By.CSS_SELECTOR, '[data-qa=gallery-button]'

    def _product_visible_offer_elements(self) -> List[WebElement]:
        return [element for element in self.driver.find_elements(*self.PRODUCT_OFFER_LOC) if element.is_displayed()]

    def product_description(self) -> str:
        """
        Read the product description from the HTML page
        :return: product description
        """
        return self.driver.find_element(*self.PRODUCT_DESCRIPTION_LOC).text

    def product_name(self) -> str:
        """
        Read the product name from the HTML page
        :return: product name
        """
        return self.driver.find_element(*self.PRODUCT_TITLE_LOC).text

    def product_short_description(self) -> str:
        """
        Read the product short description next to the image from the HTML page
        :return: product short description
        """
        return self.driver.find_element(*self.PRODUCT_SHORT_DESCRIPTION_LOC).text

    def product_navigation_text(self) -> str:
        """
        Read the product breadcrumbs navigation text from the HTML page
        :return: product breadcrumbs text
        """
        return self.driver.find_element(*self.PRODUCT_NAVIGATION_LOC).text

    def product_main_image(self) -> str:
        """
        Get the main product's image url from the HTML page
        :return: url of the image
        """
        return self.driver.find_element(*self.PRODUCT_MAIN_IMAGE_LOC).get_attribute('src')

    def product_small_images(self) -> List[str]:
        """
        Get the product's small images urls from the HTML page
        :return: List urls of the images
        """
        return [element.get_attribute('src') for element in self.driver.find_elements(*self.PRODUCT_SMALL_IMAGE_LOC)]

    def product_comparison_is_visible(self) -> bool:
        """
        Checks whther product comparison tab content is visible to user
        :return: True if visible, False otherwise
        """
        return self.driver.find_element(*self.PRODUCT_COMPARISON_PANE_LOC).is_displayed()

    def product_specification_is_visible(self) -> bool:
        """
        Checks whther product specification tab content is visible to user
        :return: True if visible, False otherwise
        """
        return self.driver.find_element(*self.PRODUCT_SPECIFICATION_PANE_LOC).is_displayed()

    def product_visible_offers(self) -> List[List[str]]:
        """
        Read offers that are shown in the HTML page
        :return: List of offers - shop name, url to the product in the shop, price
        """
        offers = []
        offer_elements = self._product_visible_offer_elements()
        for offer in offer_elements:
            shop_name = offer.find_element(*self.SHOP_NAME_LOC).text
            product_in_shop_url = offer.find_element(*self.PRODUCT_BUY_BUTTON_LOC).get_attribute('href')
            price = offer.find_element(*self.PRODUCT_PRICE_LOC).text
            offers.append([shop_name, product_in_shop_url, price])
        return offers

    def show_remaining_offers(self):
        """
        Click on the button to show remaining offers
        """
        self.driver.find_element(*self.BUTTON_SHOW_REMAINING_LOC).click()

    def show_tab(self, tab: ProductTabs):
        """
        Switch to a tab
        :param tab: specifies which tab to switch to - product price comparison or specification
        """
        self.driver.find_element(*self.PRODUCT_TABS_LOC[tab]).click()

    def show_gallery(self):
        """
        Show image gallery - click on the Gallery button
        """
        self.driver.find_element(*self.PRODUCT_GALLERY_BUTON_LOC).click()

    def open(self, product_id: int):
        """
        Open the HTML product page directly
        :param product_id: ID of the product
        """
        self.driver.get(configuration['app_url'] + PRODUCT_URI.format(product_id=product_id))
