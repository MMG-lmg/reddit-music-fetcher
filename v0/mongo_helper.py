from pymongo import MongoClient
import json_io

def get_default_client():
    return MongoClient('localhost', 27017);

def insert_many(filename,db_name,collection_name):
    data = json_io.load_data(filename)
    
    client = get_default_client()
    db = client[db_name]
    collection = db[collection_name]
    
    result = collection.insert_many(data)
    print(result.inserted_ids)