# app/schemas/student.py
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.student import Student

# Response shape (includes id, timestamps, etc.)
StudentOut = pydantic_model_creator(Student, name="StudentOut")

# Input shape (excludes read-only fields like id/created_at/updated_at)
StudentIn = pydantic_model_creator(Student, name="StudentIn", exclude_readonly=True)
