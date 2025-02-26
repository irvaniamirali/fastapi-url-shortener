from tortoise import Model, fields


class Admin(Model):
    id = fields.IntField(primary_key=True)
    admin_key = fields.CharField(max_length=12, unique=True)


class URL(Model):
    id = fields.IntField(primary_key=True)
    url = fields.CharField(max_length=255)
    key = fields.CharField(max_length=6, unique=True)
    clicks = fields.IntField(default=0)
    expire = fields.DatetimeField(null=True)
    admin = fields.ForeignKeyField("models.Admin", related_name="urls")
