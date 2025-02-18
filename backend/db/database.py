from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.Medical_records  # Connect to the `Medical_records` database
users_collection = db.users  # Collection inside `Medical_records`
