import pytest
from test_e2e.pages.category_page import CategoryPage
from test_e2e.components.pagination import Pagination
from test_e2e.components.categories_menu import CategoriesMenu


@pytest.mark.usefixtures('start_browser')
class TestCategory:

    def test_category_page(self):
        """
        Test content of category page
        """
        expected_categories = [
            'Mobilní telefony',
            'Vertikutátory',
            'Hudební nástroje'
        ]

        expected_product_names = [
            'Anatolian TS China 18"',
            'Anatolian BS Splash 10"',
            'Anatolian EMS Light Crash 16"',
            'Yamaha YFG 812 CII',
            'Yamaha YFG 811 II'
        ]

        expected_short_descriptions = [
            'Mi niekto niečo tak Bublina si všetko ako toto som ako Bublina do paže ako keby dojebal to robil keď by '
            'si niekto boršč? No ako keby oné hento ale nemám Internet. No ako keby dojebal oné. Počkaj do paže keby '
            'dojebal oné. Čo ja? Tak oné či čo som ako ...'
        ] * 5

        expected_images = [
            'https://im9.cz/iR/importprodukt-orig/95f/95f66f619659dffc8c731cf9b4a063f4.jpg',
            'http://via.placeholder.com/200x200?text=%C5%BD%C3%A1dn%C3%BD%20obr%C3%A1zek',
            'http://via.placeholder.com/200x200?text=%C5%BD%C3%A1dn%C3%BD%20obr%C3%A1zek',
            'https://im9.cz/iR/importprodukt-orig/368/3686ebc674e1cc72755a7572222a762e.jpg',
            'http://via.placeholder.com/200x200?text=%C5%BD%C3%A1dn%C3%BD%20obr%C3%A1zek'
        ]

        category_page = CategoryPage(self.driver)
        categories_menu = CategoriesMenu(self.driver)
        pagination = Pagination(self.driver)

        category_page.open(3, 1)
        assert categories_menu.category_names() == expected_categories
        assert category_page.product_names() == expected_product_names
        assert category_page.product_short_descriptions() == expected_short_descriptions
        assert category_page.product_min_prices() == ['16534', '553', '18755', '35955', '31558']
        assert category_page.product_max_prices() == ['19045', '648', '22558', '43052', '33109']
        assert category_page.product_images() == expected_images
        assert pagination.page_numbers() == ['1', '2']
