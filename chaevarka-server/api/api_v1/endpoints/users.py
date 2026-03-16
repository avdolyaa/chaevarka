from fastapi import APIRouter

from api.api_v1.schemas.user import UserRead, UserCreate, UserUpdate
from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.fastapi_users import fastapi_users
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Users"]
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)