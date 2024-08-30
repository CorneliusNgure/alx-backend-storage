#!/usr/bin/env python3
"""
Returns all students sorted by average score from a
MongoDB collection.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score from a
    MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The pymongo collection object.

    Returns:
        list: A list of dictionaries, each containing the
        student's data and their average score, sorted by
        average score in descending order.
    """

    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {
                    "$avg": "$scores"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    result = list(mongo_collection.aggregate(pipeline))

    return result
