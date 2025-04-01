import pytest
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.models.claim import Claim

TEST_DB_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_db"


@pytest.fixture()
async def test_db():
    client = AsyncIOMotorClient(TEST_DB_URL)
    db = client[TEST_DB_NAME]
    await init_beanie(database=db, document_models=[Claim])
    yield db
    client.drop_database(TEST_DB_NAME)


@pytest.fixture
async def client(test_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
