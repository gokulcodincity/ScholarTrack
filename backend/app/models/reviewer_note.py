from beanie import Document


class ReviewerNote(Document):

    application_id: int

    reviewer_notes: str

    score: int

    class Settings:
        name = "reviewer_notes"