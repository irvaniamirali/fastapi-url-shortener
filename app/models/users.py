from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField(unique=True)
    full_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=60)
