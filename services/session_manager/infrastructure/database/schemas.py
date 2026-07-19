import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import SessionModel

_TortoiseSessionCreateSchema = pydantic_model_creator(
    SessionModel,
    name="SessionCreate",
    exclude_readonly=True,
)

_TortoiseSessionReadSchema = pydantic_model_creator(
    SessionModel,
    name="SessionRead"
)

_TortoiseSessionUpdateSchema = pydantic_model_creator(
    SessionModel,
    name="SessionUpdate",
    exclude_readonly=True,
    exclude=(
        "created_at",
        "updated_at"
    )
)


class SessionCreateSchema(BaseModel):
    phone_number: str = Field()
    api_id: int = Field()
    api_hash: str = Field()
    session_string: Union[bool, None] = Field(default=None)

    @classmethod
    async def from_tortoise(cls, session_model: SessionModel):
        user_data = await _TortoiseSessionCreateSchema.from_tortoise_orm(session_model)
        return cls(
            **user_data.model_dump()
        )


class UserReadSchema(BaseModel):
    id: UUID

    phone_number: Union[str, None] = None
    api_id: Union[int, None] = None
    api_hash: Union[str, None] = None
    session_string: Union[bool, None] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    async def from_tortoise(cls, session_model: SessionModel):
        user_data = await _TortoiseSessionReadSchema.from_tortoise_orm(session_model)

        return cls(
            **user_data.model_dump()
        )


class UserUpdateSchema(BaseModel):
    phone_number: Union[str, None] = None
    api_id: Union[int, None] = None
    api_hash: Union[str, None] = None
    session_string: Union[bool, None] = None

    @classmethod
    async def from_tortoise(cls, session_model: SessionModel):
        user_data = await _TortoiseSessionUpdateSchema.from_tortoise_orm(session_model)

        return cls(
            **user_data.model_dump()
        )
