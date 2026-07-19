from tortoise.models import Model
from tortoise import fields



class SessionModel(Model):
    id = fields.UUIDField(primary_key=True)
    # client_id = fields.UUIDField(null=False)
    phone_number = fields.CharField(max_length=32, default=None)
    api_id = fields.IntField(default=None)
    api_hash = fields.CharField(max_length=64, default=None)
    session_string = fields.CharField(max_length=128, default=None)
    # auth_status: AuthStatus  # pending/active/expired/revoked

    # metadata
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    class Meta:
        ordering = ["id"]
        table = "Users"
