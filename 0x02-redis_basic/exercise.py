#!/usr/bin/env python3
"""
Redis Caching Module

This module implements a caching mechanism using Redis. It provides a
Cache class with methods for storing and retrieving data, along with
decorators to count method calls and store the history of inputs and
outputs for those methods.

Key Components:

1. **Decorators**:
   - `count_calls`: A decorator that counts how many times a
        method is called.
   - `call_history`: A decorator that records the history of
        method inputs and outputs in Redis.
   - `replay`: A function that displays the history of calls for a
        particular method, including inputs and outputs.

2. **Cache Class**:
   - **Attributes**:
     - `_redis`: An instance of the Redis client used to interact with
            the Redis database.
   - **Methods**:
     - `__init__`: Initializes the cache object and flushes the Redis
            database.
     - `store(data)`: Stores data in Redis with a randomly generated
            key and applies the `call_history` and `count_calls` decorators.
     - `get(key, fn)`: Retrieves data from Redis using a given key and
            optionally applies a conversion function `fn`.
     - `get_str(key)`: Retrieves a string value from Redis by
            decoding the bytes.
     - `get_int(key)`: Retrieves an integer value from Redis by converting
            the bytes to an integer.

Usage:

To use the caching mechanism, create an instance of the Cache class.
You can store data with the `store` method, and retrieve it using
the `get`, `get_str`, or `get_int` methods. The decorators
automatically track the number of times methods are called and
maintain a history of their inputs and outputs.

Example:

    cache = Cache()
    key = cache.store("Hello, World!")
    value = cache.get_str(key)
    print(value)  # Output: Hello, World!

    cache.store(42)
    cache.store(3.14)

    replay(cache.store)  # Displays history of calls for the store method
"""

import redis
import functools
from uuid import uuid4
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: A wrapped method that increments a Redis
            counter each time it is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs of a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: A wrapped method that stores inputs and outputs in Redis.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, result)

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.

    Args:
        method (Callable): The method for which the call history is displayed.

    Returns:
        None
    """
    redis_instance = getattr(getattr(method, "__self__"), "_redis")
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{eval(inp)}) -> {out.decode('utf-8')}")


class Cache:
    """Caching class for storing and retrieving data in Redis."""

    def __init__(self) -> None:
        """
        Initialize a new Cache object and connect to Redis.

        This method flushes the Redis database upon initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a randomly generated key.

        Args:
            data (Union[str, int, bytes, float]): The data to
                be stored in Redis.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and optionally apply a conversion
        function `fn`.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable], optional): An optional conversion
            function to apply to the retrieved data.

        Returns:
            Optional[Union[str, bytes, int, float]]: The retrieved data,
                possibly converted, or None if not found.
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

        Args:
            key (str): The key of the string data to retrieve.

        Returns:
            Optional[str]: The decoded string value or None if not found.
        """
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key of the integer data to retrieve.

        Returns:
            Optional[int]: The integer value or None if not found.
        """
        return self.get(key, lambda value: int(value))
