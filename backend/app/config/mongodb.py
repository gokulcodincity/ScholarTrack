from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.config.settings import (
    MONGO_URL,
    MONGO_DB_NAME
)

from app.models.essay import Essay
from app.models.reviewer_note import ReviewerNote


async def init_mongodb():

    client = AsyncMongoClient(
        MONGO_URL
    )

    database = client[
        MONGO_DB_NAME
    ]

    await init_beanie(
        database=database,
        document_models=[
            Essay,
            ReviewerNote
        ]
    )

    print("MongoDB ODM Connected Successfully")