from app.models.reviewer_note import ReviewerNote


async def create_reviewer_note(
    application_id: int,
    reviewer_notes: str,
    score: int
):

    note = ReviewerNote(
        application_id=application_id,
        reviewer_notes=reviewer_notes,
        score=score
    )

    await note.insert()

    return note


async def get_reviewer_note(
    application_id: int
):

    return await ReviewerNote.find_one(
        ReviewerNote.application_id == application_id
    )