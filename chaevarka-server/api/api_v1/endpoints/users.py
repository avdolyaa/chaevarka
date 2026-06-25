from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.schemas.user import UserRead, UserUpdate
from api.dependencies.authentication.fastapi_users import fastapi_users
from api.dependencies.authentication.auth import current_active_user
from api.dependencies.authentication.user_manager import get_user_manager
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Users"]
)


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user=Depends(current_active_user),
    user_manager=Depends(get_user_manager),
):
    await user_manager.delete(current_user)


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
