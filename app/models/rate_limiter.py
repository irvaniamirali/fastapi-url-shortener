from tortoise.models import Model
from tortoise import fields


class TokenBucket(Model):
    user_id = fields.CharField(max_length=10, pk=True)
    tokens = fields.IntField()
    last_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "token_buckets"
