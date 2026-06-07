from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from app.utils.enums import ApplicationStatus


class ApplicationCreate(BaseModel):
    student_id: int
    scholarship_id: int


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    scholarship_id: int
    reviewer_id: int | None = None

    status: ApplicationStatus

    review_completed: bool

    created_at: datetime

    student_name: str | None = None

    reviewer_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class ReviewerAssignment(BaseModel):
    reviewer_id: int


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationListResponse(BaseModel):
    id: int

    student_id: int

    scholarship_id: int

    reviewer_id: int | None = None

    status: ApplicationStatus

    review_completed: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ApplicationDetailResponse(BaseModel):
    application: dict

    essay: dict | None = None

    reviewer_note: dict | None = None

    decision_recorded: bool

    decision: dict | None = None