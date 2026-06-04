from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Student(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    department: Mapped[str | None] = mapped_column()

    cgpa: Mapped[float | None] = mapped_column()

    academic_year: Mapped[str | None] = mapped_column()