from typing import Optional

from fastapi_users import schemas
from pydantic import ConfigDict, Field


class UserRead(schemas.BaseUser[int]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    device_id: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    device_id: Optional[str] = None