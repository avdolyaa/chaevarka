from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from api.api_v1.endpoints.health import health_bd
from core.config import settings
from core.models.db_helper import db_helper
from api.api_v1.endpoints.devices import router as devices_router
from api.api_v1.endpoints.tea_make import router as tea_make_router
from api.api_v1.endpoints.health import router as health_router
from api.api_v1.endpoints.test import router as test_router
from api.api_v1.endpoints.auth import router as auth_router
from api.api_v1.endpoints.users import router as user_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)

main_app.include_router(devices_router)
main_app.include_router(tea_make_router)
main_app.include_router(health_router)
main_app.include_router(test_router)
main_app.include_router(auth_router)
main_app.include_router(user_router)
if __name__  == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )