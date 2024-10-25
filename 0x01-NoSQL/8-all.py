#!/usr/bin/env python3
"""
list all documents of collection module.
"""
from typing import List
import pymongo


def list_all(mongo_collection: pymongo.collection) -> List[any]:
    """
    Lists all documents in a collection.
    """
    return [doc for doc in mongo_collection.find()]
