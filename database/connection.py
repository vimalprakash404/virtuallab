import pymongo

# MongoDB connection details
mongo_uri = "mongodb+srv://vimal:GoDyyoGxDppn2bhD@cluster0.kogikhx.mongodb.net"
database_name = "v_lab"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
database = client[database_name]