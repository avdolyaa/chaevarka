from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.schemas.tea_make import TeaMakeCreate
from core.models import Tea_make


async def make_tea(session: AsyncSession, tea_data: TeaMakeCreate) -> Tea_make:
    tea_make = Tea_make(**tea_data.model_dump())
    session.add(tea_make)
    await session.commit()
    await session.refresh(tea_make)
    return tea_make

async def get_tea(session: AsyncSession, device_id: str) -> Tea_make | None:
    order = await session.scalar(select(Tea_make).where(Tea_make.device_id == device_id).where(Tea_make.status == 'waiting').order_by(Tea_make.id))
    if order:
        order.status = 'in_progress'
        session.add(order)
        await session.commit()
        await session.refresh(order)
    return order

async def post_tea_ready(session: AsyncSession, order_id: int) -> Tea_make | None:
    order_ready = await session.scalar(select(Tea_make).where(Tea_make.id == order_id))
    if order_ready:
        order_ready.status = 'completed'
        session.add(order_ready)
        await session.commit()
        await session.refresh(order_ready)
    return order_ready

async def get_tea_ready(session: AsyncSession, order_id: int) -> Tea_make:
    order = await session.scalar(select(Tea_make).where(Tea_make.id == order_id))
    return order