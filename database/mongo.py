from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['Proj']
collection = db['products']

collection.insert_one({"_id": 2, "name": "keyword", "price": 300})
