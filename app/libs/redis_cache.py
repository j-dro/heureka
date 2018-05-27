import redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

CACHE_TIMEOUT_SEC = 60


class RedisCacheException(Exception):
    pass


class RedisCacheKeyError(RedisCacheException):
    pass


class RedisCache:
    def __init__(self):
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def get(self, key) -> str:
        data = self.redis.get(key)
        if not data:
            raise RedisCacheKeyError('Key %s not found in cache' % key)

        return data.decode('utf-8')

    def setex(self, key, value):
        self.redis.setex(key, CACHE_TIMEOUT_SEC, value)
