# test_students.py
import pytest

# Name check
@pytest.mark.asyncio
async def test_create_student_success(async_client):
    payload = {
        "first_name": " Alex ",
        "last_name": " Heartt ",
        "email": " ALEXHEARTT@TEST1.com"
    }

    r = await async_client.post("/student", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["first_name"] == "Alex"
    assert data["last_name"] == "Heartt"
    assert data["email"] == "alexheartt@test1.com"
    assert "id" in data

# Email check
@pytest.mark.asyncio
async def test_create_student_duplicate_email(async_client):
    payload = {
        "first_name": "Grace",
        "last_name": "Hopper",
        "email": "dup@example.com"
    }
    r1 = await async_client.post("/student", json=payload)
    assert r1.status_code == 201

    r2 = await async_client.post("/student", json=payload)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Email already exists"

# Location check
@pytest.mark.asyncio
async def test_create_student_location(async_client):
    payload = {
        "first_name": "Alan",
        "last_name": "Turing",
        "email": "turing@example.com",
    }
    
    r = await async_client.post("/student", json=payload)
    assert r.status_code == 201

    # Header exists and points to the new resource
    assert "Location" in r.headers
    location = r.headers["Location"]
    assert location.startswith("/student")

    # Extract id and check its's an int-like string
    student_id = location.split("/student")[-1]
    assert student_id.isdigit()

     # OPTIONAL (enable later): if you add GET /student/{id}, verify it resolves
    # r2 = await async_client.get(location)
    # assert r2.status_code == 200
    # data = r2.json()
    # assert str(data["id"]) == student_id