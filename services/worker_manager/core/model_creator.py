from typing import Optional, TypeVar, Type, Generic
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, create_model, Field

T = TypeVar('T', bound=BaseModel)


class ApiResponse(BaseModel, Generic[T]):
    message: str
    detail: str
    status_code: int

    @property
    def json_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=self.status_code
        )


class ApiErrorContainer(Exception):
    model: Type[BaseModel]

    def __init__(self, model_instance: ApiResponse):
        self._model_instance = model_instance

    @property
    def json_response(self):
        return self._model_instance.json_response


def create_response_model(
        default_message: Optional[str] = None,
        default_detail: Optional[str] = None,
        model: Optional[Type[BaseModel]] = None,
        status_code: int = status.HTTP_200_OK,
        **other_data
) -> Type[ApiErrorContainer]:
    try:
        fields = {
            'message': (Optional[str], default_message),
            'detail': (Optional[str], default_detail),
            "status_code": (Optional[int], Field(default=status_code, exclude=True)),
        }

        fields.update(other_data)

        if model:
            fields['payload'] = (Optional[model], None)

        response_model = create_model(
            f"DynamicResponse_{model.__name__ if model else 'Base'}",
            **fields,
            __base__=ApiResponse if not model else ApiResponse[model]
        )

        class ResponseException(ApiErrorContainer):
            model = response_model

            def __init__(self, **kwargs):
                instance = response_model(**kwargs)
                super().__init__(instance)

        return ResponseException

    except Exception as e:
        raise HTTPException(
            detail=f"{e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
