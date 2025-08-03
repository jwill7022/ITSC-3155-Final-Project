from functools import wraps
from typing import Any, Dict, Optional, Callable
import pickle
import hashlib
import time
import redis
from redis.exceptions import  RedisError, ConnectionError
import json
from fastapi import HTTPException, status


class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        try:
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()  # Test connection
        except (ConnectionError, TimeoutError):
            self.redis_client = None
            print("Warning: Redis not available, using in-memory cache")
            self._memory_cache: Dict[str, Dict] = {}

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from function name and arguments"""
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return pickle.loads(value)
            else:
                cache_item = self._memory_cache.get(key)
                if cache_item and cache_item['expires'] > time.time():
                    return cache_item['data']
                elif cache_item:
                    del self._memory_cache[key]
        except Exception as e:
            print(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL"""
        try:
            if self.redis_client:
                return self.redis_client.setex(key, ttl, pickle.dumps(value))
            else:
                self._memory_cache[key] = {
                    'data': value,
                    'expires': time.time() + ttl
                }
                return True
        except Exception as e:
            print(f"Cache set error: {e}")
        return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                if key in self._memory_cache:
                    del self._memory_cache[key]
                    return True
        except Exception as e:
            print(f"Cache delete error: {e}")
        return False

    def clear_pattern(self, pattern: str) -> int:
        """Clear keys matching pattern"""
        try:
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
            else:
                keys_to_delete = [k for k in self._memory_cache.keys() if pattern in k]
                for key in keys_to_delete:
                    del self._memory_cache[key]
                return len(keys_to_delete)
        except Exception as e:
            print(f"Cache clear pattern error: {e}")
        return 0


# Global cache instance
cache = CacheManager()


def cached(ttl: int = 300, key_prefix: Optional[str] = None):
    """Cache decorator for functions"""

    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or f"{func.__module__}.{func.__name__}"
            cache_key = cache._generate_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or f"{func.__module__}.{func.__name__}"
            cache_key = cache._generate_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return async_wrapper if hasattr(func, '__code__') and func.__code__.co_flags & 0x80 else sync_wrapper

    return decorator
