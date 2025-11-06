# app/schemas/student.py
from app.models.student import Student, StudentStatus, WorkPotential
from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Annotated, Optional
from app.schemas.types import Str50, Str255, NormalizedEmail

class StudentCreate(BaseModel):
    """Schema for creating a new Student.
    
    Creates a new Student.
       
        Attributes: 
            first_name (str): Student's first name (max 50 chars).
            last_name (str): Student's last name (max 50 chars).
            email (str): Student's email (Normalized using function NormalizedEmail in app.schema.types).
            semester_id (int): Optional ID of the semester to assign the student to. 
            group_id (int): Optional ID of the project group to assign the student to.

        Configuration: 
            model_config: extra="forbid", Rejects any fields not defined in this schema, helping catch typos and prevent malicious data injection. 
    """
    first_name: Str50 
    last_name: Str50
    email: NormalizedEmail
    semester_id: Optional[int] = None 
    group_id: Optional[int] = None 
    model_config = ConfigDict(extra="forbid")

class StudentPatch(BaseModel):
    """Schema for updates to student records.
    
    This schema supports PATCH operations where only specified fields are updated. All fields are optional - omitted fields remain unchanged in the database.
    
        Attributes: 
            first_name (str): Student's first name (max 50 chars).
            last_name (str): Students's last name (max 50 chars).
            email (str): Student's email (automatically normalized).
            status (charenum): Student's current course status (active, passed, failed, archived).
            notes (text): Instructor's notes about the Students progress (max 255 chars).
            # group (int):  ## Does this need to exist since we already have group_id ?? 
            group_id (int): ID of the project group the student is in.
            semester_id (int): ID of the semester the student is currently in.
            work_student_potential (charenum): Recruitment potential rating (low, medium, high).

        Configuration:
            All fields default to None. The API will only update fields that are explicitly provided in the request, leaving all others unchanged.
            model_config: extra="forbid", Rejects any fields not defined in this schema, helping catch typos and prevent malicious data injection. 
        """
    first_name: Optional[Str50] = None
    last_name: Optional[Str50] = None
    email: Optional[NormalizedEmail] = None
    status: Optional[StudentStatus] = None 
    notes: Optional[Str255] = None
    group: Optional[int] = None ## why do we need this? 
    group_id: Optional[int] = None
    semester_id: Optional[int] = None
    work_student_potential: Optional[WorkPotential] = None

    model_config = ConfigDict(extra="forbid")
 
 

# Add classes for different use cases in the future. e.i. if the front end only needs a list of names then create a schema where only names get pushed. also for security dont push things that dont need to be. 
class StudentRead(BaseModel):
    """Schema that allows the retreaval of student data from the data base.
    
    Attributes:
        id: 
        first_name: 
        last_name:
        email: 
        semester_id: 
        status: 
        notes: 
        work_student_potential:
        group_id: 
        attempt_num: 
        created_at: 
        updated_at:
        model_config
    """
    id: int
    first_name: Str50
    last_name: Str50
    email: NormalizedEmail
    semester_id: Optional[int]
    status: StudentStatus
    notes: Optional[str] = None 
    work_student_potential: Optional[WorkPotential]
    group_id: Optional[int] = None
    attempt_num: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StudentList(BaseModel):
    """Schema for frontend listing of students.
    
    Attributes:
        id: 
        first_name: 
        last_name: 
        email: 
    """
    id: int
    first_name: Str50
    last_name: Str50
    email: NormalizedEmail

    model_config = ConfigDict(from_attributes=True)

# Archive and Restore endpoint bodies
class ArchiveRequest(BaseModel):
    """Endpoint for archiving a student with optional reason body."""
    reason: Optional[str] = None

class RestoreRequest(BaseModel):
    """Endpoint for restoring student from archive with optional reason body."""
    reason: Optional[str] = None

