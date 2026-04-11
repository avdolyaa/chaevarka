from sqlalchemy import Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import(
   Mapped,
   mapped_column
)
from .base import Base

class Recipe(Base):
    __tablename__ = "recipes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(default="")
    type: Mapped[str] = mapped_column(String(50), default="black")  # ???
    icon: Mapped[str | None] = mapped_column(Text, nullable=True)

    water_amount: Mapped[int] = mapped_column(Integer, default=300)
    temperature: Mapped[int] = mapped_column(Integer, default=95)
    time: Mapped[int] = mapped_column(default=3)
    tea_amount: Mapped[int] = mapped_column()

    drum_1: Mapped[int] = mapped_column(default=0)
    drum_2: Mapped[int] = mapped_column(default=0)
    drum_3: Mapped[int] = mapped_column(default=0)
    drum_4: Mapped[int] = mapped_column(default=0)
    drum_5: Mapped[int] = mapped_column(default=0)
    drum_6: Mapped[int] = mapped_column(default=0)

    is_public: Mapped[bool] = mapped_column(Boolean, default=False)  # ???