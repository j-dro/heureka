import pytest
import json
from unittest.mock import Mock, call
from app.libs.redis_cache import RedisCacheException
from app.libs.api import CachedApi

MOCK_URL = 'https://host'

RESPONSE_CATEGORY1 = '{"categoryId": 1, "title": "Category1 title"}'
RESPONSE_CATEGORY2 = '{"categoryId": 2, "title": "Category2 title"}'
RESPONSE_CATEGORIES = '[%s, %s]' % (RESPONSE_CATEGORY1, RESPONSE_CATEGORY2)
RESPONSE_PRODUCT1 = '{"categoryId": 3, "productId": 1, "title": "Product1 title"}'
RESPONSE_PRODUCT2 = '{"categoryId": 3, "productId": 2, "title": "Product2 title"}'
RESPONSE_PRODUCTS = '[%s, %s]' % (RESPONSE_PRODUCT1, RESPONSE_PRODUCT2)
RESPONSE_OFFERS_PRODUCT1 = json.dumps([
    {
        'offerId': 1,
        'productId': 1,
        'title': 'Product1 Offer1',
        'description': 'Product1 Offer1 description',
        'url': 'http://shop1.cz/product/1',
        'img_url': 'http://image-1-1',
        'price': 10.0
    }, {
        'offerId': 2,
        'productId': 1,
        'title': 'Product1 Offer2',
        'description': 'Product1 Offer2 longer description',
        'url': 'http://shop2.cz/product/1',
        'img_url': 'http://image-1-2',
        'price': 100.5
    }
])
RESPONSE_OFFERS_PRODUCT2 = json.dumps([
    {
        'offerId': 3,
        'productId': 2,
        'title': 'Product2 Offer3',
        'description': 'Product2 Offer3 description',
        'url': 'http://shop3.cz/product/2',
        'img_url': 'http://image-2-3',
        'price': 150.5
    }
])


class MockEmptyCache:
    def __init__(self):
        self.get = Mock(side_effect=RedisCacheException('Not found in cache'))
        self.set = Mock()


class MockFullCache:
    RESPONSES_DICT = {
        '/categories': RESPONSE_CATEGORIES,
        '/category/1': RESPONSE_CATEGORY1,
        '/category/2': RESPONSE_CATEGORY2,
        '/product/1': RESPONSE_PRODUCT1,
        '/product/2': RESPONSE_PRODUCT2,
        '/products/3/0/5': RESPONSE_PRODUCTS,
        '/offers/1/0/1000000': RESPONSE_OFFERS_PRODUCT1,
        '/offers/2/0/1000000': RESPONSE_OFFERS_PRODUCT2
    }

    def __init__(self):
        self.set = Mock()

    def get(self, key):
        return self.RESPONSES_DICT[key]


class MockSession:
    RESPONSES_DICT = {
        MOCK_URL + '/categories': RESPONSE_CATEGORIES,
        MOCK_URL + '/category/1': RESPONSE_CATEGORY1,
        MOCK_URL + '/category/2': RESPONSE_CATEGORY2,
        MOCK_URL + '/product/1': RESPONSE_PRODUCT1,
        MOCK_URL + '/product/2': RESPONSE_PRODUCT2,
        MOCK_URL + '/products/3/0/5': RESPONSE_PRODUCTS,
        MOCK_URL + '/offers/1/0/1000000': RESPONSE_OFFERS_PRODUCT1,
        MOCK_URL + '/offers/2/0/1000000': RESPONSE_OFFERS_PRODUCT2
    }

    def get(self, url):
        response = Mock()
        response_text = self.RESPONSES_DICT[url]
        response.text = response_text
        response.json = Mock(return_value=json.loads(response_text))
        return response


