import unittest
import redis
from flask import Flask
from core.cache import cache

app_mock = Flask(__name__)
cache.init_app(app_mock)

# needs to be initialized outside of class
redis = redis.Redis()


class TestCache(unittest.TestCase):
    def test_if_redis_is_up(self):
        pong = redis.ping()
        assert pong == True

    def tearDown(self) -> None:
        redis.delete("flask_cache_cache-test")

    def test_if_redis_can_save(self):
        @cache.cached(timeout=3, key_prefix="cache-test")
        def save():
            return "we are saved"

        save()
        assert redis.exists("flask_cache_cache-test") == True
