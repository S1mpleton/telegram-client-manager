from tortoise.models import Model
from tortoise import fields



class UserModel(Model):
    id = fields.UUIDField(primary_key=True)
    email = fields.CharField(unique=True, max_length=128, null=False)
    password_hash = fields.CharField(max_length=2048, null=False)
    is_email_verified = fields.BooleanField(default=False)

    # metadata
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_login_at = fields.DatetimeField(null=True)

    class Meta:
        ordering = ["id"]
        table = "Users"
