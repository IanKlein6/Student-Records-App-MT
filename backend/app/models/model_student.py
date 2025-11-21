# app/models/model_student.py

"""Student Tortoise model.

Tortoise model for defining students information in the database.

Classes
    StudentStatus: Abstraction classes for status options.
    WorkPotential: Abstraction classes for student potential rating.
    Student(Model): Model for all of a students information.

Info data pipeline
    Frontend <--JSON--> FastApi Router <--Pydantic Schema (data validation)--> Service Layer <--Tortoise ORM models--> Database. 
"""

from enum import Enum
from datetime import datetime, timezone
from tortoise import fields
from tortoise.models import Model
from app.models.archive_log import ArchiveAction, ArchiveLog


class StudentStatus(str, Enum):
    """Student course status option."""
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    ARCHIVED = "archived"

class WorkPotential(str, Enum):
    """Working student potential rating for recruitment purposes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Student(Model):
    """Student profile model + archive/restore functionality.
        
    This model represents a student in the system with support for archiving and restoration, including audit logging of these actions.

    #### Attributes
        id (int): Assigned Student ID.
        first_name (charfield): First name.
        last_name (charfield): Last name.
        email (charfield): Unique email.
        notes (text): Instructors notes about the student.
        semester (foreignkey): Current semester, inherited from models.Semester.
        group (foreignkey): Assigned project group, inherited from models.Group.
        status (char enum): Students course status, defined in StudentStatus.
        attempt_num (int): Number of oral exam attempts.
        word_student_potential (char enum): Working student scouting potential. 
        archived_at (date/time): When student was archived.
        created_at (date/time): When student was create.
        update_at (date/time): When student data has been last updated.

    #### Functions
        is_archived(self): check if archived. 
        __str__(self): Returns student name body.
        archive(self, reason): Archiving logic. 
        restore(self, reason): Restoring logic.

    #### Meta
        Adds indexes on (last_name, first_name) and on status.
    """
    id = fields.IntField(primary_key=True) ## change variables to id_student etc to be more descriptive 
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)
    notes = fields.TextField(null=True)

    semester = fields.ForeignKeyField("models.Semester", related_name="students", null=True, on_delete=fields.SET_NULL)
    group = fields.ForeignKeyField("models.Group", related_name="students", null=True, on_delete=fields.SET_NULL)

    status = fields.CharEnumField(StudentStatus, default=StudentStatus.ACTIVE)
    attempt_num = fields.IntField(default=0)

    work_student_potential = fields.CharEnumField(WorkPotential, null=True)
    
    archived_at = fields.DatetimeField(null=True, db_index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    ## add restore date/time?

    @property # allows access like student.is_archived
    def is_archived(self) -> bool: ## Is this redundant?? or error checking. can check student archived_at field to check??
        """Checks if student is archived, returns is not None."""
        return self.archived_at is not None # = True if archived_at has a value
    
    def __str__(self):
        """Returns request body, first and last name."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """Indexes by name and status."""
        indexes = [("last_name", "first_name"), ("status",),]

    async def archive(self, reason: str | None = None) -> None:
        """Archive student and record action.

        This method marks the student as archived and logs the action.
        It is idempotent—calling it multiple times will not create duplicate logs and it will exit early

        Process: 
            - check if student is already archived; If True, exits early.
            - Set 'archived_at' to current datetime.
            - Update 'status' to 'ARCHIVED'.
            - Save the updated student record.
            - Create an ArchiveLog entry.

        Notes:
            Async = call with await student.archive(...).
            Reason = optional explanation for students archiving.
        """
        if self.archived_at:
            return
        self.archived_at = datetime.now(timezone.utc)
        self.status = StudentStatus.ARCHIVED
        await self.save()
        await ArchiveLog.create(student=self, action=ArchiveAction.ARCHIVE, reason=reason)

    async def restore(self, reason: str | None = None) -> None:
        """Restore the student from Archived and record action
        
        Reverts an archived student back and writes a corresponding ArchiveLog. 
        It is idempotent, it will exit early if the student is not archived. 

        #### Process 
            - Check if student is not archived, if True exit. 
            - Set status to 'ACTIVE'.
            - Clear 'archived_at'.
            - Saves updated record.
            - Create ArchiveLog entry with 'RESTORE' as the action
                    
        #### Notes
            This is an async method and must be awaited. Call with await student.restore(...).
        """
        if not self.archived_at:
            return
        self.status = StudentStatus.ACTIVE
        self.archived_at = None 
        await self.save()
        await ArchiveLog.create(student=self, action=ArchiveAction.RESTORE, reason=reason)
