from datetime import date
from decimal import Decimal
from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Scholarship(Base):
    """
    Scholarship table

    Stores scholarship details created by admin.
    """

    __tablename__ = "scholarships"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        nullable=False
    )

    field: Mapped[str] = mapped_column(
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    eligibility: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    deadline: Mapped[date] = mapped_column(
        nullable=False
    )

    applications = relationship(
        "Application",
        back_populates="scholarship",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Scholarship(id={self.id}, "
            f"title='{self.title}', "
            f"amount={self.amount})>"
        )