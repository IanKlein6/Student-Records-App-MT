# app/tests/test_students.py
import pytest

# 422: missing required fields
@pytest.mark.asyncio
async def test_create_student_422_missing(async_client):
    r = await async_client.post("/students", json={"first_name": "A"})
    assert r.status_code == 422

# 422: bad email
@pytest.mark.asyncio
async def test_create_student_422_bad_email(async_client):
    r = await async_client.post("/students", json={
        "first_name": "A", "last_name": "B", "email": "not-an-email"
    })
    assert r.status_code == 422

# 404: GET non-existent
@pytest.mark.asyncio
async def test_get_student_404(async_client):
    r = await async_client.get("/students/999999")
    assert r.status_code == 404 

# 404: PATCH non-existent
@pytest.mark.asyncio
async def test_patch_student_404(async_client):
    r = await async_client.patch("/students/999999", json={"first_name": "New"})
    assert r.status_code == 404 

# 404 DELETE non-existent
@pytest.mark.asyncio
async def test_delete_student_404(async_client):
    r = await async_client.delete("/students/999999")
    assert r.status_code == 404 

# CREATE student
@pytest.mark.asyncio
async def test_create_student(async_client):
    payload = {
        "first_name": " Alex ",
        "last_name": " Heartt ",
        "email": " ALEXHEARTT@TEST1.com"
    }

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
    payload = {
        "first_name": "Grace",
        "last_name": "Hopper",
        "email": "dup@example.com"
    }
    r1 = await async_client.post("/students", json=payload)
    assert r1.status_code == 201

    r2 = await async_client.post("/students", json=payload)
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
    
    r = await async_client.post("/students", json=payload)
    assert r.status_code == 201

    # Header exists and points to the new resource
    assert "Location" in r.headers
    location = r.headers["Location"]
    assert location.startswith("/students/")

    # Extract id and check its's an int-like string
    student_id = location.rsplit("/", 1)[-1]
    assert student_id.isdigit()


# Create student in memory for testing below 
async def _create(async_client, first="Alex", last="Heartt", email="alex@test.com"):
    r = await async_client.post("/students", json={"first_name": first, "last_name": last, "email": email})
    assert r.status_code == 201, r.text
    return r.json()

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

    r2= await async_client.get(f"/students/{sid}")
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