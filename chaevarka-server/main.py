from contextlib import asynccontextmanager
import secrets
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.config import settings
from core.models.db_helper import db_helper
from api.api_v1.router import router as api_router
from views import router as views_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

if settings.docs_password:
    _security = HTTPBasic()

    def _check_docs_auth(credentials: HTTPBasicCredentials = Depends(_security)):
        ok = secrets.compare_digest(
            credentials.password.encode(), settings.docs_password.encode()
        )
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
            )

    @main_app.get("/openapi.json", include_in_schema=False)
    async def openapi(_: None = Depends(_check_docs_auth)):
        return main_app.openapi()

    @main_app.get("/docs", include_in_schema=False)
    async def docs(_: None = Depends(_check_docs_auth)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API docs")

    @main_app.get("/redoc", include_in_schema=False)
    async def redoc(_: None = Depends(_check_docs_auth)):
        return get_redoc_html(openapi_url="/openapi.json", title="API docs")

main_app.include_router(api_router)
main_app.include_router(views_router)
if __name__  == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )