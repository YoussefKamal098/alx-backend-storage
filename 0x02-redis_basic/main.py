#!/usr/bin/env python3

from exercise import Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    print(value, type(value), type(cache.get(key, fn=fn)))
    assert cache.get(key, fn=fn) == value
