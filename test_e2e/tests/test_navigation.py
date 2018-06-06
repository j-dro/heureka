import pytest
from test_e2e.pages.home_page import HomePage
from test_e2e.pages.category_page import CategoryPage, Using
from test_e2e.components.title_bar import TitleBar
from test_e2e.components.categories_menu import CategoriesMenu
from test_e2e.pages.product_page import ProductPage


@pytest.mark.usefixtures('start_browser')
class TestNavigation:

    def init(self):
        self.title_bar = TitleBar(self.driver)
        self.categories_menu = CategoriesMenu(self.driver)
        self.home_page = HomePage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)

    def test_navigation1(self):
        """
        Test navigation
        Home page: click on a category in category menu
        Category page: click on product title
        """
        self.init()

        self.home_page.open()
        assert self.home_page.page_title() == 'Kategorie'

        self.categories_menu.go_to_category('Vertikutátory')
        assert self.category_page.page_title() == 'Produkty v sekci Vertikutátory'

        self.category_page.go_to_product('Fiskars Quickfit A')
        assert self.product_page.page_title() == 'Detail produktu - Fiskars Quickfit A'

        self.title_bar.go_home()
        assert self.home_page.page_title() == 'Kategorie'

    def test_navigation2(self):
        """
        Test navigation in another way
        Home page: click on a category in category grid
        Category page: click on compare button
        """
        self.init()

        self.home_page.open()
        assert self.home_page.page_title() == 'Kategorie'

        self.home_page.go_to_category('Vertikutátory')
        assert self.category_page.page_title() == 'Produkty v sekci Vertikutátory'

        self.category_page.go_to_product('Fiskars Quickfit A', using=Using.COMPARE_BUTTON)
        assert self.product_page.page_title() == 'Detail produktu - Fiskars Quickfit A'
