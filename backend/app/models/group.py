# dummy models for now
from tortoise import fields
from tortoise.models import Model

class Group(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, unique=True)
