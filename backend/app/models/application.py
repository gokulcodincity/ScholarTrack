from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.utils.enums import ApplicationStatus


class Application(Base):
    """
    Applications submitted by students for scholarships.
    """

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False
    )

    scholarship_id: Mapped[int] = mapped_column(
        ForeignKey("scholarships.id"),
        nullable=False
    )

    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False
    )

    review_completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    scholarship = relationship(
        "Scholarship",
        back_populates="applications"
    )

    decision = relationship(
        "Decision",
        back_populates="application",
        uselist=False
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "scholarship_id",
            name="uq_student_scholarship"
        ),
    )

    def __repr__(self):
        return (
            f"<Application("
            f"id={self.id}, "
            f"student_id={self.student_id}, "
            f"scholarship_id={self.scholarship_id}, "
            f"status={self.status}"
            f")>"
        )