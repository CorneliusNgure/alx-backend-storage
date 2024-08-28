#!/usr/bin/env python3
"""
Updates the topics filed for all documents in the collection
that match the given name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the 'topics' field for all documents in the 
    collection that match the given name.

    mongo_collection: pymongo collection object
    name: School name to match (string)
    topics: List of topics to set for the matching documents
    return: The result of the update operation
    """
    filter_query = {'name': name}

    update_operation = {'$set': {'topics': topics}}

    result = mongo_collection.update_many(filter_query, update_operation)

    return result
