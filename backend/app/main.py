
# app/main.py
from typing import Optional, List
import logging

from fastapi import FastAPI, Query, HTTPException, Response, APIRouter 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q # allows for logic Querying

from app.models.student import Student
from app.utils.logger import create_logger, query_logger, delete_logger, error_logger


logging.basicConfig(
    level=logging.INFO, # change to DEBUG for debugging 
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


# Pydantic schemas
StudentOut = pydantic_model_creator(Student, name="StudentOut")
StudentIn = pydantic_model_creator(
    Student, 
    name="StudentIn",
    exclude_readonly=True, #id/created_at/updated_at excluded
)


## Basic API test DELETE WHEN IT WORKS
@app.get("/")
async def read_root():
    return {"message": "Hello World"}



##Create students 
@app.post("/student/", response_model=StudentOut, status_code=201)
async def create_student(payload: StudentCreate, response: Response):     
    """Create a student. Returns 201 with the created resource.""" #OpenAPI/Swagger docs
    try:    
        student = await Student.create(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            email = payload.email.strip().lower(), #normalize email
        )

    except IntegrityError:
        # Unique email collision
        raise HTTPException(status_code=409, detail="Email already exists")

    response.headers["Location"] = f"/student/{student.id}"
    
    create_logger.info(
        "student.create",
        extra={
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "student_id": student.id,
        },
    )

    return await StudentOut.from_tortoise_orm(student)



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
        query_logger.debug(f"Applying name filter(s): {name}")

    if email:
        email_filter = Q(email__icontains=email[0])
        for e in email[1:]:
            email_filter |= Q(email__icontains=e)
        filters |= email_filter 
        query_logger.debug(f"Applying email filter(s): {email}")

    if name or email: #runs only if filter(s) were given 
        query_logger.debug(f"Executing student search with combined filters: {filters}")
        students = await Student.filter(filters).all()

        if not students:
            query_logger.info(f"No students found with filters: name={name}, email={email}")
            raise HTTPException(status_code=404, detail="No matching students found")
        
        query_logger.info(f"Found {len(students)} student(s) with filters: name={name}, email={email}")
        return {"students": students} #returns specified student
    
    # Fallback: no filters 
    all_students = await Student.all()
    query_logger.info(f"Retrieved all students: total {len(all_students)}")
    return {"All students": await Student.all()} #return all students
   


##Delete students function 
@app.delete("/student/") #Routing decorators. like urls.py in Django 
async def delete_student(name: str, email: Optional[str] = None): # end point definition, accepts name and optional email incase of doubled student names 
    filters = Q(name=name) #filters for matching name. Q==Query 
    if email: #and email if provided 
        filters &=Q(email=email)

    delete_logger.debug(f"Delete request filters: name={name}, email={email}")

    students_to_delete = await Student.filter(filters).all() #fetching records matching the filter extracting names for return message 

    if not students_to_delete: #error for if no students found
        error_logger.warning(f"Delete failed: no student found with name={name}, email={email}")
        raise HTTPException(status_code=404, detail="Student not found")
    
    deleted_names = [student.name for student in students_to_delete] #extract students names into list for return message
    await Student.filter(filters).delete() #delete function of students. Await allow python to pause while waiting for slow Queries
   
    delete_logger.info(f"Deleted {len(deleted_names)} student(s): {deleted_names}")

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
