from datetime import datetime
from sqlalchemy import Integer


from sqlalchemy.orm import(
   Mapped,
   mapped_column
)

from .base import Base
class Tea_make(Base):
   __tablename__ = "tea_make"
   device_id: Mapped[str] = mapped_column()
   water: Mapped[int] = mapped_column(Integer, nullable=False)
   water_for_cup: Mapped[int] = mapped_column(default=300)
   temperature: Mapped[int] = mapped_column(Integer, nullable=False)
   drum_1: Mapped[int] = mapped_column(default=0)
   drum_2: Mapped[int] = mapped_column(default=0)
   drum_3: Mapped[int] = mapped_column(default=0)
   drum_4: Mapped[int] = mapped_column(default=0)
   drum_5: Mapped[int] = mapped_column(default=0)
   drum_6: Mapped[int] = mapped_column(default=0)
   type: Mapped[int] = mapped_column()
   time: Mapped[int] = mapped_column()
   tea_cnt: Mapped[int] = mapped_column()
   status: Mapped[str] = mapped_column(default='waiting')
   created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Drum_config(Base):
   __tablename__ = "drum_config"
   ingredient_name: Mapped[str] = mapped_column(nullable=False, default="Empty")
