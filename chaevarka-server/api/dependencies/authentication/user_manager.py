from fastapi import Depends
from api.dependencies.authentication.users import get_user_db
from core.authentication.user_manager import UserManager


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)