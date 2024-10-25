#!/usr/bin/env python3
"""
Inserts a new document in a collection.
"""


def insert_school(mongo_collection, **kwargs) -> str:
    """
    Inserts a new document in a collection.
    mongo_collection: (pymongo.collection.Collection)
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
