from app.libs.test_api import MockEmptyCache
from app.libs.api import CachedApi


class TestApiIntegration:
    """
    Tests in this class test integration of project classes with the real api to some extent
    """
    @classmethod
    def setup_class(cls):
        # mock empty cache to force data fetching from api, we don't need cache for these tests
        cls.api = CachedApi(cache=MockEmptyCache())

    def test_product(self):
        """
        Test fetching of product data including offers data
        """
        product = self.api.fetch_product(1)
        assert product.id == 1
        assert product.category_id == 1
        assert product.title == 'Apple iPhone 6'
        assert len(product.offers) == 5
        assert product.min_price == 15537.0
        assert product.max_price == 16620.0

    def test_remaining_calls(self):
        """
        Test remaining data fetches in short, we definitely could do it in more detail as the test above
        """

        all_categories = self.api.fetch_all_categories()
        assert len(all_categories.categories) == 3

        category = self.api.fetch_category(category_id=2)
        assert category.obj_id == 2

        assert self.api.fetch_product_count(category_id=3) == 9

        products = self.api.fetch_products(category_id=3)
        assert len(products) == 9
