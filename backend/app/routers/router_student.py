# backend/app/routers/router_student.py

"""FastAPI router for students.

Routers: 
    create_student (POST): 
    get_student_by_id (GET):
    list_students (GET):
    patch_student (PATCH):
    archive_student (POST):
    restore_student (POST):
    delete_student_public (api_route):

Notes: 

Info data pipeline:
    Frontend <--> FastApi router <--> Pydantic Schema. 
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Path, Query, HTTPException, Response, Body
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from app.models.student import Student, StudentStatus
from backend.app.schemas.schema_student import StudentCreate, StudentPatch, StudentRead, StudentList, ArchiveRequest, RestoreRequest
from app.services.students import create_student_service

logger = logging.getLogger(__name__)

# API router variable
router = APIRouter(prefix="/students", tags=["students"])

## add global error handlers at a later point in time when needed to keep routers thin and keep error handlers centralized. 
@router.post("", response_model=StudentRead, status_code=201)
async def create_student(payload: StudentCreate, response: Response):
    """Create a new student API.

    Handles POST requests from the frontend, validates the payload against the StudentCreate schema, and stores the new student in the database. Returns the created record serialized with the StudentRead schema.

    Args:
        payload: Validated student creation data.
        response: FastAPI response object for setting headers.
    
    Returns:
        The newly created student record.

    Raises: 
        HTTPException: 422 if semester_id is invalid.
        HTTPException: 409 if email already exists.

    Process: 
        - Accepts the validated request body (payload).
        - Pass the payload to the service layer (create_student_service) for creation.
        - Set a Location header pointing to the new resource (/students/{id}).
        - Return the created student serialized as StudentRead with status code 201.
    """
    student = await create_student_service(payload)        
    response.headers["Location"] = f"/students/{student.id}"
    return StudentRead.model_validate(student, from_attributes=True)

@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id(student_id: int = Path(..., ge=1)):
    """Retrieves student by ID API.
    
    Handles GET requests of students from the frontend. 
    
    Process:
        - Gets GET request with wanted student ID.
        - Awaits till student is found.
        - If not found raises 404 error.
        - If it does find the student it pass the payload student to the frontend. 
    """
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentRead.model_validate(student, from_attributes=True)

@router.get("", response_model=List[StudentList])
async def list_students(
    semester_id: Optional[int] = Query(None, ge=1),
    status: Optional[str] = Query(None, pattern="^(active|archived|failout)$"),
    q: Optional[str] = Query(None, min_length=1),  # ILIKE on first/last name
    sort: Optional[str] = Query(None, pattern="^(name|first_name|last_name|email|created_at):(asc|desc)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Retrieve a filtered and sorted list of students.

    Args: 
        semester_id: Filter by semester ID.
        status: Filter by status - 'active', 'archive', or 'failout'.
        q: Search term for first name, last name, or email (case-insensitive partial match).
        sort: Sort expression 'field:direction' (e.g., 'last_name:asc', 'created_at:desc').
        limit: Maximum number of results (1-200, default 50).
        offset: Number of results to skip (default 0).

    Returns: 
        List[StudentList]: Filtered and sorted list of student records.

    Raises:
        400: Unsupported sort Field

    Process:
        - Initialize query for all students. 
        - Apply semester filter if semester_id is provided.
        - Apply status filter if status if provided (map string to StudentStatus enum).
        - Apply search filter if a search query is provided (sorts across first_name, last_name, email).
        - Determine sort fields.
            - Use provided sort parameter, or default to created_at descending.
            - handle special case for 'name' sorting (sorts by last_name, then first_name).
            - fallback to id sorting if created_field doesn't exist.
        - Execute query with ordering, limit, and offset
        - Convert database records to StudentList response models

    Example:
        GET /students?semester_id=5&status=active&q=john&sort=last_name:asc&limit=25
        
    """
    qs = Student.all()
    # filters (combinable)
    if semester_id is not None:
        qs = qs.filter(semester_id=semester_id)

    if status:
        status_map = {
            "active": StudentStatus.ACTIVE,
            "archived": StudentStatus.ARCHIVED,
            "failout": StudentStatus.FAILED,  # alias
        }
        qs = qs.filter(status=status_map[status])

    if q:
        qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q))

    # sorting
    has_created = "created_at" in Student._meta.fields_map
    if not sort:
         ## Debate changing to alphabetical sorting of last name for default... 
        order_fields = ["-created_at"] if has_created else ["-id"]  # default 
    else:
        field, direction = sort.split(":")
        desc = direction == "desc"

        if field == "name":
            order_fields = (["-last_name", "-first_name"] if desc
                            else ["last_name", "first_name"])
        elif field in ("first_name", "last_name", "email"):
            order_fields = [f"-{field}" if desc else field]
        elif field == "created_at": 
            key = "created_at" if has_created else "id"
            order_fields = [f"-{key}" if desc else key]
        else:
            raise HTTPException(status_code=400, detail="Unsupported sort field")

    rows = await qs.order_by(*order_fields).limit(limit).offset(offset)
    return [StudentList.model_validate(r, from_attributes=True) for r in rows]


