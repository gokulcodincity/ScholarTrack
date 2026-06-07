from pydantic import BaseModel
from app.utils.sanitization import SanitizedStr
from beanie import PydanticObjectId


class ReviewerNoteCreate(BaseModel):

    application_id: int

    reviewer_notes: SanitizedStr

    score: int

    scoring_rationale: SanitizedStr | None = None


class ReviewerNoteResponse(BaseModel):

    id: PydanticObjectId

    application_id: int

    reviewer_notes: str

    score: int

    scoring_rationale: str | None = None


class ReviewSubmission(BaseModel):

    reviewer_notes: SanitizedStr

    score: int

    scoring_rationale: SanitizedStr | None = None