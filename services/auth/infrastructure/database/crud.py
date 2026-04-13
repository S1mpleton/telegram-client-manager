from typing import Union

import logging
from uuid import UUID

from pydantic import EmailStr
from shared_http.responses import (
    http_500_internal_server_error,
    http_404_not_found,
    http_409_conflict
)

from api.v1.schemas.requests import RequestAuthSchema
from core.dependencies.hashing import get_password_hash

from .models import UserModel
from .schemas import UserOutSchema, UserUpdateSchema


class CRUD:
    def __init__(self):
        pass

    @classmethod
    async def create_user(cls, auth_schema: RequestAuthSchema) -> UserOutSchema:
        if await cls.check_user_exist_by_email(auth_schema.email):
            raise http_409_conflict()(detail="This email already exist")

        try:
            user_model = await UserModel.create(
                **auth_schema.model_dump(),
                password_hash=get_password_hash(auth_schema.password)
            )
            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Create user: {e}")
            raise http_500_internal_server_error()(detail=f"Create user: {e}")

    @classmethod
    async def read_user_by_email(cls, email: Union[EmailStr, str]) -> UserOutSchema:
        if not await cls.check_user_exist_by_email(email):
            raise http_404_not_found()(detail="Email not found")

        try:
            user_model = await UserModel.get(email=str(email))
            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Read user by email: {e}")
            raise http_500_internal_server_error()(detail=f"Read user by email: {e}")

    @classmethod
    async def read_auth_by_id(cls, auth_id: Union[UUID, str]) -> UserOutSchema:
        if not await cls.check_user_exist_by_id(auth_id):
            raise http_404_not_found()(detail="Auth not found")

        try:
            user_model = await UserModel.get(id=str(auth_id))
            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Read user by id: {e}")
            raise http_500_internal_server_error()(detail=f"Read user by id: {e}")

    @classmethod
    async def update_user_by_email(
            cls,
            email: Union[EmailStr, str],
            user_update_schema: UserUpdateSchema
    ) -> UserOutSchema:
        if not await cls.check_user_exist_by_email(email):
            raise http_404_not_found()(detail="Email not found")

        try:
            user_model = await UserModel.get(email=str(email))
            user_model = user_model.update_from_dict(user_update_schema.model_dump(exclude_none=True))
            await user_model.save()

            return await UserOutSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Read user by email: {e}")
            raise http_500_internal_server_error()(detail=f"Read user by email: {e}")

    @classmethod
    async def check_user_exist_by_email(cls, email: Union[EmailStr, str]) -> bool:
        try:
            return await UserModel.filter(email=str(email)).exists()
        except Exception as e:
            logging.error(f"Check user exist by email: {e}")
            raise http_500_internal_server_error()(detail=f"Check user exist by email: {e}")

    @classmethod
    async def check_user_exist_by_id(cls, auth_id: Union[UUID, str]) -> bool:
        try:
            return await UserModel.filter(id=str(auth_id)).exists()
        except Exception as e:
            logging.error(f"Check user exist by id: {e}")
            raise http_500_internal_server_error()(detail=f"Check user exist by id: {e}")
