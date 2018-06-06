import pytest
from unittest.mock import Mock, call
from app.libs.redis_cache import RedisCache, RedisCacheException, CACHE_TIMEOUT_SEC


class TestRedisCache:
    def setup_method(self):
        self.redis = Mock()
        self.redis.set = Mock()

    def test_set(self):
        cache = RedisCache(self.redis)
        cache.set('key', 'value')

        assert self.redis.set.mock_calls == [call('key', 'value', ex=CACHE_TIMEOUT_SEC)]

    def test_get(self):
        self.redis.get = Mock(return_value=b'value')
        cache = RedisCache(self.redis)
        assert cache.get('key') == 'value'

    def test_get_not_in_cache(self):
        self.redis.get = Mock(return_value=None)
        cache = RedisCache(self.redis)
        with pytest.raises(RedisCacheException):
            cache.get('key')
