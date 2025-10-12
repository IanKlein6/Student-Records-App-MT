# app/schemas/student.py
from app.models.student import Student, StudentStatus, WorkPotential
from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Annotated, Optional
from app.schemas.types import Str50, Str255, NormalizedEmail

class StudentCreate(BaseModel):
    first_name: Str50 
    last_name: Str50
    email: NormalizedEmail
    semester_id: Optional[int] = None 
    group_id: Optional[int] = None 
    model_config = ConfigDict(extra="forbid")

class StudentPatch(BaseModel):
    first_name: Optional[Str50] = None
    last_name: Optional[Str50] = None
    email: Optional[NormalizedEmail] = None
    status: Optional[StudentStatus] = None 
    notes: Optional[Str255] = None
    group: Optional[int] = None
    group_id: Optional[int] = None
    semester_id: Optional[int] = None
    work_student_potential: Optional[WorkPotential] = None


# Add classes for different use cases in the future. e.i. if the front end only needs a list of names then create a schema where only names get pushed. also for security dont push things that dont need to be. 
class StudentRead(BaseModel):
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
    id: int
    first_name: Str50
    last_name: Str50
    email: NormalizedEmail

# Archive and Restore endpoint bodies
class ArchiveRequest(BaseModel):
    reason: Optional[str] = None

class RestoreRequest(BaseModel):
    reason: Optional[str] = None

