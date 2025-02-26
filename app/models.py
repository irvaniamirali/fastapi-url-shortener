from tortoise import Model, fields


class URL(Model):
    id = fields.IntField(primary_key=True)
    url = fields.CharField(max_length=2000)  # RFC 3986
    key = fields.CharField(max_length=6, unique=True)
    clicks = fields.IntField(default=0)
    expire = fields.DatetimeField(null=True)
    admin_url = fields.CharField(max_length=8, unique=True)
