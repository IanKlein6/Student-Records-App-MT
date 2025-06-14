from fastapi import FastAPI, Query, HTTPException, APIRouter 
from tortoise.contrib.fastapi import register_tortoise
from app.models.student import Student
from typing import Optional, List 
from tortoise.expressions import Q #allows for logic Querying 



app = FastAPI()

##Create students 
@app.post("/student/")
async def create_student(name: str, email: str):
    student = await Student.create(name=name, email=email)
    return student


##Retrieve students 
@app.get("/student/")
async def get_student(
    name: Optional[list[str]] = Query(default=None), 
    email: Optional[list[str]] = Query(default=None)
):
    filters = Q() #empty filter to alow for building of multiple filters

    if name: #allows for multiple, varying types of queries to be searched in the same batch. 
        name_filter = Q(name__icontains=name[0]) #name__icontains == non-case sensitive 
        for n in name[1:]:
            name_filter |= Q(name__icontains=n)
        filters |= name_filter # |= is OR logic
    if email:
        email_filter = Q(email__icontains=email[0])
        for e in email[1:]:
            email_filter |= Q(email__icontains=e)
        filters |= email_filter 

    if name or email: #runs only if filter(s) were given 
        students = await Student.filter(filters).all()
        if not students:
            raise HTTPException(status_code=404, detail="No matching students found")
        return {"students": students} #returns specified student

    return {"All students": await Student.all()} #return all students
   


##Delete students function 
@app.delete("/student/") #Routing decorators. like urls.py in Django 
async def delete_student(name: str, email: Optional[str] = None): # end point definition, accepts name and optional email incase of doubled student names 
    filters = Q(name=name) #filters for matching name. Q==Query 
    if email: #and email if provided 
        filters &=Q(email=email)

    students_to_delete = await Student.filter(filters).all() #fetching records matching the filter extracting names for return message 

    if not students_to_delete: #error for if no students found
        raise HTTPException(status_code=404, detail="Student not found")
    
    deleted_names = [student.name for student in students_to_delete] #extract students names into list for return message

    await Student.filter(filters).delete() #delete function of students. Await allow python to pause while waiting for slow Queries

    return { #return num of students and corresponding names for safety 
        "message": f"Deleted {len(deleted_names)} student(s).",
        "students": deleted_names,
    }
    


##Connection from Tortoise to FastAPI 
register_tortoise( 
    app, #app instance being connected. Core Object 
    db_url="postgres://postgres:postgres@localhost:5432/student_records",
    modules={"models": ["app.models.student"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
