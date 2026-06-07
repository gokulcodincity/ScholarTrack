import os
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    require_admin
)

from app.schemas.decision_schema import (
    DecisionCreate,
    DecisionUpdate,
    DecisionResponse
)

from app.models.user import User
from app.schemas.user_schema import UserResponseSchema
from app.models.reviewer_request import ReviewerRequest
from app.schemas.reviewer_request_schema import ReviewerRequestResponse

from typing import Any

from app.services.decision_service import (
    create_decision,
    get_decision_by_id,
    get_application_decision,
    get_all_decisions,
    update_decision,
    delete_decision
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post(
    "/decisions",
    response_model=DecisionResponse
)
async def create_new_decision(
    decision_data: DecisionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    decision = await create_decision(
        db,
        decision_data
    )

    if not decision:
        raise HTTPException(
            status_code=400,
            detail=(
                "Decision cannot be created. "
                "Review may not be completed, "
                "review score may not exist, "
                "or decision already exists."
            )
        )

    return decision


@router.get(
    "/decisions",
    response_model=list[DecisionResponse]
)
def get_decisions(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return get_all_decisions(db)


@router.get(
    "/decisions/{decision_id}",
    response_model=DecisionResponse
)
def get_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    decision = get_decision_by_id(
        db,
        decision_id
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.get(
    "/applications/{application_id}/decision",
    response_model=DecisionResponse
)
def get_decision_for_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    decision = get_application_decision(
        db,
        application_id
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.patch(
    "/decisions/{decision_id}",
    response_model=DecisionResponse
)
def update_existing_decision(
    decision_id: int,
    decision_data: DecisionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    decision = update_decision(
        db,
        decision_id,
        decision_data
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.delete(
    "/decisions/{decision_id}"
)
def remove_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    deleted = delete_decision(
        db,
        decision_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return {
        "message": "Decision deleted successfully"
    }

@router.get(
    "/pending-reviewers"
)
def get_pending_reviewers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Returns all pending reviewer users joined with their reviewer request details.
    """
    pending_users = db.query(User).filter(User.role == "PENDING_REVIEWER").all()
    result = []
    for user in pending_users:
        req = db.query(ReviewerRequest).filter(
            ReviewerRequest.user_id == user.id
        ).first()
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "request": {
                "university": req.university if req else None,
                "department": req.department if req else None,
                "years_of_experience": req.years_of_experience if req else None,
                "institution_email": req.institution_email if req else None,
                "resume_filename": req.resume_filename if req else None,
                "status": req.status if req else "NOT_SUBMITTED"
            }
        })
    return result

@router.get(
    "/reviewers",
    response_model=list[UserResponseSchema]
)
def get_active_reviewers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Returns all approved reviewers.
    """
    return db.query(User).filter(User.role == "REVIEWER").all()

@router.patch(
    "/users/{user_id}/approve-reviewer",
    response_model=UserResponseSchema
)
def approve_reviewer(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id, User.role == "PENDING_REVIEWER").first()
    if not user:
        raise HTTPException(status_code=404, detail="Pending reviewer not found")

    user.role = "REVIEWER"

    # Update the reviewer request status
    req = db.query(ReviewerRequest).filter(ReviewerRequest.user_id == user_id).first()
    if req:
        req.status = "APPROVED"

    db.commit()
    db.refresh(user)
    return user

@router.patch(
    "/users/{user_id}/reject-reviewer",
    response_model=UserResponseSchema
)
def reject_reviewer(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id, User.role == "PENDING_REVIEWER").first()
    if not user:
        raise HTTPException(status_code=404, detail="Pending reviewer not found")

    user.role = "STUDENT"

    # Update the reviewer request status
    req = db.query(ReviewerRequest).filter(ReviewerRequest.user_id == user_id).first()
    if req:
        req.status = "REJECTED"

    db.commit()
    db.refresh(user)
    return user


@router.get("/reviewer-requests/{user_id}/resume")
def download_reviewer_resume(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    req = db.query(ReviewerRequest).filter(ReviewerRequest.user_id == user_id).first()
    if not req or not req.resume_filename:
        raise HTTPException(status_code=404, detail="Resume not found")

    file_path = os.path.join("uploads", "resumes", req.resume_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file missing from server")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=req.resume_filename
    )