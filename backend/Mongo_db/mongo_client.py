#import os
from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017"
MONGODB_NAME = "pdf_rag"

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]

def get_chunks_collection():
    return db["chunks"]