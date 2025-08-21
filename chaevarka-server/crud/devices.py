from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Device


async def get_ip_address(session: AsyncSession) -> str | None:
    device = await session.scalar(select(Device))
    return device.ip_address if device else None

async def update_device_ip(session: AsyncSession, ip_address: str) -> Device:
    device = await session.scalar(select(Device))
    if device:
        device.ip_address = ip_address
    else:
        device = Device(ip_address=ip_address)
        session.add(device)
    await session.commit()
    await session.refresh(device)
    return device