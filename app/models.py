import json
from math import inf, ceil
from app.libs.redis_cache import RedisCache

NO_PICTURE_TEXT = 'Žadný obrázek'

PAGES_COUNT_IN_PAGINATION = 10


class Cachable:
    TO_CACHE = ['obj_id']

    def __init__(self, obj_id):
        self.obj_id = obj_id

    @property
    def json(self):
        dictionary = {}
        for key in self.TO_CACHE:
            dictionary[key] = getattr(self, key)

        return json.dumps(dictionary)

    def save_to_cache(self, cache: RedisCache):
        key = '%s%s' % (self.__class__.__name__, self.obj_id)
        cache.setex(key, self.json)

    @classmethod
    def dict_from_cache(cls, cache: RedisCache, obj_id):
        key = '%s%s' % (cls.__name__, obj_id)
        json_data = cache.get(key)
        return json.loads(json_data)

    @classmethod
    def from_cache(cls, cache: RedisCache, obj_id):
        return cls(**cls.dict_from_cache(cache, obj_id))


class Category(Cachable):
    TO_CACHE = ['obj_id', 'title']

    def __init__(self, obj_id, title):
        super().__init__(obj_id)
        self.title = title


class Categories(Cachable):
    TO_CACHE = ['obj_id', 'category_ids']

    def __init__(self, obj_id, categories):
        super().__init__(obj_id)
        self.categories = categories
        self.category_ids = [category.obj_id for category in categories]

    def save_to_cache(self, cache: RedisCache):
        super().save_to_cache(cache)
        for category in self.categories:
            category.save_to_cache(cache)

    @classmethod
    def from_cache(cls, cache: RedisCache, obj_id):
        dictionary = cls.dict_from_cache(cache, obj_id)
        dictionary['categories'] = []
        for category_id in dictionary['category_ids']:
            dictionary['categories'].append(Category.from_cache(cache, category_id))
        del dictionary['category_ids']
        return cls(**dictionary)


class Offer:
    def __init__(self, offer_id, shop_name, price, url):
        self.id = offer_id
        self.shop_name = shop_name
        self.price = price
        self.url = url


class Product:
    def __init__(self, product_id, category_id, title, description, image_urls, offers):
        self.id = product_id
        self.category_id = category_id
        self.title = title
        self.description = description
        self.image_urls = image_urls
        self.offers = offers

        self.min_price = inf
        self.max_price = -inf

        for offer in self.offers:
            if offer.price < self.min_price:
                self.min_price = offer.price

            if offer.price > self.max_price:
                self.max_price = offer.price

        if not self.image_urls:
            self.image_urls = ['http://via.placeholder.com/100x100?text=' + NO_PICTURE_TEXT]

    @property
    def sorted_offers(self):
        return sorted(self.offers, key=lambda offer: offer.price)


class Pagination:
    def __init__(self, items_count, items_per_page, current_page, show_pages_count=PAGES_COUNT_IN_PAGINATION):
        self.current_page = current_page
        self.total_pages_count = ceil(items_count / items_per_page)

        # calculate available pages for pagination
        start_page = self.current_page - (show_pages_count // 2)
        if start_page < 1:
            start_page = 1

        end_page = start_page + show_pages_count - 1
        if end_page > self.total_pages_count:
            end_page = self.total_pages_count
            start_page = end_page - show_pages_count + 1

        prepare_pages = list(range(start_page, end_page+1))
        self.available_pages = [page for page in prepare_pages if page > 0]

        # calculate prev and next page
        self.prev_page = self.current_page - 1
        if self.prev_page < 1:
            self.prev_page = None

        self.next_page = self.current_page + 1
        if self.next_page > self.total_pages_count:
            self.next_page = None
