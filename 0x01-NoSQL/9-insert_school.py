#!/usr/bin/env python3
from pymongo import MongoClient
"""Insert a document"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection.

    :mongo_collection: pymongo collection object
    :kwargs: Fields and values for the new document
    :return: The _id of the inserted document
    """

    result = mongo_collection.insert_one(kwargs)

    return result.inserted_id
