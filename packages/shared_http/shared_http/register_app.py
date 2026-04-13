from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .responses import ApiErrorContainer


async def global_handler(request: Request, exc: ApiErrorContainer):
    return JSONResponse(
        status_code=exc._model_instance.status_code,
        content=exc._model_instance.model_dump(exclude_none=True)
    )


class RegisterApp:
    def __call__(self, app: FastAPI, *args, **kwargs):
        app.add_exception_handler(ApiErrorContainer, global_handler)