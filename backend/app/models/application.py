from datetime import datetime, timezone

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
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    scholarship_id: Mapped[int] = mapped_column(
        ForeignKey("scholarships.id"),
        nullable=False,
        index=True
    )

    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
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
        default=lambda: datetime.now(timezone.utc),
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

    student = relationship(
        "User",
        foreign_keys=[student_id]
    )

    reviewer = relationship(
        "User",
        foreign_keys=[reviewer_id]
    )

    @property
    def student_name(self) -> str | None:
        return self.student.name if self.student else None

    @property
    def reviewer_name(self) -> str | None:
        return self.reviewer.name if self.reviewer else None

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