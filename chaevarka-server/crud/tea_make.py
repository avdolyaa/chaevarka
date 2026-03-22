from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.schemas.tea_make import TeaMakeCreate, TeaStatus
from core.models import Tea_make
from core.models import Device



async def make_tea(session: AsyncSession, tea_data: TeaMakeCreate) -> Tea_make:
    device_exists = await session.execute(select(Device).filter(Device.device_id == tea_data.device_id))
    if not device_exists.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="device wasn't found")
    tea_make = Tea_make(**tea_data.model_dump())
    session.add(tea_make)
    await session.commit()
    await session.refresh(tea_make)
    return tea_make

async def get_tea(session: AsyncSession, device_id: str) -> Tea_make | None:
    order = await session.scalar(select(Tea_make).where(Tea_make.device_id == device_id).where(Tea_make.status == 'waiting').order_by(Tea_make.id))
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


async def update_tea_status(session: AsyncSession, order_id: int, new_status: TeaStatus) -> Tea_make | None:
    order = await session.get(Tea_make, order_id)
    if order:
        order.status = new_status
        session.add(order)
        await session.commit()
        await session.refresh(order)
    return order


async def cancel_tea_order(session: AsyncSession, order_id: int) -> Tea_make | None:
    order = await session.get(Tea_make, order_id)
    if order:
        if order.status in [TeaStatus.COMPLETED, TeaStatus.FAILED]:
            return order
        order.status = TeaStatus.CANCELLED
        session.add(order)
        await session.commit()
        await session.refresh(order)
    return order