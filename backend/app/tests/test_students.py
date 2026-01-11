# app/tests/test_students.py

"""Unit tests for student  CRUD operations and lifecycle management.

Tests the /students endpoints for creating, retrieving, updating, archiving, and deleting student records. Validates data validation, error handling, and business logic enforcement.

Test Coverage
    Creation (POST /students):
        test_create_student: Successful creation with whitespace trimming
        test_create_student_422_missing: Missing required fields
        test_create_student_422_bad_email: Invalid email format
        test_create_student_422_invalid_semester: Non-existent semester FK
        test_create_student_duplicate_email: Duplicate email rejection (409)
        test_create_student_location: Location header validation

    Retrieval (GET /students/{id}):
        test_get_student_200: Successful retrieval of an existing student
        test_get_student_404: Non-existent student

    Update (PATCH /students{id}):
        test_patch_student_200: Successful updating of a students field
        test_patch_student_409_duplicate_email: Email uniqueness enforcement
        test_patch_student_404: Non-existent student.

    Lifecycle Management:
        test_archive_then_restore: Archive - status=archived - restore - status=active
        test_archive_restore_404: Archive/restore non-existent students

        test_delete_student_404: Archive/restore non-existent students
        test_delete_students_not_allowed: Non-admin hard delete success (in production is disabled)
        test_admin_hard_delete: Admin hard delete (permanent removal)

Fixtures
    _create: Helper to create test students with default values
    async_client: Configured httpx client (from conftest.py)
    db: Temporary in-memory database (from conftest.py)
"""

import pytest


# Create student in memory for testing below
async def _create(async_client, first_name, last_name, email):
    """Helper to create a student. Requires all fields explicitly."""
    r = await async_client.post(
        "/students", json={"first_name": first_name, "last_name": last_name, "email": email}
    )
    assert r.status_code == 201, r.text
    return r.json()


# 200: GET existing by ID
@pytest.mark.asyncio
async def test_get_student_200(async_client):
    s = await _create(async_client, first_name="John", last_name="Doe", email="get@test.com")
    r = await async_client.get(f"/students/{s['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == s["id"]
    assert data["email"] == "get200@test.com"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


# 404: GET non-existent
@pytest.mark.asyncio
async def test_get_student_404(async_client):
    r = await async_client.get("/students/999999")
    assert r.status_code == 404


# 200: PATCH existing (update first_name)
@pytest.mark.asyncio
async def test_patch_student_200(async_client):
    s = await _create(async_client, email="patch200@test.com")
    r = await async_client.patch(f"/students/{s['id']}", json={"first_name": "New"})
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == s["id"]
    assert data["first_name"] == "New"


# 404: PATCH non-existent
@pytest.mark.asyncio
async def test_patch_student_404(async_client):
    r = await async_client.patch("/students/999999", json={"first_name": "New"})
    assert r.status_code == 404


# 422: missing required fields
@pytest.mark.asyncio
async def test_create_student_422_missing(async_client):
    r = await async_client.post("/students", json={"first_name": "A"})
    assert r.status_code == 422


# 422: bad email
@pytest.mark.asyncio
async def test_create_student_422_bad_email(async_client):
    r = await async_client.post(
        "/students", json={"first_name": "A", "last_name": "B", "email": "not-an-email"}
    )
    assert r.status_code == 422


# 404 DELETE non-existent
@pytest.mark.asyncio
async def test_delete_student_404(async_client):
    r = await async_client.delete("/students/999999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_student_422_invalid_semester(async_client):
    r = await async_client.post(
        "/students",
        json={
            "first_name": "Fk",
            "last_name": "Error",
            "email": "fkerror@example.com",
            "semester_id": 999999,
        },
    )
    assert r.status_code == 422


# CREATE student
@pytest.mark.asyncio
async def test_create_student(async_client):
    payload = {"first_name": " Alex ", "last_name": " Heartt ", "email": " ALEXHEARTT@TEST1.com"}

    r = await async_client.post("/students", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["first_name"] == "Alex"
    assert data["last_name"] == "Heartt"
    assert data["email"] == "alexheartt@test1.com"
    assert "id" in data


# Email check
@pytest.mark.asyncio
async def test_create_student_duplicate_email(async_client):
    payload = {"first_name": "Grace", "last_name": "Hopper", "email": "dup@example.com"}
    r1 = await async_client.post("/students", json=payload)
    assert r1.status_code == 201

    r2 = await async_client.post("/students", json=payload)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Email already exists"


@pytest.mark.asyncio
async def test_patch_student_409_duplicate_email(async_client):
    _s1 = await _create(
        async_client, email="dup1@ex.com"
    )  # "_" in _s1 is used to fix a ruff flag since s1 isn't being called at the moment.
    s2 = await _create(async_client, email="dup2@ex.com")
    r = await async_client.patch(f"/students/{s2['id']}", json={"email": "dup1@ex.com"})
    assert r.status_code == 409


# Location check
@pytest.mark.asyncio
async def test_create_student_location(async_client):
    payload = {
        "first_name": "Alan",
        "last_name": "Turing",
        "email": "turing@example.com",
    }

    r = await async_client.post("/students", json=payload)
    assert r.status_code == 201

    # Header exists and points to the new resource
    assert "Location" in r.headers
    location = r.headers["Location"]
    assert location.startswith("/students/")

    # Extract id and check its's an int-like string
    student_id = location.rsplit("/", 1)[-1]
    assert student_id.isdigit()


# Archive + restore flow
@pytest.mark.asyncio
async def test_archive_then_restore(async_client):
    s = await _create(async_client, email="arc@test.com")
    sid = s["id"]

    r = await async_client.post(f"/students/{sid}/archive")
    assert r.status_code == 204

    r2 = await async_client.get(f"/students/{sid}")
    assert r2.status_code == 200
    assert r2.json()["status"] == "archived"

    r3 = await async_client.post(f"/students/{sid}/restore")
    assert r3.status_code == 204

    r4 = await async_client.get(f"/students/{sid}")
    assert r4.status_code == 200
    assert r4.json()["status"] == "active"


# Hard delete (admin)
@pytest.mark.asyncio
async def test_admin_hard_delete(async_client):
    s = await _create(async_client, email="harddel@test.com")
    sid = s["id"]

    # In tests TESTING=1 bypasses auth; if disabled, pass header {"X-Admin-Token": "dev-admin"}
    r = await async_client.delete(f"/admin/students/{sid}")
    assert r.status_code == 204

    r2 = await async_client.get(f"/students/{sid}")
    assert r2.status_code == 404


# 404 on archive/restore non-existent
@pytest.mark.asyncio
async def test_archive_restore_404(async_client):
    r = await async_client.post("/students/999999/archive")
    assert r.status_code == 404
    r2 = await async_client.post("/students/999999/restore")
    assert r2.status_code == 404


# Ensure DELETE /students/{id} is gone (405)
@pytest.mark.asyncio
async def test_delete_students_not_allowed(async_client):
    s = await _create(async_client, email="nodelete@test.com")
    sid = s["id"]
    r = await async_client.request("DELETE", f"/students/{sid}")
    assert r.status_code in (404, 405)


# get with filters test
# Patch test
# Delete test


# OPTIONAL (enable later): if you add GET /students/{id}, verify it resolves
# r2 = await async_client.get(location)
# assert r2.status_code == 200
# data = r2.json()
# assert str(data["id"]) == student_id
