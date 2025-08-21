from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from core.config import settings
from core.models.db_helper import db_helper
from api.api_v1.endpoints.devices import router as devices_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)

main_app.include_router(devices_router)

if __name__  == "__main__":
    print("DB URL:", settings.db.url)
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )