# backend/app/tests/test_api.py

"""API health check and basic endpoints

Tests the core FastAPI application endpoints to verify.
  - Application is properly configured and running
  - Health check endpoint returns expected response.
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(async_client):
    """Test root health check endpoint returns OK status."""
    response = await async_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
