from enum import Enum
from tortoise import fields
from tortoise.models import Model

class StudentStatus(str, Enum):
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    ARCHIVE = "archive"

class WordPotential(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Student(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)

    semester_id = fields.ForeignKeyField("models.Semester", related_name="students", null=True)
    group_id = fields.ForeignKeyField("models.Group", related_name="students", null=True)
    

    status = fields.CharEnumField(StudentStatus, default=StudentStatus.ACTIVE)
    attempt_num = fields.IntField(default=0)

    work_student_potential = fields.CharEnumField(WordPotential, null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 
    class Meta:
        indexes = [("last_name", "first_name"), ]