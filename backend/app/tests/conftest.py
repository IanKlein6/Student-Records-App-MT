import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport #needed for fastapi testing
from tortoise.contrib.test import finalizer, initializer
from app.main import app  # Ensure this points to the FastAPI app


#Database wide setup for all tests
@pytest.fixture(scope="session", autouse=True)
def initialize_tests():
    initializer(
        modules={"app": ["app.models.student", "app.models.group", "app.models.semester"]},
        db_url="sqlite://:memory:",
        app_label="app"
    )
    yield
    finalizer()

# Async test client using FastAPI and ASGITransport
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client