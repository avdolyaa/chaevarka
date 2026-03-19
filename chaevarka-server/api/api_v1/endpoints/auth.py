from fastapi import APIRouter

from api.api_v1.schemas.user import UserRead, UserCreate
from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.fastapi_users import fastapi_users
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Auth"]
)
# костыль нужно верификацию добавить
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend, requires_verification=False),
    prefix="/auth/jwt",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)

router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
)