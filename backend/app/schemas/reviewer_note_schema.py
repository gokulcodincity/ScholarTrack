from pydantic import BaseModel


class ReviewerNoteCreate(BaseModel):

    application_id: int

    reviewer_notes: str

    score: int


class ReviewerNoteResponse(BaseModel):

    id: str

    application_id: int

    reviewer_notes: str

    score: int