import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the backend directory to avoid path issues
env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/finance_db")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # The 'admin' database command below checks if the connection is actually valid
    client.admin.command('ping')
    db = client.get_database("finance_db")

    result = db.users.delete_many({})
    print(f"Cleanup Successful: Deleted {result.deleted_count} users")

    result2 = db.records.delete_many({})
    print(f"Cleanup Successful: Deleted {result2.deleted_count} records")

    print("\nDatabase completely reset and ready for new data!")

except Exception as e:
    print(f"\nERROR: Could not connect to MongoDB.")
    print(f"Details: {str(e)}")
    print("\nCheck if your MONGO_URI is correct and your MongoDB server is running.")