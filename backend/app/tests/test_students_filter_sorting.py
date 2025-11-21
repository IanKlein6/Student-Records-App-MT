# app/tests/test_students_filters_sort.py

"""Student Filtering system unit tests.

    Test Setup: 
        _create: creates model for student creation in test DB

    Tests:
        test_filters_can_be_combined: Checks if various filters can be combined when retrieving students @ /students (e.i status, semester_id)
        test_sort_by_name_and_email: Checks if students can be sorted by name and email in ascending/descending order. 
        test_default_sort_is_newest_first: Check if default sort setting returns newest added student first. 
"""

import pytest
import uuid
from app.models.semester import Semester

async def _create(async_client, **overrides):
    """Create a student profile in the test database.

    Test helper function that generates and posts student data with sensible defaults. 
    Allows selective override of any field via kwargs for flexible test scenarios. 

    Args 
        async_client: Configured httpx AsyncClient fixture for API requests
        **overrides: Optional field overrides. Supported keys:
            - i (int): Index for generating unique default names (default: 0)
            - first_name (str): Student's first name (default: "First{i}")
            - last_name (str): Student's last name (default: "Last{i}")
            - email (str): Student's email (default: auto-generated unique email)
            - semester_id (int | None): Foreign key to semester
            - group_id (int | None): Foreign key to group

    Returns
        dict: JSON response containing created student data with assigned ID
    
    Raises: 
        AssertionError: If API returns non-301 status code
    """
    i = overrides.get("i", 0)
    email = overrides.get("email") or f"user{i}-{uuid.uuid4().hex[:8]}@test.com"
    payload = {
        "first_name": overrides.get("first_name", f"First{i}"),
        "last_name": overrides.get("last_name", f"Last{i}"),
        "email": email,
        "semester_id": overrides.get("semester_id"),
        "group_id": overrides.get("group_id"),
    }
    r = await async_client.post("/students", json=payload)
    assert r.status_code == 201, f"Expected 201, got {r.status_code}. Body: {r.text}"
    return r.json()

@pytest.mark.asyncio
async def test_filters_can_be_combined(async_client):
    """Test that multiple query filters work simultaneously. 

    Verifies the /students endpoint correctly combines semester_id, status, and text search (q) filters to return only matching records.

    Test Setup
        Creates 2 semesters (S1, S2)
        Student 1: Active in S1, name "Anna Zeus"
        Student 2: Failed in S1, name "Anne Zed"
        Student 3: Archived in S2, name "Bob Yellow"

    Test Case
        Query with semester_id=S1 + status=active + q="ann"
        Expected: Only Student 1 (Anna) should match all criteria
    
    Args
        async_client: Configured httpx AsyncClient fixture for API requests

    Asserts
        Patch request returns 200 (status update successful)
        Archive request returns 204 (archive successful)
        Combine filter query returns 200 with only Student 1
    """
   # Semester creation
    sem1 = await Semester.create(name="S1")
    sem2 = await Semester.create(name="S2")

    # S1 active, semester 1
    s1 = await _create(async_client, i=1, first_name="Anna", last_name="Zeus", semester_id=sem1.id)
    # S2 failed, semester 1
    s2 = await _create(async_client, i=2, first_name="Anne", last_name="Zed", semester_id=sem1.id)
    # Mark failed (failout)
    r = await async_client.patch(f"/students/{s2['id']}", json={"status": "failed"})
    assert r.status_code == 200

    # S3 archived, semester 2
    s3 = await _create(async_client, i=3, first_name="Bob", last_name="Yellow", semester_id=sem2.id)
    r = await async_client.post(f"/students/{s3['id']}/archive", json={})
    assert r.status_code == 204

    # Combine: semester_id=1 + status=active + q='ann' (ILIKE first/last)
    r = await async_client.get("/students", params={"semester_id": sem1.id, "status": "active", "q": "ann"})
    assert r.status_code == 200
    data = r.json()
    # Should only return s1 (Anna Zeus)
    ids = [row["id"] for row in data]
    assert ids == [s1["id"]]

@pytest.mark.asyncio
async def test_sort_by_name_and_email(async_client):
    """Test Students can be sorted by name and by email.
    
    Verifies that /students endpoint correctly sorts results alphabetically by last name + first name (ascending) and by email (descending).
    
    Test Setup
        - Alex Miller (b@example.com)
        - Bea Anders (c@example.com)
        - Carl Anders (a@example.com)

    Test Case
        - sort=name:asc - Anders (Bea), Anders (Carl), Miller (Alex)
        - Combined with  q filter - Anders students maintain sort order.
        - sort=email:decs - c@, b@, a@ (descending) 

    Args
        async_client: Configured httpx AsyncClient fixture for API requests.

    Asserts
        All sort requests return 200 status
        Name sort requests return 200 status
        Email sorting orders by email descending
"""
    a = await _create(async_client, i=10, first_name="Alex", last_name="Miller", email="b@example.com")
    b = await _create(async_client, i=11, first_name="Bea", last_name="Anders", email="c@example.com")
    c = await _create(async_client, i=12, first_name="Carl", last_name="Anders", email="a@example.com")

    # name:asc → last_name, first_name ascending → Anders (Bea), Anders (Carl), Miller (Alex)
    r = await async_client.get("/students", params={"sort": "name:asc", "limit": 3, "offset": 0})
    assert r.status_code == 200
    names = [(s["last_name"], s["first_name"]) for s in r.json() if s["id"] in {a["id"], b["id"], c["id"]}]
    # Filter to these three only and compare order
    # Full list may include others created by other tests; we sort our subset for expected order
    expected = [("Anders", "Bea"), ("Anders", "Carl"), ("Miller", "Alex")]
    assert sorted(names) == expected  # ensure content
    # Also check relative order by querying with q filter to limit set
    r = await async_client.get("/students", params={"q": "Anders", "sort": "name:asc"})
    assert [(s["last_name"], s["first_name"]) for s in r.json()] == [("Anders", "Bea"), ("Anders", "Carl")]

    # email:descending order among the three → c@, b@, a@
    r = await async_client.get("/students", params={"sort": "email:desc"})
    assert r.status_code == 200
    got = [s for s in r.json() if s["id"] in {a["id"], b["id"], c["id"]}]
    emails = [s["email"] for s in got]
    assert sorted(emails, reverse=True) == emails  # desc order

@pytest.mark.asyncio
async def test_default_sort_is_newest_first(async_client):
    """Test default sort order returns newest students first.
    
    Verifies that without explicit sort parameter, the /students endpoint returns records in descending creation order (newest first).
    
    Test Setup
        Student 1 created first (i-21)
        Student 2 created second (i-22)

    Test Case
        Query without sort parameter.
        Expected: Student 2 appears before student 1 (newest first).

    Args
        async_client: Configured httpx AsyncClient fixture for API requests
    
    Asserts 
        Request returns 200 status.
        Most recently created student (s2) appears first in results.
"""
    s1 = await _create(async_client, i=21)
    s2 = await _create(async_client, i=22)
    r = await async_client.get("/students", params={"limit": 2})
    assert r.status_code == 200
    ids = [row["id"] for row in r.json()[:2]]
    # Default is created_at desc (or id desc fallback), so s2 should come before s1
    assert ids[0] == s2["id"]

