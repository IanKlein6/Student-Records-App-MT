# app/tests/conftest.py
import os
import pytest
import httpx
from tortoise import Tortoise
from backend.app.api import app

@pytest.fixture(scope="session", autouse=True)
def _testing_env():
    os.environ["TESTING"] = "1"
    yield

@pytest.fixture(scope="function")
async def db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.student", "app.models.group", "app.models.semester"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.fixture
async def async_client(db):
    import httpx
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
