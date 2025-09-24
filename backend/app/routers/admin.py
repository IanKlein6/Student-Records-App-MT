# app/routers/admin.py
import os
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from app.models.student import Student

router = APIRouter(prefix="/admin", tags=["admin"])

async def require_admin(request: Request):
    # In tests, bypass auth with TESTING=1
    if os.getenv("TESTING") == "1":
        return
    token = request.headers.get("X-Admin-Token")
    if token != os.getenv("ADMIN_TOKEN", "dev-admin"):
        raise HTTPException(status_code=403, detail="Admin token required")

@router.delete("/students/{student_id}", status_code=204)
async def hard_delete_student(student_id: int, _=Depends(require_admin)):
    deleted = await Student.filter(id=student_id).delete()
    if deleted == 0:
        # Keep 404 for non-existent ID
        raise HTTPException(status_code=404, detail="Student not found")
    # 204 No Content by spec
    return Response(status_code=204)
