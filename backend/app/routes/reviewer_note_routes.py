from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.application_service import get_application_by_id

from app.middleware.auth_middleware import (
    get_current_user,
    require_reviewer
)

from app.schemas.reviewer_note_schema import (
    ReviewerNoteCreate,
    ReviewerNoteResponse
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


@router.post("/", response_model=ReviewerNoteResponse)
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


@router.get("/{application_id}", response_model=ReviewerNoteResponse)
async def fetch_note(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_reviewer_or_admin)
):
    application = await run_in_threadpool(get_application_by_id, db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if current_user.get("role") == "REVIEWER" and application.reviewer_id != current_user.get("id"):
        raise HTTPException(status_code=403, detail="This application is not assigned to you")

    return await get_reviewer_note(
        application_id
    )