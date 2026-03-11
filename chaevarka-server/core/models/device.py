from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base
class Device(Base):
    __tablename__ = "devices"
    device_id: Mapped[str] = mapped_column(unique=True)
    ip_address: Mapped[str] = mapped_column()
    online_at: Mapped[datetime] = mapped_column(nullable=False)