from tortoise.models import Model
from tortoise import fields


class URL(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField("models.User", related_name="urls")
    url = fields.CharField(max_length=255)
    key = fields.CharField(max_length=6, unique=True)
    clicks = fields.IntField(default=0)
    expire_date = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
