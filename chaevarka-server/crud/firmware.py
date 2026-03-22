from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Firmware

async def get_latest_firmware(session: AsyncSession, device_id: str) -> Firmware | None:
    prefix = device_id[:3]
    stmt = (
        select(Firmware)
        .where(Firmware.device_prefix == prefix)
        .order_by(Firmware.version.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_firmware_by_id(session: AsyncSession, firmware_id: int) -> Firmware | None:
    return await session.get(Firmware, firmware_id)