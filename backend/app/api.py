# backend/app/api.py

"""FastApi application factory and configs.

Creates and configures the FastAPI application instance with:
    - Health check endpoint
    - Router registration for all API endpoints
    - Tortoise ORM integration (for non-test environments)

Environment Variables:
    TESTING: Set to "1" to skip database registration (for pytest-ing)

Database Models:
    When adding new models, register them in the Tortoise modules list to ensure proper schema generation and relationship handling.
"""

import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from backend.app.routers.router_student import router as students_router
from backend.app.routers.router_admin import router as admin_router

TESTING = os.getenv("TESTING") == "1"

app = FastAPI(title="Student Records API")

@app.get("/")
async def health():
    return {"message": "OK"}

# Register routers
app.include_router(students_router) 
app.include_router(admin_router)    

# Database configs (skip during testing)
if not TESTING:
    register_tortoise(
        app,
        db_url="postgres://postgres:postgres@localhost:5432/student_records",
        modules={
            "models": [
                "app.models.student", ## Might have to add backend. to the beginning of all of them to make it work right??? 
                "app.models.group", 
                "app.models.semester", 
                "app.models.archive_log",
            ]
        },
        generate_schemas=False,
        add_exception_handlers=True,
    )
