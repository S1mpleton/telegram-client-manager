"""
Create
Read
Update
Delete
"""
from typing import Union
import logging
from pydantic import EmailStr

from api.v1.schemas import http_500_internal_server_error
from database.models import ClientModel


class CRUD:
    def __init__(self):
        pass

    @classmethod
    async def create_client(cls, user_id: int,) -> UserOutSchema:
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
    async def check_client_exist_by_user_id_and_name(cls, user_id: int, client_name: str) -> bool:
        try:
            return await ClientModel.filter(user_id=user_id, name=client_name).exists()
        except Exception as e:
            logging.error(f"Check client exist by email: {e}")
            raise http_500_internal_server_error()(detail=f"Check client exist by email: {e}")
