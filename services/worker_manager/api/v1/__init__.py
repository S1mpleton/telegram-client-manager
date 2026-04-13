from fastapi import APIRouter


from .clients import router as clients_router

router_v1 = APIRouter(
    prefix="/v1"
)


router_v1.include_router(clients_router)

__all__ = ("router_v1",)
