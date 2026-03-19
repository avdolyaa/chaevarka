from fastapi import APIRouter, Depends

from .endpoints.auth import router as auth_router
from .endpoints.users import router as users_router
from .endpoints.devices import router as devices_router
from .endpoints.tea_make import router as tea_make_router
from .endpoints.health import router as health_router
from fastapi.security import HTTPBearer
http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(dependencies=[Depends(http_bearer)],)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(devices_router)
router.include_router(tea_make_router)
router.include_router(health_router)