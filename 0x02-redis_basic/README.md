# 0x02. Redis Basic
**Back-End | Redis**

This project introduces Redis, an in-memory, NoSQL key-value data store. Redis supports various data structures to manage and retrieve data quickly. This README provides explanations and examples for each data type in Redis and demonstrates how Redis operates as a key-value NoSQL store.

## Table of Contents
1. [Redis Concepts](#redis-concepts)
2. [Redis as a Key-Value NoSQL Store](#redis-as-a-key-value-nosql-store)
3. [Viewing Databases](#-viewing-databases)
4. [Data Types in Redis with Examples](#data-types-in-redis-with-examples)
5. [Using Redis as a Simple Cache](#using-redis-as-a-simple-cache)
6. [Connecting to Redis](#connecting-to-redis)
7. [Setting Up Redis on Ubuntu](#setting-up-redis-on-ubuntu)
8. [Running Redis in a Container](#running-redis-in-a-container)

---

## Redis Concepts
Redis (Remote Dictionary Server) is an in-memory data store known for its speed and support for various data types. It operates as a NoSQL database, storing data as key-value pairs, which makes it flexible for caching, real-time analytics, and messaging.

---

## Redis as a Key-Value NoSQL Store
Redis is often classified as a NoSQL database because it doesn’t rely on the structured tables and relations found in traditional SQL databases. Instead, Redis organizes data in a flexible key-value format where each entry (or "record") has:
- A **key**: Unique identifier for data (like "user:1001").
- A **value**: The associated data, which can be a string, list, set, hash, sorted set, etc.

### Example:
```python
import redis
client = redis.Redis()

# Key-Value pair in Redis
client.set("username:1001", "Alice")
print(client.get("username:1001"))  # Outputs: b'Alice'
```

In Redis, you can't directly create or drop databases in the same way you would in traditional relational databases. However, you can manage which database you're using and switch between them. Here's how to work with databases in the Redis CLI:

## Viewing Databases

Redis does not have a direct command to list all databases like in some SQL systems. However, you can find out how many databases are configured by checking the `databases` parameter in the Redis configuration. By default, there are 16 databases (numbered 0 to 15).

You can see the current configuration in the Redis CLI with the command:

```bash
CONFIG GET databases
```

### Switching Between Databases

To switch between databases, you can use the `SELECT` command followed by the database number (0-15).

```bash
SELECT 1
```

### Creating a Database

Redis does not require you to create a database explicitly. You simply select a database (e.g., `SELECT 1`), and any keys you set will be stored in that database. If the database is empty, it will still exist once you set a key in it.

### Dropping a Database

You cannot drop a database in Redis; however, you can clear all keys from a selected database using the `FLUSHDB` command.

```bash
FLUSHDB
```

### Example Usage in Redis CLI

1. **Open the Redis CLI**:
   ```bash
   redis-cli
   ```

2. **Check the number of databases**:
   ```bash
   CONFIG GET databases
   ```

3. **Switch to a different database**:
   ```bash
   SELECT 1
   ```

4. **Set a key in the selected database**:
   ```bash
   SET mykey "Hello, Redis!"
   ```

5. **Switch to another database**:
   ```bash
   SELECT 2
   ```

6. **Check that the key is not present in the new database**:
   ```bash
   GET mykey  # This should return (nil)
   ```

7. **Switch back to the previous database**:
   ```bash
   SELECT 1
   ```

8. **Retrieve the key**:
   ```bash
   GET mykey  # This should return "Hello, Redis!"
   ```

9. **Flush the current database**:
   ```bash
   FLUSHDB
   ```

### Summary
- You can't explicitly create or drop databases in Redis.
- Use `SELECT` to switch between databases.
- Use `SET` to add keys to a database and `FLUSHDB` to remove all keys from the currently selected database.
- 
---

## Data Types in Redis with Examples

Redis provides several data types that suit different use cases. Here’s a breakdown with examples of how each one works, including CLI syntax for operations.

### 1. **Strings**
Strings are the simplest data type in Redis, used to store text or binary data (e.g., integers, serialized objects).

#### Operations:
- **Set a value**: 
  - **Python**: `client.set("key", "value")`
  - **CLI**: `SET key value`

- **Get a value**: 
  - **Python**: `client.get("key")`
  - **CLI**: `GET key`

- **Set with expiration (TTL)**: 
  - **Python**: `client.setex("key", 5, "value")`
  - **CLI**: `SETEX key 5 value`

- **Check existence**: 
  - **Python**: `client.exists("key")`
  - **CLI**: `EXISTS key`

- **Get TTL**: 
  - **Python**: `client.ttl("key")`
  - **CLI**: `TTL key`

- **Set expiration time**: 
  - **Python**: `client.expire("key", 10)`
  - **CLI**: `EXPIRE key 10`

#### Example:
```python
# Setting a string with expiration
client.setex("temp_key", 5, "temp_value")

# Checking existence of a key
print(client.exists("temp_key"))  # Outputs: 1 (True)

# Getting TTL
print(client.ttl("temp_key"))  # Outputs: 4 (Remaining seconds)

# Setting expiration time
client.expire("temp_key", 10)  # Key will expire in 10 seconds
```

### 2. **Lists**
Lists are ordered collections of strings. Items can be added to the beginning or end, making lists ideal for implementing queues.

#### Operations:
- **Add to the end**: 
  - **Python**: `client.rpush("list", "value")`
  - **CLI**: `RPUSH list value`

- **Add to the front**: 
  - **Python**: `client.lpush("list", "value")`
  - **CLI**: `LPUSH list value`

- **Retrieve items**: 
  - **Python**: `client.lrange("list", 0, -1)`
  - **CLI**: `LRANGE list 0 -1`

- **Remove and get the first item**: 
  - **Python**: `client.lpop("list")`
  - **CLI**: `LPOP list`

- **Remove and get the last item**: 
  - **Python**: `client.rpop("list")`
  - **CLI**: `RPOP list`

- **Set a list item**: 
  - **Python**: `client.lset("list", 0, "new_value")`
  - **CLI**: `LSET list 0 new_value`

- **Check existence**: 
  - **Python**: `client.exists("list")`
  - **CLI**: `EXISTS list`

- **Trim a list to keep a specified range**: 
  - **Python**: `client.ltrim("mylist", start, end)`
  - **CLI**: `LTRIM mylist start end`

- **Insert an item before or after a specified value**: 
  - **Python**: `client.linsert("mylist", "BEFORE", "existing_item", "new_item")`
  - **CLI**: `LINSERT mylist BEFORE existing_item new_item`

- **Remove elements from a list**: 
  - **Python**: `client.lrem("mylist", count, "item")`
  - **CLI**: `LREM mylist count item`

- **Get the length of a list**: 
  - **Python**: `client.llen("mylist")`
  - **CLI**: `LLEN mylist`

- **Get the index of an item in a list**: 
  - **Python**: `client.lindex("mylist", index)`
  - **CLI**: `LINDEX mylist index`

#### Example:
```python
# Adding items to a list
client.rpush("tasks", "task1", "task2", "task3")
client.lpush("tasks", "urgent_task")

# Retrieving list items
print(client.lrange("tasks", 0, -1))  # Outputs: [b'urgent_task', b'task1', b'task2', b'task3']

# Removing and getting the first item
print(client.lpop("tasks"))  # Outputs: b'urgent_task'

# Modifying a list item
client.lset("tasks", 0, "modified_task1")  # Change 'task1' to 'modified_task1'
print(client.lrange("tasks", 0, -1))  # Outputs: [b'modified_task1', b'task2', b'task3']

# Getting the length of the list
print(client.llen("tasks"))  # Outputs: 3
```

### 3. **Sets**
Sets are unordered collections of unique strings. Useful for tracking unique values.

#### Operations:
- **Add members**: 
  - **Python**: `client.sadd("set", "value")`
  - **CLI**: `SADD set value`

- **Get all members**: 
  - **Python**: `client.smembers("set")`
  - **CLI**: `SMEMBERS set`

- **Remove a member**: 
  - **Python**: `client.srem("set", "value")`
  - **CLI**: `SREM set value`

- **Check membership**: 
  - **Python**: `client.sismember("set", "value")`
  - **CLI**: `SISMEMBER set value`

- **Check existence**: 
  - **Python**: `client.exists("set")`
  - **CLI**: `EXISTS set`

#### Example:
```python
# Adding members to a set
client.sadd("tags", "python", "redis", "database")
client.sadd("tags", "redis")  # Duplicate; won't be added

# Getting all set members
print(client.smembers("tags"))  # Outputs: {b'python', b'redis', b'database'}

# Removing a member
client.srem("tags", "redis")

# Checking membership
print(client.sismember("tags", "python"))  # Outputs: True
print(client.sismember("tags", "redis"))  # Outputs: False
```

### 4. **Hashes**
Hashes in Redis are maps of key-value pairs, like a dictionary, stored under a single top-level key. They’re suitable for representing objects with multiple fields.

#### Operations:
- **Set fields**: 
  - **Python**: `client.hset("hash", "field", "value")`
  - **CLI**: `HSET hash field value`

- **Get all fields**: 
  - **Python**: `client.hgetall("hash")`
  - **CLI**: `HGETALL hash`

- **Get a specific field**: 
  - **Python**: `client.hget("hash", "field")`
  - **CLI**: `HGET hash field`

- **Remove a field**: 
  - **Python**: `client.hdel("hash", "field")`
  - **CLI**: `HDEL hash field`

- **Check existence of field**: 
  - **Python**: `client.hexists("hash", "field")`
  - **CLI**: `HEXISTS hash field`

- **Check existence of hash**: 
  - **Python**: `client.exists("hash")`
  - **CLI**: `EXISTS hash`

#### Example:
```python
# Setting fields in a hash
client.hset("user:1001", "name", "Alice")
client.hset("user:1001", "age", 30)

# Getting all fields in the hash
print(client.hgetall("user:1001"))  # Outputs: {b'name': b'Alice', b'age': b'30'}

# Accessing individual fields
print(client.hget("user:1001", "name"))  # Outputs: b'Alice'

# Modifying a field
client.hset("user:1001", "age", 31)  # Change age to 31
print(client.hget("user:1001", "age"))  # Outputs: b'31'

# Deleting a field
client.hdel("user:

1001", "age")
print(client.hgetall("user:1001"))  # Outputs: {b'name': b'Alice'}
```

### 5. **Sorted Sets**
Sorted sets are similar to sets but with an associated score for each member. This score determines the order of members in the set.

#### Operations:
- **Add members with scores**: 
  - **Python**: `client.zadd("sorted_set", {"member": score})`
  - **CLI**: `ZADD sorted_set score member`

- **Get range by score**: 
  - **Python**: `client.zrangebyscore("sorted_set", min, max)`
  - **CLI**: `ZRANGEBYSCORE sorted_set min max`

- **Get members by rank**: 
  - **Python**: `client.zrange("sorted_set", 0, -1)`
  - **CLI**: `ZRANGE sorted_set 0 -1`

- **Remove members**: 
  - **Python**: `client.zrem("sorted_set", "member")`
  - **CLI**: `ZREM sorted_set member`

- **Check existence**: 
  - **Python**: `client.exists("sorted_set")`
  - **CLI**: `EXISTS sorted_set`

#### Example:
```python
# Adding members to a sorted set
client.zadd("leaderboard", {"Alice": 100, "Bob": 200, "Charlie": 150})

# Getting members by rank
print(client.zrange("leaderboard", 0, -1, withscores=True))  # Outputs: [(b'Alice', 100), (b'Charlie', 150), (b'Bob', 200)]

# Getting members by score
print(client.zrangebyscore("leaderboard", 100, 150))  # Outputs: [b'Alice', b'Charlie']

# Removing a member
client.zrem("leaderboard", "Charlie")
print(client.zrange("leaderboard", 0, -1, withscores=True))  # Outputs: [(b'Alice', 100), (b'Bob', 200)]
```

---

## Using Redis as a Simple Cache
Redis can function as an efficient caching layer due to its in-memory nature. Here's a simple example of caching data:

### Example:
```python
import redis
import time

client = redis.Redis()

def get_data(key):
    # Check cache
    cached_value = client.get(key)
    if cached_value:
        return cached_value.decode('utf-8')

    # Simulate a time-consuming operation
    value = "Expensive data from DB"
    client.setex(key, 60, value)  # Cache for 60 seconds
    return value

# Usage
print(get_data("query_1"))  # Fetch from DB and cache
time.sleep(30)
print(get_data("query_1"))  # Fetch from cache
```

---

## Connecting to Redis

### Using Python
To connect to Redis using Python, use the `redis-py` library. Here's a sample connection:

```python
import redis

# Connect to Redis server
client = redis.Redis(host='localhost', port=6379, db=0)

# Test connection
client.set("test_key", "Hello, Redis!")
print(client.get("test_key"))  # Outputs: b'Hello, Redis!'
```

### Using CLI
To connect to Redis using the command-line interface, use the following command:

```bash
redis-cli -h localhost -p 6379
```

Once connected, you can run commands directly in the CLI.

---

## Setting Up Redis on Ubuntu
To install Redis on Ubuntu, follow these steps:

1. **Update package index**:
   ```bash
   sudo apt update
   ```

2. **Install Redis server**:
   ```bash
   sudo apt install redis-server
   ```

3. **Start the Redis server**:
   ```bash
   sudo systemctl start redis.service
   ```

4. **Enable Redis to start on boot**:
   ```bash
   sudo systemctl enable redis.service
   ```

5. **Check if Redis is running**:
   ```bash
   redis-cli ping  # Should return PONG
   ```

---

## Running Redis in a Container
To run Redis in a Docker container, use the following command:

```bash
docker run --name my-redis -d -p 6379:6379 redis
```

This command starts a new Redis container named `my-redis` and maps the host port 6379 to the container's port 6379.

To connect to the Redis container using `redis-cli`, run:

```bash
docker exec -it my-redis redis-cli
```
