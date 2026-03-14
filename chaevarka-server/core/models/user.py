from fastapi_users.db import SQLAlchemyBaseUserTable
from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass