from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    get_current_user,
    require_student,
    require_reviewer,
    require_admin
)

from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationResponse,
    ReviewerAssignment,
    ApplicationDetailResponse
)

from app.schemas.reviewer_note_schema import (
    ReviewSubmission
)

from app.schemas.decision_schema import (
    DecisionCreate,
    DecisionResponse
)

from app.services.reviewer_note_service import (
    create_reviewer_note
)

from app.services.decision_service import (
    create_decision
)

from app.services.application_service import (
    create_application,
    get_application_full_details,
    get_student_applications,
    get_reviewer_applications,
    get_all_applications,
    assign_reviewer,
    submit_review
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post(
    "/",
    response_model=ApplicationResponse
)
def create_new_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_student)
):
    application = create_application(
        db,
        application_data
    )

    if not application:
        raise HTTPException(
            status_code=400,
            detail="Application already exists"
        )

    return application


@router.get(
    "/",
    response_model=list[ApplicationResponse]
)
def list_applications(
    student_id: int | None = None,
    reviewer_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if student_id:
        return get_student_applications(
            db,
            student_id
        )

    if reviewer_id:
        return get_reviewer_applications(
            db,
            reviewer_id
        )

    if current_user.get("role") == "ADMIN":
        return get_all_applications(db)

    return []


@router.get(
    "/{application_id}",
    response_model=ApplicationDetailResponse
)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    application = await get_application_full_details(
        db,
        application_id
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.get(
    "/student/{student_id}",
    response_model=list[ApplicationResponse]
)
def get_student_application_list(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_student)
):
    return get_student_applications(
        db,
        student_id
    )


@router.get(
    "/reviewer/{reviewer_id}",
    response_model=list[ApplicationResponse]
)
def get_reviewer_application_list(
    reviewer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_reviewer)
):
    return get_reviewer_applications(
        db,
        reviewer_id
    )


@router.patch(
    "/{application_id}/assign",
    response_model=ApplicationResponse
)
def assign_application_reviewer(
    application_id: int,
    reviewer_data: ReviewerAssignment,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    application = assign_reviewer(
        db,
        application_id,
        reviewer_data
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.patch(
    "/{application_id}/review",
    response_model=ApplicationResponse
)
def complete_review(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_reviewer)
):
    application = submit_review(
        db,
        application_id
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.post(
    "/{application_id}/review",
    response_model=ApplicationResponse
)
async def submit_application_review(
    application_id: int,
    review_data: ReviewSubmission,
    db: Session = Depends(get_db),
    current_user=Depends(require_reviewer)
):
    await create_reviewer_note(
        application_id,
        review_data.reviewer_notes,
        review_data.score,
        review_data.scoring_rationale
    )

    application = submit_review(
        db,
        application_id
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.patch(
    "/{application_id}/decision",
    response_model=DecisionResponse
)
async def record_application_decision(
    application_id: int,
    decision_data: DecisionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    if application_id != decision_data.application_id:
        raise HTTPException(
            status_code=400,
            detail="Application ID mismatch"
        )

    if decision_data.decided_by is None:
        decision_data.decided_by = current_user.get("id")

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