@router.patch("/{student_id}", response_model=StudentRead)
async def patch_student(student_id: int, payload: StudentPatch = Body(...)):
    """Update/Patch changes to a student's profile.

    Args: 
        student_id: Unique identifier for the student
        payload: StudentPatch object containing fields to update

    Returns: 
        StudentRead: The updated student record

    Raises: 
        404: Student not found
        400: No fields provided in payload
        409: Email already exists for another student

    Process:
        1. Retrieve student record by ID
        2. Raise 404 error if student doesn't exist
        3. Validate that at least one field is provided in payload
        4. Check if new email conflicts with existing student emails
        5. Update provided fields (first_name, last_name, email, notes, 
        group_id, semester_id, work_student_potential)
        6. Handle status changes:
            - Archive student if status set to ARCHIVED
            - Restore student if status changed from ARCHIVED to another status
            - Update status field
        7. Save changes to database
        8. Return updated student record

    Example:
        PATCH /students/123
        Body: {"first_name": "John", "email": "john@example.com"}
      """
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not payload.model_dump(exclude_none=True):
        raise HTTPException(status_code=400, detail="No fields provided")

    if payload.email and payload.email != student.email:
        exists = await Student.filter(email=payload.email).exclude(id=student_id).exists()
        if exists:
            raise HTTPException(status_code=409, detail="Email already exists")

    if payload.first_name is not None:
        student.first_name = payload.first_name
    if payload.last_name is not None:
        student.last_name = payload.last_name
    if payload.email is not None:
        student.email = payload.email
    if payload.notes is not None:
        student.notes = payload.notes
    if payload.group_id is not None:
        student.group_id = payload.group_id
    if payload.semester_id is not None:
        student.semester_id = payload.semester_id
    if payload.work_student_potential is not None:
        student.work_student_potential = payload.work_student_potential

    if payload.status is not None:
        if payload.status == StudentStatus.ARCHIVED:
            await student.archive("PATCH: status=archived")
            student = await Student.get(id=student_id)
        else:
            if student.is_archived:
                await student.restore("PATCH: status!=archived")
                student = await Student.get(id=student_id)
            student.status = payload.status

    try:
        await student.save()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists") ## Doubled up error code??? above is a 409 already inside the loop. 

    return StudentRead.model_validate(student, from_attributes=True)

@router.post("/{student_id}/archive", status_code=204)
async def archive_student(student_id: int, body: ArchiveRequest = Body(default=ArchiveRequest())):
    """Archive a Student.
    
    Archive a student there by removing them from the active list while preserving their data.

    Args: 
        student_id: Unique identifier for the student to restore.
        body: Archive request with optional reason body.
    
    Return:
        Success response. 
    
    Raises:
        404: Student not found.

    Process:
        1. Retrieve student record by ID.
        2. Raise 404 if student doesn't exist.
        3. Call archive method with provided reason.
        4. Return 204 No Content status confirming the move.

    Example: 
        POST /students/123/archive.
        Body: {"reason": "Passed"}.
    """
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.archive(body.reason)
    return Response(status_code=204)

@router.post("/{student_id}/restore", status_code=204)
async def restore_student(student_id: int, body: RestoreRequest = Body(default=RestoreRequest())):
    """Restore a student from Archive.
    
    Restore a student from being in the Archive making them visible in the active lists again. 

    Args: 
        student_id: Unique identifier for the student to restore.
        body: RestoreRequest containing optional reason for restoration.
    
    Returns:
        Success response.
    
    Raises:
        404: Student not found.

    Process:
        1. Retrieve student record by ID.
        2. Raise 404 if student doesn't exist.
        3. Call restore method with provided reason.
        4. Return 204 No Content status.
    
    Example:
        POST: /students/123/restore
        Body: {"reason": "Re-enrolled for new semester"}
    """
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.restore(body.reason)
    return Response(status_code=204)

@router.api_route("/{student_id}", methods=["DELETE"], include_in_schema=False)
async def delete_student_public(student_id: int = Path(..., ge=1)):
    """Permanent Deletion of a Student (disabled).
    
    This endpoint is intentionally disabled to prevent accidental permanent data loss. Use the archive endpoint instead to soft-delete students. Will be in-abled when safety precautions have been met. 
    
    Args: 
        student_id: Unique identifier for the student (not used).
    
    Return:
        Never returns successfully - always raises 404.
    
    Raises:
        404: Always raised - deletion is disabled for safety.
    
    Note:
        This endpoint is hidden from API documentation (include_in_schema=False).
        Permanent deletion should only be done through admin tools or database access.
    """
    raise HTTPException(status_code=404, detail="Student not found")
