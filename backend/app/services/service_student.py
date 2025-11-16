# app/services/service_student.py

"""Student service layer.

Provides business logic and data access operations for student management. 
Handles validation, error mapping, audit logging, and database interactions.

Services
    - hard_delete_student_service: Deletes student with audit trail. 
    - create_student_service: Creates student with validation and duplicate detection.    


Info data pipeline
    Frontend <--JSON--> FastApi Router <--Pydantic Schema (data validation)--> Service Layer <--Tortoise ORM models--> Database.
"""

from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from backend.app.models.model_student import Student
from app.models.semester import Semester
from app.models.archive_log import ArchiveLog, ArchiveAction


async def hard_delete_student_service(student_obj: Student, reason: str | None = None) -> None:
    """Hard Delete wrapper for deleting a Student.
    
    Takes a Student object plus a reason and writes a ArchiveLog with a HARD_DELETE tag + reason. Then deletes the student from the database. 

    Info
        Log is created first so the entry survives even if FK on ArchiveLOG is SET_NULL
    """
    # Log first so the entry survives even if FK on ArchiveLog is SET_NULL
    await ArchiveLog.create(student=student_obj, action=ArchiveAction.HARD_DELETE, reason=reason)
    await student_obj.delete()


async def create_student_service(data) -> Student:
    """Creates a new student record.

    Validates foreign key references before creation and maps database integrity errors to appropriate HTTP exceptions for API clients. 
    
    Args:
        Data = Student creation data containing first_name, last_name, email, and optional semester_id. 
        
    Returns:
        The newly created Student instance. 

    Raises: 
        HTTPException: 422 if semester_id references a non-existent semester.
        HTTPException: 409 if email already exists.
        HTTPException: 422 if any other foreign key constraint is violated.

    Process:
        - Checks if semester_id is provided and validates it exists in database.
        - Creates new student record with stripped whitespace from names.
        - Catches IntegrityError for duplicate emails and invalid foreign keys.
        - Re-raises unknown integrity errors for debugging.

    Notes: 
        To prevent duplicate student, email is checked for unique in model.Student and if will then raise a 409 error 
    """
    if getattr(data, "semester_id", None) is not None:  
        if not await Semester.filter(id=data.semester_id).exists():
            raise HTTPException(status_code=422, detail="Invalid semester_id")

    try:
        student = await Student.create(
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            email=data.email,
            semester_id=data.semester_id,
        )
        return student
    except IntegrityError as e:
        cause = getattr(e, "__cause__", None)
        sqlstate = getattr(cause, "sqlstate", None)
        #PostgreSQL unique constraint violation
        if sqlstate == "23505" or "unique" in (str(e) or "").lower():
            raise HTTPException(status_code=409, detail="Email already exists")
        # PostgreSQL foreign key violation (race condition fallback)
        if sqlstate == "23503":
            raise HTTPException(status_code=422, detail="Invalid foreign key")
        # Unknown integrity error - re-raise for debugging
        raise 
