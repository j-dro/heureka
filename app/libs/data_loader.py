import app.libs.api as api
from app.libs.redis_cache import RedisCache, RedisCacheException
from app.models import Category, Categories

CATEGORIES_OBJ_ID = ''

CATEGORY_KEYS = ['obj_id', 'title']
CATEGORIES_KEYS = ['obj_id', 'category_ids']

CATEGORY_PREFIX = 'Category'
CATEGORIES_PREFIX = 'Categories'


def object_to_dict(obj, keys):
    dictionary = {}
    for key in keys:
        dictionary[key] = getattr(obj, key)

    return dictionary


def cache_key(class_key, obj_id):
    return '%s%s' % (class_key, obj_id)


class DataLoader:
    def __init__(self):
        self.cache = RedisCache()

    def _store_category_to_cache(self, category: Category):
        category_dict = object_to_dict(category, CATEGORY_KEYS)
        self.cache.store(cache_key(CATEGORY_PREFIX, category.obj_id), category_dict)

    def _fetch_category_from_cache(self, obj_id) -> Category:
        category_dict = self.cache.load(cache_key(CATEGORY_PREFIX, obj_id))
        return Category(**category_dict)

    def _store_categories_to_cache(self, categories: Categories):
        categories_dict = object_to_dict(categories, CATEGORIES_KEYS)
        self.cache.store(cache_key(CATEGORIES_PREFIX, categories.obj_id), categories_dict)
        for category in categories.categories:
            self._store_category_to_cache(category)

    def _fetch_all_categories_from_cache(self) -> Categories:
        categories_list = []
        categories_dict = self.cache.load(cache_key(CATEGORIES_PREFIX, CATEGORIES_OBJ_ID))
        for category_id in categories_dict['category_ids']:
            categories_list.append(self._fetch_category_from_cache(category_id))
        del categories_dict['category_ids']
        return Categories(CATEGORIES_OBJ_ID, categories_list)

    def load_all_categories(self) -> Categories:
        try:
            return self._fetch_all_categories_from_cache()
        except RedisCacheException:
            categories = api.fetch_all_categories()
            self._store_categories_to_cache(categories)
            return categories
