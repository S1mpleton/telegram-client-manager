from fastapi import status
from typing import Optional, Type
from pydantic import BaseModel

from core.model_creator import create_response_model, ApiErrorContainer


def _response_factory(status_code: int, default_message: str, default_detail: str):
    def wrapper(payload_model: Optional[Type[BaseModel]] = None, **kwargs) -> Type[ApiErrorContainer]:
        return create_response_model(
            default_message=default_message,
            default_detail=default_detail,
            status_code=status_code,
            model=payload_model,
            **kwargs
        )

    return wrapper


http_200_ok = _response_factory(
    status.HTTP_200_OK,
    default_message="OK",
    default_detail="It is ok"
)

http_202_accepted = _response_factory(
    status.HTTP_202_ACCEPTED,
    default_message="Accepted",
    default_detail="Action not completed"
)

http_400_bad_request = _response_factory(
    status.HTTP_400_BAD_REQUEST,
    default_message="Conflict",
    default_detail="Bad request"
)

http_401_unauthorized = _response_factory(
    status.HTTP_401_UNAUTHORIZED,
    default_message="Unauthorized",
    default_detail="Client unauthorized"
)

http_404_not_found = _response_factory(
    status.HTTP_404_NOT_FOUND,
    default_message="Not Found",
    default_detail="Resource not found"
)

http_500_internal_server_error = _response_factory(
    status.HTTP_404_NOT_FOUND,
    default_message="Server error",
    default_detail="Server side error"
)
