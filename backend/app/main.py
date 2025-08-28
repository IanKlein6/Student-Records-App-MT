
# app/main.py

import logging, os
from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, Response, Body
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError

from app.models.student import Student, StudentStatus
from app.schemas.student import (StudentCreate, StudentPatch, StudentRead, StudentList, ArchiveRequest, RestoreRequest)
from app.services.students import hard_delete_student


#Testing potentially remove for production
TESTING = os.getenv("TESTING") == "1" 

logging.basicConfig(
    level=logging.INFO, # change to DEBUG for debugging 
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Student Records API")

## Basic API health test (uvicorn app.main:app --reload) (DELETE WHEN IT WORKS)
@app.get("/")
async def health():
    return {"message": "OK"}


##Create students 
@app.post("/student", response_model=StudentRead, status_code=201)
async def create_student(payload: StudentCreate, response: Response):     
    """Create a student. Returns 201 with the created resource.""" #OpenAPI/Swagger docs
    try:    
        student = await Student.create(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email = payload.email
        )

    except IntegrityError:
        # Unique email collision
        raise HTTPException(status_code=409, detail="Email already exists")

    response.headers["Location"] = f"/student/{student.id}"

    logger.info(
        "student.create",
        extra={
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "student_id": student.id,
        },
    )

    return StudentRead.model_validate(student, from_attributes=True)


##GET student by ID
@app.get("/student/{student_id}", response_model=StudentRead)
async def get_student_by_id(student_id: int = Path(..., ge=1)):
    student = await Student.get_or_none(id=student_id)
    if not student:
        logger.warning("student.get_by_id.not_found id=%s", student_id)
        raise HTTPException(status_code=404, detail="Student not found")
    
    logger.info("student.get_by_id.ok id=%s email=%s", student_id, student.email)
    return StudentRead.model_validate(student, from_attributes=True)

##Get student with List/Filters
@app.get("/student", response_model=List[StudentList])
async def list_student(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200), #CHANGE LIMIT IF NEEDED LATER    
    offset: int = Query(0, ge=0),
): 
    #queryset build
    qs = Student.all()

    logger.debug(
        "student.list request filters: first_name=%s last_name=%s email=%s limit=%s offset=%s", 
        first_name, last_name, email, limit, offset
    )

    if first_name:
        qs = qs.filter(first_name__icontains=first_name)
    if last_name:
        qs = qs.filter(last_name__icontains=last_name)
    if email: 
        qs = qs.filter(email__icontains=email)
    
    rows = await qs.limit(limit).offset(offset)

    logger.info("student.list returned %d students", len(rows))

    return [StudentList.model_validate(r, from_attributes=True) for r in rows]
    

## Patch student
@app.patch("/student/{student_id}", response_model=StudentRead)
async def patch_student(student_id: int, payload: StudentPatch = Body(...)):
    logger.debug(
            "student.patch start id=%s payload=%s",
            student_id, payload.model_dump(exclude_none=True)
        )
    student = await Student.get_or_none(id=student_id)
    if not student:
        logger.warning("student.patch not_found id=%s", student_id)
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Reject empty body
    if not payload.model_dump(exclude_none=True):
        raise HTTPException(status_code=400, detail="No fields provided")

    #if changing email, enforce uniqueness. Email uniqueness
    if payload.email and payload.email != student.email:
        exists = await Student.filter(email=payload.email).exclude(id=student_id).exists()
        if exists:
            logger.info("student.patch email_conflict id=%s email=%s", student_id, payload.email)
            raise HTTPException(status_code=409, detail="Email already exists")

    # apply fields
    if payload.first_name is not None:
        student.first_name = payload.first_name
    if payload.last_name is not None:
        student.last_name = payload.last_name
    if payload.email is not None:
        student.email = payload.email 
    if payload.notes is not None:
        student.notes = payload.notes
    if payload.group_id is not None:
        student.group_id = payload.group_id
    if payload.semester_id is not None:
        student.semester_id = payload.semester_id
    if payload.work_student_potential is not None:
        student.work_student_potential = payload.work_student_potential
    
    # Handle status transitions that affect archive state
    if payload.status is not None:
        if payload.status == StudentStatus.ARCHIVED:
            await student.archive("PATCH: status=archived")
            student = await Student.get(id=student_id)
        else:
            # If currently archived and caller sets a non-ARCHIVED status restore first. 
            if student.is_archived:
                await student.restore("PATCH: status!=archived")
                student = await Student.get(id=student_id)
            student.status = payload.status

    # save if not archived transition already saved
    try: 
        await student.save()
    except IntegrityError:
        logger.info("student.patch integrity_conflict id=%s email=%s", student_id, payload)
        raise HTTPException(status_code=409, detail="Email already exists")
    
    logger.info("student.patch ok id=%s", student_id)
    return StudentRead.model_validate(student, from_attributes=True)


## Archive/ Restore endpoints
@app.post("student/{student_id}/archive", status_code=204)
async def archive_student(student_id: int, body: ArchiveRequest = Body(default=ArchiveRequest())):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.archive(body.reason)
    return Response(status_code=204)

@app.post ("/student/{student_id}/restore", status_code=204)
async def restore_student(student_id: int, body: RestoreRequest = Body(default=RestoreRequest())):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.restore(body.reason)
    return Response(status_code=204)



##Delete students function 
@app.delete("/student/{student_id}", status_code=204)
async def delete_student_by_id(student_id: int = Path(..., ge=1)):
    # Delete a student by primary key. Returns 204 on success, 404 if the student does not exist.
    try: 
        deleted = await Student.filter(id=student_id).delete()
    except Exception as exc:
        logger.error("student.delete unexpected_error id=%s error=%r", student_id, exc)
        raise
    if deleted == 0:
        logger.warning("student.delete not_found id=%s", student_id)
        raise HTTPException(status_code=404, detail="Student not found")
    # 204 = no body
    logger.info("student.delete success id=%s", student_id)
    return Response(status_code=204)


## Connection from Tortoise to FastAPI 
if not TESTING:
    register_tortoise( 
        app, #app instance being connected. Core Object 
        db_url="postgres://postgres:postgres@localhost:5432/student_records",
        modules={"models": [
            "app.models.student",
            "app.models.group",
            "app.models.semester"
            ]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
