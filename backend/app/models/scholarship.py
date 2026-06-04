from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import Date

from sqlalchemy.orm import relationship

from app.models.base import Base


class Scholarship(Base):
    """
    Scholarship table

    Stores scholarship details created by admin.
    """

    __tablename__ = "scholarships"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    field = Column(
        String(100),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    eligibility = Column(
        Text,
        nullable=False
    )

    deadline = Column(
        Date,
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