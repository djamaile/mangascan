from flask_caching import Cache
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

cache = Cache(
    config={
        "DEBUG": True,
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": REDIS_HOST,
        "CACHE_REDIS_PORT": REDIS_PORT,
    }
)
