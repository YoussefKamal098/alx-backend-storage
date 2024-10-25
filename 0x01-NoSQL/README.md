# 0x01-NoSQL Project: MongoDB and Python

## Overview

This project covers working with NoSQL databases, specifically MongoDB, and demonstrates its interaction with Python through PyMongo. You will learn how to perform CRUD operations, build advanced queries, and work with MongoDB aggregation pipelines. We'll also explore Object Data Modeling (ODM) with MongoEngine and how to integrate MongoDB into Python applications. By the end of this project, you'll understand core MongoDB operations, aggregation techniques, and the power of MongoDB in modern applications.

---

## Table of Contents

- [General Concepts](#general-concepts)
- [Project Requirements](#project-requirements)
- [Setting Up MongoDB on Ubuntu 18.04](#setting-up-mongodb-on-ubuntu-1804)
- [Common MongoDB Commands](#common-mongodb-commands)
- [Creating and Dropping Collections](#creating-and-dropping-collections)
- [MongoDB Aggregations, Filters, Joins, and More](#mongodb-aggregations-filters-joins-and-more)
  - [MongoDB Aggregations](#mongodb-aggregations)
  - [Aggregation Stages](#aggregation-stages)
  - [PyMongo Aggregation Examples](#pymongo-aggregation-examples)
  - [MongoDB Aggregation Pipeline Operators](#mongodb-aggregation-pipeline-operators)
  - [MongoEngine Overview](#mongoengine-overview)
- [Example Python Scripts](#example-python-scripts)
  - [Basic CRUD Operations with PyMongo](#basic-crud-operations-with-pymongo)
  - [Using MongoEngine with MongoDB](#using-mongoengine-with-mongodb)

---

## General Concepts

1. **NoSQL:**
   - **Definition**: NoSQL stands for "Not Only SQL," encompassing a wide range of database technologies that prioritize flexibility and scalability over the rigid structures of traditional relational databases.
   - **Key Characteristics**:
     - **Flexible Schemas**: NoSQL databases allow for dynamic schemas, meaning that different records can have different fields, which is especially useful for handling unstructured or semi-structured data.
     - **Horizontal Scalability**: Many NoSQL databases are designed to scale out by distributing data across multiple servers. This makes them well-suited for handling large volumes of data and high-velocity transactions.
     - **Use Cases**: Commonly used in applications requiring rapid changes in data structure, like social media, big data analytics, content management systems, and real-time web applications.

2. **SQL vs. NoSQL:**
   - **SQL Databases**:
     - **Structure**: Use Structured Query Language (SQL) for defining and manipulating data, with a strict table-based schema where each row must adhere to the same structure.
     - **Examples**: MySQL, PostgreSQL, Oracle.
   - **NoSQL Databases**:
     - **Structure**: Store data in various formats, including key-value pairs, wide-column stores, document stores, and graph databases, allowing for more flexibility in data modeling.
     - **Example**: MongoDB stores data in JSON-like documents (BSON format), which can have different fields and structures within the same collection.
   - **Choosing Between Them**: The choice between SQL and NoSQL often depends on the specific requirements of the application, such as the need for complex transactions (favoring SQL) or the necessity for high scalability and flexibility (favoring NoSQL).

3. **MongoDB:**
   - **Overview**: MongoDB is one of the most popular NoSQL databases, designed to handle large volumes of data with a focus on high availability and performance.
   - **Data Storage**: It uses BSON (Binary JSON) format for storing data, which allows for rich data types and nested structures. This enables developers to store complex data in a single document rather than breaking it into multiple tables.
   - **Use Cases**: Ideal for applications requiring rapid development and iteration, such as e-commerce platforms, content management systems, and real-time analytics.

4. **ACID and Eventual Consistency:**
   - **ACID Properties**: Traditional SQL databases adhere to ACID principles:
     - **Atomicity**: Ensures that all operations within a transaction are completed successfully or none at all.
     - **Consistency**: Guarantees that a transaction will bring the database from one valid state to another.
     - **Isolation**: Ensures that transactions are processed independently, without interference.
     - **Durability**: Guarantees that once a transaction has been committed, it will remain so, even in the event of a failure.
   - **Eventual Consistency in MongoDB**: While MongoDB provides ACID-like guarantees for single-document transactions and collections through multi-document transactions, it generally operates on an eventual consistency model. This means that updates may not be immediately visible to all clients, but the system will eventually converge to a consistent state.
   - **Transaction Support**: In newer versions, MongoDB supports multi-document transactions, which can provide ACID properties at the collection level, allowing for more complex operations.

5. **Benefits of MongoDB:**
   - **Flexibility**: The ability to use dynamic, schema-less data models allows developers to adapt to changing application requirements without the overhead of migrating a rigid database schema.
   - **Horizontal Scaling**: MongoDB's architecture supports sharding, which distributes data across multiple servers. This makes it easier to scale out by adding more nodes to the system as data volumes grow.
   - **Fast Development**: The flexible schema accelerates application development by allowing rapid iterations and changes to data models, which is beneficial in agile environments and fast-paced projects.

---

## Project Requirements

- **MongoDB Command File:**
   - MongoDB version: 4.2, compatible with Ubuntu 18.04.
   - Each script should follow the `pycodestyle` style guide.
   - Files should end with a newline.

- **Python Requirements:**
   - Python version: 3.7 and PyMongo 3.10.
   - Use `#!/usr/bin/env python3` in Python scripts.
   - Each module must have documentation.

---

## Setting Up MongoDB on Ubuntu 18.04

To install MongoDB on Ubuntu:

```bash
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```

Verify the installation:

```bash
$ mongo --version
MongoDB shell version v4.2.8
```

Install PyMongo:

```bash
$ pip3 install pymongo
```

---

## Creating and Dropping Collections

### Creating Collections

In MongoDB, you can create a collection simply by inserting a document. However, you can also explicitly create a collection:

```bash
db.createCollection("myCollection")
```

### Dropping Collections

To drop (delete) a collection from the database, use:

```bash
db.myCollection.drop()
```

---

## Common MongoDB Commands

1. **List Databases:**
   ```bash
   $ mongo --eval 'db.adminCommand({ listDatabases: 1 })'
   ```

2. **Create or Use Database:**
   ```bash
   use my_db
   ```

3. **Insert Document:**
   ```bash
   db.school.insertOne({ name: "Holberton school" })
   ```

4. **Find All Documents:**
   ```bash
   db.school.find()
   ```

5. **Update Document:**
   ```bash
   db.school.updateOne({ name: "Holberton school" }, { $set: { address: "972 Mission Street" } })
   ```

6. **Delete Document:**
   ```bash
   db.school.deleteOne({ name: "Holberton school" })
   ```

### Example using PyMongo

Here's how to create and drop collections using PyMongo:

```python
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.my_db

# Create a collection
db.create_collection("myCollection")

# Insert a document into the collection
db.myCollection.insert_one({"name": "Sample Document"})

# Drop the collection
db.myCollection.drop()
```

---

##MongoDB Aggregations, Filters, Joins, and More

MongoDB’s aggregation framework is one of its most powerful features. It allows for advanced data manipulation and transformation via pipelines. The aggregation pipeline consists of stages, each stage performing an operation on the documents passed to it, similar to the UNIX pipeline. 

---

### MongoDB Aggregations

#### Fundamental Aggregation Syntax

An aggregation pipeline is an array of stages that process data step-by-step. Key pipeline stages include:

- **`$match`**: Filters documents (similar to SQL `WHERE` clause).
- **`$group`**: Groups documents based on a specified key (similar to SQL `GROUP BY`).
- **`$sort`**: Sorts the documents.
- **`$project`**: Reshapes the documents by including, excluding, or creating new fields.
- **`$lookup`**: Joins data from other collections (similar to SQL `JOIN`).
  
---

### Aggregation Stages & Examples

1. **`$match`:** 
   Filters documents to pass to the next stage.
   ```json
   db.orders.aggregate([{ $match: { status: "shipped" }}])
   ```

2. **`$group`:** 
   Groups documents and can perform accumulations (like sum, avg).
   ```json
   db.sales.aggregate([{ $group: { _id: "$region", totalSales: { $sum: "$amount" }}}])
   ```

3. **`$sort`:**
   Sorts documents by the specified field.
   ```json
   db.users.aggregate([{ $sort: { age: 1 }}])
   ```

4. **`$project`:**
   Reshapes documents, including/excluding fields, and creating new fields.
   ```json
   db.products.aggregate([{ $project: { name: 1, priceWithTax: { $multiply: ["$price", 1.2] }}}])
   ```

5. **`$lookup`:**
   Performs a left outer join to another collection.
   ```json
   db.orders.aggregate([{ 
     $lookup: {
        from: "customers",
        localField: "cust_id",
        foreignField: "_id",
        as: "order_details"
     }
   }])
   ```

---

### PyMongo Aggregation Examples

Here’s how you can run some of the above aggregations using PyMongo:

1. **`$match` in PyMongo:**
   ```python
   from pymongo import MongoClient

   client = MongoClient('localhost', 27017)
   db = client.my_db
   pipeline = [{'$match': {'status': 'shipped'}}]
   result = list(db.orders.aggregate(pipeline))
   print(result)
   ```

2. **`$group` in PyMongo:**
   ```python
   pipeline = [
       {"$group": {"_id": "$region", "totalSales": {"$sum": "$amount"}}}
   ]
   result = list(db.sales.aggregate(pipeline))
   print(result)
   ```

3. **`$sort` in PyMongo:**
   ```python
   pipeline = [{'$sort': {'age': 1}}]
   result = list(db.users.aggregate(pipeline))
   print(result)
   ```

4. **`$project` in PyMongo:**
   ```python
   pipeline = [
       {"$project": {"name": 1, "priceWithTax": {"$multiply": ["$price", 1.2]}}}
   ]
   result = list(db.products.aggregate(pipeline))
   print(result)
   ```

5. **`$lookup` in PyMongo:**
   ```python
   pipeline = [
       {
           '$lookup': {
               'from': 'customers',
               'localField': 'cust_id',
               'foreignField': '_id',
               'as': 'order_details'
           }
       }
   ]
   result = list(db.orders.aggregate(pipeline))
   print(result)
   ```
---

### MongoEngine Overview

**MongoEngine** is an ODM (Object-Document Mapper) for MongoDB in Python, providing a high-level abstraction to work with MongoDB in an object-oriented way. With MongoEngine, you define your data schema using Python classes, making it easier to manage data.

#### Basic Usage of MongoEngine

1. **Connect to Database:**
   ```python
   from mongoengine import connect
   connect('my_db')
   ```

2. **Define a Document Schema:**
   ```python
   from mongoengine import Document, StringField, IntField

   class User(Document):
       name = StringField(required=True)
       age = IntField()
   ```

3. **Create and Save a Document:**
   ```python
   user = User(name="Alice", age=30)
   user.save()
   ```

4. **Querying Documents:**
   ```python
   users = User.objects()
   for user in users:
       print(user.name, user.age)
   ```

5. **Updating Documents:**
   ```python
   user = User.objects(name="Alice").first()
   user.age = 31
   user.save()
   ```

6. **Deleting Documents:**
   ```python
   user.delete()
   ```

---

## Example Python Scripts

### Basic CRUD Operations with PyMongo

Here's a script demonstrating basic CRUD operations using PyMongo:

```python
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.my_db

# Create a collection
db.create_collection("users")

# Create: Insert a document
db.users.insert_one({"name": "Alice", "age": 30})

# Read: Retrieve documents
users = db.users.find()
for user in users:
    print(user)

# Update: Modify a document
db.users.update_one({"name": "Alice"}, {"$set": {"age": 31}})

# Delete: Remove a document
db.users.delete_one({"name": "Alice"})
```

### Using MongoEngine with MongoDB

Here's a script demonstrating basic CRUD operations using MongoEngine:

```python
from mongoengine import Document, StringField, IntField, connect

# Connect to MongoDB
connect('my_db')

# Define a User model
class User(Document):
    name = StringField(required=True)
    age = IntField()

# Create: Add a new user
new_user = User(name="Alice", age=30)
new_user.save()

# Read: Retrieve all users
all_users = User.objects()
for user in all_users:
    print(f"Name: {user.name}, Age: {user.age}")

# Update: Modify user information
user_to_update = User.objects(name="Alice").first()
if user_to_update:
    user_to_update.age = 31
    user_to_update.save()

# Delete: Remove a user
user_to_delete = User.objects(name="Alice").first()
if user_to_delete:
    user_to_delete.delete()
```

---
### Summary
In summary, the statement emphasizes that while SQL databases inherently provide robust ACID properties for transactions, MongoDB traditionally favored eventual consistency for better scalability and performance. However, with the introduction of multi-document transactions, MongoDB now offers the option to achieve ACID guarantees, though primarily at the collection level rather than across the entire database. This flexibility allows developers to choose the level of consistency they need based on their application's requirements.

This explanation covers the basics, and to learn more about these concepts and MongoDB's functionalities, refer to the [official MongoDB documentation](https://docs.mongodb.com/manual/) and [official MongoEngine documentation](https://mongoengine.readthedocs.io/).
