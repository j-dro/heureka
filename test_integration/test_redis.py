import pytest
from time import sleep
from app.libs.redis_cache import RedisCache, RedisCacheException

TEST_TIMEOUT_SEC = 1


class TestRedisIntegration:
    """
    This class perform integration test of RedisCache class with real Redis
    """
    def setup_method(self):
        self.cache = RedisCache(timeout_sec=TEST_TIMEOUT_SEC)
        # delete the key directly in the Redis
        self.cache.redis.delete('key')

    def test_store_and_read(self):
        """
        Test storing and reading back key/value with real Redis
        """
        self.cache.set('key', 'value')
        assert self.cache.get('key') == 'value'

    def test_key_not_found(self):
        """
        Test that missing key raises the correct exception with real Redis
        """
        with pytest.raises(RedisCacheException):
            self.cache.get('key')

    def test_key_expired(self):
        """
        Test that key/value is expired and deleted from the cache as expected
        """
        self.cache.set('key', 'value')
        sleep(TEST_TIMEOUT_SEC + 0.5)
        with pytest.raises(RedisCacheException):
            self.cache.get('key')
