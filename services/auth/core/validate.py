import logging
from typing import Annotated

from fastapi import Form, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import EmailStr

from core.exceptions import InternalServerException, UnauthorizedException
from api.v1.schemas.auth_schemas import UserOutSchema, AuthSchema
from core.database.crud import CRUD
from core.hashing import verify_password
from core.utils_jwt import decode_jwt, ACCESS_TOKEN_TYPE, TOKEN_TYPE_FIELD

oauth2_shem = OAuth2PasswordBearer(
    tokenUrl=f"/login",
    auto_error=False
)

http_bearer = HTTPBearer(auto_error=False)

async def validate_register(auth_schema: Annotated[AuthSchema, Form()]) -> UserOutSchema:
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
        logging.error(f"Validate auth: {e}")
        raise InternalServerException(detail=f"Validate auth: {e}")

    raise UnauthorizedException(detail="Invalid email or password")


def check_current_token(
        token: Annotated[str, Depends(oauth2_shem)]
) -> dict:
    try:
        return decode_jwt(jwt_token=token)

    except ExpiredSignatureError:
        raise UnauthorizedException(detail="The token's lifetime has expired")

    except InvalidTokenError:
        raise UnauthorizedException(detail="Token invalid")


class ValidateToken:
    def __init__(
            self,
            token_type: str = ACCESS_TOKEN_TYPE,
    ):
        self.token_type = token_type

    async def __call__(
            self,
            payload: Annotated[dict, Depends(check_current_token)]
    ) -> UserOutSchema:
        self.validate_token_type(payload, self.token_type)
        return await CRUD.read_user_by_email(payload.get("email"))

    @classmethod
    def validate_token_type(
            cls,
            payload: dict,
            token_type: str
    ) -> None:
        current_type = payload.get(TOKEN_TYPE_FIELD)
        if not current_type == token_type:
            raise UnauthorizedException(detail="Invalid token type")



