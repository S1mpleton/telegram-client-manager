from fastapi import APIRouter

from .views import *

router_v1 = APIRouter(
    prefix="/v1"
)

router_v1.include_router(register_router)
router_v1.include_router(login_router)
router_v1.include_router(refresh_router)
router_v1.include_router(email_actions_router)
router_v1.include_router(email_code_router)

__all__ = (
    "router_v1",
)
