#!/usr/bin/env python3
"""
Returns all students in a collection sorted by average score.
"""
from typing import Dict, Any


def top_students(mongo_collection) -> Dict[str, Any]:
    """
    Returns all students in a collection sorted by average score.
    mongo_collection: (pymongo.collection.Collection)
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "averageScore": {
                    "$avg": {
                        "$avg": "$topics.score",
                    },
                },
                "topics": 1,
            },
        },
        {
            "$sort": {"averageScore": -1},
        },
    ])
