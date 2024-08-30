#!/usr/bin/env python3
"""
Script of a function that returns list of schools having
a specific topic
"""

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    mongo_collection: pymongo collection object
    topic: Topic to search for (string)
    return: List of schools (documents) that have the specific topic
    """
    filter_query = {'topics': topic}

    result = mongo_collection.find(filter_query)

    return list(result)
