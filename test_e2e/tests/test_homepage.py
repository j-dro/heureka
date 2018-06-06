import pytest
from test_e2e.pages.home_page import HomePage
from test_e2e.components.categories_menu import CategoriesMenu


@pytest.mark.usefixtures('start_browser')
class TestHomePage:

    def test_categories(self):
        """
        Test content of homepage - category side bar and category grid
        :return:
        """
        expected_categories = [
            'Mobilní telefony',
            'Vertikutátory',
            'Hudební nástroje'
        ]

        home_page = HomePage(self.driver)
        categories_menu = CategoriesMenu(self.driver)
        home_page.open()
        assert categories_menu.category_names() == expected_categories
        assert home_page.grid_category_names() == expected_categories
