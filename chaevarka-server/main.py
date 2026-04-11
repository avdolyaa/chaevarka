from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from core.config import settings
from core.models.db_helper import db_helper
from api.api_v1.router import router as api_router
from views import router as views_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)

main_app.include_router(api_router)
main_app.include_router(views_router)
if __name__  == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )