
# app/main.py
from typing import Optional, List
import logging
import os

from fastapi import FastAPI, Path, Query, HTTPException, Response, APIRouter 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q # allows for logic Querying

from app.models.student import Student
from app.schemas.student import StudentIn, StudentOut
from app.utils.logger import create_logger, query_logger, delete_logger, error_logger


#Testing potentially remove for production
TESTING = os.getenv("TESTING") == "1" 

logging.basicConfig(
    level=logging.INFO, # change to DEBUG for debugging 
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Student Records API")


# Pydantic schemas
StudentOut = pydantic_model_creator(Student, name="StudentOut")
StudentIn = pydantic_model_creator(
    Student, 
    name="StudentIn",
    exclude_readonly=True, #id/created_at/updated_at excluded
)


## Basic API health test (uvicorn app.main:app --reload) (DELETE WHEN IT WORKS)
@app.get("/")
async def health():
    return {"message": "OK"}



##Create students 
@app.post("/student/", response_model=StudentOut, status_code=201)
async def create_student(payload: StudentIn, response: Response):     
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



##GET student by ID
@app.get("/student/{student_id}", response_model=StudentOut)
async def get_student_by_id(student_id: int = Path(..., ge=1)):
    student = await Student.get_or_none(id=student_id)
    if not student:
        query_logger.warning("student.get_by_id.not_found id=%s", student_id)
        raise HTTPException(status_code=404, detail="Student not found")
    
    query_logger.info("student.get_by_id.ok id=%s email=%s", student_id, student.email)
    return await StudentOut.from_tortoise_orm(student)


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
if not TESTING:
    register_tortoise( 
        app, #app instance being connected. Core Object 
        db_url="postgres://postgres:postgres@localhost:5432/student_records",
        modules={"models": ["app.models.student"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
