from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

from app.models.application import Application
from app.models.decision import Decision
from app.models.essay import Essay
from app.models.reviewer_note import ReviewerNote

from app.schemas.application_schema import (
    ApplicationCreate,
    ReviewerAssignment,
    ApplicationDetailResponse
)

from app.utils.enums import ApplicationStatus


def create_application(
    db: Session,
    application_data: ApplicationCreate
):
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
    try:
        db.commit()
        db.refresh(application)
    except Exception:
        db.rollback()
        raise

    return application


def get_application_by_id(
    db: Session,
    application_id: int
):
    return (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )


async def get_application_full_details(
    db: Session,
    application_id: int,
    current_user_role: str
):
    application = await run_in_threadpool(
        lambda: db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        return None

    essay = await Essay.find_one(
        Essay.application_id == application_id
    )

    reviewer_note = await ReviewerNote.find_one(
        ReviewerNote.application_id == application_id
    )

    decision = await run_in_threadpool(
        lambda: db.query(Decision)
        .filter(Decision.application_id == application_id)
        .first()
    )

    decision_recorded = decision is not None

    # Only hide the reviewer note from students if the final decision hasn't been made yet.
    # Admins and Reviewers need to see the note to make the decision!
    if not decision_recorded and current_user_role == "STUDENT":
        reviewer_note = None

    return ApplicationDetailResponse(
        application={
            "id": application.id,
            "student_id": application.student_id,
            "scholarship_id": application.scholarship_id,
            "reviewer_id": application.reviewer_id,
            "status": application.status.value,
            "review_completed": application.review_completed,
            "created_at": str(application.created_at),
            "student_name": application.student_name,
            "reviewer_name": application.reviewer_name
        },
        essay=(
            {
                "essay": essay.essay,
                "supporting_content": essay.supporting_content
            }
            if essay else None
        ),
        reviewer_note=(
            {
                "reviewer_notes": reviewer_note.reviewer_notes,
                "score": reviewer_note.score,
                "scoring_rationale": reviewer_note.scoring_rationale
            }
            if reviewer_note else None
        ),
        decision_recorded=decision_recorded,
        decision=(
            {
                "id": decision.id,
                "decision_status": decision.decision_status.value
            }
            if decision else None
        )
    )


def get_student_applications(
    db: Session,
    student_id: int,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(Application)
        .filter(
            Application.student_id == student_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_applications(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Application).offset(skip).limit(limit).all()


def get_reviewer_applications(
    db: Session,
    reviewer_id: int,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(Application)
        .filter(
            Application.reviewer_id == reviewer_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def assign_reviewer(
    db: Session,
    application_id: int,
    reviewer_data: ReviewerAssignment
):
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return None

    application.reviewer_id = reviewer_data.reviewer_id
    application.status = ApplicationStatus.UNDER_REVIEW

    try:
        db.commit()
        db.refresh(application)
    except Exception:
        db.rollback()
        raise

    return application


def submit_review(
    db: Session,
    application_id: int
):
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
    application.status = ApplicationStatus.REVIEW_DONE

    try:
        db.commit()
        db.refresh(application)
    except Exception:
        db.rollback()
        raise

    return application


def update_application_status(
    db: Session,
    application_id: int,
    status: ApplicationStatus
):
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

    try:
        db.commit()
        db.refresh(application)
    except Exception:
        db.rollback()
        raise

    return application


def delete_application(
    db: Session,
    application_id: int
):
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
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return True