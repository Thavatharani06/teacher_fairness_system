import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "teacher_fairness")

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_to_db() -> AsyncIOMotorDatabase:
    global client, db
    if db is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[MONGODB_DB_NAME]
        await ensure_indexes()
    return db


def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("Database is not initialized. Call connect_to_db first.")
    return db


async def ensure_indexes() -> None:
    database = client[MONGODB_DB_NAME]
    evaluations = database["evaluations"]
    await evaluations.create_index("teacher")
    await evaluations.create_index("fairness_result")
    await evaluations.create_index([("teacher", 1), ("fairness_result", 1)])
