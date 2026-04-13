from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import UserModel

TortoiseUserOutSchema = pydantic_model_creator(UserModel, name="TortoiseUserOutSchema")


class UserOutSchema(BaseModel):
    id: UUID = Field(description="User's id")
    password_hash: str = Field(description="User's password hash", max_length=2048)
    email: EmailStr = Field(description="User's email")
    is_email_verified: bool = Field(description="Email verify", default=False)

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await TortoiseUserOutSchema.from_tortoise_orm(auth_model)
        return cls(
            **user_data.model_dump()
        )

class UserUpdateSchema(BaseModel):
    password_hash: Union[str | None] = Field(max_length=2048, default=None)
    email: Union[EmailStr | None] = Field(default=None)
    is_email_verified: Union[bool | None] = Field(default=None)
