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
   temperature: Mapped[int] = mapped_column(Integer, nullable=False)
   sugar: Mapped[int] = mapped_column()
   type: Mapped[int] = mapped_column()
   time: Mapped[int] = mapped_column()
   tea_cnt: Mapped[int] = mapped_column()
   status: Mapped[str] = mapped_column(default='waiting')
   created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

