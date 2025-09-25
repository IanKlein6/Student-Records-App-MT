# app/services/students.py
from app.models.student import Student, ArchiveLog, ArchiveAction

# Hard delete wrapper
async def hard_delete_student_service(student: Student, reason: str | None = None) -> None:
    # Log first so the entry survives even if FK on ArchiveLog is SET_NULL
    await ArchiveLog.create(student=student, action=ArchiveAction.HARD_DELETE, reason=reason)
    await student.delete()
