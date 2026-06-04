from pymongo import MongoClient

from app.config.settings import (
    MONGO_URL,
    MONGO_DB_NAME
)

client = MongoClient(MONGO_URL)

db = client[MONGO_DB_NAME]


essays_collection = db["essays"]

reviewer_notes_collection = db["reviewer_notes"]