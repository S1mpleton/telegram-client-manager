from typing import Optional, Union
from uuid import UUID
import datetime

from pydantic import BaseModel, Field, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import (
    UserModel,
    AccessLevel,
    SubscriptionTier,
    UserStatus
)

_TortoiseUserCreateSchema = pydantic_model_creator(
    UserModel,
    name="UserCreate",
    exclude_readonly=True,
    exclude=(
        "access_level",
        "subscription_tier",
        "subscription_ends_at",
        "status",
        "last_login_at"
    )
)

_TortoiseUserReadSchema = pydantic_model_creator(
    UserModel,
    name="UserRead"
)

_TortoiseUserUpdateSchema = pydantic_model_creator(
    UserModel,
    name="UserUpdate",
    exclude_readonly=True,
    exclude=(
        "email",
        "created_at",
        "updated_at"
    )
)


class UserCreateSchema(BaseModel):
    auth_id: Optional[UUID] = Field(default=None)
    email: EmailStr = Field()
    username: str = Field(max_length=64, default="Guest")

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await _TortoiseUserCreateSchema.from_tortoise_orm(auth_model)

        return cls(
            **user_data.model_dump()
        )


class UserReadSchema(BaseModel):
    id: UUID
    auth_id: Optional[UUID] = None

    email: EmailStr
    username: str

    # access control
    access_level: AccessLevel

    # subscription
    subscription_tier: SubscriptionTier
    subscription_ends_at: Optional[datetime.datetime] = None

    # status
    status: UserStatus

    # metadata
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await _TortoiseUserReadSchema.from_tortoise_orm(auth_model)

        return cls(
            **user_data.model_dump()
        )


class UserUpdateSchema(BaseModel):
    auth_id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[Union[EmailStr, str]] = None

    access_level: Optional[AccessLevel] = None
    subscription_tier: Optional[SubscriptionTier] = None
    subscription_ends_at: Optional[datetime.datetime] = None

    status: Optional[UserStatus] = None

    last_login_at: Optional[datetime.datetime] = None

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await _TortoiseUserUpdateSchema.from_tortoise_orm(auth_model)

        return cls(
            **user_data.model_dump()
        )
