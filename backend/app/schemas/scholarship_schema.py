from datetime import date
from pydantic import BaseModel
from pydantic import Field


class ScholarshipCreate(BaseModel):
    """
    Schema for creating a scholarship.
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    field: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    amount: float = Field(
        ...,
        gt=0
    )

    eligibility: str = Field(
        ...,
        min_length=10
    )

    deadline: date


class ScholarshipUpdate(BaseModel):
    """
    Schema for updating scholarship details.
    All fields are optional.
    """

    title: str | None = None

    field: str | None = None

    amount: float | None = None

    eligibility: str | None = None

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

    class Config:
        from_attributes = True