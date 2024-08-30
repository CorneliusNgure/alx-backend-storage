#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def nginx_stats():
    """
    Function hat provides some stats about Nginx logs stored in     MongoDB
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    log_count = collection.count_documents({})
    print(f"{log_count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_count = collection.count_documents({
        "method": "GET", "path": "/status"
        })
    print(f"{status_count} status check")


if __name__ == "__main__":
    nginx_stats()
