from tortoise import fields
from tortoise.models import Model

class Student(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)

    comment = fields.TextField(null=True)
    tutor_name = fields.CharField(max_length=100)

    semester = fields.ForeignKeyField("models.Semester", related_name="students", null=True)
    current_group = fields.ForeignKeyField("models.Group", related_name="students", null=True)

    active = fields.BooleanField(default=True)
    archived = fields.BooleanField(default=False)
    passed_all = fields.BooleanField(default=False)
    
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
