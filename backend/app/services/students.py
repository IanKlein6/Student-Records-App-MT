# app/services/students.py

from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from app.models.student import Student
from app.models.semester import Semester
from app.models.archive_log import ArchiveLog, ArchiveAction


# Hard delete wrapper
async def hard_delete_student_service(student_obj: Student, reason: str | None = None) -> None:
    # Log first so the entry survives even if FK on ArchiveLog is SET_NULL
    await ArchiveLog.create(student=student_obj, action=ArchiveAction.HARD_DELETE, reason=reason)
    await student_obj.delete()

# pre-validate foreign keys and map DB integrity errors (FK→422, unique→409) so clients get correct, semantic errors.
async def create_student_service(data) -> Student:
    # Pre-validate FK (domain rule)
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
        if sqlstate == "23505" or "unique" in (str(e) or "").lower():
            raise HTTPException(status_code=409, detail="Email already exists")
        if sqlstate == "23503":
            # Race-condition-safe fallback
            raise HTTPException(status_code=422, detail="Invalid foreign key")
        raise
