from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from core.database.models import UserModel

TortoiseUserOutSchema = pydantic_model_creator(UserModel, name="TortoiseUserOutSchema")


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"

class TokenInfoWithoutRefresh(TokenInfo):
    refresh_token: Optional[str] = Field(exclude=True, default=None)




class AuthSchema(BaseModel):
    email: EmailStr = Field(description="User's email")
    password: str = Field(description="User's password", max_length=32)


class UserOutSchema(BaseModel):
    id: int = Field(description="User's id", ge=1)
    password_hash: str = Field(description="User's password hash", max_length=2048)
    email: EmailStr = Field(description="User's email")

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await TortoiseUserOutSchema.from_tortoise_orm(auth_model)
        return cls(
            **user_data.model_dump()
        )


class ResponseUserSchema(UserOutSchema):
    id: int = Field(exclude=True)

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await TortoiseUserOutSchema.from_tortoise_orm(auth_model)
        return cls(
            **user_data.model_dump(exclude={'id'})
        )
