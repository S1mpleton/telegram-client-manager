from datetime import timedelta

from infrastructure.database import UserOutSchema
from core.config import SETTINGS

from .config import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from .utils import create_jwt


def get_access_token(
        auth_out_schema: UserOutSchema
) -> str:
    jwt_payload = {
        "sub": str(auth_out_schema.id),
        "email": auth_out_schema.email,
        "email_verified": auth_out_schema.is_email_verified
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=SETTINGS.auth_jwt.access_token_expire_minutes
    )


def get_refresh_token(
        auth_out_schema: UserOutSchema
) -> str:
    jwt_payload = {
        "sub": str(auth_out_schema.id),
        "email": auth_out_schema.email,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=SETTINGS.auth_jwt.refresh_token_expire_days)
    )
