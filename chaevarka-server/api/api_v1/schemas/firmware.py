from pydantic import BaseModel

class FirmwareCheckResponse(BaseModel):
    version: str
    download_url: str

class FirmwareCreate(BaseModel):
    version: str
    device_prefix: str