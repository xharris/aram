from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI')
MONGO_NAME = os.getenv('MONGO_NAME')

client = MongoClient(MONGO_URI)
db = client[MONGO_NAME]