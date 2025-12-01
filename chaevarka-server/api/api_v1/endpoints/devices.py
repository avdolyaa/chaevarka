from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.schemas.device import DeviceIP
from core.config import settings
from core.models import db_helper
from crud.devices import get_ip_address, update_device_ip


router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Devices"]
)


@router.get("/devices/{device_id}", response_model=DeviceIP)
async def get_ip(device_id: str, session: AsyncSession = Depends(db_helper.session_getter)):
    device = await get_ip_address(session=session, device_id=device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return DeviceIP(ip_address=device.ip_address, device_id=device.device_id)


@router.post("/devices", response_model=DeviceIP)
async def register_device(
    device_ip: DeviceIP,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    device = await update_device_ip(session=session, ip_address=device_ip.ip_address, device_id=device_ip.device_id)
    return device

@router.delete("/devices")
async def clear_all_devices(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await session.execute(text("DELETE FROM devices"))
        await session.commit()
        return {"message": "Deleted all devices"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

