import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from shared_http.responses import (
    http_200_ok,
    http_401_unauthorized,
    http_500_internal_server_error
)

from api.v1.schemas.responses import (
    ResponseTokenInfoWithoutRefresh,
)
from core.jwt_token.config import REFRESH_TOKEN_TYPE
from core.jwt_token.getter import get_access_token
from core.jwt_token.validate import http_bearer, ValidateToken
from infrastructure.database import UserOutSchema

router = APIRouter()


@router.post(
    "/refresh",
    dependencies=[Depends(http_bearer)],
    response_model_exclude_none=True,
    responses={
        200: {
            "model": http_200_ok(ResponseTokenInfoWithoutRefresh).model
        },
        401: {
          "model": http_401_unauthorized().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def update_access(
        user_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=REFRESH_TOKEN_TYPE))]
):
    try:
        access_token = get_access_token(user_out_schema)
        return http_200_ok(ResponseTokenInfoWithoutRefresh)(
            payload=ResponseTokenInfoWithoutRefresh(
                access_token=access_token
            )
        ).json_response

    except Exception as e:
        logging.error(f"Router refresh: {e}")
        raise http_500_internal_server_error()(detail=f"Router refresh: {e}")
