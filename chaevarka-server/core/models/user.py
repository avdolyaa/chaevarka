from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)