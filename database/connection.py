import pymongo

# MongoDB connection details
mongo_uri = "mongodb+srv://developer05:ZZDCqMxDZKx1F3Bn@cluster0.h2hmlx6.mongodb.net"
database_name = "v_lab"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
database = client[database_name]
