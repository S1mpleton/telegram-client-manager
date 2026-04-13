from fastapi import APIRouter

from .v1 import router_v1

router_api = APIRouter(
    prefix="/api"
)

router_api.include_router(router_v1)

__all__ = ("router_api",)
