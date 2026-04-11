import os
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File, Form, HTTPException
from starlette import status
from starlette.responses import FileResponse

from api.api_v1.schemas.firmware import FirmwareCheckResponse
from api.dependencies.authentication.auth import current_superuser
from fastapi import APIRouter, Depends
from core.models import db_helper, Firmware

from core.config import settings
from crud.firmware import get_latest_firmware, get_firmware_by_id

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Firmwares"],
)

@router.post("/upload", dependencies=[Depends(current_superuser)])
async def upload_firmware(
    version: str = Form(...),
    device_prefix: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    file_location = f"uploads/{device_prefix}_{version}.bin"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    new_firmware = Firmware(
        version=version,
        device_prefix=device_prefix,
        file_path=file_location
    )
    session.add(new_firmware)
    await session.commit()
    return {"message": "Firmware uploaded successfully"}


@router.get("/devices/{device_id}/check-update", response_model=FirmwareCheckResponse)
async def check_update(device_id: str, session: AsyncSession = Depends(db_helper.session_getter)):
    firmware = await get_latest_firmware(session, device_id)
    if not firmware:
        raise HTTPException(status_code=404, detail="No firmware found for this device type")

    return FirmwareCheckResponse(
        version=firmware.version,
        download_url=f"/api/v1/devices/firmware/download/{firmware.id}"
    )

@router.get("/devices/firmware/download/{firmware_id}")
async def download_firmware(firmware_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    firmware = await get_firmware_by_id(session=session, firmware_id=firmware_id)
    if not firmware or not os.path.exists(firmware.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Firmware file not found"
        )
    return FileResponse(
        path=firmware.file_path,
        filename=f"update_v{firmware.version}.bin",
    )
