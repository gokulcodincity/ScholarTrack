from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import relationship

from app.models.base import Base
from app.utils.enums import ApplicationStatus


class Application(Base):
    """
    Applications submitted by students for scholarships.
    """

    __tablename__ = "applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    scholarship_id = Column(
        Integer,
        ForeignKey("scholarships.id"),
        nullable=False
    )

    reviewer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False
    )

    review_completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
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