from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Firmware(Base):
    __tablename__ = "firmware"
    version: Mapped[str] = mapped_column(unique=True)
    device_prefix: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()

