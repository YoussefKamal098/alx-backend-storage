#!/usr/bin/env python3
"""

"""

from redis import Redis
from typing import Union, Optional, Callable
from uuid import uuid4


class Cache:
    """Caching class"""
    def __init__(self) -> None:
        """Initialize new cache object"""
        self._redis = Redis()

        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Stores data in redis with randomly generated key"""
        key = str(uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and optionally apply a
        conversion function `fn`.
        """
        value: bytes = self._redis.get(key)

        if value and fn:
            return fn(value)
        if value:
            return value

        return None

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.
        """
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.
        """
        return self.get(key, lambda value: int(value))
