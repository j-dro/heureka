import json
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

    def _get(self, key) -> str:
        data = self.redis.get(key)
        if not data:
            raise RedisCacheKeyError('Key %s not found in cache' % key)

        return data.decode('utf-8')

    def _setex(self, key, value):
        self.redis.setex(key, CACHE_TIMEOUT_SEC, value)

    def store(self, key, data):
        self._setex(key, json.dumps(data))

    def load(self, key):
        json_data = self._get(key)
        return json.loads(json_data)
