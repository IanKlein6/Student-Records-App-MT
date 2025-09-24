#conftest.py
import pytest, asyncio, os
from httpx import AsyncClient, ASGITransport #needed for fastapi testing
from tortoise import Tortoise
from tortoise.contrib.test import getDBConfig
from app.models.student import Student
from app.main import app  # Ensure this points to the FastAPI app

@pytest.fixture(scope="session", autouse=True)
def _testing_env():
    os.environ["TESTING"] = "1"
    yield

# Points Tortoise to your models module. Add models as needed
MODELS = {"models": [
    "app.models.student",
    "app.models.group",
    "app.models.semester",
]} 

#Generation of session DB
@pytest.fixture(autouse=True, scope="session")
async def init_test_db():
    # Isolated SQLite in-memory DB for the whole test session
    await Tortoise.init(db_url="sqlite://:memory:", modules=MODELS)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

# Async test client using FastAPI and ASGITransport
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def _clean_tables():
    # wipe students; add others as needed
    await Student.all().delete()
    yield