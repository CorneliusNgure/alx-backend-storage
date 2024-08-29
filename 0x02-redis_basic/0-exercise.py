import redis
import uuid
from typing import Union

"""
Module defines a Cache class that interacts with a
Redis database.
"""


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
