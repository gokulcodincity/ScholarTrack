from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.application_service import get_application_by_id

from app.middleware.auth_middleware import (
    get_current_user,
    require_student
)

from app.schemas.essay_schema import (
    EssayCreate,
    EssayResponse
)

from app.services.essay_service import (
    create_essay,
    get_essay
)

router = APIRouter(
    prefix="/essays",
    tags=["Essays"]
)


@router.post("/", response_model=EssayResponse)
async def add_essay(
    essay_data: EssayCreate,
    current_user: dict = Depends(require_student)
):

    return await create_essay(
        essay_data.application_id,
        essay_data.essay,
        essay_data.supporting_content
    )


@router.get("/{application_id}", response_model=EssayResponse)
async def fetch_essay(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    application = await run_in_threadpool(get_application_by_id, db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    role = current_user.get("role", "").upper()
    user_id = current_user.get("id")

    if role == "STUDENT" and application.student_id != user_id:
        raise HTTPException(status_code=403, detail="You can only view your own essays")
    elif role == "REVIEWER" and application.reviewer_id != user_id:
        raise HTTPException(status_code=403, detail="This application is not assigned to you")

    return await get_essay(
        application_id
    )