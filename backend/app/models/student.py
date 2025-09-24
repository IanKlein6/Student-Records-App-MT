# app/models/student.py

from enum import Enum
from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from app.models.student import ArchiveLog, ArchiveAction, StudentStatus

# Options for student active status
class StudentStatus(str, Enum):
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    ARCHIVED = "archived"

# rating for student potential for workstudent
class WorkPotential(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Student(Model):
    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)
    notes = fields.TextField(null=True)

    semester = fields.ForeignKeyField("models.Semester", related_name="students", null=True, on_delete=fields.SET_NULL)
    group = fields.ForeignKeyField("models.Group", related_name="students", null=True, on_delete=fields.SET_NULL)

    status = fields.CharEnumField(StudentStatus, default=StudentStatus.ACTIVE)
    attempt_num = fields.IntField(default=0)

    work_student_potential = fields.CharEnumField(WorkPotential, null=True)
    
    archived_at = fields.DatetimeField(null=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Checks if student is archived or not
    @property # allows access like student.is_archived
    def is_archived(self) -> bool:
        return self.archived_at is not None # = True if archived_at has a value
    
    # Return request
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        indexes = [("last_name", "first_name"), ("status",),]

    # Invariant enforcing helpers for logging the archiving/restoring of students. centralized 
    async def archive(self, reason: str | None = None) -> None:
        if not self.archived_at:
            await ArchiveLog.create(student=self, action=ArchiveAction.ARCHIVE, reason=reason)
            return
        self.archived_at = datetime.utcnow()
        self.status = StudentStatus.ACTIVE
        await self.save()
        await ArchiveLog.create(student=self, action=ArchiveAction.ARCHIVE, reason=reason)

    async def restore(self, reason: str | None = None) -> None:
        if not self.archive_at:
            await ArchiveLog.create(student=self, action=ArchiveAction.RESTORE, reason=reason)
            return
        self.archived_at = None
        self.status = StudentStatus.ACTIVE
        await self.save()
        await ArchiveLog.create(student=self, action=ArchiveAction.RESTORE, reason=reason)

class ArchiveAction(str, Enum):
    ARCHIVE = "archive"
    RESTORE= "restore"
    HARD_DELETE = "hard_delete"

class ArchiveLog(Model):
    id = fields.IntField(primary_key=True)
    student = fields.ForeignKeyField("models.Student", related_name="archive_logs", null=True, on_delete=fields.SET_NULL)
    action = fields.CharEnumField(ArchiveAction)
    timestamp = fields.DatetimeField(auto_now_add=True)
    reason = fields.TextField(null=True)
