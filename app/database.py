import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.claims.models import Claim
from app.auth.models import User

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["claims_db"]


async def init_db():
    await init_beanie(database=db, document_models=[Claim, User])
