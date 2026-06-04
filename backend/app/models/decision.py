from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Enum

from sqlalchemy.orm import relationship

from app.models.base import Base
from app.utils.enums import DecisionStatus


class Decision(Base):
    """
    Final decision made by admin for an application.
    """

    __tablename__ = "decisions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    application_id = Column(
        Integer,
        ForeignKey("applications.id"),
        nullable=False,
        unique=True
    )

    decision_status = Column(
        Enum(DecisionStatus),
        nullable=False
    )

    decided_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    decided_at = Column(
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