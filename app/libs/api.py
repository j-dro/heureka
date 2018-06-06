import json
import re
from typing import Dict, List, Union

import requests

from app.config import configuration
from app.libs.redis_cache import RedisCache, RedisCacheException
from app.models import AllCategories, Category, Offer, Product

DEFAULT_LIMIT = 1000000

URL = configuration['api_url']
CATEGORIES_URI = '/categories'
CATEGORY_URI = '/category/{category_id}'
PRODUCTS_URI = '/products/{category_id}/{offset}/{limit}'
PRODUCT_URI = '/product/{product_id}'
PRODUCT_COUNT_URI = '/products/{category_id}/count'
PRODUCT_OFFERS_URI = '/offers/{product_id}/{offset}/{limit}'


def shop_name_from_url(url: str) -> str:
    """
    Get the shop name from url
    This is the most simple way - normally we would have the shop name in API response I suppose
    :param url: url of the product in the shop
    :return: shop name
    """

    mo = re.search('http://(.*).cz', url)
    if mo:
        return mo.group(1)
    else:
        raise ValueError('Failed to get shop name from url')


class CachedApi:
    """
    This class implements communication to the API together with caching the responses in Redis in-memory cache
    """
    def __init__(self, url=URL, cache=RedisCache(), session=requests.Session()):
        """
        Constructor
        :param url: url of the API
        :param cache: :class:`RedisCache` object
        :param session: :class:`requests.Session` object
        """
        self.url = url
        self.cache = cache
        self.session = session

    def _get(self, uri: str) -> (bool, Union[Dict, List]):
        """
        Gets either value from cache if it is there or response from API (and then caches it)
        :param uri: URI of the HTTP request
        :return: whether response was cached or not and actual response
        """
        try:
            json_data = self.cache.get(uri)
            cached_response = True
            return cached_response, json.loads(json_data)
        except RedisCacheException:
            response = self.session.get(self.url + uri)
            response.raise_for_status()
            data = response.json()
            self.cache.set(uri, response.text)
            cached_response = False
            return cached_response, data

    def fetch_all_categories(self) -> AllCategories:
        """
        Fetch all categories data from cache/API
        :return: :class:`AllCategories` object
        """
        categories = []
        cached_response, response_data = self._get(CATEGORIES_URI)

        for item in response_data:
            category_id = item['categoryId']
            categories.append(Category(obj_id=category_id, title=item['title']))

            if not cached_response:
                # sort keys for better testability
                self.cache.set(CATEGORY_URI.format(category_id=category_id), json.dumps(item, sort_keys=True))

        return AllCategories(categories)

    def fetch_category(self, category_id: int) -> Category:
        """
        Fetch one category data from cache/API
        :return: :class:`Category` object
        """
        cached_response, response_data = self._get(CATEGORY_URI.format(category_id=category_id))
        return Category(obj_id=response_data['categoryId'], title=response_data['title'])

    def fetch_product_count(self, category_id: int) -> int:
        """
        Fetch number of products in a category
        :param category_id: ID of the category
        :return: product count
        """
        cached_response, response_data = self._get(PRODUCT_COUNT_URI.format(category_id=category_id))
        return response_data['count']

    def fetch_product(self, product_id: int) -> Product:
        """
        Fetch one product's data from cache/API
        :param product_id: ID of the product
        :return: :class:`Product` object
        """
        cached_response, response_data = self._get(PRODUCT_URI.format(product_id=product_id))

        # We could fetch product details using pagination but there won't be probably that much offers per product
        product_description, product_image_urls, offers = self._fetch_product_details(product_id)

        return Product(product_id=response_data['productId'],
                       category_id=response_data['categoryId'],
                       title=response_data['title'],
                       description=product_description,
                       image_urls=product_image_urls,
                       offers=offers)

    def fetch_products(self, category_id: int, offset: int=0, limit: int=DEFAULT_LIMIT) -> List[Product]:
        """
        Fetch products' data from cache/API
        :param category_id: ID of the products category
        :param offset: offset for paginating the requests
        :param limit: maximum number of the products to fetch
        :return: List of :class:`Product` objects
        """
        products = []
        cached_response, response_data = self._get(PRODUCTS_URI.format(category_id=category_id,
                                                                       offset=offset,
                                                                       limit=limit))
        for item in response_data:
            product_id = item['productId']
            # We could fetch product details using pagination but there won't be probably that much offers per product
            product_description, product_image_urls, offers = self._fetch_product_details(product_id)

            product = Product(product_id=product_id,
                              category_id=item['categoryId'],
                              title=item['title'],
                              description=product_description,
                              image_urls=product_image_urls,
                              offers=offers)

            products.append(product)

            if not cached_response:
                # sort keys for better testability
                self.cache.set(PRODUCT_URI.format(product_id=product_id), json.dumps(item, sort_keys=True))

        return products

    def _fetch_product_details(self,
                               product_id: int,
                               offset: int=0,
                               limit: int=DEFAULT_LIMIT) -> (str, List[str], List[Offer]):
        """
        Fetch product offers from the cache/API
        From the response extract also product description and product images
        :param product_id: ID of the product to fetch
        :param offset: offset for paginating the requests
        :param limit: limit: maximum number of the offers to fetch
        :return: Product description, list of product images urls, List of :class:`Offer` objects
        """
        offers = []

        product_description = ''

        product_image_urls = []

        cached_response, response_data = self._get(PRODUCT_OFFERS_URI.format(product_id=product_id,
                                                                             offset=offset,
                                                                             limit=limit))
        for item in response_data:
            if item['description'] and len(item['description']) > len(product_description):
                product_description = item['description']

            if item['img_url']:
                product_image_urls.append(item['img_url'])

            shop_name = shop_name_from_url(item['url'])

            offers.append(Offer(offer_id=item['offerId'],
                                shop_name=shop_name,
                                price=item['price'],
                                url=item['url']))

        return product_description, product_image_urls, offers
