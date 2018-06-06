import redis

from app.config import configuration


CACHE_TIMEOUT_SEC = 600


class RedisCacheException(Exception):
    pass


class RedisCacheKeyError(RedisCacheException):
    pass


class RedisCache:
    """
    Class that implements communication with Redis in-memory cache
    """
    def __init__(self,
                 redis_object=redis.StrictRedis.from_url(configuration['redis_url']),
                 timeout_sec=CACHE_TIMEOUT_SEC):
        """
        :param redis_object: :class:`redis.StrictRedis` object
        :param timeout_sec: timeout for invalidating cache records
        """

        self.redis = redis_object
        self.timeout_sec = timeout_sec

    def get(self, key) -> str:
        """
        Get the key from cache
        :param key: cache key
        :return: value if key exists in the cache or raise RedisCacheKeyError if not
        """
        data = self.redis.get(key)
        if not data:
            raise RedisCacheKeyError('Key %s not found in cache' % key)

        return data.decode('utf-8')

    def set(self, key, value):
        """
        Store the value to cache
        :param key: cache key
        :param value: value to store
        """
        self.redis.set(key, value, ex=self.timeout_sec)
