from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.environ["MONGO_URL"]
MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]


try:
    client = MongoClient(MONGO_URL)

    # Ping MongoDB Atlas
    client.admin.command("ping")

    print("MongoDB Connected Successfully")

    db = client[MONGO_DB_NAME]

    print(f"Database Selected: {MONGO_DB_NAME}")

except Exception as e:
    print(f"MongoDB Connection Failed: {e}")