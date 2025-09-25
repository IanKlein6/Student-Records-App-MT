# backend/app/routers/admin.py
import os
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Path
from app.models.student import Student
from app.services.students import hard_delete_student_service

async def require_admin(request: Request):
    # In tests, bypass auth with TESTING=1
    if os.getenv("TESTING") == "1":
        return
    token = request.headers.get("X-Admin-Token")
    if token != os.getenv("ADMIN_TOKEN", "dev-admin"):
        raise HTTPException(status_code=403, detail="Admin token required")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)

@router.delete("/students/{student_id}", status_code=204)
async def hard_delete_student(student_id: int = Path (..., ge=1)):
    student = await Student.get_or_none(id=student_id)
    if not student: 
        raise HTTPException(status_code=404, detail="Student not found")
    await hard_delete_student_service(student, reason="ADMIN hard delete")
    return Response(status_code=204)
