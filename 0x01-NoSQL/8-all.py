#!/usr/bin/env python3
"""
list all documents of collection module.
"""
from typing import List
from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> List[any]:
    """
    Lists all documents in a collection.
    """
    return [doc for doc in mongo_collection.find()]
