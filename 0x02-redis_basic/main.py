#!/usr/bin/env python3

# ------------------------------- test store method -----------------------------------
# import redis
# from exercise import Cache
#
# cache = Cache()
#
# data = b"hello"
# key = cache.store(data)
# print(key)
#
# local_redis = redis.Redis()
# print(local_redis.get(key))


# ------------------------------- test get method -----------------------------------
# from exercise import Cache
#
# cache = Cache()
#
# TEST_CASES = {
#     b"foo": None,
#     123: int,
#     "bar": lambda d: d.decode("utf-8")
# }
#
# for value, fn in TEST_CASES.items():
#     key = cache.store(value)
#     print(value, type(value), type(cache.get(key, fn=fn)))
#     assert cache.get(key, fn=fn) == value


# ------------------------------- test count_call decorator -----------------------------------
# from exercise import Cache
#
# cache = Cache()
#
# cache.store(b"first")
# print(cache.get(cache.store.__qualname__))
#
# cache.store(b"second")
# cache.store(b"third")
# print(cache.get(cache.store.__qualname__))

# ------------------------------- test call_history decorator -----------------------------------
from exercise import Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("second")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))
