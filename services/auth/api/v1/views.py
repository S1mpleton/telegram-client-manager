import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.schemas.auth_schemas import TokenInfo, UserOutSchema, TokenInfoWithoutRefresh
from core.exceptions import InternalServerException
from core.utils_jwt import get_access_token, get_refresh_token, REFRESH_TOKEN_TYPE
from core.validate import validate_login, http_bearer, ValidateToken, validate_register

router = APIRouter(
    tags=["Auth 🔒"]
)


@router.post(
    "/register",
    responses={
        200: {
            "model": TokenInfo
        },
    }
)
async def register(
        user_out_schema: Annotated[UserOutSchema, Depends(validate_register)]
):
    try:
        access_token = get_access_token(user_out_schema)
        refresh_token = get_refresh_token(user_out_schema)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )

    except Exception as e:
        logging.error(f"Router register: {e}")
        raise InternalServerException(detail=f"Router register: {e}")


@router.post(
    "/login",
    summary="Authentication users",
    responses={
        200: {
            "model": TokenInfo
        }
    }
)
async def authentication(
        user_out_schema: Annotated[UserOutSchema, Depends(validate_login)]
):
    try:
        access_token = get_access_token(user_out_schema)
        refresh_token = get_refresh_token(user_out_schema)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )

    except Exception as e:
        logging.error(f"Router login: {e}")
        raise InternalServerException(detail=f"Router login: {e}")


@router.post(
    "/refresh",
    dependencies=[Depends(http_bearer)],
    response_model_exclude_none=True,
    response_model=TokenInfoWithoutRefresh,
    responses={
        200: {
            "model": TokenInfoWithoutRefresh
        },
    }
)
async def update_access(
        user_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=REFRESH_TOKEN_TYPE))]
):
    access_token = get_access_token(user_out_schema)
    return TokenInfo(access_token=access_token)
