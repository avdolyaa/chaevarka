from fastapi import APIRouter

from api.api_v1.endpoints.devices import router as devices_router

router = APIRouter(prefix="/api/v1")
router.include_router(
    devices_router,
    prefix="/devices"
)