import pytest
from datetime import datetime, timedelta
from jose import jwt
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.auth.models import User
from app.main import app
from app.claims.models import Claim

TEST_DB_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_db"


@pytest.fixture()
async def test_db():
    client = AsyncIOMotorClient(TEST_DB_URL)
    db = client[TEST_DB_NAME]
    await init_beanie(database=db, document_models=[Claim, User])
    yield db
    client.drop_database(TEST_DB_NAME)


@pytest.fixture
async def client(test_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def test_user() -> User:
    user = await User.insert_one(User(email="user@example.com", hashed_password="fake"))
    return user


@pytest.fixture
def create_token(test_user):
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(test_user.id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
