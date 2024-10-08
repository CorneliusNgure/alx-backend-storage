#!/usr/bin/env python3
"""
Module defines classes and methods that interacts with a
Redis database.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    The count is stored in Redis using a key based on
    the method's qualified name.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with the counting
        functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Records the input args and output of the decorated
        function in Redis lists.

        Args:
            self: Instance of the class to which the method belongs.
            *args: Positional arguments passed to the original method.
            **kwargs: Keyword arguments passed to the original method.

        Returns:
            The result of the original method call.
        """
        key = method.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        normalized_args = str(args)
        self._redis.rpush(input_key, normalized_args)

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls for a given function.

    Args:
        method (Callable): The function whose history is to be displayed.

    Returns:
        None
    """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """
    Cache class provides methods to interact with a
    Redis instance.
    It allows storing various data types in Redis with
    randomly generated keys.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """

    def __init__(self):
        """
        Initializes the Cache class by setting up a Redis
        client. Flushing the database ensures it starts empty.

        Args:
            None

        Returns:
            None
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis database with
        a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data
            to be stored in Redis (str, bytes, int, float).

        Returns:
            str: The key associated with the stored data in
            Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[
        str, bytes, int, float]]] = None) -> Optional[Union[
            str, bytes, int, float]]:
        """
        Retrieves data from the Redis database using the given key.
        An optional Callable can be passed to convert the data
        back to the desired format.

        Args:
            key(str): Key used to retrieve the data from Redis.
            fn (Optional[Callable[[bytes], Union[str, bytes,
            int, float]]]): A callable to convert the data.
            Defaults to None, returning the raw byte string.

        Returns:
            Optional[Union[str, bytes, int, float]]: The data
            retrieved from Redis.
            Returns None if the key does not exist.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis and converts it to UTF-8 string.

        Args:
            key(str): The key used to retrieve the data from Redis.

        Returns:
            Optional[str]: Data converted to a string,
            or None if the key does not exist.
        """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis and converts it to an int.

        Args:
            key(str): Key used to retrieve the data from Redis.

        Returns:
            Optional[int]: Data converted to an int,
            or None if the key does not exist.
        """
        return self.get(key, fn=int)
