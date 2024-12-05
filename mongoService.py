from pymongo import MongoClient
from bson import ObjectId
import os

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE')



client = MongoClient('f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource={MONGO_AUTH_SOURCE}&directConnection=true"')

db = client[MONGO_DATABASE]

def process_query(query):
    if "_id" in query and isinstance(query["_id"], str):
        query["_id"] = ObjectId(query["_id"])
    return query

def find(collection_name, query):
    collection = db[collection_name]

    query = process_query(query)
    
    return list(collection.find(query))

def update_one(collection_name, query, new_values):
    collection = db[collection_name]

    query = process_query(query)
    new_values = {"$set": new_values}

    collection.update_one(query, new_values)



