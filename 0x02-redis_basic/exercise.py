#!/usr/bin/env python3
"""

"""

from redis import Redis
from typing import Union
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
