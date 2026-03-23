from fastapi import APIRouter, Depends
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.schemas.tea_make import DrumConfigSchema
from api.dependencies.authentication.auth import current_superuser
from core.config import settings
from core.models import db_helper
from core.models.tea_make import Drum_config



router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Drums"],
)


@router.get("/drums/config", response_model=list[DrumConfigSchema])
async def get_all_drum_configs(session: AsyncSession = Depends(db_helper.session_getter)):
    result = await session.execute(select(Drum_config).order_by(Drum_config.id))
    return result.scalars().all()


@router.post("/drums/config", dependencies=[Depends(current_superuser)])
async def update_drum_config(
        data: DrumConfigSchema,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    drum = await session.get(Drum_config, data.id)
    if drum:
        drum.ingredient_name = data.ingredient_name
    else:
        drum = Drum_config(**data.model_dump())
        session.add(drum)

    await session.commit()
    return {"status": "success", "updated": data.id}