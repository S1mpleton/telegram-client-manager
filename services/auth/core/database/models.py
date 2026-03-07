from tortoise.models import Model
from tortoise import fields



class UserModel(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(unique=True, max_length=128, null=False)
    password_hash = fields.CharField(max_length=2048, null=False)

    class Meta:
        ordering = ["id"]
        table = "Users"
