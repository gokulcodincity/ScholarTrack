from pydantic import BaseModel


class ReviewerNoteCreate(BaseModel):

    application_id: int

    reviewer_notes: str

    score: int

    scoring_rationale: str | None = None


class ReviewerNoteResponse(BaseModel):

    id: str

    application_id: int

    reviewer_notes: str

    score: int

    scoring_rationale: str | None = None


class ReviewSubmission(BaseModel):

    reviewer_notes: str

    score: int

    scoring_rationale: str | None = None