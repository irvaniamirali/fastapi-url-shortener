from tortoise import Model, fields

from app.utils import generate_random_string


class URL(Model):
    id = fields.IntField(primary_key=True)
    target_url = fields.CharField(max_length=2000, unique=True)  # RFC 3986
    secret_key = fields.CharField(max_length=6, unique=True, default=generate_random_string())
    clicks = fields.IntField(default=0)
