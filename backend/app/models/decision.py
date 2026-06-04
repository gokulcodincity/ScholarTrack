from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.utils.enums import DecisionStatus


class Decision(Base):
    """
    Final decision made by admin for an application.
    """

    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
        unique=True
    )

    decision_status: Mapped[DecisionStatus] = mapped_column(
        Enum(DecisionStatus),
        nullable=False
    )

    decided_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    decided_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    application = relationship(
        "Application",
        back_populates="decision"
    )

    def __repr__(self):
        return (
            f"<Decision("
            f"id={self.id}, "
            f"application_id={self.application_id}, "
            f"decision_status={self.decision_status}"
            f")>"
        )