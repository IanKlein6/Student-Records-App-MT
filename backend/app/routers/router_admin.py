# backend/app/routers/router_admin.py

"""Admin API router.

Handles administrative operations requiring elevated permissions. 
All routes require valid admin token authentication via X-Admin-Token header. 

Authentication
    Admin token validation is applied to all routes cia router-level dependency. 
    Token can be bypassed in test environment (TESTING=1).

Routers
    DELETE /admin/students/{student_id}: Permanently delete a student record.

Data pipeline
    Frontend <--JSON--> FastApi Router <--Pydantic Schema (data validation)--> Service Layer <--Tortoise ORM models--> Database. 
 """

import os
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Path
from pydantic import BaseModel
from backend.app.models.model_student import Student
from backend.app.services.service_student import hard_delete_student_service

async def require_admin(request: Request):
    """Validate admin authentication token. 
    
    Checks for X-Admin-Token header and validates against ADMIN_TOKEN environment variable. 
    Bypassed automatically in test environments. 

    #### Args
        request: 403 if token is missing or invalid. 

    #### Raises
        HTTPException: 403 if token is missing or invalid.

    #### Environment Variables
        TESTING: Set to "1" to bypass authentication (test mode only).
        ADMIN_TOKEN: Expected admin token value (defaults to "dev-admin").
    """
    # Bypass authentication in test environment
    if os.getenv("TESTING") == "1":
        return
    
    token = request.headers.get("X-Admin-Token")
    expected_token = os.getenv("ADMIN_TOKEN", "dev-admin")

    if token != expected_token:
        raise HTTPException(status_code=403, detail="Admin token required")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)

# Class used by hard_delete_student
class DeleteRequest(BaseModel):
    reason: str = "Admin hard delete"

@router.delete("/students/{student_id}", status_code=204)
async def hard_delete_student(
    student_id: int = Path (..., ge=1),
    delete_data: DeleteRequest = DeleteRequest()) -> Response:
    
    """Permanently delete a student record.

    Performs a hard delete operation that removes the student from the database entirely. 
    An audit log entry is created before detection with reason tag. 
    
    **Warning**: This operation is irreversible. Use archive for all cases except when absolutely necessary.
    
    #### Args
        student_id: Unique student identifier.
    
    #### Raises
        404: Student with given ID does not exist.
        403: if admin token is invalid.
    
    #### Return 
        204: success status code. 
    """
    
    student = await Student.get_or_none(id=student_id)

    if not student: 
        raise HTTPException(status_code=404, detail="Student not found")
    
    await hard_delete_student_service(student, reason="ADMIN hard delete")

    return Response(status_code=204)
