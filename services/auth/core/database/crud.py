"""
Create
Read
Update
Delete
"""
from typing import Union
import logging
from pydantic import EmailStr

from core.database.models import UserModel
from api.v1.schemas.auth_schemas import UserOutSchema, AuthSchema
from core.exceptions import NotFoundException, InternalServerException, ConflictException
from core.hashing import get_password_hash


class CRUD:
    @classmethod
    async def create_user(cls, auth_schema: AuthSchema) -> UserOutSchema:
        if await cls.check_user_exist_by_email(auth_schema.email):
            raise ConflictException(detail="This email already exist")

        try:
            user_model = await UserModel.create(
                **auth_schema.model_dump(),
                password_hash=get_password_hash(auth_schema.password)
            )
            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Create user: {e}")
            raise InternalServerException(f"Create user: {e}")

    @classmethod
    async def read_user_by_email(cls, email: Union[EmailStr, str]) -> UserOutSchema:
        if not await cls.check_user_exist_by_email(email):
            raise NotFoundException(detail="Email not found")

        try:
            user_model = await UserModel.get(email=str(email))
            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Read user by email: {e}")
            raise InternalServerException(detail=f"Read user by email: {e}")

    @classmethod
    async def check_user_exist_by_email(cls, email: Union[EmailStr, str]) -> bool:
        try:
            return await UserModel.filter(email=str(email)).exists()
        except Exception as e:
            logging.error(f"Check user exist by email: {e}")
            raise InternalServerException(detail=f"Check user exist by email: {e}")
