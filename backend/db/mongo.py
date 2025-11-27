from pymongo import MongoClient
from backend.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db["users"]
chats_collection = db["chats"]     
messages_collection = db["messages"]