from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class TeaStatus(str, Enum):
   WAITING = "waiting"
   IN_PROGRESS = "in_progress"
   BOILING = "boiling"
   DOSING = "dosing"
   BREWING = "brewing"
   COMPLETED = "completed"
   FAILED = "failed"
   CANCELLED = "cancelled"


class TeaMakeCreate(BaseModel):
   device_id: str
   water: Annotated[int, Field(ge=50, le=300)]
   temperature: Annotated[int, Field(ge=70, le=100)]
   sugar: Annotated[int, Field(ge=0, le=5)]
   type: Annotated[int, Field(ge=0, le=6)]
   time: Annotated[int, Field(ge=0, le=5)]
   tea_cnt: Annotated[int, Field(ge=0, le=10)]

class TeaMakeResponse(TeaMakeCreate):
   id: int
   status: TeaStatus
   created_at: datetime

   class Config:
       from_attributes = True


class TeaStatusUpdate(BaseModel):
   status: TeaStatus
   @field_validator('status', mode='before')
   @classmethod
   def lowercase_status(cls, v):
      if isinstance(v, str):
         return v.lower()
      return v
