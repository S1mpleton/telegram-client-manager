import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from shared_http.responses import (
    http_200_ok,
    http_409_conflict,
    http_500_internal_server_error
)

from api.v1.schemas.responses import ResponseTokenInfo
from infrastructure.broker.fs_broker import user_registered
from core.jwt_token.getter import get_access_token, get_refresh_token
from core.jwt_token.validate import validate_register
from infrastructure.broker.schemas.user import UserRegisteredSchema
from infrastructure.database import UserOutSchema

router = APIRouter()


@router.post(
    "/register",
    responses={
        200: {
            "model": http_200_ok(ResponseTokenInfo).model
        },
        409: {
            "model": http_409_conflict().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def register(
        auth_out_schema: Annotated[UserOutSchema, Depends(validate_register)]
):
    try:
        access_token = get_access_token(auth_out_schema)
        refresh_token = get_refresh_token(auth_out_schema)

        await user_registered.publish(
            message=UserRegisteredSchema(
                auth_id=auth_out_schema.id,
                **auth_out_schema.model_dump()
            )
        )

        return http_200_ok(ResponseTokenInfo)(
            payload=ResponseTokenInfo(
                access_token=access_token,
                refresh_token=refresh_token
            )
        ).json_response

    except Exception as e:
        logging.error(f"Router register: {e}")
        raise http_500_internal_server_error()(detail=f"Router register: {e}")
