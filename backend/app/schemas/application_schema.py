from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from app.utils.enums import ApplicationStatus


class ApplicationCreate(BaseModel):
    """
    Student applies for a scholarship.
    """

    student_id: int
    scholarship_id: int


class ApplicationResponse(BaseModel):
    """
    Application details returned to client.
    """

    id: int
    student_id: int
    scholarship_id: int
    reviewer_id: int | None = None

    status: ApplicationStatus

    review_completed: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ReviewerAssignment(BaseModel):
    """
    Admin assigns reviewer.
    """

    reviewer_id: int


class ApplicationStatusUpdate(BaseModel):
    """
    Reviewer updates application status.
    """

    status: ApplicationStatus


class ApplicationListResponse(BaseModel):
    """
    Used when listing applications.
    """

    id: int

    student_id: int

    scholarship_id: int

    reviewer_id: int | None = None

    status: ApplicationStatus

    review_completed: bool

    model_config = ConfigDict(
        from_attributes=True
    )