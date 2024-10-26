#!/usr/bin/env python3
"""
Module for fetching and caching web pages with an access tracker.

This module defines a `get_page` function to retrieve HTML content from
a specified URL.
It caches the content for a limited duration (10 seconds) to
optimize repeated requests.
The function also tracks the number of times each URL is accessed.

Dependencies:
    - requests: HTTP library for making requests
    - redis: Redis client for caching and tracking data

Example:
    page_content = get_page("http://slowwly.robertomurray.co.uk")
"""

import requests
import redis
from typing import Callable
from functools import wraps

# Configure Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def cache_with_tracking(expiration: int = 10) -> Callable:
    """
    Decorator to cache the HTML content of a URL and track its access count.

    Args:
        expiration (int): Expiration time for the cache in seconds.
                            Defaults to 10.

    Returns:
        Callable: The decorated function with caching and
                    tracking functionality.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str, *args, **kwargs) -> str:
            # Generate cache and count keys
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if URL is cached
            cached_content = redis_client.get(cache_key)
            if cached_content:
                redis_client.incr(count_key)
                return cached_content.decode("utf-8")

            # Fetch content and cache it
            content = func(url, *args, **kwargs)
            redis_client.setex(cache_key, expiration, content)
            redis_client.incr(count_key)
            return content

        return wrapper
    return decorator


@cache_with_tracking(expiration=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL with caching and access tracking.

    Args:
        url (str): The URL to retrieve HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for unsuccessful requests
    return response.text
