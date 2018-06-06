import pytest
from test_e2e.pages.category_page import CategoryPage
from test_e2e.components.pagination import Pagination


@pytest.mark.usefixtures('start_browser')
class TestPagination:

    def test_pagination(self):
        """
        Test that pagination works on the Category page
        """
        expected_products_on_pages = [
            ['Apple iPhone 6', 'Apple iPHone 6S', 'Apple iPHone 5S', 'Lenovo VIBE Shot 32GB', 'Lenovo VIBE Shot 64GB'],
            ['Huawei P8', 'Huawei P8 lite', 'Samsung Galaxy S1000 mini', 'Microsoft Lumia', 'Sony Ikspíria'],
            ['Fieldman FZV 4001-E']
        ]

        pagination = Pagination(self.driver)
        category_page = CategoryPage(self.driver)

        # first page
        category_page.open(category_id=1, page_number=1)
        assert category_page.product_names() == expected_products_on_pages[0]
        assert pagination.prev_page_is_disabled() is True
        assert pagination.next_page_is_disabled() is False

        # next to second page
        pagination.go_to_next_page()
        assert category_page.product_names() == expected_products_on_pages[1]
        assert pagination.prev_page_is_disabled() is False
        assert pagination.next_page_is_disabled() is False

        # next to last page
        pagination.go_to_next_page()
        assert category_page.product_names() == expected_products_on_pages[2]
        assert pagination.prev_page_is_disabled() is False
        assert pagination.next_page_is_disabled() is True

        # second page by clicking on page number
        pagination.go_to_page(2)
        assert category_page.product_names() == expected_products_on_pages[1]
        assert pagination.prev_page_is_disabled() is False
        assert pagination.next_page_is_disabled() is False
