import asyncio
import contextlib

from api.api_v1.schemas.user import UserCreate
from api.dependencies.authentication import get_user_db
from api.dependencies.authentication import get_user_manager
from core.authentication.user_manager import UserManager
from core.models import User, db_helper
from core.config import settings
get_users_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = settings.superuser_email
default_password = settings.superuser_password
default_first_name = settings.superuser_first_name
default_last_name = settings.superuser_last_name
default_phone = settings.superuser_phone
default_is_active = True
default_is_superuser = True
default_is_verified = True

async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
        email: str = default_email,
        password: str = default_password,
        first_name: str = default_first_name,
        last_name: str = default_last_name,
        phone: str = default_phone,
        is_active: bool = default_is_active,
        is_superuser: bool = default_is_superuser,
        is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


if __name__ == "__main__":
    asyncio.run(create_superuser())