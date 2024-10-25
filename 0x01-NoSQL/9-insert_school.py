#!/usr/bin/env python3
"""
Inserts a new document in a collection.
"""

from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Inserts a new document in a collection.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
