from fastapi import Depends, BackgroundTasks
from api.dependencies.authentication.users import get_user_db
from core.authentication.user_manager import UserManager


async def get_user_manager(
    user_db=Depends(get_user_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    yield UserManager(user_db, background_tasks=background_tasks)