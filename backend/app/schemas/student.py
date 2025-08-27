# app/schemas/student.py
from app.models.student import Student, StudentStatus, WorkPotential
from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
from datetime import datetime
from typing import Annotated, Optional

class StudentCreate(BaseModel):
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr
    semester_id: int

class StudentPatch(BaseModel):
    first_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]] = None
    last_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]] = None
    email: Optional[EmailStr] = None
    status: Optional[StudentStatus] = None 
    notes: Optional[Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]] = None
    group: Optional[int] = None
    work_student_potential: Optional[WorkPotential] = None

    #email normalizer 
    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: Optional[str]) -> Optional[str]:
        return v.strip().lower() if v else v


# Add classes for different use cases in the future. e.i. if the front end only needs a list of names then create a schema where only names get pushed. also for security dont push things that dont need to be. 
class StudentRead(BaseModel):
    id: int
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr
    semester_id: Optional[int]
    status: StudentStatus
    notes: Optional[str] = None 
    work_student_potential: Optional[WorkPotential]
    group_id: Optional[int] = None
    attempt_num: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StudentList(BaseModel):
    id: int
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr

# Archive and Restore endpoint bodies
class ArchiveRequest(BaseModel):
    reason: Optional[str] = None

class RestoreRequest(BaseModel):
    reason: Optional[str] = None