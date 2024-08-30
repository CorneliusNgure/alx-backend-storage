#!/usr/bin/env python3
"""Script that provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient
from collections import Counter

def nginx_stats():
    """
    Function that provides some stats about Nginx logs stored in MongoDB
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

    # Fetch all IP addresses from the collection
    ip_addresses = collection.distinct("ip")
    
    # Count occurrences of each IP address
    ip_counts = Counter(ip for ip in collection.find({}, {"_id": 0, "ip": 1}))
    
    # Get the 10 most common IPs
    top_ips = ip_counts.most_common(10)
    
    print("IPs:")
    for ip, count in top_ips:
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    nginx_stats()
