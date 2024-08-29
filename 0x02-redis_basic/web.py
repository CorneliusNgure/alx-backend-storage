#!/usr/bin/env python3
"""
Module to fetch web pages and cache results.
"""

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()

def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the result of the page fetch and count accesses.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with caching and access counting.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        redis_client.incr(count_key)

        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode("utf-8")

        result = method(url, *args, **kwargs)

        redis_client.setex(cache_key, 10, result)

        return result

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
