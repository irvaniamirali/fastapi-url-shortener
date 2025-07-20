import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app as fastapi_app
from app.database.base import Base
from app.api.v1.deps import get_db
from fastapi_limiter import FastAPILimiter
from httpx import ASGITransport

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    yield engine
    asyncio.get_event_loop().run_until_complete(engine.dispose())

@pytest.fixture(scope="session")
async def create_test_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(test_engine, create_test_db):
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture(scope="function")
async def async_client(db_session, monkeypatch):
    # Override get_db dependency
    async def override_get_db():
        yield db_session
    fastapi_app.dependency_overrides[get_db] = override_get_db

    # Mock FastAPILimiter for tests (disable rate limiting)
    class DummyRedis:
        async def evalsha(self, *args, **kwargs):
            return 1
    monkeypatch.setattr(FastAPILimiter, "redis", DummyRedis())
    async def dummy_identifier(request):
        return "test-identifier"
    monkeypatch.setattr(FastAPILimiter, "identifier", dummy_identifier)

    async def dummy_callback(request, response, pexpire):
        return None
    monkeypatch.setattr(FastAPILimiter, "http_callback", dummy_callback)

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def user_data():
    return {"email": "testuser@example.com", "password": "testpass123"}

@pytest.fixture
async def create_user(async_client, user_data):
    resp = await async_client.post("/api/v1/auth/register", json=user_data)
    return resp

@pytest.fixture
async def user_token(async_client, user_data, create_user):
    resp = await async_client.post("/api/v1/auth/token", data={"username": user_data["email"], "password": user_data["password"]})
    return resp.json()["access_token"]
