from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.models.student import Student
from typing import Optional 
from tortoise.expressions import Q #allows for logic Querying 
from fastapi import HTTPException

app = FastAPI()

##Create students 
@app.post("/student/")
async def create_student(name: str, email: str):
    student = await Student.create(name=name, email=email)
    return student


##Retrieve students 
@app.get("/student/")
async def get_student(name: Optional[str] = None, email: Optional[str] = None):
    filters = Q() #empty filter to alow for building of multiple filters
    if name:
        filters &= Q(name=name)
    if email:
        filters &= Q(email=email)
    
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
