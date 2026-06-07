from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict
from app.utils.sanitization import SanitizedStr


class ScholarshipCreate(BaseModel):
    """
    Schema for creating a scholarship.
    """

    title: SanitizedStr = Field(
        ...,
        min_length=3,
        max_length=255
    )

    field: SanitizedStr = Field(
        ...,
        min_length=2,
        max_length=100
    )

    amount: float = Field(
        ...,
        gt=0
    )

    eligibility: SanitizedStr = Field(
        ...,
        min_length=10
    )

    deadline: date


class ScholarshipUpdate(BaseModel):
    """
    Schema for updating scholarship details.
    """

    title: SanitizedStr | None = None
    field: SanitizedStr | None = None
    amount: float | None = None
    eligibility: SanitizedStr | None = None
    deadline: date | None = None


class ScholarshipResponse(BaseModel):
    """
    Schema returned to client.
    """

    id: int
    title: str
    field: str
    amount: float
    eligibility: str
    deadline: date

    model_config = ConfigDict(
        from_attributes=True
    )


class ScholarshipStatsResponse(BaseModel):
    """
    Scholarship statistics response.
    """

    scholarship_id: int
    total_applied: int
    shortlisted: int
    awarded: int