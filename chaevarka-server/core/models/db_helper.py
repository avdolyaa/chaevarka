from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings

class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
    async def dispose(self) -> None:
        await self.engine.dispose()

db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
