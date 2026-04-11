from typing import Optional

from fastapi_users import schemas
from pydantic import ConfigDict, Field


class UserRead(schemas.BaseUser[int]):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    phone: Optional[str] = None
    profile_picture: Optional[str] = Field(None, alias="profilePicture")
    device_id: Optional[str] = Field(None, alias="deviceId")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    model_config = ConfigDict(populate_by_name=True)


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    phone: Optional[str] = None
    profile_picture: Optional[str] = Field(None, alias="profilePicture")
    device_id: Optional[str] = Field(None, alias="deviceId")