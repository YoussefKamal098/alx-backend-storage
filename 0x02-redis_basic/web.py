#!/usr/bin/env python3
"""
A simple caching mechanism for web page content using Redis.

This module provides a decorator `cache_page` that caches the
content of a web page fetched via the `get_page` function.
If the content is cached, it retrieves it from
Redis; otherwise, it fetches the content from the web and
stores it in the cache.

Caching is set to expire after 10 seconds.
The module also keeps track of the number
of times a page is accessed from the cache.
"""

import redis
import requests
import functools
from typing import Callable

# Constants for Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis()


def cache_page(fn: Callable) -> Callable:
    """
    A decorator that caches the output of a function that fetches web pages.

    Args:
        fn (Callable): The function that fetches web page content.

    Returns:
        Callable: A wrapper function that adds caching functionality.
    """
    @functools.wraps(fn)
    def wrapper(url: str, *args, **kwargs):
        """
        Wrapper function that manages caching logic for the page content.
        """

        # Cache for page content
        cache_key = f"page_cache:{url}"
        # Cache for access count
        access_count_key = f"count:{url}"

        # Attempt to retrieve cached content
        cached_content = redis_client.get(cache_key)

        if cached_content:
            """
            If content is cached, increment access count
            and return cached content
            """
            redis_client.incr(access_count_key)
            print(f"Cache found for URL: {url}")
            return cached_content.decode('utf-8')

        # If not cached, fetch content from the web
        print(f"No cached content found for URL: {url}. "
              f"Fetching from the web...")
        page_content = fn(url, *args, **kwargs)

        """
        Store the fetched content in cache with an
        expiration time of 10 seconds
        """
        redis_client.setex(cache_key, 10, page_content)
        redis_client.incr(access_count_key)

        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch the content of a web page.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The content of the web page.

    Raises:
        HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    response = requests.get(url)
    # Raise an error for bad responses (4xx or 5xx)
    response.raise_for_status()
    return response.text
