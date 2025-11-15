# app/schemas/schema_student.py

"""Overview Doc: Pydantic Schema for Students 

Defines the way in which student related data is validated, serialized, and exchanged through the API. They form the boundary between the database models and external clients (frontend, 3rd party integrations, etc.

Classes: 
    StudentCreate: Basic schema for creating a new student (POST /students).
    StudentPatch: Schema for changing/updating students data (PATCH /students{id}).
    StudentRead: Schema for retrieving all data from a student (GET /students{id}).
    StudentList: Schema for retrieving only selected data (id, first and last name, email) from a student for the use case of listing students without needing all of their data. 

    ArchiveRequest: End point for archive a student.
    RestoreRequest: End point for restoring a student if they are archived.

Notes:
    - All create and patch schemas use extra="forbid" field for stricter validation.
    - Response schemas (Read/List) use from_attributes=True for ORM compatibility.
    - This file complements app/models/model_student.py, which defines the database layer.

Info Data Pipeline:
    FastAPI endpoint <--> Pydantic schema <--> Tortoise model.
"""

from app.models.student import Student, StudentStatus, WorkPotential
from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Annotated, Optional
from backend.app.utilities.utils import Str50, Str255, NormalizedEmail

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
    group: Optional[int] = None ## Do we need this considering we already have group_id? debate reasoning and check back into relationships 
    group_id: Optional[int] = None
    semester_id: Optional[int] = None
    work_student_potential: Optional[WorkPotential] = None

    model_config = ConfigDict(extra="forbid")

class StudentRead(BaseModel):
    """Schema for retrieving a students information.

    Used to retrieve all students information from the database. 
    
        Attributes:
            id (int): Students database id number. 
            first_name (str): Student's first name (max 50 chars).
            last_name (str): Students's last name (max 50 chars).
            email (str): Student's email (automatically normalized).
            status (charenum): Student's current course status (active, passed, failed, archived).
            notes (text): Instructor's notes about the Students progress (max 255 chars).
            group_id (int): ID of the project group the student is in.
            semester_id (int): ID of the semester the student is currently in.
            work_student_potential (charenum): Recruitment potential rating (low, medium, high).
            attempt_num (int): Students number of attempts for the exam (max of 3) ## check if 3 is correct!
            created_at (date/time): Exact time student profile was created.
            updated_at (date/time): Exact time student profile was last updated.
            
            Configuration:
                All fields default to None. The API will only update fields that are explicitly provided in the request, leaving all others unchanged.
                model_config: extra="forbid", Rejects any fields not defined in this schema, helping catch typos and prevent malicious data injection. 
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

class StudentList(BaseModel): ## This might be obsolete if its possible to use StudentRead and only retrieve a few specific parts without having to retrieve all the students data. 
    """Schema for retrieval of multiple students for a list.

    A Schema that defines the GET of student data from the data base for the purpose of displaying the students in a list. Is supposed to retrieve all students with only some of their most basic information to display in the frontend list which should then be able to sort the students by filters. Abstraction is the idea behind this.
    
    Reasoning: 
        - Retrieve all students at once in order to speed up filtering process since they would all be "pre-loaded" in the list and wouldn't have to be re-retrieved at the point of filtering.
        - This is intended to increase filtering speed and reduced student information to minium is intended to increase retrieval speed. 
        
    Attributes:
        id (int): Students database id number. 
        first_name (str): Student's first name (max 50 chars).
        last_name (str): Students's last name (max 50 chars).
        email (str): Student's email (automatically normalized).

    Configuration:
            model_config = ConfigDict(from_attributes=True), ensures clean ORM to JSON conversions so Tortoise models can be serialized safely. 
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

## Add classes for different use cases in the future. e.i. if the front end only needs a list of names then create a schema where only names get pushed. also for security dont push things that dont need to be. 