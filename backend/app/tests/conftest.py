import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from httpx import ASGITransport  # ✅ Needed for FastAPI app testing
from tortoise.contrib.test import finalizer, initializer
from app.main import app  # ✅ Ensure this points to the FastAPI app

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def initialize_tests():
    initializer(
        ["app.models.student", "app.models.group", "app.models.semester"],
        db_url="sqlite://:memory:",
        app_label="models"
    )
    yield
    finalizer()
