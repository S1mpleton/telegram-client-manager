from tortoise.models import Model
from tortoise import fields



class ClientModel(Model):
    id = fields.IntField(primary_key=True)
    cid = fields.BigIntField(unique=True, generated=False, null=False)
    user_id = fields.BigIntField(unique=True, generated=False, null=False)
    name = fields.CharField(max_length=16, null=False)
    session_string = fields.CharField(max_length=2048, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        table = "Clients"
