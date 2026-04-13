from typing import Annotated
from uuid import UUID
from enum import StrEnum

from fastapi import Header, Depends
from shared_http.responses import http_400_bad_request, http_500_internal_server_error


class HeaderNames(StrEnum):
    X_USER_ID = "X-USER-ID"
    X_AUTH_ID = "X-AUTH-ID"


def get_user_id_from_header(x_user_id: Annotated[UUID, Header(alias=HeaderNames.X_USER_ID)] = None) -> UUID:
    if x_user_id is None:
        raise http_400_bad_request()(detail="X-USER-ID header is missing")

    return x_user_id


def get_auth_id_from_header(x_auth_id: Annotated[UUID, Header(alias=HeaderNames.X_AUTH_ID)] = None) -> UUID:
    if x_auth_id is None:
        raise http_400_bad_request()(detail="X-AUTH-ID header is missing")

    return x_auth_id

