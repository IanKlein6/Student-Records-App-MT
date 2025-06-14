from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.models.student import Student

app = FastAPI()

@app.post("/student/")
async def create_student(name: str, email: str):
    student = await Student.create(name=name, email=email)
    return student

@app.get("/student/")
async def get_student():
    return await Student.all()

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/student_records",
    modules={"models": ["app.models.student"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
