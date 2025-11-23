# app/tests/conftest.py

"""API testing Database Factory.

Creation and configuration of a temporary Database for testing purposes only.

Provides fixtures for isolated database testing:
    - Temporary in-memory SQLite database (created per test function)
    - Async HTTP client configured for FastAPI testing
    - Testing environment flag to prevent production DB connection

Fixtures:
    _testing_env: Sets TESTING=1 environment variable for entire test session
    db: Creates and tears down temporary test database for each test function
    async_client: Provides configured httpx AsyncClient with test database

Info:
    if api.py changes model path naming to adding backend. to the front of the import make sure to change it here!
"""

import os

import httpx
import pytest
from tortoise import Tortoise

from backend.app.api import app


@pytest.fixture(scope="session", autouse=True)
def _testing_env():
    """Set TESTING environment variable to prevent production database connection."""
    os.environ["TESTING"] = "1"
    yield


@pytest.fixture(scope="function")
async def db():
    """Initialize temporary in-memory database for testing.

    Creates a fresh SQLite database for each test function with all models registered. Database is automatically cleaned up after test completes.
    """
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "app.models.student",
                "app.models.group",
                "app.models.semester",
                "app.models.archive_log",
            ]
        },
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def async_client(db):
    """Provide async HTTP client for API testing.

    Configured with ASGI transport for direct FastAPI integration.
    Requires db fixture to ensure database is initialized before requests.
    """
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
