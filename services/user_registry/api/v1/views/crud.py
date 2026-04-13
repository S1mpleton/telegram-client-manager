import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query
from pydantic import EmailStr
from shared_http.responses import (
    http_200_ok,
    http_404_not_found,
    http_500_internal_server_error,
    http_409_conflict
)

from api.v1.schemas.requests.user import RequestCreateUserModel
from core.head_parser import (
    get_auth_id_from_header
)
from infrastructure.database import CRUD, UserReadSchema, UserCreateSchema

router = APIRouter(
    tags=["clients 👨🏻‍💼👩🏻‍💼"],
    prefix="/client",
)


@router.post(
    "/create",
    summary="",
    responses={
        200: {
            "model": http_200_ok(UserReadSchema).model
        },
        409: {
            "model": http_409_conflict().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def create_user(
        auth_id: Annotated[UUID, Depends(get_auth_id_from_header)],
        request_create_user_model: Annotated[RequestCreateUserModel, Body(...)]
):
    user_create_schema = UserCreateSchema(
        auth_id=auth_id,
        **request_create_user_model.model_dump()
    )

    user_reade_schema = await CRUD.create_user(user_create_schema)

    try:
        return http_200_ok(UserReadSchema)(
            payload=user_reade_schema
        ).json_response

    except Exception as e:
        logging.error(f"Router create: {e}")
        raise http_500_internal_server_error()(detail=f"Router create: {e}")


@router.get(
    "/getByEmail",
    summary="",
    responses={
        200: {
            "model": http_200_ok(UserReadSchema).model
        },
        404: {
            "model": http_404_not_found().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def get_user(
        user_email: Annotated[EmailStr, Query(...)]
):
    user_read_schema = await CRUD.read_user_by_email(user_email)

    try:
        return http_200_ok(UserReadSchema)(
            payload=user_read_schema
        ).json_response

    except Exception as e:
        logging.error(f"Router getByEmail: {e}")
        raise http_500_internal_server_error()(detail=f"Router getByEmail: {e}")
