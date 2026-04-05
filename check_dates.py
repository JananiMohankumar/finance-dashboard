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
    db = client.get_database("finance_db")
    print("Connected to database")
    
    records = list(db.records.find().limit(5))
    for r in records:
        print(f"Record ID: {r['_id']}, Date field: {type(r.get('date'))}, Value: {r.get('date')}")

except Exception as e:
    print(f"Error: {e}")
