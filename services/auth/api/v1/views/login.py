import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from shared_http.responses import (
    http_200_ok,
    http_404_not_found,
    http_500_internal_server_error
)

from core.jwt_token.getter import get_access_token, get_refresh_token
from core.jwt_token.validate import validate_login
from infrastructure.database import UserOutSchema
from api.v1.schemas.responses import ResponseTokenInfo

router = APIRouter()


@router.post(
    "/login",
    summary="Authentication users",
    responses={
        200: {
            "model": http_200_ok(ResponseTokenInfo).model
        },
        404: {
            "model": http_404_not_found().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def authentication(
        user_out_schema: Annotated[UserOutSchema, Depends(validate_login)]
):
    try:
        access_token = get_access_token(user_out_schema)
        refresh_token = get_refresh_token(user_out_schema)

        return http_200_ok(ResponseTokenInfo)(
            payload=ResponseTokenInfo(
                access_token=access_token,
                refresh_token=refresh_token
            )
        ).json_response

    except Exception as e:
        logging.error(f"Router login: {e}")
        raise http_500_internal_server_error()(detail=f"Router login: {e}")
