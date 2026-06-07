from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models.base import Base


class ReviewerRequest(Base):

    __tablename__ = "reviewer_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    university: Mapped[str] = mapped_column(nullable=False)

    department: Mapped[str] = mapped_column(nullable=False)

    years_of_experience: Mapped[int] = mapped_column(nullable=False)

    institution_email: Mapped[str] = mapped_column(nullable=False)

    # Stored filename of the uploaded resume
    resume_filename: Mapped[str | None] = mapped_column(nullable=True)

    # status: PENDING, APPROVED, REJECTED
    status: Mapped[str] = mapped_column(nullable=False, default="PENDING")
