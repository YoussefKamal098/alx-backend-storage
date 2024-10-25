#!/usr/bin/env python3
"""
A script for analyzing Nginx request logs stored in a MongoDB database.

This module connects to a MongoDB instance and retrieves
statistics about Nginx request logs.
It provides two primary functions:

1. `print_nginx_request_logs(nginx_collection)`: Analyzes the Nginx
        request logs to display total log counts, HTTP method statistics,
        and the number of GET requests to the /status path.

2. `print_top_ips(server_collection)`: Aggregates and displays the
        top 10 IP addresses making the most requests.
"""
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """
    Prints statistics about Nginx request logs from the
    specified MongoDB collection.

    This function calculates and displays the total number of logs,
    the count of HTTP methods (GET, POST, PUT, PATCH, DELETE),
    and the number of GET requests made to the /status path.

    Args:
        nginx_collection (pymongo.collection.Collection):
            The MongoDB collection containing Nginx request logs.

    Returns:
        None: This function prints the log statistics directly to the console.
    """
    # Total log count
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Method stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = nginx_collection.aggregate([
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
    status_check = nginx_collection.aggregate([
        {"$match": {"method": "GET", "path": "/status"}},
        {"$count": "status_count"}
    ])
    status_count = next(status_check, {}).get("status_count", 0)
    print(f"{status_count} status check")


def print_top_ips(server_collection):
    """
    Prints the top 10 IP addresses with the most requests from the
    specified MongoDB collection.

    This function aggregates request logs by IP address and sorts them
    to find the top 10 IPs that have made the most requests.

    Args:
        server_collection (pymongo.collection.Collection):
            The MongoDB collection containing server request logs.

    Returns:
        None: This function prints the top IPs and their
            request counts directly to the console.
    """
    print("IPs:")
    request_logs = server_collection.aggregate([
        {
            "$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}
        },
        {
            "$sort": {"totalRequests": -1}
        },
        {
            "$limit": 10
        },
    ])

    for request_log in request_logs:
        ip = request_log["_id"]
        ip_requests_count = request_log["totalRequests"]
        print('\t{}: {}'.format(ip, ip_requests_count))


def main():
    """
    Main entry point of the script.

    Establishes a connection to the MongoDB server and calls functions
    to print Nginx request log statistics and
    the top IP addresses making requests.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)


if __name__ == '__main__':
    main()
