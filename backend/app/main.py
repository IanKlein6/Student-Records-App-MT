# backend/app/main.py
import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers.students import router as students_router
from app.routers.admin import router as admin_router

TESTING = os.getenv("TESTING") == "1"

app = FastAPI(title="Student Records API")

@app.get("/")
async def health():
    return {"message": "OK"}

# Endpoints routers1
app.include_router(students_router) 
app.include_router(admin_router)    

if not TESTING:
    register_tortoise(
        app,
        db_url="postgres://postgres:postgres@localhost:5432/student_records",
        modules={"models": ["app.models.student", "app.models.group", "app.models.semester"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
