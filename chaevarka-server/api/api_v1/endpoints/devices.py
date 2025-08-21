from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.schemas.device import DeviceIP
from core.config import settings
from core.models import db_helper
from crud.devices import get_ip_address, update_device_ip


router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Devices"]
)


@router.get("", response_model=DeviceIP)
async def get_ip(session: AsyncSession = Depends(db_helper.session_getter)):
    ip = await get_ip_address(session=session)
    return DeviceIP(ip_address=ip)


@router.post("", response_model=DeviceIP)
async def register_device(
    device_ip: DeviceIP,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    device = await update_device_ip(session, device_ip.ip_address)
    return DeviceIP(ip_address=device.ip_address)