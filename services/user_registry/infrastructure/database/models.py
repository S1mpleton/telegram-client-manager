from enum import StrEnum

from tortoise.models import Model
from tortoise import fields


class AccessLevel(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    DELETED = "deleted"


class SubscriptionTier(StrEnum):
    FREE = "free"
    PRO = "pro"


class UserModel(Model):
    id = fields.UUIDField(primary_key=True)
    auth_id = fields.UUIDField(null=True, index=True, unique=True)

    email = fields.CharField(unique=True, max_length=128, null=False)
    username = fields.CharField(max_length=64, default="User")

    # access control
    access_level = fields.CharEnumField(AccessLevel, default=AccessLevel.USER)

    # subscription
    subscription_tier = fields.CharEnumField(SubscriptionTier, default=SubscriptionTier.FREE)
    subscription_ends_at = fields.DatetimeField(null=True)

    # status
    status = fields.CharEnumField(UserStatus, default=UserStatus.ACTIVE)

    # metadata
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_login_at = fields.DatetimeField(null=True)

    class Meta:
        table = "Users"
        ordering = ["-created_at"]
