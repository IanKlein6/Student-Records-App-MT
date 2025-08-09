## test database endpoints

import pytest

@pytest.mark.asyncio  #marker to run in async 
async def test_create_student(async_client):    # test function definition async_client comes from conftest.py
    payload = { #payload dictionary of the input being set to the api
        "name": "Test Student",
        "email": "test@student.com"
    }
    response = await async_client.post("/student/", params=payload) #sending payload to the student endpoint
    assert response.status_code == 200 #checks returning api code, 200 being okay. otherwise fail
    assert response.json() ["name"] == "Test Student" #parse the response body checking if the expected things came back\


@pytest.mark.asyncio
async def test_get_student(async_client):
    response = await async_client.get("/student/", params ={"name": "Test"})
    assert response.status_code == 200 #checks for error code
    data = response.json() #parses data
    assert "students" in data 
    assert any("Test Student" in s["name"] for s in data["students"])


@pytest.mark.asyncio
async def test_delete_student(async_client):

    #create student
    create_payload = {"name": "Delete Me", "email": "deleteme@example.com"}
    create_response = await async_client.post("/student/", params=create_payload)
    assert create_response.status_code == 200

    #delete student 
    delete_response = await async_client.delete("/student/", params={"name": "Delete Me"})
    assert delete_response.status_code == 200
    assert "Deleted 1 student" in delete_response.json()["message"]

    #test retrieve deleted student (should 404)
    get_response = await async_client.get("/student/", params ={"name": "Delete Me"})
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_student_by_name_and_email(async_client):
    #create two students = same name / different emails
    await async_client.post("/student/", params={"name": "Alex", "email": "alex1@example.com"})
    await async_client.post("/student/", params={"name": "Alex", "email": "alex2@example.com"})

    #delete only the one with a specific email
    delete_response = await async_client.delete("/student/", params={"name": "Alex", "email": "alex1@example.com"})
    assert delete_response.status_code == 200
    assert "Deleted 1 student" in delete_response.json()["message"]

    #check that the other student still exists
    get_response = await async_client.get("/student/", params={"name": "Alex"})
    assert get_response.status_code == 200
    students = get_response.json()["students"]
    assert any(s["email"] == "alex2@example.com" for s in students)
    assert all(s["email"] != "alex1@example.com" for s in students)

@pytest.mark.asyncio
async def test_delete_nonexistent_student(async_client):
    response = await async_client.delete("/student/", params={"name": "Ghost", "email": "ghost@example.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
