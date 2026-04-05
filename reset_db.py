import os
from pymongo import MongoClient

# Use the exact Mongo URI from the user's Render setup
MONGO_URI = "mongodb+srv://jananimohan:janani2004@cluster0.lnpz75r.mongodb.net/finance_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database("finance_db")

# Delete all users
result = db.users.delete_many({})
print("Deleted users:", result.deleted_count)

# Delete all records just in case
result2 = db.records.delete_many({})
print("Deleted records:", result2.deleted_count)

print("Database completely reset! Ready for a new Admin.")
