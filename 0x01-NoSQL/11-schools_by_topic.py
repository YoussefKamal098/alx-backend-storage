#!/usr/bin/env python3
"""
Returns the list of school having a specific topic.
"""

from typing import List, Any


def schools_by_topic(mongo_collection, topic: str) -> List[Any]:
    """
    Returns the list of school having a specific topic.
    mongo_collection: (pymongo.collection.Collection)
    """
    # topic_filter = {
    #     "topics": {
    #         "$elemMatch": {
    #             "$eq": topic,
    #         },
    #     },
    # }
    return [doc for doc in mongo_collection.find({"topics": topic})]
