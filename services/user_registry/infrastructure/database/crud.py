from typing import Union

import logging
from uuid import UUID

from pydantic import EmailStr
from shared_http.responses import (
    http_500_internal_server_error,
    http_404_not_found,
    http_409_conflict
)

from .models import UserModel
from .schemas import (
    UserReadSchema,
    UserCreateSchema, UserUpdateSchema,
)


class CRUD:
    def __init__(self):
        pass

    @classmethod
    async def create_user(cls, user_create_schema: UserCreateSchema) -> UserReadSchema:
        if await cls.check_user_exist_by_email(user_create_schema.email):
            raise http_409_conflict()(detail="This email already exist")

        if await cls.check_user_exist_by_auth_id(user_create_schema.auth_id):
            raise http_409_conflict()(detail="This auth id already exist")

        try:
            user_model = await UserModel.create(
                **user_create_schema.model_dump()
            )
            return await UserReadSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Create user: {e}")
            raise http_500_internal_server_error()(detail=f"Create user: {e}")

    @classmethod
    async def read_user_by_email(cls, email: Union[EmailStr, str]) -> UserReadSchema:
        if not await cls.check_user_exist_by_email(email):
            raise http_404_not_found()(detail="Email not found")

        try:
            user_model = await UserModel.get(email=str(email))
            return await UserReadSchema.from_tortoise(user_model)

        except Exception as e:
            logging.error(f"Read user by email: {e}")
            raise http_500_internal_server_error()(detail=f"Read user by email: {e}")

    @classmethod
    async def update_user_by_email(
            cls,
            email: Union[EmailStr, str],
            user_update_schema: UserUpdateSchema
    ) -> UserReadSchema:
        if not await cls.check_user_exist_by_email(email):
            raise http_404_not_found()(detail="Email not found")

        try:
            user_model = await UserModel.get(email=str(email))
            user_model = user_model.update_from_dict(user_update_schema.model_dump(exclude_none=True))
            await user_model.save()

            return await UserReadSchema.from_tortoise(user_model)

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
    async def check_user_exist_by_auth_id(cls, auth_id: Union[str, UUID]) -> bool:
        try:
            return await UserModel.filter(auth_id=str(auth_id)).exists()
        except Exception as e:
            logging.error(f"Check user exist by auth id: {e}")
            raise http_500_internal_server_error()(detail=f"Check user exist by auth id: {e}")

