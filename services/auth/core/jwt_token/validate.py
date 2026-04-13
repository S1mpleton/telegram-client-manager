import logging
from typing import Annotated

from fastapi import Form, Depends, Query
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import EmailStr
from shared_http.responses import http_500_internal_server_error, http_401_unauthorized

from api.v1.schemas.requests import RequestAuthSchema
from infrastructure.database import CRUD, UserOutSchema
from core.dependencies.hashing import verify_password

from .config import ACCESS_TOKEN_TYPE, TOKEN_TYPE_FIELD
from .utils import decode_jwt

oauth2_shem = OAuth2PasswordBearer(
    tokenUrl=f"api/v1/login",
    auto_error=False
)

http_bearer = HTTPBearer(auto_error=False)


async def validate_register(auth_schema: Annotated[RequestAuthSchema, Form()]) -> UserOutSchema:
    return await CRUD.create_user(auth_schema)


async def validate_login(
        username: EmailStr = Form(),
        password: str = Form()
) -> UserOutSchema:
    user_out_schema = await CRUD.read_user_by_email(username)

    try:
        if verify_password(plain_password=password, hashed_password=user_out_schema.password_hash):
            return user_out_schema

    except Exception as e:
        logging.error(f"Validate login: {e}")
        raise http_500_internal_server_error()(detail=f"Validate login: {e}")

    raise http_401_unauthorized()(detail="Invalid email or password")


def check_header_current_token(
        token: Annotated[str, Depends(oauth2_shem)]
) -> dict:
    try:
        return decode_jwt(jwt_token=token)

    except ExpiredSignatureError:
        raise http_401_unauthorized()(detail="The token's lifetime has expired")

    except InvalidTokenError:
        raise http_401_unauthorized()(detail="Token invalid")


def check_query_current_token(
        token: Annotated[str, Query(...)]
) -> dict:
    try:
        return decode_jwt(jwt_token=token)

    except ExpiredSignatureError:
        raise http_401_unauthorized()(detail="The token's lifetime has expired")

    except InvalidTokenError:
        raise http_401_unauthorized()(detail="Token invalid")


class ValidateToken:
    def __init__(
            self,
            token_type: str = ACCESS_TOKEN_TYPE,
    ):
        self.token_type = token_type

    async def __call__(
            self,
            payload: Annotated[dict, Depends(check_header_current_token)]
    ) -> UserOutSchema:
        self.validate_token_type(payload, self.token_type)
        return await CRUD.read_auth_by_id(payload.get("sub"))

    @classmethod
    def validate_token_type(
            cls,
            payload: dict,
            token_type: str
    ) -> None:
        current_type = payload.get(TOKEN_TYPE_FIELD)
        if not current_type == token_type:
            raise http_401_unauthorized()(detail="Invalid token type")


class ValidateQueryToken(ValidateToken):
    async def __call__(
            self,
            payload: Annotated[dict, Depends(check_query_current_token)]
    ) -> UserOutSchema:
        self.validate_token_type(payload, self.token_type)
        return await CRUD.read_auth_by_id(payload.get("sub"))
