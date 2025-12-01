from fastapi import APIRouter, Depends
from sqlalchemy import text
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Health"]
)


@router.get("/ping")
async def ping():
    return {
        "status": "ok",
        "message": "pong"
    }


@router.get("/health")
async def health_bd(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }

