from pymongo import MongoClient

client = MongoClient("mongo")
db = client["InstaChess"]
users = db["users"]
games = db["games"]