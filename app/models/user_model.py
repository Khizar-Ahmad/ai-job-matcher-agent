from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    password: Mapped[str] = mapped_column(String(255))

    desired_job_title: Mapped[str] = mapped_column(String(255))

    job_preferences: Mapped[str] = mapped_column(Text)

    skills: Mapped[str] = mapped_column(Text)

    experience_level: Mapped[str] = mapped_column(String(100))