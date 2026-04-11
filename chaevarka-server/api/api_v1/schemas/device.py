from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    device_id: str
    ip_address: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    online_at: datetime | None = None

    class Config:
        from_attributes = True