class TestApi:
    """
    Tests Api class
        - data are read from cache if present in cache
        - data are loaded from api and cached if not present in cache already
    """

    def init_api(self, data_cached):
        """
        Init Api object for the test
        :param data_cached: True - all data are in cache for the test, False - no data are in cache for the test
        """
        if data_cached:
            self.mock_cache = MockFullCache()
            session = None
        else:
            self.mock_cache = MockEmptyCache()
            session = MockSession()

        self.api = CachedApi(MOCK_URL, self.mock_cache, session)

    @pytest.mark.parametrize('data_cached', [True, False])
    def test_fetch_category(self, data_cached):
        """
        Test fetching of one category from API/cache
        :param data_cached: True - all data are in cache for the test, False - no data are in cache for the test
        """
        self.init_api(data_cached)

        category = self.api.fetch_category(1)

        assert category.obj_id == 1
        assert category.title == 'Category1 title'

        if data_cached:
            assert self.mock_cache.set.mock_calls == []
        else:
            # check that api call was also cached
            assert self.mock_cache.set.mock_calls == [
                call('/category/1', RESPONSE_CATEGORY1)
            ]

    @pytest.mark.parametrize('data_cached', [True, False])
    def test_fetch_all_categories(self, data_cached):
        """
        Test fetching of all categories from API/cache
        :param data_cached: True - all data are in cache for the test, False - no data are in cache for the test
        """
        self.init_api(data_cached)
        all_categories = self.api.fetch_all_categories()

        assert len(all_categories.categories) == 2
        assert all_categories.categories[0].obj_id == 1
        assert all_categories.categories[0].title == 'Category1 title'
        assert all_categories.categories[1].obj_id == 2
        assert all_categories.categories[1].title == 'Category2 title'

        if data_cached:
            # data were already in cache, nothing stored to cache
            assert self.mock_cache.set.mock_calls == []
        else:
            # check that not only all categories call but also individual categories calls were cached
            assert self.mock_cache.set.mock_calls == [
                call('/categories', RESPONSE_CATEGORIES),
                call('/category/1', RESPONSE_CATEGORY1),
                call('/category/2', RESPONSE_CATEGORY2)
            ]

    @pytest.mark.parametrize('data_cached', [True, False])
    def test_fetch_one_product(self, data_cached):
        """
        Test fetching of one product in a category from API/cache
        :param data_cached: True - all data are in cache for the test, False - no data are in cache for the test
        """
        self.init_api(data_cached)

        product = self.api.fetch_product(1)

        assert product.id == 1
        assert product.title == 'Product1 title'
        assert product.category_id == 3
        assert product.description == 'Product1 Offer2 longer description'
        assert product.image_urls == ['http://image-1-1', 'http://image-1-2']

        (offer1, offer2) = product.offers
        assert offer1.id == 1
        assert offer1.price == 10.0
        assert offer1.url == 'http://shop1.cz/product/1'
        assert offer1.shop_name == 'shop1'

        assert offer2.id == 2
        assert offer2.price == 100.5
        assert offer2.url == 'http://shop2.cz/product/1'
        assert offer2.shop_name == 'shop2'

        if data_cached:
            # data were already in cache, nothing stored to cache
            assert self.mock_cache.set.mock_calls == []
        else:
            # check that product call and offers call were cached
            assert self.mock_cache.set.mock_calls == [
                call('/product/1', RESPONSE_PRODUCT1),
                call('/offers/1/0/1000000', RESPONSE_OFFERS_PRODUCT1)
            ]

    @pytest.mark.parametrize('data_cached', [True, False])
    def test_fetch_products(self, data_cached):
        """
        Test fetching of a batch of products in a category from API/cache
        :param data_cached: True - all data are in cache for the test, False - no data are in cache for the test
        """
        self.init_api(data_cached)

        (product1, product2) = self.api.fetch_products(category_id=3, offset=0, limit=5)

        # check only a few things for product 1, it's enough
        assert product1.id == 1
        assert product1.title == 'Product1 title'
        assert len(product2.offers) == 1

        # check everything for product 2
        assert product2.id == 2
        assert product2.title == 'Product2 title'
        assert product2.category_id == 3
        assert product2.description == 'Product2 Offer3 description'
        assert product2.image_urls == ['http://image-2-3']

        # check offers for product 2
        assert len(product2.offers) == 1
        offer3 = product2.offers[0]
        assert offer3.id == 3
        assert offer3.price == 150.5
        assert offer3.url == 'http://shop3.cz/product/2'
        assert offer3.shop_name == 'shop3'

        if data_cached:
            # data were already in cache, nothing stored to cache
            assert self.mock_cache.set.mock_calls == []
        else:
            # check that not only products call but also each product and their offers calls were cached
            assert self.mock_cache.set.mock_calls == [
                call('/products/3/0/5', RESPONSE_PRODUCTS),
                call('/offers/1/0/1000000', RESPONSE_OFFERS_PRODUCT1),
                call('/product/1', RESPONSE_PRODUCT1),
                call('/offers/2/0/1000000', RESPONSE_OFFERS_PRODUCT2),
                call('/product/2', RESPONSE_PRODUCT2)
            ]
