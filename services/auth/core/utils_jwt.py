import jwt
from typing import Union
from datetime import datetime, timedelta

from zoneinfo import ZoneInfo

from api.v1.schemas.auth_schemas import UserOutSchema
from core.config import SETTINGS

TOKEN_TYPE_FIELD = "type"
ACCESS_LEVEL_FIELD = "rights"

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
        payload: dict,
        private_key: str = SETTINGS.auth_jwt.private_key_path.read_text(),
        algorithm: str = SETTINGS.auth_jwt.algorithm,
        expire_minutes: int = SETTINGS.auth_jwt.access_token_expire_minutes,
        expire_timedelta: Union[timedelta, None] = None
) -> str:
    to_encode = payload.copy()

    now_date_time = datetime.now(tz=ZoneInfo(SETTINGS.database.timezone))

    if expire_timedelta:
        expire = now_date_time + expire_timedelta
    else:
        expire = now_date_time + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now_date_time
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        jwt_token: Union[str, bytes],
        public_key: str = SETTINGS.auth_jwt.public_key_path.read_text(),
        algorithm: str = SETTINGS.auth_jwt.algorithm
):
    decoded = jwt.decode(jwt_token, public_key, algorithms=[algorithm])
    return decoded


def create_jwt(
        token_type: str,
        payload: dict,
        expire_minutes: int = SETTINGS.auth_jwt.access_token_expire_minutes,
        expire_timedelta: Union[timedelta, None] = None
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type
    }

    jwt_payload.update(payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def get_access_token(
        user_out_schema: UserOutSchema
) -> str:
    jwt_payload = {
        "sub": str(user_out_schema.id),
        "email": user_out_schema.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=SETTINGS.auth_jwt.access_token_expire_minutes
    )


def get_refresh_token(
        user_out_schema: UserOutSchema
) -> str:
    jwt_payload = {
        "sub": str(user_out_schema.id),
        "email": user_out_schema.email,
        # ACCESS_LEVEL_FIELD: user_out_schema.access_level
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=SETTINGS.auth_jwt.refresh_token_expire_days)
    )
