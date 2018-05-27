import app.libs.api as api
from app.libs.redis_cache import RedisCache, RedisCacheException
from app.models import Category, AllCategories


CATEGORY_KEYS = ['obj_id', 'title']
ALL_CATEGORIES_KEYS = ['category_ids']

CATEGORY_PREFIX = 'Category'
ALL_CATEGORIES_PREFIX = 'AllCategories'


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

    def _store_all_categories_to_cache(self, all_categories: AllCategories):
        all_categories_dict = object_to_dict(all_categories, ALL_CATEGORIES_KEYS)
        self.cache.store(ALL_CATEGORIES_PREFIX, all_categories_dict)
        for category in all_categories.categories:
            self._store_category_to_cache(category)

    def _fetch_all_categories_from_cache(self) -> AllCategories:
        categories = []
        all_categories_dict = self.cache.load(ALL_CATEGORIES_PREFIX)
        for category_id in all_categories_dict['category_ids']:
            categories.append(self._fetch_category_from_cache(category_id))
        return AllCategories(categories)

    def load_category_list(self) -> AllCategories:
        try:
            return self._fetch_all_categories_from_cache()
        except RedisCacheException:
            all_categories = api.fetch_all_categories()
            self._store_all_categories_to_cache(all_categories)
            return all_categories
