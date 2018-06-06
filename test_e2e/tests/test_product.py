from time import sleep
import pytest
from test_e2e.pages.product_page import ProductPage, ProductTabs
from test_e2e.components.image_gallery import ImageGallery


@pytest.mark.usefixtures('start_browser')
class TestProduct:
    def test_product_with_images(self):
        """
        Test product page content on the product with images
        """

        expected_product_short_description = \
            'Mi niekto niečo tak Bublina si všetko ako toto som ako Bublina do paže ako keby dojebal to robil keď by ' \
            'si niekto boršč? No ako keby oné hento ale nemám Internet. No ako keby dojebal oné. Počkaj do paže keby ' \
            'dojebal oné. Čo ja? Tak oné či čo som ako ... Celá specifikace'

        expected_product_description = \
            'Mi niekto niečo tak Bublina si všetko ako toto som ako Bublina do paže ako keby dojebal to robil keď by ' \
            'si niekto boršč? No ako keby oné hento ale nemám Internet. No ako keby dojebal oné. Počkaj do paže keby ' \
            'dojebal oné. Čo ja? Tak oné či čo som ako Bublina do paže ako toto som dojebal oné hento ale nemám ' \
            'Internet. Kupi mi niekto boršč? Tak oné hento oné hento ale nemám nič. Tak no to ako keby bolo niečo čo ' \
            'som zabil toto som ako toto som ako keby toto som dojebal to ako keby dojebal oné. Da mi niekto niečo.'

        expected_product_main_image = 'https://im9.cz/iR/importprodukt-orig/cf2/cf292a2388aa9598b948794a47705a92.jpg'

        expected_product_small_images = [
            'https://im9.cz/iR/importprodukt-orig/719/719cbb7f53feee082aa6a0e91a35a3c9.jpg'
        ] * 3

        expected_product_offers = [
            ['randomEshop8179', 'http://randomeshop8179.cz/product/91433', '31729'],
            ['randomEshop37350', 'http://randomeshop37350.cz/product/13073', '31818'],
            ['randomEshop97740', 'http://randomeshop97740.cz/product/38684', '32250'],
            ['randomEshop56728', 'http://randomeshop56728.cz/product/34459', '32287'],
            ['randomEshop70514', 'http://randomeshop70514.cz/product/50166', '33619'],
            ['randomEshop62282', 'http://randomeshop62282.cz/product/96327', '33888'],
            ['randomEshop72900', 'http://randomeshop72900.cz/product/71403', '34384'],
            ['randomEshop88941', 'http://randomeshop88941.cz/product/46861', '34630'],
            ['randomEshop13974', 'http://randomeshop13974.cz/product/35048', '35224'],
            ['randomEshop25854', 'http://randomeshop25854.cz/product/7769', '37019'],
            ['randomEshop15083', 'http://randomeshop15083.cz/product/6276', '37033'],
            ['randomEshop47361', 'http://randomeshop47361.cz/product/84992', '37055']
        ]

        product_page = ProductPage(self.driver)
        product_page.open(3)

        # Check product info and images
        assert product_page.product_name() == 'Apple iPHone 5S'
        assert product_page.product_navigation_text() == 'Mobilní telefony >> Apple iPHone 5S'
        assert product_page.product_short_description() == expected_product_short_description
        assert product_page.product_main_image() == expected_product_main_image
        assert product_page.product_small_images() == expected_product_small_images

        # Check tabs visibility
        assert product_page.product_comparison_is_visible() is True
        assert product_page.product_specification_is_visible() is False

        # At first only first three offers are shown
        assert product_page.product_visible_offers() == expected_product_offers[0:3]
        # Then all offers are revealed
        product_page.show_remaining_offers()
        assert product_page.product_visible_offers() == expected_product_offers

        # Switch to specification and check it
        product_page.show_tab(ProductTabs.PRODUCT_SPECIFICATION)
        assert product_page.product_comparison_is_visible() is False
        assert product_page.product_specification_is_visible() is True
        assert product_page.product_description() == expected_product_description

    def test_product_without_images(self):
        """
        Test place holder for a product image when product doesn't have any images
        """
        product_page = ProductPage(self.driver)
        product_page.open(21)

        expected_product_main_image = 'http://via.placeholder.com/300x300?text=%C5%BD%C3%A1dn%C3%BD%20obr%C3%A1zek'

        assert product_page.product_main_image() == expected_product_main_image


@pytest.mark.usefixtures('start_browser')
class TestGallery:

    def test_gallery(self):
        """
        Test behaviour of the image gallery
        """

        expected_images = [
            'https://im9.cz/iR/importprodukt-orig/cf2/cf292a2388aa9598b948794a47705a92.jpg',
            'https://im9.cz/iR/importprodukt-orig/719/719cbb7f53feee082aa6a0e91a35a3c9.jpg',
            'https://im9.cz/iR/importprodukt-orig/719/719cbb7f53feee082aa6a0e91a35a3c9.jpg',
            'https://im9.cz/iR/importprodukt-orig/719/719cbb7f53feee082aa6a0e91a35a3c9.jpg',
            'https://im9.cz/iR/importprodukt-orig/719/719cbb7f53feee082aa6a0e91a35a3c9.jpg'
        ]

        product_page = ProductPage(self.driver)
        gallery = ImageGallery(self.driver)

        def visible_only_image(image_index):
            # let's use dynamic wait until the image shows itself
            return gallery.wait_until(lambda: gallery.visible_images() == [expected_images[image_index]])

        def wait_for_image_slide_to_finish():
            # sometimes it is just too difficult when dealing with animations
            sleep(0.5)

        product_page.open(3)
        assert gallery.is_visible() is False

        # open gallery and check that it is the first image
        product_page.show_gallery()
        assert gallery.is_visible() is True
        assert visible_only_image(0) is True

        # cycle through all remaining images
        for i in range(1, 5):
            gallery.go_to_next_image()
            assert visible_only_image(i) is True
            wait_for_image_slide_to_finish()

        # check that the first image is shown after the last one
        gallery.go_to_next_image()
        assert visible_only_image(0) is True
        wait_for_image_slide_to_finish()

        # check also prev button
        gallery.go_to_prev_image()
        assert visible_only_image(4) is True
        wait_for_image_slide_to_finish()

        # check that gallery closes
        gallery.close()
        assert gallery.is_visible() is False
