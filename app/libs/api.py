import re
import requests
from app.models import AllCategories, Category, Offer, Product

DEFAULT_LIMIT = 1000

URL = 'http://python-servers-vtnovk529892.codeanyapp.com:5000'
CATEGORIES_URL = URL + '/categories'
CATEGORY_URL = URL + '/category/{category_id}'
PRODUCTS_URL = URL + '/products/{category_id}/{offset}/{limit}'
PRODUCT_URL = URL + '/product/{product_id}'
PRODUCT_COUNT_URL = URL + '/products/{category_id}/count'
PRODUCT_OFFERS_URL = URL + '/offers/{product_id}/{offset}/{limit}'


def fetch_all_categories() -> AllCategories:
    categories = []
    response = requests.get(CATEGORIES_URL)
    response_data = response.json()
    for item in response_data:
        categories.append(Category(obj_id=item['categoryId'], title=item['title']))

    return AllCategories(categories)


def fetch_category(category_id):
    response = requests.get(CATEGORY_URL.format(category_id=category_id))
    response.raise_for_status()
    response_data = response.json()
    return Category(obj_id=response_data['categoryId'], title=response_data['title'])


def fetch_product_count(category_id):
    response = requests.get(PRODUCT_COUNT_URL.format(category_id=category_id))
    response.raise_for_status()
    response_data = response.json()
    return response_data['count']


def fetch_product(product_id):
    response = requests.get(PRODUCT_URL.format(product_id=product_id))
    response.raise_for_status()
    response_data = response.json()

    product_description, product_image_urls, offers = fetch_product_details(product_id)

    return Product(product_id=product_id,
                   category_id=response_data['categoryId'],
                   title=response_data['title'],
                   description=product_description,
                   image_urls=product_image_urls,
                   offers=offers)


def fetch_products(category_id, offset=0, limit=DEFAULT_LIMIT):
    # TODO probably will have to implement pagination
    products = []
    response = requests.get(PRODUCTS_URL.format(category_id=category_id, offset=offset, limit=limit))
    response.raise_for_status()
    response_data = response.json()
    for item in response_data:
        product_id = item['productId']
        product_description, product_image_urls, offers = fetch_product_details(product_id)

        product = Product(product_id=product_id,
                          category_id=item['categoryId'],
                          title=item['title'],
                          description=product_description,
                          image_urls=product_image_urls,
                          offers=offers)

        products.append(product)

    return products


def shop_name_from_url(url):
    # the most simple way - normally we would have the shop name in API response I suppose
    mo = re.search('http://(.*).cz', url)
    if mo:
        return mo.group(1)
    else:
        raise ValueError('Failed to get shop name from url')


def fetch_product_details(product_id, offset=0, limit=DEFAULT_LIMIT):

    offers = []

    product_description = ''

    product_image_urls = []

    response = requests.get(PRODUCT_OFFERS_URL.format(product_id=product_id, offset=offset, limit=limit))
    response.raise_for_status()
    response_data = response.json()
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
