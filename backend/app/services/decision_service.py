from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.decision import Decision
from app.models.reviewer_note import ReviewerNote

from app.schemas.decision_schema import (
    DecisionCreate,
    DecisionUpdate
)


async def create_decision(
    db: Session,
    decision_data: DecisionCreate
):
    """
    Create final decision for an application.

    Business Rules:
    1. Application must exist.
    2. Review must be completed.
    3. Review score must exist.
    4. Only one decision per application.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == decision_data.application_id
        )
        .first()
    )

    if not application:
        return None

    if not application.review_completed:
        return None

    review_note = await ReviewerNote.find_one(
        ReviewerNote.application_id
        == decision_data.application_id
    )

    if not review_note:
        return None

    if review_note.score is None:
        return None

    existing_decision = (
        db.query(Decision)
        .filter(
            Decision.application_id
            == decision_data.application_id
        )
        .first()
    )

    if existing_decision:
        return None

    decision = Decision(
        application_id=decision_data.application_id,
        decision_status=decision_data.decision_status,
        decided_by=decision_data.decided_by
    )

    db.add(decision)

    db.commit()

    db.refresh(decision)

    return decision


def get_decision_by_id(
    db: Session,
    decision_id: int
):
    return (
        db.query(Decision)
        .filter(
            Decision.id == decision_id
        )
        .first()
    )


def get_application_decision(
    db: Session,
    application_id: int
):
    return (
        db.query(Decision)
        .filter(
            Decision.application_id
            == application_id
        )
        .first()
    )


def get_all_decisions(
    db: Session
):
    return (
        db.query(Decision)
        .all()
    )


def update_decision(
    db: Session,
    decision_id: int,
    decision_data: DecisionUpdate
):
    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id
        )
        .first()
    )

    if not decision:
        return None

    decision.decision_status = (
        decision_data.decision_status
    )

    db.commit()

    db.refresh(decision)

    return decision


def delete_decision(
    db: Session,
    decision_id: int
):
    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id
        )
        .first()
    )

    if not decision:
        return False

    db.delete(decision)

    db.commit()

    return True