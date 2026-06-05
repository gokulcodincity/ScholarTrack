from fastapi import APIRouter, Depends, HTTPException, status

from app.middleware.auth_middleware import (
    get_current_user,
    require_reviewer
)

from app.schemas.reviewer_note_schema import (
    ReviewerNoteCreate
)

from app.services.reviewer_note_service import (
    create_reviewer_note,
    get_reviewer_note
)

router = APIRouter(
    prefix="/reviewer-notes",
    tags=["Reviewer Notes"]
)


def require_reviewer_or_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") not in ["REVIEWER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reviewer or Admin access required"
        )
    return current_user


@router.post("/")
async def add_note(
    note_data: ReviewerNoteCreate,
    current_user: dict = Depends(require_reviewer)
):

    return await create_reviewer_note(
        note_data.application_id,
        note_data.reviewer_notes,
        note_data.score,
        note_data.scoring_rationale
    )


@router.get("/{application_id}")
async def fetch_note(
    application_id: int,
    current_user: dict = Depends(require_reviewer_or_admin)
):

    return await get_reviewer_note(
        application_id
    )