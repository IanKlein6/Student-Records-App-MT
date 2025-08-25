# app/schemas/student.py
from app.models.student import Student, StudentStatus, WorkPotential
from pydantic import BaseModel, EmailStr, Optional, StringConstraints
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


# Add classes for different usecases in the future. e.i. if the front end only needs a list of names then create a schema where only names get pushed. also for security dont push things that dont need to be. 
class StudentRead(BaseModel):
    id = int
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr
    semester_id: int
    status: StudentStatus
    
    notes: Optional[str] = None 
    work_student_potential: WorkPotential
    group_id: Optional[int] = None
    attempt_num: int
    
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class StudentList(BaseModel):
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr