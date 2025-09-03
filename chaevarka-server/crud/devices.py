from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Device


async def get_ip_address(session: AsyncSession, device_id: str) -> Device | None:
    device = await session.scalar(select(Device).where(Device.device_id==device_id))
    return device

async def update_device_ip(session: AsyncSession, ip_address: str, device_id: str) -> Device:
    device = await session.scalar(select(Device).where(Device.device_id==device_id))
    if device:
        device.ip_address = ip_address
    else:
        device = Device(ip_address=ip_address, device_id=device_id)
        session.add(device)
    await session.commit()
    await session.refresh(device)
    return device