#!/usr/bin/env python3
"""
Provides stats about Nginx logs stored in MongoDB using aggregation.
"""
from pymongo import MongoClient


def main():
    """
    Provides stats about Nginx logs stored in MongoDB using aggregation.
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Total log count
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Method stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = collection.aggregate([
        {"$match": {"method": {"$in": methods}}},
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])

    # Dictionary to store counts by method
    method_stats = {method: 0 for method in methods}
    for doc in method_counts:
        method_stats[doc["_id"]] = doc["count"]

    for method in methods:
        print(f"\tmethod {method}: {method_stats[method]}")

    # Count for GET requests to /status
    status_check = collection.aggregate([
        {"$match": {"method": "GET", "path": "/status"}},
        {"$count": "status_count"}
    ])
    status_count = next(status_check, {}).get("status_count", 0)
    print(f"{status_count} status check")


if __name__ == "__main__":
    main()
