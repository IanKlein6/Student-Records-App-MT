# backend/app/routers/students.py
import logging
from typing import Optional, List
from fastapi import APIRouter, Path, Query, HTTPException, Response, Body
from tortoise.exceptions import IntegrityError

from app.models.student import Student, StudentStatus
from app.schemas.student import (StudentCreate, StudentPatch, StudentRead, StudentList, ArchiveRequest, RestoreRequest)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/students", tags=["students"])

@router.post("", response_model=StudentRead, status_code=201)
async def create_student(payload: StudentCreate, response: Response):
    try:
        student = await Student.create(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            semester_id=payload.semester_id,
            group_id=payload.group_id,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists")
    response.headers["Location"] = f"/students/{student.id}"
    logger.info("student.create ok id=%s email=%s", student.id, student.email)
    return StudentRead.model_validate(student, from_attributes=True)

@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id(student_id: int = Path(..., ge=1)):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentRead.model_validate(student, from_attributes=True)

@router.get("", response_model=List[StudentList])
async def list_student(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    qs = Student.all()
    if first_name:
        qs = qs.filter(first_name__icontains=first_name)
    if last_name:
        qs = qs.filter(last_name__icontains=last_name)
    if email:
        qs = qs.filter(email__icontains=email)
    rows = await qs.limit(limit).offset(offset)
    return [StudentList.model_validate(r, from_attributes=True) for r in rows]

@router.patch("/{student_id}", response_model=StudentRead)
async def patch_student(student_id: int, payload: StudentPatch = Body(...)):
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
        raise HTTPException(status_code=409, detail="Email already exists")

    return StudentRead.model_validate(student, from_attributes=True)

@router.post("/{student_id}/archive", status_code=204)
async def archive_student(student_id: int, body: ArchiveRequest = Body(default=ArchiveRequest())):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.archive(body.reason)
    return Response(status_code=204)

@router.post("/{student_id}/restore", status_code=204)
async def restore_student(student_id: int, body: RestoreRequest = Body(default=RestoreRequest())):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.restore(body.reason)
    return Response(status_code=204)

@router.api_route("/{student_id}", methods=["DELETE"], include_in_schema=False)
async def delete_student_public(student_id: int = Path(..., ge=1)):
    raise HTTPException(status_code=404, detail="Student not found")
