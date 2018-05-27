import app.libs.api as api
from app.libs.redis_cache import RedisCache, RedisCacheException
from app.models import Category, Categories

CATEGORIES_OBJ_ID = ''


def object_to_dict(obj):
    dictionary = {}
    for key in obj.TO_CACHE:
        dictionary[key] = getattr(obj, key)

    return dictionary


def object_to_key(obj):
    return '%s%s' % (obj.CACHE_KEY, obj.obj_id)


def class_to_key(cls, obj_id):
    return '%s%s' % (cls.CACHE_KEY, obj_id)


class DataLoader:
    def __init__(self):
        self.cache = RedisCache()

    def _store_category_to_cache(self, category: Category):
        category_dict = object_to_dict(category)
        self.cache.store(object_to_key(category), category_dict)

    def _fetch_category_from_cache(self, obj_id) -> Category:
        category_dict = self.cache.load(class_to_key(Category, obj_id))
        return Category(**category_dict)

    def _store_categories_to_cache(self, categories: Categories):
        categories_dict = object_to_dict(categories)
        self.cache.store(object_to_key(categories), categories_dict)
        for category in categories.categories:
            self._store_category_to_cache(category)

    def _fetch_all_categories_from_cache(self) -> Categories:
        categories_list = []
        categories_dict = self.cache.load(class_to_key(Categories, CATEGORIES_OBJ_ID))
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
