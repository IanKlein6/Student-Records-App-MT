from enum import Enum
from tortoise import fields
from tortoise.models import Model

class ArchiveAction(str, Enum):
    SOFT_ARCHIVE = "soft_archive"
    RESTORE = "restore"
    HARD_DELETE = "hard_delete"

class ArchiveLog(Model):
    id = fields.IntField(pk=True)
    # Keep logs even if the Student is hard-deleted
    student = fields.ForeignKeyField(
        "models.Student",
        related_name="archive_logs",
        null=True,
        on_delete=fields.SET_NULL,
    )
    action = fields.CharEnumField(ArchiveAction)
    reason = fields.CharField(max_length=250, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
