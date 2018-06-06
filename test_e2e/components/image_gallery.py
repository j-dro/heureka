from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_e2e.components.web_component import WebComponent


class ImageGallery(WebComponent):
    """
    Abstraction of image gallery
    """
    BUTTON_CLOSE_LOC = By.CSS_SELECTOR, '[data-qa=gallery-button-close]'
    GALLERY_MODAL_LOC = By.CSS_SELECTOR, '[data-qa=gallery-modal]'
    IMAGE_LOC = By.CSS_SELECTOR, '[data-qa=gallery-image]'
    PREV_IMAGE_BUTTON_LOC = By.CSS_SELECTOR, '[data-qa=gallery-prev-image]'
    NEXT_IMAGE_BUTTON_LOC = By.CSS_SELECTOR, '[data-qa=gallery-next-image]'

    def _image_elements(self) -> List[WebElement]:
        return self.driver.find_elements(*self.IMAGE_LOC)

    def is_visible(self) -> bool:
        """
        Check the HTML page whether the gallery is open
        :return: True if gallery is visible, False otherwise
        """
        return self.driver.find_element(*self.GALLERY_MODAL_LOC).is_displayed()

    def visible_images(self) -> str:
        """
        Checks which images of the gallery are visible in the HTML page
        :return: List of urls of visible images in the gallery
        """
        images = []
        for image_element in self._image_elements():
            if image_element.is_displayed():
                images.append(image_element.get_attribute('src'))
        return images

    def go_to_prev_image(self):
        """
        Clicks on the Previous image button
        """
        self.driver.find_element(*self.PREV_IMAGE_BUTTON_LOC).click()

    def go_to_next_image(self):
        """
        Clicks on the Next image button
        """
        self.driver.find_element(*self.NEXT_IMAGE_BUTTON_LOC).click()

    def close(self):
        """
        Closes the gallery
        """
        self.driver.find_element(*self.BUTTON_CLOSE_LOC).click()
