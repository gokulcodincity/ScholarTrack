from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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
    ReviewerAssignment
)

from app.services.application_service import (
    create_application,
    get_application_by_id,
    get_student_applications,
    get_reviewer_applications,
    assign_reviewer,
    submit_review,
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
    """
    Student applies for a scholarship.
    """

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
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get application by ID.
    """

    application = get_application_by_id(
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
    """
    Get all applications of a student.
    """

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
    """
    Get all applications assigned to reviewer.
    """

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
    """
    Admin assigns reviewer.
    """

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
    """
    Reviewer marks review as completed.
    """

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