#!/usr/bin/env python3
"""
Changes all topics of a collection's document based on the name.
"""

from typing import List


def update_topics(mongo_collection, name: str, topics: List[str]) -> None:
    """
    Changes all topics of a collection's document based on the name.
    mongo_collection: (pymongo.collection.Collection)
    """

    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
