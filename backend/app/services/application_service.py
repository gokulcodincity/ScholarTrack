from sqlalchemy.orm import Session

from app.models.application import Application

from app.schemas.application_schema import (
    ApplicationCreate,
    ReviewerAssignment
)

from app.utils.enums import ApplicationStatus


def create_application(
    db: Session,
    application_data: ApplicationCreate
):
    """
    Create a new scholarship application.

    Prevent duplicate applications
    for the same scholarship.
    """

    existing_application = (
        db.query(Application)
        .filter(
            Application.student_id == application_data.student_id,
            Application.scholarship_id == application_data.scholarship_id
        )
        .first()
    )

    if existing_application:
        return None

    application = Application(
        student_id=application_data.student_id,
        scholarship_id=application_data.scholarship_id,
        status=ApplicationStatus.PENDING
    )

    db.add(application)

    db.commit()

    db.refresh(application)

    return application


def get_application_by_id(
    db: Session,
    application_id: int
):
    """
    Get application by ID.
    """

    return (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )


def get_student_applications(
    db: Session,
    student_id: int
):
    """
    Get all applications
    submitted by a student.
    """

    return (
        db.query(Application)
        .filter(
            Application.student_id == student_id
        )
        .all()
    )


def get_reviewer_applications(
    db: Session,
    reviewer_id: int
):
    """
    Get all applications assigned
    to a reviewer.
    """

    return (
        db.query(Application)
        .filter(
            Application.reviewer_id == reviewer_id
        )
        .all()
    )


def assign_reviewer(
    db: Session,
    application_id: int,
    reviewer_data: ReviewerAssignment
):
    """
    Admin assigns reviewer.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return None

    application.reviewer_id = (
        reviewer_data.reviewer_id
    )

    application.status = (
        ApplicationStatus.UNDER_REVIEW
    )

    db.commit()

    db.refresh(application)

    return application


def submit_review(
    db: Session,
    application_id: int
):
    """
    Reviewer completes review.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return None

    application.review_completed = True

    db.commit()

    db.refresh(application)

    return application


def update_application_status(
    db: Session,
    application_id: int,
    status: ApplicationStatus
):
    """
    Update application status.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return None

    application.status = status

    db.commit()

    db.refresh(application)

    return application


def delete_application(
    db: Session,
    application_id: int
):
    """
    Delete application.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return False

    db.delete(application)

    db.commit()

    return True