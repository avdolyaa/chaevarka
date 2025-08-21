from pydantic import BaseModel


class DeviceIP(BaseModel):
    ip_address: str | None